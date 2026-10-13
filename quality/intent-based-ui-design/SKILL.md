---
name: intent-based-ui-design
description: Use when work must start from user intent and align journeys, roles, permissions, states, accessibility, UI, API, documentation, and demos.
kind: skill
status: active
owner: APT
last_updated: 2026-08-16
source: consolidated APT guidance
title: "Intent Based UI Design"
domain: "design"
source_paths: ["apt-principles-agents/skills/design/intent-based-ui-design/SKILL.md"]
---

# Intent Based UI Design

## Purpose

Produce a reviewable intent based ui design outcome that is grounded in repository evidence and explicit about uncertainty.

## When to Use

Use for planning, design, implementation review, migration, troubleshooting, or documentation where the task must start from user intent and align journeys, roles, permissions, states, accessibility, UI, API, documentation, and demos.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Name the primary audiences, their top intents, entry points, context, permissions, and evidence of successful completion.
2. Map each intent across the full journey, including loading, empty, error, partial, success, denied, recovery, and repeated-use states.
3. Trace interface actions to API contracts, authorization rules, data ownership, audit behavior, documentation, and support recovery.
4. Compare navigation and interaction options using task completion, accessibility, cognitive load, responsiveness, and operational clarity.
5. Produce the audience-intent map, journey and state model, permission matrix, UI/API alignment table, accessible interaction notes, and truthful demo flow.
6. Validate representative tasks with keyboard and responsive states; report role leakage, unsupported promises, dead ends, and hidden operational behavior as blockers.

## Outputs

A concise recommendation, evidence map, required changes, risks, validation plan, support/documentation impact, and approval status.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Treat **Intent Based Ui Design** as an explicit decision with defined scope, evidence, owner, and validation.
- Required evidence: intent, audience, journey, roles, states, accessibility, UI/API alignment.
- Make the most common valid next action visible without hiding source browsing, recovery, or expert paths.
- Do not mark the design complete until non-happy states and the backing authorization/API behavior are reviewable.
- State what is verified, what is assumed, and what requires specialist or human approval.

## Required Reading

Read the canonical Design principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [Design principles](../../../principles/design/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
