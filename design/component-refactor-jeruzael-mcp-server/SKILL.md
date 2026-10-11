---
name: component-refactor
description: Refactor frontend components safely without changing behavior. Use when Codex needs to break down large, messy, duplicated, hard-to-test, or hard-to-maintain frontend components in React, React Native, Vue, Angular, Flutter, or other component-based frameworks by extracting smaller components, hooks, utilities, form sections, modals, tables, list items, cards, loading/error/empty states, formatting helpers, and clearer file organization while preserving UI, styling, data flow, API behavior, validation, state management, permissions, routing, and tests.
---

# Component Refactor

Use this skill when a frontend component works but has become too large, duplicated, unclear, or risky to change.

## Core Rule

A component refactor must preserve existing behavior unless the user explicitly asks for behavior changes. Do not turn cleanup into a redesign, feature change, API change, or unrelated rewrite.

## Workflow

1. Understand the existing component:
   - feature, user role, displayed data, user actions, props, local state, global state, hooks, API calls, child components, conditional rendering, loading/error/empty states, styling, routing, permissions, and tests
2. Identify current responsibilities:
   - page layout, data fetching, state management, form validation, API submission, filtering, search, sorting, pagination, modal control, formatting, permissions, responsive layout, and business rules
3. Identify safe extraction opportunities:
   - headers, summary cards, filter bars, search controls, tables, rows, list items, detail cards, status badges, action groups, modals, form sections, loading states, error states, empty states, formatting helpers, custom hooks, and small utilities
4. Decide clear boundaries:
   - extracted components should have a clear purpose, simple name, minimal props, predictable behavior, and no unnecessary knowledge of parent internals
5. Preserve behavior:
   - UI layout, text labels, API calls, request payloads, response parsing, state transitions, validation, loading, errors, empty states, navigation, permissions, and responsive behavior
6. Keep state ownership clear:
   - page-level state remains in the page when multiple children need it, child-only UI state can stay in the child, server state follows existing query/API patterns, and global state is not introduced unless already required
7. Simplify props:
   - pass only what the child needs; avoid huge parent objects, confusing flags, duplicated state, and deep prop drilling unless that is the project pattern
8. Extract hooks only when useful:
   - data fetching, filters, pagination, modal state, form state, selection, debounce, auth access, or responsive calculations
9. Extract utilities only when useful:
   - date, currency, status, name, address, number formatting, labels, colors, and query construction
10. Preserve API compatibility:
   - endpoint, method, params, body, headers, response parsing, error handling, cache invalidation, retry behavior, and loading semantics
11. Preserve styling compatibility:
   - classes, style props, design tokens, component library props, responsive classes, spacing, widths, scroll behavior, modal overlays, and mobile behavior
12. Organize files according to project conventions and clean imports.
13. Add or update tests where practical.
14. Run relevant checks discovered from project scripts or docs.
15. Summarize what changed, what behavior was preserved, files changed, checks run, risks, and follow-up recommendations.

Read `references/component-refactor-checklist.md` for extraction heuristics, behavior-preservation checks, test ideas, and the final report format.

## Non-Negotiable Rules

- Do not change behavior unless explicitly requested.
- Do not redesign the UI unless explicitly requested.
- Do not change API contracts during a component refactor.
- Do not introduce new libraries unless explicitly approved.
- Do not extract before understanding existing behavior.
- Do not over-abstract simple JSX.
- Do not create many tiny components with unclear purpose.
- Do not duplicate state between parent and child components.
- Do not break loading, error, empty, or permission-based states.
- Do not move business logic into presentational components.
- Do not leave unused imports, dead code, or inconsistent file organization.
- Do not refactor unrelated files just because they are nearby.

## Output Contract

When using this skill, provide:

1. Refactor target and original maintainability issue.
2. Behavior preservation statement.
3. Components, hooks, or utilities extracted.
4. State and data flow after refactor.
5. API compatibility result.
6. Styling compatibility result.
7. Files changed.
8. Tests/checks or manual verification.
9. Risks and follow-up recommendations.
