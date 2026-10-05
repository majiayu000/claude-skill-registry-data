---
name: plan-devex-review
preamble-tier: 3
version: 2.0.0
description: |
  交互式 developer experience 方案评审。先探索开发者 persona、竞品基线、
  magical moment 与 friction points，再进入评分。三种模式：
  DX EXPANSION（做成竞争优势）、DX POLISH（把所有触点打磨到位）、
  DX TRIAGE（只抓致命缺口）。
  当用户要求“DX review”“developer experience audit”“devex review”
  或“API design review”时使用。
  当用户正在规划 developer-facing 产品（API、CLI、SDK、library、platform、docs）时，
  也适合主动建议。 (gstack)
  Voice triggers（语音别名）："dx review"、"developer experience review"、
  "devex review"、"devex audit"、"API design review"、"onboarding review"。
benefits-from: [office-hours]
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
  - WebSearch
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /plan-devex-review

这是 plan 阶段的 developer experience review。重点不是直接打分，而是先把“谁在用、为什么会卡、第一眼 magical moment 是什么”问实。

## 三种模式

- `DX EXPANSION`：把 DX 做成产品优势
- `DX POLISH`：逐触点补强，尽量没有短板
- `DX TRIAGE`：只抓会挡住 adoption 的关键缺口

## Step 0 之前的预审

- 读 plan / diff / README / CLAUDE.md / docs / package manifest / CHANGELOG
- 扫 getting started、CLI help、错误消息、examples 等 DX 资产
- 判断这是不是 developer-facing surface；如果不是，直接 gate 掉

## 交互式前置调查

在正式评分前，要先做完整的 Step 0：

1. `Developer Persona Interrogation`
2. `Empathy Narrative`
3. `Competitive DX Benchmarking`
4. `Magical Moment Design`
5. `Mode Selection`
6. `Developer Journey Trace`
7. `First-Time Developer Roleplay`

这些步骤都要求用 `AskUserQuestion` 停下来收用户反馈，不能一口气跳过。

## 后续评审

- 先做 `DX Trend Check`
- 再跑 8 个 review passes
- 每一维都要引用 Step 0 的证据，而不是脱离 persona 和 benchmark 随便打分

## 关键规则

- `office-hours` 是推荐前置 skill。
- 任何评分都必须能回答：对哪个 persona、在什么场景、被什么摩擦拖慢。
- 不能偷跳 pass。即使某一维没问题，也要明确写 `No issues found`。
