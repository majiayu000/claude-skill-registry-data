---
name: api-docs
description: Write API documentation that lets a developer correctly authenticate, call, interpret, retry, paginate, version, and troubleshoot an interface using verified contracts and executable examples.
---
# API Documentation

Use when an HTTP, RPC, GraphQL, event, SDK, or other programmatic interface needs consumer-facing documentation.

## Procedure
1. Identify the authoritative schema or implementation, supported versions, audience, base or connection context, and authentication model.
2. Explain the API's conceptual resources or operations before enumerating endpoints or methods where that helps consumer understanding.
3. Document inputs, types, requiredness, units, defaults, validation, permissions, outputs, side effects, and error semantics exactly.
4. Cover pagination or streaming, ordering, filtering, rate limits, idempotency, retries, consistency, asynchronous operations, and cancellation where relevant.
5. Provide minimal executable examples plus representative error and edge examples using safe placeholder credentials and data.
6. Document versioning, deprecation, compatibility, and migration rules that consumers need to maintain integrations.
7. Validate examples against the current interface and generated schemas or contract tests where available.
8. Link deeper reference and troubleshooting without duplicating the same contract in several manually maintained places.

## Decision rules
- API docs are part of the interface contract.
- Examples must execute against the documented version or be clearly illustrative.
- Error and retry semantics matter as much as happy-path payloads.
- Do not expose real secrets in examples.

## Quality gate
The documentation is ready when a new consumer can authenticate and complete representative operations, every important field and failure behavior matches the real contract, examples are validated, version and compatibility rules are explicit, and no essential integration knowledge exists only in source code.