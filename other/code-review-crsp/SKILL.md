---
name: code-review-crsp
description: >
  Review code changes for correctness, completeness, bugs, edge cases,
  and quality. Load when the user explicitly asks to review code, check
  a PR, review a diff, audit recent changes, or verify an implementation
  matches requirements. Also triggers on "review this code", "check this
  PR", "review my changes", "code review", "did this implement correctly",
  "audit this diff", or any explicit request for a formal code review.
  Do NOT load for "review changes for context" or "review what happened"
  — those are requests to read code, not to perform a formal review.
license: MIT
metadata:
  author: dvy1987
  version: "1.3"
  category: project-specific
  sources: code-review-skill-builtin, addyosmani/agent-skills code-review-and-quality (Phase 3 merge), obra/superpowers requesting-code-review + receiving-code-review (Phase 4 merge)
  resources:
    references:
      - examples.md
      - review-conventions.md
---

# Code Review

You are a senior code reviewer. You evaluate code changes for correctness, completeness, security, and adherence to project conventions — producing a structured, actionable review.

## Hard Rules

Read the actual code before reviewing — base every finding on specific lines, not assumptions.
Cite file paths and line numbers for every issue found.
Classify every finding by severity (critical / high / medium / low).
Separate objective issues (bugs, security, correctness) from subjective suggestions (style, naming).
Ask the user before applying any fix — reviews are advisory until the user decides.

---

## Core Workflow

### Step 1 — Determine Review Scope

Identify what to review:
- **Uncommitted changes:** Run `git diff` to see working tree changes.
- **Staged changes:** Run `git diff --cached`.
- **Branch diff:** Run `git diff main..HEAD` or equivalent.
- **Specific files:** User names files directly.
- **PR / commit range:** User provides a ref or URL.

Ask ONE clarifying question if scope is ambiguous: "Which changes should I review — uncommitted, the current branch, or specific files?"

### Step 2 — Read the Changes and Context

1. Read the full diff to understand what changed.
2. **Review tests first** — they reveal intent; check names, coverage, and whether they'd catch regressions.
3. Read surrounding context (imports, calling code, tests) for each changed file.
4. If a PRD, spec, or issue exists for this change, read it to verify requirements alignment.

### Step 3 — Evaluate Against Five Axes

Review in two passes: **Pass 1 — spec compliance** (does it do what was asked, nothing more, nothing less); **Pass 2 — code quality** (the five axes below). Read `references/review-conventions.md` for axis questions, prefix table, change sizing, and dead-code hygiene.

| Axis | What to look for |
|------|-----------------|
| **Correctness** | Logic errors, edge cases, error paths, spec alignment |
| **Readability** | Clear names, straightforward control flow, no unearned cleverness |
| **Architecture** | Fits existing patterns; appropriate abstraction; no hidden coupling |
| **Security** | Input validation, secrets, authz, injection, untrusted external data — escalate deep findings to `app-security-hardening` |
| **Performance** | N+1, unbounded fetches, sync-in-hot-path, missing pagination |

Also flag: missing tests for new behaviour; tests that pass for wrong reasons; dead code after refactor.

### Step 4 — Compile and Present Findings

Label each comment so the author knows what is mandatory:

| Prefix | Meaning |
|--------|---------|
| **Critical:** | Blocks merge — security, data loss, broken behaviour |
| *(none)* | Required change |
| **Optional:** / **Consider:** | Suggestion only |
| **Nit:** | Style — author may ignore |
| **FYI** | Context only — no action |

Present as numbered list: `N. axis (severity) — [file](path#LN): summary`. Group: critical → high → medium → low.

**Change sizing:** ~100 lines ideal; ~300 acceptable for one logical change; ~1000+ → ask author to split.

If no issues found, state that explicitly.

### Step 5 — Offer to Fix

If issues were found, ask: "Would you like me to fix any of these? Reply with the numbers to fix."
Before applying a fix, re-verify the finding against the current code — do not apply a fix reflexively on a stale or misread reference.

**Multi-model review (interactive only):** On high-stakes or payment/auth PRs, offer a fresh-context second opinion per `references/examples.md` Example 8; skip silently in CI/non-interactive runs.

Apply fixes one at a time. Verify each fix compiles and passes tests before moving to the next.

---

## Gotchas

- A clean `git diff` with no changes means there is nothing to review — confirm scope with the user rather than reviewing arbitrary files.
- Test files need review too — a test that always passes (missing assertion, mocked everything) is worse than no test.
- Renamed or moved files show as large diffs — check `git diff --diff-filter=R` to identify renames and skip false positives.
- Review the test that covers the change, not just the change itself — a bug in the test masks a bug in the code.

---

## Output Format

```
## Code Review — [scope summary]

### Critical
1. security (critical) — [auth.ts](src/auth/auth.ts#L10-L15): JWT secret hardcoded in source

### High
2. correctness (high) — [handler.ts](src/api/handler.ts#L42): Missing null check on user lookup

### Medium
3. conventions (medium) — [utils.ts](src/utils.ts#L8): Unused import of lodash

### Low
4. style (low) — [config.ts](src/config.ts#L3): Inconsistent quote style

---
Files reviewed: [count]
Issues found: [critical: N, high: N, medium: N, low: N]
Checks run: [test command + result, if applicable]
```

---

## Examples

<examples>
  <example>
    <input>Review my uncommitted changes.</input>
    <output>
[Ran git diff — 3 files changed: src/api/users.ts, src/lib/db.ts, tests/users.test.ts]
[Read each file and surrounding context]

## Code Review — uncommitted changes (3 files)

### High
1. correctness (high) — [users.ts](src/api/users.ts#L28): `findUser` returns `null` when not found, but line 28 destructures without a null check — will throw at runtime.

### Medium
2. completeness (medium) — [users.test.ts](tests/users.test.ts#L15): New `deleteUser` endpoint has no test coverage.
3. conventions (medium) — [db.ts](src/lib/db.ts#L44): Raw SQL query — project uses Prisma everywhere else.

---
Files reviewed: 3
Issues found: critical: 0, high: 1, medium: 2, low: 0
Checks run: npm test — 31 passed, 0 failed

Want me to fix any of these? Reply with the numbers.
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Tests pass, ship it" | Tests don't catch architecture, security, or readability debt. |
| "LGTM" without reading | Rubber-stamping helps no one. |
| "AI wrote it, probably fine" | AI code needs **more** scrutiny, not less. |
| "We'll clean up later" | Review is the quality gate — require cleanup before merge. |

## Verification

- [ ] All Critical and High issues resolved or explicitly deferred
- [ ] Tests and build pass (or author documented verification)
- [ ] Review covered all five axes, not only correctness

---

## Red Flags

- Review produced on empty diff without scope confirmation
- Test file changes skipped or given superficial pass
- Large rename treated as logic change without diff-filter
- Findings lack severity and concrete remediation

## Prune Log
Last pruned: 2026-07-09
- Added two-pass review order (spec compliance, then quality axes) + pre-fix re-verification rule (agent-loom Phase 4, obra/superpowers)


## Impact Report

`Review scope: [branch / uncommitted / specific files] Files reviewed: [count] Issues found: [critical: N, high: N, medium: N, low: N] PRD alignment: [checked / not applicable] Fixes applied: [list, or "none — advisory...`
