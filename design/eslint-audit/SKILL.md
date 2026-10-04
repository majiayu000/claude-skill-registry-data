---
name: eslint-audit
description: ESLint audit and configuration patterns for T3 Turbo projects. Covers flat config setup, custom rule creation, oxlint integration, shared config architecture, and agent-specific ESLint guidance. Use when auditing ESLint config, creating custom rules, or troubleshooting lint errors.
allowed-tools: Read, Glob, Grep
---


# ESLint Audit & Configuration

> On-demand skill for ESLint configs and codebase audits.
> Load with: `@skill eslint-audit`

Three tool classes solve three different enforcement problems — pick by asking which question
applies:

| Question | Tool class | Load |
|---|---|---|
| Can this be a single AST pattern in one package's flat `eslint.config.js` (or its `oxlint` port)? | AST-selector `no-restricted-syntax` / `no-restricted-imports` rule | `references/ast-selector-configs.md` |
| Do I need to scan the whole tree for something too loose for a lint rule (duplicated components, parallel state stores)? | One-shot grep audit script | `references/audit-scripts.md` |
| Am I checking a file-naming convention or a fixed token allowlist (Tailwind theme classes)? | Static naming/token table | `references/naming-and-tokens.md` |

## Thinking Framework

1. **Enforced at commit time, every PR?** → AST selector. These compile into the package's flat
   config and fail CI automatically — use for anything a bad actor could silently reintroduce
   (`ctx.db` access, banned RN globals, fragile e2e selectors, raw SQL outside a transaction).
2. **One-off audit, not CI-enforced?** → grep script. Run on demand during a codebase audit;
   findings are whitelisted per-instance with an inline exception comment (`@ui-exception`,
   `@state-exception`, `@multi-component`) rather than added to the lint config — the violation
   set shrinks over time instead of being re-litigated every commit.
3. **A naming or token-allowlist question?** → the static table. No script needed — compare the
   candidate name/class directly against the table (`@theme-exception` for a deliberate token
   deviation).

`oxlint` shares the same `no-restricted-syntax`/`no-restricted-imports` selector shape as ESLint's
flat config, so a package migrating to oxlint ports the blocks in
`references/ast-selector-configs.md` directly — no rewrite needed.

## Load References

| Working on | Load |
|---|---|
| Per-package AST rule (ctx.db ban, queryOptions enforcement, RN window/document guard, e2e selector ban, oxlint parity) | `references/ast-selector-configs.md` |
| Codebase-wide grep audit (design tokens, component sourcing, state management, file isolation) | `references/audit-scripts.md` |
| File naming conventions, allowed Tailwind theme tokens, Tailwind plugin whitelist | `references/naming-and-tokens.md` |

## Worked Examples (Highlights From `references/`)

Three concrete pieces of knowledge, pulled in-body so the pattern is visible without opening a
reference file — depth on these and every other package/category lives in the `references/`
files above.

**1. CI-enforced AST selector — the `ctx.db` ban (`references/ast-selector-configs.md`,
packages/api).** This is the canonical shape every other AST-selector rule in this skill follows:
a `no-restricted-syntax` selector matching an exact AST pattern, paired with a `message` that
names the fix, not just the violation.

```javascript
{
  rules: {
    "no-restricted-syntax": [
      "error",
      {
        selector: "MemberExpression[object.name='ctx'][property.name='db']",
        message: "Import db directly: import { db } from '@{workspace}/db/client'"
      }
    ]
  }
}
```

Why it exists: `ctx.db` access is the `ctx.db.query` recursion trap — TypeScript's inference
blows up walking the full `ctx` type. Importing `db` directly from `@{workspace}/db/client`
sidesteps the recursion entirely, so the rule fails CI before a router ships the pattern.

**2. Design-token allowlist (`references/naming-and-tokens.md`) — the static-table pattern.**
Not every enforcement question needs a script or a lint rule; some are a direct table lookup:

| Category | Allowed | Forbidden |
|----------|---------|-----------|
| Background | `bg-background`, `bg-primary`, `bg-muted`, `bg-destructive` | `bg-red-600`, `bg-slate-100` |
| Text | `text-foreground`, `text-primary`, `text-muted-foreground` | `text-gray-500`, `text-blue-600` |
| Border | `border-border`, `border-input`, `border-destructive` | `border-gray-200`, `border-red-500` |

A deliberate deviation gets a `@theme-exception` comment rather than a config change — the
exception is visible at the call site, not buried in a shared allowlist.

**3. One-shot grep audit — design-token compliance (`references/audit-scripts.md`).** For
findings too loose for a single AST pattern (scanning an entire tree for a class of violation),
the audit script is a one-shot grep run on demand, not CI-enforced:

```bash
# Find files with arbitrary (non-token) colors
grep -rln "(bg|text|border)-(red|blue|green|yellow|purple|pink|gray)-[0-9]" apps/nextjs/src --include="*.tsx"
```

Findings are whitelisted per-instance with `@theme-exception` inline, not added back into the
lint config — the violation set is expected to shrink over time instead of being re-litigated
every commit.

## NEVER (What Each Rule Family Actually Guards Against)

The inline `message` string on an AST-selector rule tells a developer what to do instead; it does
not explain why the pattern is dangerous. That reasoning, generalized per rule family:

**Base (all projects)**
- **NEVER use `console.error` for error reporting.** It only reaches local stdout — swallows the
  error from Sentry/observability entirely, so on-call never sees it. Use
  `Sentry.captureException()`/`logError()` so the error surfaces where someone is actually watching.
- **NEVER leave a `TODO`/`FIXME`/`XXX`/`HACK` marker in committed code.** It's the No-TODOs iron
  law (`rules/CORE.md`) in lint form — a marker is a silent stand-in for a decision nobody made.
  Implement fully or escalate via beads; don't let the comment do the deferring.
- **NEVER use `any` or an unsafe assignment.** A single `any` breaks the type-sharing contract
  (DTOs flow through `RouterOutputs`) for every downstream consumer, silently — the error surfaces
  three files away from where the `any` actually lives, if it surfaces at all.

**packages/db**
- **NEVER write a raw `sql` tagged template outside `db.transaction()`.** An un-transacted raw
  query loses the atomicity guarantee every other Drizzle write path gets for free — a failure
  mid-query can leave a partial write with no rollback.

**packages/api**
- **NEVER access `ctx.db` in a router or service.** This is the `ctx.db.query` recursion trap —
  TypeScript's inference blows up walking the full `ctx` type. Import `db` directly from
  `@{workspace}/db/client` instead, which sidesteps the recursion entirely.
- **NEVER import `db` inside a procedure body instead of the top of the file.** It hides a heavy,
  module-level dependency behind per-request execution, obscuring the router's real dependency
  graph from anyone scanning the top of the file.

**apps/nextjs**
- **NEVER call `trpc.x.useQuery()`/`useMutation()` directly.** It bypasses the shared
  `queryOptions`/`mutationOptions` wrapper that derives cache keys consistently — two call sites
  for the "same" query that skip the wrapper can silently end up on different cache keys and never
  invalidate together.
- **NEVER use inline `style={{}}`.** It opts that element out of the semantic-token theming
  contract — dark mode and brand/theme swaps apply to Tailwind classes, not inline styles.
- **NEVER hold server-shaped data (`*Query`/`*Data`/`*Response`) in a Jotai atom.** It creates a
  second source of truth alongside React Query's cache — a mutation invalidates the query cache
  but has no reason to know the atom exists, so the atom silently goes stale.
- **NEVER let one component fire 3+ queries and also own mutations.** Mixing read-heavy and
  write-heavy responsibility in one component (STATE.md's display/action split) makes it
  impossible to reason locally about what re-renders on which change.
- **NEVER import `@radix-ui/*`, `class-variance-authority`, or `lucide-react` directly in an app
  package.** Each belongs behind `@{workspace}/ui`'s wrapper — a direct import bypasses the shared
  variant/theming/icon-library layer, so a future primitive- or icon-library swap has to hunt down
  every direct import instead of touching one package.
- **NEVER hand-roll a DTO type under `types/*`.** `RouterOutputs` from `@{workspace}/api` is the
  single source of truth for what the API actually returns — a hand-typed DTO silently drifts the
  moment the router's shape changes, with no compiler error to catch it.

**apps/expo**
- **NEVER hardcode pixel width/height.** React Native runs across device sizes the author didn't
  test on — a hardcoded dimension is the most common cause of layout breakage on a device that
  isn't the simulator.
- **NEVER reference `window`/`document`.** Neither exists in React Native's JS runtime — code
  written from web habit crashes at runtime, not at lint time, unless this rule catches it first.
- **NEVER import `react-dom`/`next/*` in Expo code.** Web-only packages either fail to resolve or
  silently no-op on native — there is no equivalent to fall back to.

**packages/e2e**
- **NEVER use `waitForTimeout`.** A fixed sleep is either too short (flaky) or too long (slow
  suite) — `waitForSelector`/expect assertions wait for the actual condition instead of a guessed
  duration.
- **NEVER select by CSS class, ID, or `:nth-child`.** All three break the moment a stylesheet or
  DOM order changes; `data-testid`/role selectors survive refactors the test was never meant to
  cover.
