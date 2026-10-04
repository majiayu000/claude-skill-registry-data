---
name: happy-notes
description: |
  iflow 知识库助手（iflow知识库），支持知识库管理、文件上传/URL导入、内容生成、联网搜索并导入知识库。
  当用户提到知识库、资料库、收藏文章、保存链接、上传文件、导入网页、
  生成报告、生成PPT、生成播客、生成思维导图、生成视频、分享知识库、
  查看生成进度、搜论文并整理、查文献并生成报告、深度研究、搜索网页并存到知识库时，使用此 skill。
  即使用户没有明确说"知识库"或"报告"，只要意图涉及文章收藏、知识整理、内容生成、
  知识分享、日常记录（如"帮我记一下这篇文章""做个PPT""分享给同事""深度研究一下"
  "记一下今天吃饭50元""帮我记个笔记""存一下这个信息"），也应触发此 skill。
  注意：如果用户只是想快速了解某个问题（如"XX是什么""帮我查一下XX"）而不涉及知识库存储或内容生成，
  不应触发此 skill，Agent 应使用自身的搜索能力直接回答。
  English triggers: knowledge base, upload file, import URL, generate report, create PPT,
  generate podcast, generate video, mind map, share notebook, deep research,
  save article, web search, literature review, academic paper, iflow.
metadata:
  openclaw:
    emoji: '📓'
    always: true
    primaryEnv: 'IFLOW_API_KEY'
  security:
    credentials_usage: |
      This skill requires a user-provisioned iflow API Key to authenticate
      with the official iflow API. The API Key is ONLY sent as an Authorization
      header to the configured iflow API endpoint. No credentials are logged,
      stored in files, or transmitted to any other destination.
---




### Cleanup Review

`python scripts/_reset_state.py` is an optional cleanup helper for the `happy-notes` skill. It may recursively remove /tmp/_skill_work, /tmp/skill_scratch. Show the exact paths first, explain whether they are skill-private temporary paths or user state, and run the cleanup only after the user confirms.

# happy-notes

iflow 知识库助手。支持：**knowledge-base**（知识库管理与文件管理）、**reports**（内容生成）、**search**（联网搜索并导入知识库）。分享功能见下方「分享功能」章节。

## Setup

> **Security note:** Credentials are only sent as HTTP headers to the configured API endpoint and never to any other domain.

1. 获取 **API Key**：访问 [API Key 管理页面](https://iflow.cn/?open=api-key) 申请
2. 存储凭证（二选一）：

```bash
# 方式 A — 配置文件（推荐，Linux/Mac）
mkdir -p ~/.config/happy-notes && echo "your_api_key" > ~/.config/happy-notes/api-key

# 方式 B — 环境变量
export IFLOW_API_KEY="your_api_key"
```

```powershell
# Windows PowerShell 用户：
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\happy-notes"
"your_api_key" | Out-File -FilePath "$env:USERPROFILE\.config\happy-notes\api-key" -Encoding utf8 -NoNewline
# 或设置环境变量：$env:IFLOW_API_KEY = "your_api_key"
```

> Windows 用户注意：必须先创建 `happy-notes` 目录再写入 api-key 文件。如遇配置问题，请访问 [API Key 管理页面](https://iflow.cn/?open=api-key) 获取帮助。

Agent 按优先级尝试：环境变量 → 配置文件。Pipeline 脚本内部自动读取凭证，无需手动初始化。

## 快速决策树

收到用户请求后，**按顺序判断**：

```
1. 用户只是问问题/查信息？ → 不走 Pipeline，Agent 自行回答
2. 操作主体是什么？
   a. 知识库本身（列表/创建/删除/改名/详情） → pipeline_kb.py
   b. 知识库中的文件（列表/重命名/删除/详情/重试） → pipeline_file_management.py
   c. 需要新建库 + 上传文件/URL → P1 (pipeline_create_kb_and_generate.py)
   d. 向已有库追加内容（文件/URL/文本） → P3 (pipeline_import_and_generate.py)
   e. 在已有库中搜索内容 → 核心目的是生成? P2 : P4
   f. 联网搜索外部网页/论文 → P6 (pipeline_web_search.py)
   g. 直接对已有库生成报告/PPT → pipeline_generate.py
   h. 查看生成进度 → pipeline_check_status.py
   i. 分享知识库 → pipeline_share.py
```

## 快速决策表

> **⚡ 多步骤任务优先用 Pipeline 脚本**。Pipeline 已封装凭证读取、参数串联、解析轮询、错误处理，一条命令完成整个流程。仅 Pipeline 不覆盖的单步操作才直接调 API（见下方「直接调 API 参考」）。

收到用户请求后，按此表选择执行方式：

| 用户意图 | 执行方式 | 关键参数 |
|---------|---------|---------|
| **建库 + 上传 + 生成** | | |
| "建个知识库，传几篇论文，生成报告" | Pipeline 1 `pipeline_create_kb_and_generate.py` | `--name` `--files` `--urls` `--output-type` `--query` |
| "建个知识库存一下这些文件"（不生成） | Pipeline 1 | `--name` `--files` `--no-generate` |
| **追加内容 + 生成** | | |
| "把这个链接/文件加到XX知识库，然后生成总结" | Pipeline 3 `pipeline_import_and_generate.py` | `--kb` + `--files`/`--urls`/`--text` `--output-type` `--query` |
| "帮我把这段内容存到知识库" | Pipeline 3 | `--kb` `--text` `--text-title` `--rename` `--no-generate` |
| **搜索 + 生成** | | |
| "在XX知识库里搜一下关于YY的，生成报告" | Pipeline 2 `pipeline_search_and_generate.py` | `--kb` `--search` **`--mode semantic`** `--output-type` `--query` |
| "搜一下知识库里有没有关于XX的文件" | Pipeline 2 | `--kb` `--search` `--mode file` `--search-only` |
| **语义检索（深度内容匹配）** | | |
| "知识库里有没有关于XX的内容" | Pipeline 4 `pipeline_semantic_search.py` | `--kb` `--query` |
| "找到相关内容后生成报告" | Pipeline 4 | `--kb` `--query` `--generate` `--output-type` |
| "检索后分享知识库" | Pipeline 4 | `--kb` `--query` `--share` |
| **文件管理** | | |
| "看看知识库里有哪些文件" | Pipeline 5 `pipeline_file_management.py list` | `--kb` |
| "把这个文件改个名" | Pipeline 5 `rename` | `--kb` `--file` `--new-name` |
| "删掉这个文件" | Pipeline 5 `delete` | `--kb` `--file` `--force` |
| "把那几个测试文件都删了" | Pipeline 5 `batch-delete` | `--kb` `--files` `--force` |
| **联网搜索 + 导入 + 生成**（搜索结果存入知识库） | | |
| "帮我搜一下关于XX的网页，整理成报告" | Pipeline 6 `pipeline_web_search.py` | `--kb` `--query` `--source WEB` `--output-type` |
| "搜一下XX的学术论文，生成综述" | Pipeline 6 | `--kb` `--query` `--source SCHOLAR` `--output-type` |
| "深度研究一下XX" | Pipeline 6 | `--kb` `--query` `--type DEEP_RESEARCH` |
| "搜一下XX的论文存到知识库"（不生成） | Pipeline 6 | `--kb` `--query` `--no-generate` |
| "搜一下XX看看有什么"（只看结果） | Pipeline 6 | `--kb` `--query` `--search-only`（⚠️ 仍需知识库） |
| **快速搜索（不涉及知识库）** | | |
| "XX是什么" / "帮我查一下XX" / "最近有什么关于XX的新闻" | **不走 Pipeline**，Agent 使用自身搜索能力直接回答 | — |
| **知识库管理** | | |
| 查看/创建/删除知识库 | `pipeline_kb.py` `list`/`create`/`delete` | `--name` / `--kb` `--force` |
| 修改知识库名称/描述 | `pipeline_kb.py` `update` | `--kb` `--name` `--description` |
| 查看知识库详情 | `pipeline_kb.py` `info` | `--kb` |
| **文件管理补充** | | |
| 查看文件详情 | `pipeline_file_management.py` `info` | `--kb` `--file` |
| 重试解析失败的文件 | `pipeline_file_management.py` `retry` | `--kb` `--file` |
| **内容生成（单独生成，不含搜索/导入）** | | |
| "帮我做个PPT" / "生成一份报告" | `pipeline_generate.py` | `--kb` `--output-type` `--query` `--preset` |
| "查看生成进度" / "做好了吗" | `pipeline_check_status.py` | `--kb` [--creation-id] |
| **搜索管理** | | |
| 停止正在进行的搜索 | `pipeline_web_search.py` `--stop` | `--kb` `--stop` |
| 删除搜索记录 | `pipeline_web_search.py` `--delete-search` | `--kb` `--delete-search` |
| **分享** | | |
| "把知识库分享给同事" | `pipeline_share.py` | `--kb` |
| **其他（极少数 Pipeline 未覆盖的操作）** | | |
| 修改知识库高级设置等 | 查阅 `references/api.md` | 仅作为最后手段 |

### `--query` 参数含义速查（⚠️ 不同 Pipeline 含义不同，传错会导致生成质量差或搜索失败）

| Pipeline | `--query` 含义 | 创作要求参数 | 默认生成 |
|----------|---------------|-------------|---------|
| P1 | — | `--query`（创作要求） | **是** → `--no-generate` 关闭 |
| P2 | — | `--query`（创作要求），搜索词用 `--search` | **是** → `--search-only` 关闭 |
| P3 | — | `--query`（创作要求） | **是**（有新内容时） → `--no-generate` 关闭 |
| P4 | `--query`（**检索关键词**） | `--gen-query`（创作要求） | **否** → `--generate` 开启 |
| P6 | `--query`（**搜索关键词**） | `--creation-query`（创作要求） | **是** → `--no-generate` 关闭 |
| P-Gen | — | `--query`（创作要求） | 始终生成 |

> **⚠️ 易错点**：
> - **P4**：搜索词用 `--query`，创作要求用 `--gen-query`。千万不要把创作要求塞进 `--query`，否则搜索结果会偏离。
> - **P6**：搜索词用 `--query`，创作要求用 `--creation-query`。不传 `--creation-query` 时脚本会自动生成默认 prompt。
> - **P2**：搜索词用 `--search`（不是 `--query`），`--query` 是创作要求。不要混淆。
>
> **记忆规则**：P4 和 P6 的 `--query` 是搜索/检索词（因为搜索是它们的核心功能），创作要求用独立参数名。其他 Pipeline 的 `--query` 就是创作要求。
> **P4 是唯一默认不生成的 Pipeline**，需要 `--generate` 显式开启。

### Pipeline 2 搜索模式选择

> **P2 有两种搜索模式，必须根据用户意图选择：**
>
> | 用户意图 | `--mode` | 原因 |
> |---------|----------|------|
> | 搜**内容/主题**（"关于XX的"） | `semantic` | 语义匹配内容片段，精准但较慢 |
> | 搜**特定文件**（"找一下叫XX的文件"） | `file` | 按文件名+摘要匹配，快速但粒度粗 |
>
> **默认是 `file` 模式。用户说"搜一下关于XX的"时，必须显式加 `--mode semantic`。**

### Pipeline 2 vs Pipeline 4 如何选？

> **一句话判断**：P2 = 核心目的是**生成**（搜索是选素材的手段）；P4 = 核心目的是**看检索结果**（生成/分享是可选附加）。

| 场景 | 用哪个 | 原因 |
|------|--------|------|
| 搜索后要**生成**内容 | **Pipeline 2** | 专为"搜索→生成"设计，支持 file/semantic 两种模式 |
| **纯检索**，只看结果不生成 | **Pipeline 4** | 返回详细片段和来源文件 |
| 检索后要**分享**知识库 | **Pipeline 4** | 内置 `--share` 参数 |
| 检索后**可能**生成（可选） | **Pipeline 4** | 用 `--generate` 可选触发生成 |

### Pipeline 2/4 vs Pipeline 6 vs Agent 自身搜索 如何选？

| 场景 | 用哪个 | 原因 |
|------|--------|------|
| 搜索**知识库内**已有内容 | **Pipeline 2/4** | 内部语义检索 |
| **联网搜索**新的网页/论文，需要**存储/整理/生成** | **Pipeline 6** | 外部搜索，结果导入知识库 |
| 需要**深度研究报告** | **Pipeline 6** (`DEEP_RESEARCH`) | 多轮搜索生成研究报告 |
| 搜**学术论文**并整理 | **Pipeline 6** (`--source SCHOLAR`) | 搜索 arxiv 等学术库 |
| 只想**快速了解**某个问题，不需要存储 | **Agent 自身搜索**（不走 Pipeline） | 用户只要答案，不涉及知识库 |

### 易混淆场景

| 用户表达 | 正确路由 | 为什么 |
|---------|---------|--------|
| "写篇博客" | type=`MARKDOWN`, query 描述博客风格 | 博客 = Markdown 报告 |
| "帮我总结一下" / "对比分析" | type=`PDF`, query 传达要求 | 总结/分析 = 报告 |
| "帮我记一下这些内容" | Pipeline 3 `--text` | 文本导入，非 URL 导入 |
| "记一下今天吃饭50元" | Pipeline 3 `--text` `--create-if-missing` | 短文本记录，自动匹配或创建知识库 |
| "今天买了本书花了30" | Pipeline 3 `--text` `--create-if-missing` | 隐含记账意图，无需用户指定知识库 |
| "把这篇文章存到知识库" | URL 导入（Pipeline 3 `--urls`） | 操作对象是链接，不是文本 |
| "找一下知识库里叫xxx的文件" | Pipeline 2 `--mode file` | 按文件名（+摘要）匹配 |
| "搜一下知识库里关于XX的，生成报告" | Pipeline 2 `--mode semantic` | 按内容语义匹配，核心目的是生成 |
| "知识库里有没有关于XX的内容" | Pipeline 4 | 语义检索内容片段 |
| "这篇论文讲了什么关于XX" | Pipeline 4 `--content-ids` | 限定文件的语义检索 |
| "做个PPT"（未指定风格） | type=`PPT`，**先询问风格** | Agent 应主动问：「PPT 有商务和卡通两种风格，您想用哪种？默认商务。」 |
| "做个卡通风格的PPT" | type=`PPT`, preset=`"卡通"` | PPT 风格参数 |
| "把文章存进去然后帮我写份报告" | Pipeline 3 | 多步任务用 Pipeline |
| "搜一下XX的论文" | **Pipeline 6** (联网搜索) | 搜外部论文并整理，不是知识库内搜索 |
| "知识库里搜一下XX" | Pipeline 2/4 | 已有内容搜索 |
| "深度研究一下XX" | **Pipeline 6** (`DEEP_RESEARCH`) | 多轮联网搜索 + 生成研究报告 |
| "深度研究一下XX的论文" | **Pipeline 6** (`DEEP_RESEARCH` + `--source SCHOLAR`) | 深度研究 + 学术论文源 |
| "XX是什么" / "帮我查一下XX" | **Agent 自身搜索**，不走 Pipeline | 用户只想要答案，不涉及知识库存储或生成 |
| "最近有什么关于XX的新闻" | **Agent 自身搜索**，不走 Pipeline | 快速查询，无需导入知识库 |

### 核心判断规则

- 用户只是**提问/查询信息**，不涉及存储、导入或生成 → **不走 Pipeline**，Agent 用自身搜索能力直接回答
- 操作对象是**知识库本身或其中的文件**（增删改查、上传、导入）→ knowledge-base
- 操作对象是**基于知识库内容的产出物**（报告、PPT、播客、思维导图、视频）→ reports
- 操作对象是**外部网页或学术论文**，且需要**导入知识库或生成产出物** → Pipeline 6（联网搜索→导入→生成）
- **多步骤任务** → 优先 Pipeline 脚本

> **搜索分流关键判断**：用户说"搜一下"时，看是否涉及知识库操作（存储、整理、生成报告等）。涉及 → Pipeline 6；不涉及 → Agent 自行搜索回答。

### Agent 常见错误（⚠️ 必须避免）

| 错误模式 | 正确做法 |
|---------|---------|
| 每个文件/URL 分别调用 Pipeline 1 创建知识库 → 产生 N 个空知识库 | **一次请求只创建一个知识库**，所有文件通过 `--files "a.pdf,b.pdf"` 逗号分隔一次传入 |
| 不检查知识库是否已存在就创建新的 | 先用 `--kb "名称"` 查询是否已有同名知识库，有则改用 Pipeline 3 追加 |
| `submitted` 状态告诉用户"已生成完成" | `submitted` 仅表示任务进入队列，只有 `success` 才是真正完成 |
| 对生成任务循环轮询状态 | 提交后告知用户预计时间，用户主动问时才查一次 |
| 用 `curl`/`iflow_api` 直接拼 HTTP 请求调 API（如 `creationList`、`shareNotebook` 等） | **必须使用 Pipeline 脚本**。Pipeline 已封装凭证、参数校验、轮询、错误重试。直接调 API 容易出错且不稳定。所有 20 个 API 端点均已有 Pipeline 覆盖，不存在"需要直接调 API"的场景 |
| Pipeline 输出有 `failedCount` 但 Agent 不告知用户 | 检查 Pipeline 输出 JSON 中的 `failedCount`/`failedItems`/`importFailedCount` 字段，**如有失败必须告知用户**（如"3 个文件已导入，1 个失败：bad.exe 格式不支持"） |

### 错误处理

| 错误码 | 场景 | Agent 应对方式 |
|--------|------|---------------|
| `40010` | 深度研究并发限制（同时只能运行 1 个） | 告知用户「您有一个深度研究任务正在进行中，请等待完成后再发起新的深度研究」。**不要重试**，建议用户稍后再试，或改用 `FAST_SEARCH` 快速搜索 |
| `500`（搜索/创作） | 搜索和创作接口限流（合计 20 次/分钟） | Pipeline 脚本内部已自动重试。如果仍然失败，告知用户「请求过于频繁，请稍后再试」 |
| `40004` | 文件尚在解析中就提交了生成任务 | 告知用户「文件正在解析中」，等待解析完成后再提交生成任务 |

## 文件上传限制

| 限制项 | 上限 | 说明 |
|--------|------|------|
| 单文件大小 | **20MB** | 超过需先压缩或拆分 |
| PDF 页数 | **500 页** | 超过需先拆分为多个文件再分批上传 |

> 用户上传大文件/长 PDF 时，Agent 应提前告知限制，建议拆分后分批导入同一知识库。

## 操作前置依赖链

**⚠️ 必须严格遵守：**

```
创建知识库 → 导入文件 → 文件解析完成(status=success) → 生成产出
```

1. **没有知识库就不能导入文件**：必须先有 `collectionId`，才能调用文件上传/导入接口
2. **文件未解析完成就不能生成产出**：必须确认 `status=success`，否则返回错误码 `40004`
3. **多步任务必须逐步确认**：用户说"导入这篇文章然后生成报告"时，必须先完成导入并确认解析完成，再提交生成任务，**不能并行提交**

### 轮询策略

| 操作类型 | 策略 | 说明 |
|---------|------|------|
| 文件解析 | Pipeline 内部自动轮询（5s 间隔） | Agent 无需干预，告知用户"正在处理"即可 |
| 内容生成（提交后） | **不轮询**，立即返回 | 告知用户预计时间，等用户问"做好了吗"时再查 |
| 内容生成（用户询问） | 单次查询 `creationList` | 查一次告知状态，不要循环轮询 |
| 联网搜索 | Pipeline 内部自动轮询 | Agent 向用户展示进度即可 |

> **关键原则**：搜索 + 创作接口共享 **20 次/分钟** 限额。内容生成任务有排队机制，高峰期耗时更长。Agent **绝不循环轮询**生成状态，提交后立即返回，用户询问时查一次。

## Pipeline 脚本

> 每个 Pipeline 的完整参数说明、输出 JSON 格式和使用示例见 `references/pipelines.md`。

| Pipeline | 脚本 | 用途 | 关键参数 |
|----------|------|------|---------|
| P1 | `pipeline_create_kb_and_generate.py` | 建库+上传+生成 | `--name` `--files` `--urls` `--output-type` |
| P2 | `pipeline_search_and_generate.py` | 搜索+生成 | `--kb` `--search` `--mode` `--output-type` |
| P3 | `pipeline_import_and_generate.py` | 追加+生成 | `--kb` `--files`/`--urls`/`--text` `--output-type` `--create-if-missing` |
| P4 | `pipeline_semantic_search.py` | 语义检索+生成/分享 | `--kb` `--query` `--generate` `--share` |
| P5 | `pipeline_file_management.py` | 文件管理 | `--kb` + `list`/`rename`/`delete`/`batch-delete`/`info`/`retry` |
| P6 | `pipeline_web_search.py` | 联网搜索+导入+生成 | `--kb` `--query` `--source` `--type` `--stop` `--delete-search` |
| P-Gen | `pipeline_generate.py` | 直接生成（已有知识库） | `--kb` `--output-type` `--query` `--preset` |
| P-KB | `pipeline_kb.py` | 知识库管理 | `list`/`create`/`delete`/`update`/`info` |
| P-Check | `pipeline_check_status.py` | 查看生成进度 | `--kb` `--creation-id` |
| P-Share | `pipeline_share.py` | 分享知识库 | `--kb` |

**通用说明：**
- **知识库定位**：所有 Pipeline 支持 `--kb`（名称模糊匹配）和 `--kb-id`（ID 精确指定）
- **输出格式**：结构化 JSON 到 stdout，进度日志到 stderr
- **参数串联**：Pipeline 1 返回的 `collectionId` 可传给其他 Pipeline 的 `--kb-id`
- **参数校验**：所有 Pipeline 在调用 API 前校验 `--output-type`、`--preset`、文件路径和 URL 格式，无效参数直接报错
- **删除确认**：Pipeline 5 删除操作默认需交互确认，Agent 调用时**必须加 `--force`**
- **列表上限**：`pipeline_kb.py list` 最多返回 100 个知识库，`pipeline_file_management.py list` 最多返回 100 个文件。超出时建议用 `--keyword`/`--file` 按关键词过滤

### 创作状态术语（⚠️ 严格区分）

| Pipeline 输出的 creationStatus | 含义 | Agent 应告知用户 |
|-------------------------------|------|-----------------|
| `submitted` | 生成任务已提交到队列，**尚未完成** | 「生成任务已提交，预计需要 10-30 分钟，您可以稍后问我"做好了吗"来查看进度」 |
| `pending` | 排队等待处理 | 「任务排队中，请耐心等待」 |
| `processing` | 正在生成中 | 「正在生成中，请稍候…」 |
| `success` | **真正完成**，内容可查看 | 「已生成完成！」 |
| `failed` | 生成失败 | 「生成失败：[具体原因]。建议检查源文件后重试」 |

> **绝对禁止**：在 `submitted` 或 `processing` 阶段使用"已完成""已生成"等措辞。只有 `success` 才代表真正完成。

## 操作指南

### 分享功能

用户可以将知识库分享给他人。分享包含以下内容的**只读快照**：

- 知识库中的**全部文件**
- 已生成的**产出物**

**分享权限：** 被分享者只能**查看**，不能编辑知识库内容，也不能基于该知识库再次生成新的产出物。

```shell
# 使用 Pipeline 脚本（推荐）
python3 scripts/pipeline_share.py --kb "AI 论文集"
```

脚本会自动查找知识库、调用分享 API、拼接分享链接并输出。

展示（Agent 用实际输出替换）：
```
知识库「AI 论文集」的分享链接已生成：
https://iflow.cn/inotebook/share?shareId=xxx

被分享者可查看知识库中的所有文件和已生成的内容（只读，不可编辑或再生成）。
```

> 如需"检索 + 分享"组合操作，可用 Pipeline 4：`pipeline_semantic_search.py --kb "..." --query "..." --share`

### 内容检索

**两种检索方式：**
- **语义检索**（`searchChunk`）：按语义匹配内容片段，精准但较慢（同步接口，几秒到几十秒）
- **文件级匹配**（`pageQueryContents`）：API 的 `fileName` 参数只按文件名匹配；Pipeline 2 的 file 模式会拉取全量文件列表后在客户端同时匹配 `fileName` 和 `summary`，快速但粒度粗

直接调 API 的用法见 `knowledge-base/SKILL.md`。

### 文本导入

用户粘贴纯文本内容要存入知识库时，**优先使用 Pipeline 3**：

```shell
python3 scripts/pipeline_import_and_generate.py \
  --kb "知识库名称" --text "用户粘贴的内容" \
  --text-title "文件标题" --rename --no-generate
```

Pipeline 内部会自动创建临时 `.md` 文件 → 上传 → 清理 → 重命名。后端不提供独立的文本创建接口，必须通过文件上传实现。手动实现方式见 `knowledge-base/SKILL.md`。

### 智能知识库匹配

> 当用户没有明确指定目标知识库时，Agent 需智能推断。完整匹配逻辑（默认配置检查 → 语义匹配 → 置信度处理 → 命名规则）见 `references/kb-matching.md`。

**核心流程**：检查默认配置 → 列出知识库按语义匹配 → 高置信度直接用 / 中等确认 / 无匹配建议创建。Pipeline 3 `--create-if-missing` 可在知识库不存在时自动创建。

## 用户体验

- **隐藏内部 ID**：展示中使用知识库名称、文件标题，ID 仅用于 API 调用
  - 正确：`已导入到知识库「AI 论文集」`
  - 错误：`已导入到知识库 c7e804b0-82f1-4617-b720-bebfac16b8d1`
- **精简进度**：不暴露内部操作细节，只报告用户关心的信息
  - 上传文件：`正在导入 attention.pdf…` → `已导入到「AI 论文集」`
  - 创作生成：`正在生成内容…` → `内容已生成`
- **批量操作**：汇总结果，如 `3 个文件已导入，1 个失败（bad.exe: 格式不支持）`
- **格式化展示**：
  ```
  你的知识库：
  1. **AI 论文集** — 5 个文件
  2. **竞品分析** — 12 个文件
  3. **技术方案** — 3 个文件
  ```

## API 参考

> **⚠️ 禁止直接用 `curl`/`iflow_api` 拼 HTTP 请求。所有 20 个 API 端点均已有 Pipeline 脚本覆盖，必须通过 Pipeline 脚本执行操作。**
>
> Pipeline 脚本已封装凭证读取、参数校验、解析轮询、错误重试，一条命令完成整个流程。直接拼 HTTP 请求容易出错（参数格式错、缺少轮询、无重试），且不利于用户理解操作进度。
>
> 如需了解 API 底层细节（仅供理解原理，不应直接调用），参见 `references/api.md`。
