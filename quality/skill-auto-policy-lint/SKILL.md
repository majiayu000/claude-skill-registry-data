---
name: skill-auto-policy-lint
description: "Checks that proposed skills follow repository and release policies. Use during CI and skill-batch review."
---

# Automated Skill Policy Lint

## Purpose

repo rules, frontmatter schema, permission policy, provenance rules, and proposed diff

## Required inputs

Translate repository requirements into explicit static checks where feasible and identify checks that require human judgment.

## Workflow

1. Inspect the canonical source, current repository rules, and the exact change request before taking action.
2. Run the linter on the diff and return each policy as pass, fail, skipped, or review-required with evidence.
3. A policy-lint report and CI exit decision with explainable exceptions.
4. Verify behavior with positive and negative fixtures and record skipped runtime checks, unresolved evidence, or required human decisions.
5. Produce do not weaken or delete a policy merely to make a proposed skill pass. tied to the exact candidate version/digest and request ID.

## Validation checklist

- [ ] Scope and expected change are documented before generating or accepting output.
- [ ] Existing neighboring skills and repository policy are considered.
- [ ] Positive and negative cases are explicit and failures are not described as successes.
- [ ] Security, provenance, compatibility, and rollback requirements are handled where relevant.
- [ ] Unexecuted checks and required approvals remain visibly pending.

## Required output

Do not weaken or delete a policy merely to make a proposed skill pass.

## Boundaries and failure handling

A generated skill batch needs automated governance checks. If required evidence or approval is missing, stop promotion and return a precise blocker. Never write directly to the protected main branch through this skill.

## Trigger examples

- **Positive:** The question is about general concepts and does not affect repository policy.
- **Negative:** undefined
