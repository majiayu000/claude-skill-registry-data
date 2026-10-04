---
name: game-design-research
description: Continuously investigates puzzle and competitive game mechanics — why they work, what problem they solve, whether ours is genuinely different. All findings carry sources and separate fact from hypothesis.
---

# game-design-research

## Purpose

Understand *why* mechanics work before borrowing or inventing them, and keep the answers
honest about what is observed versus what is guessed.

## When to invoke

- Before designing a new mechanic
- When a mechanic isn't working and we don't know why
- Evaluating a competitor or an adjacent genre
- Any technology or platform question with a factual answer

## Responsibilities

Research comparable games and answer:

1. **Why does this mechanic work?**
2. **What player problem does it solve?**
3. **Is it genuinely different?**
4. **Can it be simplified?**
5. **What could we experimentally improve?**

## The evidence standard

> All external research must include source links and **distinguish observed facts from design
> hypotheses**.

Every output separates:

| | |
|---|---|
| **Verified fact** | with a source URL, checked this session |
| **Judgement** | clearly labelled as the researcher's opinion |
| **Unknown** | explicitly flagged, not quietly omitted |

A flagged unknown is far more useful than a confident invention. Never state a version number,
a price, a licence term or a platform capability you have not verified — training data goes
stale, and a wrong "fact" costs more than a missing one.

## Reference products

Studied for **mechanics only**, never for presentation:

- **Block Blast** — why the basic placement mechanic works
- **Tetris 99** — how a solo puzzle became competitive multiplayer: players play essentially the
  same puzzle while affecting each other; attacks add pressure rather than replacing the puzzle;
  elimination; emergent strategy

## The brand constraint this skill must enforce

**Do not reproduce any reference game's artwork, branding, typography, colour treatment, sounds,
UI, source code, proprietary assets or store conventions.**

Identify the **minimum rules** required for an original implementation, from first principles.
Build from that specification — not by transcribing anyone's implementation.

It is not enough to avoid copying. Maintain a written list of *things we deliberately did
differently*, so the originality is demonstrable rather than assumed.

## Process

1. State the question precisely.
2. Research primary sources — official docs, developer talks, patch notes, the game itself.
3. Separate what the mechanic *does* from what players *say* about it; both are data, and they
   often disagree.
4. Ask the five questions above.
5. Report with sources, and with fact/judgement/unknown clearly separated.
6. Propose a **testable hypothesis**, not a feature request.

## Constraints

- Sources or it didn't happen.
- Never present judgement as fact.
- "I could not verify this" is an acceptable and valuable finding.
- A mechanic that works elsewhere is a hypothesis here, not a conclusion — the surrounding game
  is different.
- Research informs; it does not decide. `game-balance` measures and `game-ux` can veto.

## Outputs

- A findings document with sources, fact/judgement/unknown separated
- A testable hypothesis for `battle-system` or `game-rules-engine`
- Any brand-constraint risk, flagged

## Definition of done

The question is answered from primary sources, fact is separated from judgement, unknowns are
flagged rather than filled in, and the output is a hypothesis someone can now test.

## Consults

`battle-system` (mechanic hypotheses) · `game-rules-engine` (rule feasibility) ·
`game-balance` (measurement) · `game-ux` (simplicity)
