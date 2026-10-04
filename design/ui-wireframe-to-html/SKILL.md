---
name: ui-wireframe-to-html
description: >
  PRD 到 UI 线框 / 结构阶段：当需要把 PRD 的界面定义先转成 screen inventory、状态模型、ASCII 布局、低保真 HTML mockup，
  并先确认结构/状态而不是视觉 polish 时使用。这个 Skill 只负责 UI mockup 的结构阶段；如果用户要高保真、真实前端项目对齐、
  project-native preview、component map、implementation notes 或“开发完全复刻”，必须转用 ui-mockup-desktop-workbench。
---

# ui-wireframe-to-html

## 中文速查

- 中文名：PRD 到 UI 线框 / 结构阶段
- 英文稳定名：`ui-wireframe-to-html`
- 分类：产品与 PRD
- 你可以这样叫我：`把 PRD 变成线框`、`先出 UI 结构`、`先做 ASCII 布局`、`只确认页面结构和状态`、`生成低保真 HTML wireframe`
- 适合：从 PRD 界面定义输出 screen inventory、状态模型、ASCII layout 和低保真 HTML mockup，先明确结构和状态再决定是否进入高保真。
- 不适合：直接做高保真视觉；让前端复刻 UI；对齐真实项目组件、token、icon；输出 component map 或 implementation notes。这些场景用 `ui-mockup-desktop-workbench`。

## Relationship To `ui-mockup-desktop-workbench`

This Skill is the structure-only stage of the broader UI mockup workflow.

Use this Skill when the user explicitly wants to stop at structure, wireframe, information architecture, state model, or low-fidelity HTML.

Use `ui-mockup-desktop-workbench` instead when the user wants:

- high-fidelity visual handoff
- real frontend project alignment
- project-native preview route/component
- production component mapping
- implementation notes
- screenshots for final UI approval
- "开发完全复刻这个 UI"

The normal staged path is:

`PRD -> ui-wireframe-to-html -> structure confirmation -> ui-mockup-desktop-workbench -> visual handoff / preview -> implementation`

When `ui-mockup-desktop-workbench` is already active, do not call this Skill separately. The main Skill includes this structure stage internally.

## Overview

将 PRD 中的界面定义逐步推进为：

1. Screen inventory
2. State model
3. ASCII layout
4. Optional low-fidelity HTML wireframe

The purpose is to make the page structure, state coverage, and interaction skeleton reviewable before anyone spends effort on visual polish.

## Context Intake

优先确认或读取：

- 关联 PRD、页面需求、草稿或 UI 目标。
- 当前页面在全链路中的位置。
- 目标屏幕范围：主页面、列表、详情、弹窗、设置、异常状态等。
- 已有结构定义、流程图、状态说明或截图。
- 是否存在 `docs/templates-local/` 下的 UI override。
- 用户是否明确要求只做结构阶段，还是最终要进入高保真。

If the user provides enough PRD context, proceed with assumptions instead of asking broad questions. Ask only when the missing answer changes page scope or state coverage.

## Responsibilities

这个 Skill 负责：

1. 读取关联 PRD 和当前模块定位。
2. 明确页面在全链路中的位置。
3. 提取 screen inventory。
4. 补齐关键状态模型。
5. 输出 ASCII 结构图。
6. 需要时生成低保真 HTML mockup。
7. 列出进入高保真前必须确认的问题。

它不负责：

- 跳过结构层直接出视觉稿。
- 脱离 PRD 自行发明新交互。
- 用 HTML mockup 替代 UI 结构说明。
- 声称低保真 HTML 可直接复用为生产前端。
- 输出高保真视觉、project-native preview、component map 或 implementation notes。

## Workflow

1. **Read PRD and scope**
   - Identify the product goal, target users, workflow stage, and page boundaries.
   - If the PRD is missing core goals or workflow, route to `prd-architect`.
   - If the PRD has conflicts or cannot support a screen model, route to `prd-review`.

2. **Build screen inventory**
   - List pages, panels, modals, popovers, drawers, and persistent shell areas.
   - Mark each item as required, optional, or assumption.
   - Trace each screen to PRD text, UI goal, screenshot, or explicit assumption.

3. **Build state model**
   - Cover relevant states: empty, draft, loading, queued, running, stopped, success, partial failure, error, permission/login, settings, and recovery.
   - For each state, include trigger, visible regions, primary actions, next state, and recovery path.
   - Do not hide failure states in generic toast-only descriptions.

4. **Draft ASCII layout**
   - Draw the primary layout before visual styling.
   - Show fixed rails, flexible regions, scroll containers, artifact/detail panels, and modal overlays.
   - Include layout variants when a state changes the structure.

5. **Optional low-fidelity HTML**
   - Create `mockup.html` only when the user asks for a browser-openable wireframe or when visualizing structure materially helps review.
   - Keep it low fidelity: neutral styling, semantic regions, clear labels, and visible state examples.
   - Label it as structure reference, not production code.

6. **Create structure review notes**
   - List confirmed structure decisions.
   - List assumptions.
   - List blockers or questions before high fidelity.
   - Recommend `ui-mockup-desktop-workbench` when the structure is ready for high-fidelity handoff.

## Output Shape

Default outputs:

- `README.md` or concise handoff note: source PRD, scope, assumptions, and how to review.
- `screen-inventory.md`: screens, regions, source trace, and assumptions.
- `state-model.md`: states, triggers, actions, recovery, and PRD trace.
- `ascii-layout.md`: desktop or page layout structure.
- `mockup.html`: optional low-fidelity HTML wireframe.

If the user asks for a single response instead of files, include the same sections inline.

## Rules

1. Structure before visual polish.
2. State model before HTML.
3. PRD traceability before new interaction ideas.
4. Low-fidelity HTML is optional and never the source of truth.
5. If PRD has `draw.io -> SVG`总图或核心流程图，UI 文档必须承接其阶段位置。
6. If project provides `docs/templates-local/` UI overrides, use the local override for structure naming and layout expectations.
7. If the user asks for "高保真", "真实项目", "组件映射", "前端复刻", or "开发交付", route to `ui-mockup-desktop-workbench`.

## Template References

优先使用项目内 `docs/templates-local/` override；没有本地 override 时读取本 Skill 的模板：

- `references/templates/screen-inventory.md`
- `references/templates/state-model.md`
- `references/templates/ascii-layout.md`
- `references/templates/wireframe-handoff.md`
- `scripts/check_wireframe_package.py`

## Definition Of Done

完成标准：

- UI 结构先于视觉被确认。
- Screen inventory 覆盖目标页面/区域。
- 状态模型不缺关键状态和恢复路径。
- ASCII layout 展示布局区域、滚动行为和主要动作。
- 输出物至少包含 README/handoff、screen inventory、state model 和 ASCII layout。
- 需要时才生成低保真 HTML mockup。
- 明确说明下一步是否进入 `ui-mockup-desktop-workbench`。

## Evaluation

Smoke prompts:

- `基于这份 PRD 先出 UI 结构、状态模型和 ASCII 布局，不要做高保真。`
- `把这个页面需求转成低保真 HTML wireframe，重点确认状态和布局。`
- `PRD 已有页面结构时，先帮我补 screen inventory 和 state model。`

Non-trigger prompts:

- `基于 PRD 出高保真 mockup，开发要完全复刻。`
- `做真实项目 preview，并输出 component map。`
- `帮我写一份 PRD。`
- `只审一下这个 PRD 有没有问题。`

Capability checks:

- The output does not skip directly to visual styling.
- The output includes screen inventory, state model, and ASCII layout.
- Optional HTML is labeled as low-fidelity structure reference.
- The output routes high-fidelity or implementation-oriented requests to `ui-mockup-desktop-workbench`.

## Catalog Notes

- Category: `product-prd`
- Chinese name: PRD 到 UI 线框 / 结构阶段
- Status: `active`
- Relationship: structure-stage companion to `ui-mockup-desktop-workbench`.
