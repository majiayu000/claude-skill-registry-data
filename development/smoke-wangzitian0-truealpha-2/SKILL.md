---
name: smoke
description: Step 4 of the five-step flow. Run a fast check in about 30 seconds after an edit. Compile, focused tests, then connectivity. Not a deep audit.
---

# smoke: fast, cheap, honest

Smoke is the first guard after an edit. Use `audit` for depth and `close` for the exit gate.

## Order (left to right, fail fast)

1. **Compile or syntax** on the changed files only (`python -m py_compile`, `ruff check --select E,F`, `go build ./...`, `tsc --noEmit`).
2. **Focused tests** that touch the change, with `-x` (`pytest <file>::<test> -x`). Never run the full suite or whole-repository runners (`ci_runner.py all`, `check_suite_coverage.py`) during smoke.
3. **Connectivity** of what the code depends on: credentials, services, MCP servers. Commands are in `local.md`.
4. **Acceptance** of each issue deliverable that the change touches (next section).

Stop at the first red. Smoke reports the problem. It does not fix it, and it changes no project file. The scratch worktree of the acceptance checks lies outside the project.

## Acceptance checks

Acceptance runs here and in `close`. Issue and PR text do not carry it.

1. Name the check for each deliverable: a test path, a CI step or a probe command. A deliverable with no named check is a finding. Write the check, or delete the deliverable from the issue body with a comment.
2. Run the check on the change. Report `PASS` or `FAIL`.
3. Run the same check without the change: a scratch worktree at the base commit, with the new test files copied in. It must fail. A check that passes without the change proves nothing.
4. Read the call path of the check. It must call the entry point that production calls, with the arguments that production passes. A check that supplies an argument the production caller omits proves the parameter, not the wiring.
5. A criterion is a check that runs again. Name the CI step or the schedule that repeats it. A run that happened once is evidence.

## Verification rules

- **Existence is not validity.** "The variable is set" and "the process is alive" prove nothing.
  Call a read-only endpoint, or do not claim green.
- **No `grep PONG` probes.** A string match hides truncation, token overflow, and silent downgrade.
  A probe must check three things: exit code 0, wall time, and a non-empty payload of the expected shape.
- **Skipped is not passed.** Report a check that did not run as `SKIPPED`. Do not count it green.
- **Use the small model tier.** A smoke run with a large model or deep reasoning burns the rolling quota.
  Put concrete model names and flags in `local.md`. They change often.
- **Do not wait on slow CI.** When a run exceeds the budget, run the focused checks yourself and report the CI status separately.

## Report

One table, one row per check: result (`PASS`, `FAIL`, `SKIPPED`), seconds, and the count (`N passed`).
Add the total time and one sentence: which row is red.
