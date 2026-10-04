---
slug: weibo-pro
displayName: 微博数据助手 | 博文 / 评论 / 转发 / 互动
name: weibo-pro
description: 微博（Weibo）公开社交数据查询与热点分析 skill，通过 MaxHub API 查询微博内容、评论、转发、用户资料、粉丝/关注、搜索、热搜、话题和榜单。适合舆情监测、热点追踪、KOL 画像、内容传播分析和竞品研究。默认 read-only；agent 应优先使用 recipes 串联搜索→微博详情→评论/用户画像等流程，避免自行猜测 mid/uid/container_id 参数。所有请求发送到 https://www.aconfig.cn。
license: MIT-0
metadata:
  author: maxhub
  version: 4.1.4
  openclaw:
    capability: read_only
    requires_confirmation:
    - non_idempotent
    - cookie_input
    emoji: 🐦
    primaryEnv: MAXHUB_API_KEY
    requires:
      env:
      - MAXHUB_API_KEY
      bins:
      - curl
    env:
    - name: MAXHUB_API_KEY
      description: 微博（Weibo）公开社交数据查询与热点分析 skill，通过 MaxHub API 查询微博内容、评论、转发、用户资料、粉丝/关注、搜索、热搜、话题和榜单。适合舆情监测、热点追踪、KOL 画像、内容传播分析和竞品研究。默认 read-only；agent 应优先使用 recipes 串联搜索→微博详情→评论/用户画像等流程，避免自行猜测 mid/uid/container_id 参数。所有请求发送到 https://www.aconfig.cn。
      required: true
      sensitive: true
    network:
    - https://www.aconfig.cn
    riskLevel: low
    defaultMode: recipes_first_read_only
    skillClass: maxhub-api-skill
    platform: weibo
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
    - weibo
    - 微博
    - 微博内容
    - 评论
    - 转发
    - 用户资料
    - 热搜
    - 话题
    - 榜单
    - 舆情
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

# 微博数据助手

## 1. 简介

微博（Weibo）公开社交数据查询与热点分析 skill，通过 MaxHub API 查询微博内容、评论、转发、用户资料、粉丝/关注、搜索、热搜、话题和榜单。适合舆情监测、热点追踪、KOL 画像、内容传播分析和竞品研究。默认 read-only；agent 应优先使用 recipes 串联搜索→微博详情→评论/用户画像等流程，避免自行猜测 mid/uid/container_id 参数。所有请求发送到 https://www.aconfig.cn。

## 2. 详细功能

### 微博内容
- 查询任意微博的完整详情，包括正文、图片/视频附件、发布时间、来源、互动数据
- 支持 App、Web、Web 新版三端不同视角的微博详情，适配舆情研究与样本采集需求
- 拉取某条微博的转发列表，绘制传播路径并识别关键扩散节点
- 拉取某条微博的点赞用户列表，分析受众画像与互动质量
- 检查微博是否允许带图评论，识别博主互动权限设置

### 视频与频道
- 查询微博视频内容的完整详情，包括视频流地址、封面、时长与互动数据
- 拉取视频精选 Feed，了解平台视频侧的算法分发池
- 拉取视频频道的配置列表与各频道信息流，按垂类切片采集视频
- 拉取频道置顶/趋势内容，定位频道下的当前热门视频

### 发现与首页推荐
- 拉取 App 端首页推荐信息流，还原平台主页算法分发结果
- 拉取 Web 新版用户推荐时间线，对比不同端口的推荐策略

### 用户画像
- 查询微博用户的基础资料与详细资料，覆盖昵称、简介、认证、粉丝数、关注数等核心画像字段
- 支持通过用户 ID 或自定义域名（用户主页短链）两种入口定位用户
- 拉取用户的微博时间线，覆盖完整发布记录与历史轨迹
- 拉取用户的原创微博列表（剔除转发），用于评估真实内容产能
- 在用户主页内进行站内搜索，定位特定话题或时间段的发博记录
- 拉取用户的视频/超话/相册/文章/音频等多形态内容列表，构建立体内容画像
- 拉取用户主页 Feed 综合推荐
- 查询用户的视频合集列表与某个合集的详情、合集内视频列表，追踪连载内容
- 拉取用户的关注列表、粉丝列表与全部分组，分析社交图谱与圈层归属

### 评论与回复
- 拉取任意微博的一级评论列表，覆盖 App、Web、Web 新版三端
- 接力拉取评论的二级回复与楼中楼，还原完整讨论结构
- 兼容不同评论排序口径（热门/最新），适配不同分析场景

### 综合搜索矩阵
- 执行微博综合搜索，覆盖图文、视频、用户、话题等全类型结果
- 执行 AI 智能搜索与 AI 关联搜索，按语义返回相关微博与衍生话题
- 执行高级搜索，支持地域、性别、年龄、学校、工作、时间范围等多维筛选条件
- 执行实时搜索，捕捉当前正在发生的讨论与突发事件
- 按维度切分的专题搜索：用户搜索、视频搜索、图片搜索、话题搜索
- 拉取相似搜索建议，扩展长尾关键词与衍生话题
- 查询全国城市列表，配合高级搜索做地理舆情筛选

### 热搜与榜单
- 拉取微博实时热搜榜，覆盖 App、Web、Web 新版三端权威口径
- 拉取热搜分类榜单，按娱乐/社会/财经等垂类切片热点
- 拉取热搜的索引视图与摘要视图，分别对接概览与深度阅读两种使用场景
- 拉取话题搜索榜，识别当下高热话题
- 拉取文娱榜、社会榜、生活榜，按行业垂类追踪头部话题
- 拉取热搜榜单时间线，回看热搜词的上榜时间与停留轨迹

### 账号余额查询
- 查询 MaxHub API 账号剩余额度，支持 `x-api-key` 或 `Authorization: Bearer` 两种认证方式
- 频率限制：最快每 3 秒调用一次
- 接口路径：`GET /api/maxhub/balance`

## ⚖️ 法律免责与合规声明

> **使用本 skill 即表示您确认已阅读并同意以下条款：**
>
> 1. **数据来源**：本 skill 通过第三方数据服务（MaxHub API）获取 微博（Weibo） 数据，该服务**未获得 微博（Weibo） 官方授权**。本项目对数据获取的合法性不作任何保证。
> 2. **合规责任**：使用方需**自行确保**符合所在地区的数据保护法律（《个人信息保护法》/ GDPR / CCPA 等）及 微博（Weibo） 服务条款（ToS）。因使用本 skill 产生的任何法律后果由使用方自行承担。
> 3. **禁止用途**：严禁将本 skill 用于违反法律的行为，包括但不限于：侵犯个人信息权、不正当竞争、刷量操控、批量爬取用户数据等。
> 4. **平台风险**：微博可能对未授权数据访问采取封号、诉讼等法律行动。
> 5. **完整政策**：详细数据使用政策请参阅 [DATA_USAGE_POLICY.md](./DATA_USAGE_POLICY.md)。

> ### 📋 数据传输与隐私声明（请认真阅读）
>
> 1. **第三方传输**：您提供的所有 ID、关键词、链接、cookie 等参数都会通过 HTTPS 发送到 **`https://www.aconfig.cn`**（MaxHub 数据服务）进行处理。
> 2. **UGC 隐私**：拉回的 评论 / 转发 / 互动数据 等内容可能包含个人信息或敏感 UGC，请勿写入未授权的数据库或公开发布。
> 3. **凭证保护**：建议使用**独立测试账号**、定期轮换 API Key；**禁止**传入主力生产账号的 cookie 或 session 凭证。
> 4. **合规责任**：使用方需自行确保符合所在地区的数据保护法律（《个人信息保护法》/ GDPR / 微博（Weibo） ToS 等），平台账号的合规性由使用方承担。

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
| 🔒 只读 | 本技能仅用于数据查询和分析，**不执行写入 / 账户 / 发博 / 评论操作** |
| 🚫 禁止臆造路径 | 仅使用 `references/endpoints_whitelist.yaml` 中的端点，**不得自行拼接、改版本号（app/web/web_v2）、加路径段** |
| 🆔 主键不可混用 | App 用 `status_id` / `mid`、Web 用 `post_id` / `mid`、Web V2 用 `id`，**绝不可在端点间复用错误主键名** |
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
STATE_FILE="$COMPLIANCE_DIR/confirmed_weibo-pro.txt"
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
echo "legal_version=1.0.0 confirmed_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$COMPLIANCE_DIR/confirmed_weibo-pro.txt"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"weibo-pro","event":"first_time_confirmation","legal_version":"1.0.0","status":"confirmed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
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
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"weibo-pro","event":"risk_reminder","risk_type":"<matched_category>","legal_version":"1.0.0","status":"confirmed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

4. 用户拒绝或未确认时：停止，不执行后续操作

**0.6 `/legal` 命令处理（用户随时可触发）：**

当用户输入 `/legal`、`查看法律条款` 或 `法律条款` 时：

1. 读取并显示 [DATA_USAGE_POLICY.md](./DATA_USAGE_POLICY.md) 的完整内容
2. 记录审计日志：

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
mkdir -p "$COMPLIANCE_DIR"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"weibo-pro","event":"legal_review","legal_version":"1.0.0","status":"completed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
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
| 查微博详情 / 转发 / 点赞 / 视频 / 推荐 Feed | `references/post.md` | 微博详情、转发、点赞、视频详情、推荐 Feed、频道 Feed、榜单时间线（14 端点） |
| 查用户 / 粉丝 / 关注 / 微博列表 / 收藏 | `references/user.md` | 用户基本/详细信息、粉丝、关注、用户微博、原创、超话、视频、文章、音频、相册、视频合集、分组（22 端点） |
| 搜索 / 热搜 / 榜单 / AI 搜索 | `references/search.md` | 综合搜索、分类搜索、AI 搜索、高级搜索、实时搜索、视频/图片/话题/用户搜索、热搜榜、文娱/社会/生活榜、城市列表（23 端点） |
| 查评论 / 回复 | `references/comments.md` | 微博评论、子评论、评论回复（5 端点） |
| 跨端点参数查询 / 字段流追溯 | `references/param-mappings.md` | 全局红线 + 端点路由 + 字段流字典 + 错误处理总览 |
| 路径白名单硬校验 | `references/endpoints_whitelist.yaml` | 65 个端点的硬白名单 + Pre-call 4 步自检协议 |

**Step 3 — 构建最小调用计划**

- ✅ 优先使用最少端点完成任务，能用一个端点就不用两个
- ✅ 同一意图下三端（App / Web / Web V2）任选其一，**不要同时调用**
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

- 调用前比对 `endpoints_whitelist.yaml` 完成 4 步 Pre-call 自检（路径 → method → 必填 → 主键名）
- 收到 **404** → 必须先做防路径臆造自检（5 步），不要立刻切换三端版本
- 收到 **400 / 422** → 必须先做防参数臆造自检（6 步），重点检查主键命名（`status_id` vs `post_id` vs `id` vs `mid`）
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
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"weibo-pro","event":"api_call","endpoint":"<endpoint_id>","legal_version":"1.0.0","status":"success"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

> R1-R4 为数据处理红线，违反即构成合规风险。R5 为审计要求，每次调用必须记录。

### 高级使用

#### 链式调用图谱（Chain Recipes）

| 用户场景 | 链路 | 字段流 |
|---------|------|-------|
| 查微博 + 评论 + 子评论 | `app_fetch_status_detail` → `app_fetch_status_comments` → `web_v2_fetch_post_sub_comments` | `status_id` → `cid` 接力 |
| 查用户 → 微博列表 | `web_v2_fetch_user_info` → `web_v2_fetch_user_posts` | `uid` 复用 |
| 用户名 → uid（自定义域名） | `web_v2_fetch_user_info`（custom 入参） → 取 `uid` → 后续端点 | `custom` → `uid` |
| 查热搜 → 微博详情 | `web_v2_fetch_hot_search` → `web_v2_fetch_advanced_search` → `web_fetch_post_detail` | 热搜词 → `q` → `post_id` |
| 查用户全面分析 | `app_fetch_user_info_detail` + `web_v2_fetch_user_posts` + `web_v2_fetch_user_following` + `web_v2_fetch_user_fans` | `uid` 复用 |
| 视频合集追踪 | `web_v2_fetch_user_video_collection_list` → `web_v2_fetch_user_video_collection_detail` | `uid` → `cid` |
| 高级人群搜索 | `web_v2_fetch_city_list` → `web_v2_fetch_user_search`（带 region/age/gender） | `city` → query 参数 |

#### 防臆造自检清单（强制前置步骤）

**收到 404 时（A）**：
1. 路径白名单逐字符比对 → 不在清单中 STOP
2. Method 比对（全部为 GET）→ 不等 STOP
3. 三端版本段（`/app/` / `/web/` / `/web_v2/`）比对 → 错段 STOP
4. 资源 ID 来源溯源 → Agent 编造的 STOP
5. 全通过才判定"上游资源不存在"

**收到 400 / 422 时（B）**：
1. 主键名严格比对（`status_id` / `post_id` / `id` / `mid` / `uid` 不可互换）
2. 必填项齐全 + oneOf 二选一逻辑（如 `uid` 与 `custom`）
3. 评论端点 `post_id` 与 `mid` 是否同时携带（web 评论端点要求双主键）
4. 类型与格式严格匹配（pattern / enum）
5. 传参方式正确（query string）
6. 全通过才按 `message_zh` 排查

#### SKILL 版本更新

| 触发条件 | 推荐操作 |
|---------|---------|
| 合法路径持续 404 / 410 | `skillhub upgrade weibo-pro` |
| 用户问"版本是多少" | 当前版本 v4.0.0，访问 https://skillhub.cn/skills/weibo-pro |
| 多端点连续 410 | `skillhub upgrade weibo-pro --force` |
| 401 / 402 / 403 | **不是版本问题**，去 https://www.aconfig.cn 处理 |

### 常用命令速查表

| 场景 | 命令 |
|---|---|
| 查 API Key | `[ -n "${MAXHUB_API_KEY:-}" ] && echo "ok" \|\| echo "missing"` |
| 查微博详情（App） | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/weibo/app/fetch_status_detail?status_id=xxx"` |
| 查微博评论（App） | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/weibo/app/fetch_status_comments?status_id=xxx"` |
| 查用户信息（Web V2） | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/weibo/web_v2/fetch_user_info?uid=xxx"` |
| 查热搜榜 | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/weibo/web_v2/fetch_hot_search"` |
| AI 智能搜索 | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/weibo/web_v2/fetch_ai_search?query=新能源"` |
| 检查 SKILL 更新 | `skillhub info weibo-pro` |


### 📌 端到端使用示例（agent 快速上手）

**用户输入**：「帮我看 微博某条 mid 的评论」

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

### 场景一：品牌方 7×24 舆情监控

- **角色**：品牌公关 / 舆情分析师
- **需求**：实时监控品牌关键词在微博的传播情况，第一时间识别潜在危机话题
- **使用方式**：定时调用 `web_v2_fetch_realtime_search` 取实时词流 → `app_fetch_ai_smart_search` 做语义聚类 → 命中关键词后链式调 `app_fetch_status_detail` + `app_fetch_status_comments` 还原原帖 + 评论
- **预期收益**：实时舆情雷达 + 自动情感聚类，把舆情发现窗口从小时级缩短到分钟级

### 场景二：热搜趋势分析师追踪话题生命周期

- **角色**：内容运营 / 热点编辑
- **需求**：分析当日热搜词的来源、扩散路径、参与 KOL，判断话题是否值得跟进
- **使用方式**：`web_v2_fetch_hot_search` 拉热搜榜 → 取热搜词 → `web_v2_fetch_topic_search` + `web_v2_fetch_advanced_search` 取头部微博 → 链式取 `uid` → `web_v2_fetch_user_info` 补充作者画像
- **预期收益**：完整热搜传播图谱，识别话题首发账号、扩散节点与衰退点

### 场景三：MCN 机构 KOL 影响力分析

- **角色**：MCN / 投放代理
- **需求**：评估候选博主的真实影响力（粉丝活跃度、原创比例、互动健康度）
- **使用方式**：`app_fetch_user_info_detail` 拉详细资料 → `web_v2_fetch_user_original_posts` 拉原创微博 → 抽样 `app_fetch_status_comments` 检测评论真实性 → `web_v2_fetch_user_fans` 抽样粉丝画像
- **预期收益**：完整 KOL 健康度评估，识别水号与真实影响力账号

### 场景四：内容团队微博爆款追踪

- **角色**：自媒体编辑 / 内容策划
- **需求**：追踪某垂类（科技 / 体育 / 娱乐）近 24 小时的爆款微博，提炼标题与开头公式
- **使用方式**：`app_fetch_hot_search`（带 category） → `web_v2_fetch_advanced_search`（timescope=24h） → 取 Top 微博 `mid` → `app_fetch_status_detail` 取全文 → 输出爆款样本集
- **预期收益**：垂类爆款样本库 + 标题/开头公式提炼，提升原创内容 CTR

## 6. 项目架构

### 目录结构

```
maxhub-weibo/
├── SKILL.md                            # Skill 定义与使用文档（本文件）
├── README.md                           # 英文项目说明
├── README_CN.md                        # 中文项目说明
├── _meta.json                          # 版本元信息（version: 4.0.0）
└── references/
    ├── endpoints_whitelist.yaml        # 65 端点路径硬白名单 + Pre-call 4 步自检协议
    ├── param-mappings.md               # 中枢索引（全局红线 + 字段流字典 + 错误处理）
    ├── post.md                         # 微博域：详情/转发/点赞/视频/Feed（App + Web + Web V2，14 端点）
    ├── user.md                         # 用户域：资料/粉丝/关注/微博/原创/超话/视频/文章/音频（22 端点）
    ├── search.md                       # 搜索域：综合/AI/高级/实时/视频/图片/话题/热搜/榜单/城市（23 端点）
    └── comments.md                     # 评论域：评论/子评论/评论回复（App + Web + Web V2，5 端点）
```

### 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 调用方式 | `curl` + Bearer Token | HTTP GET 请求，参数通过 query string 传递 |
| 数据接口 | MaxHub API | `https://www.aconfig.cn/api/v1/weibo/{app\|web\|web_v2}/*`，通过 `MAXHUB_API_KEY` 鉴权 |
| 路径校验 | YAML 硬白名单 | `endpoints_whitelist.yaml` 提供 65 端点的逐字符校验 + 4 步 Pre-call 协议 |
| 错误处理 | 决策表 + 自检清单 | HTTP 状态码权威定义 + 防臆造自检（A/B 双轨）+ 重试策略矩阵 |
| 输出格式 | JSON Standard MaxHub Response | `{code, message, message_zh, data, cache_url}` |
| 更新通道 | SkillHub | ⭐⭐⭐ SkillHub（腾讯云 CDN） |

### API 覆盖范围

| 领域 | 端点数 | Reference 文件 |
|------|--------|---------------|
| 微博内容（Posts） | 14 | `post.md` |
| 用户（Users） | 22 | `user.md` |
| 搜索与发现（Search） | 22 | `search.md` |
| 评论（Comments） | 5 | `comments.md` |
| **合计** | **64（按 4 大领域路由，47 个核心场景端点）** | — |

### 关键设计理念

- **防臆造四道闸**：白名单（endpoints_whitelist.yaml）→ 强标记（Full path）→ 禁止规则（Forbidden）→ 错误反馈（STOP）
- **三端口径共存**：App / Web / Web V2 同一意图存在多端点，**主键命名差异（status_id / post_id / id / mid）必须严格匹配端点要求**
- **Agent 友好 7 大原则**：结构胜于叙述、明确指令优于建议、单一来源、词法稳定性、低 token 密度、边界显式声明、错误处理是契约
- **链式调用图谱**：字段流字典 + Chain Recipes + 跨 reference 链路三层联动，杜绝 Agent 编造字段名
- **错误处理契约**：HTTP 状态码权威定义 + 防臆造自检清单（A: 5 步 / B: 6 步）+ 重试策略矩阵 + 端点替换矩阵
