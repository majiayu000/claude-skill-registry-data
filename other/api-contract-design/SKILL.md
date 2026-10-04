---
name: api-contract-design
description: "Use when designing or changing an HTTP API contract consumed by another service, client, or team to specify resources, method semantics, schemas, errors, pagination, compatibility, and security boundaries before implementation. Trigger for new endpoints, public or partner APIs, versioning decisions, and contract reviews."
---

# API Contract Design

## Overview

This skill applies when designing or changing an HTTP API contract consumed by another service, client, or team. Its intended outcome is to specify resources, method semantics, schemas, errors, pagination, compatibility, and security boundaries before implementation.

## When to Use

### Preserved source section: When to Use

Use for the externally observable API contract, not for general server implementation. First identify whether the API is public, partner-facing, internal, or purely local; expectations for compatibility and disclosure differ.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Guardrails

- Do not expose secrets, stack traces, or fields a caller is not authorized to see.
- Do not silently change a public contract because an implementation would be easier.
- Ground protocol and framework-specific choices in current primary documentation when versions matter.

### Source boundary statements from: Procedure

2. **Model resources and actions.** Define identifiers, ownership, relationships, and state transitions. Prefer resource-oriented operations where they fit, but do not force CRUD onto domain actions that need clearer semantics.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Consumers, use cases, trust boundaries, and data sensitivity.
- Existing routes, schemas, conventions, versioning policy, and service limits.
- Required operations, state transitions, errors, pagination, filtering, and latency needs.
- Available contract tooling, test fixtures, and approval boundaries.

## Instructions

### Preserved source section: Procedure

1. **Discover the current contract.** Inspect existing endpoints, clients, OpenAPI definitions, tests, and version policy. Preserve established conventions unless a change is intentional and documented.
2. **Model resources and actions.** Define identifiers, ownership, relationships, and state transitions. Prefer resource-oriented operations where they fit, but do not force CRUD onto domain actions that need clearer semantics.
3. **Specify request and response schemas.** Define required and optional fields, formats, nullability, validation, size limits, and unknown-field behavior. Ensure authorization is enforced for each operation and object, not inferred from the route.
4. **Choose protocol semantics.** Use methods, status codes, safe/idempotent behavior, concurrency controls, retry semantics, and caching consistently with the API's protocol and existing consumers.
5. **Define errors and collection behavior.** Provide stable machine-readable error codes and useful human messages without leaking internals. Specify pagination, ordering, filtering, rate limits, and empty results.
6. **Review compatibility.** Classify additions, removals, renames, type changes, and semantic changes. Plan deprecation, migration windows, and client impact before introducing a breaking change.
7. **Publish and test the contract.** Update the canonical schema/docs, add positive and negative contract tests, and validate representative clients against the same definition.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

1. **Discover the current contract.** Inspect existing endpoints, clients, OpenAPI definitions, tests, and version policy. Preserve established conventions unless a change is intentional and documented.

### Source conditional guidance from: Output and Acceptance

Return endpoint purpose, request/response schemas, authorization rules, method and error semantics, compatibility assessment, examples, and contract-test evidence. Accept when consumers can implement against the definition without relying on hidden behavior and a change has a documented compatibility path.

### Source conditional guidance from: Guardrails

- Ground protocol and framework-specific choices in current primary documentation when versions matter.

## Output Format

### Preserved source section: Output and Acceptance

Return endpoint purpose, request/response schemas, authorization rules, method and error semantics, compatibility assessment, examples, and contract-test evidence. Accept when consumers can implement against the definition without relying on hidden behavior and a change has a documented compatibility path.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs

- Required operations, state transitions, errors, pagination, filtering, and latency needs.

### Source edge/failure guidance from: Procedure

5. **Define errors and collection behavior.** Provide stable machine-readable error codes and useful human messages without leaking internals. Specify pagination, ordering, filtering, rate limits, and empty results.

### Source edge/failure guidance from: Output and Acceptance

Return endpoint purpose, request/response schemas, authorization rules, method and error semantics, compatibility assessment, examples, and contract-test evidence. Accept when consumers can implement against the definition without relying on hidden behavior and a change has a documented compatibility path.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Return endpoint purpose, request/response schemas, authorization rules, method and error semantics, compatibility assessment, examples, and contract-test evidence. Accept when consumers can implement against the definition without relying on hidden behavior and a change has a documented compatibility path.
