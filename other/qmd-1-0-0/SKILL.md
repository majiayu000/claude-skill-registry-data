---
name: qmd
description: '本地搜索/索引 CLI (BM25 + 向量 + 重排)。**Auto-trigger**: 当需要本地文件搜索、语义检索时自动使用。'
homepage: https://tobi.lutke.com
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":["qmd"]},"install":[{"id":"node","kind":"node","package":"https://github.com/tobi/qmd","bins":["qmd"],"label":"安装 qmd (node)"}]}}
---

# qmd

使用 `qmd` 索引本地文件并搜索它们。

索引
- 添加集合：`qmd collection add /path --name docs --mask "**/*.md"`
- 更新索引：`qmd update`
- 状态：`qmd status`

搜索
- BM25：`qmd search "query"`
- 向量：`qmd vsearch "query"`
- 混合：`qmd query "query"`
- 获取文档：`qmd get docs/path.md:10 -l 40`

说明
- 嵌入/重排使用 Ollama，地址为 `OLLAMA_URL`（默认 `http://localhost:11434`）。
- 索引默认存放在 `~/.cache/qmd`。
- MCP 模式：`qmd mcp`。
