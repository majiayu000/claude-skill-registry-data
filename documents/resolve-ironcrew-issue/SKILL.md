---
name: resolve-ironcrew-issue
description: Implement one tracked IronCrew `IC-NNN` finding end to end across Rust code, tests, documentation, Lua examples, evaluations, and deployment evidence. Use when the user says to proceed with, fix, resolve, continue, or take the next tracked IronCrew issue or development goal. Do not use for an unrelated untracked change unless the user asks to add it to the ledger.
---

# Resolve an IronCrew issue

## Establish the contract

1. Inspect `git status`, the current branch, and overlapping diffs. Preserve
   all unrelated changes.
2. Read the `IC-NNN` row in `docs/issues/README.md` and the canonical issue page.
   Confirm its status, required outcome, and acceptance criteria against live code.
3. Trace every affected CLI/API entry point, storage backend, doc, Lua example,
   evaluation, and deployment surface. Treat the ledger as a hypothesis until
   current source confirms it.
4. State whether the evidence boundary is unit, default Rust, live PostgreSQL,
   separate process, soak, live provider, Railway, or OpenShift.
5. Before implementation, change an `open` issue to `in-progress`, regenerate
   both indexes, and verify the registry. Leave an already `in-progress` issue
   unchanged.

## Implement

- Write a focused regression that fails for the defect or missing contract
  whenever practical.
- Fix the shared abstraction rather than only one caller. Cover JSON, SQLite,
  and PostgreSQL where the contract applies to all stores.
- Keep new modules at or below 300 lines and never create one above 400. Avoid
  growing legacy oversized modules; extract cohesive responsibilities instead.
- Preserve cancellation, admission ownership, bounded memory/work, secret
  redaction, idempotency, lease fencing, and terminal compare-and-set semantics.
- Update public docs, runnable Lua examples, evaluation contracts, and
  Railway/OpenShift guidance affected by the change.

Do not broaden the issue into unrelated cleanup. Record newly confirmed,
independent defects as separate ledger candidates. If the user authorizes a new
record, allocate the next never-used ID after `docs/issues/HIGH_WATER_MARK`,
advance the marker in the same change, and never lower it or delete history.
The registry compares against `HEAD` locally and the trusted PR/push base in CI;
do not bypass that temporal check when pages are renamed or retired.

## Validate

1. Run focused tests while iterating, including negative, concurrency,
   cancellation, and resource-boundary cases appropriate to the issue.
2. Finish Rust work with formatting, exact all-target Clippy, and all-target tests.
3. Use freshly pulled `postgres:latest` with `IRONCREW_TEST_PG_URL` when the issue
   touches shared storage or replica behavior. A skipped test is not evidence.
4. Validate Lua examples when the runtime, docs, tools, crew DSL, or examples change.
5. Before closing the issue, use `$check-ironcrew` for every affected gate,
   including the replica soak whenever readiness, leases, lifecycle, routing,
   or shared-journal behavior changed.
6. Use the complete local `$check-ironcrew` gate before a requested commit/push,
   branch integration, or release preparation, then require platform CI before
   merge or tag.

## Close the ledger

Only after the required gates pass:

- set the detailed entry to `resolved` with a valid ISO date;
- replace `## Required outcome and acceptance` with
  `## Outcome and validation`, preserving the original requirement context;
- document cause, implementation, focused coverage, contract boundary, exact
  validation evidence, and commit/PR/deployment identifiers only when they exist;
- run `bun run scripts/issues_registry.ts generate` followed by the matching check;
- run `bun run scripts/check_worktree.ts` and `git status --short`; review the
  complete issue-scoped tracked and untracked diff;
- report remaining risks without upgrading local evidence to platform proof;
- propose no more than three prioritized, bounded next development goals.
