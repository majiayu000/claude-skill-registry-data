---
name: ui-component-architecture
description: >
  Keep React screens thin and reusable UI in its own package, separate from
  app screens. Triggers when authoring or restyling a page, route, screen, or
  component in an app that has a shared UI package — especially when a file is
  trending toward walls of plain <div className="..."> Tailwind markup. Bias
  toward reusing existing primitives in that package and graduating new
  reusable units into it, while avoiding premature over-extraction. Do NOT
  trigger for non-React code, for single-package apps with no shared UI
  package, or for editing the internals of one existing component. The package
  name is per-repo (see ADR-0013); do not require @repo/ui or @native/ui.
---

# UI component architecture

The failure mode this corrects: an agent authors a screen as a few hundred lines
of `<div className="...">` Tailwind soup — reimplementing a `Button`, `Card`, or
`Badge` that already exists in the shared UI package, and never graduating the
genuinely reusable pieces back into that package. The result is duplicated
styling, drifting visual language, and screens nobody can read.

The fix is two habits: **reuse before you author**, and **keep screens thin by
extracting reusable units into the shared UI package** — without over-extracting
one-off layout glue. That package MUST be its own package. Its path and import
alias are per-repo ([ADR-0013](../../docs/adr/0013-shared-ui-is-its-own-package.md)).
Discover them from the workspace (`package.json` workspaces, `packages/*`,
vendor trees). Do not invent a required name.

Apply [codebase-design](../codebase-design/SKILL.md) when choosing component
boundaries. Keep state, handlers, private components, and layout together when
they explain one capability. An extraction should hide behavior or enable useful
reuse; neither JSX length nor a second call site establishes that on its own.

## When to use

- Authoring a new page/route/screen in an app that has a shared UI package.
- Restyling or refactoring an existing screen that's heavy with inline divs.
- Building a component that looks like a reusable primitive (button, card,
  badge, input, dialog, empty state, stat, skeleton, avatar).
- The user says "build the X page", "add a Y view", "create a Z component".

## When NOT to use

- Non-React code, or a single-package app with no shared UI package to reuse into.
- A one-off layout wrapper with no independent responsibility to extract.
- Editing the internals of one existing component, not adding a new surface.

## Principles

### Reuse before you author

Before writing JSX, inventory what already exists so you don't reinvent it:

- The shared UI package — read its barrel or `package.json` `exports`. Grep for
  the thing you need.
- External registries — for blocks not yet in the shared package, see the
  `shadcn-registry-first` skill. The flow is registry → app screen → graduate the
  stable pieces into the UI package.

Don't reimplement a `Button`, `Card`, `Badge`, `Input`, `Dialog`, or
`EmptyState` that already exists.

### Keep screens thin

A route should make its data and major visual capabilities easy to follow.
Compose existing primitives and extract components with a meaningful interface.
Keep cohesive state and event handling with the UI they control. A component
that only forwards a screen's props and markup adds navigation without hiding
complexity. Private components may share a file with their owner.

### Graduate reusable units into the UI package

The load-bearing heuristic for what moves into the shared package:

- **Graduates:** a reusable presentational unit with an independent interface,
  **or** a self-contained visual primitive — `Button`, `Card`, `Badge`, `Avatar`,
  `EmptyState`, `Stat`, `Skeleton`, `Input`, `Dialog`. Reuse in a second place is
  evidence to inspect; visual similarity alone does not establish one unit.
- **Stays in the app:** app-specific composition (a particular dashboard's
  layout), one-off glue, and anything carrying data-wiring or business logic.
- **When unsure, leave it local.** A single-use component can hide substantial
  behavior, but app-specific props belong in the app. A second use is a prompt
  to review the boundary, not to move app state into the shared package.

### Style with tokens and variants, not scattered magic values

- Use theme tokens (CSS variables, the Tailwind theme) — not raw hex literals
  sprinkled through `className`.
- For components with variants, use a `cn` + variant map (or `cva`) rather than
  conditional class-string soup.
- Centralize styles for a reusable visual unit; keep incidental layout local.

## Workflow

### 1. Inventory the shared UI package

Find the package (workspace list, `packages/*`, vendor tree). List what it
already exports. Note the primitives you'll reuse so you don't rebuild them.

### 2. Sketch the screen as composition

Before writing detail, outline the page as a tree of named components. Tag each
node: _exists in the UI package_ / _app-specific composition_ / _new but looks
reusable_. This tells you what to import, what to inline, and what to extract.

### 3. Author the screen thin

Compose existing primitives and keep each interaction understandable in one
place. If a file exceeds its configured limit, split at a useful responsibility
or document a narrow increase; file height alone does not select a component.

### 4. Extract the reusable pieces

For each piece that meets the graduation heuristic:

- Put it in the UI package, next to its siblings.
- Export it from the barrel or `package.json` `exports`.
- Keep props **generic** — no app-specific types, routes, stores, or API clients
  leaking into a UI primitive. A shared UI component should be dumb and
  presentational; data comes in as props.
- Co-locate variants with `cn`/`cva`.

### 5. Verify

- The screen imports primitives from the UI package rather than redefining them.
- No app-specific imports (`@/...`, app routers, stores, API clients) inside any
  UI-package component.
- Types and build pass using the repository's commands.
- Interactions complete through the component's public interface; tests observe
  user behavior rather than its private hook or helper calls.

## What graduates vs what stays

| Stays in the app                         | Graduates to the UI package               |
| ---------------------------------------- | ----------------------------------------- |
| The `/dashboard` page layout             | `StatCard`, `Badge`, `EmptyState`         |
| Route-specific data fetching and wiring  | `Button`, `Input`, `Dialog`, `Skeleton`   |
| A hero used once on one marketing page   | A hero variant reused across 3+ pages     |
| Business logic, feature flags, app state | Presentational primitives that take props |

## Avoiding over-extraction

Over-extraction is the opposite failure and just as costly. Signs you extracted
too eagerly:

- UI-package components with props named after one specific screen.
- A component that forwards a long prop list without hiding an interaction or
  presentation decision.
- UI primitives importing app stores, routers, or API clients.

Fix: keep app-specific behavior in a cohesive app component. Extract the shared
primitive only when it has a useful presentational interface. Keep local helpers
and private components nearby even when they are used once.

## Reference

- `reference/agents-md-rule.md` — a short, paste-able always-on rule for a
  consuming repo's `AGENTS.md`. This is the highest-leverage lever: skills are
  loaded on demand and can under-trigger on "every UI edit," whereas an
  `AGENTS.md` rule is always in context. Drop it into each repo that has a
  shared UI package; fill in that repo's actual package path and import alias.
- `reference/eslint-guardrails.md` — lint rules that enforce the boundaries
  mechanically (no raw hex in app JSX, capped JSX depth, and — most importantly —
  a boundary rule banning app imports inside the UI package).

## Relationship to other skills

- `shadcn-registry-first` — sources _external_ blocks from registries. This skill
  governs _internal_ reuse and extraction. They compose: registry → app screen →
  graduate stable pieces into the UI package.
- `darkmatter-design-system` — visual language and tokens when the app uses that
  system. Those tokens still live in the UI package; this skill is the package
  boundary.
- `repository-organization` — where directories and packages live. This operates
  one level down, at the component-reuse granularity.
- `vercel-react-best-practices` — performance patterns for the components you
  write and compose.
