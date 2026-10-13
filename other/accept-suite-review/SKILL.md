---
name: accept-suite-review
description: Use when reviewing a hosted or embedded payment acceptance suite across browser boundaries, tokenization, transaction states, integration security, provider evidence, and operational recovery.
kind: skill
status: active
owner: APT
last_updated: 2026-08-16
source: consolidated APT guidance
title: "Accept Suite Review"
domain: "payments"
source_paths: ["apt-principles-agents/skills/payments/accept-suite-review/SKILL.md"]
---

# Accept Suite Review

## Purpose

Review a payment acceptance suite as an end-to-end browser, application, provider, token, transaction, and support flow while keeping provider-specific claims tied to current authoritative evidence.

## When to Use

Use for hosted forms, embedded components, redirect/lightbox experiences, tokenized acceptance, callbacks, or acceptance-suite migrations where client/server trust boundaries and transaction outcomes must be verified.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Identify the exact product/component, provider, API/version, environment, merchant configuration, supported channels, and current authoritative documentation.
2. Trace page load, origin, script/frame, session or token creation, customer input, submission, provider processing, callback/message, server verification, and final transaction state.
3. Verify sensitive-data boundaries, CSP/origin rules, authentication, token scope/lifetime, amount/order binding, replay protection, idempotency, and log redaction.
4. Test success, validation failure, decline, challenge, cancellation, timeout, duplicate action, refresh/back navigation, provider outage, late callback, and unknown-outcome recovery.
5. Check accessibility, mobile behavior, localization, error/recovery copy, telemetry correlation, support identifiers, reconciliation, and fallback ownership.
6. Issue a readiness verdict that separates repository evidence, provider-documented behavior, configured behavior, assumptions, unsupported cases, and required specialist approval.

## Outputs

An end-to-end acceptance flow, trust-boundary map, scenario matrix, sensitive-data assessment, provider-evidence index, operational findings, and readiness verdict.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Name the exact provider product, component, version, environment, merchant configuration, and authoritative evidence date.
- Trace browser, application, provider, token, callback/message, server-verification, and transaction-state boundaries.
- Verify CSP/origin, authentication, token scope/lifetime, amount binding, replay protection, idempotency, and sensitive-data handling.
- Test success, decline, challenge, cancel, timeout, duplicate, refresh, outage, late callback, and unknown-outcome recovery.
- Correlate client, server, provider, webhook/callback, transaction, and support identifiers without exposing protected data.
- Separate provider capability from enabled configuration, repository implementation, observed behavior, and assumption.

## Required Reading

Read the canonical Payments principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [Payments principles](../../../principles/payments/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
