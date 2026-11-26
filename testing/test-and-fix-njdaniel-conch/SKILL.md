---
name: test-and-fix
description: Run the test suite, categorize every failure (regression / flake / environment), fix regressions, and never silently skip. Use whenever tests fail or before opening a PR.
---

# test-and-fix

## Procedure

1. Run `go test ./...` (then `make check` for the full gate).
2. Categorize **every** failure:
   - **Regression** — the code under test is wrong, or the change broke a real contract. Fix the code (or, if the test encoded a wrong expectation, fix the test *and say so in the PR*).
   - **Flake** — passes on rerun, timing/ordering dependent. Rerun with `-count=5 -race` to confirm. Don't just rerun-until-green: file an issue for the flake with the failure output, and fix it if the fix is small (deterministic clock, channel sync, t.TempDir).
   - **Environment** — missing tool, sandbox limits, network. Note it in the PR; make the test skip *explicitly and loudly* (`t.Skipf` with reason) only if the dependency is genuinely optional.
3. Fix regressions in the current branch if in scope for the issue; otherwise file a blocking issue and stop.
4. Re-run the full suite after fixes.

## Never

- Delete or `t.Skip` a failing test to get green without flagging it prominently in the PR description (CLAUDE.md rule 6).
- Mark a regression as a flake because it passed once on rerun.
- Ship with the approval-path E2E test failing — that is always a blocker (rule 3).
