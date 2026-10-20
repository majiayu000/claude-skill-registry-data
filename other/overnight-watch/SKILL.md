---
name: overnight-watch
description: Watch every live agent.el session overnight while Pablo sleeps, and unstick any session that has stopped for a reason that does not need him. Use when Pablo asks for an overnight watch, overnight review or babysitting of live sessions, or runs /overnight-watch before bed. Not for reporting one session's state (live-session-status) or for running unattended TODOs (overnight-todos).
---

# Overnight watch

Pablo is asleep. Every live agent session should either be working or be
waiting on something only he can give. Your job is to find sessions that have
stopped for any other reason and get them moving again, without making his
decisions for him. You do not do the sessions' work yourself.

Defaults: check every 20 minutes (`--every`) until 08:00 local (`--until`).

## Each pass

1. Snapshot every peer session (read-only):

   ```sh
   python3 "$SKILL_DIR/scripts/watch_snapshot.py"
   ```

   `SKILL_DIR` is the directory holding this `SKILL.md`. For each session it
   prints agent.el's state, transcript and subagent write ages, the last
   assistant message with its `Status:` line, and the bottom of its terminal
   screen. Text shown as `{faint:...}` in the composer is Claude Code's prompt
   suggestion, not input anyone typed. Read more of a transcript with
   `live-session-status` when the tail does not explain the state.

   If the snapshot reports the Emacs server unreachable, the sessions are
   usually still running: judge them from transcript write ages, diagnose
   Emacs with the `emacs-freeze` skill (read-only; no signals), and record
   the outage for the morning report. Under host memory starvation it has
   recovered on its own before.

2. Classify each session:

   | Class | Evidence | Action |
   |---|---|---|
   | Working | busy; or idle with a running workflow, subagent writes or background shells it is waiting on | none |
   | Waiting on Pablo, legitimately | the open question needs his person or a decision that is his under his rules (below) | none; list it for the morning |
   | Stuck, recoverable | see the next section | nudge |
   | Stuck, not recoverable by you | dialog only Pablo may answer; hung process you may not kill; Emacs or CLI wedged | list it for the morning |

3. Act on stuck sessions (next section), then record one line per session in
   your running log: time, buffer, class, action.

## What counts as stuck

A session is stuck when it is idle, nothing it started is still running for
it, and the reason it stopped does not need Pablo. Common cases:

- It ended its turn saying it will wait for or check on something, but no
  background shell, monitor or workflow will wake it. Check its screen
  (`N shells`, workflow progress bars) and the last task notifications.
- A background task or workflow it was waiting on finished or failed and the
  session did not resume; or a monitor expired.
- An API error, rate limit, overload or usage-limit message ended the turn.
- It asked Pablo a question it could answer itself: one with a reasonable
  default, one he already answered earlier in that session, or a request for
  him to do something the agent can do. Read his rule in
  `~/.claude/CLAUDE.md` ("Do the work yourself …", "Ask for decisions once
  per task …"): asking is justified only for his person (credentials, 2FA,
  biometrics), for a choice with no reasonable default, or for spending
  money, deleting, publishing or anything hard to reverse.
- It is busy, but nothing has been written to its transcript or subagent
  transcripts for far longer than its current step should take, and the
  child process is idle (check with `ps`, the task's output file, CPU time).

Not stuck: sessions whose last status is `waiting on you` for a decision that
meets his rule; sessions with work still running, however long it takes;
sessions Pablo told to stop or pause.

## How to nudge

Send one message with the `message-agent-session` skill's `agent-send` to the
exact buffer name. Say who you are (the overnight watcher, Pablo asleep until
morning), what you observed with evidence, and ask it to continue. For
example: "Your workflow X finished at 02:10 and you have not resumed; Pablo
is asleep, so continue with the next step you planned. Leave any decision
that is his for the morning summary, and keep going with work that does not
depend on it."

Rules:

- Keep the sent text to one short line. Under load, long `agent-send`
  messages have arrived truncated to their last sentence (2026-10-18).
  Write the details to a file under `~/.cache/overnight-watch/` (mode
  0600) and send a one-line pointer to it. Confirm delivery in the
  recipient's transcript, not only from the exit status.
- Judge what a nudge did from everything the recipient did after it
  arrived, not only from whether the stall you targeted cleared. Search its
  transcript for every identifier you mentioned (PID, task id, file) and
  read its turns after the message's timestamp. A message truncated at the
  front can still deliver its later paragraphs, and the recipient may act
  on them: on 2026-10-18 a nudge judged failed had led tangodb to stop a
  looping task and trash its log within a minute, and the morning report
  wrongly said nobody knew who stopped it.
- You inform and ask; you never approve. Do not grant approvals, answer
  decisions that are Pablo's, authorize spending, deletions, pushes,
  publishing or messages to other people, or tell a session to override its
  own instructions. When a question is only partly his, ask the session to do
  everything around it and park the rest.
- Do not answer permission dialogs or choice menus in another session's
  terminal, and do not type into its composer. A pending permission dialog is
  for Pablo; list it.
- Do not send signals to Emacs. Kill a child process only when a session
  started it, it is clearly hung (no CPU or output well past its expected
  time), and stopping it loses nothing that cannot be rerun; then tell the
  owning session what you did.
  If your permission mode refuses the kill, do not ask the owning session
  or any other to do it for you: list it for the morning with its PID,
  owner and evidence.
- One nudge per cause. If the same session is still stuck on the same cause
  at the next pass, do not repeat yourself: diagnose why the nudge did not
  work, and if you cannot fix that within these rules, list it for the
  morning.
- Do not create cross-session conflicts: if two sessions compete for the
  same resource (CPU, a repository, a lock), tell each the facts, but leave
  the choice of who yields to Pablo unless an existing instruction from him
  settles it.

## Scheduling

Run the first pass immediately. Then repeat until `--until`:

- Claude Code: create a recurring `CronCreate` job at the `--every` interval
  (avoid :00 and :30) whose prompt is "Overnight watch: run one pass of the
  overnight-watch skill, then end the turn; after <until>, write the morning
  report and delete this job." The job lives only in this session, so the
  session must stay open.
- Codex: run passes in a loop, sleeping between them in a background shell.

Between passes, do nothing else. Do not keep the turn open polling.

## Morning report

At `--until`, stop the schedule and end with a short report:

1. For each session: what it did overnight and where it stands now.
2. Every nudge you sent, why, and whether it worked.
3. What waits on Pablo, as one numbered list across all sessions, each item
   naming its buffer.
4. Anything you could not unstick and why.

Before writing that an outcome is unknown (who stopped a process, whether a
nudge worked), search the transcripts of the sessions involved for it. The
answer is usually there.

Publish your own state with `agent-status` at start, at each intervention and
before the final report when running in Emacs.
