---
slug: douyin-pro
displayName: 抖音数据助手 | 视频 / 直播 / 用户 / 热榜
name: douyin-pro
description: 抖音（Douyin）数据查询与内容分析 skill，通过 MaxHub API 覆盖视频详情/高清链接、评论弹幕、用户主页/作品/粉丝、搜索、热榜、直播、创作者数据、内容指数与星图端点。适合短视频选题、账号画像、竞品分析和趋势监控。所有请求发送到 https://www.aconfig.cn。
license: MIT-0
metadata:
  author: maxhub
  version: 4.1.4
  openclaw:
    capability: read_only_with_write
    requires_confirmation:
    - write
    - non_idempotent
    - cookie_input
    emoji: 🎵
    primaryEnv: MAXHUB_API_KEY
    requires:
      env:
      - MAXHUB_API_KEY
      bins:
      - curl
    env:
    - name: MAXHUB_API_KEY
      description: 抖音（Douyin）数据查询与内容分析 skill，通过 MaxHub API 覆盖视频详情/高清链接、评论弹幕、用户主页/作品/粉丝、搜索、热榜、直播、创作者数据、内容指数与星图端点。适合短视频选题、账号画像、竞品分析和趋势监控。所有请求发送到 https://www.aconfig.cn。
      required: true
      sensitive: true
    network:
    - https://www.aconfig.cn
    riskLevel: medium
    defaultMode: recipes_first_read_only
    skillClass: maxhub-api-skill
    platform: douyin
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
    - douyin
    - 抖音
    - 短视频
    - 视频详情
    - 评论
    - 弹幕
    - 用户画像
    - 搜索
    - 热榜
    - 直播
    - 创作者
    - 内容指数
    - 星图
    - restricted
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

# 抖音 数据助手

## 1. 简介

抖音（Douyin）数据查询与内容分析 skill，通过 MaxHub API 覆盖视频详情/高清链接、评论弹幕、用户主页/作品/粉丝、搜索、热榜、直播、创作者数据、内容指数与星图端点。适合短视频选题、账号画像、竞品分析和趋势监控。所有请求发送到 https://www.aconfig.cn。

## 2. 详细功能

### 视频数据
- 查询抖音视频的完整详情，包含标题、封面、播放、点赞、评论、收藏、分享等核心指标
- 支持通过视频原始 ID、分享链接、短链接、二维码等多种入口快速定位视频
- 获取视频的无水印高清播放地址，便于素材归档与二次研究
- 批量查询多个视频的详情与统计数据，适合大规模选题对比与赛道扫描
- 拉取视频弹幕全量数据，复原视频实时互动氛围
- 浏览首页推荐流与单条视频的相关推荐，洞察平台分发逻辑
- 查询合集、短剧、音乐、话题的详情与对应作品列表
- 浏览知识、游戏、动漫、美食、音乐等垂直频道下的作品聚合

### 用户数据
- 查询抖音用户主页全量信息，包含昵称、签名、头像、地区、认证、粉丝数、获赞数等
- 支持通过抖音号、短 ID、加密 ID、UID 等多种用户标识互相转换与查询
- 批量查询多个用户的资料卡片，适合达人库扩量
- 拉取用户的粉丝列表与关注列表，构建关系图谱
- 拉取用户的发布作品、点赞作品、收藏夹与合辑视频

### 搜索能力
- 执行抖音综合搜索，一次返回视频、用户、话题、直播等混合结果
- 单独执行视频搜索、用户搜索、图片搜索、直播搜索、话题搜索
- 执行音乐搜索、经验搜索、讨论搜索、学校搜索与以图搜视频
- 获取搜索框联想词与话题挑战联想词，辅助关键词扩展

### 评论与弹幕
- 拉取视频一级评论列表，覆盖 App 端与 Web 端多入口
- 接力拉取每条评论下的二级回复，构建完整评论树
- 拉取视频的实时弹幕与历史弹幕全量数据

### 直播数据
- 查询用户直播间详情，包含主播信息、直播标题、封面、状态、在线人数
- 检测用户当前是否在直播以及关联的直播间标识
- 拉取直播间 IM 实时弹幕流与互动数据
- 完成直播间不同标识体系（webcast 标识与房间标识）之间的互转
- 拉取直播间送礼排行榜，识别核心粉丝与高价值用户
- 拉取直播间挂车商品列表、商品规格、优惠券、评价分与评价详情

### 热榜与趋势
- 拉取抖音综合热搜榜、直播热搜榜、音乐热搜榜、品牌热搜榜
- 浏览分类热榜、上升热榜、同城热榜、挑战热榜与总榜
- 查询活动日历的活动列表与单个活动详情
- 拉取热点话题的关联用户画像、评论词云与作品趋势
- 查询热门账号榜、账号粉丝画像、粉丝兴趣账号、粉丝兴趣话题、粉丝兴趣搜索
- 拉取视频总榜、低粉爆款榜、高播放榜、高点赞榜、高涨粉榜
- 查询话题榜、搜索榜、热词榜及其每个条目的详情
- 浏览城市列表与内容标签维度的热点分布

### 创作者后台
- 查询创作者活动列表与单个活动详情，了解平台扶持机会
- 浏览素材中心的素材榜、相关推荐与配置项
- 获取热点榜、热门话题榜、热门道具榜、热门挑战榜、热门音乐榜、热门课程榜
- 拉取行业分类、任务中心商单列表与内容品类信息
- 进行作品流量分析，包括总览、播放来源、搜索关键词、观看趋势
- 进行作品弹幕分析与观众画像，识别真实受众构成
- 拉取作品列表、作品深度分析与可下载报表
- 查询直播间历史回顾与账号诊断报告

### DOU+ 推广数据分析
- 预估 DOU+ 投放成本，按目标受众与作品给出预估消耗、曝光、互动等指标
- 拉取 DOU+ 投放数据概览、明细与趋势图，覆盖账号/视频/直播三类投放维度
- 获取指定用户可推广的作品列表，含点赞、评论量等指标
- 查询当前账号投放过的账号列表，构建投放关系图谱
- 获取 DOU+ POST 请求所需的 sec_token，作为写入类接口的前置步骤
- 浏览 DOU+ 达人分类，按分类搜索合适的达人
- 获取用户主页作品、视频详情（支持 ID 或链接）与 DOU+ 视频排行榜
- 搜索 DOU+ 用户（V1/V2）、视频与直播间，辅助投放选材与受众定位

### 星图 KOL 分析
- 通过抖音用户标识（UID、加密 ID、抖音号）反查星图达人 ID
- 拉取 KOL 基本信息、达人画像、粉丝画像与服务报价
- 查询 KOL 数据概览、转化能力、视频表现、星图指数与触达分布
- 拉取 KOL 关联推广视频、合作品牌、日活粉丝走势
- 拉取 KOL 热门评论高频词与内容关键词，洞察粉丝关注点
- 进行 KOL 搜索与短剧演员搜索，按多维度筛选合适达人
- 浏览星图榜单分类目录与具体榜单数据
- 查询作者营销字段、商业卡片、本地服务信息与作品展示
- 浏览优秀案例分类、达人传播信息与达人推荐
- 查询 IP 活动行业、IP 活动列表、活动详情、资源位列表与需求方 MCN 列表
- 生成达人主页二维码与内容趋势指引

### 抖音指数
- 查询抖音指数关键词的有效日期范围与当前热点
- 拉取热门词、关键词热度趋势与多词解读
- 拉取关键词关联词、人群画像与用户细分词
- 完成抖音指数体系内的用户标识加密
- 进行达人搜索、达人对比、相似达人推荐与达人筛选项查询
- 拉取达人的代表作品、作品里程碑与粉丝画像
- 进行品牌搜索、品牌信息验证、品牌雷达图、品牌走势线、品牌周期分析
- 拉取品牌主动指数周榜与品牌时段热门视频
- 进行话题搜索与话题详情查询
- 拉取创作灵感关键词、关键词作品、选题建议、发布趋势与时长建议
- 拉取作者画像、消费画像、互动趋势与消费趋势
- 搜索趋势研究报告、查看报告详情与智能洞察推荐

### 工具与链接
- 从分享链接、短链中提取视频标识、用户标识、直播间标识
- 生成抖音短链与视频分享二维码
- 唤起抖音 App 直跳视频、用户主页与关键词搜索
- 通过分享码反查分享内容信息

### 账号余额查询
- 查询 MaxHub API 账号剩余额度，支持 `x-api-key` 或 `Authorization: Bearer` 两种认证方式
- 频率限制：最快每 3 秒调用一次
- 接口路径：`GET /api/maxhub/balance`

## ⚖️ 法律免责与合规声明

> **使用本 skill 即表示您确认已阅读并同意以下条款：**
>
> 1. **数据来源**：本 skill 通过第三方数据服务（MaxHub API）获取 抖音（Douyin） 数据，该服务**未获得 抖音（Douyin） 官方授权**。本项目对数据获取的合法性不作任何保证。
> 2. **合规责任**：使用方需**自行确保**符合所在地区的数据保护法律（《个人信息保护法》/ GDPR / CCPA 等）及 抖音（Douyin） 服务条款（ToS）。因使用本 skill 产生的任何法律后果由使用方自行承担。
> 3. **禁止用途**：严禁将本 skill 用于违反法律的行为，包括但不限于：侵犯个人信息权、不正当竞争、刷量操控、批量爬取用户数据等。
> 4. **平台风险**：抖音可能对未授权数据访问采取封号、诉讼等法律行动。
> 5. **完整政策**：详细数据使用政策请参阅 [DATA_USAGE_POLICY.md](./DATA_USAGE_POLICY.md)。

> ### 📋 数据传输与隐私声明（请认真阅读）
>
> 1. **第三方传输**：您提供的所有 ID、关键词、链接、cookie 等参数都会通过 HTTPS 发送到 **`https://www.aconfig.cn`**（MaxHub 数据服务）进行处理。
> 2. **UGC 隐私**：拉回的 评论 / 弹幕 / 动态 等内容可能包含个人信息或敏感 UGC，请勿写入未授权的数据库或公开发布。
> 3. **凭证保护**：建议使用**独立测试账号**、定期轮换 API Key；**禁止**传入主力生产账号的 cookie 或 session 凭证。
> 4. **合规责任**：使用方需自行确保符合所在地区的数据保护法律（《个人信息保护法》/ GDPR / 抖音（Douyin） ToS 等），平台账号的合规性由使用方承担。

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

---

> 🔒🔒🔒 **HARD GATE — 以下 0️⃣ 步骤为绝对前置，不可跳过、不可绕过、不可延后** 🔒🔒🔒
>
> **0️⃣ 合规闸门（ALL 请求 · ALL 端点 · ALL risk 等级 · 不可跳过）**
>
> | 子步骤 | 内容 | 未通过后果 |
> |--------|------|-----------|
> | 0.A 首次确认 | 检查 `$HOME/.maxhub-skills/.compliance/confirmed_douyin-pro.txt`，不存在或版本过期则显示合规闸门并等待用户输入"同意" | **立即停止**，不执行 1️⃣ 及后续任何步骤 |
> | 0.B 风险检测 | 对照 risk_rules.yaml 核心风险规则（cookie_usage / batch_operation / personal_data / write_operation），命中则显示定向提醒并等待用户确认 | **立即停止**，不执行 1️⃣ 及后续任何步骤 |
>
> ⛔ **即使 risk:low 端点也必须先通过 0️⃣**。0️⃣ 与下文 4️⃣ Pre-call 自检是两道独立闸门，不可互相替代。
>
> 🔒🔒🔒 **GATE END — 0️⃣ 未通过则禁止进入以下所有步骤** 🔒🔒🔒

---

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

> ⛔ **全局前置规则（适用于 ALL risk 等级，包括 `risk: low`）**：
> 进入本表之前，**必须已通过 0️⃣ 合规闸门**（首次确认 0.A + 风险检测 0.B）。
> 本表的自检是 0️⃣ 之后的**第二道**技术性校验，不能替代 0️⃣。若 0️⃣ 未通过，本表自检结果无效。

| 端点 risk | 0️⃣ 合规闸门 | 必做技术自检 | 步骤数 |
|----------|-------------|------------|-------|
| `risk: low` | ✅ 必须通过 | ① 路径在 endpoints_whitelist.yaml | 1 步 |
| `risk: medium` | ✅ 必须通过 | ① 路径 ② method ③ 必填参数 ④ 写入确认 | 4 步 |
| `risk: high` | ✅ 必须通过 | 4 步 + 显式向用户确认参数与意图 | 5 步 |
| `risk: critical`（restricted） | ✅ 必须通过 | 6 步高风险确认流程（详见 §高风险能力清单） | 6 步 |

> 旧 SKILL 强制所有调用都做 4 步——现按 risk 等级简化技术自检。但 **0️⃣ 合规闸门不简化**，`low` 端点也必须先过合规闸门，仅技术校验步骤减为 1 步。

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
| 🔒 只读 | 本技能仅用于数据查询和分析，**不执行写入 / 账户 / 发布操作** |
| 🚫 禁止臆造路径 | 仅使用 `references/endpoints_whitelist.yaml` 中的端点，**不得自行拼接、改版本号、加路径段** |
| 📋 数据流向第三方 | 所有请求发送至 `https://www.aconfig.cn`，请使用独立测试账号并定期轮换 API Key |
| 🔑 凭证保护 | 不暴露 API Key、Cookie、Token 至日志或对话 |
| ⚠️ 高风险端点确认 | `fetch_multi_video` 等批量 / 写入端点须用户明确确认参数后才能调用 |

### 基础使用（5 步完成调用）

**Step 0 — 合规硬前置检查（不可跳过 · 不可绕过）**

> ⛔ 本步骤为**硬前置**：未通过则禁止执行 Step 1 及后续任何 API 调用。
> 本步骤**自包含**，不依赖任何外部文件即可完成基础合规检查。详细框架可参阅 [COMPLIANCE_GATE.md](./COMPLIANCE_GATE.md)，完整风险规则见 [risk_rules.yaml](./risk_rules.yaml)。

**0.0 缺失即停检查：**

检查合规确认状态文件是否存在。**若不存在，立即停止**后续操作，直接进入 0.2 首次闸门流程。

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
STATE_FILE="$COMPLIANCE_DIR/confirmed_douyin-pro.txt"
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
echo "legal_version=1.0.0 confirmed_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$COMPLIANCE_DIR/confirmed_douyin-pro.txt"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"douyin-pro","event":"first_time_confirmation","legal_version":"1.0.0","status":"confirmed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
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
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"douyin-pro","event":"risk_reminder","risk_type":"<matched_category>","legal_version":"1.0.0","status":"confirmed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

4. 用户拒绝或未确认时：停止，不执行后续操作

**0.6 `/legal` 命令处理（用户随时可触发）：**

当用户输入 `/legal`、`查看法律条款` 或 `法律条款` 时：

1. 读取并显示 [DATA_USAGE_POLICY.md](./DATA_USAGE_POLICY.md) 的完整内容
2. 记录审计日志：

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
mkdir -p "$COMPLIANCE_DIR"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"douyin-pro","event":"legal_review","legal_version":"1.0.0","status":"completed"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
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
| 查视频详情 / 播放 / 下载 / 统计 | `references/video.md` | 视频详情、批量视频、播放 URL、统计、合集 / 短剧、音乐 / 话题、分享 / 短链 / 二维码、频道内容、ID 提取（42 端点） |
| 查用户 / 粉丝 / 作品 / 喜欢 | `references/user.md` | 用户信息、粉丝 / 关注、作品、喜欢、收藏夹、合辑、用户搜索、开播信息（24 端点） |
| 搜索视频 / 用户 / 图片 / 直播 | `references/search.md` | 综合 / 视频 / 用户 / 图片 / 直播 / 话题 / 经验 / 音乐 / 讨论 / 学校 / 图像搜索 + 建议（19 端点） |
| 查热搜 / 热榜 / 活动日历 | `references/trending.md` | 热榜分类、上升 / 同城 / 挑战热点、活动日历、粉丝画像、账号 / 视频 / 话题 / 搜索热榜、首页推荐（39 端点） |
| 查创作者数据 / 作品分析 | `references/creator.md` | 创作者活动、素材中心、热门榜单、商单任务、行业分类、流量分析、观众画像、账号诊断、直播历史（31 端点） |
| 查星图 KOL / 达人分析 | `references/xingtu.md` | KOL ID 查询、基本信息、画像、报价、数据概览、KOL 搜索、转化分析、星图指数、视频表现、热榜、达人广场、MCN、IP 日历（43 端点） |
| 查评论 / 回复 / 弹幕 | `references/comments.md` | 视频评论、评论回复、视频弹幕（6 端点） |
| 查抖音指数 / 品牌 / 达人 | `references/content.md` | 关键词趋势、关联词、人群画像、达人分析、视频搜索、品牌指数、话题搜索、创作指南、趋势报告（44 端点） |
| 查直播 / 直播间 / 商品 | `references/live.md` | 直播流、弹幕、送礼排行、直播间商品、商品详情 / 评价、直播间 ID 转换（14 端点） |
| 工具与链接 | `references/tools.md` | 短链生成、分享二维码、App 跳转、分享码反查、ID 提取（5 端点） |
| 查 DOU+ 推广 / 投放分析 | `references/douplus.md` | DOU+ 成本预估、投放概览/明细/趋势图、可推广作品、投放账号、sec_token、达人分类/搜索、用户作品、视频详情、视频排行榜、用户/直播/视频搜索（16 端点） |
| 跨端点参数查询 / 字段流追溯 | `references/param-mappings.md` | 全局红线 + 端点路由 + 字段流字典 + 错误处理总览 + 替换矩阵 |
| 路径白名单硬校验 | `references/endpoints_whitelist.yaml` | 290 个端点的硬白名单 + Pre-call 4 步自检协议 |
| SKILL 版本检查与升级 | `references/update.md` | SkillHub 更新 |

**Step 3 — 构建最小调用计划**

- ✅ 优先使用最少端点完成任务，能用一个端点就不用两个
- ✅ 高风险端点（批量 / 写入）调用前**必须**让用户确认参数
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

**Step 4 - 执行并验证**

- 调用前比对 `endpoints_whitelist.yaml` 完成 4 步 Pre-call 自检（路径 -> method -> 必填 -> 写入确认）
- 收到 **404** -> 必须先做 §3.1 (A) 防路径臆造自检（5 步）
- 收到 **400 / 422** -> 必须先做 §3.1 (B) 防参数臆造自检（6 步）
- 收到 **业务 code != 0** -> 读 `message_zh` 报告用户，**不重试**

**📝 审计日志（调用成功后必须立即执行 · 非可选 · 非软要求）：**

> 以下命令与 API 调用是**原子绑定**关系。每次成功调用后必须执行，不得跳过、不得延后、不得批量补录。

```bash
COMPLIANCE_DIR="$HOME/.maxhub-skills/.compliance"
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"douyin-pro","event":"api_call","endpoint":"<endpoint_id>","legal_version":"1.0.0","status":"success"}' >> "$COMPLIANCE_DIR/audit_log.jsonl"
```

> ⚠️ Agent 自检：若本次会话中执行了 API 调用但未执行上述审计日志命令，视为**合规违规**，必须补录。


**📦 返回数据合规检查（收到响应后必须执行）：**

| # | 检查项 | 处理方式 |
|---|--------|---------|
| R1 | 个人信息脱敏 | 响应包含手机号/邮箱/身份证等 PII 时，仅展示必要字段，其余脱敏 |
| R2 | UGC 内容处理 | 响应包含评论/弹幕/动态等 UGC 时，提醒用户不用于未授权商业用途 |
| R3 | 隐私数据保护 | 响应包含他人联系方式/位置/社交关系时，不写入持久化存储 |
| R4 | 数据量控制 | 响应数据量 >100 条时，提醒用户遵循最小必要原则，建议分页 |

> R1-R4 为数据处理红线，违反即构成合规风险。R5（审计日志）已上移至 Step 4 执行流程中，为**硬绑定**步骤。

### 高级使用

#### 链式调用图谱（Chain Recipes）

| 用户场景 | 链路 | 字段流 |
|---------|------|-------|
| 查视频 + 评论 | `video.md` → `comments.md` | `aweme_id` 接力 |
| 搜索 → 视频详情 | `search.md` → `video.md` | `aweme_id` 接力 |
| 查用户 → 作品 | `user.md` → `user.md` (posts) | `sec_user_id` 接力 |
| 查创作者 → 视频详情 | `creator.md` → `video.md` | `item_id` → `aweme_id` |
| 查用户 → 星图 KOL | `user.md` → `xingtu.md` | `uid` / `sec_user_id` → `kolid` |
| 查热搜 → 视频详情 | `trending.md` → `video.md` | `aweme_id` 接力 |
| 查直播 → 观众画像 | `live.md` → `creator.md` (audience_portrait) | `room_id` 接力 |
| 查品牌趋势 → 人群画像 | `content.md` → `content.md` (portrait) | `keyword` 接力 |
| 用户全面分析 | `user.md` → `user.md` (stats+posts+likes) → `xingtu.md` | `sec_user_id` 复用 |

#### 防臆造自检清单（强制前置步骤）

**收到 404 时（A）**：
1. 路径白名单逐字符比对 → 不在清单中 STOP
2. Method 比对 → 不等 STOP
3. 参数键名比对 → 有清单外参数 STOP
4. 资源 ID 来源溯源 → Agent 编造的 STOP
5. 全通过才判定 "上游资源不存在"

**收到 400 / 422 时（B）**：
1. 参数名严格比对（大小写 / 缩写 / 复数）
2. 必填项齐全 + oneOf 二选一逻辑
3. 类型与格式严格匹配（pattern / enum）
4. 传参方式正确（query vs body）
5. 没有 IN 表外的臆造参数
6. 全通过才按 `message_zh` 排查

#### SKILL 版本更新

| 触发条件 | 推荐操作 |
|---------|---------|
| 合法路径持续 404 / 410 | `skillhub upgrade douyin-pro` |
| 用户问 "版本是多少" | 当前版本 v4.0.0，访问 https://skillhub.cn/skills/douyin-pro |
| 多端点连续 410 | `skillhub upgrade douyin-pro --force` |
| 401 / 402 / 403 | **不是版本问题**，去 https://www.aconfig.cn 处理 |

### 常用命令速查表

| 场景 | 命令 |
|---|---|
| 查 API Key | `[ -n "${MAXHUB_API_KEY:-}" ] && echo "ok" \|\| echo "missing"` |
| 查视频详情 | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/douyin/app/v3/fetch_one_video?aweme_id=xxx"` |
| 查视频评论 | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/douyin/app/v3/fetch_video_comments?aweme_id=xxx"` |
| 分享 URL 解析 | `curl -H "$maxhub_auth_header" "https://www.aconfig.cn/api/v1/douyin/app/v3/fetch_one_video_by_share_url?share_url=xxx"` |
| 检查 SKILL 更新 | `skillhub info douyin-pro` |


### 📌 端到端使用示例（agent 快速上手）

**用户输入**：「帮我看 这个抖音 aweme_id 视频的评论」

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

### 场景一：抖音内容创作者寻找选题

- **角色**：抖音短视频创作者
- **需求**：想分析近期同赛道热门视频共性，寻找下一个选题方向
- **使用方式**：调用 `trending.md` 拉取分类热榜与上升榜 → 取 `aweme_id` → 链式调 `video.md` 提取标题、话题、音乐 → 调 `comments.md` 抓取评论关键词
- **预期收益**：通过热榜 + 详情 + 评论三层链路快速锁定高互动作品共同特征，沉淀可复用的选题模板与音乐库

### 场景二：新媒体团队竞品分析

- **角色**：MCN / 品牌新媒体运营
- **需求**：监控竞品账号的作品节奏、粉丝增长与互动表现
- **使用方式**：`user.md` 取 `sec_user_id` → 拉取作品列表 + 粉丝统计 → `creator.md` 调用流量分析与观众画像 → `comments.md` 抽样评论
- **预期收益**：构建竞品账号画像数据库，量化对比内容策略与受众重合度

### 场景三：星图 KOL 投放分析

- **角色**：品牌投放 / 广告优化师
- **需求**：在投放前评估 KOL 真实粉丝画像、报价合理性与历史转化数据
- **使用方式**：`user.md` 反查 `uid` → `xingtu.md` 用 KOL ID 查询基本信息 + 服务报价 + 转化分析 + 视频表现 + 星图指数
- **预期收益**：投放前完成 KOL 健康度筛查，降低无效投放，提升 ROI 决策准确度

### 场景四：直播数据采集与商品分析

- **角色**：直播电商运营 / 数据分析师
- **需求**：实时监控直播间互动、礼物排行与挂车商品转化
- **使用方式**：`live.md` 取 `room_id` → 拉取弹幕 + 送礼排行 + 直播商品 → `live.md` 商品详情 / 评价 → `creator.md` 观众画像
- **预期收益**：构建直播间秒级监控面板，识别高转化商品组合与观众分层特征

## 6. 项目架构

### 目录结构

```
maxhub-douyin/
├── SKILL.md                            # Skill 定义与使用文档（本文件）
├── README.md                           # 英文项目说明
├── README_CN.md                        # 中文项目说明
├── _meta.json                          # 版本元信息（version: 4.0.0）
└── references/
    ├── endpoints_whitelist.yaml        # 290 端点路径硬白名单 + Pre-call 4 步自检协议
    ├── param-mappings.md               # 中枢索引（全局红线 + 字段流字典 + 错误处理 + 替换矩阵）
    ├── video.md                        # 视频域：详情/播放/下载/统计/合集/音乐/话题（42 端点）
    ├── user.md                         # 用户域：资料/粉丝/作品/喜欢/收藏夹/合辑/搜索（24 端点）
    ├── search.md                       # 搜索域：综合/视频/用户/图片/直播/话题/经验等（19 端点）
    ├── trending.md                     # 热榜域：分类/上升/同城/挑战/活动/账号/话题（39 端点）
    ├── creator.md                      # 创作者域：素材/商单/流量/画像/账号诊断（31 端点）
    ├── xingtu.md                       # 星图域：KOL/画像/报价/转化/指数/MCN/IP 日历（43 端点）
    ├── comments.md                     # 评论域：评论/回复/弹幕（6 端点）
    ├── content.md                      # 抖音指数域：关键词/品牌/人群/趋势报告（44 端点）
    ├── live.md                         # 直播域：直播流/弹幕/礼物/商品/转换（14 端点）
    ├── tools.md                        # 工具域：短链/二维码/App跳转/ID提取（5 端点）
    ├── douplus.md                      # DOU+ 推广域：成本预估/投放分析/达人搜索/视频搜索（16 端点）
    └── update.md                       # SKILL 更新机制（SkillHub）
```

### 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 调用方式 | `curl` + Bearer Token | HTTP GET / POST 请求，参数通过 query string 或 JSON body 传递 |
| 数据接口 | MaxHub API | `https://www.aconfig.cn/api/v1/douyin/*`，通过 `MAXHUB_API_KEY` 鉴权 |
| 路径校验 | YAML 硬白名单 | `endpoints_whitelist.yaml` 提供 290 端点的逐字符校验 + 4 步 Pre-call 协议 |
| 错误处理 | 决策表 + 自检清单 | HTTP 状态码权威定义 + 防臆造自检（A/B 双轨）+ 重试策略矩阵 |
| 输出格式 | JSON Standard MaxHub Response | `{code, message, message_zh, data, cache_url}` |
| 更新通道 | SkillHub | ⭐⭐⭐ SkillHub（腾讯云 CDN） |

### API 覆盖范围

| 领域 | 端点数 | Reference 文件 |
|------|--------|---------------|
| 视频（Video） | 42 | `video.md` |
| 用户（User） | 24 | `user.md` |
| 搜索（Search） | 19 | `search.md` |
| 热榜（Trending） | 39 | `trending.md` |
| 创作者（Creator） | 31 | `creator.md` |
| 星图（Xingtu） | 43 | `xingtu.md` |
| 评论（Comments） | 6 | `comments.md` |
| 抖音指数（Content） | 44 | `content.md` |
| 直播（Live） | 14 | `live.md` |
| 工具（Tools） | 13 | `tools.md` |
| DOU+ 推广（Douplus） | 16 | `douplus.md` |
| **合计** | **290** | — |

### 关键设计理念

- **防臆造四道闸**：白名单（endpoints_whitelist.yaml）→ 强标记（Full path）→ 禁止规则（Forbidden）→ 错误反馈（STOP）
- **Agent 友好 7 大原则**：结构胜于叙述、明确指令优于建议、单一来源、词法稳定性、低 token 密度、边界显式声明、错误处理是契约
- **链式调用图谱**：字段流字典 + Chain Recipes + 跨 reference 链路三层联动，杜绝 Agent 编造字段名
- **错误处理契约**：HTTP 状态码权威定义 + §3.1 防臆造自检清单（A: 5 步 / B: 6 步）+ 重试策略矩阵 + 端点替换矩阵
