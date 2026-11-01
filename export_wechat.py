#!/usr/bin/env python3
"""导出指定期为微信公众号图文 HTML。

微信公众号编辑器只保留内联样式：本脚本把 markdown 转成内联样式的
section/段落 HTML，直接粘贴进 mp.weixin.qq.com 编辑器即可。

用法:
    python export_wechat.py ../agent-weekly/docs/issue-1.md -o out/wechat-issue-1.html

依赖: pip install markdown
"""
import argparse, re, sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("pip install markdown")

STYLE = {
    "section": 'style="margin-bottom:24px;"',
    "h2": 'style="font-size:18px;font-weight:bold;margin:32px 0 12px;"',
    "h3": 'style="font-size:16px;font-weight:bold;margin:24px 0 10px;"',
    "p": 'style="font-size:15px;line-height:1.8;margin:0 0 16px;color:#3f3f3f;"',
    "li": 'style="font-size:15px;line-height:1.8;color:#3f3f3f;"',
    "blockquote": 'style="margin:16px 0;padding:10px 14px;border-left:3px solid #576b95;background:#f7f7f7;color:#666;font-size:14px;line-height:1.7;"',
    "code": 'style="font-family:monospace;font-size:13px;background:#f2f2f2;padding:2px 4px;border-radius:3px;"',
    "pre": 'style="font-family:monospace;font-size:13px;background:#f6f8fa;padding:12px;border-radius:4px;overflow-x:auto;line-height:1.5;"',
    "a": 'style="color:#576b95;"',
}


def inline_styles(html: str) -> str:
    for tag in ("h2", "h3", "p", "li", "blockquote", "pre"):
        html = re.sub(rf"<{tag}>", f'<{tag} {STYLE[tag]}>', html)
    html = re.sub(r"<ul>", '<ul style="margin:0 0 16px;padding-left:22px;">', html)
    html = re.sub(r"<ol>", '<ol style="margin:0 0 16px;padding-left:22px;">', html)
    html = re.sub(r"<code>", f'<code {STYLE["code"]}>', html)
    html = re.sub(r"<a ", f'<a {STYLE["a"]} ', html)
    return html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issue", help="docs/issue-N.md 路径")
    ap.add_argument("-o", "--out", help="输出 HTML 路径（默认 stdout）")
    args = ap.parse_args()

    text = Path(args.issue).read_text(encoding="utf-8")
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)  # 去 frontmatter
    md = markdown.markdown(text, extensions=["extra", "nl2br"])

    wrapped = f'<section {STYLE["section"]}>\n{inline_styles(md)}\n</section>'
    wrapped = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
               f'<title>{Path(args.issue).stem}</title></head><body>\n'
               f"{wrapped}\n</body></html>")

    if args.out:
        Path(args.out).write_text(wrapped, encoding="utf-8")
        print(f"written: {args.out}")
    else:
        print(wrapped)


if __name__ == "__main__":
    main()
