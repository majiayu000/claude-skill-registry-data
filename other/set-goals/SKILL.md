---
name: set-goals
description: Write or renew the project's 6 week goal in GOALS.md, and close the previous cycle in a few lines drafted from git history. Walks the stages from a working loop on your phone, into the stores, to the first 100 weekly users and beyond, each with a default goal to edit. Use when the user says "set my goal", "new cycle", "what should I focus on", "my goal ended", or when session end has said the current cycle is over.
---

# Set goals

One small file, `GOALS.md`, holds one 6 week goal. This skill writes it, renews it
when the cycle ends, and closes the old cycle in a few lines. The point is a plan
that never goes stale silently, not a planning ritual.

The file format is fixed. Setup writes it from `templates/goals.md` in the setup
skill and session end reads it, so keep exactly these headings:

```markdown
# Goals

## Current cycle: <YYYY-MM-DD> to <YYYY-MM-DD>

**Goal:** <one sentence, with the end date>.

**The one number:** <what shows it is working, and its target>.

**Must dos:**

- [ ] <must do>

**Not this cycle:** <what you are deliberately not doing>.

**Gate to the next stage:** <what has to be true before moving on>.

## Past cycles

Closed cycles move here, newest first, each with a few lines on what happened.
```

## Rules

- **One question at a time**, each with a default, so "yes" or a few words is
  enough. Same style as setup.
- **Read before asking.** Read `GOALS.md`, `CURRENT_WORK.md`, the rules file and
  `app.json` first. Only ask what they do not answer.
- **Never nag.** Do not raise goals unless the user asked or invoked this skill.
  If they are behind, say it once, plainly, then help.
- **Never mark anything done without the user confirming it.**
- **Never overwrite** `GOALS.md` without showing the change and getting a yes.
- Dates in `YYYY-MM-DD`. A cycle is 6 weeks: the end date is the start plus 42 days.
- Plain words. No long dashes in anything you write into the file.

## 1. Find out where things stand

Read `GOALS.md` and pick one case:

| Case | What to do |
| --- | --- |
| No file | Go to step 3. Mention that setup normally writes this file, then carry on. |
| Current cycle, end date passed | Step 2, then step 3. |
| Current cycle, still running, user asked to start over | Step 2 (close it early, say so in the lines), then step 3. |
| Current cycle, still running, "what should I focus on" | Step 4 only. |

## 2. Close the cycle

1. Run `git log --since=<cycle start> --oneline` and read `CURRENT_WORK.md`.
2. Ask **once**, in one block, about work that leaves no commit: store approvals or
   rejections, testers who actually opted in, account or payment setup, people
   talked to, the one number's current value. Offer "nothing else" as the default.
3. Draft the closing lines yourself from the commits and the answers. A few lines,
   no more:

   ```markdown
   ### <start> to <end>: <the goal, short>

   Met / partly met / not met. The one number: <target>, ended at <actual or "not measured">.
   Done: <must dos finished, in plain words>. Dropped: <open must dos, one reason each>.
   Learned: <one line worth carrying into the next cycle>.
   ```

4. Show the draft and ask "Anything to change?" Default: keep it.
5. Move it under **Past cycles**, below the intro line and above older entries
   (newest first). Never rewrite or delete older past cycles.

Describe what a person can now do with the app, not code names. "Purchases work
on a real phone" beats "fixed the purchase hook".

## 3. Set the next cycle

Work out the stage from the last gate, the closed cycle and the project state,
then confirm it in one line: "Looks like you are at **into the stores**. Right?"
Stages and their default goals are in `references/stages.md`. If the last gate
was not met, the default is to stay on the same stage with a smaller goal, not
to move on.

Then ask, one at a time, each with the stage default filled in for this app:

1. **The goal.** One sentence with the end date. Offer the default, edited to fit
   the app's own loop.
2. **The one number.** What shows it works, with a target. One number, not a
   dashboard. If it cannot be measured yet, measuring it becomes a must do.
3. **Must dos.** 3 to 5, each small enough to tick. Default: the stage's list
   plus any dropped must do from the closed cycle that still matters. Order them
   so the last one is the first to cut on a bad week, and say so.
4. **Not this cycle.** The things they will be tempted by. Default: the stage's
   anti goals plus anything from the backlog that looks shiny. Remind them that
   new ideas go to the backlog, not into this cycle.
5. **Gate to the next stage.** Default from the stage.

Before writing, check for things that run on the calendar rather than on effort:
store review times, tester periods, account verification, a name that blocks the
listing. If one applies, the must do that starts that clock goes first. Check the
current official rule before stating a store requirement; do not quote numbers
from memory.

Write the new **Current cycle** section, show the whole file change, and write it
on a yes. Offer to commit `GOALS.md` alone.

## 4. Mid cycle: what to focus on

Do not rewrite anything. Read the current cycle and recent commits, then answer in
a few lines:

- Days left, must dos ticked and open.
- The one open must do to do next, and why (calendar clocks first, then whatever
  unblocks the gate).
- One plain line if they are behind, naming which must do to cut, using the order
  set in step 3.

If the user wants to change the goal mid cycle, edit the current cycle in place
and add one line under it: `Changed on <date>: <why>.` Changing a goal on purpose
is fine. Letting it drift silently is the failure this skill exists to stop.

## Finish

One short summary: the cycle closed (one line), the new goal and end date, the
first must do. Session end ticks must dos from here on and gives one reminder
when the cycle ends; nothing else will chase the user.
