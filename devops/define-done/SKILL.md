---
name: define-done
description: Define acceptance criteria, risk level, and verification before editing. Use at the start of non-trivial implementation or when an issue lacks clear proof of completion.
---

# Define Done

Use this before changing code or docs on non-trivial work.

## Workflow

1. Classify risk: low, medium, or high.
2. Write testable acceptance criteria.
3. Name the minimum verification commands or manual checks.
4. Record known constraints and non-goals.
5. State rollback or recovery notes for medium/high-risk changes.

## Risk Rules

- Low: narrow copy, style, test-only, or isolated bug fix (with no business-rule change).
- Medium: user-visible behavior, business logic, data handling, CI, integrations, or multi-file behavior.
- High: auth, payments, permissions, secrets, migrations, deployment, infrastructure, tenant data, or irreversible operations.

## Test Database Requirement

Follow `system-level/core.md` (Test Database Safety) for what counts as disposable/dedicated storage and when a staging backup is required. Verification commands named in step 3 of the workflow above must satisfy that rule before this skill is considered done.

## Async/Stateful Contract Requirement

For medium/high-risk work that involves queue jobs, background workers, retries, or any record that tracks attempt/state transitions:

- State the retry limit and what happens on exhaustion (fail loudly, dead-letter, alert) — don't leave it implicit.
- Confirm the job or handler is idempotent on retry, or explicitly justify why it doesn't need to be.
- Write a test for at least one failure path (timeout, provider error, partial write), not only the happy path.
- Verify state transitions are correct under retry: a record re-attempted after a partial failure must not silently double-count, skip, or corrupt its tracked state.

## Done Means

- Acceptance criteria satisfied.
- Relevant checks run and named.
- Tests added/updated, or a reason is recorded.
- Independent review completed for non-trivial work.
- Rollout/rollback notes present when risk warrants them.
