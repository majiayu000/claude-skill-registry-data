---
name: security-review
description: Use when work must identify trust boundaries, permissions, sensitive data, abuse paths, privacy impact, compliance dependencies, and required human approvals.
kind: skill
status: active
owner: APT
last_updated: 2026-06-27
source: consolidated APT guidance
title: "Security Review"
domain: "security-risk"
source_paths: ["apt-principles-agents/skills/security-risk/security-review/SKILL.md"]
---

# Security Review

## Purpose

Produce a reviewable security review outcome that is grounded in repository evidence and explicit about uncertainty.

## When to Use

Use for planning, design, implementation review, migration, troubleshooting, or documentation where the task must identify trust boundaries, permissions, sensitive data, abuse paths, privacy impact, compliance dependencies, and required human approvals.

## Inputs

- Goal, audience, scope, constraints, and success criteria.
- Relevant source files, contracts, examples, logs, and decisions.
- Known risks, assumptions, dependencies, and approval boundaries.

## Process

1. Restate the intended outcome and affected audiences.
2. Inventory exact current behavior and source-backed constraints.
3. Apply the relevant APT principles and identify missing evidence.
4. Compare viable options, including compatibility and operational effects.
5. Produce the required artifacts: threat and data-flow review, role-permission matrix, secret handling, retention, abuse controls, audit trail, residual risk, and approval owner.
6. Review implicit authorization, excessive data collection, sensitive logs, unsupported compliance claims, and AI-generated security conclusions without review; separate blockers, recommendations, and open questions.

## Outputs

A concise recommendation, evidence map, required changes, risks, validation plan, support/documentation impact, and approval status.

## Quality Bar

The output is practical, source-backed, audience-aware, testable, reversible where possible, and does not state assumptions as facts.

## Domain Checklist

- Treat **Security Review** as an explicit decision with defined scope, evidence, owner, and validation.
- Identify assets, trust boundaries, threats, controls, residual risk, evidence, and accountable approval.
- State what is verified, what is assumed, and what requires specialist or human approval.

## Required Reading

Read the canonical Security Risk principle hub, the closest enforceable standard, the applicable checklist, and exact target-repository evidence.
## References

- [Security Risk principles](../../../principles/security-risk/README.md)
- [Templates](../../../templates/README.md)
- [Agents](../../../agents/README.md)
