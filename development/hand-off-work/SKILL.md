---
name: hand-off-work
description: Save state so that another agent or a later session can continue without guessing. Use this when you must stop before a task is finished, when context is running out, when you pass work to another agent, or when you pick up work someone else started.
---

# Hand off work

The next agent knows only what you wrote down. A vague note makes them repeat your
work or trust something that was never true.

## When to use

- You are stopping before the task is finished.
- A long task reaches a natural checkpoint.
- You are continuing from someone else's notes.

## Steps

1. **Leave the code in a known state.** Make sure that it builds, or say clearly
   that it does not. Remove temporary logging. Use a work-in-progress commit on your
   own branch if the user allows commits. Do not use a shared stash, because other
   sessions can pop it.

2. **Separate facts from guesses.** Mark what you verified by running it, and what
   you only believe.

3. **Record what failed.** Dead ends are the most valuable part of a handoff,
   because they stop the next agent from repeating them.

4. **Write the handoff.** Use the template below, and put it where the next agent
   will look, such as the PR description or a file the user chose.

5. **Name the single next step.** Make it specific enough to start immediately.

## When you receive a handoff

Treat the note as a lead, not as evidence.

1. Check the branch, the last commits and `git status`.
2. Rerun the checks it says pass.
3. Confirm any key claims against the code.
4. Continue from the next step. If the note and the code disagree, trust the code,
   and say so.

## Stop and ask when

- The state cannot be made safe to leave, such as a half-applied data change.
- The work needs a decision only the user can make.

## Common mistakes

| Tempting move | Why it fails | Do this instead |
| --- | --- | --- |
| Write "almost done" | Tells the reader nothing | List what remains |
| Leave out failed attempts | They get repeated | Record each with its reason |
| State a guess as fact | The next agent builds on it | Label it |
| Trust the previous summary | It may be wrong or stale | Check it against the code |
| Leave uncommitted work without saying so | It gets lost | State where the work is |

## Report

```markdown
Goal: <one sentence>
Branch and state: <branch, last commit, uncommitted work, builds or not>

Done and verified:
- <item>: <command and result>

Done but not verified:
- <item>

Tried and failed:
- <approach>: <why it failed>

Open questions: <decisions needed>
Next step: <one specific action>
```
