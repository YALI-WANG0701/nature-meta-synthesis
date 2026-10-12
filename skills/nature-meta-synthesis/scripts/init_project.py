"""Create an empty, traceable meta-synthesis project using only the standard library."""
from pathlib import Path
import argparse
import shutil
import sys


def initialize(root):
    root = Path(root).expanduser().resolve()
    assets = Path(__file__).resolve().parents[1] / 'assets'
    sources = [assets / 'project-brief.md', assets / 'protocol.md', assets / 'manuscript-template.md']
    sources.extend(sorted((assets / 'tables').glob('*.csv')))
    missing = [str(path) for path in sources if not path.is_file()]
    if missing or len(sources) < 4:
        raise ValueError('Required skill assets missing: ' + ', '.join(missing))
    targets = [(src, root / ('data' if src.suffix == '.csv' else '') / src.name) for src in sources]
    targets.append((None, root / 'project-state.md'))
    conflicts = [str(dst) for _, dst in targets if dst.exists()]
    if conflicts:
        raise FileExistsError('Existing project files; no files changed: ' + ', '.join(conflicts))
    for folder in ('data', 'sources', 'logs', 'drafts'):
        (root / folder).mkdir(parents=True, exist_ok=True)
    for src, dst in targets:
        if src is not None:
            shutil.copyfile(src, dst)
        else:
            dst.write_text(
                '# 元综合项目状态\n\n'
                '- 当前阶段：1，研究问题与方法选择\n'
                '- 方案版本：未确定\n'
                '- 已完成：建立空白模板；尚未检索、筛选或形成发现\n'
                '- 数据状态：空表，不构成研究结果\n'
                '- 已分配 ID：无\n'
                '- 研究者复核：尚未开展\n'
                '- 报告集及版本：尚未确定；主/拓展/背景、主体与正文范围待记录\n'
                '- 独立研究数量：未核定，不由暂归study_id推断\n'
                '- 当前活动/退役映射：尚未编码\n'
                '- 下一步：填写项目简表，检查已有综述与可用质性证据\n'
                '- 缺口/待研究者决定：研究问题、方法、范围与分工\n'
                '- 更新日期：待实际更新时填写\n', encoding='utf-8')
    return root, len(targets)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, help='Project directory; existing files are never overwritten')
    args = parser.parse_args()
    try:
        root, count = initialize(args.root)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f'Created {count} empty project files in {root}; no searches or research findings were generated.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
