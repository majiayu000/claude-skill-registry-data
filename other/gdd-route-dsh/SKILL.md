---
name: gdd-route-dsh
description: >-
  Configure the DeepSeek Harness (`dsh`) headless route for gdd's shared runner.
  Covers route configuration and troubleshooting, not interactive sessions or
  the overall delivery protocol.
disable-model-invocation: true
metadata:
  revision: "7"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "hidden DeepSeek Harness headless route for gdd: configuration, session handling, and recovery"
  summary_zh: "gdd 的隐藏 DeepSeek Harness headless route：配置、会话管理和恢复"
  kind: "mechanism"
---

# gdd-route-dsh

`dsh --profile headless` answers one task per invocation, streams NDJSON events, and can resume a
persisted session. The delivery protocol stays in [gdd](../gdd/SKILL.md), which this skill requires.
Install both in the same skills root.

## When to Use

- Dispatching a stage to DSH: set `GDD_AGENT=dsh` and run `uv run ../gdd/scripts/gdd.py stage …`,
  or pass `--agent dsh` to the runner directly.
- Diagnosing a dsh stage that exited 0 but did not do the work, refused to resume, or stalled.
- Not for choosing the increment (goal contract / `define-goal`), and not for OMP/Paseo route details
  (read [GDD transport](../gdd/references/transport.md) for those).

## Read when needed

| When | Read |
|---|---|
| Setting up or changing the route, checking unsupported flags or deadlines, or using the raw CLI | [Configuration](references/configuration.md) |
| Changing permissions, overlays, tool execution, credentials, or compaction; diagnosing an activation warning or a corrupt session | [Harness quirks](references/harness-quirks.md) |
| Estimating round cost, deciding where to split an increment, or comparing native and programmatic tool calls | [Cost notes](references/cost-notes.md) |
| A runner script command fails (for example `uv` is not found) | [Runner troubleshooting](../gdd/references/troubleshooting.md) |

For shared settings see [GDD config](../gdd/references/configuration.md); for detach modes see
[platform rules](../gdd/references/transport.md#headless-platform-rules).

## Route safety

- `--cwd` selects the working directory; the permission mode sets the write boundary. Where dsh
  enforces a sandbox, `workspace-write` allows writes inside that boundary and denies writes outside
  it even where Unix modes permit them. Reads outside are allowed. Re-confirm the boundary before
  dispatch if the profile or `DSH_PERMISSION_MODE` changes; never use full access to unblock a task.
- Detached runs require `--approval-policy never`: there is no approval channel, so a call needing
  approval is rejected. Never put credentials in a prompt, repository file, or run artifact.
- Keep experiments call-level (`--patch <overlay>.yml`), not in the harness's global configuration.
- Budget: two corrective rounds per stage, then stop and escalate (different model, narrower
  contract, or abandon).

## The runner supervises; the raw CLI is for one-offs

The shared runner owns `start|status|result|answer|tail|kill`: it creates the run directory, detaches,
keeps `state.json` current, recovers dead runs, and stops through a control file. Raw `dsh --profile
headless …` is for manual one-offs only: no detach, `state.json`, stale recovery, or stop file.

The runner's equivalent, which is what a GDD stage uses:

```text
uv run ../gdd/scripts/agent_run.py start --agent dsh --name example --prompt task.md --cwd .
uv run ../gdd/scripts/agent_run.py status example
uv run ../gdd/scripts/agent_run.py answer example
```

## One goal, one worktree, one session

- **New increment → new session.** Reusing an unrelated session re-sends its accumulated context.
- A session is anchored to its recording directory. Resuming elsewhere is refused (`was recorded in
  "<A>", not "<B>"`). A permitted same-increment revision or verification can use the runner's
  `start --resume <session-id>` in the same cwd (`--session-id` is a compatibility alias); it repeats
  permission and approval flags. GDD's fresh-stage rule still applies. For a resumed run, say where
  it was interrupted, that the tree is mid-flight, and that the prompt continues rather than restarts.
- **Parallel goals use separate worktrees and sessions**, even in the same repository. Dsh refuses
  two writers to one session (`already owned by an active write handle`); the runner refuses a second
  `start` on a live slug. Neither prevents two sessions from writing one worktree. Keep one writer
  per worktree so edits, gates, and reviewer inspection do not interleave.

Prompt with repository context **by file path**, an observable done-when, and the rules: writable paths,
no commits/pushes, orchestrator-owned tests. Require command, exit code, count line, changed files, and
unmet criteria in the report.

## Completion is two conditions, then your own gates

```
success = exit_code == 0, and the last `final` event carries reason.kind == "completed"
```

The runner, `gdd.py`, and the observer read the same states: `done` needs both conditions above;
`killed` means a runner stop (143) or a signal-style exit (`130/137/143/-2/-9/-15`, raw code retained);
everything else settled is `failed`, including exit 0 without the success marker and stale recovery.
A runner-level failure emits `error` instead of `final`; a killed run has no `final`.

Verify independently: check `git status --porcelain` for scope, run the repository's gates on the
final tree, and inspect `stderr.log` for `did not activate` / `pending (waiting for service: …)`.
A composition row can fail to load with exit 0. `tool_result.status == "completed"` means the tool
returned, not that the shell command inside it succeeded.

Poll `state.json` with `agent_run.py status`: no heartbeat event or detached notification exists.
Use `session.sessionId`, `status.phase/turn/step/usage`, `tool_call`, `tool_result`, `final`, and
`error` for progress; tool-call count is not a completion percentage.

## Stopping and recovering

- Stop through `uv run ../gdd/scripts/agent_run.py kill <slug>`. It writes `<run_dir>/stop`; the runner
  ends the process tree (POSIX group TERM, 5 s, KILL; Windows `taskkill /T /F`) and finalizes killed/143.
  Without the runner, `kill` only signals a recorded PID when the live start time matches the recorded
  one. If it cannot prove that, it signals nothing and exits 1 naming each PID and why; end the process
  tree by hand, then run `kill` (or `status`) again. `start --replace` stops the live run before moving it aside.
- The next `status`/`result`/`list`/`answer` finalizes a dead, unfinalized run as `failed` with exit −1
  and `stale_recovered: true`, idempotently while no `finalized` marker exists. Recovery uses only the
  worktree, the harness session log, and run artifacts; there is no task database, checkpoint framework,
  or WAL. For session-log recovery, read [Harness quirks](references/harness-quirks.md).
