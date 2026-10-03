---
name: uat-reopen-intake
description: Use when a user rejects, challenges, or reopens a previously accepted UAT, acceptance, or review result in an AI-assisted delivery workflow.
---

# UAT Reopen Intake

## Core Principle

When a user challenges an `accepted` result, the AI must not directly fix, directly re-accept, or silently widen the acceptance scope. It must first decide what failed, what evidence is missing, and who owns the smallest next action.

## Required Inputs

- Original receipt or acceptance summary.
- User challenge or reopen reason.
- Evidence actually covered by the original receipt.
- Current failing signal, if any.
- Candidate owner or lane, if known.

## Intake Flow

1. Run `accepted_scope_recheck`: list the route, surface, viewport, data, assertion level, fact source, and receipt identity that were actually covered.
2. Identify the `failed_gate_min` candidate: the smallest reproducible gate that contradicts the prior acceptance.
3. Classify `failure_type`:
   - `missing_evidence`
   - `scope_overclaim`
   - `real_regression`
   - `owner_boundary_unclear`
   - `environment_or_harness_gap`
   - `user_expectation_delta`
4. Record `missing_evidence`: what proof is required before any new acceptance claim.
5. Make `next_owner_decision`: who should act next, and what exact gate they must satisfy.

## Allowed Verdicts

| Verdict | Meaning |
| --- | --- |
| `reopen_required` | The challenge exposes a real gap in the prior acceptance scope. |
| `needs_failed_gate_min` | The challenge is plausible but lacks the smallest reproducible failing gate. |
| `needs_evidence` | The request needs more evidence before ownership or acceptance can be decided. |
| `reroute_owner` | The issue belongs to a different owner based on mechanism attribution. |
| `no_reopen_from_current_evidence` | Current evidence does not contradict the prior bounded receipt. |

## Output Contract

```md
verdict:
accepted_scope_recheck:
failed_gate_min_candidate:
failure_type:
missing_evidence:
next_owner_decision:
return_owner_on_fail:
must_not_claim:
remaining_risks:
```

## Common Mistakes

- Treating a user challenge as permission to immediately patch code.
- Saying `accepted` again without re-checking what was originally covered.
- Using a broad complaint as proof that all related surfaces failed.
- Assigning owner based only on the file where code lives.
- Collapsing environment or harness gaps into product failure.

## Stop Conditions

Stop and return `needs_failed_gate_min` or `needs_evidence` when the challenge lacks a reproducible signal, concrete scope, or source of truth. Do not continue into implementation until the intake decision is recorded.
