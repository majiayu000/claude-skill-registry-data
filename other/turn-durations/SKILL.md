---
name: turn-durations
description: >
  A mainline turn is worth two seconds in this engine. Any duration
  taken from the main games — a status that lasts four turns, a
  residual that bites once a turn, a screen that holds for five — is
  written as turns(n) from src/battle/turn.ts rather than as a
  millisecond literal.
---

The battle engine has no turns: moves are cast on a clock and everything the main games do "each turn" happens on a timer. The exchange rate is **one turn = 2000 ms**, chosen because that is about what an ordinary cast takes.

## Rules

- Import `turns` from `src/battle/turn.ts` and write the mainline turn count: `const DURATION = turns(4)`. Never a bare `8000`.
- A per-turn residual ticks on `RESIDUAL_TICK`, which is one turn. Do not invent a second interval for a new chipping effect.
- Look the turn count up in the modern games before converting, the same way move data is checked against PokeAPI. A status with no fixed length there (freeze thaws on a 20% roll a turn) is converted through its expectation — five turns — and the reasoning goes in the comment.
- Multipliers stay multipliers: Light Clay is ×1.6 because five turns becomes eight, and Grip Claw is ×1.75 because four becomes seven. Convert the base, keep the factor.
- Tests assert against `turns(n)` too, so a change to the rate does not mean editing forty literals.

## What is not a turn

Timings that belong to this engine rather than to the main games are plain milliseconds and stay that way: the gap between a move firing and landing, a projectile's flight, the AI's rest after a cast, the frame-derived cast time. They were never turn counts, so writing them through `turns()` would claim a mainline source they do not have.
