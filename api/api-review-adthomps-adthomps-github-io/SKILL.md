---
name: api-review
description: Use when reviewing API routes, schemas, errors, webhooks, auth boundaries, or developer experience.
title: "API Review"
kind: "platform-adapter"
domain: "platforms"
status: "active"
owner: "APT"
last_updated: "2026-06-28"
source_paths: ["apt-agent-standards/codex/skills/api-review/SKILL.md"]
---

# API Review

## Purpose
Review APIs for consistency, safety, and usability.

## When To Use
Use for endpoint changes, webhook handlers, OpenAPI docs, SDK-facing behavior, and integration work.

## When Not To Use
Do not use for purely visual frontend changes.

## Required Reading
Read:

- `.apt/standards/installable-summaries/api-standards.md`.
- `docs/project-context.md` when present.
- Route handlers, middleware, schemas, validators, and error helpers.
- API docs, OpenAPI files, examples, and SDK-facing code.
- Tests for routes, webhooks, and integration behavior.
- Environment and secret handling for external APIs.

## Process
1. Inventory endpoints, methods, request inputs, responses, and errors.
2. Check naming consistency and route responsibility.
3. Check validation, auth, authorization, and tenant/account boundaries.
4. Check status codes, error shape, and client-facing messages.
5. Check idempotency, retries, timeout behavior, and webhook duplicate delivery.
6. Check logs for sensitive data exposure.
7. Compare docs and tests against actual behavior.

## Output Format
Return findings first, ordered by severity, with file references. Include open questions, validation gaps, suggested fixes, and tests to add.

## Validation Checklist
- Contract changes are documented.
- Auth and errors are explicit.
- Webhooks and retries are safe.
- Sensitive values are not logged.
- Tests cover critical success and failure paths.
- Docs match implementation.
