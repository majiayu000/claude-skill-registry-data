---
name: plan-ceo-review
preamble-tier: 4
version: 1.0.0
description: |
  创始人视角的 mega plan review。重新审视问题与范围，给出 Scope Expansion /
  Selective Expansion / Hold Scope / Scope Reduction 四种模式，并把 scope 变化
  都变成显式用户决策。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
  - WebSearch
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /plan-ceo-review

这是 founder mode。目标不是替计划“盖章”，而是追问：**这个需求背后真正值得做的 10-star product 是什么？**

## 工作模式

用户必须明确选择一种 scope posture：

- `SCOPE EXPANSION`：大胆加，找 Platonic ideal。
- `SELECTIVE EXPANSION`：当前范围为基线，但逐条呈现可选扩展。
- `HOLD SCOPE`：不扩不减，把现有计划打磨到坚固。
- `SCOPE REDUCTION`：像外科手术一样砍到最小可行。

无论哪种模式，所有 scope 变化都必须通过 `AskUserQuestion` 让用户显式确认，绝不静默加减。

## 预审内容

正式 review 前会做：

- system audit：最近提交、当前 diff、stash、TODO / FIXME 热点、历史痛点
- 读取 `CLAUDE.md`、`TODOS.md`、设计文档、旧 handoff note
- landscape check：现有方案、竞品、搜索结果与第一性原理三层综合
- prerequisite offer：如果没有 design doc，优先建议先跑 `/office-hours`

## Step 0：Nuclear Scope Challenge

这一阶段必须完成：

1. `Premise Challenge`：这是不是对的问题？有没有更直接的结果导向？
2. `Existing Code Leverage`：哪些子问题已被现有代码部分解决？
3. `Dream State Mapping`：当前状态 -> 本计划 -> 12 个月理想状态
4. `Implementation Alternatives`：至少 2-3 条显著不同的实现路线，写清 effort、risk、复用关系

## 评审视角

该 skill 会带着 CEO / founder 的思维习惯审视计划：

- 关注是否在解决 proxy problem
- 关注范围是否过宽或过窄
- 关注 6-12 个月后的产品轨迹
- 关注是否错过了更高杠杆、更高品位的方案
- 关注体验、信任、边缘情况是否从一开始就被当成一等公民

## 输出要求

至少应产出：

- `NOT in scope`
- `What already exists`
- `Dream state delta`
- 关键 scope 决策与未决项
- 图示 / 结构图（适用时）
- `TODOS.md` 更新建议
- review log 与 readiness dashboard

## 关键规则

- 只做 plan review，不进入实现。
- 任何 expansion 都必须成为单独的 opt-in 决策。
- 已选模式一旦确定，就要忠实执行，不要中途偷偷漂移成别的模式。
