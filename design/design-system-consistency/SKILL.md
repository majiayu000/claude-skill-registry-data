---
name: design-system-consistency
description: Keep user interfaces visually consistent with the existing product design system. Use when Codex needs to add screens, improve old screens, standardize inconsistent UI, apply brand guidelines, create dashboards, forms, landing pages, admin pages, mobile screens, reports, settings pages, refactor UI components, clean inconsistent buttons/cards/inputs/badges/icons, align loading/error/empty states, prepare UI for client presentation, or prepare a product for handover or launch while reusing established colors, typography, spacing, layout patterns, components, border radius, shadows, navigation patterns, and responsive conventions.
---

# Design System Consistency

Use this skill when UI work must look like it belongs to the same product instead of a one-off screen.

## Core Rule

Inspect existing design sources and repeated UI patterns before making visual changes. Reuse tokens, components, variants, and layout conventions before introducing new styles.

## Workflow

1. Identify the UI area:
   - screen, component, user role, current visual issue, existing reference UI, brand guideline source, and whether the task is new UI, cleanup, or redesign alignment
2. Inspect design sources:
   - theme files, CSS variables, Tailwind config, global CSS, component library setup, shared UI components, layouts, existing buttons/cards/forms/icons/badges, empty/loading/error states, README notes, style guides, and brand assets
3. Identify the current design pattern:
   - background, primary/secondary colors, text hierarchy, muted text, borders, surfaces, buttons, inputs, border radius, shadows, spacing rhythm, typography scale, icons, page headers, tables, modals, navigation, and status badges
4. Compare the target UI against existing patterns:
   - identify exact inconsistencies in colors, fonts, sizes, weights, button variants, card styles, radius, shadows, padding, margins, icons, forms, tables, states, badges, and layout
5. Reuse existing components first:
   - Button, Card, Input, Select, Badge, Modal, Table, Layout, PageHeader, EmptyState, ErrorBanner, Spinner, Skeleton, StatCard, FormSection, and SectionHeader
6. Use existing tokens:
   - colors, typography, spacing, radius, border, shadow, z-index, animation, status, and semantic variants
7. Follow existing patterns for:
   - buttons, form fields, cards, containers, icons, status badges, page layouts, navigation, loading states, error states, empty states, success messages, toasts, and mobile behavior
8. Avoid unnecessary visual complexity:
   - extra colors, font sizes, shadows, gradients, card styles, borders, animations, or decorative elements that do not support the user's task
9. Apply brand guidelines consistently when provided:
   - flag conflicts between new brand guidance and current app styles before mixing them
10. Add or update shared components only when they solve a repeated pattern.
11. Preserve responsive behavior, auth/permission behavior, loading/error/empty states, and existing business flow while polishing visuals.
12. Run relevant checks discovered from project scripts or docs.
13. Summarize references used, patterns identified, inconsistencies found, changes made, reused components/tokens, files changed, checks, risks, and follow-up recommendations.

Read `references/design-system-checklist.md` for design-source inspection, inconsistency categories, token/component reuse guidance, state consistency checks, and the final report format.

## Non-Negotiable Rules

- Do not invent new styles before inspecting existing ones.
- Do not hardcode random colors when design tokens exist.
- Do not introduce a new UI library unless approved.
- Do not mix unrelated icon styles.
- Do not create duplicate button, card, input, badge, or modal styles unnecessarily.
- Do not change brand identity without instruction.
- Do not redesign the whole screen if the task is consistency cleanup.
- Do not sacrifice usability for decoration.
- Do not remove loading, error, empty, success, or unauthorized states while improving visuals.
- Do not break responsive behavior while standardizing UI.
- Do not create visual changes that conflict with role or permission behavior.
- Keep UI changes focused, explainable, and consistent with project conventions.

## Output Contract

When using this skill, provide:

1. UI area reviewed or updated.
2. Existing design references used.
3. Design system patterns identified.
4. Exact inconsistencies found.
5. Changes made.
6. Components and tokens reused.
7. Responsive and state consistency notes.
8. Files changed.
9. Tests/checks or manual verification.
10. Risks and follow-up recommendations.
