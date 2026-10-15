---
name: nextjs
description: Version-aware Next.js rules. Use for ANY work in a project that depends on `next` — routes, pages, layouts, Server Components, Server Actions, data fetching, caching, middleware/proxy, next.config, next/image. Resolves the project's installed Next.js version and router first, then loads only that version's reference.
---

# Next.js (version-aware)

Never write Next.js code from memory of "the latest" version. APIs differ across majors (sync vs async `params`, caching defaults, `middleware` vs `proxy`). Code must match the version this project actually runs.

## 1. Resolve the version (once per session)

- If session context contains `[arsenal] stack:` with `next@<version>`, use it.
- Otherwise resolve it from the package that owns the file being edited (monorepo: nearest `package.json` above that file), in this order:
  1. `node_modules/next/package.json` → `"version"` — installed, authoritative.
  2. Lockfile entry (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lock`).
  3. `dependencies.next` range in `package.json` — use its lowest satisfying major and state that the version is unverified.
- Router: `app/` or `src/app/` → App Router; `pages/` or `src/pages/` → Pages Router; both → follow the router of the file being edited.

## 2. Load exactly one reference

| Installed major | Read |
|---|---|
| 14 | [references/v14.md](references/v14.md) |
| 15 | [references/v15.md](references/v15.md) |
| 16 | [references/v16.md](references/v16.md) |

No matching reference (≤ 13 or ≥ 17): do NOT extrapolate from the nearest file. Read the official upgrade guide for that major (`https://nextjs.org/docs/app/guides/upgrading/version-<major>`, index at `https://nextjs.org/docs/llms.txt`) and the project's existing code, and say the rules came from docs, not a curated reference.

For an API introduced in a later minor than the reference covers, confirm it exists in the installed type definitions (`node_modules/next/*.d.ts`) before using it.

## 3. Rules for every version

- Existing project conventions (router, `src/` layout, data-fetching style, TS/JS) beat generic best practice.
- In `app/`, components are Server Components by default. Add `'use client'` only where state, effects, browser APIs, or event handlers are needed — as deep in the tree as possible, never on a layout by reflex.
- Never import server-only code (DB clients, secrets, `next/headers`) into a `'use client'` module. Only `NEXT_PUBLIC_*` env vars reach the browser.
- Treat every Server Action as a public HTTP endpoint: validate input and check authorization inside the action.
- Do not upgrade `next`/`react` or run codemods unless the task asks for it.
- Verify with the project's own scripts: type check first; run `next build` when routing, config, caching, or the server/client boundary changed — it catches errors the type check misses.
