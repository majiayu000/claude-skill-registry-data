---
name: gdd-route-omp
description: >-
  Launch a detached oh-my-pi/OMP print-mode job so omp -p survives the dispatching session. For long
  headless tasks or a turn killed midway, set a timeout, poll runner status, inspect the NDJSON
  event log and resume from the saved session ID. Not for tmux-agent-control.
metadata:
  revision: "7"
  areas: "software-development,work-management"
  targets: "pi"
  summary: "detached runner for long `omp -p` runs; polled completion, session-id recovery (requires skill `gdd`)"
  summary_zh: "脱离会话的 runner 跑 `omp -p` 长任务；轮询完成、按 session id 恢复（需要 skill `gdd`）"
  kind: "entry"
---

# gdd-route-omp

Run long OMP print-mode jobs through GDD's shared detached runner. Install both skills.
For detachment, timeouts, cleanup, state and artifact formats, see
[GDD transport](../gdd/references/transport.md). Use its runner, not a bare background job.

## Dispatch

- GDD selects OMP by default when no route is configured; pass `--agent omp` for standalone
  dispatch. `OMP_BIN` overrides the executable on PATH. Use a native executable on Windows
  for multiline prompts. Set an explicit model and compatible thinking effort when they must
  be reproducible. The route forwards `--profile`, model, thinking, and the explicit resume ID;
  the prompt is last. Results use prompted JSON, not a native schema flag.
- The adapter selects print mode, JSON events and non-interactive approval (`yolo`).
  Launch only with operator authority, an isolated worktree, bounded permissions and
  independent gates. Agent output is not authorization to publish or alter shared state.
- The optional POSIX `scripts/omp-run.sh` sets `GDD_AGENT=omp` and forwards to the shared
  runner; `OMP_RUN_SH` can override it. The legacy runner `--backend` is ignored with a
  warning; it does not select a supervisor.

```text
uv run ../gdd/scripts/agent_run.py start --agent omp --name SLUG --prompt FILE --cwd DIR --max-time DURATION
uv run ../gdd/scripts/agent_run.py status SLUG
```

Only if a script command fails (for example `uv` is not found), read
[the runner troubleshooting reference](../gdd/references/troubleshooting.md).

## Observe and accept

1. Poll runner `status` at turn boundaries; use bounded `tail` for event progress, not raw
   NDJSON or process-name matching. Budget time for all child work; serialize heavy gates on
   constrained hosts.
2. Require the last assistant `message_end.stopReason` to be present and not `error`,
   `aborted`, or `length`. Read `answer.md` and the result; exit zero alone cannot prove
   completion, especially for empty, truncated or still-waiting answers. Require actual gate
   exit codes; a background verifier may die at runner cleanup. Re-run the repo gate yourself.
3. On `ECONNREFUSED`, check whether operator configuration or logs confirm an endpoint
   restart. If confirmed, retry once after recovery; if it fails again, report or select an
   authorized fallback rather than retrying indefinitely. Do not infer a model defect.

## Recover

Use runner `list` or `status` to distinguish a live run from a stale one and recover its
recorded `session_id`. Start a new named runner invocation with `--agent omp` and
`--resume <id>`; the prompt should state what remains in the same interrupted stage.
Do not use implicit last-session selection or TTY-only restoration for headless recovery.
For interactive steering, use the installed CLI's interactive resume on that ID only after
the headless process has stopped. Never attach two writers to one session.
