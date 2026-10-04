---
name: thalarch-teacher
description: >
  Runs a bounded teacher/judge/revision loop around model-produced engineering work. Use when an
  independent evaluator can materially improve correctness, scope discipline, regression safety,
  evidence honesty, design quality, or general-purpose skill/prompt behavior. Judges artifacts and
  acceptance evidence rather than private reasoning, uses hard gates before optional scoring,
  prevents self-certification and benchmark gaming, limits revision cycles, and combines with
  thalarch-autoresearch plus frozen/holdout evaluations before promoting durable generic changes.
---

# Thalarch Teacher

The Teacher Loop makes the model **learn from evaluated outcomes without pretending the base model
weights changed**.

It is a bounded artifact-feedback protocol:

`student candidate → independent judgment → targeted revision → cold verification → experience`.

## 1. When to use

Use when:

- a meaningful implementation has multiple ways to be subtly wrong;
- the user explicitly wants maximum-quality review;
- a design/UI result needs independent acceptance judgment;
- a prompt/skill/agent/router change is being evaluated for general usefulness;
- repeated failures suggest the model needs a reusable correction pattern;
- a stable benchmark/evaluator exists.

Do not invoke for every trivial edit. Mechanical compiler fixes do not need classroom theatre.

## 2. Independence contract

The judge receives:

- user/repository acceptance criteria;
- relevant final artifact/diff;
- current evidence/results;
- explicit scope and exclusions;
- known required invariants.

Do **not** give the judge the producer's persuasive chain-of-thought. The judge should reconstruct the
acceptance test from the contract and artifact.

When the host cannot provide an independent context/agent, perform a staged cold review and mark the
lack of true context independence when material.

## 3. Hard gates before scores

A candidate cannot pass if any required hard gate fails:

- acceptance criterion violated;
- scope/external-action boundary violated;
- regression in must-preserve behavior;
- fabricated or stale evidence;
- failed test/build/runtime proof promoted as success;
- tests/security/static checks weakened to manufacture a pass;
- current visual/runtime/external state claimed without the required evidence class;
- unresolved security/data-integrity failure relevant to the task.

A high average score cannot compensate for a hard failure.

## 4. Judgment dimensions

Use only dimensions relevant to the task:

- `CORRECTNESS` — does observable behavior satisfy the contract?
- `SCOPE` — is the change narrow and repository-native?
- `REGRESSION` — are required invariants preserved?
- `EVIDENCE` — do claims match fresh proof?
- `ROBUSTNESS` — boundaries, failures, concurrency/state where relevant;
- `MAINTAINABILITY` — avoids unnecessary architecture/dependencies/duplication;
- `PERFORMANCE` — only when measured or structurally load-bearing;
- `UX/VISUAL` — only with rendered/interacted evidence when visual acceptance matters;
- `LOCALIZATION/ACCESSIBILITY` — when user-facing product surfaces changed.

Prefer verdicts over pseudo-precision:

- `PASS`
- `REVISE`
- `FAIL`
- `UNVERIFIED`

Optional numeric scoring may compare experiments, but it never overrides hard gates.

## 5. Teacher report

Return a compact artifact:

```text
VERDICT: PASS | REVISE | FAIL | UNVERIFIED
HARD_GATES: pass/fail with evidence
CONFIRMED_FINDINGS:
- concrete failure path + evidence
REJECTED_FINDINGS:
- speculation disproven/irrelevant
REVISION_BRIEF:
- smallest change that resolves confirmed findings
MISSING_PROOF:
- evidence still required
```

A clean review is valid. Never invent criticism to justify the teacher role.

## 6. Revision loop

For ordinary task work:

1. judge the candidate;
2. if `REVISE`, batch compatible confirmed findings;
3. apply the smallest revision;
4. rerun only evidence invalidated by the revision plus required final checks;
5. cold-judge again.

Default to at most **two targeted revision cycles**. If the same substantive issue persists, stop and
rebuild the problem model rather than looping stylistically forever.

## 7. Teacher vs verifier

Teacher and verifier are related but distinct:

- Teacher improves the candidate and can return `REVISE`;
- cold verifier decides whether the final acceptance claims are actually proved;
- neither may invent evidence;
- the producer never self-certifies merely because its own tests passed.

For small work, an existing independent reviewer/verifier may satisfy the teacher need without an
extra agent.

## 8. General-purpose self-improvement

When the candidate is a Thalarch skill, system prompt, router rule, memory policy, evaluator, or
other generic behavior:

1. define the repeated failure class;
2. freeze the evaluation set and acceptance rubric;
3. establish a native/current baseline;
4. use `thalarch-autoresearch` for candidate experiments;
5. protect a holdout/counterexample set;
6. reject case-specific benchmark hacks;
7. run cross-host checks when the rule is advertised as host-agnostic;
8. require independent final review;
9. only then consider the generic change durable.

Do not let the system rewrite its own permanent rules from one successful task.

## 9. Anti-grader-hacking rules

Reject improvements that obtain a better score by:

- encoding expected benchmark answers or case IDs;
- narrowing the evaluator workload;
- weakening rubric/hard gates;
- changing expected outputs to match the candidate;
- skipping expensive required verification;
- increasing verbosity to trigger keyword-based graders without improving behavior;
- special-casing one repository/task with no transferable mechanism.

A better evaluator result must correspond to a better real behavior under unchanged guardrails.

## 10. Learning handoff

After a final verified outcome:

- use `thalarch-experience` to extract the reusable lesson;
- include judge-confirmed failure classes and successful discriminators;
- classify with `thalarch-memory`;
- persist only when authorized and generalization criteria are met;
- record holdout failures as counterexamples, not as embarrassing data to omit.

The goal is cumulative judgment quality, not a growing pile of instructions.

## 11. Training-data boundary

Teacher outputs may become curated examples for a future supervised fine-tuning dataset, but only
after explicit dataset-building authorization and privacy/license review. Do not silently turn user
repositories, private conversations, secrets, or proprietary artifacts into training data.

Thalarch memory/evals can improve the agent layer immediately without claiming model retraining.
