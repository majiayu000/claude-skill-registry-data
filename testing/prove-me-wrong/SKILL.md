---
name: prove-me-wrong
description: Use when a leading diagnosis or nontrivial fix has initial support and needs one adversarial counterexample before acceptance.
---

# Prove Me Wrong

> Your agent has a theory. Make it try to kill it.

Use this at the commitment point: a leading claim is about to drive a substantial fix or be declared correct. It is not a prediction log for debugging steps. Skip mechanical edits.

## Write the attack card

Keep the card to four lines:

```text
Claim: <specific causal explanation or behavior the fix guarantees>
Smallest falsifier: <one observable result that contradicts the claim>
Strongest plausible competitor: <an alternative that fits known facts>
Cheapest safe attack: <a controlled check that can expose the falsifier>
```

Make the claim narrow and observable. Choose a credible competitor with a different prediction.

The attack must exercise the conditions under which the claim predicts an outcome. Missing the relevant path or state is inconclusive, not falsification.

## Attack the claim

Run one realistic controlled counterexample before accepting the claim:

1. Preserve the baseline and change only the variable that distinguishes the claim from its competitor.
2. Prefer a focused reproduction, test, query, log, toggle, or temporary instrumentation over a broad rewrite.
3. Record observation separately from interpretation, then remove temporary instrumentation.

For a completed fix, construct the counterexample within the requested workflow. Derive it from a boundary, state transition, concurrency path, integration seam, or surviving competitor—not an arbitrary edge case. When practical, show a regression test failing without the fix and passing with it.

## Classify and stop

- **Falsified:** The falsifier occurred. Reject or narrow the claim and promote a surviving competitor.
- **Survived:** The attack distinguished the alternatives and did not falsify the claim. Say it survived this attack, not that it was proved.
- **Inconclusive:** A confounder or unexercised precondition prevented discrimination. Do not count the result as support.
- **Unavailable:** The safe attack requires missing access, environment, data, or authority. Mark the claim unverified.

Stop after a decisive falsifier. Otherwise stop after the strongest cheap realistic attack when further checks are costlier, outside scope, or unavailable. Add attacks only when the stakes justify safe, authorized work.

Revert speculative edits justified only by a falsified claim. Preserve user work and independently justified improvements; passing tests alone do not justify an edit.

Completed-fix example:

```text
Claim: A unique key makes job execution idempotent.
Attack: Crash after the external send but before recording completion, then retry.
Observation: The retry sends the external action twice.
Verdict: Falsified; uniqueness prevents duplicate rows, not duplicate side effects.
```

## Report the challenge

Report only:

```text
Attack: <counterexample attempted>
Observation: <what occurred>
Verdict: <falsified | survived | inconclusive | unavailable>
Residual risk: <important path not exercised, or none identified>
```
