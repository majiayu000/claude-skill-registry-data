---
name: game-security
description: Threat-models competitive gameplay — client manipulation, impossible moves, altered seeds, replay attacks, forged scores, match manipulation, protocol abuse, leaderboard cheating.
---

# game-security

## Purpose

Assume competitive clients are hostile, and make sure the server can always prove what happened.

> **Assume competitive clients are untrusted.**

## When to invoke

- Any protocol or validation change
- Anything touching seeds, scores, rankings or leaderboards
- Before ranked play ships, and again before any leaderboard goes public
- When a rejection path is added or modified

## Responsibilities

Client manipulation · impossible moves · altered seeds · replay attacks · forged scores · match
manipulation · protocol abuse · leaderboard cheating.

## What the architecture already buys us

Much of this is defended by design rather than by a security feature:

- The server re-simulates every action with the **same core** — impossible moves cannot survive
- State hashes detect divergence per turn
- Replays make every ranked result independently verifiable after the fact
- The engine's rejection path is total and is fuzzed

The job is to find what those three do *not* cover.

## The seed problem

The PRNG is deterministic **by design** — that is the fairness promise. The consequence is that
anyone who knows the seed in advance can pre-compute the entire piece sequence and plan the
whole match.

Therefore: **match seeds must be server-issued and unpredictable.** Never client-proposed, never
derived from anything a client controls, never sent before the match starts. This is the single
sharpest security consequence of the determinism design.

## Threat register

| Threat | Primary defence |
|---|---|
| Client manipulation | server re-simulation |
| Impossible moves | engine rejection + validation |
| Predicted or altered seeds | server-issued, unpredictable seeds |
| Replay attacks | sequence numbers, idempotent rejection |
| Forged scores | leaderboard entries validated from replay |
| Match manipulation (collusion, throwing) | pattern detection, ranked only |
| Protocol abuse (flood, malformed) | rate limiting, total rejection path |
| Timing manipulation | tick-based windows, server clock authority |

## The hardest problem: cheater vs bug

Early in a project, a validation failure is **almost always our own engine bug**, not an
attacker. A detection system that cannot tell the two apart will ban honest players and destroy
trust faster than any cheat would.

So every rejection must log enough context — seed, versions, action, both states, first divergent
turn — for `replay-debugger` to classify it. Detection responses escalate slowly: reject the
action first; flag for review second; never auto-ban on a single signal.

## Process

1. Model the threat concretely: who does what, and what do they gain?
2. Check whether the architecture already prevents it.
3. If not, design the mitigation — or record it as an explicitly accepted risk.
4. Have `game-test-engineer` build the hostile input case.
5. Verify the rejection is total: no partial application, no state change, idempotent.

## Constraints

- Malformed or illegal input is rejected, **never partially applied**. This is a security
  boundary, not just a correctness one.
- Leaderboard entries are validated from replay, never trusted from the client.
- Detection response policy is written down **before** it is needed.
- No security measure may make the honest path slower or more annoying.

## Definition of done

The threat is modelled, mapped to a mitigation or an accepted risk, covered by a hostile-input
test, and its failure mode distinguishes an attacker from our own bug.

## Consults

`multiplayer-sync` (protocol) · `piece-generator` (seed handling) ·
`replay-debugger` (classification) · `game-test-engineer` (fuzzing)
