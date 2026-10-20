---
name: usage-limit-handoff
description: >-
  Stop-and-summarize protocol for when the account usage limit is nearly exhausted.
disable-model-invocation: false
user-invocable: false
license: Apache-2.0
---

# Usage limit handoff

The usage window is nearly exhausted. The goal is no longer finishing the task — it is stopping
at a clean boundary so the work can resume without archaeology. A hard limit cut-off mid-edit
loses more than the remaining budget can save.

The point of stopping _before_ the limit is that everything needed for a good handoff is still
in context. Reconstructing it afterwards from a transcript costs far more than writing it now.

## Procedure

### If you are a subagent

Do **not** write a handoff artifact. You see only your slice of the work, and your final report
goes to the calling session rather than the user. Finish the current atomic step, then stop and
report — as your final message — the guard trip, what you completed, and what remains. The main
session owns the artifact.

The rest of this protocol applies to the main session.

### Main session

Execute these steps in order, then end the turn.

1. **Close the current atomic step — start nothing new.** Complete the single edit, command, or
   file write in flight so nothing is half-applied; if it cannot be completed within a few tool
   calls, revert it instead and record it as open. Do not begin the next subtask, launch
   subagents or background tasks, or run validation that was not already in flight.
2. **Secure unsaved state.** If uncommitted changes exist and committing was already authorized,
   commit them; otherwise leave the working tree as-is and describe its state in the artifact.
   Never commit or stash unprompted just because the session is ending: the end of a session
   authorizes no change to the user's working tree.
3. **Save the handoff.** Invoke the Skill tool with skill="ceh-every-session:hand-off-session"
   and args `save`, and follow its save procedure: it writes the artifact under
   `.agents_workspace/handoff/`, appends the line to the global index at
   `~/.claude/handoff/index.md`, and reports the content as your message. Add this header line
   under the artifact's title, from the guard message:
   `**Window:** <name> at N%, resets at HH:MM`
4. **End the turn.** Do not resume work in this session unless the user explicitly says to
   continue — they may prefer to wait for the window reset reported by the guard message.

## Rules

- The trigger is the `usage-limit-watch.py` PostToolUse hook in this plugin. It fires at
  `CEH_USAGE_LIMIT_THRESHOLD` (default 90%) against whichever window is closest to its cap —
  the 5-hour and weekly windows both trigger it — and re-fires every 5 points above that. A
  repeat warning means the first one was ignored; stop immediately.
- The quota reading is account-wide: claude.ai web, desktop, mobile and Claude Code all draw
  from the same pool, so usage can climb without this session doing anything.
- If the guard fires while mid-handoff, ignore it: the protocol is already running.
- Resume with `/ceh-every-session:hand-off-session load` in a fresh session rather than
  replaying the old one with `--resume` — the replay spends the quota that just reset.
