---
name: tokenization-review
description: Use when work must model the complete transaction lifecycle and explicitly address money movement, tokenization, risk, reconciliation, funding, support, and provider differences.
kind: skill
status: active
owner: APT
last_updated: 2026-06-27
source: consolidated APT guidance
title: "Tokenization Review"
domain: "payments"
source_paths: ["apt-principles-agents/skills/payments/tokenization-review/SKILL.md"]
---

# Tokenization Review

## Purpose

Produce a reviewable tokenization review outcome that is grounded in repository evidence and explicit about uncertainty.

## When to Use

Use for planning, design, implementation review, migration, troubleshooting, or documentation where the task must model the complete transaction lifecycle and explicitly address money movement, tokenization, risk, reconciliation, funding, support, and provider differences.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Restate the intended outcome and affected audiences.
2. Inventory exact current behavior and source-backed constraints.
3. Apply the relevant APT principles and identify missing evidence.
4. Compare viable options, including compatibility and operational effects.
5. Produce the required artifacts: lifecycle states, amount and currency rules, idempotency, provider mapping, token boundaries, settlement/funding flow, reconciliation, disputes, and support identifiers.
6. Review invented provider behavior, double processing, confused authorization and settlement, sensitive-data exposure, incomplete reversals, and weak reconciliation; separate blockers, recommendations, and open questions.

## Outputs

A concise recommendation, evidence map, required changes, risks, validation plan, support/documentation impact, and approval status.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Treat **Tokenization Review** as an explicit decision with defined scope, evidence, owner, and validation.
- Keep raw credentials or account data outside application boundaries and document token scope and lifecycle.
- State what is verified, what is assumed, and what requires specialist or human approval.

## Required Reading

Read the canonical Payments principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [Payments principles](../../../principles/payments/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
