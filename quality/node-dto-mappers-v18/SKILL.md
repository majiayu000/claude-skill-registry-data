---
id: typescript.dto-mappers.node-dto-mappers-v18
name: Node DTO Mappers v18+
description: >
  Reviews DTO mapping in Node.js TypeScript code, focusing on transport contracts, normalization, validation boundaries, and safe mapping in backend services and scripts.
stack:
  - TypeScript
  - Node.js
category: dto-mappers
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - node dto mapping
  - node dto mappers
  - backend mapping
  - normalization boundary
  - api contract mapping
compatibility:
  runtime:
    node: "18+"
---

# Node DTO Mappers v18+

## Purpose

Use this skill for DTO mapping in Node.js TypeScript code.

This variant emphasizes transport contracts, normalization, and server-side mapping boundaries where validation and persistence may differ from browser-facing view models.

## When to Use

Use this skill when:

- backend services map transport DTOs to domain or persistence shapes
- scripts normalize external payloads
- mapping must sit near validation boundaries

## Do

Keep mapping pure and explicit.

Validate untrusted inputs before relying on the shape.

Separate transport DTOs from internal domain or persistence models.

## Do Not

Avoid leaking raw transport payloads into core logic.

Avoid skipping validation when the payload is untrusted.

## Review Checklist

- [ ] Node mapping boundary is explicit.
- [ ] Validation happens before trust.
- [ ] Transport and internal shapes are separate.
- [ ] Mapping remains deterministic.

## Expected Output

1. Identify Node DTO boundaries.
2. Recommend validation plus mapping.
3. Keep contracts separate from internal models.
4. Avoid raw payload leakage.
5. Produce backend-safe mapping guidance.
