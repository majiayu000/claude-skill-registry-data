---
name: qmd-zh
description: 本地混合搜索 Markdown 笔记和文档。适用于搜索笔记、查找相关内容或从已索引的文档集合中检索文档。
homepage: https://github.com/tobi/qmd
metadata: {"clawdbot":{"emoji":"🔍","os":["darwin","linux"],"requires":{"bins":["qmd"]},"install":[{"id":"bun-qmd","kind":"shell","command":"bun install -g https://github.com/tobi/qmd","bins":["qmd"],"label":"通过 Bun 安装 qmd"}]}}
---

# qmd - 快速 Markdown 搜索

适用于 Markdown 笔记、文档和知识库的本地搜索引擎。一次索引，快速搜索。

## 适用场景（触发短语）

- "搜索我的笔记 / 文档 / 知识库"
- "查找相关笔记"
- "从我的文档集合中检索 Markdown 文件"
- "搜索本地 Markdown 文件"

## 默认行为（重要）

- 优先使用 `qmd search`（BM25）。它通常即时返回结果，应作为默认选择。
- 仅在关键词搜索失败且需要语义相似度匹配时，才使用 `qmd vsearch`（冷启动时可能非常慢）。
- 除非用户明确要求最高质量的混合检索结果且能接受较长运行时间/超时，否则避免使用 `qmd query`。

## 前置条件

- Bun >= 1.0.0
- macOS: `brew install sqlite`（SQLite 扩展）
- 确保 PATH 包含：`$HOME/.bun/bin`

安装 Bun（macOS）：`brew install oven-sh/bun/bun`

## 安装

`bun install -g https://github.com/tobi/qmd`

## 配置

```bash
qmd collection add /path/to/notes --name notes --mask "**/*.md"
qmd context add qmd://notes "此集合的描述"  # 可选
qmd embed  # 首次运行以启用向量 + 混合搜索
```

## 索引范围

- 专为 Markdown 文档集合设计（通常为 `**/*.md`）。
- 测试表明"杂乱"的 Markdown 也能正常工作：分块基于内容（每个分块约几百个 token），而非严格按标题/结构划分。
- 不是代码搜索的替代品；请使用代码搜索工具来搜索代码仓库/源码树。

## 搜索模式

- `qmd search`（默认）：快速关键词匹配（BM25）
- `qmd vsearch`（最后手段）：语义相似度搜索（向量）。由于每次运行可能需要在本地加载 LLM（例如 Qwen3-1.7B），通常较慢。
- `qmd query`（一般跳过）：混合搜索 + LLM 重排序。通常比 `vsearch` 更慢，且可能超时。

## 性能说明

- `qmd search` 通常即时完成。
- `qmd vsearch` 在某些机器上可能需要约 1 分钟，因为查询扩展可能会在每次运行时将本地模型加载到内存中；向量查找本身通常很快。
- `qmd query` 在 `vsearch` 之上增加了 LLM 重排序，因此可能更慢且交互使用可靠性更低。
- 如果需要频繁进行语义搜索，建议保持进程/模型处于热启动状态（例如，如果你的环境支持的话，使用长生命周期的 qmd/MCP 服务器模式），而不是每次都冷启动 LLM。

## 常用命令

```bash
qmd search "查询词"             # 默认
qmd vsearch "查询词"
qmd query "查询词"
qmd search "查询词" -c notes     # 搜索指定集合
qmd search "查询词" -n 10        # 返回更多结果
qmd search "查询词" --json       # JSON 格式输出
qmd search "查询词" --all --files --min-score 0.3
```

## 实用选项

- `-n <数量>`：返回结果数量
- `-c, --collection <名称>`：限制搜索范围到指定集合
- `--all --min-score <阈值>`：返回所有高于阈值的结果
- `--json` / `--files`：代理友好的输出格式
- `--full`：返回完整文档内容

## 文档检索

```bash
qmd get "path/to/file.md"       # 完整文档
qmd get "#docid"                # 按搜索结果中的 ID 检索
qmd multi-get "journals/2025-05*.md"
qmd multi-get "doc1.md, doc2.md, #abc123" --json
```

## 维护

```bash
qmd status                      # 索引健康状态
qmd update                      # 重新索引已变更的文件
qmd embed                       # 更新嵌入向量
```

## 保持索引最新

自动化索引流程，确保在添加/编辑笔记时搜索结果保持最新。

- 对于关键词搜索（`qmd search`），通常只需 `qmd update`（速度很快）。
- 如果你依赖语义/混合搜索（`vsearch`/`query`），可能还需要运行 `qmd embed`，但这可能较慢。

定时任务示例（cron）：

```bash
# 每小时增量更新（保持 BM25 索引最新）：
0 * * * * export PATH="$HOME/.bun/bin:$PATH" && qmd update

# 可选：每晚更新嵌入向量（可能较慢）：
0 5 * * * export PATH="$HOME/.bun/bin:$PATH" && qmd embed
```

如果你的 Clawdbot/Agent 环境支持内置调度器，可以在那里运行相同的命令，而非使用系统 cron。

## 模型与缓存

- 使用本地 GGUF 模型；首次运行时会自动下载。
- 默认缓存路径：`~/.cache/qmd/models/`（可通过 `XDG_CACHE_HOME` 覆盖）。

## 与 Clawdbot 记忆搜索的关系

- `qmd` 搜索的是你显式索引到集合中的**本地文件**（笔记/文档）。
- Clawdbot 的 `memory_search` 搜索的是**Agent 记忆**（之前交互中保存的事实/上下文）。
- 两者配合使用：`memory_search` 用于"我们之前决定/学到了什么？"，`qmd` 用于"我的磁盘笔记/文档中有什么相关内容？"。
