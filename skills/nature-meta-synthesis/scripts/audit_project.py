"""Check evidence structure, not scientific validity. Standard library only; no files changed."""
from pathlib import Path
import argparse
import csv
import json
import sys

FILES = ('search-log', 'screening-log', 'study-register', 'appraisal', 'evidence-units',
         'codebook', 'theme-evidence', 'relations', 'claim-ledger', 'audit-log')
OPTIONAL = ('corpus-register', 'code-assignments', 'revision-log', 'sensitivity-checks',
            'reference-checks', 'draft-claim-map')
KEYS = {'search-log': 'search_id', 'appraisal': 'appraisal_id', 'evidence-units': 'evidence_id',
        'codebook': 'code_id', 'theme-evidence': 'mapping_id', 'relations': 'relation_id',
        'claim-ledger': 'claim_id', 'audit-log': 'log_id'}
KEYS.update({'corpus-register': 'report_id', 'code-assignments': 'assignment_id',
             'revision-log': 'revision_id', 'sensitivity-checks': 'check_id',
             'reference-checks': 'reference_id', 'draft-claim-map': 'draft_id'})
MINIMUM = {
    'study-register': ('report_id', 'study_id', 'inclusion_status', 'human_review_status'),
    'evidence-units': ('evidence_id', 'study_id', 'report_id', 'source_path', 'pdf_page', 'print_page',
                       'location', 'original_text', 'code_ids', 'human_review_status'),
    'theme-evidence': ('mapping_id', 'theme_id', 'evidence_id', 'code_ids', 'human_review_status'),
    'relations': ('relation_id', 'supporting_evidence_ids', 'counter_evidence_ids',
                  'independent_study_count', 'human_review_status'),
    'claim-ledger': ('claim_id', 'claim_type', 'supporting_evidence_ids', 'counter_evidence_ids',
                     'human_review_status'),
}
MINIMUM.update({'corpus-register': ('report_id', 'corpus_role', 'independence_status'),
                'code-assignments': ('assignment_id', 'evidence_id', 'code_id', 'assignment_status'),
                'revision-log': ('revision_id', 'table', 'row_id', 'reason'),
                'sensitivity-checks': ('check_id', 'relation_id', 'criterion'),
                'reference-checks': ('reference_id', 'title', 'primary_source'),
                'draft-claim-map': ('draft_id', 'manuscript_version', 'evidence_ids')})
STATUS_FIELDS = {'codebook': 'code_status', 'theme-evidence': 'mapping_status',
                 'code-assignments': 'assignment_status', 'relations': 'relation_status',
                 'claim-ledger': 'claim_status'}


def is_active(name, row):
    return row.get(STATUS_FIELDS.get(name, ''), '').lower() not in {'retired', 'superseded'}


def split_ids(value):
    return [part.strip() for part in (value or '').split(';') if part.strip()]


def audit(root):
    root = Path(root).expanduser().resolve()
    data = root / 'data'
    issues, warnings, tables = [], [], {}
    for name in FILES + OPTIONAL:
        path = data / (name + '.csv')
        if not path.is_file():
            if name in FILES:
                issues.append(f'Missing table: {name}.csv')
            tables[name] = []
            continue
        try:
            with path.open(encoding='utf-8-sig', newline='') as handle:
                reader = csv.DictReader(handle)
                fields = reader.fieldnames or []
                missing = set(MINIMUM.get(name, ())) - set(fields)
                if name in KEYS and KEYS[name] not in fields:
                    missing.add(KEYS[name])
                if missing:
                    issues.append(f'{name}: missing fields {sorted(missing)}')
                rows = []
                for line, row in enumerate(reader, 2):
                    if None in row or any(value is None for value in row.values()):
                        issues.append(f'{name} line {line}: malformed CSV row')
                    normalized = {k: (v or '').strip() for k, v in row.items() if k is not None}
                    if any(normalized.values()):
                        rows.append(normalized)
                tables[name] = rows
        except (OSError, UnicodeError, csv.Error) as exc:
            issues.append(f'{name}: cannot read CSV: {exc}')
            tables[name] = []
    for name, key in KEYS.items():
        seen = set()
        for row in tables[name]:
            value = row.get(key, '')
            if not value:
                issues.append(f'{name}: blank {key}')
            elif value in seen:
                issues.append(f'{name}: duplicate {key}={value}')
            seen.add(value)
    pairs = set()
    included_studies = set()
    included_pairs = set()
    pair_rows = {}
    for row in tables['study-register']:
        pair = (row.get('report_id', ''), row.get('study_id', ''))
        if not all(pair):
            issues.append('study-register: missing report_id or study_id')
        if pair in pairs:
            issues.append(f'study-register: duplicate report/study pair {pair}')
        pairs.add(pair)
        pair_rows[pair] = row
        if row.get('inclusion_status') == 'include':
            included_studies.add(pair[1])
            included_pairs.add(pair)
    reports = {pair[0] for pair in pairs if pair[0]}
    corpus = {row.get('report_id'): row for row in tables['corpus-register'] if row.get('report_id')}
    for rid, row in corpus.items():
        if rid not in reports:
            issues.append(f'corpus-register: report not in study-register {rid}')
        if row.get('corpus_role') not in {'main', 'extension', 'background', 'pending', 'excluded'}:
            issues.append(f'{rid}: invalid corpus_role={row.get("corpus_role")!r}')
        if row.get('independence_status') not in {'', 'confirmed', 'pending', 'not_applicable'}:
            issues.append(f'{rid}: invalid independence_status')
    evidence = {row.get('evidence_id'): row for row in tables['evidence-units'] if row.get('evidence_id')}
    codes = {row.get('code_id') for row in tables['codebook'] if row.get('code_id')}
    inactive_codes = {row.get('code_id') for row in tables['codebook'] if not is_active('codebook', row)}
    pending = 0
    valid_status = {'pending', 'verified', 'rejected', 'not_applicable'}
    for name, rows in tables.items():
        for row in rows:
            field = STATUS_FIELDS.get(name)
            if field and row.get(field, '').lower() not in {'', 'active', 'candidate', 'retired', 'superseded'}:
                issues.append(f'{name}: invalid {field}={row.get(field)!r}')
            if 'human_review_status' in row:
                status = row.get('human_review_status', '')
                if status not in valid_status:
                    issues.append(f'{name}: invalid human_review_status={status!r}')
                pending += status == 'pending'
            for field in ('code_ids',):
                for code in split_ids(row.get(field)):
                    if code not in codes:
                        issues.append(f'{name}: unknown code_id={code}')
                    elif name == 'theme-evidence' and is_active(name, row) and code in inactive_codes:
                        (issues if row.get('human_review_status') == 'verified' else warnings).append(f'{row.get("mapping_id")}: active mapping uses retired code {code}')
    for row in tables['evidence-units']:
        eid = row.get('evidence_id', '?')
        if (row.get('report_id'), row.get('study_id')) not in pairs:
            issues.append(f'{eid}: report/study pair missing from register')
        located = row.get('source_path') and (row.get('pdf_page') or row.get('print_page') or row.get('location'))
        if row.get('pdf_page') and (not row['pdf_page'].isdigit() or int(row['pdf_page']) < 1):
            issues.append(f'{eid}: pdf_page must be a positive page index')
        if not located or not row.get('original_text'):
            message = f'{eid}: source, locator or original text missing'
            (issues if row.get('human_review_status') == 'verified' else warnings).append(message)
    for row in tables['appraisal']:
        if (row.get('report_id'), row.get('study_id')) not in pairs:
            issues.append(f'{row.get("appraisal_id", "appraisal")}: report/study pair missing')
    for row in tables['codebook']:
        for cid in split_ids(row.get('replaced_by')):
            if cid not in codes: issues.append(f'{row.get("code_id")}: unknown replacement code {cid}')
        for eid in split_ids(row.get('evidence_ids')):
            if eid not in evidence:
                issues.append(f'{row.get("code_id")}: unknown example evidence_id={eid}')
    for row in tables['theme-evidence']:
        eid = row.get('evidence_id', '')
        if not row.get('theme_id'):
            issues.append(f'{row.get("mapping_id")}: theme_id missing')
        if eid not in evidence:
            issues.append(f'{row.get("mapping_id")}: unknown evidence_id={eid}')
        elif is_active('theme-evidence', row) and row.get('human_review_status') == 'verified' and evidence[eid].get('human_review_status') != 'verified':
            issues.append(f'{row.get("mapping_id")}: verified mapping uses unverified evidence {eid}')
        if is_active('theme-evidence', row) and eid in evidence and row.get('relation_to_theme') == 'support' and evidence[eid].get('contribution_role') == 'context_only':
            (issues if row.get('human_review_status') == 'verified' else warnings).append(f'{row.get("mapping_id")}: context-only evidence cannot be primary theme support')
    for name in ('relations', 'claim-ledger'):
        for row in tables[name]:
            label = row.get(KEYS[name], '?')
            support = split_ids(row.get('supporting_evidence_ids'))
            counter = split_ids(row.get('counter_evidence_ids'))
            known = [evidence[eid] for eid in support if eid in evidence]
            for eid in support + counter:
                if eid not in evidence:
                    issues.append(f'{label}: unknown evidence_id={eid}')
            active = is_active(name, row)
            verified = active and row.get('human_review_status') == 'verified'
            formal = name == 'relations' or row.get('claim_type') in {'synthesis_finding', 'interpretive_proposition'}
            if verified and formal and not support:
                issues.append(f'{label}: verified result has no supporting evidence')
            if verified and formal:
                for eid in support + counter:
                    if eid in evidence and evidence[eid].get('human_review_status') != 'verified':
                        issues.append(f'{label}: verified result uses unverified evidence {eid}')
                for ev in known:
                    if (ev.get('report_id'), ev.get('study_id')) not in included_pairs:
                        issues.append(f'{label}: support report/study pair is not marked included')
            if active and formal:
                scope = row.get('analysis_scope') or 'main'
                for ev in known:
                    rid = ev.get('report_id')
                    role = corpus.get(rid, {}).get('corpus_role')
                    text_layer = ev.get('unit_type')
                    reason = None
                    if ev.get('contribution_role') == 'context_only':
                        reason = 'context-only evidence used as primary support'
                    elif role == 'background' or (text_layer == 'theoretical_text' and row.get('analysis_basis') != 'theoretical_text'):
                        reason = 'background/theoretical text used as empirical support'
                    elif scope == 'main' and role and role != 'main':
                        reason = f'{role} evidence mixed into main scope'
                    if reason:
                        (issues if verified else warnings).append(f'{label}: {reason} ({ev.get("evidence_id")})')
            if active and name == 'relations' and row.get('independent_study_count'):
                count = row['independent_study_count']
                expected = len({ev.get('study_id') for ev in known if ev.get('study_id')})
                if not count.isdigit() or int(count) != expected:
                    issues.append(f'{label}: independent_study_count={count}, expected {expected} from support IDs')
                unresolved = []
                for ev in known:
                    rid = ev.get('report_id')
                    independence = corpus.get(rid, {}).get('independence_status') or pair_rows.get((rid, ev.get('study_id')), {}).get('independence_status')
                    if independence != 'confirmed': unresolved.append(rid)
                if unresolved:
                    (issues if verified else warnings).append(f'{label}: independence unconfirmed for {sorted(set(unresolved))}; count should remain blank until checked')
    assignments = {r.get('assignment_id'): r for r in tables['code-assignments']}
    for row in tables['code-assignments']:
        label = row.get('assignment_id', '?')
        if row.get('evidence_id') not in evidence or row.get('code_id') not in codes:
            issues.append(f'{label}: unknown evidence or code')
        elif is_active('code-assignments', row) and row.get('code_id') in inactive_codes:
            (issues if row.get('human_review_status') == 'verified' else warnings).append(f'{label}: active assignment uses retired code')
        if row.get('superseded_by') and row['superseded_by'] not in assignments:
            issues.append(f'{label}: unknown replacement assignment')
    relation_ids = {r.get('relation_id') for r in tables['relations']}
    claim_ids = {r.get('claim_id') for r in tables['claim-ledger']}
    for row in tables['sensitivity-checks']:
        label = row.get('check_id', '?')
        if row.get('relation_id') not in relation_ids:
            issues.append(f'{label}: unknown relation')
        removed, kept = set(split_ids(row.get('removed_report_ids'))), set(split_ids(row.get('kept_report_ids')))
        if removed & kept: issues.append(f'{label}: reports both removed and kept')
        for rid in removed | kept:
            if rid not in reports: issues.append(f'{label}: unknown report {rid}')
        for eid in split_ids(row.get('surviving_support_ids')) + split_ids(row.get('surviving_counter_ids')):
            if eid not in evidence: issues.append(f'{label}: unknown surviving evidence {eid}')
            elif evidence[eid].get('report_id') in removed: issues.append(f'{label}: surviving evidence from removed report {eid}')
    for name, fields in [('revision-log', ('source_evidence_ids',)), ('draft-claim-map', ('evidence_ids',))]:
        for row in tables[name]:
            label = row.get(KEYS[name], '?')
            for field in fields:
                for eid in split_ids(row.get(field)):
                    if eid not in evidence: issues.append(f'{label}: unknown evidence {eid}')
            if name == 'draft-claim-map':
                for cid in split_ids(row.get('claim_ids')):
                    if cid not in claim_ids: issues.append(f'{label}: unknown claim {cid}')
                for lid in split_ids(row.get('relation_ids')):
                    if lid not in relation_ids: issues.append(f'{label}: unknown relation {lid}')
    for row in tables['search-log']:
        if row.get('query_status') in {'planned', 'access_failed'} and (row.get('result_count') or row.get('exported_record_count')):
            warnings.append(f'{row.get("search_id")}: non-executed search has a result/export count; clarify basis')
    counts = {name: len(rows) for name, rows in tables.items()}
    active_counts = {name: sum(is_active(name, row) for row in rows) for name, rows in tables.items()}
    scaffold = not any(counts.values())
    status = 'ISSUES_FOUND' if issues else ('SCAFFOLD_ONLY' if scaffold else 'STRUCTURE_OK')
    return {'status': status, 'row_counts': counts, 'active_row_counts': active_counts, 'pending_human_review_rows': pending,
            'issues': issues, 'warnings': warnings,
            'limits': 'Checks structure only. Does not verify quotations, human review truth, search coverage, study independence or scientific interpretations.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    args = parser.parse_args()
    result = audit(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result['issues'] else 0


if __name__ == '__main__':
    sys.exit(main())
