---
name: api-integration
description: Design and implement APIs, external integrations, webhooks, clients, and service boundaries using technology-agnostic principles.
metadata:
  internal: true
---

# api-integration

Use this skill for APIs, HTTP clients, webhooks, third-party integrations, service communication, pagination, retries, and integration boundaries.

## Principles

Define explicit contracts for requests, responses, errors, and side effects.

Validate data crossing external boundaries.

Distinguish transport concerns from business logic.

For outbound calls consider:

- timeouts
- retries
- retry safety
- idempotency
- rate limits
- pagination
- partial failure
- authentication
- observability

Do not retry non-idempotent operations blindly.

For webhooks consider:

- authenticity
- replay protection when required
- duplicate delivery
- idempotent handling
- failure recovery

Keep provider-specific assumptions isolated where practical.

Do not leak transport-specific details throughout unrelated application code.

## Adaptation

Use project evidence to determine the actual language, framework, runtime, and existing conventions.

When stack-specific implementation guidance is needed, prefer project evidence, native framework or language mechanisms, and relevant user-installed specialist skills. Technology-specific guidance must not redefine or weaken the core engineering requirement.