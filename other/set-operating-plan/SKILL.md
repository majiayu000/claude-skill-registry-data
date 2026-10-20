---
name: set-operating-plan
description: >-
  Turns an agreed business plan into a 90-day operating plan of at most three objectives with owned
  key results and weekly inputs, called by ceh-business-plan:develop-business-plan.
disable-model-invocation: false
user-invocable: false
license: Apache-2.0
---

# Set operating plan

Convert a plan into the next 90 days of work. Done is a §13 in `BUSINESS_PLAN.md` where every
objective retires a named risk, every key result has one owner and a date, and the team knows
which number to look at each week.

## Procedure

1. Read the plan, schema in `${CLAUDE_PLUGIN_ROOT}/references/business-plan-schema.md`. Take the
   ranked risks from §12, the channel test from §09, and the cash-out month from §11.
2. Choose the objectives, three at most. The first is whatever retires the top risk in §12. An
   objective that touches no risk and no revenue is cut. Andy Grove's rule for objectives was few
   enough that people remember them without looking.
3. Give each objective two to four key results. Each is a number and a date, and on that date it
   is plainly met or not met. "Launch the beta" fails this. "20 accounts complete setup unaided by
   15 May" passes.
4. Pair each key result with a counter-metric so it cannot be met by doing damage. Volume pairs
   with quality: signups with activation, sales with refunds, speed with defects. (Grove's paired
   indicators.)
5. Name the controllable input behind each key result: the thing someone can choose to do more of
   this week. Revenue is an output. Calls made, demos given, pages published are inputs. Amazon
   under Jeff Bezos reviewed inputs weekly for that reason.
6. Assign one owner per key result. One name, not a team. Shared ownership means nobody is asked
   when it slips.
7. Write the stop-doing list. For each thing currently taking time, ask Peter Drucker's question:
   if we were not already doing this, would we start it now? At least one item must go. New work
   with nothing removed is how plans fail quietly.
8. Find the bottleneck. Trace one customer from first contact to cash collected, time each step,
   and name the slowest. Effort spent anywhere else does not raise output. When a key result is
   later missed, ask why five times before changing the plan (Taiichi Ohno's practice at Toyota).
9. Allocate money and person-weeks to each objective. State the total against the runway in §11
   and say what is deliberately unfunded. Keep a buffer of about a fifth unallocated, so
   overruns land in the buffer instead of cutting an objective.
10. Set the cadence: a weekly input review of 30 minutes, a monthly re-score of the PMF gate and
    the kill criteria, a re-plan at 90 days.
11. Write §13 now, then show it. Writing before asking keeps the plan if the session is
    interrupted.
12. Ask about the weakest line, one question per turn, three questions at most. Revise §13 in
    place after each answer. An owner or date still open is marked `[assumption]`.

## Checks on the plan

| Check         | Ask                                                          | Fails when                                               |
| ------------- | ------------------------------------------------------------ | -------------------------------------------------------- |
| Count         | Are there three objectives or fewer?                         | Everything in the old roadmap survived as an objective   |
| Risk link     | Does each objective retire a §12 risk or produce revenue?    | An objective exists because it is interesting to build   |
| Falsifiable   | Could each key result plainly fail on its date?              | It describes activity: "work on", "explore", "improve"   |
| Controllable  | Can the owner move the weekly input by their own effort?     | The weekly number is an outcome nobody can directly push |
| Smallest step | Is the first release the smallest thing that tests the risk? | The first customer contact is months away                |
| Affordable    | Does the spend fit inside the runway with the buffer intact? | The plan runs out of cash before its own review date     |
| Kill dates    | Are the §12 kill criteria on the calendar?                   | They exist in §12 and nowhere anyone will see them       |

On the smallest step, Reid Hoffman's line is the useful bias: a first version you are not
embarrassed by shipped too late. Apply it to scope, never to honesty with customers or to anything
that touches their money, safety, or data.

## Rules

- Draft first from the plan, then ask. The user corrects owners and dates faster than they compose
  them.
- Never invent owners, headcount, or budget. With a solo founder, every owner is that person and
  the plan says so, which is itself the capacity check.
- A solo founder gets one objective, not three, because one person's capacity cannot carry three.
- Dates are calendar dates, not "Q2" or "week 6", so a key result is plainly met or missed on the
  day.
- When the capacity does not cover the objectives, cut objectives. Do not stretch the weeks.
- The operating plan follows the business plan. If a key result needs a customer, price, or
  channel the plan has not settled, stop and send it back rather than planning around the gap.
- Keep the confidence tags on any forecast number inside a key result.

## Output

Written into §13 of `BUSINESS_PLAN.md` as one subsection, replaced whole on a re-run. The
milestone lines above it, including those other skills tagged, stay:

```markdown
### Operating plan

Period: <start date> to <end date>

**Objective 1:** <outcome> — retires §12 risk <#>

| Key result (number, date) | Counter-metric | Weekly input | Owner | Budget |
| ------------------------- | -------------- | ------------ | ----- | ------ |

**Stop doing:** <thing>, <thing>
**Bottleneck:** <step> — <what is being done about it>
**Unfunded on purpose:** <thing>
**Spend:** <total> of <runway>, buffer <amount>

**Cadence:** weekly inputs <day>, monthly gate and kill-criteria review <date>, re-plan <date>
```

## Stop conditions

- §12 has no ranked risks or no kill criteria → there is nothing for the objectives to retire.
  Report it and name `ceh-business-plan:run-premortem`.
- The 90-day spend exceeds the runway → stop and report the shortfall. Do not write a plan the
  cash cannot carry.
- **No human to answer** (a headless run, or called by another agent): ask nothing. Draft and
  revise from what the plan holds, tag every gap `[assumption]`, and end with the questions you
  would have asked, in order, each with the assumption you used instead.

## Hands off to

- When an objective is a product build, suggest `ceh-build-planning` for the technical plan.
  This skill owns the business objective, not the architecture.
- When §11 has no cash-out month, suggest `ceh-business-plan:stress-test-unit-economics` first.
- When §09 has no channel test, suggest `ceh-business-plan:plan-go-to-market` first.
