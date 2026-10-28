---
name: autopilot
description: Drive an existing wayfinder map, spec, or set of tickets to completion through fresh top-level Claude Code, Codex, or Grok sessions.
disable-model-invocation: true
argument-hint: "Path to a wayfinder map, spec, or ticket"
---

# Autopilot

Run approved pipeline work until it is complete or reaches a genuine human gate. Keep `wayfinder`, `to-spec`, `to-tickets`, and `implement` authoritative; this skill adds a fresh-process loop around them.

## Start the loop

1. Require a reference to a `wayfinder` map, a spec, or a ticket. Run from the target Git repository.
2. Select the current harness as the provider: `claude` in Claude Code, `codex` in Codex, `grok` in Grok. When running directly from a terminal, require the user to choose.
3. Resolve this skill's installed directory, then run the bundled script by absolute path while keeping the target repository as the working directory:

```bash
bash <autopilot-skill-dir>/scripts/autopilot.sh --provider <claude|codex|grok> --root <ref>
```

Pass `--repo <path>` when the target is not the current repository, `--max-iterations <n>` to replace the default limit of 50, and `--log-file <path>` to mirror the per-run log to another path.

Run the script as a background task: one iteration is a full build lifecycle and routinely outlasts a foreground shell-command timeout. Its exit is the completion signal (for a `--tmux` run, one background `--wait`). Immediately report the run ID, worker session model and effort, log path, and printed observer commands. Then report worker milestones and five-minute heartbeats as they arrive; leave routine tool events in the log. Stream them by running `--follow 2>&1 | grep --line-buffered -E 'Autopilot: (iteration |selected |next |worker(:| alive)|ticket )|quiet threshold|gate|failed|invalid|interrupted|stopped'` under `Monitor` where available (re-arm when it expires; every `--follow` line is `<timestamp> Autopilot: <message>`); otherwise read `--status` and the log tail each time the turn resumes, and when the run exits. On exit `2` (needs input), `3` (blocked), `4`, or `5` (failure), ping the user (`PushNotification` where available, otherwise in the chat report) with the status and reason.

Foreground run mode prints progress to stderr and one terminal result object to stdout; completion is exit code `0` with `status: complete`. Observer modes keep their operational messages on stderr: `--status` prints one state object, `--history` prints an array of retained states, `--tmux` prints one launch object, and `--follow` streams the human-readable run log to stdout, and `--wait` blocks until the run leaves `running`, prints the final state object, and exits with the run's terminal code (below). To wait on a run you did not start in this shell, prefer one `--wait` call with `run_in_background` over any sleep or `/loop` polling of `--status`. With no run for the root, `--status` prints `{"status":"none",…}` and exits 1.

Use the printed commands to inspect a run independently:

```bash
bash <autopilot-skill-dir>/scripts/autopilot.sh --status --root <ref> [--repo <path>]
bash <autopilot-skill-dir>/scripts/autopilot.sh --follow --root <ref> [--repo <path>]
bash <autopilot-skill-dir>/scripts/autopilot.sh --history --root <ref> [--repo <path>]
```

`--follow` exits when the run does; `--history` returns every retained run for the root. For a detached terminal-owned run, add `--tmux`. Its stdout is a launch object rather than the eventual worker result. Report the printed `status`, `follow`, and `tmux attach` commands; continue monitoring through `--status` until the run reaches a terminal state. Read the exact terminal result from the `result_file` in status.

## Worker model and effort

Every worker session is one sub-session of the run, and every run reports which model and reasoning effort those sub-sessions use. The report appears in four places: the `worker session model <model> (<source>), effort <level> (<source>)` line at run start, the per-iteration line, each heartbeat, and `--status` (as the `model`, `model_source`, `effort`, `effort_source`, and `reported_model` state fields). A `--tmux` launch object carries the same values.

Set them explicitly to pin every sub-session:

```bash
bash <autopilot-skill-dir>/scripts/autopilot.sh --provider <claude|codex|grok> --root <ref> --model <name> --effort <level>
```

`AUTOPILOT_MODEL` and `AUTOPILOT_EFFORT` are the environment equivalents. Valid effort levels are `low|medium|high|xhigh|max` for `claude` and `none|minimal|low|medium|high|xhigh|max` for `codex` and `grok`; the runner rejects anything else before starting a worker.

The `source` names where each value came from: `requested` for a flag or environment variable, `settings` for the resolved Claude Code settings chain (`model` and `effortLevel`, honoring `CLAUDE_CONFIG_DIR`), `config` for `$CODEX_HOME/config.toml` (`model` and `model_reasoning_effort`) or `$GROK_HOME/config.toml` (`[models].default` and `[models].default_reasoning_effort`), and `provider default` when neither is set and the provider chooses. Claude and Grok workers also report the model the session actually resolved; that authoritative value is announced when it differs from the requested one (an alias like `opus` resolving to a dated model ID) and is kept in state as `reported_model`.

## Fresh-process contract

Each iteration launches a new top-level CLI process with normal user and project configuration but with permission prompts and sandboxing bypassed (`--dangerously-skip-permissions` / `--dangerously-bypass-approvals-and-sandbox` / `--always-approve`): headless workers cannot answer prompts, so only start the loop on work the user has already approved for autonomous execution. It performs exactly one decision ticket or one build ticket, finishes all nested review and verification agents, records durable tracker and Git state, and exits.

Before launching it, the runner parses current statuses, claims, and blocking edges, chooses the deterministic frontier unit, and passes a compact JSON manifest: mode, exact selected unit, parent, direct blocker states, whole frontier, and launch `HEAD`. The worker revalidates that unit and its direct blockers, then progressively loads the parent's Build Contract, ticket-named sections, blocker resolutions, path-local instructions, and seam files. Closed sibling bodies and the full parent are on-demand context rather than a fresh-process orientation tax.

The runner keeps durable state, a human-readable log, and raw provider events under the target repository's Git directory. Claims made by that run include the ID, so a later invocation of the same command can recognize and resume its own interrupted work item without taking over another session's work. A per-root lock prevents concurrent runner processes from sharing that identity. Terminal state remains inspectable; rerunning a completed root starts a new run, while failures and human gates resume the existing run.

A heartbeat proves that the worker process is alive. It defaults to five minutes; set `AUTOPILOT_HEARTBEAT_SECONDS` to a positive number of seconds when a different cadence is needed. `quiet threshold reached` means it has emitted no provider event for two heartbeat intervals; treat that as a prompt to inspect the log or attach, not proof that the worker is hung. The runner never kills quiet work automatically.

Use the installed workflow skills as the single source of truth. The script locates them all to validate the installation, then passes only the selected mode's workflow to the worker: `wayfinder` for a decision ticket, `implement` for build work. If the pipeline skills are absent, install this repository's complete skill collection before retrying.

## Ticket status

Every unit is marked in progress before work starts and closed after it is verified and committed, so the markdown tracker under `.scratch/` always reflects reality. The worker writes the transition into the file's YAML frontmatter (`status: in-progress` plus `claimed-by: autopilot:<run-id>`, then `status: closed` plus `## Resolution`) for build tickets and directly implemented specs; a `wayfinder` decision ticket gets only the claim, its `status` staying `open` until it closes.

The runner does not take that on trust. It snapshots every work item beside the root before each iteration, announces each status change afterwards (`ticket .scratch/x/tickets/01-y.md: ready-for-agent -> closed`), and fails the run when a successful result names a different unit or one whose file is not closed. It then rereads the tracker itself and replaces the worker's `status` and `next_ref` with the authoritative next frontier, completion, human gate, or blocked state. A unit this run claimed and left open is announced as an open claim.

Stopping at a gate leaves the in-progress marker and the run's claim in place on purpose: that marker is how a later process recognizes its own resumable work rather than colliding with another session's.

## Human gates

A build ticket whose frontmatter says `deploy-gate: true` is a human gate after it closes: the runner stops with `needs_input` instead of continuing to the next ticket, because the unit must be deployed on its own before its dependents are built (expand before migrate before contract; a command before the enforcement that relies on it). Deploy, then rerun the same command; the closed ticket is the resume point.

Headless workers cannot conduct a live interview or approve a new spec or ticket breakdown. Stop with `needs_input` when `wayfinder` reaches a HITL ticket, `to-spec` needs publication approval or a decision answered, `to-tickets` needs an open build decision answered, or implementation exposes an undecided product question. After resolving the gate interactively, rerun the same command; tracker state and commits are the resume point.

If an interrupted owned claim cannot be safely resumed from the current tracker and worktree state, stop with `needs_input` and identify the claim and unresolved changes. Never clear or take over a differently owned claim automatically.

Exit codes are `0` complete, `2` needs input, `3` blocked, `4` worker failure, `5` runner/configuration failure, `129` hangup, `130` interrupted, and `143` terminated.
