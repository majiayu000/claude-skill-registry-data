---
name: responsive-behavior-planner
description: Defines how layout, controls, content priority, and interactions adapt across available space. Use when the user asks to plan responsive behavior, breakpoint strategy, container behavior, mobile/tablet/desktop adaptations, navigation changes, content reflow, or interaction differences before implementation.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: planner
  audience: frontend-developers-product-designers
  tags:
    - responsive-design
    - layout
    - breakpoints
    - content-priority
    - interaction-design
    - frontend
  status: draft
  side_effects: none
---

# Responsive Behavior Planner

## Purpose

Create an implementation-ready plan for how an interface should adapt as available space changes. Define layout, navigation, controls, content priority, interaction behavior, and state handling across narrow, medium, wide, and constrained containers without relying on vague “make it responsive” guidance.

This skill focuses on responsive behavior decisions, not finished visual styling or CSS implementation.

## When to use this skill

Use this skill when:

- The user asks how an interface should adapt across mobile, tablet, desktop, or wide layouts.
- A page, component, dashboard, form, navigation system, or content-heavy view needs a breakpoint or container-query plan.
- Requirements define desktop behavior but omit narrow-screen or constrained-container behavior.
- Controls, filters, tables, cards, media, or sidebars need priority and reflow rules.
- The team needs design and implementation guidance before writing responsive CSS.
- The user uses phrases such as “make this responsive,” “plan the mobile behavior,” “what happens at smaller widths,” “define breakpoints,” “adapt this layout,” or “responsive UX.”

Do not use this skill when:

- The user only asks for visual art direction, color, typography, or brand style.
- The task is limited to fixing one CSS overflow bug with no broader behavior planning.
- The user wants a full accessibility audit rather than responsive behavior planning.
- The request is only about backend, data modeling, or non-interface architecture.
- A finalized responsive design spec already exists and only needs implementation.

## Inputs to inspect

Inspect the smallest useful set of available inputs:

- Product brief, user stories, acceptance criteria, or design requirements
- Current screenshots, wireframes, prototypes, or design files
- Existing responsive behavior in the product or related components
- Target users, devices, usage contexts, and accessibility constraints
- Content inventory, content length variations, localization needs, and media dimensions
- Core user tasks and actions by priority
- Relevant routes, components, layouts, styles, tokens, or framework configuration
- Existing breakpoints, container widths, grid systems, navigation patterns, and component variants

When repository access is available, inspect relevant files such as:

- `README.md`
- `src/`, `app/`, `pages/`, `components/`, or `layouts/`
- `styles/`, CSS modules, Sass files, CSS-in-JS files, or design-token files
- `tailwind.config.*`, theme configuration, or breakpoint constants
- Storybook stories, examples, demo pages, screenshots, or visual regression fixtures

## Planning dimensions

Cover these dimensions when they affect the interface:

- **Available space:** viewport width, viewport height, container width, orientation, split-screen, zoom, and embedded contexts.
- **Layout structure:** columns, regions, grids, stacking, sidebars, panels, sticky areas, and scroll containers.
- **Content priority:** what remains visible, moves lower, collapses, truncates, summarizes, becomes progressive disclosure, or is removed only when truly nonessential.
- **Controls:** navigation, filters, search, sort, pagination, toolbars, menus, primary actions, secondary actions, destructive actions, and form controls.
- **Interactions:** hover, touch, keyboard, drag, swipe, long-press, focus order, modal versus inline behavior, and pointer precision differences.
- **State behavior:** loading, empty, error, selected, expanded, validation, disabled, and overflowing states at each layout mode.
- **Performance and implementation:** image sizing, expensive content, layout shift, hydration-sensitive behavior, and component reuse.

## Workflow

1. **Frame the responsive problem.** Restate the target interface, primary user task, key content, most important actions, known constraints, and unsupported assumptions.
2. **Inventory responsive inputs.** Identify existing breakpoints, component variants, layout primitives, content types, user contexts, and known problem widths or containers.
3. **Prioritize content and actions.** Rank critical, supporting, optional, and decorative content. Rank actions as primary, secondary, contextual, destructive, or rare.
4. **Choose adaptation units.** Decide whether behavior should respond to viewport breakpoints, container queries, content thresholds, orientation, height, or a combination. Prefer component-owned container behavior when components appear in multiple contexts.
5. **Define layout modes.** Name each mode by behavior, not just device labels, such as `single-column`, `compact-toolbar`, `two-column`, `sidebar-expanded`, or `wide-dashboard`.
6. **Map reflow rules.** Specify how regions reorder, stack, resize, wrap, collapse, pin, scroll, or become progressive disclosure as space changes.
7. **Map control adaptations.** Define how navigation, filters, forms, action bars, tables, and dense controls change while preserving discoverability and task completion.
8. **Map interaction adaptations.** Replace hover-only or precision-pointer assumptions with touch, keyboard, and reduced-space alternatives. Preserve focus order and avoid hidden required actions.
9. **Cover state and content stress cases.** Plan long labels, localization, dynamic lists, empty states, errors, loading, selected items, validation messages, media aspect ratios, and user zoom.
10. **Identify implementation implications.** Extract required component variants, CSS primitives, breakpoints or container thresholds, state props, test fixtures, and QA scenarios without writing code unless asked.
11. **Validate continuity.** Check that each mode supports the primary task, exposes required controls, preserves context during transitions, avoids data loss, and has no unreachable actions.
12. **Record open decisions.** List decisions that materially affect responsive behavior, with safe defaults when evidence supports them.

## Output format

Return:

```md
## Responsive frame

- Interface:
- Primary task:
- Key content:
- Critical actions:
- Constraints:
- Assumptions:

## Content and action priority

| Item | Priority | Behavior when space shrinks | Notes |
|---|---|---|---|

## Layout modes

| Mode | Trigger or threshold | Layout behavior | Primary risks |
|---|---|---|---|

## Responsive behavior plan

### Mode: Name

- Layout:
- Navigation and controls:
- Content priority:
- Interaction changes:
- State behavior:
- Implementation notes:

## Component adaptation matrix

| Component or region | Compact behavior | Medium behavior | Wide behavior | Stress cases |
|---|---|---|---|---|

## QA checklist

- [ ] Primary task is possible in every mode.
- [ ] Required controls remain discoverable and keyboard-accessible.
- [ ] Content reflows without horizontal overflow unless intentionally scrollable.
- [ ] Long content, localization, zoom, loading, empty, and error states are covered.
- [ ] Mode transitions preserve user context and input.

## Open decisions

| Priority | Decision | Why it matters | Suggested default |
|---|---|---|---|
```

Use concrete mode names and thresholds when evidence supports them. If exact pixel values are unknown, describe behavioral thresholds and explain what evidence should determine final values.

## Quality bar

The task is complete only when:

- The plan prioritizes content and actions before choosing layout mechanics.
- Each layout mode has a clear trigger and behavioral purpose.
- Navigation, controls, content, interactions, and states are covered where relevant.
- Required actions remain available and understandable in every supported mode.
- Hover-only, desktop-only, and fixed-width assumptions are replaced or explicitly justified.
- Stress cases include long content, dynamic data, user zoom, loading, empty, and failure states when relevant.
- Implementation implications are specific enough for design, engineering, and QA to act on.
- Open decisions are separated from established requirements and assumptions.

## Edge cases

- If the component can appear in multiple containers, prefer container-based behavior over page-level viewport assumptions.
- If the interface contains dense data, decide whether to reflow, summarize, pin key columns, provide row details, or use intentional horizontal scrolling.
- If controls collapse into menus or drawers, preserve primary actions outside hidden menus unless there is a clear reason not to.
- If content is removed at compact sizes, confirm it is decorative or available through an equivalent path.
- If orientation, height, or split-screen use changes behavior, document it separately from width breakpoints.
- If existing breakpoints conflict with content needs, recommend content-driven thresholds rather than inheriting arbitrary values.
- If responsive behavior may affect accessibility, call out focus order, reading order, target size, zoom, and reduced-motion implications.

## Related skills

- `layout-art-direction`
- `ui-design-direction-builder`
- `interface-state-coverage-review`
- `user-flow-planner`
