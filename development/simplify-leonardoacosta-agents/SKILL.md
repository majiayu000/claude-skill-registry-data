---
name: simplify
description: >
  Review recently changed code for reuse opportunities, quality issues, and efficiency problems,
  then fix them. Use when: (1) user asks to "simplify", "clean up", or "review" changed code,
  (2) after implementing a feature to check for over-engineering, (3) code smell detection —
  duplication, unnecessary abstractions, dead branches, verbose patterns. Keywords: simplify,
  clean up, refactor, review changes, code quality, over-engineered, duplication, dead code,
  git diff, after feature, reuse, typescript, type assertion, async, barrel export.
  Diff-scoped only (recent changes). For whole-codebase dead code removal, use reducing-entropy.
---


# Simplify

Review changed code for reuse, quality, and efficiency. Fix what you find.

## North Star

Simplification is measured by **cognitive load per line**, not line count. A longer file can be
simpler if each line does exactly one obvious thing.

Before touching anything, ask: *"Will the reader understand this faster after my change?"*
If the answer is no or uncertain — leave it.

## Workflow

### Step 1: Get the diff

```bash
git diff HEAD          # unstaged changes
git diff --staged      # staged changes
git diff HEAD~1        # last commit
```

If user specifies a file or range, scope to that.

### Step 2: Classify each change

For every changed file, mark each section:

| Signal | Fix |
|--------|-----|
| Abstraction used in exactly 1 place | Inline — extraction costs indirection |
| `any` cast or type assertion `as X` | Find the real type; assertion = hidden bug |
| `async` function with no `await` | Remove `async` — misleads callers about cost |
| Generic function signature does less than type implies | Collapse to concrete type |
| `Promise.all([singlePromise])` | Unwrap to single `await` |
| Barrel re-exports something used in only 1 file | Remove from barrel to reduce bundle surface |
| `useEffect` reads state but deps array is empty | Missing dep or wrong abstraction |
| Type guard duplicated across 3+ call sites | Extract to dedicated `isX()` predicate |
| Object spread merging 4+ sources `{...a,...b,...c,...d}` | Explicit `Object.assign` — makes override order visible |
| Comment explains what the code does (not why) | Delete — rewrite code to be self-documenting |
| WHY-comment restates or over-explains what CORE.md's Comment Discipline clause already covers | Trim to one line, or cite the rule/skill/doc instead of expounding |

### Step 3: Efficiency check

- **N+1 queries**: Loop calling DB/API per item → batch with `findMany(ids)` or `Promise.all`
- **Sync in async context**: Blocking call (`fs.readFileSync`, `JSON.parse` on large input) inside async fn → use async variant
- **Redundant fetches**: Same data fetched in sibling branches → hoist above the branch
- **Over-fetching**: `select *` when 2 columns suffice → explicit column selection
- **Unnecessary re-renders** (React): expensive derived value recomputed on every render → `useMemo`

### Step 4: Apply fixes

Make targeted edits — do not rewrite files. Each fix should be independently reviewable.

**Example — inlining a single-use abstraction:**

```typescript
// BEFORE: function used exactly once, adds indirection with no reuse
function buildParams(filters: Filters) {
  return new URLSearchParams(Object.entries(filters)).toString()
}
const url = `/api/events?${buildParams(filters)}`

// AFTER: inline — same logic, zero indirection cost
const url = `/api/events?${new URLSearchParams(Object.entries(filters))}`
```

After fixing, verify:
```bash
npx tsc --noEmit 2>&1 | head -20   # TypeScript
pnpm test --run 2>&1 | tail -20     # Tests (if they exist)
```

## Cut-format (over-engineering report)

When the ask is "what can we delete / is this over-engineered" rather than "fix it", report findings
in the cut-format: one line per finding, location + what to cut + what replaces it. Scannable,
deletion-focused, and distinct from a correctness review.

`L<line>: <tag> <what>. <replacement>.`  (use `<file>:L<line>:` for multi-file diffs)

| Tag | Means | Replacement |
| --- | --- | --- |
| `delete:` | dead code, unused flexibility, speculative feature | nothing |
| `stdlib:` | hand-rolled thing the standard library ships | name the function |
| `native:` | dependency or code doing what the platform already does | name the feature |
| `yagni:` | abstraction with one implementation, config nobody sets, layer with one caller | inline it |
| `shrink:` | same logic, fewer lines | show the shorter form |

Examples:
- `L12-38: stdlib: 27-line email validator class. "@"-check + a confirmation mail is the real validation, 1 line.`
- `L4: native: moment.js imported for one format call. Intl.DateTimeFormat, 0 deps.`
- `repo.ts:L88: yagni: AbstractRepository with one implementation. Inline until a second exists.`

End with the only metric that matters: `net: -<N> lines possible.` If there is nothing to cut, say
`Lean already. Ship.` and stop. Scope is over-engineering ONLY — correctness, security, and
performance route to a normal review pass, not this one. (Adopted from `DietrichGebert/ponytail`,
MIT — recon `docs/recon/ponytail.md`.)

## Intensity

The over-engineering pass runs at three strictness levels, default **full**. Set via the request
("simplify lite", "be ruthless / ultra") — the level changes how hard you push deletion, never the
safety floor.

| Level | Behavior |
| --- | --- |
| **lite** | Name the lazier alternative in one line and let the user pick. Apply nothing unprompted. |
| **full** | The cut-format enforced, shortest reviewable diff, shortest explanation. Default. |
| **ultra** | Deletion before addition; ship the one-liner and challenge whether the requirement itself is needed, in the same response. |

No level simplifies away trust-boundary validation, error handling that prevents data loss, security,
or accessibility — those are never on the chopping block regardless of intensity.

## Communication Protocol

- **1–3 issues**: Fix silently, then summarize what changed and why.
- **4+ issues**: Present findings as a prioritized list first — ask before applying non-trivial changes.
- **Refactor-sized fix** (change touches >20 lines or crosses file boundaries): Stop. Report the scope and ask for confirmation before proceeding.

## NEVER

- **NEVER** rename things just for style — only if the name is actively misleading. Rename diffs flood PRs and erode reviewer trust in the rest of the change.
- **NEVER** add abstraction to "prepare for future changes" — YAGNI. There is no future requirement, only the one you have now.
- **NEVER** split a function that's only called once — extraction creates indirection that isn't paid back without a second call site.
- **NEVER** add error handling where the caller already handles it — double-wrapping hides the original error and adds noise.
- **NEVER** change working tests to match refactored internals unless types force it — tests exist to catch regressions, not to mirror implementation details.
- **NEVER** rewrite files wholesale — targeted edits only. Wholesale rewrites hide real changes in noise.
- **NEVER** fix things not in the diff — scope creep kills reviews and breaks the "one concern per PR" contract.

## Quick Decision

```
Is this code duplicated elsewhere?
  Yes → reuse existing
  No → Is it used in exactly 1 place?
         Yes (abstraction) → inline it — indirection costs more than it saves
         No → leave it

Does this abstraction add cognitive load without saving lines?
  Yes → inline it
  No → keep it

Does this fix make the code faster for the READER?
  No / Unsure → leave it
```
