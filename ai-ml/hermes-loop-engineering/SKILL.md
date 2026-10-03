---
name: hermes-loop-engineering
description: Use when repeated delivery failures, disputed acceptance, weak evidence patterns, owner-routing mistakes, or trial observations may need reusable governance improvement.
---

# Hermes Loop Engineering

## Core Principle

Turn delivery failures into reusable governance improvements only after evidence, observation, and forward-testing support the change.

This is human-in-the-loop self-improvement, not automatic model training.

## When To Use

Use this skill after an intake, evidence-boundary, acceptance-scope, or owner-boundary review surfaces a pattern that may recur.

Typical triggers:

- the same kind of UAT reopen appears again,
- an agent repeats an evidence overclaim,
- a verifier repeatedly accepts beyond scope,
- owner routing fails for the same reason,
- a candidate rule may need to become wording, a template field, or a hard gate,
- a trial observation needs a keep / revise / promote / drop decision.

## Loop

1. Capture the delivery failure or disputed outcome.
2. State the evidence boundary.
3. Identify the smallest failed gate or missing evidence.
4. Decide whether the signal is one-off, repeated, or systemic.
5. Fill or reference a `trial_observation`.
6. Choose the smallest improvement:
   - keep as observation,
   - revise wording,
   - add or revise a template field,
   - add an example,
   - forward-test a candidate,
   - consider a hard gate.
7. Record false-positive, false-negative, and maintenance risks.
8. Return keep / revise / promote / drop.

## Output Contract

```md
verdict:
failure_signal:
evidence_boundary:
candidate_pattern:
reuse_scope:
not_reuse_scope:
observed_repetition:
agent_rationalization:
recommended_change:
forward_test_needed:
forward_test_result:
behavior_change_evidence:
promotion_level:
false_positive_risk:
maintenance_cost:
rollback_condition:
next_owner:
must_not_claim:
```

## Verdict Vocabulary

| Verdict | Use When |
| --- | --- |
| `record_observation` | The signal is useful but not yet reusable. |
| `revise_wording` | A light wording change can reduce a repeated mistake. |
| `revise_template` | A missing field or template shape causes repeated gaps. |
| `add_example` | A concrete scenario would teach the judgment better than a rule. |
| `forward_test_candidate` | The candidate looks useful but needs pressure testing. |
| `promote_to_hard_gate_candidate` | The pattern is repeated, high-risk, low-noise, and cheap to check. |
| `drop_candidate` | The candidate is too broad, noisy, stale, or misleading. |

## Self-Improvement Proof

Do not treat a skill or template edit as proof that the system improved.

Minimum proof:

- a prior failure is captured,
- the old agent behavior or bad conclusion is visible,
- an artifact changes,
- a forward-test or later real case shows a better decision,
- false-positive and maintenance cost stay acceptable.

If behavior change is not observed, return `forward_test_candidate`, not `promote_to_hard_gate_candidate`.

## Common Mistakes

- Treating one failure as proof that a new rule is needed.
- Calling a document edit "self-evolution" without testing whether it changes agent behavior.
- Promoting a warning into a hard gate before measuring false positives.
- Adding governance weight when a narrower example or wording change would work.
- Keeping stale candidates because they sound important.

## Safety Boundary

Do not claim the system has learned unless a later artifact, example, template, or skill changes future agent behavior in a bounded way.

Prefer the smallest durable improvement that reduces the observed mistake.
