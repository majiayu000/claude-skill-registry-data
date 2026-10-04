---
name: test
description: Audit and harden tests after /work and before /docs. Reads the linked issue architecture, changed files, commits, diff, and existing tests; derives an edge-case test matrix; adds only missing tests; runs the tightest verification loop; commits test-only changes; hands off to /docs.
---

# /test

Before rendering user-facing output, read `../_shared/plain-output.md`.

Harden the completed work with tests before a PR is opened.

This skill is a workflow gate. It compares what `/work` built against the locked issue architecture and asks: "What behavior could still be wrong even if the happy path passes?"

Do not redesign production code. Do not hide failing tests. Do not use broad snapshots as a substitute for behavioral assertions.

Usage: `/test <issue#>` or `/test` when the issue can be discovered from commits.

## Preconditions

- `/work` has completed or the current branch already contains implementation commits.
- Current branch is not `main`, `master`, or `trunk`.
- Working tree is clean before audit. If dirty, stop and ask the user to commit, stash, or confirm those changes are part of the test pass.
- `gh` is authenticated when issue context is needed.
- A linked issue exists through one of:
  - explicit `/test <issue#>`
  - recent commit body with `Refs #<n>`, `Fixes #<n>`, or `Closes #<n>`
  - branch name containing an issue number

## Process

### 1. Load the contract

Collect:

```bash
gh issue view <n> --json number,title,body,url,state
git status --short
git log --oneline origin/main..HEAD
git diff --stat origin/main...HEAD
git diff origin/main...HEAD
```

If the base branch is not `main`, use the PR target branch or the issue's known base.

Read changed production files and nearby tests. Use `rg --files` and repo conventions to find test files. If framework behavior matters, inspect installed package source or official docs before writing tests.

### 2. Derive the test matrix

Create a small matrix from the issue architecture and actual diff:

```markdown
| Behavior | Risk | Existing proof | Missing test |
|---|---|---|---|
| <observable behavior> | <failure mode> | <test or none> | <test to add or none> |
```

Cover these edge-case classes when relevant:

- boundary inputs: empty, min, max, malformed, duplicate, unknown, nullish
- lifecycle states: initial, active, retrying, cancelled, completed, failed
- error paths: typed errors, adapter failures, validation failures, permission failures
- idempotency: repeated commands, retries, duplicate events, replay
- concurrency: races, ordering, cancellation, partial completion
- persistence: missing rows, stale rows, migration compatibility, rollback shape
- external I/O: timeouts, rate limits, pagination, webhook retries, bad responses
- security: authorization, least privilege, input confusion, data leakage
- observability: logs, metrics, audit events, failure visibility
- regressions: the bug or drift that originally motivated the issue

Only add tests that prove observable behavior or protected invariants. Do not test private implementation details unless the repository already treats that boundary as public.

### 3. Add missing tests

Edit only test files, fixtures, and minimal test helpers.

Allowed:

- new tests for changed behavior
- fixtures needed by those tests
- small test helper changes when they reduce duplication and match repo style

Forbidden:

- production code changes
- broad refactors
- snapshots without focused assertions
- skipped tests as proof
- weakening assertions to pass
- deleting tests unless they are replaced by stronger boundary tests

If a missing test reveals a production bug, stop after recording the failing test and evidence. Do not patch production code inside `/test`; hand back to `/work` or `/debug`.

### 4. Run proof

Run the tightest verification available, strongest first:

1. New/changed tests only.
2. Relevant integration or end-to-end test.
3. Full package test command.
4. Type-check or lint only when runtime tests are not available.

Record exact commands and outcomes.

If tests fail because the implementation is wrong, stop and report the failing command and exact error. If tests fail because the test is wrong, fix the test and rerun.

### 5. Commit test-only changes

If tests were added or changed:

```bash
git add -- <test-paths-and-fixtures-only>
git commit -m "test: cover #<issue> edge cases"
```

Do not stage production files. If no tests were missing, do not commit.

## Output

Use Plain Senior output:

````markdown
## Decision
Tests hardened, or no missing tests found.

## Why
- issue=<issue url>
- missing_tests_added=<n>
- highest_risk_case=<case or "None known">

## Example
```bash
<most important test command run>
```

## Proof
- <command> -> <result>
- <command> -> <result>

## Risk
<uncovered edge, failing production behavior, or "None known">

## Next
Run `/docs` to update required documentation before opening the pull request.
````

Then end with exactly this line and stop:

> Tests hardened. Run `/docs` to update required documentation.

If a production bug is exposed, do not print the handoff. End with:

> Tests exposed a production failure. Run `/work` or `/debug` to fix it before `/pr`.
