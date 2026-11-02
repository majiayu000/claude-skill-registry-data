---
name: ci-fleet-engineering
description: "Use when adding, editing, or debugging ANY GitHub Actions workflow that mutates shared data, publishes an artifact, reports, or runs on a cron, and when diagnosing CI failures, cancelled runs, lock contention, lost work, or alert noise. Carries the fleet doctrine: the compute/apply lock split, budgets that publish vs timeouts that kill, restore/publish guards, the never-started/displaced-run sweeper, the health auditor that never fails (findings go to one self-closing issue), the static gate checker (apply gating, GH_TOKEN in scope, reporter-may-fail), a red X reserved for broken, and the shell/scheduler traps (pipefail with tee, the [ -n x ] && ARGS+= trap, inputs as env, late crons, [skip ci] vs workflow_run). Triggers on workflow yml, cron, concurrency group, timeout-minutes, gh release upload, cancelled run, CI alert, lock, publish step skipped, GH_TOKEN, reporter, health issue, skip ci."
---

# CI Fleet Engineering

The full doctrine with incident write-ups: `docs/CI-FLEET.md`. The one-sentence
version: **a green run must have done something, a red run must mean something,
and no run may destroy work — its own or another's.**

## When writing or editing a workflow

1. **Mutates shared data?** Use the compute/apply split —
   `docs/templates/split-writer-workflow-template.yml` is the copyable shape.
   The lock (one shared concurrency group, `cancel-in-progress: false`) is held
   ONLY by the short apply job. GitHub keeps ONE pending run/job per group and
   DESTROYS the older pending on a newer arrival — short holds are survival.
   Run `python3 tools/check_workflow_gates.py` after touching any apply job.
2. **Long compute?** The tool takes `--max-minutes`, measured from PROCESS
   START, able to fire INSIDE one item, exiting 0 so publish still runs. Step
   `timeout-minutes` is a continue-on-error BACKSTOP above it, judged by a
   verdict step: fired + output grew → `::warning::`; fired + nothing → fail.
3. **Restores:** only a NON-EXISTENT release is a first run. Never `|| true` a
   restore. Snapshot-and-check any shared SQLite with
   `tools/sqlite_publish_guard.py`. `--clobber` = delete-then-upload; never
   clobber-upload a file that can be rejected (2 GB cap → both assets vanish).
4. **Uploads** wrap in `tools/gh_retry.sh` (must-persist, fails loudly);
   **dispatches** in `tools/gh_dispatch.sh` (fire-and-forget, exits 0).
5. **Never `cmd || true`**: capture the exit code and `::warning::` it.
   `tool | tee log` needs `set -o pipefail` (or `${PIPESTATUS[0]}`) or a crash
   goes green.
6. **Inputs as env, never pasted.** `${{ inputs.x }}` inside `run:` is text
   substitution: a quote closes the string, free text is injection. Map to
   `env:` and read `"$X"`. Optional flags are `if [ -n "$X" ]; then ARGS+=(...); fi`,
   never `[ -n "$X" ] && ARGS+=(...)`: that returns 1 on empty input, and as a
   step's (or function's) last line it fails the step under `bash -e`.
7. **Every step that runs `gh` has `GH_TOKEN` in scope** (step, job or
   workflow env). A runner has no ambient credential; a publish step without
   it fails and skips everything after it.
8. **Reporters never fail on their findings.** A dashboard, auditor or status
   check exits 0 whenever it read what it came to read, and puts findings in
   the step summary, a `::warning::`, or an issue. A step in a `REPORTERS`
   workflow that can exit non-zero carries `# reporter-may-fail: <why>`
   naming its OWN mechanics.
9. **Schedule for the lag.** Crons run four to five hours late; when work must
   follow a release, trigger it with `workflow_run`. A bot commit marked
   `[skip ci]` fires no `push` workflows at all, including deploys; chain
   those with `workflow_run` and use `paths-ignore` instead.

10. **A push retry rebases and resolves, never `pull --rebase || true`.** A
   conflict leaves the rebase half-done and every retry fails. Generated
   file: this run's copy wins. Hand-edited file: main's wins, or stop with an
   error. Abort a rebase that cannot continue (`docs/CI-FLEET.md` §3).
11. **Failures are remembered on the item, not the runner.** A failure list on
   the runner dies with it, and the same poison items lead every run. Cap a
   download's total time, not only each read. Adopt an artifact already
   hosted before regenerating it.
12. **Ingest hands off to the gate, and the gate publishes.** Never let
   discovery publish new items before the audits that judge them have run.
   Give each source of a shared queue a fair share.

## Standing guardians (enable once per repo)

- `.github/workflows/retry-infra-failures.yml` + `tools/retry_infra_failures.py`
  — re-runs never-started runs and queue-displaced runs/apply-jobs. The gate is
  "zero steps ran," which is the no-side-effect proof; verify changes with
  `DRY_RUN=1` against real history.
- `.github/workflows/workflow-health.yml` + `tools/audit_workflow_health.py`:
  daily judge of what each workflow's last SCHEDULED run PRODUCED (BROKEN,
  KILLED, FAILED, DROPPED, STALE, SILENT, DRAINED), each against its OWN
  cadence. `NO_YIELD_LINE` workflows skip only the yield check; their failures
  still count. Self-cancelling workflows (`cancel-in-progress: true`) are not
  KILLED. **The auditor never fails.** Urgent findings (BROKEN, KILLED: the
  ones nothing else alerts) go to ONE self-closing issue via
  `tools/report_workflow_health.py`, opened or updated in place, closed when
  the fleet is clean.
- `tools/check_workflow_gates.py`: static checks, exit 1 on violation. Apply
  jobs fully gated; every `gh` step has `GH_TOKEN`; reporter workflows
  (`REPORTERS`) never exit non-zero without `# reporter-may-fail:`. Tests:
  `tools/test_workflow_health.py`, `tools/test_workflow_health_gate.py`.

## When diagnosing

- Run duration includes QUEUE time — read job-level startedAt/completedAt
  before diagnosing slowness (a "673-minute run" was a 1-minute job).
- A cancelled run with zero steps was displaced, not stopped; one with steps
  was stopped by a human or timeout. Never blur these.
- A check that reports "nothing to do" suspiciously fast is a finding, not a
  completion — verify what was OFFERED to it (markers, filters) before
  believing the count. Timestamps + TTLs on every "verified" marker; record
  the SOURCE on every "already tried" marker; persist evidence, not verdicts.
