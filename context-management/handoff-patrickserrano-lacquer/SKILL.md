---
name: handoff
description: >
  Write a structured handoff document before a session ends, before a
  context-heavy interruption (SSH/tmux disconnect, context running low, a
  worktree being handed to another worker or agent), or when explicitly
  asked for a handoff — captures progress, what worked/failed, and the exact
  next step so a fresh session can resume without re-deriving context. Own
  version of the dx plugin's `/dx:handoff`.
---

# Handoff

A handoff doc exists to save the *next* reader (a fresh session, a different
agent, or you tomorrow) from re-deriving everything this session already
figured out. Write for someone with zero memory of this conversation, not a
recap for someone who was watching.

## What to include

- **Goal.** One sentence: what this session was actually trying to accomplish.
- **Done — verifiably.** What's complete, stated as a fact a reader can check
  (a commit hash, a passing test name, a file path with the final content) —
  not "implemented X" without a way to confirm it.
- **In-flight / blocked.** What's partially done, and specifically *why* it
  stopped — a failing test with its actual output, a decision waiting on the
  user, an external dependency not yet available. "Ran out of time" without a
  concrete blocker is not useful to the next reader.
- **Explicitly not done.** Anything the goal implies but this session didn't
  touch — cheap to state, expensive for the next reader to discover by
  assuming it's covered.
- **Next concrete step.** Not "continue the work" — the literal next action:
  which file, which command, which decision needs making first.
- **Decisions made and why.** Only the ones that weren't obvious — a
  constraint that ruled out the default approach, a tradeoff chosen
  deliberately. Skip anything a reader could re-derive from the diff itself.

## Where it goes

Don't silently create or overwrite a tracked file. Ask where it belongs if
unclear, or default to an untracked scratch location (e.g. a `HANDOFF.md` at
the repo root, gitignored, or the session's own scratchpad) — a handoff doc
is working state, not something that should land in a PR by accident.

## Keep it short

If the honest answer to "what's done" is "everything, cleanly" — say that in
one line and stop. A handoff doc's value is proportional to how much
re-derivation it saves, not its length.
