---
name: product-tracking-implementation-guide
description: "Turn an approved product telemetry plan into a repository-specific implementation guide with file locations, sequencing, tests, rollout, and rollback. Use before implementing analytics instrumentation or when requesting a tracking implementation plan. Turkish triggers: tracking uygulama rehberi, geliştirici handoff'u, örnek payload ve QA."
---

# Product Tracking: Implementation Guide

Map an approved telemetry contract to the actual codebase without changing source code.

## Workflow

1. Read the approved tracking plan and the factual audit; list missing inputs instead of inventing them.
2. Locate initialization, existing wrappers, framework boundaries, authentication transitions, and representative feature paths.
3. Prefer one established wrapper or boundary per runtime. Explain any intentional exception.
4. Map every planned event to a file, lifecycle point, required data source, and testable acceptance criterion.
5. Describe rollout order, feature flags if already available, monitoring, failure isolation, and rollback.

## Deliverable

Provide a guide with:

```text
Prerequisites and exclusions
Architecture and ownership
Event-to-code mapping
Identity and consent integration
Test plan and fixtures
Rollout, observability, rollback
Open decisions
```

## Guardrails

- Do not generate provider credentials, secrets, or network calls.
- Do not propose broad refactors solely for telemetry.
- Treat generated events as unimplemented until a code review and representative tests pass.
