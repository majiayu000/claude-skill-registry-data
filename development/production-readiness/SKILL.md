---
name: production-readiness
description: Harden code and pipelines for production. Use when the user asks for production-ready code, hardening, release readiness, performance, monitoring, or reliability.
---

# Production Readiness

## Overview
Apply production hardening checks and identify missing pieces before release.

## Checklist
- Reliability: error handling, retries, idempotency, timeouts.
- Observability: logging, metrics, tracing, alerts.
- Security: secrets handling, PII, access control, dependency risks.
- Performance: profiling, resource limits, bottlenecks.
- Operations: configs, migrations, rollout and rollback.
- Testing: unit, integration, smoke coverage, and CI signals.

## Output
- List concrete gaps with recommended fixes.
- Suggest minimal test plan to prove readiness.
- Call out any release blockers.
- Be explicit about what was not verified.

## Acceptance Criteria
- Gaps are mapped to concrete fixes and owners or next steps.
- Readiness verdict is stated with evidence vs assumptions.
