---
name: piece-generator
description: Owns deterministic seeded piece generation and competitive fairness. Use when touching the PRNG, piece pools, distributions, or anything that could introduce nondeterminism.
---

# piece-generator

## Purpose

Own deterministic piece generation. This skill exists to protect one product promise:

> **Same pieces. Same opportunity. Your move.**

and to prevent the single most damaging class of bug in the project — accidental
nondeterminism, which invalidates replays silently and is often discovered months later.

## When to invoke

- Any change to the PRNG, seeding, piece pools, weights or distributions
- Adding **any** new consumer of randomness anywhere in `/core`
- Investigating a piece-sequence mismatch between two clients
- Difficulty-curve work (SURVIVAL)

## Inputs

- The change requested
- Current `generator_version`
- Whether the change affects competitive modes

## Responsibilities

Seeded PRNG · piece pools · distribution · sequence reproduction · difficulty distributions ·
identical competitive sequences · generator statistical tests.

## Process

1. Ask first: **does this change the sequence any existing seed produces?** If yes, it needs a
   `generator_version` bump, full stop.
2. Confirm the change draws from the correct **sub-stream**. Piece randomness is isolated by
   construction.
3. For distribution changes, verify statistically over large samples — not by eyeballing a few
   runs.
4. Add a test that two players from one seed receive identical sequences.
5. Record any statistical-test results in ADR-003.

## Constraints

- **`Math.random()` appears nowhere in this project.**
- The PRNG state is part of match state: serialisable, hashable, advanced explicitly.
- Piece generation gets its **own isolated sub-stream**. This is the rule that matters most:
  if piece draws ever share a stream with anything else — a cosmetic effect, an AI tiebreak —
  then adding or removing that consumer silently shifts every historical sequence and
  invalidates every replay.
- 32-bit-safe arithmetic. Use `Math.imul` for 32-bit multiply; mind `>>>` vs `>>`.
- Old `generator_version`s are kept, never migrated.
- **The match seed itself must be server-issued and unpredictable** in competitive modes. The
  PRNG is deliberately predictable; a client that knows the seed can pre-compute the entire
  sequence and plan ahead. That is a `game-security` concern this skill must flag, not solve.

## The board-awareness question

Should the generator guarantee at least one placeable piece given the current board?

**Default: no, not in Duel.** A board-aware generator is no longer purely seed-deterministic
across two players with different boards, which breaks the fairness promise outright. If
anti-frustration is wanted in solo modes, it must be a separate, documented configuration —
never quietly enabled everywhere.

## Outputs

- The change, its tests, and a `generator_version` bump if sequences moved
- Statistical results for any distribution change
- A flag to `game-security` if seed handling is involved

## Testing expectations

Identical seed → identical sequence, proven across two JS runtimes. Two players from one seed
receive identical sequences. Distribution verified over large samples. **A test that adds
another consumer of randomness and proves the piece sequence is unchanged** — this is the test
that protects the sub-stream isolation.

## Consults

`game-rules-engine` (integration) · `game-test-engineer` (statistical tests) ·
`game-security` (seed unpredictability) · `replay-debugger` (version pinning) ·
`game-balance` (distribution effects)

## Definition of done

The sequence is reproducible from a seed on any runtime, sub-streams are provably isolated,
distributions are statistically verified, and no historical replay has been invalidated.
