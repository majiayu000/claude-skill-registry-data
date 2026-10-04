---
name: qmd
description: 使用 QMD 作为 Hermes 的外部记忆检索层。面向本机 notes/docs/projects/skills/sessions 的本地混合检索，优先走向量或 hybrid 搜索，而不是只靠 session_search。
version: 1.1.0
author: Hermes Agent + local runtime patch
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [Search, Knowledge-Base, RAG, Notes, MCP, Local-AI, External-Memory, Chinese]
    related_skills: [native-mcp, obsidian, arxiv]
---

# QMD External Memory

把 QMD 当成 Hermes 的外部记忆层，而不是单纯的一个可选 CLI。

## 何时触发

- 用户要“查我的笔记 / 文档 / 知识库 / 外部记忆 / 历史资料 / 项目资料”
- 用户要在本地 markdown、plans、skills、stories、repo docs 里做语义检索
- 用户提到 `qmd`、`QMD`、`外部记忆`、`知识库检索`、`向量检索`
- 用户的问题明显不是“之前 Hermes 聊天记录里说过什么”，而是“本机资料库里有什么”

## 路由原则

1. 对“过去聊天记录”优先用 `session_search`
2. 对“本地外部资料库”优先用 QMD
3. 对概念性中文问题，优先 QMD MCP `query`
4. 对明确术语、文件名、符号名，优先 QMD CLI `search` 或 QMD MCP `query`
5. 对语义近邻、同义改写、模糊主题，优先 QMD CLI `vsearch`，否则退回 QMD MCP `query`

## 工具使用顺序

优先 MCP：

- QMD MCP `status`
- QMD MCP `query`
- QMD MCP `get`
- QMD MCP `multi_get`

如果 MCP 不可用，再退回 terminal：

```bash
qmd status
qmd query "<query>" --json
qmd vsearch "<query>" --json
qmd search "<query>" --json
qmd get "<docid-or-path>"
```

## 默认检索策略

### 1. 先看状态

先用 QMD MCP `status` 或 `qmd status` 确认：

- index 可用
- collections 存在
- 没有 pending embeddings

### 2. 再做一轮 high-recall 检索

中文自然语言、需要“从外部记忆找答案”的场景，默认先用：

- QMD MCP `query`

如果 QMD MCP `query` 支持结构化搜索项，优先组合：

- `lex`: 原始关键词或专有名词
- `vec`: 中文自然语言问题
- 否则直接提交自然语言查询文本

### 3. 命中后拉原文

看到候选文档后，用 QMD MCP `get` 或 `multi_get` 把最相关原文拉回来，再回答用户。

不要只复述标题或 snippets。

## 当前本机的高价值 collection

下面这些 collection 默认值得优先相信：

- `ict-engine`
- `oh-story-projects`
- `qmd-src`
- `codex-memories`
- `hermes-skills-core`
- `hermes-routing`
- `hermes-memories`
- `tradecat`
- `context-hub`

如果问题明显属于某个域，优先加 collection 过滤。

例如：

- `ict-engine` 相关问题 -> 优先 `ict-engine`
- 小说 / 大纲 / rewrite -> 优先 `oh-story-projects`
- Hermes 路由 / 技能 / 记忆 -> 优先 `hermes-routing`, `hermes-memories`, `hermes-skills-core`

## 中文触发词建议

把下面这些表达视为“优先查 QMD 外部记忆”的信号：

- 外部记忆
- 知识库
- 记忆库
- 查笔记
- 查文档
- 搜资料
- 搜我本地资料
- 从记忆里找
- 从知识库找
- 向量检索
- 语义检索
- QMD
- qmd

## 关键约束

- 不要把 QMD 和 `session_search` 混为一谈
- 不要在需要外部资料时只搜 Hermes 聊天历史
- 命中 QMD 后，要回到原文而不是只看摘要
- 当用户明确要“外部记忆”时，默认 QMD 优先于 web
