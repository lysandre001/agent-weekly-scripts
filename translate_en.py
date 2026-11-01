#!/usr/bin/env python3
"""把指定期翻译为英文版（LLM 翻译，本地运行）。

默认走 OpenAI 兼容接口（也适用于 Kimi/Moonshot、DeepSeek 等）：
    export OPENAI_API_KEY=...
    export OPENAI_BASE_URL=https://api.moonshot.cn/v1   # 可选
    python translate_en.py ../agent-weekly/docs/issue-1.md -o ../agent-weekly/docs-en/issue-1.md

调性要求（写死在 prompt 里）：
- 保留全部引文、出处链接、时间坐标
- 不增译判断；中文特有的机构名保留拼音+英文注释
"""
import argparse, os, re, sys
from pathlib import Path

PROMPT = """Translate the following Chinese newsletter issue into English.

Rules:
- Preserve every quote, source link, and date exactly.
- Do not add opinions or commentary that are not in the original.
- Keep proper nouns; for Chinese-specific organizations add pinyin + brief English gloss on first mention.
- Newsletter tone: factual, dense, dry wit welcome. Keep the markdown structure (headings, lists, blockquotes) identical.
- Output ONLY the translated markdown, no preamble.

---
%s
"""


def call_llm(text: str) -> str:
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )
    model = os.environ.get("TRANSLATE_MODEL", "gpt-4o-mini")
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": PROMPT % text}],
        temperature=0.3,
    )
    return resp.choices[0].message.content


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issue", help="docs/issue-N.md 路径")
    ap.add_argument("-o", "--out", help="输出英文 md 路径（默认 <input>/../docs-en/issue-N.md）")
    args = ap.parse_args()

    text = Path(args.issue).read_text(encoding="utf-8")
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("请设置 OPENAI_API_KEY（可选 OPENAI_BASE_URL / TRANSLATE_MODEL）")

    out_path = Path(args.out) if args.out else Path(args.issue).parent.parent / "docs-en" / Path(args.issue).name
    translated = call_llm(text)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(translated, encoding="utf-8")
    print(f"written: {out_path}")


if __name__ == "__main__":
    main()
