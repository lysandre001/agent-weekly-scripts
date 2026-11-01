#!/usr/bin/env python3
"""导出指定期为 Substack 版本。

Substack 编辑器支持直接粘贴 Markdown，本脚本做三件事：
1. 去 frontmatter，提取 date/标题
2. 顶部插入 Substack 友好的导语块（subtitle + 期号）
3. 输出干净的 .md，粘贴进 substack.com/publish 即可

用法:
    python export_substack.py ../agent-weekly/docs/issue-1.md -o out/substack-issue-1.md
"""
import argparse, re
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issue", help="docs/issue-N.md 路径")
    ap.add_argument("-o", "--out", help="输出 markdown 路径（默认 stdout）")
    args = ap.parse_args()

    raw = Path(args.issue).read_text(encoding="utf-8")
    n = re.search(r"issue-(\d+)", args.issue).group(1)

    date = ""
    fm = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if fm:
        dm = re.search(r"^date:\s*(\S+)", fm.group(1), re.M)
        date = dm.group(1) if dm else ""
        raw = raw[fm.end():]

    title_m = re.search(r"^#\s+(.+)$", raw, re.M)
    title = title_m.group(1).strip() if title_m else f"Agent 周刊 第 {n} 期"
    body = raw.replace(f"# {title}", "", 1).strip()

    out = f"**Agent 周刊 第 {n} 期**{(' · ' + date) if date else ''}\n\n{body}"
    out += "\n\n---\n*Agent 周刊：记录下一代个人电脑级浪潮下逐渐成型的基础建设、共识、转型，以及值得注意的社会问题。*\n"

    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"written: {args.out}")
    else:
        print(out)


if __name__ == "__main__":
    main()
