---
name: ui-api-alignment-review
description: Use when work must start from user intent and align journeys, roles, permissions, states, accessibility, UI, API, documentation, and demos.
kind: skill
status: active
owner: APT
last_updated: 2026-08-16
source: consolidated APT guidance
title: "UI API Alignment Review"
domain: "design"
source_paths: ["apt-principles-agents/skills/design/ui-api-alignment-review/SKILL.md"]
---

# UI API Alignment Review

## Purpose

Produce a reviewable ui api alignment review outcome that is grounded in repository evidence and explicit about uncertainty.

## When to Use

Use for planning, design, implementation review, migration, troubleshooting, or documentation where the task must start from user intent and align journeys, roles, permissions, states, accessibility, UI, API, documentation, and demos.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Inventory user intents, routes, controls, roles, current UI states, API operations, schemas, side effects, lifecycle states, and support paths from exact sources.
2. Build an alignment matrix from each visible action and state to its API operation, permission, input, response, completion evidence, error, retry/recovery, audit, and owner.
3. Review loading, empty, queued, partial, stale, conflicted, denied, failed, rolled-back, eventual-success, and offline behavior for truthful messaging and accessible interaction.
4. Check that authorization is enforced by the service and represented consistently in navigation, controls, validation, errors, and support guidance without leaking hidden capabilities.
5. Pair UI task tests with API contract, negative-path, idempotency/concurrency, and compatibility tests; identify mocks or demos that conceal real behavior.
6. Return blockers, mismatched states, role leakage, unsupported controls, contract changes, smallest coherent fixes, validation evidence, and accountable owners.

## Outputs

A concise recommendation, evidence map, required changes, risks, validation plan, support/documentation impact, and approval status.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Treat **Ui Api Alignment Review** as an explicit decision with defined scope, evidence, owner, and validation.
- Required evidence: intent, audience, journey, roles, states, accessibility, UI/API alignment.
- Require a traceable UI-action-to-API-operation matrix that includes permissions, side effects, errors, recovery, and ownership.
- Test interface and contract changes together across non-happy, concurrent, delayed, stale, and denied states.
- State what is verified, what is assumed, and what requires specialist or human approval.

## Required Reading

Read the canonical Design principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [Design principles](../../../principles/design/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
