---
name: usage-limits
description: Plan work to fit inside the Claude Code 5-hour and weekly usage limits. Use before starting anything long, when a limit is getting close, when asked how much usage is left, whether a job fits before the reset, when to stop and hand off, and when asked to work cheaply or stretch the rest of the limit.
---

# usage-limits (directory edition)

Running out of limit halfway through a job is a scheduling failure, not bad
luck. Size the job against what is left, then either commit to finishing or
order the work so that being cut off costs as little as possible.

This edition is Markdown only. It reads no files outside the project, no
credentials and no session logs, and it prints no automatic cost line after
each reply. The numbers come from the user: ask them to run `/usage` and tell
you the percentages and reset times it shows. The full edition, with the live
reading, the measured pace, the cost line, low power and the relay, is at
https://github.com/ridelink0/claude-code-usage-limits.

## 1. Measure

Ask once: "Run `/usage` and tell me the 5-hour and weekly percentages and when
each resets." Whichever window has less room relative to its reset is the
binding one. Never invent a number, a price or a pace; if the user has not
said, the budget is unknown.

## 2. Size the job before starting it

Count the work in turns, not in tasks:

| Work | Turns |
| --- | --- |
| Read and answer a question about existing code | 1 to 2 |
| One edit plus the check that it worked | 2 to 4 |
| A feature touching three or four files | 10 to 20 |
| Debugging something with an unknown cause | 15 or more, and unpredictable |

Hold back about a fifth of the budget for landing the work: the test run, the
commit and the handoff note. Work cut off just before the commit is worth
nothing.

## 3. Decide, out loud

Say which of these applies before doing anything expensive, in one line:

- **It fits.** Say so and work normally. Cheapness is not a virtue when the
  budget is not tight.
- **It fits only if nothing goes wrong.** Say so, suggest `/effort low` to the
  user, and do the valuable part first.
- **It may not fit.** Say exactly "it may not fit", and name when the binding
  window resets. Then do the whole request anyway, ordered so that a cutoff
  costs little: the most valuable part first, saved at clean boundaries, with
  a short running note of what is done, what is next and which files are
  mid-change.
- **The window resets first.** Then the limit is not the constraint. Say so
  and stop optimising for it.

Scaling the work down is the user's call, never yours. Once you have said it,
stop repeating budget commentary.

## 4. Spending less per turn

Only when the budget is tight. `references/tactics.md` has the levers, largest
first. The two that matter most: the user's `/effort` (reasoning is billed as
output, the most expensive tokens), and reading less, once. Changing the
running session's effort or model is the user's hand, not yours: put the
suggestion in front of them in one line and keep working.
`references/token-efficient.md` has the rule set behind working tersely.

## 5. Before the wall

When the binding window is nearly spent, write the handoff while there is room:
what is done, what is next, which files are mid-change, and the exact command
that checks the work. Save it in the project (for example `HANDOFF.md`) so the
next session starts from it.
