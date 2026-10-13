---
name: refactor-safety
description: Use when work must implement maintainable changes that preserve contracts, limit blast radius, validate behavior, and update operational knowledge.
kind: skill
status: active
owner: APT
last_updated: 2026-06-27
source: consolidated APT guidance
title: "Refactor Safety"
domain: "engineering"
source_paths: ["apt-principles-agents/skills/engineering/refactor-safety/SKILL.md"]
---

# Refactor Safety

## Purpose

Produce a reviewable refactor safety outcome that is grounded in repository evidence and explicit about uncertainty.

## When to Use

Use for planning, design, implementation review, migration, troubleshooting, or documentation where the task must implement maintainable changes that preserve contracts, limit blast radius, validate behavior, and update operational knowledge.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Restate the intended outcome and affected audiences.
2. Inventory exact current behavior and source-backed constraints.
3. Apply the relevant APT principles and identify missing evidence.
4. Compare viable options, including compatibility and operational effects.
5. Produce the required artifacts: change boundary, contract impact, tests, security review, performance evidence, rollout, rollback, and documentation updates.
6. Review broad rewrites, implicit behavior changes, insufficient tests, unsafe migrations, and code/docs drift; separate blockers, recommendations, and open questions.

## Outputs

A concise recommendation, evidence map, required changes, risks, validation plan, support/documentation impact, and approval status.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Treat **Refactor Safety** as an explicit decision with defined scope, evidence, owner, and validation.
- Required evidence: change boundary, contract impact, tests, security, rollout, rollback, documentation.
- State what is verified, what is assumed, and what requires specialist or human approval.

## Required Reading

Read the canonical Engineering principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [Execution principles](../../../principles/execution/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
