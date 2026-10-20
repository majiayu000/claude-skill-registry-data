---
name: iru-nextjs-code-one-task
description: >-
  Implement a single task from a Next.js `implementation_plan.md`-style task list — the implementation, its tests,
  and its checkbox update. First detects the project's exact profile at runtime — the installed Next.js major
  (14, 15, or 16), App Router vs Pages Router (or both), whether `cacheComponents` is on (so the version/model
  profile is one of `14`, `15`, `16-prev`, `16-cc`), `src/` layout, `proxy.ts` vs `middleware.ts`, `output`
  mode (`export`/`standalone`), test runner (Vitest or Jest via `next/jest`, plus Playwright), styling approach,
  linter, and any project `AGENTS.md`/`CLAUDE.md` guidance (including the version-matched docs bundled under
  `node_modules/next/dist/docs/`) — then loads only the matching guidance from this skill's own `reference/`
  directory: this catalog's TypeScript agreements plus Next-specific code style, Server vs Client Components, data
  fetching and caching organized by version/model (applying only the detected profile's rules), Server Actions,
  Route Handlers and the proxy, routing and rendering (special files, dynamic segments, `generateStaticParams`,
  SSG/SSR/ISR/PPR and route segment config per model, static-export constraints), metadata and SEO, the Pages
  Router, testing, security, and — for a task that adds or changes a page, component or list — the catalog's UI
  contract mapped onto Next.js (`Screen › Region › Component` decomposition; interactive Client Components fed
  serializable props by Server Components; lists through server pagination or a client `@tanstack/react-virtual`
  virtualizer; Playwright component tests against a standalone Vite gallery plus screen/flow tests against the
  production build, capturing `.ui-screenshots/` across left-to-right/right-to-left × light/dark with axe checks at
  the `.ui-quality.yml` level). Re-checks the current code state, implements exactly what the task specifies
  without changing any route's rendering mode the task didn't ask to change, writes/updates tests (does not run
  them), then — unless it stopped on a blocker — checks off this task's own checkbox in `implementation_plan.md`
  with a "group validation pending" note and reports the files touched, tests written, the expected `next build`
  classification (static/SSG/dynamic/partial) of every route it touched, and any deviation from `reference/`.
  Never runs tests, coverage, quality checks, license headers, or `next build` — those happen once per group in
  `iru-nextjs-code-one-task-group`. Invoke as `/iru-nextjs-code-one-task <task description>`, passing the task's
  own text including its exact `implementation_plan.md` checkbox line(s). The Next.js counterpart to
  `iru-typescript-code-one-task`.
model: sonnet
allowed-tools: Read Edit Write Bash(node -p *) Bash(npm ls *) Bash(pnpm ls *) Bash(yarn why *) Bash(git status *) Bash(git diff *) Bash(git log *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *)
---

# Implement one plan task (Next.js)

Carry out a single task's implementation, tests, and checkbox update in a Next.js project — nothing else. This is
the narrowest execution unit for a `nextjs`-tagged task in the `iru-code` pipeline: `iru-nextjs-code-one-task-group`
calls it once per task in a bucket (possibly many at once, in parallel agents), then runs license headers, TSDoc,
tests, coverage, code quality, `next build`, and Playwright once for the whole bucket.

What makes it different from `iru-typescript-code-one-task`, and why Step 1 is longer:

1. **The same code means different things in different Next.js versions and caching models.** `fetch` is cached
   by default in 14 and not in 15+; `params` is a plain object in 14 and a Promise from 15; `export const
   revalidate = 60` is ISR in the previous model and a build error under Cache Components. Step 1 pins the profile
   so that only one set of rules is applied.
2. **The route's rendering mode is part of the contract.** A stray `cookies()` at the top of a layout turns every
   static route below it dynamic and nothing fails until someone reads the build table. This skill states the mode
   it expects for each route it touched; the group skill checks it against `next build`.

It uses a medium model on purpose: the plan carries the hard reasoning; the Next.js rules live in `reference/`.

## Step 1 — Detect the project profile, then read only the reference material this task needs

Detect each of these once, from the project root (the directory holding `next.config.*`; in a monorepo, the app
package the task names). Don't guess any of them from memory.

1. **Next.js version**: `node -p "require('next/package.json').version"` (falls back to the `next` range in
   `package.json` when `node_modules` is absent — say so in Step 7). Also note the `react` version.
2. **Router**: `app/` or `src/app/` → App Router; `pages/` or `src/pages/` → Pages Router; both → hybrid (each file
   follows the router its directory belongs to). A root `app/` wins over `src/app/`.
3. **Caching model** (App Router on 16): read `next.config.{ts,mjs,js}` for `cacheComponents: true`. Never infer it
   from the scaffold's age — a `create-next-app` 16.4 run may emit it enabled together with
   `partialPrefetching: true`. Also note `output: "export"`/`"standalone"`, `typedRoutes`, `reactCompiler`, and
   any `experimental` keys the task's area depends on (`authInterrupts`, `serverActions`, `taint`).
4. **Profile**: `14` (13.4–14.x), `15` (15.x; note whether it is ≥15.5 for `PageProps`/`RouteContext`/
   `next typegen`), `16-prev` (16 without `cacheComponents`), `16-cc` (16 with it). Pages-Router-only code has no
   caching profile beyond the version. A 15 canary with `experimental.ppr`/`dynamicIO` is `15` plus a flag — report
   it rather than applying `16-cc` rules.
5. **Request interception**: `proxy.ts` (16, export `proxy`) or `middleware.ts` (14/15, export `middleware`; on 16
   a leftover kept for the Edge runtime), next to `app/`.
6. **Test runners**: `vitest.config.*` → Vitest; `jest.config.*` importing `next/jest` → Jest; `playwright.config.*`
   + `@playwright/test` → Playwright e2e (note its `testDir`). Also note where existing tests live.
7. **Styling and lint**: Tailwind (v3 config file vs v4 `@import "tailwindcss"`), CSS Modules, Sass, CSS-in-JS;
   `eslint.config.mjs` (flat, `eslint-config-next`), legacy `.eslintrc` (≤15), or `biome.json`.
8. **Package manager**: `packageManager` field or lockfile.
9. **Agent guidance**: read the project's `AGENTS.md`/`CLAUDE.md` if present. When it carries the
   `create-next-app` block pointing at `node_modules/next/dist/docs/`, those docs match the installed version: for
   the specific API the task uses, `grep -ril` that directory and read the one relevant page — not the whole tree.

Then read `reference/README.md` first — it is short and routes you to the rest — and only what it points at for this
task. The routing, restated:

| Read | When |
|---|---|
| `reference/code-style.md` | **Always.** |
| `reference/server-and-client-components.md` | **App Router, always.** |
| `reference/data-fetching-and-caching.md` | Data reads, caching, revalidation, anything affecting static/dynamic. Read the shared rules + **only the detected profile's section**. |
| `reference/server-actions.md` | Server Actions, forms posting to them, `useActionState`/`useFormStatus`/`useOptimistic`. |
| `reference/route-handlers.md` | `route.ts`, webhooks, BFF endpoints, `proxy.ts`/`middleware.ts`. |
| `reference/routing-and-rendering.md` | New routes/segments/layouts/special files, dynamic segments, `generateStaticParams`, segment config, navigation, `output: "export"` projects. |
| `reference/metadata-and-seo.md` | `metadata`/`generateMetadata`/`viewport`, OG images, sitemap/robots, JSON-LD. |
| `reference/pages-router.md` | The touched code lives under `pages/` — replaces the Server/Client Components file for those files. |
| `reference/testing.md` | The task writes or updates tests — nearly always. |
| `reference/security.md` | Actions, handlers, proxy, sessions/auth, env vars, server data passed to Client Components, headers/CSP, user input. |
| `reference/ui-contract.md` + `reference/ui-implementation.md` | The task adds or changes a page, layout, component, list or other UI. `reference/ui-screenshots.ts` is the shared Playwright helper to copy into the e2e directory's `support/` when the project has none. |

A one-line change inside an existing Client Component is `code-style.md` + `server-and-client-components.md` +
`testing.md`. Don't read the rest speculatively.

If `reference/` is missing (the skill directory was copied without it), proceed with this repository's own
`CLAUDE.md`/`AGENTS.md` conventions and the surrounding code's style, and say so in Step 7 — don't guess at what the
reference would have said.

## Step 2 — Re-check the current code state

Read the actual current content of the file(s) the task touches before editing — other tasks in the same bucket
may be landing concurrently, and "current code state" notes passed in may be stale. For every route the task
touches, also read the layouts above it and the data modules it imports: whether a route is static or dynamic is
decided by the whole tree, not the file you edit.

Note what the surrounding code already does about the things `reference/` has opinions on — where data access
lives, how actions return errors, how tests mock the session, which styling approach is used. The reference is the
default for new code; a file that consistently does something else wins, and the divergence goes in Step 7.

## Step 3 — Implement exactly what the task specifies

Apply the reference files Step 1 selected, for the detected profile only, plus this repository's own
`CLAUDE.md`/`AGENTS.md` conventions where they are more specific. Non-negotiable, because a later gate enforces
them or because getting them wrong is a security defect:

- **Profile-correct APIs.** `await` request APIs and `params` on 15+ (never on 14); two-argument `revalidateTag`,
  `updateTag`, `refresh` only on 16; `'use cache'`/`cacheLife`/`cacheTag` only under `16-cc`; route segment config
  `dynamic`/`revalidate`/`fetchCache`/`dynamicParams` never under `16-cc`; `proxy.ts` vs `middleware.ts` as
  detected. Nothing from `output: "export"`'s forbidden list in an export project.
- **Every Server Action and Route Handler authenticates, validates, and authorizes inside itself** — no reliance on
  a layout, the proxy, or a hidden button. Data modules start with `import "server-only"` (App Router only).
- **No secrets or whole rows cross to the client** — DTOs as props, `NEXT_PUBLIC_` only for genuinely public
  values.
- **`'use client'` on the smallest interactive leaf**, never on a page or layout unless the task requires it.
- **Don't change a route's rendering mode the task didn't ask to change.** Under `16-cc`, request data and
  uncached I/O go inside `<Suspense>`; never add `export const instant = false` to make the build pass unless the
  task says the route may block.
- **Full TSDoc** on every exported symbol (`@param`/`@returns`/`@throws`); a one-line summary for default-exported
  `page`/`layout` components.
- **No `any`, `readonly` by default, named exports** except where Next.js requires a default export.
- **No new runtime dependency and no `next.config` change** unless the task explicitly calls for it — otherwise
  that's a blocker to report (Step 5). Never flip `cacheComponents`, never upgrade Next.

For a task that adds or changes UI, also **decompose first** (`ui-contract.md` §2): write the `Screen › Region ›
Component` tree for what the task touches — inputs, events, visual states, reuse, and for each component whether it
is a Server or a Client Component — and keep it for Step 7. Pages own data and pass DTO props down; interactive
leaves are Client Components emitting typed callbacks; collections are server-paginated or client-virtualized
(`ui-implementation.md`), never an unbounded `map`; styles use logical properties.

Don't add anything the task didn't ask for — no speculative abstractions, no unrelated cleanup, no restyling.

## Step 4 — Write or update the tests

Follow `reference/testing.md` and the existing tests next to the code. Client Components and synchronous Server
Components with React Testing Library; leaf async Server Components by calling them as functions; Server Actions and
Route Handlers called directly with the session, `next/headers`, and `next/cache` mocked — **always including the
anonymous, wrong-owner, and invalid-input cases, asserting no side effects**. Add or extend a Playwright spec only
for a user-visible flow the task adds (a form submit, a redirect, an auth gate) and only if the project already has
Playwright. Keep async Server Components thin so their logic is unit-testable — a page with branching logic and no
unit test is a coverage gap the group skill will send back.

For UI, also write UI tests per `ui-contract.md` §6–§8 and `ui-implementation.md`, if the project has Playwright:
stories for each visual state of every added/changed Client Component (rendered by the gallery), a screen spec for
a changed page against the production build with upstreams faked, and a flow spec for a new flow — all capturing
the `.ui-quality.yml` matrix through the project's `ui-screenshots.ts` helper (created from
`reference/ui-screenshots.ts` if missing, with `@axe-core/playwright` as the one permitted new dev dependency) with
the accessibility check. A project without Playwright: behaviour tests only, and report the gap.

Do not run the tests, the type-checker, or `next build` — `iru-nextjs-code-one-task-group` does, once for the whole
bucket.

## Step 5 — When to interrupt the user

Keep interruptions rare. Stop and use `AskUserQuestion` (or plain text if there's no real choice) only when:

- The task is ambiguous in a way that changes correctness, scope, or **a route's rendering mode** and can't be
  safely inferred (e.g. it asks for per-user content on a page the plan elsewhere expects to stay static).
- The task's approach is infeasible against the real code — it names a route, action, or module that doesn't exist,
  or asks for something the detected profile forbids (a Server Action in an `output: "export"` project,
  `export const revalidate` under `16-cc`). Name the profile rule; don't silently translate it into another API
  unless the translation is mechanical and documented in `reference/` (then do it and report it).
- It needs a new dependency, a `next.config` change, or a new environment variable the task didn't mention.
- The profile detection in Step 1 is genuinely ambiguous (no `node_modules` and a `next` range spanning two majors).

Don't stop merely because the task is nontrivial. Don't report a task done to work around a blocker — report it
blocked (Step 7) with what was tried and why it failed. A conflict between `reference/` and the surrounding code is
not a reason to stop: follow the surrounding code and report the divergence.

## Step 6 — Check off this task's checkbox now

Unless this task stopped on a blocker, update `implementation_plan.md` at the repository root before reporting.
Re-read it fresh (sibling tasks may be editing it concurrently), find this task's own checkbox line by the exact
text passed in, flip `[ ]` to `[x]` for it and for every sub-task completed, and add a short note, e.g. `- [x] Task
2. **Add `addTodo` Server Action** — implemented, tests added; group validation pending.` — the same "pending"
wording `iru-nextjs-code-one-task-group` replaces once it has validated the bucket. Edit only this task's own
line(s). If the task stopped on a blocker, leave its checkbox untouched.

## Step 7 — Report the outcome

Hand control back with a short summary:

- **The detected profile** — Next version, router(s), `14`/`15`/`16-prev`/`16-cc`, `src/` or not, proxy vs
  middleware, `output` mode, unit runner and whether Playwright exists — and the reference files actually read
  (plus any bundled `node_modules/next/dist/docs` page consulted).
- **The files touched** and **the tests added/updated** (not run).
- **For UI work**: the `Screen › Region › Component` decomposition (with Server/Client per component), the stories
  and UI specs added, and the screenshot states they will capture (`<kind>/<Id>/<state>`).
- **Expected route classification** for every route the task added or whose tree it touched, in `next build` terms
  — e.g. `/todos ƒ (reads the session cookie)`, `/posts/[slug] ● (generateStaticParams)`, `/shop ◐ (cookie read
  under Suspense)`, `/api/todos/[id] ƒ`, `/ unchanged ○` — and whether any of them changed mode, and why. Name the
  files that are only reachable through e2e (thin async pages/layouts) so the coverage gate can account for them.
- **Whether this task stopped on a blocker** (Step 5), with enough detail for the caller to surface it.
- **Any deliberate deviation from `reference/`** — matching a file that uses another convention, a profile rule
  translated into its equivalent, a default export Next.js requires — or that `reference/` was missing.

This skill never captures a quality baseline and never runs tests, coverage, linting, type-checking, or
`next build`.
