---
slug: sora2
displayName: Sora2 数据助手 | 动态帖子 / 评论 / 二创 / 用户
name: sora2
description: Sora2 内容创作与作品分析 skill，通过 MaxHub API 查询作品、用户、评论、回复、二创/Remix、下载/媒体信息，并支持上传图片、创建视频等创作相关写操作。适合 AI 视频创作工作流、作品复盘、二创传播分析和素材管理。属于 read_write skill；agent 对 create/upload/download 等非只读能力必须按 confirmation 规则确认，普通查询优先走 recipes 与字段流字典。所有请求发送到 https://www.aconfig.cn。
license: MIT-0
metadata:
  author: maxhub
  version: 4.1.4
  openclaw:
    capability: read_write
    requires_confirmation:
    - write
    - non_idempotent
    - media_upload
    - download
    emoji: 🎥
    primaryEnv: MAXHUB_API_KEY
    requires:
      env:
      - MAXHUB_API_KEY
      bins:
      - curl
    env:
    - name: MAXHUB_API_KEY
      description: Sora2 内容创作与作品分析 skill，通过 MaxHub API 查询作品、用户、评论、回复、二创/Remix、下载/媒体信息，并支持上传图片、创建视频等创作相关写操作。适合 AI 视频创作工作流、作品复盘、二创传播分析和素材管理。属于 read_write skill；agent 对 create/upload/download 等非只读能力必须按 confirmation 规则确认，普通查询优先走 recipes 与字段流字典。所有请求发送到 https://www.aconfig.cn。
      required: true
      sensitive: true
    network:
    - https://www.aconfig.cn
    riskLevel: medium
    defaultMode: recipes_first_confirm_write
    skillClass: maxhub-api-skill
    platform: sora2
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
    - sora2
    - AI视频
    - 作品
    - 评论
    - 回复
    - Remix
    - 二创
    - 下载
    - 上传
    - 创建视频
    - read_write
    category: creative
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

# Sora2 数据助手

## 1. 简介

Sora2 内容创作与作品分析 skill，通过 MaxHub API 查询作品、用户、评论、回复、二创/Remix、下载/媒体信息，并支持上传图片、创建视频等创作相关写操作。适合 AI 视频创作工作流、作品复盘、二创传播分析和素材管理。属于 read_write skill；agent 对 create/upload/download 等非只读能力必须按 confirmation 规则确认，普通查询优先走 recipes 与字段流字典。所有请求发送到 https://www.aconfig.cn。

> **架构亮点**：本 Skill 采用三层结构 — **Atomic 原子层**（端点的标准化封装）+ **Recipe 编排层**（多步业务场景脚本）+ **Reference 详情层**（端点 5 区契约）。Agent 可按"目标 → recipes 匹配 → atoms 映射 → reference 详情"四步路径精准调用，杜绝臆造。

## 2. 详细功能

### 作品数据
- 查询 Sora2 作品的完整详情，包含作者信息、视频内容、点赞/评论/转发统计、Cameo 出镜信息等
- 支持通过作品 ID 或作品分享链接两种方式查询作品
- 拉取指定作品下的一级评论列表，支持翻页
- 拉取指定评论下的全部二级回复，构建完整评论树
- 查询某个作品的全部 Remix 二创列表，追踪内容传播链路
- 获取作品的无水印视频下载链接，下载受限时自动降级为带水印版本
- 拉取 Sora2 首页的推荐 Feed 流，识别近期热门作品

### 用户数据
- 按用户名搜索 Sora2 平台用户
- 查询指定用户的完整资料画像，包含昵称、头像、简介、粉丝数、作品数、Cameo 数等
- 拉取指定用户已发布的全部作品列表
- 查看指定用户的关注列表与粉丝列表
- 拉取指定用户的 Cameo 出镜记录，分析其在他人作品中的出镜表现

### AI 视频生成
- 上传图片素材，作为后续图生视频任务的输入
- 创建文生视频任务，根据文字 prompt 生成 Sora2 视频
- 创建图生视频任务，基于上传的图片素材生成 Sora2 视频
- 轮询查询视频生成任务的实时状态（排队中、生成中、已完成、失败）
- 获取视频生成任务完成后的最终视频 URL 与元信息

### 平台热榜
- 拉取 Sora2 全平台 Cameo 出镜热度榜单，识别平台明星用户与高频出镜内容

### 账号余额查询
- 查询 MaxHub API 账号剩余额度，支持 `x-api-key` 或 `Authorization: Bearer` 两种认证方式
- 频率限制：最快每 3 秒调用一次
- 接口路径：`GET /api/maxhub/balance`

## ⚖️ 法律免责与合规声明

> **使用本 skill 即表示您确认已阅读并同意以下条款：**
>
> 1. **数据来源**：本 skill 通过第三方数据服务（MaxHub API）获取 Sora2 数据，该服务**未获得 Sora2 官方授权**。本项目对数据获取的合法性不作任何保证。
> 2. **合规责任**：使用方需**自行确保**符合所在地区的数据保护法律（《个人信息保护法》/ GDPR / CCPA 等）及 Sora2 服务条款（ToS）。因使用本 skill 产生的任何法律后果由使用方自行承担。
> 3. **禁止用途**：严禁将本 skill 用于违反法律的行为，包括但不限于：侵犯个人信息权、不正当竞争、刷量操控、批量爬取用户数据等。
> 4. **平台风险**：Sora2 可能对未授权数据访问采取封号、内容下架等法律行动。
> 5. **完整政策**：详细数据使用政策请参阅 [DATA_USAGE_POLICY.md](./DATA_USAGE_POLICY.md)。

> ### 📋 数据传输与隐私声明（请认真阅读）
>
> 1. **第三方传输**：您提供的所有 ID、关键词、链接等参数都会通过 HTTPS 发送到 **`https://www.aconfig.cn`**（MaxHub 数据服务）进行处理。
> 2. **UGC 隐私**：拉回的 评论 / 回复 / 二创作品 等内容可能包含个人信息或敏感 UGC，请勿写入未授权的数据库或公开发布。
> 3. **凭证保护**：建议使用**独立测试账号**、定期轮换 API Key。
> 4. **合规责任**：使用方需自行确保符合所在地区的数据保护法律（《个人信息保护法》/ GDPR / Sora2 ToS 等），平台账号的合规性由使用方承担。

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
| 🔒 只读优先 | 默认仅用于数据查询；`create_video` / `upload_image` 为写入接口，**须用户明确确认参数后调用** |
| 🚫 禁止臆造路径 | 仅使用 `references/endpoints_whitelist.yaml` 中的端点，**不得自行拼接、改版本号、加路径段** |
| 🧭 优先走编排 | 优先尝试匹配 `recipes/_index.md` 中的预编排脚本；命中即按 Atomic Steps 顺序调用，避免临场拼凑 |
| 📋 数据流向第三方 | 所有请求发送至 `https://www.aconfig.cn`，请使用独立测试账号并定期轮换 API Key |
| 🔑 凭证保护 | 不暴露 API Key、Cookie、Token 至日志或对话 |

### 路由策略：Recipes → Atoms → Reference 三级路径

> Agent 接到用户请求后，**优先按"先编排、后原子、再详情"的顺序进入文档**，避免一上来就读全部 reference。

```
用户输入
   ↓
① 读 recipes/_index.md（轻量索引，~100 行）
   ↓ 匹配 trigger_keywords（命中 → 走 Recipe；未命中 → 步骤 ②）
   ↓
② 读 atoms/_index.md（原子映射表，~30 行核心）
   ↓ 按业务别名找 atom_id → endpoint_id → reference 文件
   ↓
③ 仅在需要 5 区契约（IN/OUT/ERR）时，读对应 reference 文件
   ↓
④ 调用前比对 endpoints_whitelist.yaml 完成 4 步 Pre-call 自检
```

### 基础使用（6 步完成调用）

**Step 0 — 合规硬前置检查（不可跳过 · 不可绕过）**

> ⛔ 本步骤为**硬前置**：未通过则禁止执行 Step 1 及后续任何 API 调用。
> 本步骤**自包含**，不依赖任何外部文件即可完成基础合规检查。详细框架可参阅 [COMPLIANCE_GATE.md](./COMPLIANCE_GATE.md)，完整风险规则见 [risk_rules.yaml](./risk_rules.yaml)。

**0.0 缺失即停检查：**

检查合规确认状态文件是否存在。**若不存在，立即停止**后续操作，直接进入 0.2 首次闸门流程。

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
STATE_FILE="$COMPLIANCE_DIR/confirmed_sora2.txt"
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
echo "legal_version=1.0.0 confirmed_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$COMPLIANCE_DIR/confirmed_sora2.txt"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"sora2","event":"first_time_confirmation","legal_version":"1.0.0","status":"confirmed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

**0.5 风险检测（每次用户请求都执行）：**

对照以下**核心风险规则**（完整规则见 [risk_rules.yaml](./risk_rules.yaml)）检查用户请求：

| 风险类别 | 关键词（命中即触发提醒） | 定向提醒要点 |
|---------|----------------------|------------|
| `cookie_usage` | cookie / session / 登录凭证 / token / 凭证 / 登录态 | 确认使用本人账号凭证，不使用他人 cookie/session |
| `batch_operation` | 批量 / 全部 / 所有 / 循环 / 批次 / 大规模 / 全量 / 遍历 | 遵循最小必要原则，不用于刷量/批量注册 |
| `personal_data` | 粉丝列表 / 关注列表 / 用户画像 / 联系方式 / 社交关系 / 手机号 / 邮箱 / 粉丝画像 / 受众画像 / 个人信息 / 隐私数据 | 遵循《个人信息保护法》最小必要原则，不存储不传播 |
| `write_operation` | 端点白名单中 `write_operation: true` 或 `requires_user_confirmation: true` 标志 | 确认参数正确，了解操作不可撤销 |

**命中风险时的处理流程**：
1. 显示对应类别的定向风险提醒（完整模板见 [COMPLIANCE_GATE.md](./COMPLIANCE_GATE.md) §3.3）
2. 等待用户明确确认（同 0.3 规则）
3. 确认后记录审计日志再继续：

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"sora2","event":"risk_reminder","risk_type":"<matched_category>","legal_version":"1.0.0","status":"confirmed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

4. 用户拒绝或未确认时：停止，不执行后续操作

**0.6 `/legal` 命令处理（用户随时可触发）：**

当用户输入 `/legal`、`查看法律条款` 或 `法律条款` 时：

1. 读取并显示 [DATA_USAGE_POLICY.md](./DATA_USAGE_POLICY.md) 的完整内容
2. 记录审计日志：

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
mkdir -p "$COMPLIANCE_DIR"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"sora2","event":"legal_review","legal_version":"1.0.0","status":"completed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

3. 显示完毕后，根据当前是否已通过首次闸门决定下一步：
   - 未通过首次闸门 → 返回 0.2 继续等待用户确认
   - 已通过首次闸门 → 询问用户是否继续之前的操作

**Step 1 — 检查 API Key**

```bash
[ -n "${MAXHUB_API_KEY:-}" ] && echo "ok" || echo "missing"
```

若返回 `missing`，停止并提示用户配置 `MAXHUB_API_KEY`。

**Step 2 — 优先匹配 Recipe（编排层）**

读 `references/recipes/_index.md`，按用户目标匹配 `trigger_keywords`：

| Recipe 文件 | 覆盖场景 | 典型触发词 |
|-----------|---------|----------|
| `recipes/post.md` | 作品全维度分析、评论回复链、Remix 传播图谱、视频下载 | 帖子分析、评论、回复、二创、下载 |
| `recipes/user.md` | 用户画像、作品列表、社交关系、Cameo 出镜分析 | 用户分析、粉丝、关注、Cameo |
| `recipes/tools.md` | AI 视频生成（文生/图生）、任务轮询、Cameo 热榜 | 生成视频、文生视频、图生视频、热榜 |

命中 Recipe → 直接按其 Atomic Steps 顺序执行，跳到 Step 5。

**Step 3 — Recipe 未命中：进入原子层**

读 `references/atoms/_index.md`，按业务别名（atom_id）找到对应 endpoint_id：

| 业务别名 | atom_id | 端点 | 用途 |
|---------|---------|-----|------|
| 查作品 | `get_post` | get_post_detail | 作品详情 |
| 查评论 | `list_comments` | get_post_comments | 一级评论 |
| 查回复 | `list_replies` | get_comment_replies | 二级回复 |
| 查 Remix | `list_remix` | get_post_remix_list | 二创列表 |
| 查下载 | `get_download` | get_video_download_info | 无水印 URL |
| 查 Feed | `get_feed` | get_feed | 推荐流 |
| 搜用户 | `search_users` | search_users | 用户名搜索 |
| 查用户主页 | `get_profile` | get_user_profile | 用户资料 |
| 查用户作品 | `list_user_posts` | get_user_posts | 用户作品 |
| 查关注 | `list_following` | get_user_following | 关注列表 |
| 查粉丝 | `list_followers` | get_user_followers | 粉丝列表 |
| 查 Cameo 出镜 | `list_cameo` | get_user_cameo_appearances | 出镜记录 |
| 上传图片 ⚠️ | `upload_image` | upload_image | 写入：图片上传 |
| 创建视频 ⚠️ | `create_video` | create_video | 写入：AI 视频生成 |
| 查任务状态 | `get_task_status` | get_task_status | 异步任务进度 |
| 查任务详情 | `get_task_detail` | get_task_detail | 最终视频 URL |
| 查 Cameo 热榜 | `get_cameo_board` | get_cameo_leaderboard | 全平台热榜 |

**Step 4 — 仅按需读 reference 详情层**

按 atom 表中 `file` 字段找对应详情：

| Reference 文件 | 覆盖端点数 | 5 区结构 |
|--------------|-----------|---------|
| `references/post.md` | 6 | 用途 / USE 边界 / IN（参数表）/ OUT（链式字段）/ ERR（错误处理）|
| `references/user.md` | 6 | 同上 |
| `references/tools.md` | 5 | 同上（含写入端点的 requires_user_confirmation 标记）|
| `references/param-mappings.md` | — | 中枢索引（全局红线 + 字段流字典 + 错误处理 + 替换矩阵）|
| `references/endpoints_whitelist.yaml` | 18 | 路径硬白名单 + Pre-call 4 步自检协议 |
| `references/update.md` | — | SkillHub 更新 |


**🔍 运行时合规自检（构建调用计划时必须逐项确认）：**

| # | 检查项 | 通过条件 | 不通过处理 |
|---|--------|---------|-----------|
| C1 | 意图合法性 | 用户请求属于合法场景（公开数据分析/竞品研究/内容创作辅助/学术研究/自动化测试） | STOP，告知用户该用途不在合法范围内 |
| C2 | 参数来源 | 所有 ID/关键词/链接来自用户本人提供或公开可见内容 | STOP，要求用户说明数据来源 |
| C3 | 无他人凭证 | 请求不涉及使用他人 cookie/session/token | STOP，要求使用本人账号凭证 |
| C4 | 最小必要 | 请求范围已限定在最小必要数据，非批量/全量采集 | STOP，要求用户明确缩小范围 |
| C5 | 端点合规 | 目标端点在 `endpoints_whitelist.yaml` 中且未被移除 | STOP，告知该端点不可用 |

> 任一项不通过即停止，不进入执行步骤。已通过 Step 0.5 风险确认的请求无需重复 C4。

**Step 5 — 执行并验证**

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
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"sora2","event":"api_call","endpoint":"<endpoint_id>","legal_version":"1.0.0","status":"success"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

> R1-R4 为数据处理红线，违反即构成合规风险。R5 为审计要求，每次调用必须记录。

### 高级使用

#### 链式调用图谱（来自 recipes/）

| 用户场景 | 链路 | 字段流 | Recipe 位置 |
|---------|------|-------|------------|
| 查作品 + 评论 + 回复 | `get_post` → `list_comments` → `list_replies` | `post_id` → `comment_id` 接力 | `recipes/post.md` |
| 下载作品视频 | `get_post` → `get_download` | `post_id` 复用 | `recipes/post.md` |
| 看作品 + 二创 | `get_post` → `list_remix` | `post_id` 复用 | `recipes/post.md` |
| 用户名 → 用户作品 | `search_users` → `get_profile` → `list_user_posts` | `username` → `user_id` | `recipes/user.md` |
| 文生视频（异步） | `create_video` → 轮询 `get_task_status` → `get_task_detail` | `task_id` 接力 | `recipes/tools.md` |
| 图生视频（异步） | `upload_image` → `create_video` → 轮询 → `get_task_detail` | `image_id` → `task_id` | `recipes/tools.md` |
| Cameo 热榜 → 用户主页 | `get_cameo_board` → `get_profile` | `user_id` 复用 | `recipes/tools.md` |

#### 防臆造自检清单（强制前置步骤）

**收到 404 时（A）**：
1. 路径白名单逐字符比对 → 不在清单中 STOP
2. Method 比对 → 不等 STOP
3. 参数键名比对 → 有清单外参数 STOP
4. 资源 ID 来源溯源 → Agent 编造的 STOP
5. 全通过才判定"上游资源不存在"

**收到 400 / 422 时（B）**：
1. 参数名严格比对（大小写 / 缩写 / 复数）
2. 必填项齐全 + oneOf 二选一逻辑
3. 类型与格式严格匹配（pattern / enum）
4. 传参方式正确（query vs body）
5. 没有 IN 表外的臆造参数
6. 全通过才按 `message_zh` 排查

#### 异步任务最佳实践（仅适用 create_video）

- **轮询间隔**：5–10 秒一次
- **状态语义**：`pending` / `running` 不视为失败，必须继续轮询
- **轮询上限**：建议 10 分钟封顶；超时后把 `task_id` 返回用户
- **推荐**：宿主 Agent 支持子会话时，spawn 子会话专职轮询，主会话保持响应

#### SKILL 版本更新

| 触发条件 | 推荐操作 |
|---------|---------|
| 合法路径持续 404 / 410 | `skillhub upgrade sora2` |
| 用户问"版本是多少" | 当前版本 v4.0.0，访问 https://skillhub.cn/skills/sora2 |
| 多端点连续 410 | `skillhub upgrade sora2 --force` |
| 401 / 402 / 403 | **不是版本问题**，去 https://www.aconfig.cn 处理 |

### 常用命令速查表

| 场景 | 命令 |
|---|---|
| 查 API Key | `[ -n "${MAXHUB_API_KEY:-}" ] && echo "ok" \|\| echo "missing"` |
| 查作品详情 | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/sora2/get_post_detail?post_id=s_xxx"` |
| 查作品评论 | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/sora2/get_post_comments?post_id=s_xxx"` |
| 查任务状态（轮询） | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/sora2/get_task_status?task_id=xxx"` |
| 检查 SKILL 更新 | `skillhub info sora2` |


### 📌 端到端使用示例（agent 快速上手）

**用户输入**：「帮我看 Sora2 某个 post_id 的二创列表」

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

### 场景一：Sora2 内容创作者寻找爆款规律

- **角色**：Sora2 内容创作者
- **需求**：想分析近期 Sora2 平台的热门作品有哪些共同特征，寻找下一个 Remix 灵感
- **使用方式**：匹配 `recipes/post.md` 中的 `trending_post_analysis` Recipe → 自动按 `get_feed` → `get_post` 链路执行
- **预期收益**：通过 Feed + 详情链路快速锁定高 totalScore 作品，提炼可复用的提示词模板

### 场景二：AI 视频研究者批量采集 Cameo 数据

- **角色**：AI 视频领域研究者
- **需求**：需要全平台 Cameo 出镜热榜及上榜用户的完整出镜记录，分析 Cameo 传播规律
- **使用方式**：匹配 `recipes/tools.md` 中的 `cameo_full_dataset` Recipe → 按 `get_cameo_board` → `list_cameo` 批量执行
- **预期收益**：一次调用矩阵覆盖全平台 Top Cameo 用户，构建完整的 Cameo 数据集

### 场景三：社媒分析师追踪 Remix 传播链

- **角色**：社媒数据分析师
- **需求**：跟踪某个爆款作品的全部 Remix 二创及其作者，绘制传播图谱
- **使用方式**：匹配 `recipes/post.md` 中的 `remix_chain_analysis` Recipe → `get_post` → `list_remix` → `get_profile` 三步走
- **预期收益**：完整的内容传播链分析，识别 KOL 二创节点

## 6. 项目架构

### 目录结构（Atoms + Recipes + Reference 三层）

```
maxhub-sora2/
├── SKILL.md                            # Skill 定义与使用文档（本文件）
├── README.md                           # 英文项目说明
├── README_CN.md                        # 中文项目说明
├── _meta.json                          # 版本元信息（version: 4.0.0）
└── references/
    ├── atoms/                          # ⚛️ 原子层（标准化端点封装）
    │   └── _index.md                   #   18 端点 × 业务别名映射表（atom_id / chain_role / idempotent / write_op）
    ├── recipes/                        # 📜 编排层（多步业务场景脚本）
    │   ├── _index.md                   #   全部 Recipe 索引（trigger_keywords + 文件路径）
    │   ├── post.md                     #   作品域 Recipes（详情/评论/Remix/下载等）
    │   ├── user.md                     #   用户域 Recipes（画像/社交/Cameo 出镜）
    │   └── tools.md                    #   工具域 Recipes（视频生成/任务轮询/热榜）
    ├── post.md                         # 📖 Reference 详情：作品域 6 端点（5 区契约）
    ├── user.md                         # 📖 Reference 详情：用户域 6 端点
    ├── tools.md                        # 📖 Reference 详情：工具域 5 端点（含写入）
    ├── param-mappings.md               # 🔗 中枢索引（全局红线 + 字段流字典 + 错误处理 + 替换矩阵）
    ├── endpoints_whitelist.yaml        # 🛡️ 18 端点路径硬白名单 + Pre-call 4 步自检协议
    └── update.md                       # 🔄 SKILL 更新机制（SkillHub）
```

### 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 调用方式 | `curl` + Bearer Token | 查询用 HTTP GET（参数走 query string）；写操作（upload_image / create_video）用 POST |
| 数据接口 | MaxHub API | `https://www.aconfig.cn/api/v1/sora2/*`，通过 `MAXHUB_API_KEY` 鉴权 |
| 原子层 | atoms/_index.md | 端点封装为 atom，含业务别名 + 链路角色 + 幂等性 + 写入标记 |
| 编排层 | recipes/*.md | 多步业务脚本，含 trigger_keywords + Atomic Steps + 字段流绑定 + on_err |
| 路径校验 | YAML 硬白名单 | `endpoints_whitelist.yaml` 提供 18 端点的逐字符校验 + 4 步 Pre-call 协议 |
| 错误处理 | 决策表 + 自检清单 | HTTP 状态码权威定义 + 防臆造自检（A/B 双轨）+ 重试策略矩阵 |
| 输出格式 | JSON Standard MaxHub Response | `{code, message, message_zh, data, cache_url}` |
| 更新通道 | SkillHub | ⭐⭐⭐ SkillHub（腾讯云 CDN） |

### API 覆盖范围

| 领域 | 端点数 | 原子数 | Recipes 数 | Reference 文件 |
|------|--------|-------|----------|---------------|
| 作品（Posts） | 6 | 6 | 5+ | `post.md` |
| 用户（Users） | 6 | 6 | 4+ | `user.md` |
| 工具与 Cameo（Tools） | 5 | 5 | 5+ | `tools.md` |
| **合计** | **18** | **18** | **14** | — |

### 关键设计理念

- **三层架构**：Atomic 原子层（端点标准化）+ Recipe 编排层（业务场景脚本）+ Reference 详情层（5 区契约），Agent 按"目标 → recipes → atoms → reference"四步精准定位
- **防臆造四道闸**：白名单（endpoints_whitelist.yaml）→ 强标记（Full path）→ 禁止规则（Forbidden）→ 错误反馈（STOP）
- **Agent 友好 7 大原则**：结构胜于叙述、明确指令优于建议、单一来源、词法稳定性、低 token 密度、边界显式声明、错误处理是契约
- **链式调用图谱**：字段流字典 + Recipe Atomic Steps + 跨 reference 链路三层联动，杜绝 Agent 编造字段名
- **错误处理契约**：HTTP 状态码权威定义 + §3.1 防臆造自检清单（A: 5 步 / B: 6 步）+ 重试策略矩阵 + 端点替换矩阵
