"""Summarize registered project state; never infer database hits or independence."""
from collections import Counter
from pathlib import Path
import argparse
import json
from audit_project import audit, is_active, FILES, OPTIONAL


def summarize(root):
    import csv
    root = Path(root).expanduser().resolve()
    checked = audit(root)
    tables = {}
    for name in FILES + OPTIONAL:
        path = root/'data'/(name+'.csv')
        if path.exists():
            try:
                with path.open(encoding='utf-8-sig', newline='') as f:
                    rows = [{k:(v or '').strip() for k,v in row.items() if k is not None} for row in csv.DictReader(f)]
                    tables[name] = [r for r in rows if any(r.values())]
            except (OSError, UnicodeError, csv.Error):
                tables[name] = []  # The audit already reports the read error.
        else: tables[name] = []
    register = tables['study-register']
    registered = {r['report_id'] for r in register if r.get('report_id')}
    corpus = {r['report_id']:r for r in tables['corpus-register'] if r.get('report_id')}
    configured = bool(corpus)
    selected = {rid:r for rid,r in corpus.items() if r.get('corpus_role') in {'main','extension'}}
    unresolved = sorted(rid for rid,r in selected.items() if r.get('independence_status') != 'confirmed')
    selected_pairs = [r for r in register if r.get('report_id') in selected]
    missing_register = set(selected) - {r.get('report_id') for r in selected_pairs}
    study_count = None
    if configured and selected and not unresolved and not missing_register and not checked['issues']:
        study_count = len({r['study_id'] for r in selected_pairs if r.get('study_id')})
    evidence = tables['evidence-units']
    by_role = {}
    if configured:
        for role in ['main','extension','background']:
            rows = [r for r in evidence if corpus.get(r.get('report_id'),{}).get('corpus_role') == role]
            by_role[role] = {'reports':sum(r.get('corpus_role')==role for r in corpus.values()),
                             'registered_units':len(rows),
                             'located_units':sum(r.get('extraction_status')=='located' for r in rows),
                             'substantive_units':sum(r.get('contribution_role')=='substantive' for r in rows),
                             'context_only_units':sum(r.get('contribution_role')=='context_only' for r in rows),
                             'unclassified_contribution_units':sum(r.get('contribution_role') not in {'substantive','context_only'} for r in rows),
                             'unit_types':dict(Counter(r.get('unit_type') or 'unreported' for r in rows)),
                             'evidence_subjects':dict(Counter(r.get('evidence_subject') or corpus.get(r.get('report_id'),{}).get('evidence_subject') or 'unreported' for r in rows))}
    return {'status':checked['status'],'registered_reports':len(registered),
            'table_rows':checked['row_counts'],'active_table_rows':checked['active_row_counts'],
            'corpus_configuration':'configured' if configured else 'not_configured',
            'corpus_by_role':by_role if configured else None,
            'fulltext_status_counts':dict(Counter(r.get('fulltext_status') or 'unreported' for r in corpus.values())) if configured else None,
            'confirmed_independent_studies_main_and_extension':study_count,
            'independence_unresolved_reports':unresolved,
            'independence_note':'Count requires a configured selected corpus, confirmed independence, valid report/study links and no structural errors; otherwise null.',
            'pending_human_review_rows':checked['pending_human_review_rows'],
            'issues':checked['issues'],'warnings':checked['warnings'],
            'limits':'Registered-state summary only; not database hit totals, completed PRISMA flow, scientific confidence or proof of human review.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True)
    args=parser.parse_args()
    result=summarize(args.root)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 2 if result['issues'] else 0


if __name__=='__main__':
    raise SystemExit(main())
