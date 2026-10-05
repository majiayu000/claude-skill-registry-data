---
name: tiktok-skill
description: 用于 TikTok 达人数据、TikTok 达人作品、TikTok KOL 作品列表、TikTok 博主视频列表、TikTok 网红近期发布、TikTok 内容调研和创作者内容分析。支持三大能力：(1) 关键词搜索 TikTok 视频，可按最多点赞、相关度排序，并按发布时间筛选；(2) 博主作品抓取，按主页链接或用户名批量获取公开作品列表，支持最新/最热排序；(3) 视频评论分析，按视频链接或作品 ID 获取评论内容、评论者与互动数据。无需登录账号，只读公开数据，输出结构化 JSON 供 AI 直接做选题、竞品监控与舆情分析。
license: MIT
version: 1.0.0
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
    GUAIKEI_API_TOKEN: "TikTok 数据 API 访问令牌（长度 16-256，仅含字母、数字、下划线、连字符）。可通过 https://www.guaikei.com 自助开通，或联系开发者微信 13395823479（备注：TikTok 技能）获取支持。"
  category:
    - "Data&APIs"
    - "内容创作"
    - "数据分析"
    - "商业运营"
  tags:
    - "TikTok"
    - "tiktok"
    - "TikTok数据"
    - "TikTok搜索"
    - "TikTok评论"
    - "TikTok作品"
    - "TikTok达人"
    - "TikTok达人数据"
    - "TikTok达人作品"
    - "TikTokKOL"
    - "TikTokKOL作品"
    - "TikTok博主"
    - "TikTok博主作品"
    - "TikTok网红"
    - "TikTok竞品分析"
    - "TikTok数据分析"
    - "TikTok选题"
    - "TikTok爆款"
    - "TikTok视频下载"
    - "TikTok运营工具"
    - "TikTok关键词挖掘"
    - "TikTok舆情"
    - "TikTok内容分析"
    - "评论区洞察"
    - "短视频运营"
    - "短视频数据"
    - "海外短视频"
    - "跨境营销"
    - "海外社媒"
    - "红人营销"
    - "KOL筛选"
    - "网红筛选"
    - "竞品分析"
    - "营销分析"
    - "content-analysis"
    - "competitor-analysis"
    - "influencer-tracking"
    - "social-listening"
    - "social-media-analytics"
    - "short-video"
    - "short-video-marketing"
    - "content-discovery"
    - "video-search"
    - "viral-content"
    - "market-research"
    - "data-scraping"
    - "api-wrapper"
  schemas:
    - name: "搜索入参"
      file: "assets/search_cli_req.schema.json"
    - name: "搜索出参"
      file: "assets/search_cli_resp.schema.json"
    - name: "作品入参"
      file: "assets/post_cli_req.schema.json"
    - name: "作品出参"
      file: "assets/post_cli_resp.schema.json"
    - name: "评论入参"
      file: "assets/comment_cli_req.schema.json"
    - name: "评论出参"
      file: "assets/comment_cli_resp.schema.json"
  examples:
    - "搜索 TikTok 上 AI 相关最火视频: node scripts/tiktok/search-cli.js --keyword 'AI' --sort 1 --limit 20"
    - "查最近一周 AI 模型 20 条内容: node scripts/tiktok/search-cli.js --keyword 'AI model' --time 7 --limit 20"
    - "抓取某博主最热的 30 条作品: node scripts/tiktok/post-cli.js --url 'https://www.tiktok.com/@username' --sort 1 --limit 30"
    - "抓取某博主最近 30 条作品: node scripts/tiktok/post-cli.js --url 'https://www.tiktok.com/@username' --limit 30"
    - "分析某条视频 40 条评论: node scripts/tiktok/comment-cli.js --url 'https://www.tiktok.com/@username/video/1234567890123456789' --limit 40"
---

# TikTok数据技能 · TikTok搜索 · KOL作品 · 作品评论

## 1. 能力概览

一句话：**把 TikTok 的公开内容（搜索结果 / 博主作品 / 视频评论）拿回来，输出成 AI 可直接消费的结构化 JSON。**

| 能力       | 入口脚本                        | 必填参数                 | 返回                                                |
| ---------- | ------------------------------- | ------------------------ | --------------------------------------------------- |
| 关键词搜索 | `scripts/tiktok/search-cli.js`  | `--keyword`              | 作品列表：作者、点赞/评论/分享/收藏、标签、播放地址 |
| 博主作品   | `scripts/tiktok/post-cli.js`    | `--url`（主页或用户名）  | 该博主公开作品列表（支持最新 / 最热排序）           |
| 视频评论   | `scripts/tiktok/comment-cli.js` | `--url`（视频链接或 ID） | 评论正文、评论者、点赞数、回复数、IP 归属地         |

> **前置条件**：必须在**技能根目录**执行，且环境变量 `GUAIKEI_API_TOKEN` 已配置。未配置时所有命令返回退出码 `3`、`error_code=AUTH_REQUIRED`——此时**直接提示用户配置 Token，不要重试、不要换参数**。

---

## 2. 何时调用 / 何时不调用

### 2.1 应该调用

- 用户要查 **TikTok** 的公开内容（视频 / 图文 / 作者 / 评论 / 趋势）。
- 用户要做**爆款选题调研、竞品账号监控、红人筛选、评论舆情分析、内容风格拆解**。
- 用户已给出 TikTok 关键词、视频链接、博主主页链接，希望拿到结构化数据。
- 用户拿到数据后还要继续做总结、对比、排序、聚类、出报告 / 表格。

### 2.2 不应调用

- 用户只要文案 / 标题 / 脚本，没有要查 TikTok 数据。
- 平台不是 TikTok（抖音、小红书、B 站、微博、公众号）→ 路由到对应技能。**本技能只处理 TikTok。**
- 要求登录态、私密、隐藏数据 → 不支持。
- 既有关键词又有可识别链接且目标不明 → **先追问，不要猜**。

### 2.3 能力边界（明确不做）

发布 / 点赞 / 评论 / 关注 / 私信等**写操作**一律不支持；不登录任何账号；不采集手机号、位置、私信等隐私字段；不替用户做营销决策——职责是把数据拿回来，分析交给上层。

---

## 3. 调用路由（先判断，再执行）

| 用户意图                                           | 脚本          | 判定关键词                                    |
| -------------------------------------------------- | ------------- | --------------------------------------------- |
| 搜关键词、找某类内容、找爆款                       | `search-cli`  | 搜索 / 找 / 关键词 / 爆款 / 最火              |
| 看某博主 / 达人 / 网红的作品、主页、账号、近期发布 | `post-cli`    | 作品 / 主页 / 账号 / 博主 / 达人 / 网红 / KOL |
| 看某条视频的评论、留言                             | `comment-cli` | 评论 / 留言 / 评论区的观点                    |

### 3.1 消歧义规则（必须遵守）

1. **单独出现"视频"二字，不要默认归 `post-cli`**。
   - 有"关键词"且无"评论" → `search-cli`（用户想搜这类视频）。
   - 明确"这个视频的评论 / 留言" → `comment-cli`。
   - 只有出现"作品 / 主页 / 账号 / 博主 / 达人" → `post-cli`。
2. **评论优先级高于作品**：若给的链接是 `/video/<id>` 且问的是评论 → `comment-cli`；若问的是"这个人的作品" → `post-cli`（用 `@username`）。
3. 用户给了 `/video/<id>` 链接却要"作品列表" → 先确认是要该作者的作品还是该视频的评论。

### 3.2 参数推断规则

| 用户说法                      | 参数                       |
| ----------------------------- | -------------------------- |
| 相关度 / 默认                 | `--sort 0`（搜索）         |
| 最火 / 点赞最多 / 爆款 / 最热 | `--sort 1`（搜索）         |
| 最近发的 / 按时间倒序         | `--sort 0`（作品）         |
| 最热的作品                    | `--sort 1`（作品）         |
| 一天 / 24 小时                | `--time 1`                 |
| 一周 / 7 天                   | `--time 7`                 |
| 一个月 / 三个月 / 半年        | `--time 30` / `90` / `180` |
| N 条 / 前 N 条 / 要 N 个      | `--limit N`                |

默认值：`sort=0`、`time=0`、`limit=10`。

> ⚠️ **搜索的 `--sort` 与作品的 `--sort` 不要混用**：前者是"相关度 / 最多点赞"，后者是"最新 / 最热"。

**任何参数被非法值回退，都会出现在输出 JSON 的 `warnings` 数组里，必须回显给用户，不要当成原样生效。**

---

## 4. 执行方式

> 完整参数说明见 [references/options.md](references/options.md)；字段级 Schema 见 `assets/` 下的 6 个 JSON Schema（draft-07）。

```bash
# 关键词搜索
node scripts/tiktok/search-cli.js --keyword "AI" --sort 1 --limit 20
node scripts/tiktok/search-cli.js --keyword "AI model" --time 7 --limit 20

# 博主作品
node scripts/tiktok/post-cli.js --url "https://www.tiktok.com/@username" --limit 30
node scripts/tiktok/post-cli.js --url "https://www.tiktok.com/@username" --sort 1 --limit 30

# 视频评论
node scripts/tiktok/comment-cli.js --url "https://www.tiktok.com/@username/video/1234567890123456789" --limit 40
```

**可用的输入形态**

- 博主：`https://www.tiktok.com/@username`、带参数链接 `https://www.tiktok.com/@username?lang=en`、或直接 `author_sec_uid`
- 视频：`https://www.tiktok.com/@username/video/<id>`、短链、或直接作品 `<id>`

**执行纪律**

- 只把 **stdout** 当机器可读输出（纯 JSON）；banner / 进度 / 错误日志都在 **stderr**，不要混在一起解析。
- 单次 `--limit` 建议 **≤ 1000**。
- 不要因为一次空结果就自动放宽条件重试：**先把空结果告诉用户**，由用户决定是否换关键词 / 放宽 `--time`。

---

## 5. 输出契约（AI 解析必读）

所有入口输出**同一个信封**，成功与失败结构一致：

```json
{
  "status": "success | empty | error",
  "error_code": "OK | NO_MATCH | AUTH_REQUIRED | INVALID_KEYWORD | ...",
  "message": "人类可读说明",
  "timestamp": "2026-09-16 21:00:00",
  "request": {
    "command": "search",
    "keyword": "AI",
    "sort": 1,
    "time": 0,
    "limit": 20
  },
  "metadata": {
    "skill_version": "1.0.0",
    "skill_name": "tiktok-creator-videos",
    "runtime_version": "22.22.2",
    "execution_time": 8421
  },
  "results": [],
  "warnings": ["数量 99999 无效，已回退为 10"]
}
```

### 5.1 `status` 语义

| status    | 含义                       | `results` | 该怎么做                                   |
| --------- | -------------------------- | --------- | ------------------------------------------ |
| `success` | 拿到数据                   | 非空数组  | 直接分析                                   |
| `empty`   | **请求成功，但确实没数据** | `null`    | 视为有效结果，告知用户没搜到，不要当成失败 |
| `error`   | 请求失败                   | `null`    | 按 `error_code` 处理，不要编造数据         |

### 5.2 退出码

| 退出码 | 含义                                          | Agent 行为                                           |
| ------ | --------------------------------------------- | ---------------------------------------------------- |
| `0`    | 成功（`success` 或 `empty`）                  | 继续分析                                             |
| `1`    | 运行错误（网络 / 超时 / 接口异常 / 参数非法） | 展示 `message`，询问用户是否换参数重试               |
| `3`    | `AUTH_REQUIRED`：Token 缺失或格式错误         | **立即停止**，提示配置 `GUAIKEI_API_TOKEN`，禁止重试 |

### 5.3 错误码处理

| error_code        | 处理方式                                                 |
| ----------------- | -------------------------------------------------------- |
| `AUTH_REQUIRED`   | 停止并提示配置 Token。禁止重试、禁止改参数绕行           |
| `INVALID_KEYWORD` | 提示关键词需 2–100 字符、不能含 `< > " ' &` 与 http 链接 |
| `NO_MATCH`        | 有效空结果，建议换关键词或放宽 `--time`                  |
| `NETWORK_ERROR`   | 已内置重试；仍失败则提示检查网络，最多手动重试 1 次      |
| `TIMEOUT_ERROR`   | 已内置重试；仍失败则建议降低 `--limit` 后重试            |
| 其它（服务端码）  | 原样展示 `error_code` + `message`，不要自行猜测含义      |

### 5.4 `warnings` 必须回显

当传入参数不合法被自动回退时（如 `--sort 9`、`--limit 99999`），`warnings` 数组会说明"哪个参数被改成了什么"。**必须原样转告用户**，不能假装参数按原值生效了。

### 5.5 禁止行为

- ❌ 不编造、不补全、不凭记忆填充任何数据。
- ❌ 收到 `AUTH_REQUIRED` 后不重试、不换脚本、不改参数。
- ❌ 不把 `empty` 当成"用户要的内容不存在"以外的结论（不等于接口坏了）。
- ❌ 不在用户未同意时自动放宽搜索条件。

---

## 6. 结果消费建议（提升最终交付质量）

拿到 `results` 后，按用户原始目标组织输出，而不是原样吐 JSON：

- **选题调研** → 按 `digg_count` 降序取 Top N，归纳标题句式 / 标签 / 时长分布规律
- **竞品监控** → 按 `create_time` 排发布节奏，统计更新频率与爆款占比
- **评论洞察** → 按 `digg_count` 取高赞评论做观点聚类，输出正负向占比
- **红人筛选** → 交叉 `author_nickname` / 平均互动 / 发布频次，给出候选清单
- **需要留档** → 每次运行会自动写入日志文件，路径在 stderr 的"已保存到 …"一行

---

## 7. 安全与合规（Trust）

- **只读**：不登录 TikTok 账号，不执行发布 / 点赞 / 评论 / 关注 / 私信等任何写操作，无风控封号风险。
- **最小权限**：仅请求业务所需的一个环境变量 `GUAIKEI_API_TOKEN`；不读取本地其他文件、不写技能目录以外路径（日志写入系统临时目录）。
- **凭据保护**：Token 只从环境变量读取，不写入 stdout、不写进日志、不出现在错误信息里。
- **数据外发范围（务必知悉）**：调用时会向 `https://www.guaikei.com` 发送：你的 **API Token**、**查询关键词**或**目标 URL/ID**，以及技能名与 Node 版本。除此之外不采集任何本地信息。
- **数据合规**：仅获取 TikTok 公开可见数据（昵称、公开作品、公开评论）。不含手机号、位置、私信等隐私字段。数据仅限个人 / 团队内部分析；对外发布或商用前请自行确认授权，并对用户昵称等做脱敏处理。
- **无第三方依赖**：仅使用 Node.js 内置模块（`https` / `fs` / `path` / `os` / `querystring`），无 npm 依赖、无远程脚本加载、无 `eval` / `child_process`。

---

## 8. 常见问题

| 现象                            | 原因与处理                                                                   |
| ------------------------------- | ---------------------------------------------------------------------------- |
| 退出码 3 / AUTH_REQUIRED        | Token 未配置或格式不对（需 16–256 位字母数字下划线连字符）                   |
| 搜索结果为空                    | 换更通用的关键词，或 `--time 0` 放开时间窗；`empty` 是正常结果不是错误       |
| 结果条数少于 `--limit`          | 服务端无可返回更多，或单次上限被截断；降到 ≤ 1000 分批取                      |
| 一直超时                        | 减小 `--limit` 后重试；脚本已内置指数退避重试                                |
| 想看"最热作品"却按时间倒序      | `post-cli` 要用 `--sort 1`                                                   |
| 参数没生效 / 结果与预期排序不同 | 检查输出里的 `warnings`，参数不合法时会被静默回退为默认值                    |
| 日志文件在哪                    | 见 stderr 中"已保存到 …"那一行（系统临时目录 `tiktok-guaikei/logs/<日期>/`） |

## 9. 环境与支持

- 环境：Node.js ≥ 16.14.0，Windows / macOS / Linux 全平台；必需 `GUAIKEI_API_TOKEN`。
- 官网：<https://www.guaikei.com>（自助开通 Token、查阅用量与接口说明）。
- 支持：微信 `13395823479`（备注：TikTok 技能）。
- 变更记录：[references/changelog.md](references/changelog.md)
