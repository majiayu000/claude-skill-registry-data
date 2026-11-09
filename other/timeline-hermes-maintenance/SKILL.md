---
name: timeline-hermes-maintenance
description: Use when the local Hermes gateway, kanban board, or task workers stall.
version: 1.0.0
author: Timeline
license: MIT
platforms: [macos]
metadata:
    hermes:
        tags: [hermes, kanban, gateway, rate-limit, maintenance]
---

# Timeline Hermes Maintenance

The project's task work runs as Hermes kanban cards executed by worker processes under the local
gateway. When the board "stalls", the cause is almost never a card body: it is the gateway draining,
a provider rate limit, or a card the dispatcher cannot see. Diagnose in that order.

Paths here are Hermes-standard and portable. No account handle, list id or session id belongs in
this file - those live in the gitignored identifier map described in
`Documentation/Reference/Configure.md`.

## When to Use

- Cards sit `running` with no output, or several flip to `blocked` at once.
- The UI (TUI, dashboard) feels frozen or slow.
- A maintenance sweep is asked for, or work seems to be running in the background that nobody
  started.

## Sweep order

Run these in order; each one rules out the previous cause.

1. **Rule out resources first, and do not revisit them on a hunch.** `uptime` reports load,
   `memory_pressure | tail -4` reports free percentage, `df -h /` reports free space. A healthy
   answer means stop guessing at exhaustion and go to the gateway log.
2. **Count the workers.**
   `ps -eo pid,etime,command | grep -E 'managed_worker|kanban_worker_client' | grep -v grep` lists
   every live worker and its age. Each running card has one `kanban_worker_client`; a
   `managed_worker` with no client beside it is a finished card whose process has not exited yet.
3. **Read the gateway's own account.** `tail -40 $HERMES_HOME/logs/gateway.log` carries
   `kanban dispatcher [default]: spawned=N reclaimed=N crashed=N` per pass, plus any
   `Restart deferred` line. `$HERMES_HOME` is the agent's profile directory; the paths below are
   relative to it, so they read the same on any machine.
4. **Count the rate limit by minute.**
   `grep 'RateLimitError' $HERMES_HOME/logs/gateway.error.log | grep -oE '^[0-9-]+ [0-9]{2}:[0-9]{2}' | uniq -c | tail -10`.
   A cluster in one or two minutes is the provider throttling, not a code defect.
5. **Read the board.** `hermes kanban list` prints every card with status and assignee;
   `hermes kanban show <id>` adds runs and comments.
6. **Read the block reason, not the status.** A `blocked` card carries `last_failure_error`:

    ```sh
    sqlite3 $HERMES_HOME/kanban.db "select id,status,consecutive_failures,substr(last_failure_error,1,200) from tasks where status='blocked'"
    ```

    The wording decides which failure below you are looking at.

## Failure: every worker dies at the same moment

A restart request (`hermes gateway restart`, delivered as SIGUSR1) does not stop the gateway. It
enters a drain and defers while work units finish, logged as
`Restart deferred: waiting on N active work unit(s) … Ns remaining before force drain`. During that
window the gateway stops answering worker receipts, and each worker will not redial - its reconnect
is wrapped in `outside_restart_wait()` in `hermes_cli/kanban_worker_client.py`. The budget is a
constant in that file, not a config key: `OWNER_WAIT_S = 180.0`.

Past 180 s the worker raises and the card fails with
`Kanban owner refused: Kanban owner silent for <n>s`. The run never reached the task, so the failure
says nothing about the card body.

- Silence budgets of 180-190 s across several cards at once are this failure, not N independent
  bugs.
- Kanban workers are not counted among the drain's work units, so a drain reporting
  `waiting on 1 active work unit(s)` can still cut every worker.
- A chat session that is itself the last work unit holds the drain open, and every extra tool call
  in that session extends the outage.
- Never request a restart while cards are running: let the board drain first, or accept that each
  in-flight card fails one attempt and lands `blocked`.

## Failure: workers throttle each other

The dispatcher has no cap on simultaneous workers (`dispatch_interval_seconds: 60`,
`auto_decompose_per_tick`), so several cards can start within minutes of each other. Against a
per-minute provider limit they produce a `429` storm, and `api_max_retries` governs how long the UI
appears frozen while it backs off.

A `fallback_providers` entry naming the same model on the same account gives zero relief: it fails
on the same limit. Confirm the fallback model id differs from `model.default` before trusting the
chain.

## Failure: a card the dispatcher cannot see

`dispatch` only spawns assigned cards. A card that is `ready` with a null assignee reports
`(unassigned)` in `hermes kanban list` and stays there forever with no error and no event. Assign it
or it is not queued.

## Reading the database safely

`$HERMES_HOME/state.db` and `$HERMES_HOME/kanban.db` are WAL-mode; read them with `sqlite3` while
the gateway runs. Never write to either by hand - a direct write bypasses the claim lock and the
failure counter. The `tasks` table has no `blocked_reason` and no `attempts` column: block text is
`last_failure_error` and crash history lives in `task_events`.

Counting every table in `state.db` is slow because the FTS shadow tables are huge; query the table
you need instead of enumerating all of them.

## Claim → test

| Claim                            | Test                                                                                                            |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| A sweep is needed at all         | `uptime`, `memory_pressure \| tail -4`, `df -h /`                                                               |
| Workers are live, and how old    | `ps -eo pid,etime,command \| grep -E 'managed_worker\|kanban_worker_client'`                                    |
| The gateway is draining          | `grep 'Restart deferred' $HERMES_HOME/logs/gateway.log \| tail -1`                                              |
| A provider is throttling         | `grep 'RateLimitError' $HERMES_HOME/logs/gateway.error.log \| tail -3`                                          |
| Why a card is blocked            | `sqlite3 $HERMES_HOME/kanban.db "select id,substr(last_failure_error,1,160) from tasks where status='blocked'"` |
| A card will never dispatch       | `hermes kanban list` shows `(unassigned)` beside a `ready` card                                                 |
| The fallback can relieve a limit | `grep -A3 'fallback_providers' $HERMES_HOME/config.yaml` names a model different from `model.default`           |
