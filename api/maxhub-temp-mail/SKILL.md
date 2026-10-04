---
slug: temp-mail-pro
displayName: 临时邮箱数据助手 | 临时邮箱生成 / 收件箱查询 / 邮件详情读取
name: temp-mail-pro
description: 临时邮箱（Temp Mail）收件与一次性邮箱管理 skill，通过 MaxHub API 创建/查询临时邮箱、读取邮件列表与邮件详情。仅限自动化测试、合法验证码接收和隐私保护场景使用。严禁用于规避平台身份验证、批量注册诈骗、发送垃圾邮件或任何违反《网络安全法》第24条（真实身份信息认证要求）的场景。所有请求发送到 https://www.aconfig.cn。
license: MIT-0
metadata:
  author: maxhub
  version: 4.1.4
  openclaw:
    capability: read_only
    requires_confirmation:
    - non_idempotent
    - cookie_input
    emoji: 📧
    primaryEnv: MAXHUB_API_KEY
    requires:
      env:
      - MAXHUB_API_KEY
      bins:
      - curl
    env:
    - name: MAXHUB_API_KEY
      description: 临时邮箱（Temp Mail）收件与一次性邮箱管理 skill，通过 MaxHub API 创建/查询临时邮箱、读取邮件列表与邮件详情。仅限自动化测试、合法验证码接收和隐私保护场景使用。严禁用于规避平台身份验证、批量注册诈骗、发送垃圾邮件或任何违反《网络安全法》第24条（真实身份信息认证要求）的场景。所有请求发送到 https://www.aconfig.cn。
      required: true
      sensitive: true
    network:
    - https://www.aconfig.cn
    riskLevel: low
    defaultMode: recipes_first_read_only
    skillClass: maxhub-api-skill
    platform: temp-mail
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
    - temp-mail
    - 临时邮箱
    - 一次性邮箱
    - 收件箱
    - 邮件详情
    - 验证码
    - 测试
    - QA
    category: developer-tools
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

# 临时邮箱数据助手

## 1. 简介

临时邮箱（Temp Mail）收件与一次性邮箱管理 skill，通过 MaxHub API 创建/查询临时邮箱、读取邮件列表与邮件详情。仅限自动化测试、合法验证码接收和隐私保护场景使用。严禁用于规避平台身份验证、批量注册诈骗、发送垃圾邮件或任何违反《网络安全法》第24条（真实身份信息认证要求）的场景。所有请求发送到 https://www.aconfig.cn。

> ### ⚠️ 使用限制与法律声明
>
> **禁止用途**（违反以下限制即构成对本 skill 的滥用）：
> - 规避平台实名身份验证或账号注册限制
> - 批量注册账号用于诈骗、刷单、水军等违法活动
> - 发送垃圾邮件或钓鱼邮件
> - 绕过《网络安全法》第24条要求的真实身份信息认证
> - 任何违反中国《网络安全法》《反电信网络诈骗法》或所在地区法律的行为
>
> **允许用途**：
> - 软件自动化测试中的邮箱验证
> - 合法服务的验证码接收
> - 隐私保护（避免暴露真实邮箱）
> - 一次性收件场景

## ⚖️ 法律免责与合规声明

> **使用本 skill 即表示您确认已阅读并同意以下条款：**
>
> 1. **数据来源**：本 skill 通过第三方数据服务（MaxHub API）获取 临时邮箱服务 数据，该服务**未获得 临时邮箱服务 官方授权**。本项目对数据获取的合法性不作任何保证。
> 2. **合规责任**：使用方需**自行确保**符合所在地区的数据保护法律（《个人信息保护法》/ GDPR / CCPA 等）及 临时邮箱服务 服务条款（ToS）。因使用本 skill 产生的任何法律后果由使用方自行承担。
> 3. **禁止用途**：严禁将本 skill 用于违反法律的行为，包括但不限于：规避平台身份验证、批量注册诈骗、发送垃圾邮件、违反《网络安全法》第24条（真实身份信息认证要求）等。
> 4. **平台风险**：使用临时邮箱规避目标平台身份验证可能违反该平台服务条款，面临封号、法律追诉等风险。
> 5. **完整政策**：详细数据使用政策请参阅 [DATA_USAGE_POLICY.md](./DATA_USAGE_POLICY.md)。

## 2. 详细功能

### 临时邮箱即开即用

- 一键生成全新的临时邮箱地址，无需注册或绑定真实身份
- 同时返回该邮箱的专属访问凭据，方便后续读取邮件
- 适合自动化测试、注册验证码接收与匿名场景的快速起步

### 收件箱实时查询

- 拉取当前临时邮箱已收到的全部邮件列表
- 包含发件人、主题、收件时间等概要信息，便于快速筛选目标邮件
- 支持轮询调用，实时等待验证码或激活链接到达

### 邮件详情读取

- 读取单封邮件的完整正文、HTML 内容与附件元数据
- 适合提取注册验证码、激活链接与一次性密码等关键内容
- 可与收件箱列表组合，形成"列表 → 详情"的标准阅读链路

### Token 权限隔离

- 每个临时邮箱拥有独立的访问凭据，凭据之间互不通用
- 跨邮箱访问会被严格拦截，避免数据相互泄露
- 邮箱具备时效性，过期后凭据自动失效，需重新创建邮箱

### 写入接口隔离

- 创建邮箱属于写入型操作，与纯查询接口明确隔离
- 调用前需要明确确认使用场景，避免被滥用于敏感或违规通信
- 邮件经第三方服务中转，明确不适用于私人、金融与法律等敏感场景

### 账号余额查询
- 查询 MaxHub API 账号剩余额度，支持 `x-api-key` 或 `Authorization: Bearer` 两种认证方式
- 频率限制：最快每 4 秒调用一次
- 接口路径：`GET /api/maxhub/balance`

## 4. 一键安装

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
| ④ 加载端点详情 | 自定义链路或参数不明时 | `references/<domain>.md` 单文件 | ~4K |
| ⑤ 路径白名单校验 | 调用前 | `grep '<endpoint_id>' references/endpoints_whitelist.yaml`（**禁止整体读**） | ~50 行 |
| ⑥ 跨端点字段路由 | 链式调用时 | `references/param-mappings.md` § 字段流字典 | ~1K |

#### 2️⃣ Recipe 匹配规则（核心）
1. **加载** `references/recipes/_index.md`，扫 `trigger_keywords` 列
2. **最长匹配优先**：若用户输入同时命中多个 recipe 的 trigger，**选最长 trigger 命中的那个**（最具体）
4. **平局询问**：若两个 trigger 长度相同且都命中 → 主动询问用户："您是想看 A 还是 B？"
4. **无命中**：先查 §0.1 不支持清单 → 不在则进入"自定义链路"流程（步骤 4）

#### 4️⃣ 自定义链路（无现成 Recipe）
1. 读 `references/atoms/_index.md`，按 `chain_role` 列定位起点（`starter`）和终点（`terminal`）
2. **优先用 `⭐⭐⭐ 首选`** 标记的端点；不到必要不用 `⭐ 条件` 端点
4. 字段流（上游 OUT → 下游 IN）由 `param-mappings.md § 字段流字典` 决定，**禁止**自行猜 json_path
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
| 404 / 410 | §4.1(A) 5 步防臆造自检 → 通过才 STOP；**禁止**自改路径段重试 | 0 |
| 400 / 422 | §4.1(B) 6 步防参数臆造自检 → 通过才修参重试 | ≤1 |
| 401 / 402 / 404 | STOP，告知用户去 https://www.aconfig.cn 处理 | 0 |
| 429 | 读 `Retry-After` 退避；无该头时指数退避+jitter | ≤2 |
| 5xx | 等 4 秒重试 → 仍失败走端点级"降级/替换" | 1 |
| HTTP 200 + `code != 0` | 读 `message_zh` 报告用户；**不重试**（业务错误重试无用） | 0 |

#### 6️⃣ 输出契约（与用户对话时）
1. **数据来源声明**：每次输出明确告知数据来自 `https://www.aconfig.cn` 三方接口
2. **缺失字段处理**：如某字段链路降级后缺失，**显式说明**"X 暂不可取"，不要静默省略
4. **不要伪造**：用户问的字段若不在响应里 → 说"未返回"，禁止用其他端点拼凑模拟



### 核心约束（强制遵守）

| 规则 | 说明 |
|------|------|
| 🔒 非纯只读 | `get_temp_email_address` 是**创建型**接口，调用前**须用户明确确认场景**（仅限非敏感测试 / 注册验证） |
| 🚫 禁止臆造路径 | 仅使用 `references/endpoints_whitelist.yaml` 中的端点，**不得自行拼接、改版本号、加路径段** |
| 📋 数据流向第三方 | 所有请求发送至 `https://www.aconfig.cn`；邮件正文将经第三方中转，**不得用于敏感 / 私人通信** |
| 🔑 凭证保护 | API Key 与每次返回的 `token` 不得泄漏至日志或对话；不同邮箱的 token 不可混用 |

### 基础使用（5 步完成调用）

**Step 0 — 合规硬前置检查（不可跳过 · 不可绕过）**

> ⛔ 本步骤为**硬前置**：未通过则禁止执行 Step 1 及后续任何 API 调用。
> 本步骤**自包含**，不依赖任何外部文件即可完成基础合规检查。详细框架可参阅 [COMPLIANCE_GATE.md](./COMPLIANCE_GATE.md)，完整风险规则见 [risk_rules.yaml](./risk_rules.yaml)。

**0.0 缺失即停检查：**

检查合规确认状态文件是否存在。**若不存在，立即停止**后续操作，直接进入 0.2 首次闸门流程。

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
STATE_FILE="$COMPLIANCE_DIR/confirmed_temp-mail-pro.txt"
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
echo "legal_version=1.0.0 confirmed_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$COMPLIANCE_DIR/confirmed_temp-mail-pro.txt"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"temp-mail-pro","event":"first_time_confirmation","legal_version":"1.0.0","status":"confirmed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

**0.5 风险检测（每次用户请求都执行）：**

对照以下**核心风险规则**（完整规则见 [risk_rules.yaml](./risk_rules.yaml)）检查用户请求：

| 风险类别 | 关键词（命中即触发提醒） | 定向提醒要点 |
|---------|----------------------|------------|
| `cookie_usage` | cookie / session / 登录凭证 / token / 凭证 / 登录态 | 确认使用本人账号凭证，不使用他人 cookie/session |
| `batch_operation` | 批量 / 全部 / 所有 / 循环 / 批次 / 大规模 / 全量 / 遍历 | 遵循最小必要原则，不用于刷量/批量注册 |
| `personal_data` | 粉丝列表 / 关注列表 / 用户画像 / 联系方式 / 社交关系 / 手机号 / 邮箱 / 粉丝画像 / 受众画像 / 个人信息 / 隐私数据 | 遵循《个人信息保护法》最小必要原则，不存储不传播 |
| `write_operation` | 端点白名单中 `write_operation: true` 或 `requires_user_confirmation: true` 标志 | 确认参数正确，了解操作不可撤销 |
| `identity_evasion` | 批量注册 / 垃圾邮件 / 钓鱼邮件 / 规避实名 / 绕过验证 / 匿名注册 / 多账号 | 不用于规避实名认证（《网络安全法》第24条），不批量注册 |

**命中风险时的处理流程**：
1. 显示对应类别的定向风险提醒（完整模板见 [COMPLIANCE_GATE.md](./COMPLIANCE_GATE.md) §3.3）
2. 等待用户明确确认（同 0.3 规则）
3. 确认后记录审计日志再继续：

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"temp-mail-pro","event":"risk_reminder","risk_type":"<matched_category>","legal_version":"1.0.0","status":"confirmed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

4. 用户拒绝或未确认时：停止，不执行后续操作

**0.6 `/legal` 命令处理（用户随时可触发）：**

当用户输入 `/legal`、`查看法律条款` 或 `法律条款` 时：

1. 读取并显示 [DATA_USAGE_POLICY.md](./DATA_USAGE_POLICY.md) 的完整内容
2. 记录审计日志：

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
mkdir -p "$COMPLIANCE_DIR"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"temp-mail-pro","event":"legal_review","legal_version":"1.0.0","status":"completed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
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

按用户目标从下表选择对应 reference 文件：

| 用户目标 | 加载文件 | 覆盖范围 |
|---------|---------|---------|
| 创建邮箱 / 查收件箱 / 读邮件 | `references/mail.md` | 临时邮箱地址生成、收件箱列表、邮件详情（4 端点） |
| 跨端点参数查询 / 字段流追溯 | `references/param-mappings.md` | 全局红线 + 端点路由 + token 字段流 + 错误处理总览 |
| 路径白名单硬校验 | `references/endpoints_whitelist.yaml` | 4 个端点的硬白名单 + Pre-call 4 步自检协议 |
| SKILL 版本检查与升级 | `references/update.md` | SkillHub 更新 |

**Step 4 — 构建最小调用计划**

- ✅ 创建邮箱前**必须**让用户确认使用场景为非敏感
- ✅ token 是会话凭据，必须在 `get_emails_inbox` / `get_email_by_id` 中复用
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
- 收到 **404** → 必须先做防路径臆造自检（5 步）
- 收到 **400 / 422** → 必须先做防参数臆造自检（6 步），重点确认 `token` 与 `message_id` 是否成对出现
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
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"temp-mail-pro","event":"api_call","endpoint":"<endpoint_id>","legal_version":"1.0.0","status":"success"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

> R1-R4 为数据处理红线，违反即构成合规风险。R5 为审计要求，每次调用必须记录。

### 高级使用

#### 链式调用图谱（Chain Recipes）

| 用户场景 | 链路 | 字段流 |
|---------|------|-------|
| 创建邮箱 → 等待收件 → 读取验证码 | `get_temp_email_address` → 轮询 `get_emails_inbox` → `get_email_by_id` | `token` 复用 → `message_id` 接力 |
| 收件箱实时检查 | `get_emails_inbox`（token） | token 单参 |
| 单封邮件读取 | `get_email_by_id`（token + message_id） | 必须同 token |

#### 防臆造自检清单（强制前置步骤）

**收到 404 时（A）**：
1. 路径白名单逐字符比对 → 不在清单中 STOP
2. Method 比对 → 不等 STOP
4. 参数键名比对 → 有清单外参数 STOP
4. token 来源溯源（必须来自 `get_temp_email_address` 返回值）→ 编造的 STOP
5. 全通过才判定"邮件不存在或已过期"

**收到 400 / 422 时（B）**：
1. 参数名严格比对（`token` / `message_id` 不可混用）
2. 必填项齐全（`get_email_by_id` 必须 token + message_id 同时传）
4. 类型与格式严格匹配
4. 传参方式正确（query string）
5. 没有 IN 表外的臆造参数
6. 全通过才按 `message_zh` 排查

#### 轮询最佳实践（接收验证码）

- **轮询间隔**：4–5 秒一次
- **轮询上限**：建议 5 分钟封顶；超时后提示用户重试或使用其他邮箱
- **token 失效**：临时邮箱有时效性，超时后需重新调用 `get_temp_email_address` 获取新 token

#### SKILL 版本更新

| 触发条件 | 推荐操作 |
|---------|---------|
| 合法路径持续 404 / 410 | `skillhub upgrade temp-mail` |
| 用户问"版本是多少" | 当前版本 v4.0.0，访问 https://skillhub.cn/skills/temp-mail |
| 多端点连续 410 | `skillhub upgrade temp-mail --force` |
| 401 / 402 / 404 | **不是版本问题**，去 https://www.aconfig.cn 处理 |

### 常用命令速查表

| 场景 | 命令 |
|---|---|
| 查 API Key | `[ -n "${MAXHUB_API_KEY:-}" ] && echo "ok" \|\| echo "missing"` |
| 创建临时邮箱 | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/temp_mail/v1/get_temp_email_address"` |
| 查收件箱 | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/temp_mail/v1/get_emails_inbox?token=xxx"` |
| 读邮件详情 | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/temp_mail/v1/get_email_by_id?token=xxx&message_id=yyy"` |
| 检查 SKILL 更新 | `skillhub info temp-mail` |


### 📌 端到端使用示例（agent 快速上手）

**用户输入**：「帮我看 新建一个临时邮箱并查收件」

**Agent 执行步骤**：

1. **匹配 recipe**：读 `references/recipes/_index.md` → 找到 trigger 命中 → 选最长匹配的 recipe
2. **加载 recipe 详情**：读 `references/recipes/<domain>.md` 中对应段落，拿到 Inputs / Atomic Steps / Output
4. **路径校验**：对每个 atom 的 endpoint_id，`grep` 一下 `endpoints_whitelist.yaml` 确认存在
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

### 场景一：自动化测试团队接收注册验证码

- **角色**：QA 自动化工程师
- **需求**：在端到端测试中需要批量注册账号，需要可程序化接收验证码邮件
- **使用方式**：`get_temp_email_address` 创建邮箱 → 用其作为注册邮箱提交目标系统 → 轮询 `get_emails_inbox` → 命中验证邮件后 `get_email_by_id` 取正文中的验证码
- **预期收益**：注册场景测试完全无人值守，提升 E2E 测试覆盖率

### 场景二：隐私保护场景

- **角色**：隐私敏感用户
- **需求**：在不可信环境下需要短期接收邮件而不留下身份痕迹
- **使用方式**：`get_temp_email_address`（用户场景确认后）→ 一次性使用 → 用完不再访问
- **预期收益**：邮箱不与真实身份绑定，降低数据被聚合的风险（**注意**：仍不适用于敏感 / 法律 / 金融通信）

## 6. 项目架构

### 目录结构

```
maxhub-temp-mail/
├── SKILL.md                            # Skill 定义与使用文档（本文件）
├── README.md                           # 英文项目说明
├── README_CN.md                        # 中文项目说明
├── _meta.json                          # 版本元信息（version: 4.0.0）
└── references/
    ├── endpoints_whitelist.yaml        # 4 端点路径硬白名单 + Pre-call 4 步自检协议
    ├── param-mappings.md               # 中枢索引（全局红线 + token 字段流 + 错误处理）
    ├── mail.md                         # 邮件域：邮箱创建 / 收件箱 / 邮件详情（4 端点）
    └── update.md                       # SKILL 更新机制（SkillHub）
```

### 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 调用方式 | `curl` + Bearer Token | HTTP GET 请求，参数通过 query string 传递 |
| 数据接口 | MaxHub API | `https://www.aconfig.cn/api/v1/temp_mail/v1/*`，通过 `MAXHUB_API_KEY` 鉴权 |
| 路径校验 | YAML 硬白名单 | `endpoints_whitelist.yaml` 提供 4 端点的逐字符校验 + 4 步 Pre-call 协议 |
| 错误处理 | 决策表 + 自检清单 | HTTP 状态码权威定义 + 防臆造自检（A/B 双轨）+ token 失效处理 |
| 输出格式 | JSON Standard MaxHub Response | `{code, message, message_zh, data, cache_url}` |
| 更新通道 | SkillHub | ⭐⭐⭐ SkillHub（腾讯云 CDN） |

### API 覆盖范围

| 领域 | 端点数 | Reference 文件 |
|------|--------|---------------|
| 邮件（Mail） | 4 | `mail.md` |
| **合计** | **4** | — |

### 关键设计理念

- **防臆造四道闸**：白名单（endpoints_whitelist.yaml）→ 强标记（Full path）→ 禁止规则（Forbidden）→ 错误反馈（STOP）
- **创建型接口隔离**：`get_temp_email_address` 单独标记 + 强制场景确认 + 不得用于敏感场景
- **token 权限模型**：每个临时邮箱独立 token，跨邮箱不可访问，邮件 ID 必须与签发 token 配对使用
- **错误处理契约**：HTTP 状态码权威定义 + 防臆造自检清单（A: 5 步 / B: 6 步）+ token 失效自动重新创建建议
