---
name: cybersource-review
description: Use when reviewing a CyberSource integration against its exact products, APIs, versions, credentials, merchant configuration, transaction flows, risk services, tokens, events, and current provider evidence.
kind: skill
status: active
owner: APT
last_updated: 2026-08-16
source: consolidated APT guidance
title: "Cybersource Review"
domain: "payments"
source_paths: ["apt-principles-agents/skills/payments/cybersource-review/SKILL.md"]
---

# Cybersource Review

## Purpose

Review a CyberSource integration without treating the provider name as a single uniform product or assuming that documented capabilities are enabled for the merchant, region, API, and version in scope.

## When to Use

Use for integration design, implementation review, migration, incident analysis, or documentation involving CyberSource payment, token, authentication, risk, reporting, event, or related services.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Inventory exact CyberSource products/services, APIs, versions, environments, regions, merchant IDs/configuration, processors, credentials, and authoritative documentation dates.
2. Trace each supported payment and risk flow across request fields, identifiers, tokens, decisions, status transitions, follow-on actions, events/webhooks, reports, and reconciliation.
3. Verify authentication/signing, secret storage, endpoint selection, permissions, token domains, sensitive-data scope, idempotency/merchant references, and log redaction.
4. Map raw responses, errors, risk decisions, and processor/network results without inventing universal semantics; identify configuration- and processor-dependent behavior.
5. Test success, decline, review, challenge, timeout, duplicate, unknown outcome, delayed event, reversal/refund, outage, credential rotation, and reconciliation scenarios.
6. Report verified capability, enabled configuration, implementation evidence, gaps, operational readiness, support/escalation needs, and provider or specialist questions.

## Outputs

A product/configuration inventory, end-to-end flow map, field/status mapping, security and token review, scenario results, evidence index, readiness verdict, and provider questions.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Name exact products/services, APIs, versions, regions, environments, processors, merchant configuration, and documentation dates.
- Separate provider-documented capability, contracted/enabled service, merchant configuration, repository implementation, and observed behavior.
- Verify credentials/signing, endpoints, permissions, token scope, sensitive-data boundaries, identifiers, idempotency, and redaction.
- Trace payment, risk, authentication, token, event/webhook, reporting, follow-on, and reconciliation states used by the integration.
- Preserve raw provider/processor results and test decline, review, challenge, timeout, duplicate, unknown, delayed, reversal, outage, and rotation cases.
- Route unresolved product behavior to current authoritative CyberSource evidence or an accountable provider specialist.

## Required Reading

Read the canonical Payments principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [Payments principles](../../../principles/payments/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
