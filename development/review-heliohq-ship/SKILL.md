---
name: review
version: 0.2.1
description: >
  Static code review of the active diff: trace changed paths and report concrete
  P1/P2/P3 correctness, security, or spec bugs with file:line evidence. Use for
  code review or bug checks. Not runtime QA.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Write
  - AskUserQuestion
---

# Ship: Review

This file is an operating contract for an AI reviewer.

## Mission

1. Find real bugs in the active change scope.
2. Report findings first, ordered `P1`, then `P2`, then `P3`.
3. Add a short diagnosis only if multiple findings share one root cause.

## Red Flag

**Never:**
- Report a bug before understanding the changed code path
- Read only diff hunks — read full changed files
- Report a concern without `file:line` and trigger
- Report style nits, refactor wishes, or use `B1`/`B2` severity
- Ignore staged or unstaged work in standalone mode
- Lead with philosophy instead of findings
- Force a diagnosis when findings don't share one root cause
- Write a vague "looks good" report with no evidence trail

## Valid Findings

Report only issues that meet at least one of these:

- violates the spec or acceptance criteria
- causes broken behavior or a runtime error
- causes data loss, partial writes, or inconsistent state
- creates a security or trust-boundary vulnerability
- breaks callers, consumers, or shared interfaces after a change
- lets tests pass while the real behavior is still wrong

A finding without a traced code path or concrete observation is not a
valid finding.

Do not report:

- style preferences
- naming opinions
- speculative future concerns
- unrelated refactor ideas
- missing comments

## Severity

| Label | Use when |
|------|----------|
| `P1` | ship-stopping correctness failure, security issue, data loss, or major regression |
| `P2` | real bug or spec deviation with narrower scope or blast radius |
| `P3` | concrete lower-impact bug or edge-case failure |

`P3` is still a real bug. It needs the same evidence standard as `P1`
and `P2`.

## Context

Use the smallest possible setup contract:

- `spec`: caller-provided, else `<task_dir>/plan/spec.md` if it exists
- `task_dir`: caller-provided, else `.ship/tasks/ad-hoc-review-<branch>`
- `scope`: the active change scope = `<base>...HEAD` plus any staged or unstaged worktree changes

If there is no spec, do a diff-only review and say so explicitly.
If there are no changes, write a short clean report and stop.

## Procedure

### 1. Resolve the review scope

Resolve `<base>` first — not every repo has `origin/HEAD` set:

```bash
BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
[ -z "$BASE" ] && BASE=$(git rev-parse --verify origin/main >/dev/null 2>&1 && echo main || echo master)

git diff "$BASE"...HEAD --name-only
git diff --cached --name-only
git diff --name-only
```

Use the union of those file lists as the review scope in both pipeline
and standalone mode. In a clean worktree, the staged and unstaged lists
are empty.

### 2. Read the spec first

If a spec exists:

- extract the acceptance criteria
- note required behavior and edge cases
- keep that checklist in mind while reviewing

If no spec exists:

- continue with diff-only review
- say "Spec unavailable; reviewed against code and diff only"

### 3. Investigate the changed code path

Before writing any finding, understand:

- what changed
- what the code is trying to do
- which path fails and why

For every changed file:

1. Read the full file
2. Read directly affected callers and consumers when needed
3. Trace cross-file effects when types, interfaces, or shared constants changed
4. If a potential bug is unclear, keep tracing until you can prove or disprove it

Do not infer behavior from names, comments, tests, or the spec alone.
Do not stop at the first bug. Review the full scope before finalizing.

### 4. Look for bugs systematically

Check for:

- spec violations
- runtime errors and unchecked null or undefined paths
- missing error handling at system boundaries
- race conditions and shared mutable state hazards
- data integrity bugs around multi-step writes
- security and trust-boundary issues
- forgotten enum arms or stale consumers
- tests that assert the wrong thing
- reward-hacking style shortcuts that pass tests while violating task intent
- fixture-coupled branches, hardcoded expected values, or harness edits that only exist to satisfy the current checks
- cross-file inconsistencies from partial updates

### 5. Rank findings

Rank findings `P1`, then `P2`, then `P3`; within a bucket, order by user
impact. Never use `B1`, `B2`, or any non-severity numbering scheme.

### 6. Diagnose only if it helps

After collecting all findings, ask whether several findings share one
structural deficiency, for example:

- validation responsibility is distributed instead of enforced at the boundary
- shared mutable state has no ownership model
- multi-step writes have no transaction boundary
- duplicated logic drifted across files
- tests are coupled to implementation details instead of behavior

If one clear root cause explains multiple findings, add a short
diagnosis after the findings. Otherwise omit diagnosis.

## Output

Write to `<task_dir>/review.md`.

`review.md` is freeform. Favor concise, actionable review notes over a
rigid template. Findings come first. Open questions come after findings.

Each finding must include: severity (`P1`, `P2`, or `P3`), short title,
`file:line`, trigger or concrete observation, impact, and fix direction.

Example:

```markdown
# Code Review

## Findings

### P1: Missing transaction around user write and audit write
- File: `src/services/createUser.ts:48`
- Trigger: user insert succeeds and audit insert fails
- Impact: state becomes inconsistent
- Fix: wrap both writes in one transaction or add rollback

### P2: New enum value is not handled in status mapping
- File: `src/email/status.ts:22`
- Trigger: `DeliveryStatus.Bounced` reaches this switch
- Impact: callers receive the wrong label
- Fix: add the missing enum arm and cover it in tests

## Diagnosis

Persistence responsibilities are split across layers, so every new write
path must remember the same defensive work.
```

## Error Handling

| Condition | Action |
|-----------|--------|
| No spec found | Continue with diff-only review and say so explicitly |
| No changes found | Write a clean report and stop |
| Diff too large (>3000 lines) | Split by subsystem or directory, then merge into one review |
| Some context is ambiguous | Investigate further; if still unresolved, record an open question instead of a bug |
| Cannot read the diff at all | Escalate as blocked |

## Execution Handoff

Output the report card — read the format from `../shared/report-card.md`
(resolved against this skill's base directory, not the working directory):

```
## [Review] Report Card

| Field | Value |
|-------|-------|
| Status | <DONE / FINDINGS / BLOCKED> |
| Summary | <Clean / N findings> |

### Metrics
| Metric | Value |
|--------|-------|
| P1 | <count> |
| P2 | <count> |
| P3 | <count> |

### Artifacts
| File | Purpose |
|------|---------|
| <task_dir>/review.md | Findings with evidence |

### Next Steps
1. **Fix findings** — /ship:dev to fix the reported bugs
2. **QA next (if clean)** — /ship:qa to test the running application
3. **Full workflow** — /ship:auto to handle fixes, QA, refactor, and shipping
```
