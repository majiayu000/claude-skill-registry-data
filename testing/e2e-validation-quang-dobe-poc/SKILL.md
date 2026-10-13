---
name: e2e-validation
description: At the final implementation step, author automated e2e tests from every E2E-n case in <feature>.test.md and run them via the project test-runner. Done-when all cases are green. Used by the software-engineer agent.
---

# E2E validation skill

## Mission
Turn the Tester's black-box spec into automated, runnable e2e tests at the feature's final implementation step (the E2E validation gate in `plan.md`). This is the feature's acceptance — there is no separate end-of-feature Tester pass.

## Inputs
- `docs/<feature>/<feature>.test.md` — every `E2E-n` case (`Covers` / `Given` / `When` / `Then`).
- The project `test-runner` agent (run by role via `project-seams`); project `test-rules` for e2e layout.

## Procedure
1. Read every `E2E-n` case in `<feature>.test.md`.
2. Author one automated e2e test per case, keyed to its `Covers` criterion. Translate `Given`/`When`/`Then` into setup / action / assertion.
3. Use resilient, semantic selectors and assertions (role/test-id/text, not brittle CSS/internal-state). Keep tests independent — each sets up its own state.
4. Run the suite via the project's `test-runner` agent. The step is **done only when every `E2E-n` case is green**.
5. Report pass/fail per case and the files added.

## Boundary
Runs the project test-runner; does not invent acceptance cases beyond `test.md`, flip `[X]`, write `status.md`, or commit. Full contract: `pipeline-protocol`.
