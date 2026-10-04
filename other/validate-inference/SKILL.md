---
name: validate-inference
description: Validates an inferred premise with a concrete observation before an action depends on it. Use when a draft or plan contains "since / because / given X, do Y" where X is a state claim not observed this turn, when about to skip a step because a prior run covered it, when declaring a fix complete because the named occurrence is fixed, or when acting on remembered rather than re-read state. Walks the discipline (name the inference, cost the validation, validate with a tool call, act on the observation) plus its recording step, so a wrong premise is caught by one cheap read instead of cascading into every downstream action built on it.
derives_from: ../../governance/validate-inference-before-action.md
---

# Validate Inference (before acting on it)

## Overview

The failure mode this skill interrupts: an assistant infers a premise (most
commonly "nothing changed since the prior X, so skip / proceed"), acts on the
inference, and the action propagates a wrong premise into downstream work. By the
time a later check catches it, the cascade has touched multiple artefacts, and the
rework costs orders of magnitude more than the single tool call that would have
validated the premise at its source.

An inferred premise is a claim about state that the next action depends on and
that has not been directly observed in the current turn. The trigger surface is
textual and catchable in your own draft: clauses of the form "since / because /
given / per / based on X, [action]" where X has not been verified this turn. The
canonical rule ([`validate-inference-before-action`](../../governance/validate-inference-before-action.md))
states the discipline; this skill is its workflow wrapper for the moment the
trigger fires.

## When to Use

- A draft or plan contains "since / because / given / per / based on / following /
  according to" followed by a state claim not observed this turn.
- About to SKIP a step (a subagent, a test, a gate, a review) on the grounds that a
  prior run covered it or that nothing relevant changed.
- About to declare a fix complete because the named occurrence is fixed (the
  parallel-occurrence inference).
- About to reuse a prior approval, a prior file read, or a prior tool result as if
  it were current state.
- NOT for ambiguity about what the requestor wants: that is decision doubt, and the
  [`clarify-before-acting`](../../governance/clarify-before-acting.md) rule's
  question protocol governs it instead.

## Process

1. **Name the inference.** Stop at the trigger clause and state X precisely, in one
   sentence. If X cannot be named precisely, the premise is too vague to act on;
   refine it before continuing.
2. **Pick the cheapest concrete validation.** One or two tool calls almost always
   suffice: `git status` / `git diff` for "what changed"; a grep for "are there
   parallel occurrences"; a file re-read for "what does it say now"; a status call
   for "what is the current state"; a re-run for "does the check still pass".
3. **Run it and read the result.** The validation must be an observation, not a
   second inference ("I assume X because last time Y" does not validate anything).
4. **Act on the validated observation.** If the validation confirms X, proceed,
   and carry the evidence into any record the action produces. If it refutes X,
   REPLAN from the observed state; do not partially adjust the planned action.
5. **Record the validation where the workflow keeps records.** A structured cycle
   (a sweep, an audit, a review) records what was validated alongside the action,
   so a skipped step can never be reconstructed as an unexplained silence.

## Red Flags

- "The prior run covered this scope" used to skip anything, without a diff or
  status read taken this turn.
- "Only a comment changed, so the tests will pass" and its relatives: behaviour
  claims inferred from change-size intuitions.
- Fixing the cited instance and declaring the class fixed without a project-wide
  search for parallel occurrences.
- A validation that is itself an inference, or a validation run AFTER the action
  it was supposed to gate.
- Treating a screenshot, quote, or tool result from an earlier turn as current
  state.
- Skipping the validation because the action feels reversible: reversible actions
  still propagate wrong premises into downstream work before anyone reverses them.

## Verification

The skill's invocation is complete when:

- Every trigger clause in the draft or plan names a premise that is either
  observed this turn (cite the observation) or validated by a tool call whose
  result is read before the dependent action runs.
- A refuted premise led to a replan from the observed state, not a patch of the
  original plan.
- Any structured record the workflow produces carries the validation beside the
  action it gated.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The validation costs a tool call; I am confident." | The cost is seconds and bounded; a wrong premise's cascade cost is unbounded. Confidence is not an observation. |
| "I checked this earlier in the session." | State drifts between turns. The premise must be current-turn observed or re-validated. |
| "It is faster to just do the action and see." | The rule's only carve-out is the collapse case: the action is fully reversible AND the validation would cost about as much as the action itself, so the action is its own observation. Anything broader ("it is safe", "it feels reversible") is the failure mode the rule names; the red flag above applies. |
| "The skip saves an expensive subagent." | A skipped reviewer whose scope did change is the canonical cascade: the saved dispatch returns as multiple follow-up fixes. |

## See Also

- Canonical rule [`validate-inference-before-action`](../../governance/validate-inference-before-action.md):
  the discipline, the cascade worked example, the anti-patterns, and the
  exception protocol this skill wraps.
- Canonical rule [`evidence-grounded-completion`](../../governance/evidence-grounded-completion.md):
  the assertion-side counterpart (claims need observations; this skill covers
  actions needing validated premises).
- Sibling skill [`validation-sweep`](../validation-sweep/SKILL.md): its dispatch
  declarations are the recorded form of step 5 in a sweep context.
- Sibling skill [`surface-instruction-concern`](../surface-instruction-concern/SKILL.md):
  the instruction-intake counterpart; its stale-state check is this discipline
  applied to what an instruction assumes.
