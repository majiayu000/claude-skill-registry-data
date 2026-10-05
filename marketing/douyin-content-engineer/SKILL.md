---
name: douyin-content-engineer
description: 抖音内容引擎 — AI驱动的内容电商助手。覆盖带货视频分析、竞品账号分析、抖音爆款视频挖掘、短视频爆款逻辑分析。提供4个能力：①关键词搜索（可按点赞/最新排序、时间窗、时长、图文类型筛选）②博主主页作品抓取 ③视频/图文评论抓取 ④实时热榜。输出结构化 JSON（含作者、互动数据、标签、链接）。当用户需要搜抖音视频、抓博主作品、看抖音评论、查抖音热榜、做竞品/对标账号监控、短视频选题调研、评论舆情分析、热点追踪、爆款挖掘时使用。触发词：抖音搜索、抖音热榜、抖音评论、抖音作品、博主作品、对标账号、抖音竞品分析、抖音数据分析、短视频运营、抖音舆情监控、抖音热点、舆情监控、热点追踪、爆款挖掘、douyin search、douyin content、douyin post、douyin hot search、douyin comments。
version: 1.3.0
license: MIT
metadata:
  enabled: true
  type: command
  runtime: "nodejs@16.14.0+"
  requires:
    bins:
      - "node"
    env:
      - "GUAIKEI_API_TOKEN"
  env_desc:
    GUAIKEI_API_TOKEN: "抖音数据 API 访问令牌。未配置时无法调用接口；可通过 https://www.guaikei.com 开通，或联系开发者(wx 13395823479)获取支持。"
  category:
    - "Data&APIs"
    - "内容创作"
    - "数据分析"
    - "商业运营"
    - "办公效率"
  tags:
    - "抖音"
    - "douyin"
    - "抖音搜索"
    - "抖音热榜"
    - "抖音评论"
    - "抖音作品"
    - "抖音竞品分析"
    - "抖音数据分析"
    - "短视频运营"
    - "短视频"
    - "舆情监控"
    - "热点追踪"
    - "爆款挖掘"
    - "竞品分析"
    - "营销分析"
    - "search"
    - "数据挖掘"
    - "content-analysis"
    - "competitor-analysis"
    - "marketing"
    - "trend-tracking"
  schemas:
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
  examples:
    - '搜抖音里"AI 教程"最火的视频: node src/douyin/search-cli.js --keyword "AI 教程" --sort 1'
    - '看最近一周抖音上"AI 模型"最新的 20 条内容: node src/douyin/search-cli.js --keyword "AI 模型" --sort 2 --time 7 --limit 20'
    - "查抖音今天有什么热点/热搜榜: node src/douyin/hot-cli.js"
    - '抓这个抖音博主最近 30 条作品: node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx" --limit 30'
    - '看这条抖音视频的 40 条评论: node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx" --limit 40'
---

# 🚀 抖音内容引擎 - 抖音关键词搜索、竞品分析、舆情监控与热榜跟踪工具

## 1. 🛠️ 技能概述

提炼自实战内容创作经验，适用于抖音、小红书等短视频/图文平台的选题策划与标题创作。支持**关键词搜索排序**、**博主作品抓取**、**视频/图文评论抓取**、**实时热榜获取**，输出结构化 JSON，适用于短视频选题、竞品监控、舆情分析、热点追踪。

> **合规前置说明（重要）**：调用本技能会把用户提供的关键词/链接发送至第三方数据 API（域名 `www.guaikei.com`）以换取结果。本技能不上传任何本地文件，不登录任何账号，无任何写操作（不发布/点赞/评论/关注）。仅处理抖音公开数据，不支持私密/登录态数据；数据仅限个人/团队内部分析。

**🔥 核心特性**

- 安全：无需登录抖音账号，无风控/封号风险
- 强大：单次最多可获取 1W 条数据
- 全面：出参覆盖作者、互动、标签、链接等可用数据及有价值数据都会返回
- 轻量：零第三方依赖，Node.js 内置模块直接运行
- 友好：stdout 纯 JSON、日志走 stderr，便于 AI 稳定解析

## 2. ✅ 何时调用与能力边界

**🎯 应调用**：

- 用户明确要查 **抖音** 的公开内容（视频/图文/作者/评论/热榜）。
- 用户要做关键词搜索、爆款选题调研、对标账号监控、评论洞察、热点追流。
- 用户提供了抖音关键词、视频/主页链接，希望拿到结构化数据。

**🚫 不调用**：

- 用户只想要文案/标题/脚本，未要求查抖音数据。
- 平台不是抖音：小红书 / 快手 / B站 / 微博 / 公众号 → 路由到对应技能，**不要用本技能**。
- 要求私密/登录态/隐藏数据。
- 既无关键词也无可识别抖音链接且目标不明 → 先追问。

## 3. 🔀 意图路由决策树（按顺序判断，命中即停）

```
1. 提到"热榜/热搜/热点/今天什么火/榜单"            → hot-cli.js（无需参数）
2. 提到"评论/留言"且指向某个视频                    → comment-cli.js（需视频链接或 aweme_id）
3. 提到"作品/主页/账号/博主/对标账号"                → post-cli.js（需主页链接或 sec_uid）
4. 有关键词且无 1/2/3 的信号                        → search-cli.js（需关键词）
5. 以上都不明确                                     → 先向用户追问，禁止猜测执行
```

> ⚠️ 歧义规则：单独出现"视频"二字时，**不要默认归 post**。有"关键词"且无"评论" → search；"这个视频的评论/留言" → comment；仅当"作品/主页/账号/博主"出现时才用 post。

## 4. 🧺 自然语言 → 命令映射（重要，执行前对照）

执行前先收集足够输入，避免无效调用。

### 4.1 🔍 关键词搜索（search-cli）

至少要确认：`keyword`（2-50 字符）。可选：

- `sort`：0 综合 / 1 最多点赞 / 2 最新发布
- `time`：0 全部 / 1 一天内 / 7 七天内 / 180 半年内
- `duration`：0 不限 / 1 1分钟内 / 2 1-5分钟 / 3 5分钟以上
- `content`：0 不限 / 1 视频 / 2 图文
- `limit`：1-10000，默认 10

| 用户口语化指令                    | 对应命令                                             | 参数推导                    |
| --------------------------------- | ---------------------------------------------------- | --------------------------- |
| "搜一下 / 找 AI 相关视频"         | `node src/douyin/search-cli.js --keyword "AI"`       | 带关键词即搜索              |
| "找点赞最多的 / 最火的 AI 视频"   | `--keyword "AI" --sort 1`                            | 最火/点赞最多 → sort=1      |
| "最新的 AI 教程，要 20 条"        | `--keyword "AI 教程" --sort 2 --limit 20`            | 最新 → sort=2；数量 → limit |
| "近一周最火的短视频"              | `--keyword "短视频" --time 7 --sort 1`               | 一周 → time=7               |
| "半年内最新 20 条 AI 教程"        | `--keyword "AI 教程" --sort 2 --time 180 --limit 20` | 半年 → time=180             |
| "减肥视频，只要 1 分钟以下的"     | `--keyword "减肥" --duration 1`                      | 1分钟以下 → duration=1      |
| "AI 模型，5 分钟以上的，前 50 条" | `--keyword "AI 模型" --duration 3 --limit 50`        | 5分钟以上 → duration=3      |

### 4.2 📡 博主作品（post-cli）

至少要确认：`url`（主页 URL 或 sec_uid）。可选：`limit`（0-10000，默认 10）。
适用链接：`https://www.douyin.com/user/MS4wLjABxxx`、`https://v.douyin.com/xxx`、或直接使用 `sec_uid`。
`limit = 0` 表示获取博主的互动数据（关注数、粉丝数、总获赞数）等信息。

| 用户口语化指令                  | 对应命令                                                                      |
| ------------------------------- | ----------------------------------------------------------------------------- |
| "查看这个博主的所有作品 / 主页" | `node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx"` |
| "抓取 MS4wLjABxxx 的作品"       | `node src/douyin/post-cli.js --url "MS4wLjABxxx"`                             |
| "获取他最近 50 条视频"          | 上面命令加 ` --limit 50`                                                      |

### 4.3 💬 评论分析（comment-cli）

至少要确认：`url`（视频 / 图文 URL 或 aweme_id）。可选：`limit`（1-10000，默认 10）。
适用链接：`https://www.douyin.com/video/xxx`、`https://www.douyin.com/note/xxx`、或直接使用 `aweme_id`。

| 用户口语化指令              | 对应命令                                                                  |
| --------------------------- | ------------------------------------------------------------------------- |
| "看看这个视频的评论 / 留言" | `node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx"` |
| "获取这条视频的 100 条评论" | 上面命令加 ` --limit 100`                                                 |

### 4.4 📡 热榜（hot-cli.js）

| 用户口语化指令                | 对应命令                     |
| ----------------------------- | ---------------------------- |
| "抖音今天有什么热点 / 热搜榜" | `node src/douyin/hot-cli.js` |

## 5. 💡 执行约定

1. 在技能根目录执行；**stdout 只输出 JSON，日志/横幅走 stderr**。
2. **执行前检查清单**：
   - `GUAIKEI_API_TOKEN` 是否已配置？未配置 → 不执行，按 `AUTH_REQUIRED` 话术引导（见第 8 节）。
   - 必填项是否齐全？缺关键词/链接 → 用追问模板，禁止猜测。
3. **耗时预期**：单次调用通常 10-60 秒（任务创建 + 轮询），limit 越大越慢，不要在 30 秒内判定失败或重复执行。
4. **退出码**：`0`=成功（含空结果）、`1`=运行/输入错误、`2`=参数或用法错误、`3`=鉴权失败（缺/错 token）。
5. 空结果（`status:"empty"`）退出码为 0，属正常情况，不是失败。
6. 执行完成后，优先返回：本次目标、关键参数、结构化 JSON 结果，必要时再补一小段摘要。
7. 适合衔接的后续动作：选题汇总、高赞对比、评论观点聚类、竞品内容风格总结、博主发文节奏分析、报告与表格生成。

## 6. 📜 输出契约

所有输出（成功/失败/空结果）都是统一信封结构：

```json
{
  "status": "success | empty | error",
  "error_code": "OK | NO_MATCH | INVALID_KEYWORD | INVALID_URL | INVALID_ARGS | AUTH_REQUIRED | AUTH_ERROR | TIMEOUT | HTTP_5xx | ...",
  "message": "人类可读的说明",
  "timestamp": "2026/9/13 14:30:00",
  "request": {
    "command": "search",
    "keyword": "AI 教程",
    "sort": 1,
    "time": 7,
    "duration": 0,
    "content": 0,
    "limit": 20
  },
  "metadata": {
    "skill_version": "1.3.0",
    "runtime_version": "22.x",
    "execution_time": 34210
  },
  "results": [
    {
      "aweme_id": "7xxx",
      "desc": "视频描述",
      "author_nickname": "作者",
      "author_sec_uid": "MS4wLjABxxx",
      "author_url": "https://www.douyin.com/user/MS4wLjABxxx",
      "digg_count": 123456,
      "comment_count": 8901,
      "share_count": 1200,
      "collect_count": 3400,
      "url": "https://www.douyin.com/video/7xxx",
      "create_time": 1757000000,
      "create_time_str": "2026/9/4 20:13:20",
      "tags": ["#AI"]
    }
  ]
}
```

- `status=error` 时 `results` 为 `null`，错误原因看 `error_code` + `message`。
- `request` 中 `keyword_raw` 为用户原始输入关键词，`keyword` 为清洗后实际使用的关键词，两者不一致时以 `keyword` 为准。
- 各命令 results 元素的完整字段见 `assets/*_resp.schema.json`；完整选项见 [references/options.md](references/options.md)。

## 7. 🤖 错误码 → 应对策略（Agent 必读）

| error_code                     | 退出码 | 含义                               | Agent 应该做什么                                                                          |
| ------------------------------ | ------ | ---------------------------------- | ----------------------------------------------------------------------------------------- |
| `AUTH_REQUIRED` / `AUTH_ERROR` | 3      | token 未配置 / 无效或过期          | **禁止重试**。告知用户需配置 `GUAIKEI_API_TOKEN`，引导到 https://www.guaikei.com 自助开通 |
| `INVALID_KEYWORD`              | 1      | 关键词不合法（长度/链接/特殊符号） | 向用户转述 message，请其更换关键词；禁止自动改词重试                                      |
| `INVALID_URL`                  | 1      | 无法识别链接或 ID                  | 请用户提供：主页链接（post）或视频/图文链接（comment）                                    |
| `INVALID_ARGS`                 | 2      | 参数解析失败                       | 按 --help 用法修正命令后重试一次                                                          |
| `NO_MATCH`（status=empty）     | 0      | 无结果，**不是失败**               | 告知用户；可建议放宽条件（`--time 0`、换更常用词），经用户同意后再试                      |
| `TIMEOUT` / `NETWORK_ERROR`    | 1      | 超时/网络错误                      | 可告知用户后重试，最多 1 次；仍失败则停止并报告                                           |
| `HTTP_5xx` / 其他              | 1      | 服务端或未知错误                   | 如实报告 message，不要编造原因，不要反复重试                                              |

## 8. 🛑 硬性禁止条款

- 不得编造数据；不得把空结果说成有结果。
- 不得在未征得用户同意的情况下自动修改搜索条件重试。
- `AUTH_REQUIRED` / `AUTH_ERROR` 后不得重试。
- 不得把 stderr 中的任何提示文案原样转述给用户（stderr 仅供诊断，对外只报告 `message` 与关键参数）。
- 不得用本技能做登录态、私密数据获取或任何写操作。

## 9. 🧠 追问模板（输入不足时使用）

- 缺关键词：「你想搜索抖音里的什么内容？可以给我一个关键词，例如"AI 教程"。」
- 缺博主链接（post）：「请提供博主主页链接（douyin.com/user/xxx 或 v.douyin.com 短链），或直接给 sec_uid。」
- 缺视频链接（comment）：「请提供视频或图文链接（douyin.com/video/xxx、douyin.com/note/xxx 或 v.douyin.com 短链）。」
- 链接类型不明：「你给的这个链接是想看这个博主的作品，还是这条视频的评论？」

## 10. 🎧 环境、合规与支持

- 环境：Node.js 16.14.0+，Windows/Linux/macOS；必需环境变量 `GUAIKEI_API_TOKEN`（https://www.guaikei.com 自助开通）。
- 配置方式：Windows `set GUAIKEI_API_TOKEN=你的TOKEN`；Linux/macOS `export GUAIKEI_API_TOKEN=你的TOKEN`。
- 合规：仅处理抖音公开数据；数据仅限个人/团队内部分析，禁止违规分发；调用会把关键词/链接发送至第三方 API，使用前请确认数据外发与授权范围。
- 更多帮助：访问 [抖音内容引擎技能官网](https://www.guaikei.com) 。

## 11. ❓ 常见问题

- 没结果：放宽关键词或减少限定（`--time 0`）、换更贴近的词。
- 结果太多：补场景/人群/品牌/时间/账号，控制 limit。
- 调用失败：先确认 token 已配置有效（退出码 3 = token 问题）。
- 账号安全：只读能力，不登录/不发布/不点赞/不评论，无封号风险。
