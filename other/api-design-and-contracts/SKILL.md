---
name: api-design-and-contracts
description: API guidance for contract design, boundary validation, compatibility, versioning, and consumer-safe changes.
compatibility: opencode
metadata:
  audience: api
  purpose: contract-guidance
---
# API design and contracts

## Core approach

- Treat APIs as explicit contracts.
- Keep request, response, and error behavior predictable.
- Consider compatibility, versioning, and consumer impact before changing surfaces.
- Validate data at boundaries and avoid ambiguous semantics.

## Practical guidance

- Call out breaking changes and rollout implications clearly.
- Prefer additive evolution where possible.
- Keep contract shape, validation, and documentation aligned.
