---
name: drag-and-drop
description: "Implement drag-and-drop in LWC using HTML5 Drag and Drop API, keyboard alternatives, and accessible announcements. NOT for kanban migration from legacy Lightning."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - User Experience
  - Reliability
triggers:
  - "lwc drag drop"
  - "reorder list lwc"
  - "drag file into lwc"
  - "kanban drag and drop lwc"
tags:
  - lwc
  - drag-drop
  - a11y
inputs:
  - "items to reorder or move"
  - "accessibility requirements"
outputs:
  - "component with dragstart/dragover/drop handlers + keyboard fallback"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

# LWC Drag and Drop

Native HTML5 Drag and Drop works in LWC — no library needed. The tricky parts are (1) preventing default on dragover, (2) carrying item identity via dataTransfer, and (3) providing a keyboard-accessible alternative (focus + arrow keys). This skill lays out the template, the JS handlers, and the ARIA live-region announcements.

## When to Use

Any reordering UI (priority list, board columns, file drop zones). Not for complex trees (use a specialized library behind an LWC wrapper).

Typical trigger phrases that should route to this skill: `lwc drag drop`, `reorder list lwc`, `drag file into lwc`, `kanban drag and drop lwc`.

## Recommended Workflow

1. Template: add `draggable="true"`, `@dragstart`, `@dragover` (with preventDefault), `@drop` on source/target elements.
2. Pass identity via `event.dataTransfer.setData('text/plain', itemId)`.
3. Keyboard alternative: `@keydown` on item, arrow keys reorder with the same handler logic.
4. Announce drag start/drop via a `role="status"` aria-live region.
5. Jest test: simulate dragstart/drop; assert reorder + announcement.

## Key Considerations

- `dragover` must call `event.preventDefault()` or `drop` never fires.
- Touch devices don't fire drag events — detect and show reorder buttons.
- dataTransfer is cleared after drop — capture any data synchronously in dragstart.
- aria-grabbed is deprecated; announce via live region instead.

## Worked Examples (see `references/examples.md`)

- *Priority list reorder* — Case priority list
- *File drop zone* — Attachments upload

## Common Gotchas (see `references/gotchas.md`)

- **Missing preventDefault** — Drop never fires; silent bug.
- **Touch devices** — Mobile users can't reorder.
- **No keyboard path** — A11y audit fails.

## Top LLM Anti-Patterns (full list in `references/llm-anti-patterns.md`)

- Using an external drag library for simple lists
- Skipping keyboard support
- No aria-live announcement

## Official Sources Used

- Lightning Web Components Developer Guide — https://developer.salesforce.com/docs/platform/lwc/guide/
- Lightning Data Service — https://developer.salesforce.com/docs/platform/lwc/guide/data-wire-service-about.html
- LWC Recipes — https://github.com/trailheadapps/lwc-recipes
- SLDS 2 — https://www.lightningdesignsystem.com/2e/
