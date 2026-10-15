---
name: daily-plan
description: Morning planning loop. Reads context/Priorities.md, kb/wiki/_hot.md, and last 7 days of decisions/log.md. Proposes ONE top focus for the day and identifies one AI-assisted task. Read-only — does not modify anything except (optionally) decisions/log.md with a single-line entry.
disable-model-invocation: true
---

# /daily-plan — Morning Loop

> First skill of the day. Aligns the day's focus with the week's priorities before the inbox steers things.

## When to use
- First thing in the morning, before opening email/Slack
- After a long break (returning from PTO, weekend, etc.)

## When NOT to use
- Multiple times per day — defeats the purpose
- When `context/Priorities.md` is still placeholder — run `/onboard` first

## Inputs
- `context/Priorities.md`
- `kb/wiki/_hot.md` (if exists and < 7 days old)
- `decisions/log.md` last 7 days
- (Optional) calendar / inbox snapshot — if MCP is connected

## Outputs
- Three-line summary in chat:
  - **Top focus:** one sentence
  - **AI-assisted task:** which slash command + what
  - **What I'm not doing today:** explicit non-goals
- (Optional) one-line entry in `decisions/log.md`: `## YYYY-MM-DD — Day plan: <focus>`

## Hard rules
- **MUST be terse.** Three lines, not three paragraphs.
- **MUST NOT** propose more than one top focus. The constraint is the value.
- **MUST flag** when `_hot.md` is stale (>7 days) — but don't refuse to run.
- **MUST NOT** modify `context/`, `connections.md`, or any skill/agent.

## Steps

1. Read `context/Priorities.md`. Identify "this week" focus.
2. Read `kb/wiki/_hot.md`. Note: leverage gap of the week, hot articles, candidates.
3. Read `decisions/log.md` last 7 days. Note: recent commitments, pending follow-ups.
4. Synthesize:
   - **Top focus:** what advances the week's priority most?
   - **AI-assisted task:** what part can Claude do or accelerate?
   - **Not doing today:** name 1-2 things you're explicitly punting
5. (Optional) Append a one-line entry to `decisions/log.md`.

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Priorities.md` is placeholder | Onboarding incomplete | Pause; suggest `/onboard` |
| `_hot.md` is stale | Last weekly review was >7 days ago | Note the staleness; run `/weekly-operating-review` later today |
| Three+ candidate focuses | Real ambiguity in priorities | Propose ONE; surface the others as "not doing today" |
| No AI-assisted task is obvious | Day is admin-heavy | That's fine. Say so — "no AI lift today" is a valid output. |

## Reference files
- `context/Priorities.md`
- `kb/wiki/_hot.md`
- `references/3ms-framework.md` — Find Constraint
- `docs/CADENCE.md`

## Improvement loop
After each run:
1. Did the operator follow the proposed top focus? If consistently no → recommendation logic is wrong
2. Did the AI-assisted task actually get used? If not → wrong slash command suggested
3. Did the day end where it started (per `/end-of-day-review`)? If yes for 3+ days → priorities are stale
