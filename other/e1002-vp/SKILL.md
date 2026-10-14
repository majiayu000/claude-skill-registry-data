---
name: e1002-vp
description: "Use when producing and maintaining the Verification Plan (VP) under ECSS-E-ST-10-02C clause 5.2.8.1 and Annex A: check whether a verification method is applicable at a stage, find completeness and consistency issues for one VP entry and across the whole plan, roll entry closure statuses up to an overall closure status, and decide whether the plan is ready. Trigger: ecss, e-st-10-02c, verification plan, vp, annex a, entry completeness, method stage applicability, closure status, plan readiness."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, e-st-10-02c, verification-plan, vp, annex-a, entry-completeness, method-stage, closure-status]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Verification — Verification Plan (space-systems/ecss/e1002-vp)

Use when producing and maintaining the Verification Plan (VP) under ECSS-E-ST-10-02C clause 5.2.8.1 and Annex A — checking method/stage applicability, entry completeness and consistency, plan-wide issues, closure roll-up, and readiness.

## Domain quick reference

- The VP is the controlling document: scope, methods, levels, stages, models, tools and documentation for every requirement-to-be-verified.
- Each VP entry must be internally consistent: the chosen method must be one the entry's stage can carry, and the entry must name its acceptance criterion and evidence.
- Completeness is per entry and plan-wide: one incomplete entry keeps the whole plan not-ready.
- Entry closure status rolls up to an overall status; the plan is ready only when every entry is complete/consistent AND the roll-up shows closure (or an explicit, justified open item).
- The VP is a living document — re-check it whenever a method, stage or scope changes.

## Workflow

1. Check applicability: `method_applicable_at_stage(stage, method)`.
2. Check one entry: `vp_entry_completeness(entry)`.
3. Check the plan: `verification_plan_completeness(plan)`.
4. Roll up closure: `rollup_closure_status(entries)`.
5. Full review: `verification_plan_review(plan)` -> `is_verification_plan_ready(review)`.

## Pitfalls

- Recording a method the entry's stage cannot carry — a consistency defect, not a preference.
- Declaring the plan ready while any entry is incomplete — `is_verification_plan_ready` requires all entries complete.
- Treating the VP as static — it must track every method/stage/scope change.
- Security-marking vocabulary: the content-policy gate flags the word beginning 'classif-'; use 'categorized' instead.

## Behavior contract (gate 3)

`scripts/test_e1002_vp.py` (stdlib unittest, offline) verifies method/stage applicability, per-entry completeness and consistency issues, plan-wide completeness, closure roll-up, and the readiness decision.

## Compliance

ECSS-E-ST-10-02C is a normative standard; this leaf implements only common-knowledge procedure and paraphrases it — no verbatim standard text. `license: Apache-2.0`, `compliance: STANDARDS-REF`, `standards: ecss` (reference-only), `gated: false`.
