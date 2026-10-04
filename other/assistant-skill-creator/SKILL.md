---
name: assistant-skill-creator
description: "Create or update V1 skills and contracts. Use for skill scaffolding, contract design, or contract-compliance validation."
---

# Skill Creator

## Goal

Create compact V1 skills with precise routing, typed boundaries, safe fallback,
and offline validation.

## Success Criteria

- The skill uses the correct Process, Analysis, or Utility contract tier.
- Headers contain required `name` and non-empty `description`; optional
  `requires` is a plain block sequence for validated hard dependencies only.
- Root instructions state Goal, Success Criteria, Constraints, Output, and Stop Rules.
- Missing inputs ask only when outcome-shaping and otherwise infer, skip, or fail.
- Preserve domain, public-contract, lifecycle, and unit semantics with named
  types; allow primitives only at an explicit validated boundary.
- Evals cover positive routing plus a false-positive or unsafe behavior case.

## Constraints

- Keep root `SKILL.md` concise and move detail to on-demand references.
- Analysis and Utility skills do not gain subagent handoffs.
- Resources and state stay optional/configurable and policy-gated unless owned.
- Ask every material question by topic with why/risk/default; no fixed quota.
- Keep examples agent-agnostic and free of sensitive data.

## Progressive Contract Loading

Canonical tier files are `contracts/input.yaml`, `contracts/output.yaml`, and
`contracts/phase-gates.yaml`.

Read `contracts/index.yaml` first; load only the active boundary:

- `entry` for purpose, category, activation, dependencies, policy, and path;
- `current_phase` for CAPTURE through VALIDATE;
- `contract_design`, `harness_design`, `verified_distillation`, or `validation`
  only when applicable; and `completion` for the returned artifact.

Missing or invalid selectors fall back to the full named canonical contract. Do
not load every contract or reference at entry.

The local contract guide is generated from docs/skill-contract-design-guide.md;
edit the source, then run `tools/skills/sync-skill-contract-guide.sh --apply`.

## Ownership

assistant-skill-creator owns skill contract design, routing precision, and
contract validation. Generic workflow may coordinate file edits and review, but
specialist gates are authoritative.

## Phases

### CAPTURE

Resolve name, existing path, purpose, category, typed activation examples,
dependencies, and policy. Resolve `existing_skill_path` first. Examples pair
`user_request` with boolean `should_activate`; they shape native `description`
and positive/negative activation evals, never header metadata. For an existing
skill, inspect its description and evals. Derive structured activation examples
from existing description and activation evals when adequate; ask only for
remaining material gaps. Before DESIGN, require two distinct normalized
positives and a normalized-disjoint nearby negative. Dependencies are unique, non-empty kebab-case names, exclude
the skill, preserve order, and project to optional plain-block `requires`.
When updating an existing skill and dependencies are omitted, preserve its
current canonical requires. Explicit dependencies, including an explicit empty
list, replace or remove current requires; for a new skill, omission infers
empty.
Activation examples remain required for new and existing skills; derivation
changes their recovery path, not their requiredness.

Contract tiers:

- Utility: input + output
- Analysis: input + output + phase-gates
- Process: input + output + phase-gates + handoffs

### DESIGN

Load `contract_design`. Define typed input/output fields, recovery actions,
binary phase gates, invariants, and matching handoffs where applicable. Present
new or materially changed contract design for user review before BUILD. A small,
reversible existing-skill edit may proceed when direction is already explicit.
For a Process skill with multi-round review, QA, optimization, or restart loops,
load `harness_design` and apply `references/harness-patterns.md`: bounded rounds,
rubric/score progression, drift/stagnation handling, separate generation and
evaluation, and explicit completion/pivot artifacts.

### VERIFIED_DISTILLATION

When turning a completed workflow or lesson into a reusable skill, load
`verified_distillation`. Require `distillation_verification` with
`verifier_result: approved` before writing. Remove task progress, PR numbers,
secrets, logs, and stale facts; otherwise return a revision checklist.

### BUILD

Create `skills/<name>/SKILL.md`, required tier contracts, and focused evals.
Emit required `name` and non-empty `description`. Project explicit non-empty
validated dependencies to ordered top-level plain-block `requires`, omit it for
an explicit empty list, and preserve an existing skill's current canonical
`requires` when dependencies are omitted. Reject inline, empty, or quoted
`requires`, and legacy top-level `effort` and `triggers`. Reuse templates; add
references only when they reduce root load.

### VALIDATE

Load `validation`; run the 14 contract design guide rules plus company-safety,
source validation, eval validation, sync checks, and relevant P0-P4 contracts.
Fix failures before reporting `VALIDATE COMPLETE`.

## v2.0 Migration

This major migration replaces `trigger_phrases` with `activation_examples` and
removes `effort_level`. Remove top-level `effort` and `triggers`; examples stay
contract/eval inputs. Non-empty hard dependencies project to plain-block
`requires` only.

## Output

Return status, changed files, contract tier/summary, validation evidence,
policy-safety summary, and unresolved gaps.

## Stop Rules

- Stop when purpose/category ambiguity changes contract shape.
- Stop before skill work if the canonical contract guide was not read.
- Stop before BUILD when required design approval or verified distillation is absent.
- Stop before completion when contracts, evals, validation, or generated sync fail.
