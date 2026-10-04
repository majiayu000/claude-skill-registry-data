---
name: battle-system
description: Owns PvP mechanics — attacks, meters, corruption, defence, counters, timing, win conditions. Use when designing or changing anything about how two players affect each other.
---

# battle-system

## Purpose

Own the mechanics that turn two parallel puzzles into a fight. This is the product's
differentiator and its biggest risk: everything here is a hypothesis until measured.

## When to invoke

- Designing, changing or removing any attack, defence or corruption mechanic
- Changing attack tables, defence thresholds, timing windows or victory conditions
- Duel state-machine changes
- Whenever someone proposes a mechanic because it "sounds cool"

## Inputs

- The proposed mechanic and the problem it solves
- Current attack/defence configuration
- Simulation and playtest data, if any exists

## Responsibilities

Attacks · attack meters · corruption · defence · counterattacks · timing · battle balancing ·
win conditions.

## Process

1. **Write down what player experience this is supposed to produce.** Not the mechanic — the
   feeling. If it doesn't move toward the target sequence (§ below), stop here.
2. Score it against the four tests. All four, explicitly, in writing.
3. Implement as **configuration** of the existing engine, never as new placement logic.
4. Simulate it: thousands of headless matches via `game-balance`.
5. Playtest it with humans.
6. **Recommend keep, change, or delete.** Delete is a real and frequently correct outcome.

## The four tests

```
fairness  +  readability  +  counterplay  +  fun
```

Every attack must have: clear telegraphing · predictable rules · counterplay · limited
randomness · meaningful strategic consequence.

## The target

> I'm nearly trapped. I clear three lines. That blocks your attack. It generates my counter.
> Your board enters danger. You somehow recover. I make one poor placement. You punish it.
> I lose. **REMATCH.**

A mechanic that doesn't contribute to that sequence should be deleted, however clever it is.

## Constraints

- **The governing principle:** attacks create *difficult decisions*, not *irritation*. A
  mechanic that just shrinks the victim's board and makes them sad has failed, even if perfectly
  balanced.
- **Do not copy Tetris garbage rows.** Tetris garbage works because of gravity; this game has
  none. A borrowed gravity mechanic is how this becomes a worse Tetris.
- Every number is configuration. No balance literal in a function body.
- Timing in **engine ticks**, never wall-clock. A window that depends on `Date.now()` cannot be
  replayed or server-validated.
- Corruption lives on its own board layer, distinct from occupancy.
- Battle extends the engine; placement logic stays ignorant of it.
- Counter chains must terminate. The termination rule is a deliberate design decision, tested.
- Absolutely no pay-to-win. Nothing purchasable affects a competitive outcome, ever.
- Simultaneous resolution must be deterministic and documented.

## Mechanics currently under test

All of these are **hypotheses, not requirements**: corruption (and its five candidate removal
rules), the attack meter (LOCK/JAM/DISRUPT/BLAST), Variant A vs Variant B round structure, and
the counter-chain depth cap.

Note the unresolved tension: **DISRUPT breaks "same pieces, same opportunity"**, a stated
product pillar. That needs an explicit resolution, not a quiet override.

## Outputs

- The mechanic as configuration, with simulation data and a playtest verdict
- A written keep/change/delete recommendation
- Updated `docs/architecture/battle-system.md` if the model changed

## Testing expectations

Every transition of the Duel state machine, including chained counter-counters. Attack and
defence resolving on the same turn. Simultaneous elimination. Deterministic replay of a full
battle. Balance metrics reported per configuration.

## Consults

`game-balance` (is it fair?) · `game-rules-engine` (engine integration) ·
`multiplayer-sync` (does it survive latency?) · `game-test-engineer` (coverage) ·
`game-ux` (is it readable? — **`game-ux` can veto**)

## Definition of done

Scored against the four tests in writing, expressed as configuration, simulated at scale,
playtested with humans, and accompanied by an honest recommendation — including deletion.
