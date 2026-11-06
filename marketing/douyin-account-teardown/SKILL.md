---
name: douyin-account-teardown
description: "获取抖音真实一手数据，逆向拆解抖音平台账号，根据账号互动数据及账号作品数据，产出可复刻的运营手册。当用户提出「拆解某账号」「分析对标号」「看看XX号为什么火」「复刻这个账号的风格」「抓取抖音账号数据」「竞品账号分析」「对标账号数据」「账号诊断」等需求时使用。产出结构化数据 + 互动指标 + 形态拆解 + 差距定位。支持五大能力：(1) 关键词搜索视频/图文，可按点赞数、发布时间、视频时长、内容类型筛选排序；(2) 实时热榜查询，获取抖音热搜词条与热度数据；(3) 单条作品详情，按视频链接或 aweme_id 获取文案、互动与作者；(4) 博主作品抓取，按主页链接或 sec_uid 获取公开作品列表；(5) 视频评论分析，按视频链接或 aweme_id 获取评论内容与互动数据。"
license: MIT
version: "1.4.2"
display_name: 🎯抖音账号拆解
display_name_en: DouYin Account Teardown
description_zh: 获取抖音真实一手数据，逆向拆解抖音平台账号，根据账号互动数据及账号作品数据，产出可复刻的运营手册。当用户提出「拆解某账号」「分析对标号」「看看XX号为什么火」「复刻这个账号的风格」「抓取抖音账号数据」「竞品账号分析」「对标账号数据」「账号诊断」等需求时使用。产出结构化数据 + 互动指标 + 形态拆解 + 差距定位。
description_en: Acquire authentic first-hand DouYin data for reverse account deconstruction; produce replicable operation manuals from account engagement and content data. Triggered by requests for account deconstruction, benchmark analysis, viral account research, style replication, DouYin data crawling, competitor/benchmark account analysis, or account diagnosis. Deliver structured data, engagement metrics, pattern breakdown and gap identification.

metadata:
  openclaw:
    emoji: "🎬"
    primaryEnv: GUAIKEI_API_TOKEN
    requires:
      bins:
        - node
      env:
        - GUAIKEI_API_TOKEN
  enabled: true
  runtime: "nodejs@16.14.0+"
  env_desc:
    GUAIKEI_API_TOKEN: "抖音数据 API 访问令牌。未配置时无法调用接口；可通过 https://www.guaikei.com 开通并获取支持。"
  keywords:
    - "抖音"
    - "抖音搜索"
    - "抖音热搜"
    - "抖音热榜"
    - "抖音评论"
    - "需求挖掘"
    - "痛点分析"
    - "评论挖掘"
    - "作品详情"
    - "博主作品"
    - "对标账号"
    - "短视频数据分析"
    - "douyin"
    - "douyin search"
    - "douyin hot"
    - "douyin comments"
    - "douyin detail"
  category:
    - "数据分析"
    - "内容创作"
    - "Data&APIs"
  tags:
    - "抖音"
    - "抖音搜索"
    - "抖音热搜"
    - "抖音热榜"
    - "抖音评论"
    - "需求挖掘"
    - "痛点分析"
    - "视频数据"
    - "抖音作品"
    - "作品详情"
    - "博主主页"
    - "对标账号"
    - "选题"
    - "竞品分析"
    - "舆情监控"
    - "douyin"
    - "douyin-search"
    - "douyin-hot"
    - "douyin-comments"
    - "douyin-detail"
    - "抖音数据分析"
    - "达人筛选"
    - "带货达人"
    - "短视频运营"
    - "短视频"
    - "舆情监测"
    - "需求洞察"
    - "情绪动机挖掘"
    - "舆情数据获取"
    - "热点追踪"
    - "爆款挖掘"
    - "content-analysis"
    - "competitor-analysis"
    - "marketing"
    - "trend-tracking"
  schemas:
    - name: "输出信封"
      file: "assets/output_envelope.schema.json"
    - name: "搜索入参"
      file: "assets/search_cli_req.schema.json"
    - name: "搜索出参"
      file: "assets/search_cli_resp.schema.json"
    - name: "作品入参"
      file: "assets/post_cli_req.schema.json"
    - name: "作品出参"
      file: "assets/post_cli_resp.schema.json"
    - name: "热榜出参"
      file: "assets/hot_cli_resp.schema.json"
    - name: "评论入参"
      file: "assets/comment_cli_req.schema.json"
    - name: "评论出参"
      file: "assets/comment_cli_resp.schema.json"
    - name: "作品详情入参"
      file: "assets/detail_cli_req.schema.json"
    - name: "作品详情出参"
      file: "assets/detail_cli_resp.schema.json"
  examples:
    - '抖音上"AI 教程"最火的视频 → node src/douyin/search-cli.js --keyword "AI 教程" --sort 1'
    - '最近一周关于"AI 模型"的最新内容，要 20 条 → node src/douyin/search-cli.js --keyword "AI 模型" --sort 2 --time 7 --limit 20'
    - "今天抖音有什么热点 / 热搜榜 → node src/douyin/hot-cli.js"
    - '这个博主最近 30 条作品 → node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx" --limit 30'
    - '看看这个对标账号多少粉丝、多少获赞 → node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx" --limit 0'
    - '这条视频的评论区都在说什么 → node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx" --limit 40'
    - '这条视频的评论里有什么痛点 → 先确认至少取 50 条，同意后 node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx" --limit 50，再读 references/demand-mining.md'
    - '这条视频多少播放、点赞和文案 → node src/douyin/detail-cli.js --url "https://www.douyin.com/video/xxx"'
    - '搜索结果里第 3 条不错，展开看看 → node src/douyin/detail-cli.js --url <上一条搜索结果里的 url>'
    - '帮我找 1 分钟以内的减肥短视频，先来 30 条 → node src/douyin/search-cli.js --keyword "减肥" --duration 1 --limit 30'
    - '半年内最火的 AI 教程图文 → node src/douyin/search-cli.js --keyword "AI 教程" --sort 1 --time 180 --content 2'
---

# 🎯 抖音账号拆解

抖音公开数据只读获取工具。支持**关键词搜索排序**、**博主作品抓取**、**单条作品详情**、**视频/图文评论抓取**、**实时热榜获取**，输出结构化 JSON，适用于短视频选题、竞品监控、舆情分析、热点追踪、需求挖掘。

## 1. ⚠️ 执行前置清单（每次执行前必须过一遍，缺一不可）

1. **先 `cd` 到本 SKILL.md 所在目录**，再执行下面的 `node src/douyin/*.js` 命令。
2. **确认环境变量 `GUAIKEI_API_TOKEN` 已配置且有效**。未配置 → 不执行命令，直接走 §8 的 `AUTH_REQUIRED` 话术，禁止先跑一遍"试试看"。
3. **一次只跑一条命令，跑完等它自己结束**。查询最多 20 次，间隔从 2 秒起增加，之后每次最长 60 秒；算上单次请求 20 秒超时，`--limit` 很大时最长约 22 分钟。**进程未退出前不要判定失败，不要并发或重复发起同一条命令。**
4. **必填参数不齐就先追问**（见 §10），禁止猜测关键词或链接。

## 2. 💎 价值与典型场景（10 秒判断该不该用）

| 你是谁      | 你要做的事                       | 用哪个命令               |
| ----------- | -------------------------------- | ------------------------ |
| 短视频运营  | 找爆款选题、看高赞内容的共同点   | `search-cli.js --sort 1` |
| 品牌 / 投放 | 监控对标账号的发文节奏与内容策略 | `post-cli.js`            |
| 内容分析    | 看一条视频的文案、播放和互动     | `detail-cli.js`          |
| 舆情 / 客服 | 判断一条视频的评论区在骂还是在夸 | `comment-cli.js`         |
| 产品 / 运营 | 从一条视频的评论里看痛点和诉求   | `comment-cli.js`，再读 `references/demand-mining.md` |
| 所有人      | 今天抖音在火什么，追热点         | `hot-cli.js`             |

**典型产出**：结构化 JSON（标题、作者、点赞/评论/收藏/分享、标签、链接、发布时间），可直接导入 Excel / BI，或交给 AI 生成选题库、竞品对比表、舆情周报、需求痛点清单。结果还会自动落盘到技能目录的 `logs/` 下便于复盘。

**为什么用它而不是自己爬**：无需登录抖音账号，无风控封号风险；零第三方依赖，Node.js 内置模块直接跑；单次最多 1 万条；stdout 纯 JSON、日志走 stderr，AI 可直接解析。

> **合规前置**：调用本技能会把用户提供的关键词/链接发送至第三方数据 API（域名 `www.guaikei.com`）以换取结果。本技能不上传本地文件、不登录账号、无任何写操作（不发布/点赞/评论/关注）。仅处理抖音公开数据，数据仅限个人/团队内部分析。

## 3. 🎯 识别卡（选命令，命中即停）

| 用户要什么                         | 命令                             | 最少要有              |
| ---------------------------------- | -------------------------------- | --------------------- |
| 搜视频/图文、爆款、选题            | `node src/douyin/search-cli.js`  | `--keyword`           |
| 博主作品、主页、对标账号、粉丝数据 | `node src/douyin/post-cli.js`    | 主页链接或 `sec_uid`  |
| 某条视频/图文的评论（含痛点、需求挖掘、观点聚类） | `node src/douyin/comment-cli.js` | 视频链接或 `aweme_id` |
| 某条视频/图文的详情、播放、点赞、文案 | `node src/douyin/detail-cli.js`  | 视频链接或 `aweme_id` |
| 热搜、热榜、今天什么火             | `node src/douyin/hot-cli.js`     | 无参数                |

> 用户要「痛点 / 需求挖掘 / 观点聚类」时，仍用 `comment-cli.js` 取数。命令成功结束后必须先读 `references/demand-mining.md` 再写结论。

## 4. 🛠️ 命令与参数

> 完整取值含义见 `references/options.md`（**仅在需要确认枚举含义时才读取**，不要每次都读）。

### 4.1 关键词搜索 `search-cli.js`

| 参数         | 缩写 | 必填 | 取值                                           | 默认 |
| ------------ | ---- | ---- | ---------------------------------------------- | ---- |
| `--keyword`  | `-k` | ✅   | 2–50 个字符，不能是链接，不含 `< > " ' &`      | —    |
| `--sort`     | `-s` |      | 0 综合 / 1 最多点赞 / 2 最新发布               | 0    |
| `--time`     | `-t` |      | 0 全部 / 1 一天内 / 7 七天内 / 180 半年内      | 0    |
| `--duration` | `-d` |      | 0 不限 / 1 1分钟以下 / 2 1-5分钟 / 3 5分钟以上 | 0    |
| `--content`  | `-c` |      | 0 不限 / 1 视频 / 2 图文                       | 0    |
| `--limit`    | `-l` |      | 1–10000（**包月 Token 实际最多 30**）              | 10   |

**数量约定**：未指定 `--limit` 时只返回 10 条。用户说"全部/越多越好"再显式设 `--limit`，不要自作主张抓 10000 条。用户未说明套餐时优先默认 10；需要更多时先说明可能受套餐限制。关键词以 `-` 开头时写成 `--keyword=-AI`，或 `node src/douyin/search-cli.js -- -AI`。

**套餐双上限（重要）**：技能侧硬上限为 10000（按量 Token）。**包月 Token** 超限会返回 `PLAN_LIMIT`（后端 errcode 14），不要当网络错误重试：搜索/作品最多 **30**，评论最多 **50**；详情与热榜无此条数限制。具体以官网与本次 `message` 为准。

### 4.2 博主作品 `post-cli.js`

| 参数      | 缩写 | 必填 | 取值                                                                           | 默认 |
| --------- | ---- | ---- | ------------------------------------------------------------------------------ | ---- |
| `--url`   | `-u` | ✅   | `douyin.com/user/xxx`、`v.douyin.com/xxx` 短链，或 `sec_uid`（`MS4wLjA` 开头） | —    |
| `--limit` | `-l` |      | 0–10000（**包月最多 30**；**`0` = 只取博主互动数据**）                          | 10   |

成功时 `results` 是**对象**，含 `post`（作品数组）和 `user`（博主信息）。

### 4.3 视频评论 `comment-cli.js`

| 参数      | 缩写 | 必填 | 取值                                                                                   | 默认 |
| --------- | ---- | ---- | -------------------------------------------------------------------------------------- | ---- |
| `--url`   | `-u` | ✅   | `douyin.com/video/xxx`、`douyin.com/note/xxx`、`v.douyin.com/xxx`，或纯数字 `aweme_id` | —    |
| `--limit` | `-l` |      | 1–10000（**包月最多 50**）                                                              | 10   |

### 4.4 作品详情 `detail-cli.js`

| 参数    | 缩写 | 必填 | 取值                                                                                   | 默认 |
| ------- | ---- | ---- | -------------------------------------------------------------------------------------- | ---- |
| `--url` | `-u` | ✅   | `douyin.com/video/xxx`、`douyin.com/note/xxx`、`v.douyin.com/xxx`，或纯数字 `aweme_id` | —    |

没有 `--limit`。成功时 `results` 是**一条作品对象**（文案、互动、作者、播放地址），不是数组，也不含评论。图文（note）通常没有播放数和时长，属正常情况。

### 4.5 实时热榜 `hot-cli.js`

不接受任何参数，直接 `node src/douyin/hot-cli.js`。返回约 50 条。失败时最多重试 3 次，不走大约 22 分钟的长查询。

## 5. 🔀 意图路由决策树（按顺序判断，命中即停）

```
1. 提到"热榜/热搜/热点/今天什么火/榜单"   → hot-cli.js（无参数）
2. 提到"评论/留言/痛点/需求挖掘/观点聚类"且指向某个视频 → comment-cli.js（需视频链接或 aweme_id）
3. 提到"痛点/需求挖掘/观点聚类"但没有视频链接 → 先追问视频链接（§10）
4. 提到单条视频/图文的"详情/播放量/点赞/文案/这条内容本身" → detail-cli.js（需视频链接或 aweme_id）
5. 提到"作品/主页/账号/博主/对标账号"       → post-cli.js（需主页链接或 sec_uid）
6. 有关键词且无 1/2/3/4/5 的信号           → search-cli.js（需关键词）
7. 以上都不明确                            → 先追问（§10），禁止猜测执行
```

> ⚠️ 消歧规则：单独出现"视频"二字**不要默认归 post，也不要默认归 detail**。有关键词且无"评论/详情" → search；"这个视频的评论/留言" → comment；"这条视频的播放/点赞/详情" → detail；只有出现"作品列表/主页/账号/博主"才用 post。
> ⚠️ 链接类型冲突：`/user/` 链接只能给 post。`/video/`、`/note/` 可以给 comment 或 detail：出现「评论」用 comment，出现「详情、播放、点赞、文案」用 detail。两个都没说时先追问，不要猜。传成博主命令会得到 `INVALID_URL`。
> ⚠️ 痛点、需求挖掘、观点聚类：命令成功结束后，必须先读取 `references/demand-mining.md` 再写结论。当时没有视频链接时先追问链接。用户没同意至少取 50 条之前，不把 `--limit` 改成 50 后直接执行。

## 6. 🗣️ 自然语言 → 命令映射（执行前对照）

| 用户口语                        | 命令                                         | 参数推导                    |
| ------------------------------- | -------------------------------------------- | --------------------------- |
| "搜一下 AI 相关的视频"          | `--keyword "AI"`                             | 带关键词即搜索              |
| "找点赞最多的 / 最火的 AI 视频" | `--keyword "AI" --sort 1`                    | 最火/点赞最多 → sort=1      |
| "最新的 AI 教程，要 20 条"      | `--keyword "AI 教程" --sort 2 --limit 20`    | 最新 → sort=2；数量 → limit |
| "近一周最火的短视频"            | `--keyword "短视频" --time 7 --sort 1`       | 一周 → time=7               |
| "半年内最火的 AI 教程"          | `--keyword "AI 教程" --sort 1 --time 180`    | 半年 → time=180             |
| "减肥视频，只要 1 分钟以下的"   | `--keyword "减肥" --duration 1`              | 1分钟以下 → duration=1      |
| "AI 模型的图文内容，前 30 条"   | `--keyword "AI 模型" --content 2 --limit 30` | 图文 → content=2；包月勿超 30 |
| "看看这个博主最近发了啥"        | `post-cli.js --url <主页链接> --limit 20`    | 未说条数 → 默认 10，可问    |
| "他多少粉丝"                    | `post-cli.js --url <主页链接> --limit 0`     | 只要互动数据 → limit=0      |
| "这条视频评论区在骂什么"        | `comment-cli.js --url <视频链接> --limit 40` | 舆情场景 → 适当加大 limit   |
| "评论里有什么痛点 / 做需求挖掘" | `comment-cli.js --url <视频链接>`            | 先确认至少 50 条；结束后读 `references/demand-mining.md` |
| "这条视频多少播放 / 看下详情"   | `detail-cli.js --url <视频链接>`             | 只要这一条，不加 limit。图文通常没有播放数 |
| "搜索结果里第 3 条不错，展开看看" | `detail-cli.js --url <上一条结果里的 url>` | 用上一条结果里的 url 字段 |

## 7. 📜 输出契约

stdout 只有一份统一信封（成功 / 空结果 / 错误结构相同）：

```json
{
  "status": "success | empty | error",
  "error_code": "OK | NO_MATCH | INVALID_KEYWORD | INVALID_URL | INVALID_ARGS | AUTH_REQUIRED | AUTH_ERROR | PLAN_LIMIT | TIMEOUT | NETWORK_ERROR | HTTP_5xx | ...",
  "message": "人类可读的说明",
  "timestamp": "2026/10/20 21:30:00",
  "request": {
    "command": "search",
    "keyword": "AI 教程",
    "sort": 1,
    "limit": 20
  },
  "metadata": {
    "skill_version": "1.4.2",
    "runtime_version": "22.x",
    "execution_time": 34210
  },
  "results": [
    {
      "aweme_id": "7xxx",
      "desc": "…",
      "author_nickname": "…",
      "digg_count": 123456,
      "url": "…",
      "create_time_str": "2026/9/4 20:13:20"
    }
  ]
}
```

- `status=error` 时 `results` 为 `null`，原因看 `error_code` + `message`。
- 信封字段见 `assets/output_envelope.schema.json`。搜索、评论、热榜成功时 `results` 是数组。博主作品成功时 `results` 是对象，包含 `post`（作品数组）和 `user`（博主信息）。作品详情成功时 `results` 是一条作品对象。条目字段见 `assets/*_cli_resp.schema.json`；
- **向用户汇报时只摘关键字段**（标题/作者/点赞/链接/时间），不要把整份 JSON 原样粘贴——单条结果含大量封面与播放 URL，会撑爆上下文。
- 适合衔接的后续动作：选题汇总、高赞对比、竞品内容风格总结、博主发文节奏分析、报告与表格生成。
- 用户要做需求挖掘、痛点或评论观点聚类时，先读取 `references/demand-mining.md`，再按其中的步骤归纳。按该文档第 7 节的四段输出给用户：痛点、诉求、差异化信号、样本说明。不粘贴整份评论 JSON。

## 8. 🚨 退出码与错误码 → Agent 应对

| error_code                     | 退出码 | 含义                                   | Agent 必须做什么                                                                |
| ------------------------------ | ------ | -------------------------------------- | ------------------------------------------------------------------------------- |
| `AUTH_REQUIRED` / `AUTH_ERROR` | 3      | token 未配置 / 无效或过期              | **禁止重试**。引导到 [抖音账号拆解](https://www.guaikei.com) 自助开通并配置 `GUAIKEI_API_TOKEN` |
| `PLAN_LIMIT`                   | 1      | 套餐单次条数超限（常见于包月 Token）   | **禁止同参重试**。转述 `message`；可建议降低 `--limit`（搜索/作品≤30，评论≤50）或到官网升级按量；**须用户同意后再跑** |
| `INVALID_KEYWORD`              | 1      | 关键词不合法（长度/是链接/含特殊符号） | 转述 `message`，请用户换词；**禁止自动改词重试**                                |
| `INVALID_URL`                  | 1      | 无法识别链接或 ID，或链接类型传错      | 请用户提供：主页链接（post），或视频/图文链接（comment 评论、detail 详情）       |
| `INVALID_ARGS`                 | 2      | 参数解析失败，或枚举/范围越界          | 按 `--help` 修正后重试**一次**；**禁止改成默认值后自动再跑**                    |
| `NO_MATCH`（status=empty）     | 0      | 无结果，**不是失败**                   | 如实告知；可建议放宽（`--time 0`、换更常用词），**经用户同意后**再试            |
| `TIMEOUT` / `NETWORK_ERROR`    | 1      | 超时或网络错误                             | 可告知用户后重试，**最多 1 次**。搜索约 9 分钟、作品、作品详情和评论约 20 分钟内，服务端仍复用同一任务。热榜不走这组复用。进程被提前结束后，不要马上再跑同一条命令，马上再跑不会更快 |
| `API_SCHEMA_CHANGED`           | 1      | 成功响应的结果结构与约定不一致             | 按失败报告 `message`。不要把它说成没有结果                                      |
| `HTTP_5xx` / 其他              | 1      | 服务端或未知错误                       | 如实报告 `message`，不编造原因，不反复重试                                      |

## 9. 🛑 硬性禁止条款

- 不得编造数据；不得把空结果说成有结果。
- 不得在未征得用户同意的情况下自动修改搜索条件重试。
- `AUTH_REQUIRED` / `AUTH_ERROR` / `PLAN_LIMIT` 后不得同参重试；`PLAN_LIMIT` 不得擅自改成更大 `--limit`。
- 不得把 stderr 中的日志文案原样转述给用户（stderr 仅诊断用，对外只报 `message` 与关键参数）。
- 不得用本技能做登录态、私密数据获取或任何写操作。
- 不得在未 cd 到技能目录的情况下执行 `node src/douyin/*.js`。

## 10. 🧠 追问模板（输入不足时使用）

- 缺关键词：「你想搜索抖音里的什么内容？给我一个关键词，例如"AI 教程"。」
- 缺博主链接：「请提供博主主页链接（douyin.com/user/xxx 或 v.douyin.com 短链），或直接给 sec_uid。」
- 缺视频链接：「请提供视频或图文链接（douyin.com/video/xxx、douyin.com/note/xxx 或 v.douyin.com 短链）。」
- 链接类型不明：「你给的这个链接，是想看这个博主的作品，这条视频的详情，还是这条视频的评论？」
- 视频链接但没说评论还是详情：「这条视频你是要看评论，还是要看播放、点赞和文案？」
- 数量不明：「默认返回 10 条，需要更多的话告诉我具体条数。」
- 需求挖掘但条数不足 50：「默认 10 条不够判断痛点。是否至少取 50 条评论？」

## 11. 🔧 环境与合规

- 环境：Node.js 16.14.0+，Windows / Linux / macOS；必需环境变量 `GUAIKEI_API_TOKEN`。
- 配置方式：Windows cmd `set GUAIKEI_API_TOKEN=你的TOKEN`；Windows PowerShell `$env:GUAIKEI_API_TOKEN="你的TOKEN"`；Linux/macOS `export GUAIKEI_API_TOKEN=你的TOKEN`。令牌为 16–256 位字母、数字、下划线或连字符。
- 合规：仅处理抖音公开数据；调用会把关键词/链接发送至第三方 API（www.guaikei.com），使用前请确认数据外发与授权范围；数据仅限个人/团队内部分析，禁止违规分发。
- 更多帮助：[抖音账号拆解官网](https://www.guaikei.com)。

## 12. ❓ 常见问题

- 没结果：放宽关键词或减少限定（`--time 0`），换更常用的词；空结果退出码是 0，属正常。
- 结果太多：补场景/人群/品牌/时间/账号，并控制 `--limit`。
- 调用失败：先看退出码——3 = token 问题；2 = 参数问题；1 = 关键词/链接/网络/服务端。
- 播放地址和分享链接有时效，过期后需要重新获取。图文通常没有播放数和时长。
- 计费与单次上限以官网说明为准。技能侧硬上限 10000 条/次（按量）；**包月**搜索/作品最多 30、评论最多 50，超限为 `PLAN_LIMIT`，不是网络故障。
- 账号安全：只读能力，不登录/不发布/不点赞/不评论，无封号风险。
