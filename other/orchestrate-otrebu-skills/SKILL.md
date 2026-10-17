---
name: orchestrate
description: Supervise detached agent-CLI workers through a run-scoped tmux or cmux control loop.
disable-model-invocation: true
---

# Orchestrate

Treat the current session as the **control tower**. Keep decomposition, worker routing, integration, user communication, and final review in this session. Use `orchestrate.sh` to control detached agent-CLI workers in tmux or cmux.

Resolve `ORCH` to the absolute `orchestrate.sh` adjacent to the `SKILL.md` that loaded this skill. Verify that it is executable before continuing. Use the output of `"$ORCH" help` as the authority for command syntax, supported profiles, and defaults; the current help command exits with status 1 after printing that output.

## Control invariants

- Launch full-auto workers only in directories the user has entrusted to autonomous edits and commands.
- Record the active `ORCH_HOME` and choose a unique run prefix. Start every worker ID with that prefix so concurrent control towers sharing the state directory cannot collide.
- Record each worker's ID, directory, workstream, and latest state in a ledger file at `$ORCH_HOME/<run-prefix>-ledger.md`, rewritten on every change; after a context summary, read it back rather than trusting memory. Pass explicit ledger IDs to `waitall` and `stop`; reserve no-ID `waitall`, `stop --all`, and `gc` for recovery after confirming the entire `ORCH_HOME` is in scope.
- Route human decisions to the user. Treat `--answer` as an assertion that the user chose the supplied response, and pass it only after receiving that choice.
- Interpret `DONE` as a settled worker screen. Establish task completion separately by reading the logs, checking for trailing questions or unfinished plans, reviewing the result, and running verification.
- Interpret `TIMEOUT` as a live worker that needs inspection or more time. Inspect with `poll` or `logs`, then wait again.
- Run commands that may exceed the host's foreground limit (`spawn`, `run`, `wait`, `waitall`, and `stop`) through the host's non-blocking execution facility, retaining the handle until stdout is collected.

For two or more concurrent workers, read [references/fan-out.md](references/fan-out.md) completely before creating any worker, then apply it alongside the loop below.

## Dispatch loop

1. **Plan the workstreams.** Give each active workstream one owner, one bounded deliverable, one verification requirement, and explicit coordination boundaries. Serialize work that edits the same checkout or depends on unfinished output. This step is complete when every active workstream has an unambiguous boundary, owner, deliverable, and verification requirement.

2. **Spawn and ledger each worker.** Give it a stable ID matching `[A-Za-z0-9_-]+`, a trusted directory, and the appropriate mux and agent profile:

   ```bash
   "$ORCH" spawn <id> --dir <trusted-dir> [--mux tmux|cmux] [--agent <profile>]
   ```

   Record the returned worker in the run ledger. Inspect it with `poll` after spawn. This step is complete when each dispatched worker is live, recorded, and ready to accept a task.

3. **Dispatch and supervise.** Send a prompt containing the objective, scope, deliverable, verification requirement, coordination boundaries, and this human-input contract:

   > If you need a human decision, print a line exactly: `>>> NEEDS_HUMAN: <your question>` and stop. Otherwise keep going until verification passes, with status notes in the same message as your next action.

   Use `run` for a single worker or a follow-up:

   ```bash
   "$ORCH" run <id> --file <prompt-file> --timeout 1200
   ```

   Parse the single `STATE=<state>` line and take the matching action:

   | State | Control-tower action |
   |---|---|
   | `DONE` | Collect `logs --lines 2000`. Check for a trailing question, unfinished plan, missing deliverable, and failed or absent verification before accepting the result. |
   | `NEEDS_INPUT` | Capture the dialog with `poll` or `logs`, surface it to the user, then deliver their choice with `run --answer -- "<choice>"`. |
   | `TIMEOUT` | Inspect current state and output, then call `wait` with an appropriate timeout. |
   | `GONE` | Collect remaining logs, clean its metadata with `stop`, and recover, reassign, or explicitly drop the workstream with a recorded reason. |

   Treat `BUSY` and `UNKNOWN` from `poll` as active states that require further inspection or waiting. This step is complete when every dispatched worker has produced a reviewable result, been reassigned, or been explicitly dropped.

4. **Integrate accepted output.** Inspect every result and diff in the control tower, resolve interactions, and run the required verification on the integrated state. Send focused follow-ups with another `run` when a deliverable or verification is incomplete. This step is complete when all accepted output forms one coherent result and its required verification passes.

5. **Review the whole result.** Account for every workstream, worker state, dropped item, verification result, and unresolved question. This step is complete when no actionable finding or unaccounted workstream remains.

6. **Clean up the run.** Collect any final logs, then call `stop <id>` for each worker in the ledger. Preserve unrelated workers and every worktree; worktree removal requires separate user authorization. This step is complete when every worker created by this run is stopped and its metadata is gone.

## Completion gate

Call the task complete only when every workstream is completed or explicitly dropped, all accepted output is integrated, required verification has passed, no human decision or trailing worker question remains, the control tower has reviewed the combined result, and run-scoped cleanup is complete.

## Conditional operations

Immediately before using non-core commands such as `attach`, `list`, or `gc`, authoring a custom agent profile, recovering after a crash, or tuning completion detection, run `"$ORCH" help` and follow the installed script's current output. For a custom profile, also inspect the `P_*` profile contract at the top of the adjacent `orchestrate.sh`. Validate an unverified profile with a throwaway worker before trusting its state classification.
