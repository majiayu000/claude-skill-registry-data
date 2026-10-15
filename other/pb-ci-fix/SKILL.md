---
name: pb-ci-fix
description: >-
  Fix red CI or set up GitHub Actions end to end: read the failing run, find
  the root cause, patch and validate the workflow, push only after GO, and
  watch the run go green on the pushed commit. Use for "CI is red", "the
  build fails on GitHub", "set up CI for this repo", "fix the workflow".
category: engineering-method
kind: playbook
trigger: ["CI is red", "set up CI", "fix the GitHub Actions run"]
inputs: [repo, "failing_run_id?"]
requires:
  skills: [github, deja-memory, systematic-debugging, ci-pipeline, github-actions-generator, github-actions-validator, bdbresilience, verification-before-completion, "gh (external)"]
  agents: []
  mcps: []
  store: []
go_points: [git push]
outputs: [".github/workflows/*.yml", "production_artifacts/pb-ci-fix-<date>.md"]
verify: "gh run list --commit <sha> --json conclusion -q '.[0].conclusion' == success"
difficulty: intermediate
est_time: 15-45 min
---

# Fix red CI or set up GitHub Actions
What you get: a green GitHub Actions run on a pushed commit, with the cause and the fix written down.

## Inputs
- repo — the current directory, or the one the user names
- failing_run_id (optional) — from the GitHub Actions page; otherwise the latest failed run

## Steps
1. github — repo → `gh run list --limit 5` (gh missing, not authenticated, or no GitHub remote → log it, give the `gh auth login` / remote hint, stop) and `gh run view <id> --log-failed` excerpt in the run log — failing job and step named; no workflows exist → go to step 4 (setup path; skips steps 2, 3 and 6, and step 7 runs the new workflow's commands locally)
2. deja-memory — error text → `deja fix` result in the run log — prior fix found, or "none"
3. systematic-debugging — failing step → root cause and a local repro command — repro fails locally, or the reason it cannot run locally (a config-only fault: the validator or step commands are the repro for step 7)
4. ci-pipeline (no workflows) or github-actions-generator (patch) — root cause → `.github/workflows/*.yml` diff — diff touches only the cause
5. github-actions-validator — workflows → validator report — zero errors after the mandatory rerun
6. bdbresilience — only if step 3 classified the failure as transient → retry or timeout on that step only — no blanket retries
7. verification-before-completion — repro command → fresh passing output pasted in the run log — output pasted, not claimed
8. git commit `ci: <cause>` — stage only the changed `.github/workflows/*` files (never the run log) → SHA in the run log — commit succeeds (any hook failure is reported, never bypassed with --no-verify)
9. [GO] git push — SHA → remote branch (name the branch in the WAITING FOR GO line) — The run stops here until the human types GO. Each retry cycle that pushes again needs its own fresh GO here.
10. github — SHA → `<id>` from `gh run list --commit <sha> --limit 1 --json databaseId` (wait until it exists), then `gh run watch <id> --exit-status` — `gh run list --commit <sha> --json conclusion -q '.[0].conclusion'` equals `success`; otherwise back to step 3, at most 2 cycles (each push behind a fresh GO at step 9), then stop and escalate

Run log: `production_artifacts/pb-ci-fix-<date>.md`

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- GO is by contract in every harness. The go-gate hook is only a backstop on Claude Code, OpenCode and agy (Codex: unverified; Cursor, Kimi: none). A missing hook is never permission to proceed.
- A failed check stops the run: write the failure into the run log and report. No silent retries beyond what a step names.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
