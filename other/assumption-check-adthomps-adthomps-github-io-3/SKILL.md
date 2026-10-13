---
name: assumption-check
description: Use when work must frame the real problem, expose assumptions, compare meaningful options, and explain decisions in beginner-clear language.
kind: skill
status: active
owner: APT
last_updated: 2026-06-27
source: consolidated APT guidance
title: "Assumption Check"
domain: "thinking"
source_paths: ["apt-principles-agents/skills/thinking/assumption-check/SKILL.md"]
---

# Assumption Check

## Purpose

Produce a reviewable assumption check outcome that is grounded in repository evidence and explicit about uncertainty.

## When to Use

Use for planning, design, implementation review, migration, troubleshooting, or documentation where the task must frame the real problem, expose assumptions, compare meaningful options, and explain decisions in beginner-clear language.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Restate the intended outcome and affected audiences.
2. Inventory exact current behavior and source-backed constraints.
3. Apply the relevant APT principles and identify missing evidence.
4. Compare viable options, including compatibility and operational effects.
5. Produce the required artifacts: problem statement, desired outcome, constraints, assumptions, options, tradeoffs, decision, and unresolved questions.
6. Review solution-first framing, false certainty, hidden constraints, and decisions without measurable outcomes; separate blockers, recommendations, and open questions.

## Outputs

A concise recommendation, evidence map, required changes, risks, validation plan, support/documentation impact, and approval status.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Treat **Assumption Check** as an explicit decision with defined scope, evidence, owner, and validation.
- Record evidence, confidence, impact if wrong, validation method, owner, and review date.
- State what is verified, what is assumed, and what requires specialist or human approval.

## Required Reading

Read the canonical Thinking principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [Thinking principles](../../../principles/thinking/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
