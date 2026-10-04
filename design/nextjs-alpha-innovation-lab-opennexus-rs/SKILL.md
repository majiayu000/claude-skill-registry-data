---
name: nextjs
description: This skill should be used every time you work on Next.js projects or Next.js app code changes in this repository.
compatibility: opencode
---

# Next.js Project Structure Rules

This file defines the preferred Next.js project organization for this repo, constrained to folder names that appear in the official Bulletproof React project structure.

## Core Principles

1. Organize by feature and domain, not by file type.
2. Keep app-level orchestration in `app/` only.
3. Treat `features/` as the primary unit of change and ownership.
4. Share across features through top-level `components/`, `hooks/`, `lib/`, `types/`, `utils/`, and `config/`, never by reaching into another feature.
5. Keep feature boundaries explicit: local UI, logic, API calls, state, types, and utilities live together.
6. **Always use `next/link` for internal navigation** - never use `<a href="...">` for internal routes.

## Server Logging (MANDATORY)

1. All server logs must be written to a gitignored project-local directory.
2. Use `pino` as the approved server logging library.

## E2E Testing (MANDATORY)

1. Browser/runtime E2E testing must always use the `agent-browser` skill.
2. The `agent-browser` requirement is strict; do not substitute ad-hoc/manual browser testing.
3. If a server is already running, do not kill it just to rerun tests.

## Tailwind CSS v4 (MANDATORY)

**Tailwind CSS v4 is the only permitted CSS framework.**

### Strict Rules

1. **v4 only** - use current Tailwind v4 setup, not older Tailwind patterns.
2. **No CSS-in-JS** - no styled-components, Emotion, or CSS modules.
3. **No inline styles** - use Tailwind utility classes.
4. **Component patterns** - compose complex styles with utility classes instead of custom class systems.
5. **Arbitrary values** - use square bracket notation for one-off values such as `w-[300px]`.
6. **clsx/tailwind-merge** - use `clsx` and `tailwind-merge` for conditional classes.

### Anti-Patterns (NEVER DO THESE)

- Using styled-components, Emotion, or similar
- Using `@apply` to extract classes
- Using inline `style` props
- Mixing Tailwind with other CSS solutions

## Top-Level Layout

```text
src/
├── app/          # application layer
├── assets/       # static assets
├── components/   # shared components
├── config/       # global configuration
├── features/     # feature based modules
├── hooks/        # shared hooks
├── lib/          # reusable libraries
├── stores/       # global state stores
├── testing/      # test utilities and mocks
├── types/        # shared types
└── utils/        # shared utility functions
```

## Folder Semantics

- `app/`: application glue and composition only.
  - `routes/`, `app.tsx`, `provider.tsx`, `router.tsx`
- `features/`: each feature is a self-contained folder.
  - `features/awesome-feature/`
- `components/`: shared components used across the application.
- `hooks/`: shared hooks used across the application.
- `lib/`: reusable libraries preconfigured for the application.
- `types/`: shared types used across the application.
- `utils/`: shared utility functions.
- `config/`: global configuration and exported environment variables.
- `assets/`: static assets such as images and fonts.
- `stores/`: global state stores.
- `testing/`: test utilities and mocks.

## Feature Structure (Bulletproof)

Each feature owns its UI, logic, and API integration. Add only what the feature needs.

```text
src/features/awesome-feature/
├── api/         # exported API request declarations and API hooks
├── assets/      # feature-specific static assets
├── components/  # feature-scoped UI
├── hooks/       # feature-scoped hooks
├── stores/      # feature state stores
├── types/       # feature types
└── utils/       # feature utilities
```

## Feature Size And Atomicity

Features must stay small, focused, and explainable in one sentence. Avoid turning a single feature into a god-folder that owns multiple unrelated responsibilities.

When a feature grows too large, split it into smaller atomic features using flat names under `features/`:

```text
features/<feature-name>-<subfeature>/
```

This keeps boundaries explicit without introducing an extra architectural layer that Bulletproof React does not define.

Good examples:

- `features/chat-panel-transcript/`
- `features/chat-panel-sidebar/`
- `features/chat-panel-summary/`
- `features/conversation-list/`
- `features/conversation-search/`

Avoid splitting by arbitrary file type or low-level implementation detail.

Less useful examples:

- `features/chat-panel-buttons/`
- `features/chat-panel-utils/`
- `features/chat-panel-misc/`

Use a separate feature when the code has its own UI, logic, state, API interaction, or user-facing responsibility. Keep code nested inside an existing feature when it is only a private implementation detail of that feature.

Rules of thumb:

1. If a feature has multiple distinct user-facing responsibilities, split it.
2. If a folder needs many unrelated components, hooks, stores, and types, split it.
3. If a piece can be understood, tested, and replaced on its own, it can likely be its own feature.
4. Keep cross-feature imports forbidden; compose features at the `app/` layer.

## File Naming

1. Use `kebab-case` for folders and files.
2. Filename matches the primary component or concern.
3. One logical concern per file.

## Import Rules

1. `features/` can import from `components/`, `hooks/`, `lib/`, `types/`, `utils/`, `config/`, and `stores/`.
2. `components/`, `hooks/`, `lib/`, `types/`, `utils/`, `config/`, and `stores/` never import from `features/`.
3. Cross-feature imports are forbidden; compose features at the `app/` layer.

## Example Structure

```text
src/
├── app/
│   ├── routes/
│   ├── app.tsx
│   ├── provider.tsx
│   └── router.tsx
├── assets/
├── components/
├── config/
├── features/
│   └── awesome-feature/
│       ├── api/
│       ├── assets/
│       ├── components/
│       ├── hooks/
│       ├── stores/
│       ├── types/
│       └── utils/
├── hooks/
├── lib/
├── stores/
├── testing/
├── types/
└── utils/
```
