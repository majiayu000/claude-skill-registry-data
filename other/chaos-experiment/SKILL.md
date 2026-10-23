---
name: chaos-experiment
description: "Use when planning, running or writing up a deliberate failure experiment (fault injection, a game day) on a running system: a steady-state hypothesis, one realistic fault, a bounded blast radius, abort criteria written first, a way back, and what was learned."
---

# chaos-experiment

A method for breaking something on purpose and learning from it without causing an outage. "Let's see what
happens" is not an experiment: with no hypothesis nothing can be confirmed, with no limit the test can become
the incident. The block owns no injection tool and no scheduler. It adds the design and the write-up that the
resilience code blocks leave out; the tests of one library's retry or breaker behaviour stay with the stack
blocks (`skills/polly-resilience-pitfalls`, `skills/go-http-resilience-pitfalls`, `skills/jvm-resilience-observability`,
`skills/dotnet-conventions` §8). Related: `skills/slo-design` §2 (the error budget an experiment spends),
`skills/failure-classification-before-retry` §1 (the reactions an experiment is meant to check),
`skills/blameless-incident-review-pitfalls` (the write-up tone), `skills/feature-flag-lifecycle` §2 (a switch as an abort).

## When
- Someone wants to check that a failover, a fallback, a timeout or a degraded mode really works.
- A game day or a recurring fault-injection run is being planned.
- An experiment plan is reviewed before it touches anything real.

## Steps

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | The plan: hypothesis on steady state, realistic fault, blast radius, abort criteria, way back | an experiment is designed or reviewed | [`01-design-the-experiment.md`](./references/01-design-the-experiment.md) |
| 2 | Running it, stopping it, the write-up and the follow-up | an experiment is about to run or has just run | [`02-run-stop-learn.md`](./references/02-run-stop-learn.md) |

## Output / checkpoint
No pipeline checkpoint. A written plan before anything runs (hypothesis, the measurable steady state, the single
fault and its size, the scope, the abort criteria and who can trigger them, the way back, the people told) and a
short write-up after (confirmed or refuted, what surprised us, follow-up actions with owners).

## Guardrails
- Never run an experiment without written abort criteria and a person able to stop it.
- Never inject a fault nobody can undo, or one on data that cannot be restored.
- Never run on a system you cannot measure: with no steady-state signal, the result is unreadable.
- Never run during an incident, a freeze, a peak you were not cleared for, or with the budget already spent
  (`skills/slo-design` §2).
- Never carry another team's sizes, durations or thresholds: they come from your traffic and your budget.
- The block never starts an injection tool itself; a person authorises and starts the run.

## Origin
The Principles of Chaos Engineering (principlesofchaos.org, read 2026-10-19) and one MIT skill collection's
experiment workflow, rewritten. Provenance, what was removed and not verified:
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
