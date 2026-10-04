---
name: web-server-development
description: "Use when implementing an HTTP server, routing layer, reverse proxy, or web-serving runtime to define supported protocol behavior, concurrency and resource limits, and trust boundaries before exposing a listener; test malformed requests and filesystem access in a local harness. Trigger for request parsing, routing, middleware, static files, or server lifecycle work."
---

# Web Server Development

## Overview

This skill applies when implementing an HTTP server, routing layer, reverse proxy, or web-serving runtime. Its intended outcome is to define supported protocol behavior, concurrency and resource limits, and trust boundaries before exposing a listener; test malformed requests and filesystem access in a local harness.

## When to Use

### Preserved source section: When to Use

Use for a server that accepts HTTP or a related web protocol. State whether the target is an educational implementation, embedded server, or production service and which protocol version/features are supported.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Safety and Acceptance

Do not bind publicly or deploy merely because local tests pass. Accept only when the stated protocol subset, boundary checks, resource limits, and failure behavior are verified; report which security properties depend on a proxy or platform outside the server.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Routes, methods, request/response formats, body limits, and compatibility needs.
- Concurrency, timeouts, TLS or proxy termination, logging, and deployment environment.
- Authentication, authorization, filesystem access, and network exposure boundaries.

## Instructions

### Preserved source section: Procedure

1. **Define the wire contract.** Specify request-line and header parsing, framing, supported methods, status codes, connection reuse, and unsupported protocol features.
2. **Parse defensively.** Enforce header/body limits, reject ambiguous framing, normalize paths once, and fail closed on malformed or conflicting fields.
3. **Keep routing and effects separate.** Match routes explicitly, validate inputs before handlers run, and make authentication and authorization checks visible at the server boundary.
4. **Protect static and dynamic content.** Prevent path traversal, unsafe redirects, header injection, request smuggling, and unescaped output. Avoid serving secrets or hidden files.
5. **Bound resource use.** Set connection, request, queue, upload, idle-time, and response limits. Handle slow clients and cancellation without leaking work.
6. **Test adversarial and lifecycle cases.** Cover malformed requests, oversized bodies, disconnects, concurrent requests, shutdown, TLS/proxy assumptions, and error responses in an isolated local environment.
7. **Observe before deployment.** Add structured logs and health signals without recording credentials or sensitive request bodies. Keep listener exposure and firewall changes behind explicit approval.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Safety and Acceptance

Do not bind publicly or deploy merely because local tests pass. Accept only when the stated protocol subset, boundary checks, resource limits, and failure behavior are verified; report which security properties depend on a proxy or platform outside the server.

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs

- Concurrency, timeouts, TLS or proxy termination, logging, and deployment environment.

### Source edge/failure guidance from: Procedure

2. **Parse defensively.** Enforce header/body limits, reject ambiguous framing, normalize paths once, and fail closed on malformed or conflicting fields.
6. **Test adversarial and lifecycle cases.** Cover malformed requests, oversized bodies, disconnects, concurrent requests, shutdown, TLS/proxy assumptions, and error responses in an isolated local environment.

### Source edge/failure guidance from: Safety and Acceptance

Do not bind publicly or deploy merely because local tests pass. Accept only when the stated protocol subset, boundary checks, resource limits, and failure behavior are verified; report which security properties depend on a proxy or platform outside the server.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Safety and Acceptance

Do not bind publicly or deploy merely because local tests pass. Accept only when the stated protocol subset, boundary checks, resource limits, and failure behavior are verified; report which security properties depend on a proxy or platform outside the server.
