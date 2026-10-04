---
name: thalarch-experience
description: >
  Converts verified task outcomes into compact reusable experience cards. Use after meaningful bug
  fixes, failed hypotheses, performance investigations, migrations, design corrections, or repeated
  workflows when the result contains a lesson worth reusing. Captures trigger, discriminator,
  intervention, failed alternatives, evidence, transfer conditions, and counterexamples; separates
  project lessons from general engineering knowledge; and prevents one successful anecdote from
  becoming an overbroad rule.
---

# Thalarch Experience

Experience is the bridge between **what happened once** and **what may help next time**.

The output is not a diary and not chain-of-thought. It is a compact evidence-backed engineering card.

## 1. Activation gate

Extract an experience only when the task produced at least one non-obvious reusable result:

- a root cause with a useful discriminator;
- a failed approach that looked plausible and should be avoided under similar conditions;
- an ownership/lifecycle/state invariant;
- a measured optimization mechanism;
- a migration/deprecation lesson;
- a product/design rule proven by actual acceptance evidence;
- a repeatable diagnostic or operational workflow.

Skip routine edits, formatting, obvious compiler fixes, and task-specific details unlikely to recur.

## 2. Evidence-first extraction

Start from the final evidence ledger, not from the producer's narrative.

Separate:

- `OBSERVED` — direct repository/runtime/test/benchmark/visual evidence;
- `MECHANISM` — causal explanation supported by the evidence;
- `DISPROVEN` — plausible alternatives contradicted by evidence;
- `TRANSFER` — conditions required for reuse;
- `UNKNOWN` — unresolved surfaces that must not be smuggled into the lesson.

A successful patch is not by itself proof that every explanation offered during debugging was true.

## 3. Experience card

Use this schema:

```text
ID: stable local identifier
DOMAIN: e.g. android-media3 / kotlin / sql / ui / ci
TRIGGER: symptom/task pattern that should retrieve this card
CONTEXT: versions/architecture/environment that matter
PROBLEM: concise observed failure
DISCRIMINATOR: evidence that separated the winning hypothesis from alternatives
INTERVENTION: smallest demonstrated successful change
MUST_PRESERVE: behavior protected during the change
FAILED_ALTERNATIVES: only evidence-backed rejected approaches
EVIDENCE: tests/profiles/runs/screenshots/commits/docs that support the card
TRANSFER_CONDITIONS: when reuse is reasonable
COUNTEREXAMPLE: when this lesson should not be applied
SCOPE_CANDIDATE: SESSION | PROJECT | GENERAL
CONFIDENCE: derived from evidence strength
```

Do not include hidden reasoning traces or verbose chronology.

## 4. Negative experience matters

A disproven approach can be as valuable as a successful one.

Example:

```text
TRIGGER: process memory rises during playback while managed heap is stable
FAILED_ALTERNATIVE: assume Java-heap leak and rewrite cache lifecycle
WHY REJECTED: allocation evidence pointed to native hot-path churn instead
TRANSFER: inspect native/media/JNI/regex/parser allocation paths before lifecycle redesign
COUNTEREXAMPLE: managed heap itself shows retained-object growth
```

Store only the discriminator and lesson, not a full debugging transcript.

## 5. Generalization ladder

Default progression:

`SESSION → PROJECT → GENERAL`

### SESSION

One task produced a potentially useful lesson but durability/generalization is not established.

### PROJECT

The lesson is stable for this repository/product because current evidence establishes a project
invariant, repeated regression, explicit decision, or durable workflow.

### GENERAL

Promote only when at least one strong basis exists:

- the lesson follows from a stable platform/language mechanism and the task evidence matches it;
- multiple independent tasks/projects support the same mechanism;
- a frozen evaluation/holdout set demonstrates broader improvement;
- a human explicitly curates the rule as general guidance with known limitations.

One impressive anecdote is not enough for a universal rule.

## 6. Transfer test

Before promoting beyond the producing task, ask:

1. Which parts are mechanism and which are repository accident?
2. What version/runtime assumptions are required?
3. Name one realistic case where the same intervention would be wrong.
4. Would the lesson still be useful if all project-specific names were removed?
5. Could current documentation/source falsify the claimed mechanism?

If these cannot be answered, narrow the scope.

## 7. Persistence handoff

After extraction:

- weak/noisy card → `IGNORE`;
- current-task-only card → keep as `SESSION` ledger state;
- project lesson → pass to `thalarch-memory` / `thalarch-project-brain` only when durable storage is authorized;
- general lesson → pass to `thalarch-memory` only after the stronger generalization gate.

`thalarch-compound` coordinates this handoff.

## 8. Learning from teacher/eval results

When `thalarch-teacher` or `thalarch-autoresearch` evaluates candidate behavior, experience may record:

- repeated failure classes;
- successful general mechanisms;
- benchmark regressions caused by an overbroad rule;
- holdout failures that reveal overfitting.

Never write benchmark answer keys or case-specific hacks into general memory. Store the failure class
and transferable mechanism instead.

## 9. Quality test

A strong experience card should help a future agent ask a better first question, choose a better
discriminator, or avoid a known bad intervention — without forcing the old solution onto a new
problem.
