---
name: trigger-cadence
description: 'Builds outbound sequences that start from a specific buying trigger (funding, hiring, tech change, leadership move, product usage) instead of a static persona list, with a routing table that picks the cadence for each trigger. Use when: outbound sequence, cold email cadence, signal-based outbound, trigger-based prospecting, sales sequence, follow-up cadence, re-engagement campaign.'
---

# Trigger Cadence (SPARK Framework)

Persona-only sequences send the same five emails to everyone who matches a title. Trigger Cadence starts from why this account might buy *now*, routes each trigger to its own cadence, and makes every touch reference the trigger so the outreach reads as timely rather than templated.

## Core Principle

**No trigger, no sequence.** An account without a current reason to talk goes to nurture, not to a rep's inbox queue.

## The SPARK Framework

| Letter | Step | The Question |
|---|---|---|
| **S** | Signal | What changed at the account in the last 30 days? |
| **P** | Point of view | What does that change likely break or unlock for them? |
| **A** | Ask | What is the smallest useful next step (a teardown, a benchmark, 15 minutes)? |
| **R** | Route | Which cadence fits this trigger's urgency and buyer? |
| **K** | Keep-warm rule | When does the sequence pause and hand the account to nurture? |

## Trigger Routing Table

| Trigger | Buyer | Cadence | Touches / days |
|---|---|---|---|
| New funding | Founder / VP | Fast: email, LinkedIn, email, call | 4 / 10 |
| Hiring for the role you replace or support | Hiring manager | Medium: email, email, LinkedIn, email | 4 / 14 |
| Tech stack change | Technical owner | Medium: email with teardown, follow-up, call | 3 / 12 |
| New executive | New leader | Slow: congrats + POV, value asset, ask | 3 / 21 |
| Product usage spike (PLG) | Active user, then admin | Fast: in-app, email, call | 3 / 7 |

## Process

1. **Detect** - pull triggers from signal sources; discard any older than 30 days
2. **Write the POV** - one sentence per account linking the trigger to a specific consequence
3. **Route** - pick the cadence from the table; one active sequence per account at a time
4. **Draft touches** - every touch names the trigger or its consequence; no touch without new value
5. **Set the keep-warm rule** - no reply after the last touch, or trigger resolved → nurture for 60 days
6. **Review** - sample 10 drafts; any that would make sense sent to a different account get rewritten

## Output

Save to `outputs/trigger-cadence-[segment]-[YYYY-MM-DD].md`

| Artifact | Description |
|---|---|
| **Trigger list** | Account, trigger, date, POV sentence |
| **Routed cadences** | Touch-by-touch copy per trigger type |
| **Keep-warm and handoff rules** | When sequences pause and where accounts go next |

## Tips

1. **The swap test** - if a touch works for any account, it is a template, not outreach
2. **Short beats clever** - under 90 words per email
3. **Measure by trigger** - reply rate per trigger type shows which signals are worth buying

## Pairs With

- **signal-radar** - supplies market-level triggers
- **context-anchor** - supplies Audience and Voice for tone
- **battle-scanner** - supplies competitor-switch triggers
