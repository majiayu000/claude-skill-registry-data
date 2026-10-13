---
name: nano-pdf-zh
description: 使用自然语言指令编辑 PDF 文件，通过 nano-pdf CLI 实现。
homepage: https://pypi.org/project/nano-pdf/
metadata: {"bot":{"emoji":"📄","requires":{"bins":["nano-pdf"]},"install":[{"id":"uv","kind":"uv","package":"nano-pdf","bins":["nano-pdf"],"label":"安装 nano-pdf (uv)"}]}}
---

# nano-pdf (中文版)

使用 `nano-pdf` 命令通过自然语言指令对 PDF 的特定页面进行编辑。

## 快速开始

```bash
nano-pdf edit deck.pdf 1 "将标题改为'Q3业绩报告'并修正副标题中的拼写错误"
```

注意事项：
- 页码编号从 0 或 1 开始，具体取决于工具版本和配置；如果结果页码偏移了一位，请尝试另一种编号方式。
- 在发送输出 PDF 之前，请务必检查输出结果是否正确。
