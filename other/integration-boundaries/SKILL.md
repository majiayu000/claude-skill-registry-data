---
name: integration-boundaries
description: Guidance for external integrations, service boundaries, webhooks, retries, idempotency, and failure-aware interface design.
compatibility: opencode
metadata:
  audience: integrations
  purpose: boundary-guidance
---
# Integration boundaries

## Core approach

- Treat integration points as failure-prone boundaries.
- Design for retries, idempotency, timeouts, and partial failure.
- Keep authentication, rate limiting, and data-shape assumptions explicit.
- Preserve observability across boundaries.

## Practical guidance

- Make boundary behavior visible through logs, metrics, tracing, or other diagnostics when possible.
- Prefer simple, testable integration seams over abstraction-heavy wrappers.
