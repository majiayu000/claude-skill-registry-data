---
name: frontend-ui
description: UI/UX guidelines for app development in this Turborepo (apps/web and future apps). Use when designing or implementing app pages, layouts, navigation, or interactions with Tailwind and @repo/ui components.
---

# Frontend UI (Apps)

## Overview

Design and implement app UI/UX with consistent patterns, accessibility, and performance. Reuse shared components from `@repo/ui`, keep the landing page lightweight, and follow App Router conventions.

## Scope and Boundaries

- Apps may import packages; packages must not import apps.
- Prefer shared UI in `packages/ui` to avoid duplication across apps.
- App-specific UI belongs under the app (for web: `apps/web/src/components`).
- Import UI components via subpath exports (no barrel imports).

## Workflow

1. Scan existing app layouts/components to preserve established patterns.
2. Decide whether the UI should be shared (packages/ui) or app-specific.
3. Build the UI using `@repo/ui` components and Tailwind utilities.
4. Add or update local app components using the `~/` path alias.
5. Validate UX details: hierarchy, spacing, responsive behavior, states, and a11y.
6. Keep changes minimal and avoid new dependencies unless required; ask first.

## UI/UX Guidelines

- Layout: establish clear hierarchy with headings and section spacing; keep pages lightweight.
- Typography: use the existing Geist Sans/Mono setup unless explicitly asked to change.
- Color: rely on the UI theme tokens and CSS variables; avoid ad-hoc palettes.
- States: include hover/focus/active/disabled plus empty, loading, and error states.
- Responsiveness: design mobile-first and avoid horizontal scroll.
- Motion: use subtle, purposeful motion only when it improves clarity.

## Implementation Rules

- App Router only: routes live in `apps/web/src/app` (use `page.tsx` and `layout.tsx`).
- Use `~/` for local imports (e.g., `~/components/...`).
- Do not duplicate global CSS imports already defined in `apps/web/src/app/globals.css`.

## Accessibility and Semantics

- Use semantic elements (`header`, `nav`, `main`, `footer`) and proper heading order.
- Ensure keyboard access and visible focus states.
- Use buttons for actions and links for navigation.
- Provide labels or ARIA attributes where needed.

## Client Component Guidance

- Default to Server Components in apps.
- Add `"use client"` only when needed (hooks, browser APIs, event handlers).
- Isolate client components to the smallest subtree.

## Output Format (PR-ready)

- Follow the repo response format: Plan, Edits, Review Notes, Validation.
- In Review Notes, include a PR summary (what/why), risks, and follow-ups.

## Validation Commands

- `pnpm --filter web lint`
- `pnpm --filter web typecheck`
- `pnpm --filter web build`
- `pnpm --filter web format`
- Use repo-wide `pnpm lint` / `pnpm typecheck` when required.
