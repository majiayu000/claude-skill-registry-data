---
name: ui-accessible-component
description: Use when building or reviewing an interactive UI widget (dialog, menu, combobox, tabs, tooltip) — compose behavior/accessibility from a headless primitive and style from design tokens instead of hand-rolling focus, keyboard, and ARIA.
stacks: [node]
domains: [web]
phases: [dev]
tags: [ui, accessibility, react, headless, shadcn, radix, aria]
scope: kit
---
**When to use.** Any time the task adds/changes an interactive component. *Why:* hand-written widgets
are where a11y bugs (focus loss, no keyboard, wrong roles) hide, and an agent reliably forgets them.

**Procedure.**
1. Identify the widget's WAI-ARIA APG pattern; if custom, open the APG page for it.
2. Take behavior from a headless primitive (Base UI / Radix); never re-implement focus-trap, keyboard nav, or ARIA by hand.
3. Style only via design tokens (see `design-token-steward`) — no hard-coded colors/spacing.
4. **Done when:** keyboard-only operable, visible focus, `aria-*` matches the APG pattern, contrast ≥ 4.5:1, `prefers-reduced-motion`/`prefers-color-scheme` respected — verified by an axe-core run pasted into the result, not asserted.

**Knowledge:** KNOWLEDGE-LIBRARY.md §A1. **Example:** the Base UI dialog snippet there.
