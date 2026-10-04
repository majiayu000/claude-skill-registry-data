---
slug: instagram-pro
displayName: Instagram 数据助手 | 帖子 / Reels / Stories / 用户
name: instagram-pro
description: Instagram 公开社交数据查询与内容分析 skill，通过 MaxHub API 查询帖子/Reels/Stories/Highlights、评论、点赞列表、用户资料、粉丝/关注、搜索、标签和相关内容。适合海外社媒运营、KOL 画像、内容互动分析、竞品跟踪和趋势研究。默认 read-only，侧重公开或用户授权范围内的数据；agent 应优先使用 recipes 进行单端点或链式调用，并避免采集超出用户授权的个人信息。所有请求发送到 https://www.aconfig.cn。
license: MIT-0
metadata:
  author: maxhub
  version: 4.1.4
  openclaw:
    capability: read_only
    requires_confirmation:
    - non_idempotent
    - cookie_input
    emoji: 📸
    primaryEnv: MAXHUB_API_KEY
    requires:
      env:
      - MAXHUB_API_KEY
      bins:
      - curl
    env:
    - name: MAXHUB_API_KEY
      description: Instagram 公开社交数据查询与内容分析 skill，通过 MaxHub API 查询帖子/Reels/Stories/Highlights、评论、点赞列表、用户资料、粉丝/关注、搜索、标签和相关内容。适合海外社媒运营、KOL 画像、内容互动分析、竞品跟踪和趋势研究。默认 read-only，侧重公开或用户授权范围内的数据；agent 应优先使用 recipes 进行单端点或链式调用，并避免采集超出用户授权的个人信息。所有请求发送到 https://www.aconfig.cn。
      required: true
      sensitive: true
    network:
    - https://www.aconfig.cn
    riskLevel: low
    defaultMode: recipes_first_read_only
    skillClass: maxhub-api-skill
    platform: instagram
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
    - instagram
    - IG
    - Reels
    - Stories
    - Highlights
    - 帖子
    - 评论
    - 用户资料
    - 粉丝
    - 关注
    - 搜索
    - 标签
    - 社媒分析
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

# Instagram 数据助手

## 1. 简介

Instagram 公开社交数据查询与内容分析 skill，通过 MaxHub API 查询帖子/Reels/Stories/Highlights、评论、点赞列表、用户资料、粉丝/关注、搜索、标签和相关内容。适合海外社媒运营、KOL 画像、内容互动分析、竞品跟踪和趋势研究。默认 read-only，侧重公开或用户授权范围内的数据；agent 应优先使用 recipes 进行单端点或链式调用，并避免采集超出用户授权的个人信息。所有请求发送到 https://www.aconfig.cn。

> ### 🚨 高风险平台警告 — Instagram / Meta
>
> **Meta 对未授权 scraping 有积极的诉讼历史，使用本 skill 存在显著法律风险：**
>
> - **诉讼历史**：Meta 自 2022 年起加大对第三方数据服务的打击力度，多起 scraping 诉讼获得有利判决
> - **GDPR 合规**：Instagram 用户数据受 GDPR 保护，未经授权获取欧洲用户数据可能面临巨额罚款（最高全球营收 4%）
> - **Stories/Highlights 隐私**：Stories 等临时内容具有隐私期待，爬取可能侵犯用户合理隐私期望
> - **粉丝/关注列表**：获取他人粉丝列表和关注列表构成社交图谱采集，属于高敏感操作
> - **账号封禁**：Meta 对可疑 API 访问会立即封禁相关账号
> - **建议**：优先使用 [Instagram Graph API](https://developers.facebook.com/docs/instagram-api) 官方接口

## 2. 详细功能

### 帖子数据
- 查询 Instagram 帖子完整详情，覆盖图文、Carousel 多图、视频、Reels 多种形态
- 支持通过短码、媒体 ID、分享链接三种入口直接定位帖子
- 提供帖子点赞用户列表、被标记用户、音乐元数据等关联信息
- 支持帖子 oEmbed 嵌入数据获取，便于第三方页面引用
- 提供短码与媒体 ID 双向互转，解决跨接口资源 ID 不一致的问题

### Reels 与 Stories
- 拉取指定用户的全部 Reels 短视频列表
- 获取系统推荐 Reels 流，洞察平台分发偏好
- 查询用户当日 Stories 快拍内容
- 查询用户 Highlights 精选合集，并支持深入到精选内的具体 Reel 明细
- 查询音乐相关帖子流，支持以同款音乐为线索发现热门内容

### 评论与回复
- 拉取帖子一级评论列表，支持游标翻页
- 拉取指定评论下的二级回复链路
- 提供单条评论翻译能力，覆盖跨语种内容理解
- 支持批量翻译评论，满足海外舆情整理与摘要场景

### 用户画像
- 通过用户名、用户 ID 获取用户完整资料卡
- 提供用户简要信息接口，适合需要轻量数据的场景
- 拉取用户全部投稿帖子、Reels、被标记的帖子、转发记录
- 拉取用户粉丝列表、关注列表，分析受众构成
- 获取用户 About 信息、曾用名历史、相似账号推荐
- 提供用户 ID 与用户名双向互转，便于跨接口数据接力

### 搜索能力
- 支持用户搜索，按账号关键词定位目标博主
- 支持综合搜索，一次返回用户、帖子、话题等多类型结果
- 支持 Reels 视频搜索、音乐搜索，定位特定话题或 BGM 内容
- 支持 Hashtag 话题搜索、Location 地点搜索
- 提供 Explore 探索页与探索分区帖子流

### 地点与话题图谱
- 查询 Hashtag 话题下的帖子流，识别话题热度
- 查询 Location 地点详情、地点帖子流、附近地点列表
- 支持按经纬度坐标搜索附近内容
- 提供城市与地区列表，构建层级化地理筛选

### 多版本接口共存
- 同时提供三套接口版本并行运行，覆盖不同稳定性与数据丰富度需求
- 不同版本之间端点互为备份，单版本异常时可降级切换
- 不同版本字段丰富度各有侧重，可按业务场景择优调用

### 账号余额查询
- 查询 MaxHub API 账号剩余额度，支持 `x-api-key` 或 `Authorization: Bearer` 两种认证方式
- 频率限制：最快每 3 秒调用一次
- 接口路径：`GET /api/maxhub/balance`

## ⚖️ 法律免责与合规声明

> **使用本 skill 即表示您确认已阅读并同意以下条款：**
>
> 1. **数据来源**：本 skill 通过第三方数据服务（MaxHub API）获取 Instagram（Meta 旗下） 数据，该服务**未获得 Instagram（Meta 旗下） 官方授权**。本项目对数据获取的合法性不作任何保证。
> 2. **合规责任**：使用方需**自行确保**符合所在地区的数据保护法律（《个人信息保护法》/ GDPR / CCPA 等）及 Instagram（Meta 旗下） 服务条款（ToS）。因使用本 skill 产生的任何法律后果由使用方自行承担。
> 3. **禁止用途**：严禁将本 skill 用于违反法律的行为，包括但不限于：侵犯个人信息权、不正当竞争、刷量操控、批量爬取用户数据等。
> 4. **平台风险**：Meta 对未授权 scraping 有积极的诉讼历史，可能采取封号、诉讼等法律行动，GDPR 下欧洲用户数据面临巨额罚款风险。
> 5. **完整政策**：详细数据使用政策请参阅 [DATA_USAGE_POLICY.md](./DATA_USAGE_POLICY.md)。

> ### 📋 数据传输与隐私声明（请认真阅读）
>
> 1. **第三方传输**：您提供的所有 ID、关键词、链接、cookie 等参数都会通过 HTTPS 发送到 **`https://www.aconfig.cn`**（MaxHub 数据服务）进行处理。
> 2. **UGC 隐私**：拉回的 评论 / Stories / Reels 等内容可能包含个人信息或敏感 UGC，请勿写入未授权的数据库或公开发布。
> 3. **凭证保护**：建议使用**独立测试账号**、定期轮换 API Key；**禁止**传入主力生产账号的 cookie 或 session 凭证。
> 4. **合规责任**：使用方需自行确保符合所在地区的数据保护法律（《个人信息保护法》/ GDPR / Instagram（Meta 旗下） ToS 等），平台账号的合规性由使用方承担。

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
| 🔒 只读 | 本技能仅用于数据查询和分析，**不执行写入 / 账户操作** |
| 🚫 禁止臆造路径 | 仅使用 `references/endpoints_whitelist.yaml` 中的端点，**不得自行拼接、改版本号、加路径段** |
| 📋 数据流向第三方 | 所有请求发送至 `https://www.aconfig.cn`，请使用独立测试账号并定期轮换 API Key |
| 🔑 凭证保护 | 不暴露 API Key、Cookie、Token 至日志或对话 |
| 🔀 版本不互通 | V1 / V2 / V3 端点参数不兼容，**禁止跨版本套用参数名** |

### 基础使用（5 步完成调用）

**Step 0 — 合规硬前置检查（不可跳过 · 不可绕过）**

> ⛔ 本步骤为**硬前置**：未通过则禁止执行 Step 1 及后续任何 API 调用。
> 本步骤**自包含**，不依赖任何外部文件即可完成基础合规检查。详细框架可参阅 [COMPLIANCE_GATE.md](./COMPLIANCE_GATE.md)，完整风险规则见 [risk_rules.yaml](./risk_rules.yaml)。

**0.0 缺失即停检查：**

检查合规确认状态文件是否存在。**若不存在，立即停止**后续操作，直接进入 0.2 首次闸门流程。

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
STATE_FILE="$COMPLIANCE_DIR/confirmed_instagram-pro.txt"
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
echo "legal_version=1.0.0 confirmed_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$COMPLIANCE_DIR/confirmed_instagram-pro.txt"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"instagram-pro","event":"first_time_confirmation","legal_version":"1.0.0","status":"confirmed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

**0.5 风险检测（每次用户请求都执行）：**

对照以下**核心风险规则**（完整规则见 [risk_rules.yaml](./risk_rules.yaml)）检查用户请求：

| 风险类别 | 关键词（命中即触发提醒） | 定向提醒要点 |
|---------|----------------------|------------|
| `cookie_usage` | cookie / session / 登录凭证 / token / 凭证 / 登录态 | 确认使用本人账号凭证，不使用他人 cookie/session |
| `batch_operation` | 批量 / 全部 / 所有 / 循环 / 批次 / 大规模 / 全量 / 遍历 | 遵循最小必要原则，不用于刷量/批量注册 |
| `personal_data` | 粉丝列表 / 关注列表 / 用户画像 / 联系方式 / 社交关系 / 手机号 / 邮箱 / 粉丝画像 / 受众画像 / 个人信息 / 隐私数据 | 遵循《个人信息保护法》最小必要原则，不存储不传播 |
| `write_operation` | 端点白名单中 `write_operation: true` 或 `requires_user_confirmation: true` 标志 | 确认参数正确，了解操作不可撤销 |
| `cross_border` | 当前 skill 属于境外平台（instagram/tiktok/linkedin/twitter/reddit/youtube/threads/lemon8）时自动触发 | 遵守《数据安全法》第31条和《个人信息保护法》第38条 |

**命中风险时的处理流程**：
1. 显示对应类别的定向风险提醒（完整模板见 [COMPLIANCE_GATE.md](./COMPLIANCE_GATE.md) §3.3）
2. 等待用户明确确认（同 0.3 规则）
3. 确认后记录审计日志再继续：

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"instagram-pro","event":"risk_reminder","risk_type":"<matched_category>","legal_version":"1.0.0","status":"confirmed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

4. 用户拒绝或未确认时：停止，不执行后续操作

**0.6 `/legal` 命令处理（用户随时可触发）：**

当用户输入 `/legal`、`查看法律条款` 或 `法律条款` 时：

1. 读取并显示 [DATA_USAGE_POLICY.md](./DATA_USAGE_POLICY.md) 的完整内容
2. 记录审计日志：

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
mkdir -p "$COMPLIANCE_DIR"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"instagram-pro","event":"legal_review","legal_version":"1.0.0","status":"completed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
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
| 查帖子 / Reels / Stories / Highlights / 音乐帖 / 翻译 | `references/post.md` | 帖子详情、Reels、Stories、Highlights、点赞、标记、shortcode↔media_id 转换、评论翻译（20 端点） |
| 查用户 / 粉丝 / 关注 / About / 曾用名 / 相似用户 | `references/user.md` | 用户资料、帖子、Reels、Followers、Following、Tagged、相似推荐（37 端点） |
| 搜索 / 探索 / 话题 / 地点 / 坐标 | `references/search.md` | 用户搜索、综合搜索、Hashtag、Location、坐标、城市、Explore（24 端点） |
| 查评论 / 回复 | `references/comments.md` | V1/V2/V3 帖子评论与子评论回复（6 端点） |
| 跨端点参数查询 / 字段流追溯 | `references/param-mappings.md` | 全局红线 + 端点路由 + V1/V2/V3 字段流字典 + 错误处理总览 |
| 路径白名单硬校验 | `references/endpoints_whitelist.yaml` | 88 端点的硬白名单 + Pre-call 4 步自检协议 |

**Step 3 — 构建最小调用计划**

- ✅ 优先使用最少端点完成任务，能用一个端点就不用两个
- ✅ 跨版本切换时**必须**重新读取该版本的 reference，禁止套用其他版本参数
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

- 调用前比对 `endpoints_whitelist.yaml` 完成 4 步 Pre-call 自检（路径 → method → 必填 → 写入确认）
- 收到 **404** → 必须先做 §3.1 (A) 防路径臆造自检（5 步）
- 收到 **400 / 422** → 必须先做 §3.1 (B) 防参数臆造自检（6 步）
- 收到 **业务 code != 0** → 读 `message_zh` 报告用户，**不重试**


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
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"instagram-pro","event":"api_call","endpoint":"<endpoint_id>","legal_version":"1.0.0","status":"success"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

> R1-R4 为数据处理红线，违反即构成合规风险。R5 为审计要求，每次调用必须记录。

### 高级使用

#### 链式调用图谱（Chain Recipes）

| 用户场景 | 链路 | 字段流 |
|---------|------|-------|
| 搜索用户 → 帖子详情 | `v3_search_users` → `v3_get_post_info_by_code` | `username` → `code` |
| 查帖子 + 评论 + 回复（V3） | `v3_get_post_info_by_code` → `v3_get_post_comments` → `v3_get_comment_replies` | `code` → `media_id` + `comment_id` 接力 |
| 查帖子 + 评论 + 回复（V2） | `v2_fetch_post_info` → `v2_fetch_post_comments` → `v2_fetch_comment_replies` | `code_or_url` → `comment_id` 接力 |
| 查用户 → 帖子 + Reels | `v3_get_user_profile` → `v3_get_user_posts` + `v3_get_user_reels` | `user_id` / `username` 复用 |
| 用户全面画像 | `v2_fetch_user_info` → `v2_fetch_user_posts` + `v2_fetch_user_followers` + `v2_fetch_user_stories` | `user_id` 复用 |
| Hashtag → 帖子流 | `v2_search_hashtags` → `v2_fetch_hashtag_posts` | `keyword` 接力 |
| Location → 附近 + 帖子 | `v3_get_location_info` → `v3_get_location_nearby` + `v3_get_location_posts` | `location_id` 复用 |

> ⚠️ **V3 关键陷阱**：`v3_get_comment_replies` 的必填参数是 **`media_id` + `comment_id`**，不是 `code` + `comment_id`。需先用 `v3_shortcode_to_media_id` 把 code 转成 media_id 再调用。

#### 防臆造自检清单（强制前置步骤）

**收到 404 时（A）**：
1. 路径白名单逐字符比对 → 不在清单中 STOP
2. Method 比对 → 不等 STOP
3. 参数键名比对 → 有清单外参数 STOP
4. 资源 ID 来源溯源 → Agent 编造的 STOP
5. 全通过才判定"上游资源不存在"

**收到 400 / 422 时（B）**：
1. 参数名严格比对（大小写 / 缩写 / 复数 / 版本差异）
2. 必填项齐全 + oneOf 二选一逻辑（V2/V3 大量端点支持 `username` 或 `user_id` 二选一）
3. 类型与格式严格匹配（pattern / enum）
4. 传参方式正确（query vs body）
5. 没有清单外的臆造参数（如把 V1 的 `max_id` 用到 V3 的 `after`）
6. 全通过才按 `message_zh` 排查

#### V1 / V2 / V3 版本选型建议

| 维度 | V1 | V2 | V3 |
|---|---|---|---|
| 稳定性 | 较旧，部分端点已迁移 | 中等，仍主力 | 最新，推荐优先使用 |
| 字段丰富度 | 基础 | 中等 | 最丰富（含 Carousel / oEmbed / 推荐 Reels） |
| 翻页参数 | `max_id` / `end_cursor` | `pagination_token` | `after` / `first` / `last` |
| 推荐场景 | 历史脚本兼容 | 综合搜索、Stories、Highlights | 用户 / 帖子主流查询 |

#### SKILL 版本更新

| 触发条件 | 推荐操作 |
|---------|---------|
| 合法路径持续 404 / 410 | `skillhub upgrade instagram-pro` |
| 用户问"版本是多少" | 当前版本 v4.0.0，访问 https://skillhub.cn/skills/instagram-pro |
| 多端点连续 410 | `skillhub upgrade instagram-pro --force` |
| 401 / 402 / 403 | **不是版本问题**，去 https://www.aconfig.cn 处理 |

### 常用命令速查表

| 场景 | 命令 |
|---|---|
| 查 API Key | `[ -n "${MAXHUB_API_KEY:-}" ] && echo "ok" \|\| echo "missing"` |
| 查帖子详情（V3 by code） | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/instagram/v3/get_post_info_by_code?code=Cxxxx"` |
| 查用户资料（V3） | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/instagram/v3/get_user_profile?username=xxx"` |
| 查帖子评论（V3） | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/instagram/v3/get_post_comments?code=Cxxxx"` |
| 综合搜索（V3） | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/instagram/v3/general_search?query=xxx"` |
| 检查 SKILL 更新 | `skillhub info instagram-pro` |


### 📌 端到端使用示例（agent 快速上手）

**用户输入**：「帮我看 @username 这个 IG 用户的最近 post」

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

### 场景一：Instagram 网红营销选号

- **角色**：跨境 DTC 品牌投放经理
- **需求**：批量分析候选 KOL 的粉丝量、互动率、Reels 表现，筛选投放对象
- **使用方式**：`v3_search_users` 搜索领域关键词 → 取 `username` → 链式调 `v3_get_user_profile` + `v3_get_user_posts` + `v3_get_user_reels`，提取 follower_count / 平均点赞 / Reels 播放
- **预期收益**：一次链路完成数十账号筛选，量化对比互动率，避免凭直觉选号

### 场景二：海外品牌话题与舆情监控

- **角色**：海外品牌 PR / 公关团队
- **需求**：监控品牌相关 Hashtag 与 Location 下的实时帖子流，及时发现负面或爆款
- **使用方式**：`v2_search_hashtags` → `v2_fetch_hashtag_posts` 拉取热门帖；`v3_get_location_posts` 监控线下门店所在 Location；对热门帖 `v3_get_post_comments` 深挖评论情感
- **预期收益**：构建 Hashtag + Location + 评论的三维舆情监控网，关键事件响应提速

### 场景三：社媒数据爬取与素材库构建

- **角色**：内容运营 / 数据分析师
- **需求**：批量采集竞品账号近 30 天的所有帖子与 Reels，建立内容素材库
- **使用方式**：`v3_get_user_id_by_username` 解析 `user_id` → `v3_get_user_posts` + `v3_get_user_reels` 翻页采集 → 对高互动帖 `v3_get_post_info_by_code` 取详情 + Carousel 媒体地址
- **预期收益**：完整素材库 + 字段标准化，支撑选题、剪辑、广告 Hook 提炼

### 场景四：用户增长 / 粉丝结构分析

- **角色**：增长分析师
- **需求**：分析自有账号或竞品账号的 Followers / Following 重合度、粉丝头像与 bio 特征
- **使用方式**：`v2_fetch_user_followers` + `v2_fetch_user_following` 采集列表 → 抽样 `v2_fetch_user_info` 取每个粉丝的 bio / 是否私密 / followers_count
- **预期收益**：识别核心粉丝群体画像，为后续投放圈选与内容定位提供依据

## 6. 项目架构

### 目录结构

```
maxhub-instagram/
├── SKILL.md                            # Skill 定义与使用文档（本文件）
├── README.md                           # 英文项目说明
├── README_CN.md                        # 中文项目说明
├── _meta.json                          # 版本元信息（version: 4.0.0）
└── references/
    ├── endpoints_whitelist.yaml        # 88 端点路径硬白名单 + Pre-call 4 步自检协议
    ├── param-mappings.md               # 中枢索引（全局红线 + 字段流字典 + 错误处理 + 版本差异）
    ├── post.md                         # 帖子域：详情/Reels/Stories/Highlights/点赞/标记/转换/翻译（20 端点）
    ├── user.md                         # 用户域：资料/帖子/粉丝/关注/About/曾用名/相似用户（37 端点）
    ├── search.md                       # 搜索域：用户/综合/Hashtag/Location/坐标/Explore（24 端点）
    └── comments.md                     # 评论域：V1/V2/V3 帖子评论与子回复（6 端点）
```

### 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 调用方式 | `curl` + Bearer Token | HTTP GET 请求，参数通过 query string 传递 |
| 数据接口 | MaxHub API | `https://www.aconfig.cn/api/v1/instagram/*`，通过 `MAXHUB_API_KEY` 鉴权 |
| 路径校验 | YAML 硬白名单 | `endpoints_whitelist.yaml` 提供 88 端点的逐字符校验 + 4 步 Pre-call 协议 |
| 错误处理 | 决策表 + 自检清单 | HTTP 状态码权威定义 + 防臆造自检（A/B 双轨）+ V1↔V2↔V3 替换矩阵 |
| 输出格式 | JSON Standard MaxHub Response | `{code, message, message_zh, data, cache_url}` |
| 更新通道 | SkillHub | ⭐⭐⭐ SkillHub（腾讯云 CDN） |

### API 覆盖范围

| 领域 | 端点数 | Reference 文件 |
|------|--------|---------------|
| 帖子（Posts / Reels / Stories / Highlights） | 34 | `post.md` |
| 用户（Users） | 24 | `user.md` |
| 搜索（Search / Explore / Location / Hashtag） | 23 | `search.md` |
| 评论（Comments） | 6 | `comments.md` |
| **合计** | **88** | — |

### 关键设计理念

- **防臆造四道闸**：白名单（endpoints_whitelist.yaml）→ 强标记（Full path）→ 禁止规则（Forbidden）→ 错误反馈（STOP）
- **多版本路由**：V1 / V2 / V3 三版本并行，每个版本独立维护参数命名与翻页协议，杜绝 Agent 跨版本套用
- **链式调用图谱**：字段流字典 + Chain Recipes + 跨 reference 链路三层联动，重点防护 V3 子评论需 `media_id` 这类细节陷阱
- **错误处理契约**：HTTP 状态码权威定义 + §3.1 防臆造自检清单（A: 5 步 / B: 6 步）+ V1↔V2↔V3 替换矩阵
