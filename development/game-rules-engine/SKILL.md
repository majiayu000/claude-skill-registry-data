---
name: game-rules-engine
description: Owns the deterministic puzzle simulation — board, pieces, placement, clearing, scoring, game-over. Use when changing any rule of how the game actually works.
---

# game-rules-engine

## Purpose

Own the deterministic puzzle simulation. This skill guards the single most important asset in
the project: one implementation of the rules that the client, the server, the tests and the AI
all agree on.

## When to invoke

- Any change to board behaviour, piece placement, clearing, scoring, combos or game-over
- Adding or altering a rule, however small
- Any change to `applyAction` or the event log
- When another skill's change needs a new engine capability

## Inputs

- The rule change being requested, and *why*
- The current `rules_version`
- `docs/architecture/game-engine.md`

## Responsibilities

Board representation · piece representation · legal placement · line and column detection ·
clearing · scoring · game-over detection · deterministic simulation · the event log.

## Process

1. **State the rule in prose first.** If it cannot be written as one unambiguous sentence, it is
   not ready to implement. Ambiguity here becomes a desync later.
2. **Write the test before the code.** Including the nasty case, not just the happy path.
3. Implement as a pure state transition: `(state, action, rules) -> [newState, events]`.
4. Check the rule is expressible as **configuration**. If it needs a literal in a function body,
   the rules schema is wrong — fix the schema, not the function.
5. Decide whether observable behaviour changed. If yes → bump `rules_version` and add a **new**
   golden replay; never edit an existing one.
6. Update `docs/architecture/game-engine.md` if a boundary moved.

## Constraints

- **No rules change ships without tests in the same commit.** This is not negotiable and it is
  the main thing this skill exists to enforce.
- Integer-only simulation math. No `Math.sin/cos/pow/exp/log`, no floats in anything hashed.
- No `Math.random()`, no `Date.now()`, no `performance.now()`. Time and randomness are inputs.
- No imports from `/client`, `/server`, `/platform`, or any renderer or audio library.
- `applyAction` is **pure and total**: it never mutates its input, never throws on an illegal
  action, and never half-applies. A partially applied action is the worst failure mode in a
  networked game.
- Events must carry everything consumers need. If the renderer has to recompute what cleared,
  the event is under-specified.
- Battle mechanics extend the engine; placement logic does not learn about attacks.

## Outputs

- The rule change, its tests, and a golden replay if behaviour changed
- An updated rules schema if the change introduced a new configurable
- A note to `game-balance` if the change affects any tunable number

## Testing expectations

Unit tests for the rule. Property tests for any invariant it touches. A golden replay for any
behaviour change. Specifically cover: almost-full boards, simultaneous row+column clears
(including the intersection-counted-twice bug), boards where no piece fits, multi-clears, and
attack+defence resolving on the same turn.

Test failure output must print the board (`■ · X`), the action and the events. A board-game test
that fails with `expected true, got false` has wasted an hour.

## Consults

`piece-generator` (sequence changes) · `battle-system` (battle events) · `board-analysis`
(metrics) · `game-test-engineer` (coverage) · `game-balance` (tunable numbers) ·
`replay-debugger` (version pinning)

## Definition of done

The rule is stated in one sentence, expressed as configuration, covered by a test that would
fail without it, and — if behaviour changed — pinned by a new `rules_version` with old replays
still verifying.
