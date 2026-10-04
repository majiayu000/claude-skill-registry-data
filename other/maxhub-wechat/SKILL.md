---
slug: wechat-pro
displayName: 微信数据助手 | 公众号 / 视频号 / 文章 / 评论
name: wechat-pro
description: 微信公众号（WeChat Official Accounts）公开内容查询与文章分析 skill，通过 MaxHub API 查询公众号文章、账号信息、评论、阅读互动、视频/媒体相关数据和搜索能力。适合公众号内容选题、舆情分析、账号画像、评论研究和媒体监控。默认 read-only，但部分媒体/评论数据具有隐私和版权敏感性；agent 应按 recipes 调用并遵守数据最小化与授权边界。所有请求发送到 https://www.aconfig.cn。
license: MIT-0
metadata:
  author: maxhub
  version: 4.1.4
  openclaw:
    capability: read_only
    requires_confirmation:
    - non_idempotent
    - cookie_input
    emoji: 💬
    primaryEnv: MAXHUB_API_KEY
    requires:
      env:
      - MAXHUB_API_KEY
      bins:
      - curl
    env:
    - name: MAXHUB_API_KEY
      description: 微信公众号（WeChat Official Accounts）公开内容查询与文章分析 skill，通过 MaxHub API 查询公众号文章、账号信息、评论、阅读互动、视频/媒体相关数据和搜索能力。适合公众号内容选题、舆情分析、账号画像、评论研究和媒体监控。默认 read-only，但部分媒体/评论数据具有隐私和版权敏感性；agent 应按 recipes 调用并遵守数据最小化与授权边界。所有请求发送到 https://www.aconfig.cn。
      required: true
      sensitive: true
    network:
    - https://www.aconfig.cn
    riskLevel: low
    defaultMode: recipes_first_read_only
    skillClass: maxhub-api-skill
    platform: wechat
    authType: bearer_env
    dataSource: MaxHub API via https://www.aconfig.cn
    agentUse:
      entrypoint: SKILL.md §4 Agent Decision Tree
      intentIndex: references/recipes/_index.md
      chainDetails: references/recipes/<domain>.md
      fieldFlow: references/param-mappings.md
      endpointWhitelist: references/endpoints_whitelist.yaml
      selectionPolicy: recipes_first_then_atoms; longest_trigger_match; ask_on_tie
      parameterPolicy: use recipe extract/in_map and field-flow dictionary; never invent path or parameters
    privacy:
      thirdParty: https://www.aconfig.cn
      transmits:
      - MAXHUB_API_KEY
      - user_supplied_ids
      - keywords
      - urls
      - optional_cookies_or_tokens
      guidance: Use only for authorized data processing; minimize personal data; do not expose secrets in logs or prompts.
  hermes:
    tags:
    - wechat
    - 微信公众号
    - 公众号文章
    - 评论
    - 账号信息
    - 阅读互动
    - 搜索
    - 媒体监控
    category: data-analysis
    intents:
    - query
    - analyze
    - search
    - chain
    - report
    locale:
    - zh-CN
    - en
---

> ⛔ **合规硬前置指令（HARD PREREQUISITE — Agent 不得跳过）**
>
> 在执行任何 API 调用、读取 reference 文件、匹配 recipe 之前，Agent **必须**先完成 §基础使用 Step 0 的合规检查。
>
> - **禁止**绕过 Step 0 直接进入 Step 1（检查 API Key）或更后续步骤
> - **禁止**以"用户已多次使用"为由跳过首次闸门或风险检测
> - **禁止**将 Step 0 的合规检查视为可选步骤
> - 若 Step 0 未通过（首次确认缺失、用户拒绝、风险检测未确认），**立即停止**，不执行任何后续操作
>
> 违反此指令将导致法律合规风险，Agent 必须严格执行。

# 微信数据助手

## 1. 简介

微信公众号（WeChat Official Accounts）公开内容查询与文章分析 skill，通过 MaxHub API 查询公众号文章、账号信息、评论、阅读互动、视频/媒体相关数据和搜索能力。适合公众号内容选题、舆情分析、账号画像、评论研究和媒体监控。默认 read-only，但部分媒体/评论数据具有隐私和版权敏感性；agent 应按 recipes 调用并遵守数据最小化与授权边界。所有请求发送到 https://www.aconfig.cn。

> ### 🚨 高风险平台警告 — 微信
>
> **微信生态数据抓取存在显著法律风险，请谨慎使用：**
>
> - **法律打击**：腾讯已多次对第三方公众号内容抓取工具发律师函，并采取民事诉讼和刑事报案
> - **通讯数据保护**：微信视频号、公众号数据涉及用户社交关系链，中国法律对此类数据保护更为严格
> - **微信 ToS**：微信服务协议明确禁止第三方自动化抓取公众号内容、视频号数据
> - **全部 POST 端点**：本 skill 所有端点均为 POST 请求（参数在请求体），表明数据获取非官方渠道
> - **建议**：优先使用 [微信开放平台](https://open.weixin.qq.com) 官方 API

## 2. 详细功能

### 公众号文章
- 通过文章链接还原公众号图文文章的完整正文，包括标题、作者、发布时间、富文本内容、配图
- 拉取文章的阅读量、在看数、点赞数、分享数等互动统计数据
- 拉取文章下的留言区评论与作者精选评论列表
- 拉取被精选评论的多层回复，还原完整对话
- 拉取与该文章相关联的延伸阅读推荐文章列表
- 获取文章内嵌的广告物料信息，用于商业内容研究

### 公众号账号
- 查询任意公众号的账号资料，包括账号名、简介、认证主体、头像、二维码等画像信息
- 分页拉取该公众号的历史文章列表，按时间倒序回溯全部发文记录
- 查询公众号开通的服务列表（菜单、商城、小程序等），构建账号矩阵全景

### 视频号视频
- 查询视频号视频的完整详情，包括标题、文案、封面、视频流地址、互动数据
- 支持通过视频对象 ID、导出 ID、分享链接三种入口反查同一条视频
- 拉取视频号视频下的评论列表，分析受众反馈与情感倾向
- 获取视频的对外分享链接，便于侧链分析与跨平台引流追踪
- 拉取某个视频号账号下的全部视频列表，用于内容矩阵盘点

### 视频号账号与合集
- 查询视频号账号的基本信息，包括账号名、简介、粉丝数、认证主体
- 查询视频号创作者的主页资料，构建独立的视频号 KOL 画像
- 拉取该视频号账号下的合集（专辑）列表
- 拉取某个合集内的全部视频，追踪连载/系列化内容
- 在某个视频号账号内按关键词搜索其历史视频

### channel_id ↔ username 互转
- 把视频号短号（sph 短号 / channel_id）解析为标准账号用户名，解决跨入口数据互通问题

### 视频号直播
- 拉取某个视频号账号的历史直播列表，识别直播节奏与开播规律
- 查询某场直播的完整详情，包括直播标题、开播时间、回放链接、互动数据

### 微信搜一搜
- 通过搜一搜入口在微信生态内统一检索内容，支持公众号文章与视频号视频两种业务类型切换
- 一次搜索即可定位候选公众号、候选视频号、候选文章/视频，作为后续画像采集的入口

### 账号余额查询
- 查询 MaxHub API 账号剩余额度，支持 `x-api-key` 或 `Authorization: Bearer` 两种认证方式
- 频率限制：最快每 3 秒调用一次
- 接口路径：`GET /api/maxhub/balance`

## ⚖️ 法律免责与合规声明

> **使用本 skill 即表示您确认已阅读并同意以下条款：**
>
> 1. **数据来源**：本 skill 通过第三方数据服务（MaxHub API）获取 微信（WeChat） 数据，该服务**未获得 微信（WeChat） 官方授权**。本项目对数据获取的合法性不作任何保证。
> 2. **合规责任**：使用方需**自行确保**符合所在地区的数据保护法律（《个人信息保护法》/ GDPR / CCPA 等）及 微信（WeChat） 服务条款（ToS）。因使用本 skill 产生的任何法律后果由使用方自行承担。
> 3. **禁止用途**：严禁将本 skill 用于违反法律的行为，包括但不限于：侵犯个人信息权、不正当竞争、刷量操控、批量爬取用户数据等。
> 4. **平台风险**：腾讯对未授权的微信生态数据抓取有积极的法律打击行动（律师函、民事诉讼、刑事报案），微信服务协议明确禁止第三方自动化抓取。
> 5. **完整政策**：详细数据使用政策请参阅 [DATA_USAGE_POLICY.md](./DATA_USAGE_POLICY.md)。

> ### 📋 数据传输与隐私声明（请认真阅读）
>
> 1. **第三方传输**：您提供的所有 ID、关键词、链接、cookie 等参数都会通过 HTTPS 发送到 **`https://www.aconfig.cn`**（MaxHub 数据服务）进行处理。
> 2. **UGC 隐私**：拉回的 公众号文章 / 评论 / 视频号内容 等内容可能包含个人信息或敏感 UGC，请勿写入未授权的数据库或公开发布。
> 3. **凭证保护**：建议使用**独立测试账号**、定期轮换 API Key；**禁止**传入主力生产账号的 cookie 或 session 凭证。
> 4. **合规责任**：使用方需自行确保符合所在地区的数据保护法律（《个人信息保护法》/ GDPR / 微信（WeChat） ToS 等），平台账号的合规性由使用方承担。

## 3. 一键安装

### 鉴权

#### 获取 API Key

请前往 [MaxHub 控制台](https://www.aconfig.cn) 注册账号并获取 API Key。

#### 配置 API Key

**方案 1：OpenClaw 配置**

将 `MAXHUB_API_KEY` 添加到 `~/.openclaw/openclaw.json` 中：

```json
{ "env": { "MAXHUB_API_KEY": "ak_xxxx..." } }
```

**方案 2：终端环境变量**

```bash
export MAXHUB_API_KEY="ak_xxxx..."
```

### 依赖安装

本 Skill 不需要额外脚本依赖，所有调用通过 `curl` 完成 HTTP 请求即可，无第三方库依赖。

### 环境变量配置

| 环境变量 | 说明 | 是否必填 | 获取方式 |
|---|---|---|---|
| `MAXHUB_API_KEY` | MaxHub 数据 API Key | 是 | [MaxHub 控制台](https://www.aconfig.cn) |

## 4. 使用指南


### 🤖 Agent Decision Tree（必读 · 决定调用顺序）

> 此小节定义 agent 在每次接到用户请求时的**标准决策流程**。严格按此顺序执行可大幅提升命中率与减少误调用。

#### 1️⃣ 文档加载顺序（按需 · 不要一次性全读）
| 步骤 | 何时读 | 加载文件 | 估算 token |
|------|-------|---------|-----------|
| ① 永远先读 | 接到任何请求时 | `SKILL.md` §0.1（不支持清单）+ §4（本节） | ~1K |
| ② 选择 recipe | 用户语义清晰时 | `references/recipes/_index.md`（仅索引） | ~1.5K |
| ③ 加载 recipe 详情 | 匹配到具体 recipe 时 | `references/recipes/<domain>.md` 的对应段落 | ~500/段 |
| ④ 加载端点详情 | 自定义链路或参数不明时 | `references/<domain>.md` 单文件 | ~3K |
| ⑤ 路径白名单校验 | 调用前 | `grep '<endpoint_id>' references/endpoints_whitelist.yaml`（**禁止整体读**） | ~50 行 |
| ⑥ 跨端点字段路由 | 链式调用时 | `references/param-mappings.md` § 字段流字典 | ~1K |

#### 2️⃣ Recipe 匹配规则（核心）
1. **加载** `references/recipes/_index.md`，扫 `trigger_keywords` 列
2. **最长匹配优先**：若用户输入同时命中多个 recipe 的 trigger，**选最长 trigger 命中的那个**（最具体）
3. **平局询问**：若两个 trigger 长度相同且都命中 → 主动询问用户："您是想看 A 还是 B？"
4. **无命中**：先查 §0.1 不支持清单 → 不在则进入"自定义链路"流程（步骤 3）

#### 3️⃣ 自定义链路（无现成 Recipe）
1. 读 `references/atoms/_index.md`，按 `chain_role` 列定位起点（`starter`）和终点（`terminal`）
2. **优先用 `⭐⭐⭐ 首选`** 标记的端点；不到必要不用 `⭐ 条件` 端点
3. 字段流（上游 OUT → 下游 IN）由 `param-mappings.md § 字段流字典` 决定，**禁止**自行猜 json_path
4. 链路完成后，可向维护方建议把它编排成新 recipe

#### 4️⃣ 调用前自检（按 risk 分级 · 节省 token）
| 端点 risk | 必做自检 | 步骤数 |
|----------|---------|-------|
| `risk: low` | ① 路径在 endpoints_whitelist.yaml | 1 步 |
| `risk: medium` | ① 路径 ② method ③ 必填参数 ④ 写入确认 | 4 步 |
| `risk: high` | 4 步 + 显式向用户确认参数与意图 | 5 步 |
| `risk: critical`（restricted） | 6 步高风险确认流程（详见 §高风险能力清单） | 6 步 |

> 旧 SKILL 强制所有调用都做 4 步——现按 risk 等级简化。`low` 端点（占绝大多数）只校验路径即可。

#### 5️⃣ 错误处理快速决策
| 现象 | 行动 | 重试 |
|------|------|------|
| 404 / 410 | §3.1(A) 5 步防臆造自检 → 通过才 STOP；**禁止**自改路径段重试 | 0 |
| 400 / 422 | §3.1(B) 6 步防参数臆造自检 → 通过才修参重试 | ≤1 |
| 401 / 402 / 403 | STOP，告知用户去 https://www.aconfig.cn 处理 | 0 |
| 429 | 读 `Retry-After` 退避；无该头时指数退避+jitter | ≤2 |
| 5xx | 等 3 秒重试 → 仍失败走端点级"降级/替换" | 1 |
| HTTP 200 + `code != 0` | 读 `message_zh` 报告用户；**不重试**（业务错误重试无用） | 0 |

#### 6️⃣ 输出契约（与用户对话时）
1. **数据来源声明**：每次输出明确告知数据来自 `https://www.aconfig.cn` 三方接口
2. **缺失字段处理**：如某字段链路降级后缺失，**显式说明**"X 暂不可取"，不要静默省略
3. **不要伪造**：用户问的字段若不在响应里 → 说"未返回"，禁止用其他端点拼凑模拟



### 核心约束（强制遵守）

| 规则 | 说明 |
|------|------|
| ⚠️ POST 写入语义 | **23 个端点全部为 POST 方法 + `risk: high`**，参数走 JSON Body，**非 query string**，调用前必须用户确认参数 |
| 🔒 只读用途 | 虽然 HTTP 方法为 POST，但本技能仅用于数据查询，**不执行写入 / 账户 / 发文 / 评论操作** |
| 🚫 禁止臆造路径 | 仅使用 `references/endpoints_whitelist.yaml` 中的端点，**不得自行拼接、改版本号（v2）、加路径段** |
| 🚫 禁止重复调用 | POST 端点重复调用会重复扣配额，**5xx 重试上限 1 次**，业务错误 `code != 0` 不重试 |
| 📋 数据流向第三方 | 所有请求发送至 `https://www.aconfig.cn`，请使用独立测试账号并定期轮换 API Key |
| 🔑 凭证保护 | 不暴露 API Key、Cookie、Token 至日志或对话 |

### 基础使用（5 步完成调用）

**Step 0 — 合规硬前置检查（不可跳过 · 不可绕过）**

> ⛔ 本步骤为**硬前置**：未通过则禁止执行 Step 1 及后续任何 API 调用。
> 本步骤**自包含**，不依赖任何外部文件即可完成基础合规检查。详细框架可参阅 [COMPLIANCE_GATE.md](./COMPLIANCE_GATE.md)，完整风险规则见 [risk_rules.yaml](./risk_rules.yaml)。

**0.0 缺失即停检查：**

检查合规确认状态文件是否存在。**若不存在，立即停止**后续操作，直接进入 0.2 首次闸门流程。

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
STATE_FILE="$COMPLIANCE_DIR/confirmed_wechat-pro.txt"
if [ -f "$STATE_FILE" ]; then cat "$STATE_FILE"; else echo "NOT_FOUND"; fi
```

**0.1 读取并校验确认状态：**

- 返回 `NOT_FOUND` → 进入 0.2 首次闸门
- 返回的 `legal_version` 低于 `1.0.0` → 法律内容已更新，重新进入 0.2 首次闸门
- 返回的 `legal_version` 等于 `1.0.0` → 已确认，跳到 0.5 风险检测

**0.2 首次使用合规闸门（仅首次触发）：**

向用户显示以下**完整**合规提醒（本内容自包含，无需读取外部文件）：

> ⚠️ **法律合规提醒**
>
> 本 skill 通过第三方数据聚合服务（MaxHub API）获取数据，**非平台官方 API**。
>
> **数据来源声明**：
> - 本项目不持有、不存储、不控制任何平台数据
> - 所有数据请求经 MaxHub API（`https://www.aconfig.cn`）中转至各平台
> - MaxHub API 的数据获取方式未获得各平台官方授权
>
> **合法使用场景**：公开数据分析、竞品研究、内容创作辅助、学术研究、自动化测试
>
> **禁止使用场景**：
> - 电信诈骗相关活动（《反电信网络诈骗法》）
> - 侵犯他人通信自由和通信秘密（《宪法》第40条）
> - 规避实名身份验证（《网络安全法》第24条）
> - 代发私信或消息
> - 收集、存储未公开的个人信息（联系方式、位置、社交关系）
> - 使用他人登录凭证（cookie/token）访问非本人数据
>
> **已移除的高风险能力**：刷量操控、反爬绕过、会话伪造、批量提取、私信、登录加密等端点已从代码中完全移除。
>
> **完整法律条款**：请参阅 [数据使用政策](./DATA_USAGE_POLICY.md) 和 [合规审查清单](./COMPLIANCE_CHECKLIST.md)。
>
> 输入 **"同意"** 确认已阅读并遵守以上条款，或输入 **/legal** 查看完整法律条款。

**0.3 确认验证规则：**

- ✅ **接受**（明确肯定）：`同意` / `确认` / `我已阅读并同意` / `我同意` / `确认同意`
- ❌ **拒绝**（模糊回应，需提示用户使用明确措辞）：`嗯` / `ok` / `行` / `好的` / `可以` / `嗯嗯` / `好` / `yes`
- 模糊回应提示："请使用明确措辞确认（如输入'同意'），以确保您已阅读并理解合规条款。"
- **用户拒绝或未确认时**：立即停止，不执行 Step 1 及后续任何步骤。即使用户再次要求执行操作，也必须先完成合规确认。

**0.4 确认通过后，写入状态并记录审计日志：**

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
mkdir -p "$COMPLIANCE_DIR"
echo "legal_version=1.0.0 confirmed_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$COMPLIANCE_DIR/confirmed_wechat-pro.txt"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"wechat-pro","event":"first_time_confirmation","legal_version":"1.0.0","status":"confirmed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

**0.5 风险检测（每次用户请求都执行）：**

对照以下**核心风险规则**（完整规则见 [risk_rules.yaml](./risk_rules.yaml)）检查用户请求：

| 风险类别 | 关键词（命中即触发提醒） | 定向提醒要点 |
|---------|----------------------|------------|
| `cookie_usage` | cookie / session / 登录凭证 / token / 凭证 / 登录态 | 确认使用本人账号凭证，不使用他人 cookie/session |
| `batch_operation` | 批量 / 全部 / 所有 / 循环 / 批次 / 大规模 / 全量 / 遍历 | 遵循最小必要原则，不用于刷量/批量注册 |
| `personal_data` | 粉丝列表 / 关注列表 / 用户画像 / 联系方式 / 社交关系 / 手机号 / 邮箱 / 粉丝画像 / 受众画像 / 个人信息 / 隐私数据 | 遵循《个人信息保护法》最小必要原则，不存储不传播 |
| `write_operation` | 端点白名单中 `write_operation: true` 或 `requires_user_confirmation: true` 标志 | 确认参数正确，了解操作不可撤销 |
| `social_graph` | 社交关系链 / 社交图谱 / 好友列表 / 聊天记录 / 通讯录 | 不采集通讯数据，了解《宪法》第40条对通信自由的保护 |

**命中风险时的处理流程**：
1. 显示对应类别的定向风险提醒（完整模板见 [COMPLIANCE_GATE.md](./COMPLIANCE_GATE.md) §3.3）
2. 等待用户明确确认（同 0.3 规则）
3. 确认后记录审计日志再继续：

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"wechat-pro","event":"risk_reminder","risk_type":"<matched_category>","legal_version":"1.0.0","status":"confirmed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

4. 用户拒绝或未确认时：停止，不执行后续操作

**0.6 `/legal` 命令处理（用户随时可触发）：**

当用户输入 `/legal`、`查看法律条款` 或 `法律条款` 时：

1. 读取并显示 [DATA_USAGE_POLICY.md](./DATA_USAGE_POLICY.md) 的完整内容
2. 记录审计日志：

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
mkdir -p "$COMPLIANCE_DIR"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"wechat-pro","event":"legal_review","legal_version":"1.0.0","status":"completed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

3. 显示完毕后，根据当前是否已通过首次闸门决定下一步：
   - 未通过首次闸门 → 返回 0.2 继续等待用户确认
   - 已通过首次闸门 → 询问用户是否继续之前的操作

**Step 1 — 检查 API Key**

```bash
[ -n "${MAXHUB_API_KEY:-}" ] && echo "ok" || echo "missing"
```

若返回 `missing`，停止并提示用户配置 `MAXHUB_API_KEY`。

**Step 2 — 匹配意图 → 选择 reference**

按用户目标从下表选择对应 reference 文件，每个文件自包含其领域的全部端点定义：

| 用户目标 | 加载文件 | 覆盖范围 |
|---------|---------|---------|
| 查公众号文章 / 评论 / 账号 | `references/mp.md` | 文章详情、统计、评论、回复、相关推荐、广告、账号资料、文章列表、服务（9 端点） |
| 查视频号 / 视频 / 直播 / 合集 | `references/channels.md` | 视频号信息、ID 互转、用户视频、视频详情、评论、分享 URL、用户资料、合集、直播（12 端点） |
| 搜一搜 / 跨端搜索 | `references/search.md` | 公众号 + 视频号统一搜索 + 视频号视频筛选搜索（2 端点） |
| 跨端点参数查询 / 字段流追溯 | `references/param-mappings.md` | 全局红线 + 端点路由 + 字段流字典 + 错误处理总览 |
| 路径白名单硬校验 | `references/endpoints_whitelist.yaml` | 24 个端点的硬白名单 + Pre-call 5 步自检协议（含 POST Body 校验） |

**Step 3 — 构建最小调用计划**

- ✅ 优先使用最少端点完成任务，能用一个端点就不用两个
- ✅ 调用任何端点前**必须让用户确认 Body 参数**（risk: high 强制要求）
- ✅ 视频号入口三选一（`object_id` / `export_id` / `share_url`），不要同时携带
- ❌ 禁止"先 head/tail 试运行"或"先调一个看看"等探索性调用

**🔍 运行时合规自检（构建调用计划时必须逐项确认）：**

| # | 检查项 | 通过条件 | 不通过处理 |
|---|--------|---------|-----------|
| C1 | 意图合法性 | 用户请求属于合法场景（公开数据分析/竞品研究/内容创作辅助/学术研究/自动化测试） | STOP，告知用户该用途不在合法范围内 |
| C2 | 参数来源 | 所有 ID/关键词/链接来自用户本人提供或公开可见内容 | STOP，要求用户说明数据来源 |
| C3 | 无他人凭证 | 请求不涉及使用他人 cookie/session/token | STOP，要求使用本人账号凭证 |
| C4 | 最小必要 | 请求范围已限定在最小必要数据，非批量/全量采集 | STOP，要求用户明确缩小范围 |
| C5 | 端点合规 | 目标端点在 `endpoints_whitelist.yaml` 中且未被移除 | STOP，告知该端点不可用 |

> 任一项不通过即停止，不进入执行步骤。已通过 Step 0.5 风险确认的请求无需重复 C4。

**Step 4 — 执行并验证**

- 调用前比对 `endpoints_whitelist.yaml` 完成 5 步 Pre-call 自检（路径 → method=POST → 必填 → 用户确认 → Body=JSON）
- 收到 **404** → 必须先做防路径臆造自检（5 步），不要立刻切换 mp/channels/search 段
- 收到 **400 / 422** → 必须先做防参数臆造自检（6 步），重点检查 `oneOf: [object_id, export_id, share_url]` 三选一
- 收到 **业务 code != 0** → 读 `message_zh` 报告用户，**不重试**（避免重复扣配额）


**📦 返回数据合规检查（收到响应后必须执行）：**

| # | 检查项 | 处理方式 |
|---|--------|---------|
| R1 | 个人信息脱敏 | 响应包含手机号/邮箱/身份证等 PII 时，仅展示必要字段，其余脱敏 |
| R2 | UGC 内容处理 | 响应包含评论/弹幕/动态等 UGC 时，提醒用户不用于未授权商业用途 |
| R3 | 隐私数据保护 | 响应包含他人联系方式/位置/社交关系时，不写入持久化存储 |
| R4 | 数据量控制 | 响应数据量 >100 条时，提醒用户遵循最小必要原则，建议分页 |
| R5 | 审计日志 | 每次成功调用后记录审计日志到 `$HOME/.maxhub-skills/.compliance/audit_log.jsonl`，event 为 `api_call` |

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"wechat-pro","event":"api_call","endpoint":"<endpoint_id>","legal_version":"1.0.0","status":"success"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

> R1-R4 为数据处理红线，违反即构成合规风险。R5 为审计要求，每次调用必须记录。

### 高级使用

#### 链式调用图谱（Chain Recipes）

| 用户场景 | 链路 | 字段流 |
|---------|------|-------|
| 搜一搜 → 公众号文章 | `fetch_search`（business_type=mp） → `fetch_article_detail` | `keyword` → 文章 `url` |
| 查文章 + 评论 + 回复 | `fetch_article_detail` → `fetch_article_comments` → `fetch_comment_replies` | `url` 复用 + `content_id` |
| 查账号 → 文章列表 → 详情 | `fetch_account_profile` → `fetch_account_articles` → `fetch_article_detail` | `username` → 文章 `url` |
| 查视频号 → 视频详情 → 评论 | `fetch_channel_info` → `fetch_user_videos` → `fetch_video_detail` → `fetch_video_comments` | `username` → `object_id` |
| channel_id → username | `fetch_channel_id_to_username` → 后续视频号端点 | `channel_id` → `username` |
| 视频号直播追踪 | `fetch_channel_info` → `fetch_live_history` → `fetch_live_detail` | `username` → `live_id` |
| 视频号合集 | `fetch_user_collections` → `fetch_collection_videos` | `username` → `topic_id` |
| 视频号内搜索 | `fetch_search_channel_videos` | `username + keyword` 双必填 |

#### 防臆造自检清单（强制前置步骤）

**收到 404 时（A）**：
1. 路径白名单逐字符比对（注意 `/wechat_mp/v2/` vs `/wechat_channels/v2/` vs `/wechat_search/v2/`）→ 不在清单中 STOP
2. Method 比对（**全部为 POST**，不是 GET）→ 不等 STOP
3. 参数键名比对（`url` / `username` / `object_id` 不可互换）→ 有清单外参数 STOP
4. 资源 ID 来源溯源 → Agent 编造的 STOP
5. 全通过才判定"上游资源不存在"

**收到 400 / 422 时（B）**：
1. 参数名严格比对（大小写 / 缩写 / 复数）
2. 必填项齐全 + oneOf 三选一逻辑（视频详情 `object_id` / `export_id` / `share_url`）
3. **POST Body 是否为合法 JSON**（非 query string、非表单）
4. Content-Type 是否为 `application/json`
5. 类型与格式严格匹配（pattern / enum）
6. 全通过才按 `message_zh` 排查

#### POST 端点最佳实践

- **JSON Body 序列化**：使用语言原生 JSON 序列化，不要手拼字符串
- **Content-Type 必填**：`-H "Content-Type: application/json"`
- **重试策略**：5xx 重试 ≤ 1 次；4xx / 业务错误**不重试**，避免重复扣配额
- **用户确认门槛**：所有端点 `risk: high`，调用前必须把完整 Body 给用户确认

#### SKILL 版本更新

| 触发条件 | 推荐操作 |
|---------|---------|
| 合法路径持续 404 / 410 | `skillhub upgrade wechat-pro` |
| 用户问"版本是多少" | 当前版本 v4.0.0，访问 https://skillhub.cn/skills/wechat-pro |
| 多端点连续 410 | `skillhub upgrade wechat-pro --force` |
| 401 / 402 / 403 | **不是版本问题**，去 https://www.aconfig.cn 处理 |

### 常用命令速查表

| 场景 | 命令 |
|---|---|
| 查 API Key | `[ -n "${MAXHUB_API_KEY:-}" ] && echo "ok" \|\| echo "missing"` |
| 查公众号文章详情 | `curl -X POST -H "$maxhub_auth_header" -H "Content-Type: application/json" -d '{"url":"https://mp.weixin.qq.com/s/xxx"}' "https://www.aconfig.cn/api/v1/wechat_mp/v2/fetch_article_detail"` |
| 查文章评论 | `curl -X POST -H "$maxhub_auth_header" -H "Content-Type: application/json" -d '{"url":"https://mp.weixin.qq.com/s/xxx"}' "https://www.aconfig.cn/api/v1/wechat_mp/v2/fetch_article_comments"` |
| 查公众号文章列表 | `curl -X POST -H "$maxhub_auth_header" -H "Content-Type: application/json" -d '{"username":"gh_xxx"}' "https://www.aconfig.cn/api/v1/wechat_mp/v2/fetch_account_articles"` |
| 查视频号视频详情 | `curl -X POST -H "$maxhub_auth_header" -H "Content-Type: application/json" -d '{"object_id":"xxx"}' "https://www.aconfig.cn/api/v1/wechat_channels/v2/fetch_video_detail"` |
| 搜一搜 | `curl -X POST -H "$maxhub_auth_header" -H "Content-Type: application/json" -d '{"keyword":"AI"}' "https://www.aconfig.cn/api/v1/wechat_search/v2/fetch_search"` |
| 检查 SKILL 更新 | `skillhub info wechat-pro` |


### 📌 端到端使用示例（agent 快速上手）

**用户输入**：「帮我看 微信公众号某篇文章的评论」

**Agent 执行步骤**：

1. **匹配 recipe**：读 `references/recipes/_index.md` → 找到 trigger 命中 → 选最长匹配的 recipe
2. **加载 recipe 详情**：读 `references/recipes/<domain>.md` 中对应段落，拿到 Inputs / Atomic Steps / Output
3. **路径校验**：对每个 atom 的 endpoint_id，`grep` 一下 `endpoints_whitelist.yaml` 确认存在
4. **risk: low 的端点直接调用，risk: medium+ 先与用户确认**
5. **链式传递**：上游响应的 json_path 字段（如 `$.data.bvid`）按 recipe 的 `extract` 列绑定为变量，传给下游端点
6. **错误处理**：按 §错误处理决策表行动；不要自改路径或瞎加参数
7. **输出**：组装结果给用户，标明数据来自三方接口；缺失字段显式说"未取到"

**反例（agent 不要这么做）**：
- ❌ 全文加载 `endpoints_whitelist.yaml`（大文件，浪费上下文）
- ❌ 看到 404 就改路径段重试（会被防臆造规则阻断）
- ❌ 把没在响应里的字段编一个值返回给用户
- ❌ 链式调用时忽略 recipe 的 `extract` 列，自己猜 json_path


## 5. 使用场景

### 场景一：MCN 团队视频号内容研究

- **角色**：视频号运营 / MCN 内容策划
- **需求**：分析头部视频号近期爆款视频的封面、标题、互动数据，沉淀爆款公式
- **使用方式**：`fetch_channel_info` 锁定账号 → `fetch_user_videos` 拉视频列表 → 取 `object_id` → `fetch_video_detail` + `fetch_video_comments` 取详情与评论 → 必要时 `fetch_video_share_url` 取分享链接做侧链分析
- **预期收益**：视频号爆款样本集 + 评论情感分析，提炼可复用的视频号选题模板

### 场景二：增长团队微信生态搜索调研

- **角色**：增长 PM / 竞品分析师
- **需求**：在微信生态（公众号 + 视频号）内调研竞品关键词的曝光分布与头部账号
- **使用方式**：`fetch_search` 跨端搜索（business_type 切换 mp/channels） → 取头部公众号 / 视频号 → 链式调 `fetch_account_profile` / `fetch_channel_info` 补全画像
- **预期收益**：完整微信生态竞品图谱，识别公众号 + 视频号双端的内容投放分布

### 场景三：数据团队账号矩阵分析

- **角色**：数据分析师 / 品牌策略
- **需求**：评估某品牌的微信账号矩阵（多个公众号 + 多个视频号）整体内容产能与互动健康度
- **使用方式**：批量传入 `username` 列表 → 并行调用 `fetch_account_profile` + `fetch_account_articles` + `fetch_channel_info` + `fetch_user_videos` → 汇总文章数 / 视频数 / 平均互动 → 输出账号矩阵看板
- **预期收益**：账号矩阵健康度报表，识别高产 / 低产账号与内容产能差距

## 6. 项目架构

### 目录结构

```
maxhub-wechat/
├── SKILL.md                            # Skill 定义与使用文档（本文件）
├── README.md                           # 英文项目说明
├── README_CN.md                        # 中文项目说明
├── _meta.json                          # 版本元信息（version: 4.0.0）
└── references/
    ├── endpoints_whitelist.yaml        # 24 端点路径硬白名单 + Pre-call 5 步自检协议（含 POST Body 校验）
    ├── param-mappings.md               # 中枢索引（全局红线 + 字段流字典 + 错误处理）
    ├── mp.md                           # 公众号域：文章详情/统计/评论/回复/广告/账号（9 端点，全 POST）
    ├── channels.md                     # 视频号域：信息/视频/评论/分享/合集/直播（12 端点，全 POST）
    └── search.md                       # 搜一搜域：跨端统一搜索 + 视频号视频筛选搜索（2 端点，POST）
```

### 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 调用方式 | `curl` + Bearer Token + JSON Body | **HTTP POST 请求**，参数走 JSON Body，需带 `Content-Type: application/json` |
| 数据接口 | MaxHub API | `https://www.aconfig.cn/api/v1/{wechat_mp\|wechat_channels\|wechat_search}/v2/*`，通过 `MAXHUB_API_KEY` 鉴权 |
| 路径校验 | YAML 硬白名单 | `endpoints_whitelist.yaml` 提供 24 端点的逐字符校验 + 5 步 Pre-call 协议（含 POST Body=JSON 校验） |
| 错误处理 | 决策表 + 自检清单 | HTTP 状态码权威定义 + 防臆造自检（A/B 双轨）+ POST 重试策略（5xx ≤ 1 次） |
| 输出格式 | JSON Standard MaxHub Response | `{code, message, message_zh, data, cache_url}` |
| 更新通道 | SkillHub | ⭐⭐⭐ SkillHub（腾讯云 CDN） |

### API 覆盖范围

| 领域 | 端点数 | HTTP 方法 | 风险等级 | Reference 文件 |
|------|--------|----------|----------|---------------|
| 公众号（MP） | 9 | POST | high | `mp.md` |
| 视频号（Channels） | 12 | POST | high | `channels.md` |
| 搜一搜（Search） | 2 | POST | high | `search.md` |
| **合计** | **24** | **全 POST** | **全 high** | — |

### 关键设计理念

- **POST 写入语义全管控**：23 个端点全部 POST + risk:high，强制用户确认参数，5xx 重试 ≤ 1 次，杜绝重复扣配额
- **防臆造四道闸**：白名单（endpoints_whitelist.yaml）→ 强标记（Full path）→ 禁止规则（Forbidden）→ 错误反馈（STOP）
- **三端段隔离**：`/wechat_mp/v2/` / `/wechat_channels/v2/` / `/wechat_search/v2/` 路径段不可混用
- **Agent 友好 7 大原则**：结构胜于叙述、明确指令优于建议、单一来源、词法稳定性、低 token 密度、边界显式声明、错误处理是契约
- **链式调用图谱**：字段流字典 + Chain Recipes + 跨 reference 链路三层联动，杜绝 Agent 编造字段名
- **错误处理契约**：HTTP 状态码权威定义 + 防臆造自检清单（A: 5 步 / B: 6 步含 POST Body 校验）+ POST 重试策略矩阵
