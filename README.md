# agent-weekly-scripts

[Agent 周刊](https://github.com/lysandre001/agent-weekly) 的导出工具。

| 脚本 | 用途 | 依赖 |
|---|---|---|
| `export_wechat.py` | 导出指定期为微信公众号图文 HTML（内联样式，直接粘贴进编辑器） | `pip install markdown` |
| `translate_en.py` | 翻译指定期为英文版（LLM，保留引文/出处/时间坐标） | `pip install openai` + `OPENAI_API_KEY` |
| `export_substack.py` | 导出指定期为 Substack markdown（去 frontmatter + 期号导语 + 尾注） | 无 |

## 用法

```bash
python export_wechat.py ../agent-weekly/docs/issue-1.md -o out/wechat-issue-1.html
python export_substack.py ../agent-weekly/docs/issue-1.md -o out/substack-issue-1.md
python translate_en.py ../agent-weekly/docs/issue-1.md -o ../agent-weekly/docs-en/issue-1.md
```

微信公众号：打开输出的 HTML，全选复制，粘贴进 mp.weixin.qq.com 编辑器即可（样式走内联，编辑器不会剥掉）。

Substack：新建 post，把输出的 md 全文粘贴进编辑器（Substack 原生支持 markdown 粘贴）。

## 约定

- 输入统一是 `agent-weekly/docs/issue-N.md`，frontmatter 的 `date` 会被读取。
- 翻译调性写死在 `translate_en.py` 的 prompt 里：事实密度优先，观点必须可溯源。
