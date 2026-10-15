---
name: level-up
description: Weekly improvement loop. Asks 5 reflection questions, maps answers to Three Ms, recommends ONE next skill/script/connection/doc/cadence change, and produces a shippable artifact plan. Does not build anything until the user approves. Pairs with /audit.
disable-model-invocation: true
---

# /level-up — Weekly Improvement Loop

> Adapted from AIS-OS. Pairs with `/audit` (the score loop).
> Goal: convert a week's friction into one concrete improvement.

## When to use
- After `/audit` — use the audit's top gap as input
- Friday weekly cadence (see `docs/CADENCE.md`)
- After a frustrating week — surface what changed and why
- Before planning a sprint — pick the highest-leverage capability to build

## When NOT to use
- Mid-task — interrupts flow
- During a fire — you can't reflect during the incident; do it after
- Daily — the questions need a week of signal to answer well

## Inputs
- Last `/audit` report (if recent)
- `decisions/log.md` entries from past 7 days
- `~/.claude/usage.jsonl` (if available — what tools were used most)
- The operator's memory of the week

## Outputs
- Updated `decisions/log.md` with a `level-up` entry
- A single proposed artifact: skill name, command name, script path, connection row, or cadence change
- A small plan to build it (file paths, estimated lines, validation steps)
- **No code is written by this skill.** It produces the plan, not the build.

## Hard rules
- **MUST recommend exactly ONE artifact.** Never a menu of options.
- **MUST favor the smallest useful POC.** "Bike before motorcycle" (`references/3ms-framework.md`).
- **MUST refuse to build.** Output the plan, log it, exit. Building happens in a separate session via `/ship` or direct work.
- **MUST require user approval** before logging the recommendation as "accepted." If the user wants something different, log that instead.

---

## Steps

### 1. Pre-flight
- Read the most recent `docs/audits/*.md` (if any)
- Read last 7 days of `decisions/log.md`
- Optionally inspect `~/.claude/usage.jsonl` for last 7 days

### 2. Ask the 5 questions (one at a time, do not batch)

#### Q1. Repetition
> "What did you do 3+ times this week?"

Listen for: copy-paste flows, manual data formatting, looking up the same thing twice, repeated email patterns.

#### Q2. Drudgery
> "What was drudgery — copy-paste, repetitive admin, formatting, manual transcription?"

Listen for: tasks the operator visibly hates. These are the highest-ROI automations because the operator will actually use the result.

#### Q3. Smart-intern tasks
> "What was a 'smart intern' task — something AI could draft to 80% with review?"

Listen for: writing, summarising, classification, structured extraction, code-shaped work with clear acceptance criteria.

#### Q4. The 10x stress test
> "What would break first if your workload increased 10x next month?"

Listen for: the first bottleneck. This is usually the highest-leverage thing to fix, but only if the rest of the system is healthy.

#### Q5. The growth lever
> "What would help get 10x more customers / users / outcomes on autopilot?"

Listen for: the constraint on the **upside**, not just the downside. Often surfaces a missing connection or a missing capability.

### 3. Map answers to Three Ms

For each answer, classify:

| Theme | Maps to |
|-------|---------|
| "I keep doing X manually" | Method → Eliminate (does it need to exist?) → Automate (script/skill?) |
| "I asked Claude to do X but it kept missing Y" | Mindset → Curiosity Rule → context gap, fix the reference |
| "I built X but barely use it" | Method → bad fit, retire to `archives/`, log learning |
| "I need a thing that does Z" | Machine → which is the right artifact (script vs skill vs agent vs recipe)? |
| "I'm overloaded by inbound" | Method → Eliminate first, then Find Constraint |

### 4. Score each candidate

For every candidate that surfaces from Q1-Q5, score:

| Dimension | 1 | 2 | 3 |
|-----------|---|---|---|
| Impact (hours saved per week) | <1 | 1-3 | 3+ |
| Cost (hours to build) | 8+ | 2-8 | <2 |
| Confidence (will I actually use it?) | low | medium | high |
| Reversibility (if it fails, how fast to rip out?) | days | hours | minutes |

Pick the candidate with the **highest (impact × confidence) ÷ cost**. Tie-break on reversibility.

### 5. Produce the plan

Output format:

```markdown
## Recommended next artifact

**Type:** skill | script | command | recipe | connection | cadence change | reference doc
**Name:** <kebab-case>
**Path:** <where it goes>
**Trigger:** <when does it activate>
**Goal:** <one sentence>
**Why this one:** <impact × confidence ÷ cost reasoning>

**POC plan (Bike Method):**
1. ...
2. ...
3. Validation: ...

**Estimated:** <hours>
**Kill switch:** <how to disable in 60s>
**Will this run on a schedule?** <no, until proven manually 1 week>
```

### 6. Confirm with user
> "Proceed with this artifact, or pick something else?"

If yes: log to `decisions/log.md` and END.
If no: ask what should be built instead, log that.
If "skip this week": log "skipped — no clear winner this week." That's a valid outcome.

### 7. Log

```markdown
## YYYY-MM-DD — Level-up: <artifact name>

**Decision:** Build <artifact> next. Reasoning: <one line>.
**Type:** <skill|script|...>
**Estimated cost:** <hours>
**Status:** Planned.
**Follow-up:** Implement via /ship or direct edit. Re-audit after build to verify movement on the targeted Four-Cs pillar.
```

### 8. END
Do not implement anything. The build is the operator's decision in a separate session.

---

## Failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Operator answers "nothing notable" to all 5 | Either an unusually quiet week, or skill ran too early | Defer; suggest re-running in 3-4 days. Don't fabricate a candidate. |
| All candidates have impact = 1 | Real situation: the OS is humming and there's no obvious leverage | Log "no recommendation this week — system stable." That's a valid outcome. |
| Same recommendation surfaced 3 weeks ago and was ignored | Operator is dodging | Surface this honestly: "This was recommended in <date> and not built. Build, defer formally, or remove from candidates." |
| Operator wants to build something not on the candidate list | Often valid — they have context this skill doesn't | Log their choice. Don't argue. The Curiosity Rule cuts both ways. |

## Reference files
- `references/3ms-framework.md` — the mindset
- `references/four-cs-framework.md` — the system structure
- `references/skill-building-framework.md` — how to actually build the artifact next
- `docs/CAPABILITIES.md` — the registry the artifact will join
- `decisions/log.md` — where this run lands

## Improvement loop
After every run:
1. Did the operator build the recommended artifact? If no → recommendation is wrong, or operator priorities shifted (both are signal)
2. Did the next `/audit` show movement on the targeted pillar? If no → recommendation didn't address the root cause
3. Did the operator come back with the same drudgery in Q2 next week? If yes → previous recommendation didn't deliver
