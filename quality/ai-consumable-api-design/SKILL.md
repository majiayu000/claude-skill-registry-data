---
name: ai-consumable-api-design
description: Use when work must select API styles from audience and behavior, then make contracts predictable, secure, observable, evolvable, and usable by humans and agents.
kind: skill
status: active
owner: APT
last_updated: 2026-08-16
source: consolidated APT guidance
title: "AI Consumable API Design"
domain: "api"
source_paths: ["apt-principles-agents/skills/api/ai-consumable-api-design/SKILL.md"]
---

# AI Consumable API Design

## Purpose

Produce a reviewable ai consumable api design outcome that is grounded in repository evidence and explicit about uncertainty.

## When to Use

Use for planning, design, implementation review, migration, troubleshooting, or documentation where the task must select API styles from audience and behavior, then make contracts predictable, secure, observable, evolvable, and usable by humans and agents.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Define the agent tasks, discovery path, authority, autonomy, supported tools, data sensitivity, side effects, approval boundaries, and accountable human owner.
2. Inventory the current schema, authentication and authorization, errors, idempotency, concurrency, pagination, asynchronous states, rate behavior, compatibility, observability, and support recovery.
3. Design stable machine-readable operations with explicit names, types, requiredness, enums, constraints, descriptions, examples, and deterministic success and failure shapes.
4. Separate read, propose, preview, and mutate capabilities; define least-privilege scopes, confirmation behavior, duplicate/stale request handling, cancellation, rollback, and audit evidence.
5. Build executable agent examples and evaluation cases for happy, malformed, adversarial, unauthorized, partial, duplicate, delayed, and incompatible requests.
6. Validate schema consumption, tool selection, side-effect visibility, injection/untrusted-content boundaries, human approval, observability, deprecation, and support identifiers before release.

## Outputs

A concise recommendation, evidence map, required changes, risks, validation plan, support/documentation impact, and approval status.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Treat **Ai Consumable Api Design** as an explicit decision with defined scope, evidence, owner, and validation.
- Required evidence: audience, schema, auth, errors, idempotency, examples, compatibility, operations.
- Require deterministic schemas and error/retry semantics so an agent does not have to guess which action is safe.
- Test least privilege, protected-action approval, duplicate execution, stale context, untrusted content, and partial failure as first-class contract cases.
- State what is verified, what is assumed, and what requires specialist or human approval.

## Required Reading

Read the canonical Api principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [API principles](../../../principles/api/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
