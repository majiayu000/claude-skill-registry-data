---
name: using-monitors
description: "USING thrum monitor to schedule reminders, periodic script checks and pane nudges; use when asked to set up a monitor or verify one delivered"
---

# Thrum Monitors - Reminders, Pane Prompts And Script Checks

## Overview

A monitor runs a command, keeps the output lines that match a regex, and
delivers them as Thrum messages to a target: a continuous monitor sends each
kept line, a scheduled monitor sends all the lines of a run in one message. With
`--schedule` it runs the command once per cron tick; without it the command runs continuously
and restarts with backoff when it exits. Monitors persist across daemon
restarts and run only on the daemon that owns them.

A monitor reaches an agent in two ways. Its matched lines arrive as inbox
messages, read at the next inbox check. Its command can also be a script that
runs `thrum tmux send` to put a short prompt into the agent's own pane, which
starts a turn. Keep the wording and logic of anything that will change in a
script file: you then edit the script, and the monitor stays as it is.

## Why A Script File

Put a monitor's command in a script file at a stable path, not inline:

- The command, its arguments, `--cwd` and `--env` are fixed when the monitor
  starts. Changing an inline command means deleting the monitor and starting a
  new one, which drops its run history and health record and leaves a gap with
  no check running. An edited script takes effect on the next tick.
- A script can be tested by hand before it is wired up. Run it with the send
  step removed and read what it would deliver: a pattern that matches far too
  much or nothing at all shows up here, not in the target's inbox.
- A script that types into a pane uses `thrum tmux send`, never raw
  `tmux send-keys`. `thrum tmux send` waits for the pane to be idle and for a
  human to finish typing, checks for an open dialog before pressing Enter, and
  sends text and Enter in one call. Raw `tmux send-keys` skips all of that and
  can type into someone's half-written input or answer a dialog.

Every flag below appears in `thrum monitor start --help`. Re-read the help
before relying on a flag not listed here.

## Command Surface

```bash
thrum monitor start --name <n> --match <re> --to @agent [--schedule "<cron>"] \
  [--notify-on-success] [--debounce 60s] [--env K=V] [--cwd <dir>] -- <cmd> [args...]
thrum monitor list [--all]
thrum monitor show <name|id>
thrum monitor logs <name|id> [-n 50]
thrum monitor update <name|id> [--match <re>] [--to <t>] [--debounce <d>] [--schedule "<cron>"]
thrum monitor stop <name|id>
thrum monitor restart <name|id>
thrum monitor delete <name|id>
```

- `--name`, `--match` and `--to` are required; the command follows `--`.
- The daemon accepts caller-relative target aliases on start/update and persists
  the registered caller's concrete ID. Register the runtime with
  `thrum quickstart`, or give an explicit recipient. Repair a legacy unresolved
  alias with `thrum monitor update <id> --to @<agent>`, then restart; list/show
  display its unresolved-target warning.
- `--schedule` takes a 5-field cron expression. `update --schedule` changes the
  cron of a scheduled monitor at any time. Setting a first schedule or removing
  it (`--schedule ""`) switches the mode, which is refused while the monitor is
  running and allowed while it is stopped.
- `--debounce` is leading-edge with a 30s minimum (default 1m).
- `update` changes only the match, target, debounce and schedule. The command,
  its arguments, `--cwd` and `--env` are fixed when the monitor starts, so text
  written inline in the command can be changed only by deleting the monitor and
  starting a new one. Text kept in a script file is changed by editing the file.
- `--cwd` is the working directory the command runs in (default: the directory
  you start the monitor from). `--env` adds one `KEY=VALUE` variable to the
  command's environment and can be repeated.
- `stop` leaves a stopped record that still holds the name; `delete` frees the
  name. Use a unique name per monitor.

## What Is Delivered

Each output line is tested against `--match` on its own. A line is truncated at
2048 bytes with a marker appended.

Read generated summaries as `<name>@<host>` and system notices as
`[monitor:<name>@<host>]`; an unavailable hostname omits `@<host>`.
Matched summaries show up to 160 characters of the deciding line; read the full
matched output below, within the existing output and message limits.

A scheduled (`--schedule`) job is a one-shot run, so its exit code is
authoritative. It delivers ONE message at exit that carries every matched line,
in order. A continuous job has no exit code per line, so it classifies and
delivers and classifies each matched line on its own, by its words.

| Scheduled job                                                   | Delivered as                                  |
| --------------------------------------------------------------- | --------------------------------------------- |
| Non-zero exit                                                  | `[FAIL] <name>@<host>: exit code N` with the output tail, then the matched lines |
| Command failed to start                                         | `[FAIL] <name>@<host>: <start error>` with details and an inspect command |
| Exit 0, a matched line starts `ERROR:`, `FATAL:` or `FAIL:`     | `[FAIL] <name>@<host>: <matched line>` + all matched lines |
| Exit 0, highest prefix is `WARN:`, `WARNING:` or `ALERT:`        | `[WARN] <name>@<host>: <matched line>` + all matched lines |
| Exit 0, lines matched, no such prefix                           | All matched lines, in order, verbatim         |
| Exit 0, nothing matched, `--notify-on-success`                  | `[OK] <name>@<host>: succeeded`                      |
| Exit 0, nothing matched                                         | Nothing (logged only)                         |

Cadence: the first non-zero scheduled run sends its `[FAIL]` notice; repeats of
that failure are not sent again until the outcome changes or the re-escalation
interval (30 minutes) passes. An exit-0 run that matched lines sends its message
on every run.

On a scheduled job only these prefixes, at the very start of a line, label the
output, with the colon directly after the word: `ERROR:`, `FATAL:` and `FAIL:`
fail it; `WARN:`, `WARNING:` and `ALERT:` warn. Any other prefix, including
`ALERT-<NAME>:`, `ERROR :`, `INFO:`, `OK:`, `NOT_OK:` and lowercase forms, is
neutral. They are read before any wording in the body, and
the highest one decides the label. Words such as `done`, `ok`, `complete`, `failures` or `error` neither
drop nor relabel a line, and `WARN: batch not complete` stays a warning.
`--notify-on-success` adds the generic `[OK]` only for a run in which nothing
matched; an empty matched line counts as a match and is announced as
`[matched N empty line(s)]`.

The whole message, including its label and framing, never exceeds the daemon's configured message-body limit. Matched
lines are sent whole while they fit both budgets: the in-memory retention budget (each line costs its bytes plus a small
fixed overhead, so a line close to the limit, or many short lines, can be cut or omitted earlier than their plain total
would suggest) and the final rendered message including its label. Lines that do not fit are replaced by
`[N more matched lines omitted]`, and a first line that does not fit is cut and marked. The limit is never below 1024
bytes (the configuration floor), enough for the framing and an omission marker with ordinary job names; when variable
framing such as a very long job name does not fit, the monitor sends a bounded summary that starts with `+N omitted`
instead of the lines. A run keeps only a bounded prefix of its lines in memory (at most the delivery limit, or 1 MiB
when the limit is disabled, counting a small fixed overhead per line) but counts every match, so the omitted count is
exact and an `ERROR:`/`WARN:` line past the retained prefix still sets the label.

| Continuous job (no `--schedule`)                                | Delivered as                                  |
| --------------------------------------------------------------- | --------------------------------------------- |
| Contains `error`, `fatal`, `fail`, `permission denied`          | `[FAIL] <name>@<host>: <matched line>` + line |
| Contains `warn` or `warning`                                    | `[WARN] <name>@<host>: <matched line>` + line       |
| Contains a whole word `success`, `succeeded`, `complete`, `completed`, `done`, `ok` | Not delivered (logged only)   |
| Any other matched line                                          | The line, verbatim                            |

A continuous job checks a line for a negated completion word (`not complete`)
first, then for a level prefix (`ERROR:`, `WARN:`, `INFO:`, optionally after a
timestamp), then for the words above. Tokens such as `fail=0` are not failures;
the phrase `0 errors` still contains `error`.

Delivery limits:

- A continuous job delivers the first matching line in each debounce window at
  once and holds later ones for a trailing summary. A scheduled job has no
  debounce; its lines are aggregated as above.
- The `[FAIL]` body for a non-zero exit carries only the last 500 bytes of
  output, so the message that matters goes last.

## Choosing A Reminder Form

| Need                                                              | Form                          |
| ----------------------------------------------------------------- | ----------------------------- |
| Fixed wording, enough that it is read at the next inbox check     | Inbox reminder                |
| Must start a turn, or the wording will change as the work moves   | Pane prompt through a script  |
| A probe that reports a finding only when something is wrong       | Script check                  |

A reminder that arrives, in the inbox or in the pane, shows the schedule fired.
It does not show that the work moved. Check the work itself (commits, queue,
state) before treating the reminder as progress.

## Inbox Reminder

An inbox reminder is a monitor whose command only prints a fixed line. Give the
line a stable prefix and match exactly that prefix.

```bash
thrum monitor start --name standup-nudge --to @<your_agent_name> \
  --match '^REMINDER-STANDUP:' --schedule "0 9 * * 1-5" -- \
  echo "REMINDER-STANDUP: post the status update, then reply to the open review"
```

- Schedule the reminder; words in its text, including "failures", "error" and
  "done", then neither relabel nor drop it, and the exit code decides success.
- Make the body an instruction with the next concrete step; a bare "reminder"
  carries no action.
- Add `--notify-on-success` only when a delivered line must be guaranteed for a
  run that matched nothing.
- An inline `echo` suits wording that will not change. For wording that will
  change, use a pane prompt through a script.

## Pane Prompt Through A Script

Use this form for a recurring nudge that must start a turn, and for any reminder
whose wording follows the work. The standard case is plan follow-up: a
brainstormer or plan owner schedules a prompt that tells it to check how
implementation of its plan is going and to notify the coordinator or the
orchestrators working on the plan if blockers have not moved.

The monitor runs a script file. The script runs
`thrum tmux send <your-agent> "<prompt>"`: the daemon types the text into the
pane and submits it. The prompt text and all logic live in the script.
The target runtime's composer may interpret @name as a file mention; use bare
agent names in pane prose and thrum send --to for message addressing.

Put the script at a stable path you own, outside tracked source, that survives a
restart of your session. Use its absolute path in the monitor command.

```bash
#!/usr/bin/env bash
# plan-nudge.sh: prompt my own pane to follow up on my plan.
# Edit AGENT and PROMPT when the plan moves. The monitor stays as it is.
AGENT="<your-agent>"
PROMPT="Check how implementation of <plan> is going. If the blockers have not moved since the last check, notify the coordinator or the orchestrators working on it."

T=$(command -v timeout || command -v gtimeout)
if [ -n "$T" ]; then "$T" 30 thrum tmux send "$AGENT" "$PROMPT" >/dev/null 2>&1; else thrum tmux send "$AGENT" "$PROMPT" >/dev/null 2>&1; fi
rc=$?
case "$rc" in
  0) exit 0 ;;
  3 | 4)
    echo "WARN: PLAN-NUDGE send exit $rc, the prompt was typed into $AGENT but its submit is not confirmed; look at the pane"
    exit 0
    ;;
  *)
    echo "PLAN-NUDGE: thrum tmux send to $AGENT failed with exit $rc"
    exit "$rc"
    ;;
esac
```

```bash
chmod +x <script-dir>/plan-nudge.sh
<script-dir>/plan-nudge.sh    # run once by hand: the prompt lands, nothing prints

thrum monitor start --name plan-nudge-<your-agent> --to @<your-agent> \
  --match 'PLAN-NUDGE' --schedule "0 */2 * * *" --cwd <your-worktree> -- \
  <script-dir>/plan-nudge.sh
```

Exit codes of a text `thrum tmux send`, from its help:

| Exit  | Meaning                                                           | Script does                          |
| ----- | ----------------------------------------------------------------- | ------------------------------------ |
| 0     | Delivered                                                         | Prints nothing, exits 0              |
| 3     | Held: the text was typed, the confirming Enter was withheld       | Prints a `WARN:` line, exits 0       |
| 4     | Verdict unknown: Enter may or may not have been sent              | Prints a `WARN:` line, exits 0       |
| 1     | Any other error                                                   | Prints the finding, exits non-zero   |

What the monitor then delivers to `--to`, per the scheduled-job table above:

| Script outcome                         | Target receives                              |
| -------------------------------------- | -------------------------------------------- |
| Prompt delivered                       | Nothing in the inbox; the prompt in the pane |
| Exit 3 or 4                            | One `[WARN]` message for that tick           |
| Any other non-zero exit, or the `timeout` (124) | One `[FAIL] <name>@<host>: exit code N` message with the finding line |

Rules:

1. Keep the prompt to one or two sentences. It is a nudge; the plan and your
   state hold the detail.
2. When the plan moves (a blocker clears, a new one appears, a different
   orchestrator owns the work), edit the script. The next tick uses the new
   text. Do not run `thrum monitor update` and do not delete and recreate the
   monitor for a change of wording or logic.
3. Change the monitor only for what the monitor owns: `update --schedule` for a
   new cadence, `update --to` for a new recipient of failure notices.
4. Bound the send with `timeout`; a hung send holds the tick.
5. Never call raw `tmux send-keys` from a monitor script. `thrum tmux send` is
   the only way a script types into a pane (see Why A Script File).
6. Target your own pane. Prompt another agent's pane only when that agent's
   owner asked for it.
7. Never send the text a second time from the script. After exit 3 or 4 the text
   may already sit in the pane: look at the pane and submit or clear it. The
   next tick sends again by itself.
8. Keep the output quiet on success. A matching line on every tick fills the
   inbox with the reminder the pane already received.
9. Start the monitor with `--cwd` set to your own worktree, so the send runs
   from the checkout that carries your identity.

## Script Check

A script check runs a bounded, synchronous probe and reports through its exit
code and one structured line.

```bash
#!/usr/bin/env bash
# disk-check.sh: report the root volume when it passes the threshold.
LIMIT=90
T=$(command -v timeout || command -v gtimeout) || exit 2
u=$("$T" 10 df -P / | awk 'NR==2 {print $5}' | tr -dc 0-9)
[ "$u" -lt "$LIMIT" ] && exit 0
echo "CHECK-DISK: root volume at ${u} percent used, free space then rerun df -h /"
exit 3
```

```bash
chmod +x <script-dir>/disk-check.sh
thrum monitor start --name disk-check --to @<your_agent_name> \
  --match '^CHECK-DISK:' --schedule "*/15 * * * *" -- <script-dir>/disk-check.sh
```

Change the threshold or wording by editing the script; the monitor stays.

Rules:

1. Bound every probe with `timeout <secs>`; a hung probe holds the tick.
2. Exit 0 for healthy and print nothing matching, which keeps the run quiet.
3. Exit non-zero for a failure; the daemon sends the `[FAIL]` notice with the
   exit code and output tail.
4. Print a matching line that names the subject, the observed value and the
   next action. A generic `OK` or `done` line carries no information.
5. Use a distinct stable prefix per outcome (`CHECK-DISK:` for a finding,
   `REMINDER-DISK:` for a nudge) so `--match` selects what must reach the
   target.

| Outcome  | Script does                              | Target receives                    |
| -------- | ---------------------------------------- | ---------------------------------- |
| Quiet    | Exit 0, no matching line                 | Nothing                            |
| Failure  | Non-zero exit, finding line last         | One `[FAIL] <name>@<host>: exit code N` message with the tail and the finding line |
| Finding  | Exit 0, matching line(s)                 | The line(s), verbatim (labeled only by an `ERROR:`/`FATAL:`/`FAIL:` or `WARN:`/`WARNING:`/`ALERT:` prefix) |
| Reminder | Exit 0, one stable-prefix instruction    | The line, verbatim                 |

A `--match` that never matches the script's real output delivers nothing and
raises no error. Test the regex against the exact output before starting.

## Verify By Delivery

Start the monitor with a unique name, `--to` the verifying agent, and a
one-minute schedule, then read the delivered message back in full.

```bash
thrum monitor start --name verify-<unique> --to @<your_agent_name> --match '^VERIFY-<unique>:' \
  --schedule "* * * * *" -- echo "VERIFY-<unique>: delivery body check"
thrum inbox --unread
thrum message get <message-id>      # the complete delivered body
thrum monitor logs verify-<unique>  # the matches the daemon recorded
thrum monitor delete verify-<unique>
```

Confirm the body carries the prefix, the wording and no unexpected `[FAIL]`
or `[WARN]` label. Delete the monitor when done; never alter a monitor another
agent owns.

A pane prompt sends nothing to the inbox when it works. Verify it by running the script once by hand and seeing the
prompt in the pane, then by `thrum monitor show` reporting exit 0 after the first tick.

## Troubleshooting

- Nothing arrived: `thrum monitor show` for state and last exit, `thrum monitor logs` for recorded matches. No recorded
  match means the regex did not match, or (continuous job) the line was completion-classified and suppressed; run the
  command by hand and compare its output with the regex.
- Message labeled `[FAIL]` unexpectedly: the job exited non-zero, the line starts
  with `ERROR:`/`FATAL:`/`FAIL:`, or (continuous job) the line contains a fail or
  error substring.
- Name already in use: a stopped record holds it. `thrum monitor delete` it.
- Pane prompt did not appear: `thrum monitor show` for the last exit, then run
  the script by hand. Check that the script path is absolute and executable,
  that the agent name in the script is current, and that the monitor's
  `--cwd` is your worktree.
- Pane prompt shows the old wording: the script was not saved, or the monitor
  was started with a different script path than the one you edited.
- `[WARN]` naming a held or unknown send: the text may sit unsubmitted in the
  pane. Look at the pane and submit or clear the text. Do not send the text
  again by hand; the next tick sends it.
