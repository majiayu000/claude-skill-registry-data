---
name: douyin-bluesea-collector
description: >
  抖音蓝海爆品采集：结合抖音热搜榜与关键词下的视频数据，从小众高需求的细分场景切入找蓝海爆品，避开红海大词竞争。当用户要在抖音找蓝海品、避开大词竞争、从细分场景选品、看抖音热搜、按关键词看视频热度时必须触发。关键词：抖音、蓝海、爆品、细分场景、热搜榜、关键词、选品。
  支持四大能力：
  (1) 关键词搜索视频/图文，可按点赞数、发布时间、时长、内容类型筛选排序；
  (2) 实时热榜查询，获取抖音热搜词条与热度数据；
  (3) 博主作品抓取，按主页链接或 sec_uid 获取公开作品列表；
  (4) 视频评论分析，按视频链接或 aweme_id 获取评论内容与互动数据。
  Use when: 用户需要搜抖音视频、查抖音热榜/热搜、抓取博主作品列表、分析视频评论区、做短视频选题/竞品分析/舆情监控/热点追踪/爆款挖掘/抖音运营数据分析。
  Do NOT use when: 平台非抖音（小红书/B站/微博→对应技能）、需登录态或私密数据、仅要文案创作不需数据查询、既无关键词也无可识别链接且目标不明（先追问）。
  触发词：抖音搜索、抖音热榜、抖音评论、抖音博主、抖音竞品分析、短视频选题、抖音舆情、抖音数据分析、douyin search、douyin analytics、douyin comment。
license: MIT
metadata:
  enabled: true
  type: command
  runtime: "nodejs@16.14.0+"
  version: 1.0.0
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
  tags:
    - "抖音"
    - "douyin"
    - "抖音蓝海"
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
    - "抖音数据"
    - "抖音API"
    - "数据挖掘"
    - "抖音运营工具"
    - "短视频数据"
    - "抖音关键词挖掘"
    - "抖音热点监控"
    - "博主数据分析"
    - "评论区洞察"
    - "爆款视频发现"
    - "content-analysis"
    - "competitor-analysis"
    - "marketing"
    - "trend-tracking"
    - "douyin analytics"
    - "social media monitoring"
    - "social media analytics"
    - "short video"
    - "short video marketing"
    - "influencer tracking"
    - "trend analysis"
    - "content discovery"
    - "video search"
    - "viral content"
    - "social listening"
    - "api wrapper"
    - "data scraping"
    - "market research"
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
    - "搜索抖音'AI教程'最火视频: node src/douyin/search-cli.js --keyword 'AI教程' --sort 1"
    - "查看最近一周'AI模型'最新20条内容: node src/douyin/search-cli.js --keyword 'AI模型' --sort 2 --time 7 --limit 20"
    - "查抖音今天热搜榜: node src/douyin/hot-cli.js"
    - "抓取某博主最近30条作品: node src/douyin/post-cli.js --url 'https://www.douyin.com/user/MS4wLjABxxx' --limit 30"
    - "分析某条抖音视频40条评论: node src/douyin/comment-cli.js --url 'https://www.douyin.com/video/xxx' --limit 40"
---

# 抖音蓝海爆品采集助手

## 1. 🛠️ 技能概述

抖音蓝海爆品采集：结合抖音热搜榜与关键词下的视频数据，从小众高需求的细分场景切入找蓝海爆品，避开红海大词竞争。支持**关键词搜索排序**、**博主作品抓取**、**视频评论分析**、**实时热榜获取**，适用于短视频选题、竞品监控、舆情分析、热点追踪，助力爆款内容策划与流量运营。

> **🔥核心优势**
>
> - **安全**：无需登录抖音账号，无风控 / 封号风险
> - **强大**：单次最多可获取 1W 条数据，内置批量与多维筛选
> - **全面**：出参覆盖作者、互动、标签、链接等可用数据及有价值数据都会返回
> - **轻量**：无需部署服务，Node.js 一键运行，仅依赖内置模块
> - **友好**：stdout 纯 JSON、日志走 stderr，便于 AI 稳定解析与二次分析

## 2. ✅ 何时调用与能力边界

### 🎯 在以下场景优先调用：

- 用户明确要查 **抖音** 的公开内容（视频 / 图文 / 作者 / 评论 / 热榜）。
- 用户要做 **关键词搜索**、**爆款选题调研**、**竞品监控**、**评论洞察**、**博主作品追踪**、**热点追流**。
- 用户提供了抖音关键词、视频链接、博主主页链接，希望拿到结构化数据。
- 用户后续还要基于结果做总结、对比、筛选、报告生成。

### 🚫 不应调用

- 用户只想要文案/标题/脚本，未要求查抖音数据。
- 平台不是抖音（小红书、B站、微博、公众号）→ 路由到对应技能。
- 要求私密/登录态/隐藏数据。
- 既无关键词也无可识别抖音链接且目标不明 → 先追问。

### ✅ 擅长处理（直接执行）

- 按关键词搜索抖音视频/图文，支持排序与多维筛选
- 查询抖音实时热榜词条与热度数据
- 按博主主页链接或 sec_uid 获取公开作品列表
- 按视频/图文链接或 aweme_id 获取评论内容
- 基于获取到的数据做总结、对比、聚类等二次分析

### ⚠️ 需素材才能做

- 关键词搜索：需用户提供 2-50 字符的关键词
- 博主作品抓取：需用户提供博主主页 URL 或 sec_uid
- 评论分析：需用户提供视频/图文 URL 或 aweme_id
- 批量数据获取：需用户明确指定 limit 参数

### ❌ 超出范围（不做，引导替代方案）

- 非抖音平台数据 → 路由到小红书/B站/微博对应技能
- 登录态/私密/隐藏数据 → 不支持，仅处理公开数据
- 发布/点赞/评论/关注等写操作 → 不支持，安全只读
- 替用户做营销策略决策 → 拿回数据后交上层分析
- 文案/标题/脚本创作 → 查到数据后可辅助，但不代替创作技能

> 意图不明确时先追问，不要盲目执行命令。

### 🛑 本技能不需要、不负责：

登录账号、发布/点赞/评论/关注等写操作、获取非公开数据、替用户做营销策略判断。职责是**先把数据拿回来**，再交上层分析。

## 3. 🔀 调用路由

> **Note:** 请先通过 [抖音数据获取官网](https://www.guaikei.com) 开通并配置环境变量 `GUAIKEI_API_TOKEN` 后，再按意图路由：

| 意图             | 脚本                        | 必填                 | 典型结果                        |
| ---------------- | --------------------------- | -------------------- | ------------------------------- |
| 搜关键词内容     | `src/douyin/search-cli.js`  | `keyword`            | 视频/图文列表、作者、互动、链接 |
| 看热搜/热点/榜单 | `src/douyin/hot-cli.js`     | 无                   | 热榜词条、热度、搜索量          |
| 看博主最近作品   | `src/douyin/post-cli.js`    | 主页 URL 或 sec_uid  | 博主公开作品列表                |
| 看视频/图文评论  | `src/douyin/comment-cli.js` | 视频 URL 或 aweme_id | 评论内容、评论者、互动          |

### 🧭 消歧义（重要）

- 单独出现"视频"二字时，不要默认归 `post`。
- 有"关键词"且无"评论" → `search`（用户想搜某个视频）。
- "这个视频的评论/留言" → `comment`。
- 仅当"作品/主页/账号/博主"出现时才用 `post`。

## 4. 🧺 输入收集规则

执行前先收集足够输入，避免无效调用。

### 4.1 🔍 关键词搜索（search-cli）

至少要确认：`keyword`（2-50 字符）。可选：

- `sort`：0 综合 / 1 最多点赞 / 2 最新发布
- `time`：0 全部 / 1 一天内 / 7 七天内 / 180 半年内
- `duration`：0 不限 / 1 1分钟内 / 2 1-5分钟 / 3 5分钟以上
- `content`：0 不限 / 1 视频 / 2 图文
- `limit`：1-10000，默认 10

### 4.2 📡 博主作品（post-cli）

至少要确认：`url`（主页 URL 或 sec_uid）。可选：`limit`（1-10000，默认 10）。
适用链接：`https://www.douyin.com/user/MS4wLjABxxx`、`https://v.douyin.com/xxx`、或直接使用 `sec_uid`。

### 4.3 💬 评论分析（comment-cli）

至少要确认：`url`（视频 / 图文 URL 或 aweme_id）。可选：`limit`（1-10000，默认 10）。
适用链接：`https://www.douyin.com/video/xxx`、`https://www.douyin.com/note/xxx`、或直接使用 `aweme_id`。

## 5. 📜 执行与输出约定

- 在技能根目录执行；只输出纯 JSON 到 stdout，日志/banner 走 stderr。
- 没有关键词：先追问关键词。
- 没有链接：先追问视频 / 主页链接或 ID。
- 链接类型不明确：先确认这是视频还是博主主页。
- 没有 `GUAIKEI_API_TOKEN`：提醒用户先配置环境变量，再执行。
- 退出码：`0`=成功（含 empty），`1`=运行错误（接口异常/网络/超时），`3`=auth_required（缺/错 token）。
- 失败须向用户说明原因，**不编造数据，不把空结果当成功**。空结果退出码 0 属正常。
- 完整选项见 可参阅 [完整选项说明](references/options.md) ；LLM理解技能的详细选项，可参阅技能 `assets` 目录中文件。
- 执行完成后，优先返回：本次目标、关键参数、结构化 JSON 结果，必要时再补一小段摘要。
- 适合衔接的后续动作：选题汇总、高赞对比、评论观点聚类、竞品内容风格总结、博主发文节奏分析、报告与表格生成。

## 6. 💡 调用示例

```bash
node src/douyin/search-cli.js --keyword "AI 教程" --sort 1
node src/douyin/search-cli.js --keyword "AI模型" --sort 2 --time 7 --limit 20
node src/douyin/hot-cli.js
node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx" --limit 50
node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx" --limit 100
```

- 🤖 自然语言触发示例："帮我搜抖音里'AI 教程'最火的视频""抖音今天有什么热点""分析这条抖音视频评论区的主要观点"。
- 🧠 若用户表达笼统（如"帮我做抖音竞品分析"），优先拆成两步：① 确认关键词 / 竞品链接 / 博主主页；② 再调用对应脚本拿回数据。

## 7. 🎧 环境、合规与支持

- 环境：Node.js 16.14.0+，兼容 Windows/Linux/macOS；必需 `GUAIKEI_API_TOKEN`；官网 <https://www.guaikei.com>。
- 合规：仅处理抖音公开数据，不支持私密/隐藏/登录态数据；数据仅限个人/团队内部分析，禁止违规分发；依赖第三方 API（guaikei.com），使用前确认数据外发与授权范围。
- 支持：官网 <[抖音搜索技能官网](https://www.guaikei.com)>（自助开通 TOKEN）；微信 `13395823479`（备注：抖音技能）。

## 8. ❓ 常见问题

- 没结果：放宽关键词或减少限定（`--time 0`）、换更贴近的词。
- 结果太多：补场景/人群/品牌/时间/账号。
- 调用失败：先确认 `GUAIKEI_API_TOKEN` 已配置有效（退出码 3 即 token 问题）。
- 账号安全：只读能力，不登录/发帖/点赞/评论。
- Q: 获取的数据包含用户个人信息吗？
  A: 仅获取抖音公开可见数据（昵称、公开作品、评论内容等）。
  不收集手机号、位置、私信等隐私信息。数据通过第三方
  API（guaikei.com）获取，使用前请确认数据外发与授权范围。

- Q: 数据可以公开发布或商用吗？
  A: 数据仅限个人/团队内部分析使用。如需商用或公开发布，
  请确认已获得相应授权，并对用户昵称等个人信息做脱敏处理
  （如打码、化名替换）。

- Q: API Token 会被泄露吗？
  A: Token 仅存储在本地环境变量中，不会出现在 stdout 输出中。
  日志走 stderr 且不包含 Token 明文。但仍建议不要在公共
  场合展示终端输出。
