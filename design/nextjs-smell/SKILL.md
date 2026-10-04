---
name: frontend-smell
description: >
  Deep-audit TypeScript, React, Next.js (App Router) and frontend-design code for
  smells — patterns that ship but corrode performance, a11y, type safety, bundle size,
  or render correctness. Trigger whenever the user asks to "review my component",
  "audit this page", "why is my Next.js slow", "is this TypeScript any good", "check
  my RSC boundaries", "why is my bundle huge", "is this accessible", "review my
  Tailwind", "look at my React code", "fix my hydration error", or pastes a .tsx /
  .ts / page.tsx / layout.tsx / route.ts / tailwind.config / next.config / CSS module
  and asks for feedback. Also on vague reviews ("thoughts?", "code review pls") when
  the artifact is a frontend file, and on single-concern asks ("is my useEffect
  right?"). Produces a compound-smell report with severity, confidence, effort,
  diff-style fixes, and a prioritised roadmap, optionally driven by Biome / ESLint /
  Knip / tsc / Lighthouse / axe / Stylelint when files are on disk.
---
 
# Frontend Smell Auditor — TypeScript / Next.js / Design
 
Identifies frontend code that ships but rots: type holes, RSC boundary mistakes,
re-render storms, bundle bloat, a11y gaps, design-system drift, dead code.
 
**If files are on disk** → run `scripts/prescan.sh` first (see §Pre-Scan).
**If input is pasted** → skip to §Audit Protocol and analyse inline.
**If a single file/snippet** → still run §Audit Protocol but scope to what's visible
and flag what cannot be checked without the rest of the project.
 
---
 
## How to use this skill
 
1. **Decide input mode** — disk vs pasted vs single-file snippet.
2. **Run the pre-scan** if files are on disk and CLI tools are available. The
   pre-scan is cheap, deterministic, and surfaces smells your eyes will miss
   (unused exports, type errors, dead a11y, bundle outliers).
3. **Walk the Smell Taxonomy** below. Don't try to memorise it — scan the table,
   match signals you actually see, ignore the rest. Confidence > coverage.
4. **Cluster.** If 3+ smells interact, name the cluster — it's more useful than a
   long list of individual gripes.
5. **Write the report** in the §Output Format. Severity, confidence, effort, fix.
6. **Don't moralise.** The goal is a teammate-style review the user can act on,
   not a lecture about React philosophy.
The taxonomy is the substance of this skill. The CLI scripts make it cheaper. The
output format makes it actionable. The why-it-matters notes (§Mental Models) keep
you honest about which smells are real and which are just taste.
 
---
 
## Smell Taxonomy
 
Each smell: **ID · Severity · Detection signal · Compounds with**.
IDs are namespaced: **T**ype, **R**eact, **N**ext, **D**esign, **A**11y, **B**undle,
**P**erf, **S**tyle.
 
### 🔴 CRITICAL — Bugs, data leaks, broken UX
 
| ID | Smell | Signal | Compounds With |
|---|---|---|---|
| T1 | **`any` Escape Hatch** | `any`, `as any`, `// @ts-ignore`, `// @ts-expect-error` without a linked issue/reason | T2, T6 |
| T2 | **Type Lie** | `as Foo` on a value of unknown shape (API response, `JSON.parse`, `localStorage`) — no runtime validation (zod/valibot/arktype) | T1, N4 |
| R1 | **Stale Closure Hook** | `useEffect`/`useCallback`/`useMemo` with deps array that omits a referenced var — common with `setInterval`, event listeners, async fetches | R2, R7 |
| R2 | **Effect Doing Render Work** | `useEffect` that `setState` from props/state synchronously — should be derived state or `useMemo`, not an effect | R1, P1 |
| N1 | **Server Secret in Client Bundle** | `process.env.SOMETHING` (no `NEXT_PUBLIC_` prefix used as if private but read inside `"use client"` file or imported transitively) — or actual API key in a Client Component | N2, B3 |
| N2 | **Boundary Violation** | Server-only API (`db`, `fs`, `headers()`, `cookies()`, server SDK) imported into a `"use client"` component or one of its ancestors after `"use client"` | N1, N3 |
| N3 | **Hydration Mismatch** | `Date.now()`, `Math.random()`, `typeof window`, `localStorage`, `new Date()` rendered in a Server Component or in initial render of Client Component without `useEffect`/`suppressHydrationWarning` strategy | N2 |
| N4 | **Unvalidated Server Action / Route Handler Input** | `formData`/`request.json()` used directly without schema validation — fields trusted as-typed | T2 |
| A1 | **Interactive Element Without Accessible Name** | `<button>`, `<a>`, `<input>` with only icon/image children, no `aria-label`, no visible text, no `aria-labelledby` | A2, A4 |
| A2 | **Click Handler on Non-Interactive Element** | `onClick` on `<div>`/`<span>` with no `role`, `tabIndex`, key handler — invisible to keyboard & SR users | A1 |
| A3 | **Form Field Without Label** | `<input>`/`<select>`/`<textarea>` with no associated `<label>`, no `aria-label`, no `aria-labelledby` | A1 |
 
### 🔴 HIGH — Real cost, real fix
 
| ID | Smell | Signal | Compounds With |
|---|---|---|---|
| T3 | **Boolean Soup** | 3+ boolean props/state for what is really a 1-of-N enum (`isLoading` + `isError` + `isSuccess` + `isIdle`) — should be a discriminated union / state machine | R6 |
| T4 | **Stringly Typed** | `string` where a literal union, enum, or branded type would prevent invalid values (status, role, id) | T2 |
| T5 | **Index Type Without Guards** | `Record<string, T>` accessed as `obj[key]` without checking — `noUncheckedIndexedAccess` is off or being bypassed | T1 |
| T6 | **Optional Chain as Type Safety** | `foo?.bar?.baz?.qux` 4+ deep — masking that the type doesn't actually describe the shape | T1, T2 |
| R3 | **Promoted Subtree** | `"use client"` near the top of a layout/page when only a leaf needs interactivity — drags an entire subtree to the client bundle | N5, B1 |
| R4 | **Key Index Anti-Pattern** | `key={i}` on a list that is reordered, filtered, or has insertions — causes wrong-row state, focus loss, animation glitches | R5 |
| R5 | **Provider Avalanche** | 5+ nested context Providers in `_app`/root layout, each rerendering the whole tree on any change — should be co-located, split, or a state lib | R6, P1 |
| R6 | **State in the Wrong Place** | Local UI state mirrored from server state without invalidation; or server state pushed into context instead of a query lib (TanStack Query, SWR, RSC fetch) | T3, R5, P2 |
| R7 | **Prop Drilling Through Memo Walls** | `memo`/`useCallback`/`useMemo` everywhere "for performance" but reference identity broken upstream → memoisation is a no-op | P1 |
| N5 | **Client-side Data Fetch Where RSC Would Do** | `useEffect(() => fetch(...))` in a Client Component for data that doesn't depend on user interaction — should be a Server Component fetch | R3, P3 |
| N6 | **Layout Reads Cookies/Headers** | `cookies()`/`headers()` called in a `layout.tsx` — opts the entire route subtree out of static rendering / PPR | P3 |
| N7 | **Fetch Waterfall** | Sequential `await fetch` calls with no data dependency between them — should be `Promise.all` or parallel suspense boundaries | P3 |
| N8 | **Cache Key Wrong** | `fetch(url, { cache: 'no-store' })` everywhere "to be safe", or `revalidatePath('/')` after every mutation — cache busted reflexively | P3 |
| N9 | **`<img>` Instead of `next/image`** | Raw `<img>` for non-trivial images — no LCP optimisation, no auto-sizing, no AVIF/WebP | B4, P4 |
| N10 | **Client-Side Routing With `<a>`** | `<a href="/internal">` for in-app nav — full reload, loses router state | — |
| B1 | **Whole-Library Import** | `import _ from 'lodash'`, `import * as Icons from 'lucide-react'`, `import { Button } from '@mui/material'` (vs `@mui/material/Button`) — no tree-shaking | R3, B2 |
| B2 | **Heavy Lib in Client Bundle** | Moment, lodash, Chart.js, Three.js, full markdown parser bundled into a route that renders once — should be `next/dynamic` with `ssr: false` or moved server-side | B1, P4 |
| B3 | **Client Component Imports Server Util** | Util file mixes server (`process.env`, `fs`) and client utilities — entire file ends up client-side, including server logic and any leaked secrets | N1, N2 |
| A4 | **Color-Only Information** | Status conveyed only by colour (red/green dot, red text) — no icon, no text alternative | A1 |
| A5 | **Focus Trap Missing in Modal** | Modal/dialog/dropdown opens but Tab leaves it; no focus return on close; no `Esc` handler | A2 |
| A6 | **Heading Skip / No Landmark** | `<h1>` → `<h4>` jump; or page with no `<main>`, `<nav>`, `<header>` landmarks | A8 |
| D1 | **Design Token Bypass** | Raw hex/rgb (`#3b82f6`, `rgb(59,130,246)`) or magic px values in components when a token (`--color-primary`, `theme.colors.primary`, `bg-primary`) exists | D2 |
| D2 | **Tailwind Class Soup** | 15+ utility classes inline with conditional logic, repeated across components — should be `@apply`, `cva`, or a component | D1, D5 |
| D3 | **Inconsistent Spacing Scale** | Random px values (`mt-[7px]`, `p-[13px]`) bypassing the spacing scale | D1 |
 
### 🟡 MEDIUM — Toil and drift
 
| ID | Smell | Signal | Compounds With |
|---|---|---|---|
| T7 | **`Function` / `object` / `{}`** | Catch-all types instead of `(...args: unknown[]) => unknown` or proper interfaces | T1 |
| T8 | **Enum Where Union Suffices** | TS `enum` (especially numeric) when a string literal union works — runtime cost, awkward iteration | T4 |
| T9 | **Implicit `any` from JS Boundary** | Untyped `.js` import or untyped 3rd-party module declared as `any` via `declare module` | T1 |
| R8 | **Controlled-vs-Uncontrolled Flip** | `value={undefined}` then `value={x}` on the same input — React warns; user-visible bugs in form state | R6 |
| R9 | **Inline Object/Function in Heavy List** | `<List items={items} onClick={() => ...} config={{...}} />` — new identity each render, defeats `memo` on `<List>` | R7, P1 |
| R10 | **Effect Fetch on Mount** | `useEffect(() => fetch(...), [])` for data that should be in a query lib or RSC — no caching, no dedupe, no SSR | N5, P2 |
| N11 | **`use client` in Every File** | More than ~60% of `app/` files are `"use client"` — RSC benefits forfeited | R3 |
| N12 | **Server Action Without `revalidate`** | Mutation in a server action that returns success but never invalidates the cache it just made stale | N8 |
| N13 | **Loading.tsx Wrapping Whole Route** | Single `loading.tsx` at route root for a page that has independent slow + fast sections — should split into multiple `<Suspense>` boundaries | N7 |
| N14 | **Metadata in Wrong File** | `export const metadata` in a Client Component file (gets ignored) or duplicated across layout & page | — |
| N15 | **Missing `"server-only"` / `"client-only"`** | Files containing secrets/server logic with no `import 'server-only'` to hard-fail accidental client imports | N1, N2 |
| B4 | **No Image Sizing** | `<Image>` or `<img>` without `width/height` or `fill` + parent sizing — CLS hit | A6, P4 |
| B5 | **No Font Optimisation** | `<link rel="stylesheet" href="fonts.googleapis...">` instead of `next/font` — render-blocking, FOIT/FOUT | P4 |
| B6 | **Barrel File Bloat** | `src/components/index.ts` re-exporting everything; tree-shaking depends on bundler heroics; circular import risk | B1 |
| P1 | **Premature Memoisation** | `useMemo`/`useCallback`/`memo` on trivial values/components with no measurable render cost | R7 |
| P2 | **Re-fetch Storm** | Same endpoint hit by 3+ components on the same render with no shared cache/dedupe | R6, R10 |
| P3 | **Non-Streaming Critical Path** | Whole page blocks on the slowest fetch when a streaming `<Suspense>` fallback would unblock the shell | N7, N13 |
| P4 | **Image / Video Without Lazy Strategy** | Below-the-fold media without `loading="lazy"`, `priority` (for LCP), or sizing | N9, B4 |
| A7 | **Decorative `alt` Wrong** | `<img>` with `alt="image"` / `alt="photo"` / no `alt` for content imgs; or content `alt=""` for decorative | A1 |
| A8 | **Tab Order Surprises** | `tabIndex={1}`-`tabIndex={5}` (positive values), or `outline: none` without a replacement focus style | A5 |
| A9 | **Link Text "Click Here"** | Link text out of context (`click here`, `read more`, `here`) repeated across page — SR rotor noise | — |
| D4 | **Component Variant Explosion** | Component with 8+ boolean variant props instead of a typed `variant` enum + `cva`/recipes | T3, D2 |
| D5 | **Inconsistent Import of Same Component** | `Button` from `@/ui/button`, `@/components/Button`, `@/lib/Button` across the codebase — partial migration, drift | B6 |
| D6 | **Dark-Mode Drift** | Some components support dark mode via `dark:` / tokens, others hardcode light values | D1 |
| S1 | **CSS Specificity War** | `!important` 3+ times in a file; selectors with depth > 3; resetting your own framework | D1 |
| S2 | **Z-index Lottery** | `z-[9999]`, `z-[99999]`, `z-[100]` scattered — no documented stacking layer scale | S1 |
 
### 🟢 LOW — Noise / mild drift
 
| ID | Smell | Signal | Compounds With |
|---|---|---|---|
| T10 | **Type Aliases for Primitives Without Branding** | `type UserId = string` with no `__brand` — cosmetic only, doesn't prevent mixing IDs | T4 |
| T11 | **Unused Generics** | `function f<T>(x: string): string` — `T` not used | — |
| R11 | **`useState` Initialiser Recomputed** | `useState(expensiveFn())` instead of `useState(() => expensiveFn())` | P1 |
| R12 | **Forwarded `ref` Missing** | Reusable input/button doesn't forward ref → can't be used by libraries needing focus/anchor refs | — |
| N16 | **Duplicate `<head>` Content** | Same meta tags in layout and page metadata exports | N14 |
| B7 | **Unused Polyfill / Legacy Browser Target** | `core-js` / IE shims / `target: 'es5'` in a project where browser baseline is modern | — |
| D7 | **Magic Breakpoints** | `@media (max-width: 763px)` rather than the design scale (`md`, `sm`) | D3 |
| D8 | **Inline Styles for Static Values** | `style={{ marginTop: 16 }}` for values the design system already names | D1 |
| S3 | **Vendor Prefix Soup** | Hand-written `-webkit-`, `-moz-` for properties autoprefixer/Lightning CSS handles | — |
| L1 | **Console Survivor** | `console.log` left in production code (>2 instances) | — |
| L2 | **TODO/FIXME Without Owner** | `// TODO` with no name, ticket, or date | — |
| L3 | **Commented-Out Code Block** | 5+ lines of commented-out JSX/TS — git remembers, files don't have to | — |
 
---
 
## Compound Smell Clusters
 
When 3+ smells interact, name the cluster. It's more memorable than a flat list.
 
| Severity | Smells | Cluster | What's actually happening |
|---|---|---|---|
| 🔴 | T1 + T2 + N4 | **Trust Fall** | `any`/`as` plus unvalidated server input — your types are decorative, runtime can be anything |
| 🔴 | R1 + R2 + R10 | **Effect Soup** | Effects doing render work, with stale closures, fetching on mount — every interaction triggers cascading re-runs |
| 🔴 | N1 + N2 + B3 | **Boundary Bleed** | Server logic & secrets imported into the client tree because util files mix concerns |
| 🔴 | R3 + N11 + B2 | **Client-First Next.js** | `"use client"` near the root, heavy libs bundled, RSC benefits forfeited — Next.js as an SPA |
| 🟡 | A1 + A2 + A3 + A5 | **Keyboard-Hostile UI** | Built for mouse users; SR users get nothing, keyboard users get traps |
| 🟡 | D1 + D2 + D3 + D6 | **Design System Drift** | Tokens exist but half the codebase ignores them — design rebrand will be a multi-week migration |
| 🟡 | R7 + P1 + R9 | **Memo Theatre** | `memo`/`useCallback`/`useMemo` everywhere; new object/function identities upstream make all of it a no-op |
| 🟡 | N7 + P2 + P3 | **Waterfall Architecture** | Sequential awaits, duplicate fetches, no streaming — TTFB is a server problem you've made worse |
| 🟢 | T10 + T11 + L2 | **Cosmetic Cleanliness** | Looks tidy, doesn't prevent any actual class of bug |
 
---
 
## Audit Protocol
 
### Phase 0: Pre-Scan (files on disk)
 
If files are on disk and Node is available, run the bundled pre-scan. It runs the
right CLI tools in the right order, with sensible defaults, and prints a digest.
You don't have to use everything it returns — pick the signals that show up.
 
```bash
bash scripts/prescan.sh <project-root>
```
 
What it does, and what each signal tells you:
 
| Tool | What it catches | Maps to smells |
|---|---|---|
| `tsc --noEmit` | Type errors, missing exports, contract drift | T1, T2, T9 |
| **Biome** (`biome check`) or ESLint (`eslint --max-warnings=0`) | Lint, a11y rules, RSC rules, hooks deps | R1, R2, R4, A1, A2, A3, N2 |
| `knip` | Unused files, exports, deps, types | B6, L3, D5 |
| `eslint-plugin-react-server-components` (or Biome's `useExhaustiveDependencies` + `noClientInServer`) | RSC boundary violations | N2, N15 |
| `eslint-plugin-jsx-a11y` (or Biome a11y group) | A11y rules at lint time | A1–A9 |
| `stylelint` | CSS smells, specificity, `!important` overuse | S1, S2, D7 |
| `next build` (analyze) + `@next/bundle-analyzer` | Per-route bundle size, duplicate deps | B1, B2, B5, B6 |
| `lighthouse` / `lhci autorun` | LCP, CLS, accessibility score, unused JS/CSS | A1+, B2, P3, P4 |
| `pa11y` / `axe` (CI) | Runtime a11y issues a static linter can't see | A1–A9 |
| `depcheck` (fallback if `knip` not available) | Unused/missing deps | B6 |
| `madge --circular` | Circular imports | B6, B3 |
 
The script will skip any tool that isn't installed and report which it ran. You
can run individual tools yourself — see `scripts/prescan.sh` for exact commands
and `references/cli-cheatsheet.md` for one-liners.
 
> **Don't gate on tool availability.** If only `tsc` runs, that's still useful.
> If nothing runs, fall back to inline reading. The taxonomy is the skill; the
> tools are an accelerant.
 
### Phase 1: Read with intent
 
Open the entry points first: `app/layout.tsx`, `app/page.tsx`, `next.config.{ts,js,mjs}`,
`tsconfig.json`, `package.json`, `tailwind.config.*` (or `app/globals.css` for v4).
Then dive into the file(s) the user asked about.
 
For each file, ask in this order:
 
1. **Boundary** — server or client? Why? Is the directive at the right level?
2. **Types** — does the type describe reality, or is it `any`/`as`/optional-chain
   theatre?
3. **Effects** — what side effects exist, are deps honest, is render work happening
   in `useEffect`?
4. **State** — local vs server vs URL vs context — is it in the right place?
5. **A11y** — can a keyboard-only user do everything a mouse user can?
6. **Bundle** — what does this file pull into the client?
7. **Design** — tokens or magic values? Variant prop or boolean explosion?
8. **Dead** — is anything here unreferenced, commented out, or shimming a feature
   that shipped?
This order matches the severity gradient: a boundary mistake leaks secrets, a
dead-code smell wastes a few KB. Triage accordingly.
 
### Phase 2: Cluster
 
Before writing the report, ask: do any 3+ findings tell a single story? If so,
lead with the cluster, then list the contributing smells under it. A reader who
sees "Effect Soup" once will remember it; a reader who sees R1, R2, R10 in
isolation won't.
 
### Phase 3: Write the report (see §Output Format)
 
---
 
## Mental Models
 
These are the "why" behind the taxonomy. Use them to calibrate severity and to
push back on the user when they want to fix the wrong thing first.
 
### Boundaries are physical, not stylistic
`"use client"` isn't a code-organisation choice — it's a promise to the bundler
that everything reachable from this file (statically) ships to the browser. The
single highest-leverage Next.js smell is putting `"use client"` higher than it
needs to be. Move it down to the leaf, lift static content into Server Components,
and pass them as `children`. (See `references/nextjs-rsc.md`.)
 
### Types describe reality, or they don't
A type is a runtime contract only at the boundary where data enters your program
(network, storage, env, user input). Inside the boundary, types are static. So
`any` deep inside is a smell, but `any` at the boundary plus a runtime validator
is correct. The fix for T1/T2 is almost always "validate at the boundary with
zod/valibot/arktype, infer the type from the schema."
 
### Effects are escape hatches, not glue
React's mental model is: render is a pure function of props + state; effects
synchronise with external systems. Anything else is a smell. Computing derived
values in `useEffect` (R2) is the most common version — the fix is usually a
plain expression or `useMemo`.
 
### Memoisation costs nothing only if it's free
`memo`, `useCallback`, `useMemo` cost a comparison and a closure allocation. If
you don't measure, you don't know if it's a win. The default should be "no
memoisation" — and you reach for it when you have a profiler trace, not a vibe.
 
### A11y automation catches 30–40%
Lint rules and axe will catch missing `alt`, missing labels, role/handler
mismatches. They will not catch logical reading order, focus return, screen
reader naming quality, modal traps, motion preferences. So when you report A1–A9
findings from tooling, also flag what the tooling can't see.
 
### The bundle is the contract with the user
Every byte you ship is a tax on the user's network, battery, and CPU. Bundle
smells (B1–B6) are not "performance polish" — on mobile/3G, they're correctness.
 
---
 
## Output Format
 
Use this exact structure. It scans well in a chat or PR comment and is easy to
copy into an issue tracker.
 
```markdown
# Frontend Smell Audit: <project / file>
 
## TL;DR
<2–4 sentences. The headline finding. If there's a cluster, name it.>
 
## Cluster: <name> 🔴/🟡  (omit this section if no cluster)
<one paragraph: what's actually happening, why it matters, what fixing it unlocks>
 
## Findings
 
### 🔴 <ID> · <Smell name> · confidence: <high|med|low> · effort: <S|M|L>
**Where:** `path/to/file.tsx:42`
**What:** <1–2 sentences, concrete>
**Why it matters:** <1 sentence — bundle bytes, user impact, bug class>
**Fix:**
```diff
- bad code
+ good code
```
<short note on tradeoffs / migration if non-obvious>
 
### 🟡 <ID> · ...
<repeat>
## What I couldn't check
<files not provided, runtime checks not run, types not resolvable, etc.>
 
## Refactor roadmap
1. **Today (<1h):** <smallest, safest, highest-leverage fix>
2. **This week:** <medium-effort fixes, usually a cluster>
3. **Backlog:** <speculative or large refactors>
```
 
### Notes on the format
 
- **Confidence** matters because some smells are pattern-matches (high) and some
  need codebase context to be sure (low). Be honest — low-confidence findings
  are still worth raising, just labelled.
- **Effort** is rough: S = single file, M = a few files / one PR, L = touches
  architecture or many files.
- **Diff fixes** are mandatory for 🔴/🟡. If you can't write the fix, downgrade
  confidence and say so. A complaint without a fix is a vibe.
- **Limit** the report to ~10 findings unless the user explicitly asks for
  exhaustive. Lead with severity, then leverage. The 11th finding is rarely the
  one that changes their day.
 
---
 
## When to deviate from the taxonomy
 
The taxonomy isn't doctrine. Two cases where you should ignore it:
 
1. **Project conventions override.** If the codebase has 200 components using
   `index.ts` barrels and the user isn't asking about bundle size, don't lecture
   them on B6. Match the local style unless it's actively causing the problem
   they came in with.
 
2. **Scope respect.** If the user pasted one component and asked one question,
   answer that question first. The full audit goes after, and only if they want
   it. Skill triggering doesn't mean firehose.
 
---
 
## Reference files
 
- `references/nextjs-rsc.md` — RSC/SSR/Client component boundary rules, common
  mistakes, the children-as-props pattern, `server-only` / `client-only`.
- `references/typescript-strict.md` — strict-mode flags, validation libs (zod /
  valibot / arktype), branded types, discriminated unions.
- `references/a11y-checklist.md` — what tooling catches, what it doesn't,
  WCAG-AA quick-reference for components.
- `references/cli-cheatsheet.md` — one-liners for every CLI tool the pre-scan
  uses, plus what the output means.
- `references/design-tokens.md` — Tailwind / CSS-vars / cva / shadcn patterns,
  variant modelling, dark-mode strategy.
 
Read them on demand. Don't load all of them; load what the audit needs.
 
---
 
## Scripts
 
- `scripts/prescan.sh` — runs every available CLI tool in the right order,
  prints a digest. Skips missing tools gracefully.
- `scripts/rsc-boundary-check.mjs` — fast static check for `"use client"`
  files importing server-only modules. Useful when you don't have ESLint
  configured for it.
- `scripts/bundle-suspects.mjs` — greps for known-heavy imports (`lodash`,
  `moment`, full `@mui`, `chart.js`, etc.) in client files and prints
  candidates for `next/dynamic` or replacement.
 
Each script is documented in its header.
