---
name: avs-cvv-analysis
description: Use when analyzing AVS and card-security-code signals, provider mappings, fraud-policy treatment, data-handling limits, customer impact, and false-positive risk.
kind: skill
status: active
owner: APT
last_updated: 2026-08-16
source: consolidated APT guidance
title: "AVS CVV Analysis"
domain: "payments"
source_paths: ["apt-principles-agents/skills/payments/avs-cvv-analysis/SKILL.md"]
---

# AVS CVV Analysis

## Purpose

Analyze AVS and card-security-code results as contextual risk signals—not universal proof of identity, authorization, or fraud—and define safe, evidence-backed policy treatment.

## When to Use

Use when mapping provider result codes, tuning fraud decisions, reviewing checkout behavior, investigating declines, migrating processors, or documenting how address and security-code results influence decisions.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Identify provider/acquirer/network, channel, geography, transaction type, code set/version, merchant configuration, and authoritative mapping sources.
2. Map raw AVS and security-code results without collapsing unavailable, unsupported, not processed, partial match, mismatch, and provider error states.
3. Trace how each signal combines with authorization response, authentication, device/account history, amount, velocity, and other risk evidence.
4. Evaluate approve, decline, review, step-up, retry, and customer-message policies using conversion, fraud, chargeback, and false-positive evidence by segment.
5. Verify that security-code values are never retained after authorization and that logs, analytics, support tools, and examples expose only permitted results.
6. Produce mapping conflicts, unsupported assumptions, policy recommendations, monitoring thresholds, customer/support impacts, and accountable approvals.

## Outputs

A raw-to-normalized code map, policy decision table, segment performance analysis, data-handling review, customer/support guidance, monitoring plan, and approval record.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Preserve raw provider results and distinguish match, partial, mismatch, unavailable, unsupported, not processed, and error states.
- Treat AVS and security-code outcomes as contextual signals, not standalone identity, fraud, or authorization verdicts.
- Validate mappings against the exact current provider/acquirer/network documentation and enabled merchant configuration.
- Measure conversion, fraud, chargeback, review, and false-positive effects by geography, channel, issuer, and customer segment.
- Never store the security-code value after authorization; redact sensitive values from logs, analytics, support tools, and fixtures.
- Give policy changes owners, thresholds, monitoring, rollback, customer messaging, support guidance, and risk approval.

## Required Reading

Read the canonical Payments principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [Payments principles](../../../principles/payments/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
