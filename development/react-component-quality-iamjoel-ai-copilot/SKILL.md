---
name: react-component-quality
description: High-quality React component authoring focused on single responsibility, low coupling, and English-only code and comments. Use when adding or refactoring client components in this repo to enforce modularity, composability, and clarity without mixing responsibilities.
---

# React Component Quality

## Intent
- Treat each component as a single responsibility boundary: one component = one clear purpose, data source, and output.
- Favor composition over polymorphism to keep coupling low with parents, services, and utilities.
- Keep all code, identifiers, and comments in English so future collaborators can understand intent instantly.

## Workflow
1. Clarify what the component renders, which data it consumes, and what events it emits before writing JSX.
2. Keep state and business logic in the safest narrow scope—lift to parents or hooks if multiple children need the same data.
3. Pass only the props necessary for rendering; wrap additional behavior in callbacks or context readers that stay external to the component.
4. Break out helpers (formatting, data transforms, effect setups) into custom hooks or utility functions when they would otherwise inflate the component body.
5. Prefer `useMemo` / `useCallback` only when profiling shows actual recomputation concerns; default to keeping components pure.
6. Write `Prop` types or interfaces that describe the minimal shape needed for rendering; rely on optional fields sparingly.

## Architecture Guidelines
- Use descriptive component names that match their single responsibility (e.g., `UserRow`, `CheckoutSummary`, `StatusBadge`).
- Avoid deep prop chains by grouping related props into objects or by exposing render props/hooks that share context for multiple values.
- Keep presentational logic (JSX) decoupled from data handling; map data to view models outside the JSX block when possible.
- Limit module-level imports to what the component actually uses; prefer dependency injection via props or hooks rather than reaching into stores and singletons directly.
- When composing children, prefer passing render callbacks or context providers instead of forcing knowledge of parent internals.

## Communication
- Label every prop, helper, and handler with names that describe intent rather than implementation details.
- Annotate complex sections with short English comments explaining the why (not the what), but avoid redundant comments around trivial JSX.
- Write every new code or inline comment in English to keep this repository accessible to all contributors.

## Definition of Done
- The component has a single, well-defined responsibility with trimmed props, focused rendering, and no hidden side effects.
- Coupling is minimized by delegating shared logic to hooks/services and exposing a narrow API surface.
- Tests or storybook stories (where required) illustrate the component's API, and all documentation remains in English.
