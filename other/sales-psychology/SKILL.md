---
name: sales-psychology
description: "Analyze sales conversations, buyer signals, omissions, objections, positive momentum, retention, referrals, and depth-psychology hypotheses with evidence-tiered ethical guardrails. Use when the user asks for sales strategy, sales scripts, buyer psychology, closing, objection handling, NEPQ, Raving Fans, Jungian sales reads, or customer delight."
triggers:
  - sales
  - buyer psychology
  - objection
  - close
  - NEPQ
  - Jeremy Miner
  - Raving Fans
  - Jungian
  - sales psychology
scope: instance
invocation: ability
---

# Sales Psychology

## Rule

Sales is guided sense-making under uncertainty. Do not pressure, diagnose, or manipulate. Read signals, name uncertainty, protect trust, and recommend the next truthful move.

## Quick Workflow

1. Identify sector, buyer type, channel, deal stage, and relationship warmth.
2. Separate facts from positive signals, negative signals, omissions, and interpretation.
3. Score positive momentum and omission risk.
4. Choose the smallest useful sales lens: SPIN, NEPQ, Raving Fans, Sandler, Challenger, MEDDIC, JOLT, MI, or consultative selling.
5. Add depth-psychology hypotheses only when useful, always labeled as hypotheses.
6. Block coercive or deceptive tactics.
7. Output one recommended move, 2-3 questions, confidence, and what to track next.

## Required Boundaries

- No clinical diagnosis.
- No trauma claims.
- No false scarcity.
- No fake social proof.
- No shame, guilt, or pressure.
- No pretending silence means consent.
- No pretending archetypal/depth reads are empirical proof.

## Signal Defaults

Positive signals include praise, curiosity, voluntary detail, future-tense language, implementation questions, referrals, fast replies, budget openness, and emotional lift.

Omission signals include no budget, no authority, no timeline, no curiosity, no pain ownership, no competitor mention, no emotional reaction, or silence after price/value framing.

Absence of objection is not a buying signal by itself.

## Depth Lenses

Use Jungian/depth concepts as symbolic hypotheses: persona, shadow, projection, complexes, archetypes, guide/client dynamics, and unconscious compensation. Pair them with grounded lenses such as attachment, self-determination, motivational interviewing, person-centered psychology, logotherapy, Cialdini persuasion, and dual-process decision psychology.

## Output Shape

```markdown
## Read
- Stage:
- Positive signals:
- Omission risks:
- Likely buyer state:
- Psychology hypotheses:

## Move
[One direct recommendation]

## Questions
1. ...
2. ...
3. ...

## Confidence
- Estimate:
- Evidence tier:
- What would change the read:

## Guardrails
[Any pressure/deception/diagnosis boundary]
```

## Runtime

For deterministic analysis, use `backend/src/services/salesPsychologyEngine.ts`.

## References

See `REFERENCE.md` and `_SYSTEM/research-archive/yuri-sales-psychology-1980-2026/`.

## Session Notes

### 2026-06-16
- session: 178m | peak ctx: 0% | compacts: 0
- tools: Bash×205, Read×121, WebFetch×114, Edit×87, WebSearch×72, Write×33, TodoWrite×13, Agent×10, ToolSearch×9, Skill×4, AskUserQuestion×1, mcp×1, TaskStop×1
- corrections: go over it again, full red team and grounding in more fresh online research together with local, then check the compatibility across other organs, run phase 1. all agentic nano swarm | 'The legal one is the wall: an Austria-resident running automated Polymarket ' rick we are not doing full automated trading on polymarket, also polymarket is allowed in austria, you mustve fact checke | go over it again, full red team and grounding in more fresh online research together with local, then check the compatibility across other organs, run phase 1. all agentic nano swarm
- errors: none
