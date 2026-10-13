---
name: engineering-patterns
metadata:
  version: "2.0.0"
description: >
  Production engineering pattern library spanning 11 phases — Foundation, Resilience,
  Performance, Data Integrity, Observability, Deployment, Scalability, Edge Cases, Security
  Deep, Compliance/DR/FinOps, and AI/HITL. Activates when auditing code for production
  readiness, applying hardening patterns, reviewing system design, pattern audit, apply phase,
  harden this, production-ready, resilience patterns, observability gaps, security review, DR
  plan, FinOps, or AI guardrails. Use alongside engineering-staff-workflows for execution. Not
  for writing the implementation itself — that is engineering-staff-workflows.
---

## When to Use / When NOT

**Use when** — auditing a service or system for production readiness, or applying a specific hardening phase to existing code.

**Do NOT use when** — writing the implementation (use engineering-staff-workflows) or making a quick single-file fix that does not need a phase audit.

# Engineering Patterns — 11-Phase Production Library

## How to Use This Skill

1. **Audit mode** → Run `/engineering-patterns:audit-patterns` to score a codebase against all 11 phases
2. **Apply mode** → Run `/engineering-patterns:apply-phase <N>` to get actionable patterns for a specific phase
3. **Reference** → Load any `reference/phase-NN-*.md` file for deep-dive on a specific concern

---

## The 11 Phases

| # | Phase | Key Concern |
|---|-------|-------------|
| 01 | Foundation | Code quality, testing, CI/CD baseline |
| 02 | Resilience | Error handling, retries, circuit breakers |
| 03 | Performance | Caching, query optimization, profiling |
| 04 | Data Integrity | Transactions, idempotency, validation |
| 05 | Observability | Logging, tracing, metrics, alerting |
| 06 | Deployment | Blue-green, canary, feature flags, rollback |
| 07 | Scalability | Horizontal scaling, queues, sharding |
| 08 | Edge Cases | Concurrency, timeouts, large payloads |
| 09 | Security Deep | Auth, secrets, injection, supply chain |
| 10 | Compliance / DR / FinOps | Audit logs, BCP, cost controls |
| 11 | AI / HITL | LLM integration, prompt safety, human gates |

---

## Scoring System

Each phase is scored **0–5**:
- **0** — Not addressed
- **1** — Acknowledged but not implemented
- **2** — Partial implementation, gaps present
- **3** — Implemented, not tested under load/failure
- **4** — Implemented and validated
- **5** — Implemented, tested, monitored, and documented

**Target:** Phase 1–6 at ≥ 4 before shipping to production. Phase 7–11 at ≥ 3.

---

## Decision Priority (Applied Across All Phases)

**Maintainability > Correctness > Security > Observability > Scalability > Performance > Cleverness**

Never sacrifice Security silently. Call out conflicts explicitly.

---

## Activation Rules

- Always state which phase(s) you are addressing
- Load the relevant `reference/phase-NN-*.md` before making recommendations
- Surface a GAPS section if any phase scoring is below 3
- Flag builder's bias if Claude expands scope beyond the requested phase

## FAIL Conditions

Named failure modes for this skill. Each is a hard stop, not a warning.

- **Applying a later phase (Scalability, Performance) before Foundation and Resilience hold** → scaling broken code faster — the phases are ordered, do not skip the baseline.
- **Treating the 11-phase list as exhaustive coverage** → a domain-specific abuse vector slips through — the list is a floor, not a ceiling; add what the system needs.
- **Marking a phase done off its heading without applying the underlying pattern** → checkbox theater — each phase requires the actual pattern implemented and verified.
- **Silently trading Security for Performance or Cleverness** → violates the decision priority — conflicts are called out explicitly, never resolved silently.
- **Returning a production-ready verdict without the Security Deep and DR phases** → shipping with unmodeled blast radius — those phases are mandatory before any prod-ready claim.
- **Using this skill as the builder** → it is a pattern checklist, not an implementation engine — route the actual build to engineering-staff-workflows.

## Evals

- ✅ **SHOULD TRIGGER** — "audit this service for production readiness before we ship."
- ✅ **SHOULD TRIGGER** — "apply the resilience and observability phases to this code."
- ❌ **SHOULD NOT TRIGGER** — "write the actual retry logic for me" — route to engineering-staff-workflows.
