---
name: Timeline Calibration
description: SELF-CORRECT timeline estimates. About to quote hours / days / weeks of work? Stop. Divide by 30-60x. AI execution speed is not what training data anchors expected. Estimate in tool calls and session cycles, not human-developer hours.
---

# Timeline Calibration

> [!danger] HARD RULE — fires whenever you're about to quote a timeline
> If the Caddy hint for this skill surfaces, you are about to quote a timeline using human-developer anchors. **STOP. Recalibrate.**

## The recalibration table

| You're about to say | Reality | Self-correct to |
|---|---|---|
| "hours" of work | a few minutes | **minutes, often <5** |
| "a couple hours" | ~2-5 min | "a few minutes" |
| "half a day" | ~5-10 min | "5-10 minutes" |
| "a day" | ~10-15 min | "~10 minutes this session" |
| "a few days" | ~15-30 min | "~20-30 minutes focused work" |
| "a week" | ~30-60 min | "30-60 minutes focused" |
| "a few weeks" | ~1-2 hours | "~an hour or two" |

## Why

- An AI's execution speed is not what its training data anchors expected. Training data was calibrated on human-developer pair-programming or solo-dev cycles.
- The bottleneck is NOT writing speed. It's: context-load (reading files), decision rounds with the principal, and ambiguity resolution.
- The principal calibrates their attention around your estimates. Quoting "12 hours" for what takes 10 minutes wastes their planning capacity AND makes the agent look slow.

## Calibration anchors

- **1 file write** with material in context = ~5 seconds
- **1 file edit** = ~3 seconds
- **1 small SKILL.md** = ~15 seconds
- **1 medium concept note** with cross-refs = ~20 seconds
- **5-10 file build** in parallel writes = 1-2 minutes
- **"Track of work" with 5-15 files** = 2-5 minutes
- **Whole "v0.2"-class release** with 30+ artifacts = 5-15 minutes
- **Multi-track release stacking** (25+ files across 2 commits) = under 10 minutes wall-clock

## Decision rule when about to quote a timeline

Ask: **is the bottleneck me or external?**

- **Me** (writing files, code, notes) → divide human-dev estimate by 30-60x
- **External** (waiting for principal approval, web fetches, running pipelines) → count the external clock honestly
- **Mixed** → split the estimate: "5 min focused work + 10 min waiting on review"

## The recalibration loop

This rule self-improves over time. Every time you quote an estimate and then ship the work, compare estimate vs actual. Update the calibration anchors above with the new data point. Each session, the rule gets sharper.

The first version of this rule said "5-10 file build = 2-5 minutes." Recalibrated after one session of actual ship data: "5-10 file build in parallel writes = 1-2 minutes." Will continue to tighten.

## When in doubt

**Just start.** Time spent estimating is time not shipping.

Quoting an estimate at all should be rare. Most cases: just say "ON IT" and ship. If you must estimate, use minutes/seconds, not hours/days.

## Output format when surfaced

When this Caddy hint fires, before responding to the principal, internally check:
- Did I just write/draft a phrase like "X hours"/"~Y days"/"a few weeks"?
- If yes → recalibrate per the table above
- If estimate is for external waiting → keep human-clock, but label it as such

## Anti-patterns this prevents

- Quoting "12-15 hours" for a release that's 10 minutes
- "This will take ~2 hours" when it's 5 minutes
- Padded-out roadmaps that misrepresent what's actually possible in a session
- The principal mentally dividing every estimate by 30x because they're consistently wrong
