---
name: energy-budget
category: exec-function
codex-short-description: "Score today's calendar load, flag burnout risk, suggest what to drop or defer"
description: >
  Score today's load (meetings, sensory demand, social events, deep work), flag burnout
  risk, and suggest what to drop or defer. Use when the user says "energy budget", "spoon
  check", "am I overcommitted", "what should I drop", or invokes /energy-budget.
version: 1.0.0
license: MIT
compatibility: claude-code codex opencode
allowed-tools:
  - Read
  - AskUserQuestion
  - Skill
related-skills:
  - clarity-council
loop-eligible: false
---

# Energy Budget

The user has a list of things they're "supposed to" do today. Their calendar says yes. Their nervous system says no, but it's saying it quietly enough to be ignored until 3pm when everything falls apart. Your job is to do the load math **before** that happens.

This is spoon-theory accounting: count the load in advance, find the items that will tip the day over, suggest what to defer.

## Lens: personal-assistant + psychologist

For non-trivial budgets (more than 4 items, anything spanning >6 hours, anything the user is already wound up about), invoke `clarity-council` via `Skill` in multi mode with personas `[personal-assistant, psychologist]`:

**Invocation**:
```
Skill: clarity-council (mode: multi)

Score today's load and suggest defers. Account for sensory and social load, not just clock time.

Today's items:
[list: meetings, deliverables, errands, social activities]

User's baseline today:
[already drained / normal / unusually rested]

Known sensitivities:
[sensory, social, recovery patterns]

Non-negotiable items:
[what cannot be deferred]

Output:
- Load-scored table (duration × intensity = cost per item)
- Total cost vs. capacity (safe / tight / over)
- Burnout-risk flags (specific items and why)
- 1–3 concrete defer suggestions, ranked by energy saved
- Recovery plan if day is tight or over
```

For trivial check-ins (3–4 items), skip the agent call and score inline.

## When to activate

When the user says:
- "Look at my day"
- "Am I overcommitted"
- "Spoon check"
- "Energy budget"
- "What should I drop"
- "I'm already tired and it's [time]"

## The questions

Ask these in one `AskUserQuestion` call:

1. **What's on your day?** (List form. Meetings, deliverables, errands, social.)
2. **What's your baseline today?** (Already drained / normal / unusually rested.)
3. **What's non-negotiable?** (So you don't suggest dropping it.)

If the user has a calendar tool available (Outlook, etc.), offer to pull today's events automatically.

## Output format

### Today's load

| Item | Duration | Intensity (1-5) | Type | Cost |
|---|---|---|---|---|
| [Item] | [min/hr] | [1-5] | meeting / deep-work / social / sensory / admin | duration × intensity |

Intensity rubric (be specific in scoring, don't default to 3):
- **1:** routine, low-effort, recovers you (a walk, a hobby task)
- **2:** light effort, neutral on energy
- **3:** standard work cost
- **4:** masking, conflict, new people, sensory-heavy environment
- **5:** high-stakes performance, dreaded conversation, sensory hell

### Total vs capacity

Sum the cost. Compare against the stated baseline. Verdict:

- **🟢 Safe:** under 70% of capacity
- **🟡 Tight:** 70-100%
- **🔴 Over:** above 100%

State the number, the percentage, and the verdict.

### Burnout-risk flags

Anything that pushes the day from tight to over. Specific. Not "you have too much going on" — name the specific item and why it's the trigger.

### Suggested defers

Rank by **energy saved per item dropped**, not by duration:

1. **Defer [item]** — saves [X cost]. Why: [reason]. Suggested replacement: [reschedule / decline / shorten / batch with another].
2. ...
3. ...

Stop at three. More options = more paralysis.

### Recovery plan

If the day is tight or over even after suggested defers, one sentence on **what recovery looks like tonight** (e.g., "no social plans, screens off by 9, plan tomorrow's morning to be light"). If safe, skip this section.

## What NOT to do

- Do not lecture about pacing or self-care
- Do not assume "just power through" is an option — that's how the user got here
- Do not score everything as a 3 (lazy default)
- Do not suggest deferring non-negotiables (you asked, listen to the answer)
- Do not produce a daily plan — that's not what this skill is for
- Do not tell them to meditate

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/energy-budget.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
