---
name: kanban-test
description: 'Test a kanban feature against its approved test plan or a bug against reproduction and regression scope. Write current-execution results with PASS/FAIL/REJECT/BLOCKED. Use in testing.'
---

# Kanban Phase 4 — Testing (Autonomous)

Argument: `<feature_name>`.

Prove the feature against the plan's test cases. The report's `status:` IS the decision — `kf stage` reads it and blocks the wrong direction.

**Invoked through `kf run`?** If your prompt starts with `kf-run:`, you are a worker for this stage only: skip the "move to stage" step below, never run `kf stage` / `kf approve` / `kf archive` / `kf run`, never edit approved contract artifacts, do not commit, and end your final message with two lines exactly: `STATUS: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` and `Summary: <one or two sentences>`. The main agent reads them and decides the transition.

---

## 1. Move to testing

```bash
kf stage {feature_name} testing
```

(Already there → skip.)

If `kf stage` refuses the move, run `kf validate --change {feature_name}` to see what is missing — unfinished `tasks.md` checkboxes block entry to testing (DoD), so tick them in implementation first.

Every entry to testing creates a new execution id. Keep old reports as evidence, but never reuse them as proof for the current implementation. Read the current id from `kf status` or `kf instruct ... --change`.

**Where the code lives:** when the item has a worktree (`kf status` shows `Worktree:`/`Domain:`), run the app and its tests inside the worktree path — that is where implementation landed. For HTTP/browser checks prefer `http://<domain>` (start the project's dev server on the allocated port); if the machine's domain infra is not set up, use the `127.0.0.1:<port>` fallback shown in `kf status` and say so in the report.

## 2. Run against the plan's test cases

Read the Test Strategy from `phase-1-spec-requirement.md` (Test Level / UI Tests / Tools / Coverage Target) — it was committed in the approved plan. Detect the real test tooling from the repo. Execute exactly what the level promises: `unit` → unit suite; `unit+integration` → + integration; `full` → + UI/E2E suite (Playwright/Cypress/...). If `full` and the UI tests are missing or skipped, that's a gap — report it, don't fake coverage.

Track TC-by-TC: Status / Actual / Expected / Tool / Evidence.

For `kind: bug`, use the bug report's reproduction, expected result, acceptance criteria and regression strategy instead of a phase-2 test plan. Verify the defect is fixed and run the affected regression suite; use descriptive test IDs or actual test names in the results table. Do not require FR/UC/TC artifacts for a bug.

## 3. Write testing-result

```bash
kf instruct testing-result --change {feature_name}
```

Fill `phase-4-testing-result.md`, set frontmatter `status:` to exactly one of:

- `PASS` — all tests pass, coverage target met
- `FAIL` — tests failing
- `REJECT` — feature does not meet acceptance criteria
- `BLOCKED` — cannot test (env/tooling)

Always write the report, including `execution:` from the current template. Include per-TC results, actual commands, evidence and coverage against the approved target. In the "Commands and Evidence" table the Exit code column must be the real numeric exit code of each command you ran; `kf validate` rejects a `PASS` report that has no command row or any exit code other than `0` (`testing_exit_code`). Keep status and conclusion consistent. Missing tooling, skipped required tests or unmeasured required coverage cannot count as PASS. Write outcomes here; keep phase-2-test-case.md unchanged.

## 4. The directional gate decides

- `PASS` → `kf stage {feature_name} review`
- `FAIL`/`REJECT` → loop to implementation, apply the fix, then enter testing again and write a result for the new execution id:

```bash
kf stage {feature_name} implementation
```

...then return here and re-test before attempting review again.

- `BLOCKED` → stop and report the environment/tooling blocker. Do not advance or substitute a known issue for required passing tests.

Still failing after one fix cycle → STOP, show failing tests, ask: fix deeper / record as known issue / abort.

---

## Done

Report written with a decisive status. Hand off:

```text
If PASS: load the kanban-review skill.
If FAIL/REJECT: kanban-implement first, then testing with a new execution id.
If BLOCKED: stop and report the blocker.
```
