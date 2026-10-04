---
name: ompm
description: 'Oh-My-PM 全系统前门与全局意图路由：理解用户想做什么，路由到最合适的 skill 或 workflow 并一句话说明理由。当用户提出产品管理相关需求但不确定该用哪个能力时使用；也覆盖广义入口请求，如"产品经理工作入口"、"下一步该做什么"、"帮我规划产品工作"、"我要写 PRD"、"分析竞品"、"复盘"等。 Also triggers on: PM work entry point, what should I do next, help me plan product work, route my PM request.'
layer: workflow
input-from: user
output-to: clarify-requirements,competitive-analysis,market-research,product-strategy,prd-gen,prototype-design,feedback-synthesis,retrospective,quick-prd,full-pm-cycle,feature-launch
---

# OMPM 意图路由（全局前门）

Oh-My-PM 的全局入口：理解你想做什么，路由到最合适的 skill 或 workflow。

本 skill 是意图路由逻辑的唯一权威；Claude Code 的 `/ompm` 命令（`commands/ompm.md`）只是激活本 skill 的 shim。

## 路由判定

按以下优先级处理输入：**help → workflow 直派 → 新手引导 → 模式 B 任务后导航 → 意图路由（一般规则）→ 空对话引导**。

### 1. Help Detection

**如果输入是 `help` 或 `?`，输出下方「能力图」，然后结束。**

### 2. Workflow 直派（兼容用法）

如果输入的第一个词是 workflow 名（`quick-prd` / `full-pm-cycle` / `feature-launch`），将剩余内容原样传给该 workflow 执行。

| 用法 | 示例 |
|:-----|:-----|
| `quick-prd "功能描述" [竞品...]` | `ompm quick-prd "用户改版" 淘宝 京东` |
| `full-pm-cycle "产品名" [type]` | `ompm full-pm-cycle "新项目管理工具"` |
| `feature-launch "功能名" [日期]` | `ompm feature-launch "注册流程" 2026-05-01` |

在 Claude Code 中以上用法对应 `/ompm <workflow> ...`；直接命令（不带 `/ompm` 前缀）等效：`/quick-prd`、`/full-pm-cycle`、`/feature-launch`。

### 3. 新手引导（首次使用）

**判定**：输入为"新手"、"新手入门"、"第一次用"、"guide"、"教程"等引导类请求；或无输入参数，且 `docs/product/` 下完全无任何产物（首次使用的信号）→ 进入新手引导。

**教程话术**（输出后紧接实战，不要只发说明）：

> **我能交付什么**
> - 竞品与市场研究——摸清对手在做什么、市场往哪走
> - 策略三件套——定位 → 优先级 → 路线图
> - PRD——把需求落成可评审的文档
> - HTML 原型——可交互的设计验证
> - 发布准备——从 PRD 到上线的检查与协调
> - 复盘——上线效果分析，排出下轮迭代计划
>
> **我怎么工作**：你描述处境 → 我选当前最合适的一个能力直接开始做 → 你补充反馈 → 我判断下一步。每次只决定当前一步，你不需要规划全程。
>
> **怎么开始**：直接说说你正在做的产品、功能，或者卡住的地方——说得乱也可以，我来整理。

**教程后接续**：用户描述处境后，按下方「意图路由」的规则立即路由执行，不让用户重新输入；任务完成后，用一句话告诉用户刚才使用了哪个能力，例如"刚才帮你完成的是竞品分析"。

**硬性规则**：
- 已在对话中出现的信息不重复提问
- 不要求用户记住任何命令——教程之后全程自然语言
- 教程用任务语言表达，不展示完整 skill 目录（完整清单只在 `help` 时输出）

### 4. 意图路由（无参或自然语言输入）

无输入、或输入是一段自然语言需求描述时，执行意图路由：

**Step 1 — 读取上下文**：
- 当前对话上下文（用户刚才在讨论什么、已经做过什么）
- `docs/product/.ompm/current-workflow.json`（如存在）— 进行中工作流的阶段与状态
- `docs/product/` 下已有产物（PRD、定位、竞品分析、发布计划等，确认存在性即可）

**Step 2 — 判断"当前最有价值的下一步"**：
- 有进行中的工作流 → 继续该工作流的下一阶段（按 `current_stage` 推断）
- 需求描述模糊、关键信息缺失 → 先 `clarify-requirements`
- 已有竞品/市场研究但无策略 → `product-strategy`
- 已有 PRD 但尚未发布 → `feature-launch`
- 明确要 PRD → 要竞品上下文用 `quick-prd`，直接写用 `prd-gen`
- 上线后话题（数据、反馈、下一步做什么） → `retrospective` / `feedback-synthesis`
- 都不匹配 → 按下方能力图给出 2-3 个候选，让用户选择

**Step 3 — 路由并用一句话说明理由**，然后激活对应 skill / workflow。例如：

> 你已有竞品分析和定位文档，但还没有 PRD —— 最有价值的下一步是生成 PRD，启动 `quick-prd`。

### 模式 B：任务后导航

**判定**：当前对话中已有任何 skill 的产出（竞品报告、PRD、复盘结论等）→ 进入任务后导航。

**优先级**：模式 B 先于「意图路由 Step 2 的一般规则」执行——有产出按下方导航地图续接，无产出才按一般规则判断。

**导航地图**：

| 来源 skill | 结论信号 | 下一步 | 理由 |
|:-----------|:---------|:-------|:-----|
| clarify-requirements | 方案已批准 | `prd-gen` | 信息已齐，直接生成 |
| clarify-requirements | 发现缺市场/竞品数据 | `market-research` / `competitive-analysis` | 先补齐感知层数据，再回来生成 |
| competitive-analysis | 找到差异化机会 | `product-strategy` | 机会转定位 |
| competitive-analysis | 要落成具体需求 | `prd-gen` | 对比结论直接转功能需求 |
| market-research | 市场/用户结论已出 | `product-strategy` | 结论转定位与优先级 |
| product-strategy | 定位/优先级/路线图完成 | `prd-gen` | 策略落 PRD |
| prd-gen | PRD 已定稿 | `prototype-design` 或 `feature-launch` | 先验证交互，或直接准备发布 |
| prototype-design | 原型已验证 | `feature-launch` | 进入发布准备 |
| feedback-synthesis | 主题已聚类 | `retrospective` | 与上线指标对照复盘 |
| retrospective | 迭代计划已出 | `market-research` 或 `prd-gen` | 下一轮：验证新方向，或写新需求 |

**路由话术**统一为：

> 刚才 {skill} 的核心结果是 {X}——下一步先用 **{skill}**，因为 {理由}。

随后立即执行对应 skill，不让用户重新输入。

### 空对话引导

**判定**：无输入参数，且对话中也没有可用于判断的信息（无产出、无进行中工作流、无明确话题；`docs/product/` 下完全无产物的首次使用场景已由上方「新手引导」接管）→ 输出下方固定引导话术，然后等待，不罗列完整菜单：

> 把你现在想处理的事情直接发过来——可以是一个需求、一段材料、一个想法，信息不完整也可以。想看全部能力，输入 `help`。

### 边界情况

- 用户同时提多个需求 → 问"先解决哪个？一个一个来。"
- 需求超出能力图范围 → 明示能力清单，不编造能力
- 上下文足以判断 → 直接路由，不重复索取用户已提供的信息

---

## 能力图（Help 输出）

按你的目标选择入口；skill 均支持自然语言直接触发（如"帮我分析竞品"）。

### 我要写 PRD

| 场景 | 入口 |
|:-----|:-----|
| 快速 PRD + 竞品对比 | `quick-prd "功能描述" [竞品...]` |
| 直接生成 PRD（上下文已齐） | `prd-gen` skill |
| 需求还说不清，先梳理 | `clarify-requirements` skill |

### 我要了解竞品 / 市场 / 用户

| 场景 | 入口 |
|:-----|:-----|
| 竞品功能对比、差异化机会 | `competitive-analysis` skill |
| 市场趋势、行业报告、用户研究 | `market-research` skill |

### 我要定策略

| 场景 | 入口 |
|:-----|:-----|
| 定位、价值主张、优先级、路线图 | `product-strategy` skill |

### 我要做原型

| 场景 | 入口 |
|:-----|:-----|
| HTML 交互原型验证设计 | `prototype-design` skill |

### 我要规划 0-1 产品

| 场景 | 入口 |
|:-----|:-----|
| 完整 PM 周期（研究→策略→PRD→发布→复盘） | `full-pm-cycle "产品名"` |

### 我要发版

| 场景 | 入口 |
|:-----|:-----|
| 发布物料（灰度/回滚/监控/checklist）+ 可选全流程编排 | `feature-launch "功能名"` |

### 我要复盘

| 场景 | 入口 |
|:-----|:-----|
| 上线效果分析 + 下轮迭代计划 | `retrospective` skill |
| 汇总多渠道用户反馈 | `feedback-synthesis` skill |
