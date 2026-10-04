---
name: frontend-classification
description: Classify whether a ticket is frontend or UI work. Use when deciding whether design-aware planning, visual verification, UI tests, or screenshot capture applies.
user-invocable: false
---

## Frontend/UI Classification

This is the single source of truth for "is this frontend/UI work?". `refine` (design-aware refinement), `implement` (Design Check gate and `isUiTicket` flag), and any other caller apply exactly this rule — never restate the keyword list inline in a calling skill; reference this skill instead.

A ticket or task is classified as **frontend/UI** when its title, description, acceptance criteria, or digest summary mention any of:

- UI components, pages, views, layouts, forms, or modals
- Visual design, styling, CSS, animations, or themes
- Frontend frameworks (React, Angular, Vue, Svelte, etc.)

If none of these signals are present, treat the work as backend/infrastructure/data and skip design-specific behavior.

## Visual-check signals (subset)

A stronger subset of signals indicates the change is *visually verifiable* and warrants the `ui:visual-check` label / interactive browser verification: CSS, layout, responsive behavior, themes, design tokens, styling, visual polish, animations, or appearance changes.
