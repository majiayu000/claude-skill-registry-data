---
name: api-design
description: REST API design patterns including resource naming, versioning, error handling
---

# API Design

Opinionated patterns for designing REST APIs that are intuitive to consume, stable across versions, and easy to evolve. Covers resource modeling, URL conventions, versioning strategy, and error contracts.

## Delegation

This skill delegates to the superpowers/ECC equivalent when available. If the user has `superpowers:api-design` or `everything-claude-code:api-design` installed, invoke that version for the full implementation.

## Standalone Behavior

- Model resources as nouns (`/users`, `/orders/{id}`), not verbs; use HTTP methods for actions
- Version via URL prefix (`/v1/`) for breaking changes; use headers for content negotiation only
- Return consistent error envelopes: `{ error: { code, message, details } }` with appropriate HTTP status
- Use pagination cursors over page numbers for large collections; include `next` and `prev` links
- Document every endpoint with request/response examples and error codes before implementation begins
