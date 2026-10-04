---
name: thalarch-doubt
description: >
  Fresh-context adversarial challenge for non-trivial engineering decisions before they harden
  into implementation. Use for D2+ work when a decision changes branching, crosses boundaries,
  asserts a non-compiler-verifiable property, has high blast radius, or rests on uncertain context.
  Extracts the artifact and contract, challenges them independently, reconciles findings against
  evidence, and stops after a bounded number of cycles instead of turning review into recursion.
---

# Thalarch Doubt Gate

Final review is sometimes too late. A wrong architectural or causal decision becomes expensive after
several files depend on it. This skill introduces a **bounded in-flight disconfirmation gate** for
important decisions while correction is still cheap.

Use doubt to reduce premature closure, not to manufacture hesitation.

## 1. Trigger only on meaningful decisions

Activate when at least one applies:

- branching/state behavior changes;
- a module/service/data boundary changes;
- correctness depends on thread safety, idempotency, ordering, lifecycle, ownership, or another
  property the compiler cannot prove;
- a version-sensitive external API or framework pattern is load-bearing;
- the codebase is unfamiliar and a wrong assumption would propagate;
- the decision is difficult to reverse or has security/data/production blast radius;
- a D2+ reasoning step has a strong leading answer but weak disconfirming evidence.

Skip for mechanical renames, formatting, obvious one-line edits, pure inspection, or deterministic
tooling operations.

## 2. Materialize the decision

Write a compact decision artifact:

- `DECISION` — what is about to stand;
- `CONTRACT` — observable requirements/invariants it must satisfy;
- `EVIDENCE` — only current facts supporting it;
- `UNCERTAINTY` — what could still make it wrong.

If the decision cannot be stated compactly, return to planning/reasoning before challenging it.

## 3. Preserve reviewer independence

When a clean specialist/subagent context exists, send only:

- the smallest reviewable artifact/diff/proposal;
- the contract and relevant constraints;
- directly necessary repository evidence.

Do **not** send the producer's hidden reasoning narrative or a persuasive explanation of why the
choice is believed correct. The reviewer should reconstruct the judgment independently.

If the host cannot provide an independent context, perform a degraded self-challenge and record
that independence was unavailable. Do not pretend self-review is equivalent to fresh-context review.

## 4. Challenge for failure, not approval

The challenge should try to falsify the artifact under the contract. Look for:

- unstated assumptions;
- counterexamples and edge cases;
- hidden shared state/coupling;
- violated project conventions or compatibility constraints;
- incorrect boundary ownership;
- failure modes under unexpected timing/input/environment;
- proof substitution or version/API assumptions that were not grounded.

A clean result is valid. Never force the reviewer to invent a defect.

## 5. Reconcile instead of obeying

Every finding is evidence to inspect, not an automatic verdict.

Classify each material finding as:

- `CONTRACT_GAP` — the contract was incomplete/ambiguous; fix the contract first;
- `CONFIRMED` — supported defect/risk requiring a change;
- `TRADEOFF` — real risk intentionally accepted with rationale;
- `NOISE` — unsupported once checked against actual context.

Reviewer confidence alone never upgrades a finding to `CONFIRMED`.

## 6. Bound the loop

After a confirmed issue changes the artifact, run another doubt cycle only if the changed decision
still meets the trigger criteria.

Stop when:

- only already-addressed/trivial/noise findings remain;
- the artifact is supported by discriminating evidence;
- three substantive cycles have completed;
- the next uncertainty requires a user/domain decision or unavailable evidence.

Three unresolved cycles are a signal to decompose the artifact or escalate, not permission for an
infinite agent loop.

## 7. Interaction with tests and final review

A failing regression/property/invariant test designed to disprove the behavioral claim can satisfy
the doubt requirement for that specific claim because it is executable disconfirmation.

`thalarch-doubt` is **in-flight**. `thalarch-review` remains the post-implementation quality gate and
`thalarch-verifier` remains the cold completion gate.

## 8. Cross-model use

A different model may catch shared-model blind spots, but external model invocation is an external
cost/tool action and must obey the current host and authorization policy.

Never silently invoke an external CLI/service. If cross-model evidence is unavailable or not
authorized, continue with host-native independent review and keep the limitation explicit.

## Shortcut defenses

Do not accept these rationalizations:

- "I am confident" — confidence is not disconfirmation.
- "Final review will catch it" — wrong direction is cheaper to catch before implementation expands.
- "The reviewer disagreed, therefore I am wrong" — reconcile against evidence.
- "More reviewers are always safer" — extra contexts without distinct evidence add cost and noise.
- "One more cycle cannot hurt" — unbounded review can become avoidance.

## Completion evidence

Record only:

`DECISION | CONTRACT | CHALLENGE RESULT | DISPOSITION | RESIDUAL UNCERTAINTY`

Do not expose private chain-of-thought.