---
name: effector-fsd
description: "Use when designing, reviewing, generating, or refactoring Feature-Sliced Design project structure for Effector ecosystem applications: layers, slices, segments, public APIs, imports, placement of Effector models, Farfetched operations, Atomic Router routes, Next.js adapters, and Steiger checks."
license: MIT
---

# Effector + Feature-Sliced Design Skill

## Purpose

Use this skill for **project structure** in applications that combine Feature-Sliced Design with the Effector ecosystem.

This skill answers:

- where code belongs in `app`, `pages`, `widgets`, `features`, `entities`, `shared`
- how Effector models are split by ownership
- where Farfetched queries/mutations/contracts/barriers live
- how Atomic Router routes and protected routes are placed
- how Next.js `app`/`pages` framework folders coexist with FSD layers
- how public APIs, `@x` cross-imports, and import boundaries work
- how to review and lint FSD architecture with Steiger

Use `effector-ecosystem` alongside this skill for exact Effector/Farfetched/React/Next.js API usage. This skill owns **placement and structure**; `effector-ecosystem` owns **reactive code semantics**.

## Activation triggers

Use this skill when the user asks about:

- FSD, Feature-Sliced Design, layers, slices, segments, public API
- where to place `model`, `ui`, `api`, `lib`, `route.ts`, contracts, mappers, forms, queries, mutations, barriers, widgets, providers, or adapters
- refactoring `src/api`, `src/components`, `src/store`, `src/hooks`, `src/utils` into FSD
- protected routes/auth flow placement
- Next.js + FSD folder conflicts
- import boundary violations, direct imports, cross-imports, `@x`
- Steiger or FSD linting
- reviewing an Effector project for architecture boundaries

## First response behavior

When the user asks a placement question, answer with:

1. The layer/slice/segment where the code belongs.
2. The reason in FSD terms: responsibility, dependency direction, ownership.
3. The Effector-specific boundary: which model owns the event/store/query/mutation/route.
4. A small folder tree or import example.
5. Anti-patterns to avoid.

When the question is mostly about exact Effector/Farfetched API syntax, defer to `effector-ecosystem` but keep placement guidance here.


## Full audit mode

When the user asks for a full FSD/Effector architecture audit, do not only check import direction and folder names. Also inspect **ownership of cross-cutting Effector flows**:

1. Find all slice public APIs and compare exported surface with actual consumers. Flag feature public APIs that leak raw mutations, internal stores, or implementation events when consumers only need semantic facts such as `profileUpdated` or a `$$feature` facade.
2. Find page models that listen to feature/entity mutation successes. Because Effector models are static once imported, require a route `$isOpened` gate or move invalidation to an app/entity integration owner.
3. Find APIs/contracts placed in `pages`. If the operation or contract describes a reusable business resource, move it to an `entity`; if it is a user action, move the mutation to a `feature`; keep only page-only filters/list queries in `pages`.
4. Find global auth/unauthorized/barrier/invalidation wiring. Cross-slice policy that imports many features/entities belongs in `app`, not inside `shared`, and not scattered through unrelated pages.
5. Find shared adapters that store domain state indirectly, such as auth headers mirrored from session. Verify `shared` stays transport-only or document an adapter boundary.
6. Report “no cycles/import violations found” only after also checking whether public APIs are too broad and whether hidden orchestration is placed in the wrong owner.

For each finding, give the target owner (`app`, `page`, `widget`, `feature`, `entity`, `shared`), the dependency reason, and a minimal folder/import example.

## Non-negotiable FSD rules

### 1. Dependency direction is downward by layer

Default layer order:

```txt
app -> pages -> widgets -> features -> entities -> shared
```

A module inside a slice can import only from:

- the same slice via relative imports
- public APIs of slices on lower layers
- `shared` infrastructure

It must not import from higher layers or from sibling slices on the same layer, except explicit `@x` public APIs for justified entity relationships.

### 2. Public API is mandatory

Every slice must expose a public API through `index.ts`.

External code imports from:

```ts
import { UserAvatar, userQuery } from '@/entities/user';
```

not from:

```ts
import { userQuery } from '@/entities/user/api/user.query';
import { $user } from '@/entities/user/model/user.model';
```

Inside a slice, use relative imports. Between slices, use absolute imports through public APIs.

### 3. App and Shared are sliceless layers

`app` and `shared` are layers and slices at the same time. They contain segments directly, not business slices.

Good:

```txt
shared/api/
shared/ui/
shared/lib/date/
app/providers/
app/routes/
app/model/
```

Bad:

```txt
shared/user/
shared/features/
app/entities/
```

### 4. Segments group by purpose, not by dumping ground names

Use conventional segments:

```txt
ui      # rendering and visual composition
model   # stores, events, business rules, contracts if they describe the model
api     # backend operations, DTO mappers, endpoint-specific remote logic
lib     # local helpers for this slice/segment
config  # feature flags/config for this owner
route   # route declaration/re-export when route ownership is local
```

Avoid generic dumping grounds:

```txt
components/
hooks/
helpers/
utils/
types/
store/
```

A small `types.ts` or `utils.ts` is acceptable only when it is tightly scoped and not mixing multiple domains.

### 5. Create only useful layers and segments

Do not scaffold every layer and segment by default. Add a layer/segment when it has real content and a clear owner.

Most apps need at least:

```txt
app/
pages/
shared/
```

Add `entities`, `features`, and `widgets` when the product complexity justifies them.

## Default Effector + FSD project shape

```txt
src/
  app/
    entrypoint/
    providers/
    routes/
    model/
    styles/

  pages/
    <page>/
      index.ts
      route.ts
      ui/
      model/
      api/        # page-specific only
      lib/

  widgets/
    <widget>/
      index.ts
      ui/
      model/
      lib/

  features/
    <user-action>/
      index.ts
      ui/
      model/
      api/
      lib/

  entities/
    <domain-entity>/
      index.ts
      @x/         # only explicit entity cross-import APIs
      ui/
      model/
      api/
      lib/

  shared/
    api/
    config/
    routes/
    ui/
    lib/
    i18n/
    assets/
```

Do not create empty folders.

## Effector placement defaults

### `app`

Put here:

- application bootstrap and providers
- router/history creation and startup
- `appStarted`, `appStopped`, global lifecycle
- global Scope/provider wiring
- Next.js `EffectorNext` root/provider adapters
- app-wide route protection composition
- app-wide analytics/i18n/storage pickup orchestration
- integration code that imports multiple business layers

Example:

```txt
app/model/app.model.ts
app/routes/router.ts
app/routes/protected.ts
app/providers/effector-provider.tsx
```

### `pages/<page>`

Put here:

- complete route/screen UI
- page-specific orchestration
- `pageStarted`, route params, page filters/sorting/pagination
- route-specific data loading composition
- page-only queries/mutations that are not reusable elsewhere
- page-level error/loading/redirect state

Example:

```txt
pages/users/route.ts
pages/users/model/page.model.ts
pages/users/api/users-page.query.ts
pages/users/ui/users-page.tsx
```

### `widgets/<widget>`

Put here only when the block is large, self-contained, and reused or independently meaningful.

Examples:

```txt
widgets/sidebar/
widgets/user-card-list/
widgets/checkout-summary/
```

Do not create a widget for every small card, form, or one-page block.

### `features/<user-action>`

Put here:

- user actions and business capabilities
- submit forms for actions
- action-specific mutations
- action-specific validation and UI
- events such as `formSubmitted`, `profileUpdated`, `loginSubmitted`

Good feature names:

```txt
features/session-login
features/session-logout
features/profile-update
features/comment-create
features/order-cancel
```

Bad feature names:

```txt
features/open-modal
features/set-search
features/button-click
features/use-form
```

### `entities/<domain-entity>`

Put here:

- domain object types/contracts/mappers
- reusable entity stores and derived facts
- reusable entity read queries
- entity visuals that do not orchestrate features/pages
- domain-specific local helpers

Examples:

```txt
entities/user/model/user.contract.ts
entities/user/model/user.mapper.ts
entities/user/api/user.query.ts
entities/user/ui/user-avatar.tsx
entities/session/model/session.model.ts
```

Entities must not import features, widgets, pages, or app.

### `shared`

Put here only domain-independent foundation:

```txt
shared/api/base-url.ts
shared/api/errors.ts
shared/api/http.ts
shared/config/env.ts
shared/ui/button.tsx
shared/lib/date/format-date.ts
shared/i18n/index.ts
shared/routes/index.ts
```

`shared` must not know `user`, `session`, `order`, `profile`, `dashboard`, or product-specific workflows.

## Farfetched placement defaults

- Reusable read by domain: `entities/<entity>/api/*.query.ts`
- User action write: `features/<action>/api/*.mutation.ts`
- Page-only list/load: `pages/<page>/api/*.query.ts`
- Base URL, generic request helpers, generic error mapper: `shared/api/*`
- Contract for domain object: owning entity or action/page if page/action-specific
- DTO mapper: near the contract/operation owner
- Auth/session refresh barrier that imports session domain: `entities/session` or `app`, not `shared`
- Pure transport retry/barrier helper with no domain imports: may be in `shared/api`
- Applying a global barrier to operations from multiple layers: `app` integration module

Strict rule: `shared/api` may contain transport infrastructure, but must not import `entities/session` or open routes. If a barrier updates session state or uses session contracts, it is not shared.

## Routing placement defaults

- Domain-neutral route path declarations: `shared/routes`
- Atomic Router router/history configuration: `app/routes`
- Protected route composition used globally: `app/routes/protected.ts`
- Page-owned route: `pages/<page>/route.ts`
- Route params -> data load orchestration: `pages/<page>/model/page.model.ts`
- Redirect policy that coordinates auth/session and pages: `app/routes` or page route model

Do not hide routing decisions in React `useEffect` or shared API modules.

## Next.js placement defaults

FSD `app` and `pages` conflict with Next.js framework folders. Prefer the official FSD recommendation: keep framework folders at project root and rename FSD layers to `_app` and `_pages`.

```txt
app/                         # Next.js App Router
  users/[userId]/page.tsx    # thin adapter
src/
  _app/                      # FSD App layer
  _pages/user/               # FSD Pages layer
  widgets/
  features/
  entities/
  shared/
```

Next App Router page adapter:

```tsx
// app/users/[userId]/page.tsx
export { UserPage as default } from '@/_pages/user';
```

For Effector SSR/RSC, framework route files may create a Scope, call `allSettled(pageStarted, { scope, params })`, serialize it, and render the FSD page public API. Do not let framework route files become business models.

Use `index.server.ts` when a slice must expose server-only modules separately from client-safe public API.

## Review priority

When reviewing FSD + Effector code, look first for:

1. Upward imports and same-layer cross-imports.
2. Direct imports from another slice internals.
3. `shared` containing business domain code.
4. Features named after technical UI events instead of user actions.
5. Page-specific orchestration leaking into features/entities/shared.
6. Entities importing features/pages/app.
7. Farfetched contracts/queries/mutations placed in global buckets.
8. Auth barriers in `shared` importing session entities or routing.
9. Next.js framework folders swallowing the FSD application structure.
10. Models split by `stores.ts/events.ts/effects.ts` instead of responsibility.

## Required references

Before giving a detailed answer, consult the relevant files:

- `references/00-source-policy.md`
- `references/01-core-rules.md`
- `references/02-effector-placement.md`
- `references/03-layer-recipes.md`
- `references/04-routing-nextjs.md`
- `references/05-farfetched-placement.md`
- `references/06-public-api-imports.md`
- `references/07-review-checklist.md`
- `references/08-anti-patterns.md`
- `references/09-migration-playbook.md`
- `references/10-tooling.md`
- `references/11-effector-audit-ownership.md`

## Default answer style

Be decisive on placement. Show a small tree and import examples.

When several placements are possible, choose the strict FSD default first, then list exceptions.

Do not over-scaffold. Prefer the smallest structure that preserves ownership and dependency direction.
