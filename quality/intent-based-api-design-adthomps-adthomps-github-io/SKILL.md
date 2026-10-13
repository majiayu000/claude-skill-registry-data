---
name: intent-based-api-design
description: Use when work must select API styles from audience and behavior, then make contracts predictable, secure, observable, evolvable, and usable by humans and agents.
kind: skill
status: active
owner: APT
last_updated: 2026-08-16
source: consolidated APT guidance
title: "Intent Based API Design"
domain: "api"
source_paths: ["apt-principles-agents/skills/api/intent-based-api-design/SKILL.md"]
---

# Intent Based API Design

## Purpose

Produce a reviewable intent based api design outcome that is grounded in repository evidence and explicit about uncertainty.

## When to Use

Use for planning, design, implementation review, migration, troubleshooting, or documentation where the task must select API styles from audience and behavior, then make contracts predictable, secure, observable, evolvable, and usable by humans and agents.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Identify human consumer groups, their top tasks, prerequisite knowledge, frequency, risk, current workarounds, and evidence of successful completion.
2. Map each intent to resources or operations, permissions, inputs, states, side effects, completion evidence, errors, recovery, and support ownership before selecting protocol details.
3. Design predictable names, schemas, defaults, errors, pagination, asynchronous behavior, versioning, and examples with progressive disclosure from first success to advanced use.
4. Trace authentication, authorization, idempotency, retries, limits, compatibility, observability, and deprecation to the consumer journey rather than documenting them as detached mechanics.
5. Test onboarding, common tasks, debugging, recovery, and migration with representative beginner and expert consumers using only the published contract and tooling.
6. Return the intent map, contract decisions, executable examples, usability findings, compatibility plan, documentation gaps, support path, and accountable approval.

## Outputs

A concise recommendation, evidence map, required changes, risks, validation plan, support/documentation impact, and approval status.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Treat **Intent Based Api Design** as an explicit decision with defined scope, evidence, owner, and validation.
- Required evidence: audience, schema, auth, errors, idempotency, examples, compatibility, operations.
- Prove that names, operations, states, and examples match consumer tasks rather than storage or internal service boundaries.
- Validate first success, debugging, recovery, and migration with representative humans using only published materials.
- State what is verified, what is assumed, and what requires specialist or human approval.

## Required Reading

Read the canonical Api principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [API principles](../../../principles/api/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
