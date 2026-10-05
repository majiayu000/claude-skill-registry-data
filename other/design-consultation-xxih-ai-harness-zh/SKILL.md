---
name: design-consultation
preamble-tier: 4
version: 1.0.0
description: |
  设计合作伙伴模式。围绕产品上下文、竞品研究、审美方向、设计系统与 mockup，
  从零建立一套可落地的设计方案，并写入 DESIGN.md。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - WebSearch
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /design-consultation

这是 gstack 的设计系统起草器。目标是围绕你的产品实际语境，给出一套能指导后续 `/design-shotgun`、`/design-html`、`/design-review` 的设计基线。

## 核心流程

1. `Pre-checks`：确认项目上下文、浏览器和设计工具是否就绪。
2. `Product Context`：梳理产品目标、受众、约束。
3. `Research`：用户允许时做设计与竞品研究。
4. `Design Outside Voices`：并行引入外部审美声音。
5. `Complete Proposal`：给出完整审美方向、排版、颜色、布局、动效与组件主张。
6. `Drill-downs`：按用户反馈细化。
7. `Design System Preview`：
   - Path A：优先 AI mockups
   - Path B：工具不可用时生成 HTML preview page
8. `Write DESIGN.md & Confirm`

## DESIGN.md 应包含

- Product Context
- Aesthetic Direction
- Typography
- Color
- Spacing
- Layout
- Motion
- Decisions Log
- Design System

## 关键规则

- 设计要和产品定位、商业语气、用户心智绑在一起，而不是做抽象风格板。
- mockup 与 comparison board 是重要决策工具，不只是展示层。
