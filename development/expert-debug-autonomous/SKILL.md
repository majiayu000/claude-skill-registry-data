---
name: expert-debug-autonomous
description: >
  Runs an autonomous debug cycle: reads linter/TS/test diagnostics, applies fixes
  in priority order, re-checks, and repeats until clean or max iterations. Use when
  the user asks to fix all problems, debug autonomously, fix lint errors, resolve
  diagnostics, or run a full problem-fix cycle in one go.
---

# Expert Debug — Autonomous

Runs a single autonomous cycle that gathers all problems, fixes them in priority order, re-checks, and repeats until clean or limits are hit.

## Workflow

1. **Gather** — Read ReadLints for workspace; run `npm run lint` and `npm test` if available.
2. **Prioritize** — Order by: (a) build-blocking, (b) errors, (c) warnings. Group by file.
3. **Fix** — Apply one fix per edit. Prefer StrReplace for targeted changes.
4. **Re-check** — Run ReadLints on modified files; re-run lint/test.
5. **Loop** — Repeat until: zero errors/warnings, or 5 iterations, or no progress.
6. **Report** — Summarize: files changed, issues fixed, remaining (if any).

## Priority Order

| Priority | Type | Action |
|----------|------|--------|
| 1 | Build/compile errors | Fix first |
| 2 | Linter errors | Fix in file order |
| 3 | TypeScript errors | Fix types/imports |
| 4 | Test failures | Fix tests or code per failure |
| 5 | Warnings | Fix if trivial |

## Safety Limits

- Max **5 iterations** per cycle.
- Stop if **no progress** between iterations.
- Max **20 files** modified in one cycle.
- Ask before destructive changes (delete files, large refactors).

## Fix Strategies

- **cSpell unknown word** → Add to `cspell.json` words/overrides.
- **ESLint** → Apply suggested fix or disable with justification.
- **Missing import** → Add import from correct module.
- **Unused variable** → Remove or prefix with `_`.
- **Type error** → Add type, fix signature, or use `as` only when necessary.

## Trigger Terms

Use when user says: fix all problems, debug autonomously, fix lint errors, resolve diagnostics, run debug cycle, fix everything in one run.

For priority criteria and edge cases, see [reference.md](reference.md).
