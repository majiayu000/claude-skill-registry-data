---
name: phase-3-risks
description: Phase 3 — Risk Matrix with STRIDE threat modeling and technical risk catalog
version: 2.0.0
tags: [security, stride, risk, threat-modeling, phase-3]
trigger_keywords: [risk, stride, threat, security analysis]
requires_approval: false
estimated_duration: 15-25 minutes
---

# Skill: Phase 3 — Risk Matrix

## Purpose

Execute Phase 3: perform STRIDE threat modeling on the primary API surface, build a technical risk catalog, and ensure all CRITICAL risks have mitigations before proceeding to implementation.

## STRIDE Analysis Template

| Threat | Component | Attack vector | Severity | Mitigation |
|---|---|---|---|---|
| **S**poofing | [Component] | [Attack] | HIGH/CRITICAL | [Mitigation] |
| **T**ampering | [Component] | [Attack] | HIGH/CRITICAL | [Mitigation] |
| **R**epudiation | [Component] | [Attack] | MEDIUM/HIGH | [Mitigation] |
| **I**nfo Disclosure | [Component] | [Attack] | CRITICAL | [Mitigation] |
| **D**enial of Service | [Component] | [Attack] | HIGH | [Mitigation] |
| **E**levation of Privilege | [Component] | [Attack] | CRITICAL | [Mitigation] |

## Technical Risk Catalog Template

| Risk | Probability | Impact | Score | Mitigation |
|---|---|---|---|---|
| [Technical risk] | L/M/H | CRITICAL/HIGH/MEDIUM | [Calculated] | [Mitigation strategy] |

**Risk scoring:** Probability × Impact = Score
- Low × Critical = HIGH
- Medium × Critical = HIGH
- High × Critical = CRITICAL

## Examples from banking-walkthrough.md

**STRIDE — Payment API:**
- **Info Disclosure (IDOR):** Customer accesses another customer's transactions — CRITICAL — mitigated by strict account ownership check at repository layer (not controller — prevents bypass)
- **DoS:** Request flood on payment endpoint — HIGH — mitigated by rate limiting (per account + per IP) + circuit breaker

**Technical Risks:**
- Card network timeout mid-authorization — Medium probability × CRITICAL impact — mitigated by Saga with compensation + idempotency keys + Outbox pattern
- PostgreSQL primary failure — Low probability × CRITICAL impact — mitigated by synchronous multi-AZ replication + Patroni HA + RTO ≤30s

## Gate rule

**No CRITICAL risk may remain unmitigated.** If a CRITICAL risk has no mitigation, it blocks Phase 4.

All HIGH risks must have at least a documented mitigation strategy (implementation can be deferred, but the strategy must exist).

## Output artifact

Save as `docs/risk-matrix.md` or append to the main planning document.
