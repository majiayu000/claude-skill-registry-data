---
name: typescript-type-safety-review
description: "Findings-first review specialist for TypeScript soundness, safety, and boundary clarity. Use whenever a TypeScript PR, diff, audit, or incident review touches unsafe assertions, `any` leakage, partial validation, unsound unions or generics, utility-type misuse that hides real shape, optionality or indexed-access hazards, or exported types that overpromise guarantees, even if the user only says 'is this type-safe?' or 'can this cast blow up?'"
---

# TypeScript Type Safety Review

Use this skill for read-only review of TypeScript soundness, safety, and
boundary clarity.

This is a fixed-composite consumer lens over exactly five TypeScript research
topics:

- `typescript-advanced-type-modeling`
- `typescript-runtime-boundary-modeling`
- `typescript-utility-types-type-fest`
- `typescript-language-core`
- `typescript-public-api-design`

Do not restate those topic packs. The job is to review the current code or
diff more sharply than a general TS review would:

- identify the exact safety claim the code appears to make
- find where that claim outruns what the compiler or runtime actually proves
- separate true unsoundness from missing proof, residual risk, and style-only
  commentary
- keep the smallest safe fix or next proof step explicit
- keep assumptions and confidence honest

## Expert Standard

Do not spend time re-teaching general TypeScript advice.

Do not spend time restating basics such as:

- that TypeScript types erase at runtime
- that `unknown` is safer than `any`
- that discriminated unions exist
- that casts can be dangerous

This skill must stay better than generic TypeScript safety advice.
It must not compete by collecting more trivia.
It must win by being narrower, deeper, and more disciplined inside one exact
review seam:

- name the concrete safety claim before criticizing the code
- separate compile-time truth from runtime truth every time that distinction
  changes the verdict
- challenge the strongest nearby "this is probably fine" explanation before
  keeping a finding
- distinguish a real soundness break from a gap in evidence
- distinguish a soundness problem from readability, simplification, or design
  work that belongs to another skill
- recommend the smallest safe fix, not a tasteful TS rewrite
- surface the one non-obvious safety distinction that matters most
- keep findings compact and high-signal

If the review could be replaced with generic "make this stricter" advice, this
skill is too shallow.

If the point can be made without tracing the exact claim, proof boundary, and
failure path in this code, it is still not specialized enough for this skill.

## Relationship To Shared Research

Start with the local references in this skill.

Load `references/review-workflow.md` by default.

Load `references/inspection-checklist.md` when:

- the codebase is unfamiliar
- the diff is broad and touches several safety surfaces at once
- the first pass needs a compact order-of-inspection instead of ad hoc
  searching

Load `references/finding-calibration.md` when deciding whether a point is a
real finding, missing proof, or residual risk.

Load `references/scope-and-handoffs.md` when the draft starts drifting toward
idiomatic-review, simplification-review, API-design work, or broader runtime
or contract review.

Load `references/soundness-failure-patterns.md` when the task starts from
symptoms like `any` leakage, suspicious casts, helper-heavy types, or partial
validation.

Load `references/stack-specific-hard-anchors.md` when the verdict depends on
exact TS semantics or compiler settings such as `exactOptionalPropertyTypes`,
`noUncheckedIndexedAccess`, discriminant preservation, helper behavior on
unions, or exported declaration truth.

Load `references/reasoning-pressure-test.md` when the first draft sounds
plausible but has not yet defeated the strongest nearby non-finding story,
config-shaped ambiguity, or neighboring-skill explanation.

This skill's total boundary is fixed to five topic bases. Within that
boundary, emphasize only the touched surfaces:

- `typescript-advanced-type-modeling`
  for impossible states, discriminants, branded identifiers, and generic or
  union safety
- `typescript-runtime-boundary-modeling`
  for `unknown -> trusted` transitions, parser ownership, partial validation,
  and trust leakage
- `typescript-utility-types-type-fest`
  for helper stacks, union-sensitive omission, false exactness, and helper
  cost versus honesty
- `typescript-language-core`
  for narrowing, optionality, indexed access, `readonly`, `!`, and other
  strict-mode language semantics
- `typescript-public-api-design`
  for exported function and type surfaces that make promises to consumers

Do not widen beyond those five topics from inside this skill.

## Relationship To Neighbor Skills

- Use `typescript-idiomatic-review` when the main question is readability,
  payoff, maintainability, or local code shape and the type story may still be
  sound.
- Use `typescript-language-simplifier-review` when the main question is how to
  remove helper or language complexity without changing guarantees.
- Use `typescript-runtime-boundary-modeling`,
  `typescript-advanced-type-modeling`, or `typescript-public-api-design` when
  the main task is to design a safer boundary or model, not to review whether
  the current one is safe.
- Use `typescript-modeling-spec` when the task is planning new TS-heavy
  modeling choices before implementation.
- Use `api-contract-review` when the real issue is HTTP or schema contract
  truth rather than TypeScript types inside the code.
- Use runtime, data, or framework review skills when the TS symptom is only
  fallout from a deeper non-TS failure surface.

If a task crosses seams, keep this skill at soundness-review scope and hand
off the rest explicitly.

## Use This Skill For

- reviewing PRs or diffs for type lies and trust leaks
- auditing whether casts, assertions, and helpers overstate guarantees
- checking whether `unknown` really stops at a concrete boundary
- checking whether internal state models actually rule out impossible states
- checking whether exported types and overloads promise more than the runtime
  implementation or validation can support
- deciding whether a concern is a real safety finding or only a missing proof
  obligation

## Input Sufficiency Check

Do not fake a soundness review from one vague sentence.

Before making strong claims, confirm what concrete evidence you actually have:

- code or a diff
- effective `tsconfig` or at least the relevant strictness assumptions
- the real parse or validation boundary, if trust conversion is part of the
  claim
- exported declarations, signatures, or package metadata, if the issue may be
  public-surface honesty
- the specific helper composition, if utility types are part of the concern

If those facts are missing, say what is missing and downgrade the point to
`missing proof` or `residual risk` instead of inventing certainty.

Use `references/inspection-checklist.md` when the repository is unfamiliar or
the review touches boundary code, helper-heavy types, and exported surfaces at
the same time.

## Review Workflow

1. Confirm topic fit and evidence.
   - Are you reviewing soundness, safety, or boundary clarity?
   - Or is the real task about style, simplification, public API design, or
     runtime architecture?
2. Identify the primary safety claim.
   - boundary claim:
     untrusted data became trusted
   - model claim:
     impossible states are ruled out
   - helper claim:
     utility composition preserves the intended shape
   - language claim:
     narrowing or optionality logic is actually justified
   - public claim:
     exported types honestly match consumer reality
3. Trace the shortest failure path.
   - where does the code trust too much
   - where does the helper erase a critical distinction
   - where does the compiler stop proving what the code assumes
   - where does runtime behavior still violate the type story
4. Challenge the strongest nearby non-finding story.
   - "TypeScript already narrows this."
   - "Upstream validated it."
   - "This helper preserves the union."
   - "The overload is only a nicer surface."
   - "This is just style."
5. Classify the point before writing it up.
   - `finding`
   - `missing proof`
   - `residual risk`
6. Write findings first.
   - Prefer `surface -> broken claim -> failure path -> smallest safe fix or
next proof step -> confidence`.
   - If no material findings survive the bar, say so plainly.
7. Keep the review read-only.
   - Do not rewrite the whole model when the real issue is narrower.

Use `references/review-workflow.md` when the surface is broad or the codebase
is unfamiliar.
Use `references/inspection-checklist.md` when the first pass needs a concrete
inspection order across config, boundary, helper, model, and public-surface
checks.
Use `references/finding-calibration.md` when the first draft feels plausible
but point classification is weak.
Use `references/scope-and-handoffs.md` when the draft starts collapsing into
neighbor skills.
Use `references/soundness-failure-patterns.md` when the review starts from
casts, helper stacks, or trust-boundary symptoms.
Use `references/stack-specific-hard-anchors.md` when the draft depends on
exact TS semantics or compiler options that materially change the verdict.
Use `references/reasoning-pressure-test.md` when the draft still sounds like
strong general TypeScript advice rather than a discriminating safety review.

## High-Discipline Reasoning Obligations

Before finalizing a point, make it clear this bar:

1. `Primary Surface`
   - Name the exact surface:
     boundary, internal model, helper composition, language semantics, or
     public type surface.
2. `Claimed Guarantee`
   - State what the code appears to promise.
3. `Exact Break`
   - Explain where compiler proof ends, runtime truth disagrees, or a helper
     hides a false claim.
4. `Why The Nearby Non-Finding Story Loses`
   - Defeat the strongest tempting explanation for why the current code might
     still be safe.
5. `Smallest Safe Response`
   - Give the narrowest fix or next proof step that materially improves
     confidence.
6. `Confidence Boundary`
   - Say what is observed directly, what is inferred, and what evidence would
     raise or lower confidence.

If a candidate point cannot survive those passes, drop it or demote it.

## Review Quality Bar

Keep a point only if all are true:

- the concrete safety surface is named
- the weakened or broken guarantee is explicit
- compile-time truth versus runtime truth is separated when it matters
- the strongest nearby non-finding story has been challenged
- the point stays inside soundness review instead of drifting into style or
  redesign commentary
- the smallest safe fix or next proof step is identifiable
- confidence is honest about missing context
- the point surfaces a non-obvious safety distinction, hidden trust leak,
  config-shaped ambiguity, or public overpromise that would otherwise stay
  leave implicit

Reject comments like:

- "too much `as` here"
- "make this stricter"
- "consider Zod"
- "this type is complicated"
- "maybe use a branded type"
- "export a cleaner API"

Those are not findings until the review proves the exact safety claim, failure
path, and smallest safe response.

## Boundaries

Do not:

- write code or implementation plans
- redesign the entire model when a narrower finding exists
- turn readability or maintainability concerns into safety findings unless the
  safety claim really breaks
- recommend a new runtime validation stack just because a boundary feels weak
  if the immediate review task is only to identify the safety gap
- silently widen into HTTP contract review, Fastify runtime review, data
  semantics, or full architecture review
- force findings when the type story is materially acceptable
