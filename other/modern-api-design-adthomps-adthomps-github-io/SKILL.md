---
name: modern-api-design
description: Use when work must select API styles from audience and behavior, then make contracts predictable, secure, observable, evolvable, and usable by humans and agents.
kind: skill
status: active
owner: APT
last_updated: 2026-08-16
source: consolidated APT guidance
title: "Modern API Design"
domain: "api"
source_paths: ["apt-principles-agents/skills/api/modern-api-design/SKILL.md"]
---

# Modern API Design

## Purpose

Produce a reviewable modern api design outcome that is grounded in repository evidence and explicit about uncertainty.

## When to Use

Use for planning, design, implementation review, migration, troubleshooting, or documentation where the task must select API styles from audience and behavior, then make contracts predictable, secure, observable, evolvable, and usable by humans and agents.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Inventory consumers, intents, interaction patterns, existing contracts, compatibility obligations, deployment boundaries, support needs, and operational constraints.
2. Compare candidate API styles using semantics, latency, consistency, caching, discoverability, tooling, evolution, failure recovery, and consumer capability; record the decision rationale.
3. Define identity and authorization, request and response schemas, validation, errors, idempotency and concurrency, pagination, async completion, rate behavior, versioning, and deprecation as one contract.
4. Map webhooks, events, polling, retries, timeouts, observability, correlation/support identifiers, and partial-failure recovery to explicit owners and states.
5. Produce machine-readable schemas plus runnable human and agent examples, contract/negative/replay tests, compatibility mapping, migration steps, and rollback evidence.
6. Review invented behavior, unsafe retries, ambiguous states, permission gaps, hidden breaking changes, non-executable examples, and operations without support ownership.

## Outputs

A concise recommendation, evidence map, required changes, risks, validation plan, support/documentation impact, and approval status.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Treat **Modern Api Design** as an explicit decision with defined scope, evidence, owner, and validation.
- Required evidence: audience, schema, auth, errors, idempotency, examples, compatibility, operations.
- Demonstrate why the selected protocol and interaction style fit the consumer and behavior better than viable alternatives.
- Treat compatibility, migration, observability, and support recovery as contract requirements rather than post-design additions.
- State what is verified, what is assumed, and what requires specialist or human approval.

## Required Reading

Read the canonical Api principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [API principles](../../../principles/api/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
