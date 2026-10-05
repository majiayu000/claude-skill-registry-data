---
name: plan-design-review
preamble-tier: 4
version: 1.0.0
description: |
  设计师视角的 plan review。对信息架构、交互状态、情绪弧线、AI slop 风险、
  设计系统一致性、响应式与可访问性做 0-10 打分，并在需要时生成或更新 mockup。 (gstack)
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

# /plan-design-review

这是设计师视角的 plan review。目标不是问“好不好看”，而是判断这份计划是否足以做出可信、清晰、有辨识度的真实产品体验。

## 预备阶段

- 做 design-scope assessment，确认这份计划是否真的涉及 UI / UX。
- 检查 `DESIGN.md` 是否存在，已有设计系统能否复用。
- 如果设计环境可用，默认优先生成或更新视觉 mockup，帮助后续 review 更具体。

## 评分方法

每个关键设计维度都按 `0-10` 评分，并解释：

- 当前为什么不是 10
- 10/10 会长什么样
- 提高到更高分需要补哪些内容

## 七个 review pass

1. `Information Architecture`
2. `Interaction State Coverage`
3. `User Journey & Emotional Arc`
4. `AI Slop Risk`
5. `Design System Alignment`
6. `Responsive & Accessibility`
7. `Unresolved Design Decisions`

## 关键产物

- `NOT in scope`
- `What already exists`
- `TODOS.md` 更新
- 完成总结
- 未决设计决策
- 已批准 mockups（如果生成了）
- review log 与 readiness dashboard

## 关键规则

- 有 UI scope 时，mockup 与 comparison board 是默认工具，不是可有可无的装饰。
- 对“AI 味很重、缺乏 hierarchy、信任感不足”的风险要直接点名。
- 这是 plan review，不写业务代码。
