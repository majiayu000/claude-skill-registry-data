---
name: recover
description: After an interruption (network drop, API error, credits or quota exhausted, rate limit, Esc, crash, machine sleep), work out what was in flight, check the health of this session's subagents, teammates and background jobs, then retry or resume each piece as appropriate. Use when the user types /recover or says there was an interruption and to retry or resume.
disable-model-invocation: true
argument-hint: "[optional note on what was interrupted]"
---

# recover

Something interrupted this session. Find out what was in flight, check every
worker this session owns, then retry or resume each piece. Don't redo work that
already landed, and never repeat an action outside the machine.

User note, if any: `$ARGUMENTS`

## 1. Work out what was in flight

- Read back from the end of the conversation. Find the last user request, how far
  you got, and any tool call that has no result or ended in an error.
- Read the work-state lists (`work_state_read`, includeClosed=false) and any plan
  file you were executing. Items marked `doing` are suspects.
- Note any mid-turn user message you hadn't addressed yet. It still counts.

## 2. Name the cause, because it decides the response

| Sign | Cause | Response |
|---|---|---|
| connection reset, timeout, 5xx, `overloaded` | transient | retry once now; if it fails again, wait briefly and retry once more |
| `429`, rate limit | rate limit | wait the stated time, or a minute, then retry. Never loop fast |
| credits, quota, billing, usage limit | exhausted | **don't retry**: report which workers stopped and what each needs, and wait for the user |
| `Interrupted by user`, Esc | the user stopped you | **don't redo it blindly**: say where it stopped and ask whether to continue that step, unless the user's message already says to |
| auth expired (SSO, OAuth, MCP login) | credentials | tell the user the exact login command; don't work around it |
| context summary just happened | compaction | trust the summary for intent and re-check facts on disk |
| none visible | unknown | treat it as transient, but verify before redoing |

## 3. Check the health of every worker this session owns

Check them all, and run independent checks in parallel.

- **Teammates:** run `~/.claude/skills/team-teardown/scripts/reap-teammates.sh --idle`
  as a dry run. Its IDLE lines are your idle teammates. Then check your team's
  panes: `tmux list-panes -a -F '#{pane_id} #{pane_dead} #{pane_dead_status} #{session_name}:#{window_index}'`
  and match them against `~/.claude/teams/session-<first 8 chars of your session id>/config.json`
  (members and their `tmuxPaneId`).
  - Working: leave it running, and note what it's on.
  - Idle with its lane unfinished: SendMessage it to continue, restating the lane
    in one line.
  - Idle and finished: collect its report if you never received it, by asking it
    to resend.
  - Dead pane or exited process: respawn it with the same brief and a new name
    suffix. Exit status 127 after an upgrade means the binary moved, and the
    session itself needs a restart: tell the user.
- **Background subagents:** any agent you launched without a completion
  notification. Check its transcript under
  `~/.claude/projects/*/<session id>/subagents/`. A file updated in the last
  couple of minutes means it's still running; leave it. A stale file means it
  died: relaunch it with the same prompt.
- **Background shells, Monitors, crons:** check that each is still running
  (CronList for crons; the job's output file or process for the rest). Restart
  only what is needed and isn't running.
- **Other sessions' workers** (panes in windows you don't own, other team ids):
  report them, never touch them.

## 4. Before redoing any step, check whether it already happened

An interrupted call may have succeeded before the error came back.

- File writes and edits: read the file. Is the change there?
- Commits: run `git log -3` and `git status`.
- Anything visible outside the machine (Slack or email message, PR or comment,
  push, deploy, pipeline run, ticket, MCP write): **look for it first** (read the
  channel or thread, `gh pr list`, `gh run list`). Redo it only if it is
  definitely absent. If you can't tell, ask; don't risk a double post or deploy.
- Installs, migrations, state changes: inspect the current state before running
  anything again.

## 5. Resume

Carry on with the remaining work in its original order, under the same
permissions and constraints as before. An interruption doesn't widen what you
may do. Update work-state items as they finish.

## 6. Report

Lead with a short table:

```
| Item | Was | Now |
|---|---|---|
| <step or worker> | <interrupted / dead / idle / fine> | <retried ✓ / resumed / already done / waiting on you: …> |
```

Then one line on the cause, if known, and anything that needs the user, such as
a login, credits or a decision. Keep the rest of the update brief.
