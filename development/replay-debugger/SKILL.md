---
name: replay-debugger
description: Reproduces any match deterministically from rules version, seed and action log, and locates the first divergence, illegal action, state mismatch, scoring mismatch or desync.
---

# replay-debugger

## Purpose

Given `rules_version + generator_version + seed + action log`, reconstruct the match and find
exactly where reality diverged from expectation.

This is the most valuable debugging tool the project will have, because a desync report without
it is "the final states differ" — which tells you nothing about a 120-turn match.

## When to invoke

- A desync between client and server
- A golden replay failing
- A cross-runtime determinism failure
- Any bug reported with a seed
- A disputed match result

## Responsibilities

Deterministic reconstruction · locating the **first** divergence · identifying illegal actions,
state mismatches, scoring mismatches and multiplayer desynchronisation.

## Process

1. **Resolve the pinned versions.** A replay runs against the code it was recorded under, not
   against current code. Getting this wrong produces a false divergence and sends you hunting a
   bug that doesn't exist.
2. Reconstruct from the seed and action log.
3. Binary-search the checkpoint hashes to the first diverging turn.
4. Dump both states side by side, plus the action and the events, as readable boards.
5. Classify: illegal action · state mismatch · scoring mismatch · generator mismatch · engine bug.
6. Hand a minimal reproduction to `game-test-engineer` so it becomes a permanent test.

## Classify honestly

The four causes look similar at first and have completely different fixes:

| Symptom | Usually means |
|---|---|
| Divergence at turn 1 | wrong seed, wrong version, or a generator change |
| Divergence at a specific action | an engine bug or an illegal action accepted |
| Divergence only on one platform | float or iteration-order nondeterminism |
| Divergence only under load | a race in the network layer, not the engine |

**Early in the project, a desync is almost always our bug — not a cheater.** A tool that cannot
distinguish the two will get honest players accused.

## Constraints

- Runs with **no rendering** and **no network**.
- Must resolve pinned `rules_version` / `generator_version`, never "current".
- Reconstruction produces the identical final state *and* the identical event log — an event-log
  mismatch with matching state is still a bug.
- Never modify a replay to make it pass.
- Output is readable: boards printed as `■ · X`, not as hex dumps.

## Outputs

- The first divergent turn, both states, the action, and a classification
- A minimal reproduction for the test suite
- A golden corpus entry once fixed

## Testing expectations

A deliberately corrupted action log is detected and the first divergent turn reported. A replay
recorded under `rules_version` N still verifies after N+1 ships with different balance numbers.
Runs headlessly in CI.

## Consults

`game-rules-engine` (engine semantics) · `piece-generator` (sequence mismatches) ·
`multiplayer-sync` (network desync) · `game-test-engineer` (permanent regression)

## Definition of done

The divergence is located to a specific turn, correctly classified, minimally reproduced, and
turned into a test that would have caught it.
