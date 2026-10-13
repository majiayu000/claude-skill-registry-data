---
name: payment-links-review
description: Use when work must design the customer-to-merchant journey from discovery through checkout, payment, fulfillment signals, returns, support, and partner operations.
kind: skill
status: active
owner: APT
last_updated: 2026-06-27
source: consolidated APT guidance
title: "Payment Links Review"
domain: "ecommerce"
source_paths: ["apt-principles-agents/skills/ecommerce/payment-links-review/SKILL.md"]
---

# Payment Links Review

## Purpose

Produce a reviewable payment links review outcome that is grounded in repository evidence and explicit about uncertainty.

## When to Use

Use for planning, design, implementation review, migration, troubleshooting, or documentation where the task must design the customer-to-merchant journey from discovery through checkout, payment, fulfillment signals, returns, support, and partner operations.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Restate the intended outcome and affected audiences.
2. Inventory exact current behavior and source-backed constraints.
3. Apply the relevant APT principles and identify missing evidence.
4. Compare viable options, including compatibility and operational effects.
5. Produce the required artifacts: journey and state map, checkout options, payment lifecycle, merchant and partner onboarding, failure recovery, accessibility, analytics, and support flow.
6. Review conversion-only design, hidden fees or states, brittle checkout recovery, unclear merchant operations, and payment behavior detached from customer intent; separate blockers, recommendations, and open questions.

## Outputs

A concise recommendation, evidence map, required changes, risks, validation plan, support/documentation impact, and approval status.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Treat **Payment Links Review** as an explicit decision with defined scope, evidence, owner, and validation.
- Trace authorization, capture, settlement, funding, reconciliation, reversal, dispute, and support evidence.
- State what is verified, what is assumed, and what requires specialist or human approval.

## Required Reading

Read the canonical Ecommerce principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [Ecommerce principles](../../../principles/ecommerce/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
