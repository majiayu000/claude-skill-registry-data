---
name: software-concept-architect-review
description:
  Audits concept and application design arguments and optional code conformance only when the user
  explicitly invokes $software-concept-architect-review. Read-only; use for purpose fitness, independence, composition,
  drift, and product-subset review.
metadata:
  language: en
  translation_of: software-concept-architect-review-cn
  openclaw:
    homepage: https://github.com/ontology-of-everything/concept-skills
---

# Software Concept Architect · Review

Focus: can the concept and application designs fulfill their respective purposes, and does the
implementation conform? Run only on explicit `$software-concept-architect-review` invocation and remain read-only.
Design can be reviewed without code; without specifications, review only observable code properties.
Mark conclusions unsupported by missing material as unverified.

## Model

A **concept** is a behavioral unit designed for one purpose. A concept argument connects its purpose
to its operational principle (OP), state, and actions. An application argument connects the
application purpose to concept selection, synchronizations, and end-to-end scenarios. Conformance to
an unsuitable model does not establish fitness; successful OP tests do not prove the purpose, and
locally sound concepts do not prove the application purpose.

Review five dimensions:

- **Fitness:** behavior meets the real need under stated assumptions.
- **Independence:** concept definitions do not depend on other concepts; this repository also
  requires concept modules not to reference one another.
- **Composition:** **synchronization may restrict behavior, never extend the contract**. Restriction
  alone is not a violation; remaining scenarios must still meet the need.
- **Drift:** implementation differs from a confirmed behavioral contract; distinguish omissions from
  contradictions.
- **Product subsets:** each subset preserves its purpose, entry points, required synchronizations,
  and resources.

Evidence means a fact supported by inspected requirements, models, code, or tests. Missing evidence
is not evidence of absence.

## Audit

1. **Scope** — Read `references/spec-format.md`, requirements, concept and synchronization
   specifications, the overall PRD, and staged links. With code, trace real entry points, calls,
   state/schema, migrations, and tests. Record versions, terms, facts, inferences, coverage, and
   gaps.
2. **Design arguments** — State concept and application purposes. For every concept, test the
   contract → OP → purpose argument and specificity, completeness, independence, and familiarity.
   Review application selection and synchronizations against end-to-end scenarios. Novelty or
   infrastructure identity alone is not a defect.
3. **Drift and independence** — When code exists, use `references/drift-checklist.md` to compare
   signatures, outputs, invariants, state, and dependencies, including public calls, shared mutable
   state, private access, and DTO/protocol leakage. Same-named local type parameters are not
   semantic dependencies.
4. **Composition** — Use `references/composition-checklist.md` to trace each action and
   synchronization from the application purpose. Check each concept's composed behavior sequences,
   then completions, bindings, isolation, failure, replay, loops, and under-/over-synchronization.
5. **Dependencies and subsets** — Check product inclusion dependencies separately from code
   restrictions. A product graph need not mirror a code graph.
6. **Aggregate** — Cross-check includes, actions and queries, parameters, outputs, bindings, and
   diagrams. Merge findings by root cause and report all five dimensions; an unexecuted check cannot
   pass.

## Report

```markdown
# Audit Report <date>

Scope: <requirements/spec/code versions; verified and unverified material> Summary: <coverage,
finding count, severity>

| Proposition or finding | Scenario and evidence | Failed relation or assumption | Impact/severity | Fix route |
| ---------------------- | --------------------- | ----------------------------- | --------------- | --------- |

Coverage: <five dimensions and every concept, entry point, or rule group> Fix order: <merged root
causes, affected locations, current fix, dependencies>
```

Medium or higher severity needs current specification or code evidence; pure design review is a
specification-level projection. Separate missing OP tests from purpose failure. Without
implementation, do not report implementation violations. Attach a scenario to every under- or
over-synchronization claim.

Route model defects to `software-concept-architect-design`, transcription/index errors to `software-concept-architect-prd`, and code
violations to `software-concept-architect-build`. Read `references/sources.md` when source definitions or
criteria must be verified. Do not write specifications, code, or history.
