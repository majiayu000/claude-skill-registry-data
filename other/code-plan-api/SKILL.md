---
name: code-plan-api
description: Design API contracts. Use when asked to plan REST, GraphQL, gRPC, TRPC, OpenAPI, protobuf, or schema contract changes.
---

Generate an actionable API design plan based on task analysis and research.

## Process

### Step 1 - Identify Context

- Inspect changed files with `jj diff -s`; restrict with `jj diff -- path`.
- Focus on user-specified files, endpoints, clients, protocols, or paths.
- Identify the target protocol and schema format (REST, GraphQL, gRPC, TRPC, OpenAPI, protobuf, Zod/TypeBox, etc.).

### Step 2 - Research and Scout

Apply a scout lens to analyze existing API handlers, clients, schemas, validators, middleware, tests, and local API conventions:

- Map relevant files, conventions, and call paths; cite file paths and line numbers.
- Distinguish confirmed patterns from one-offs; stay read-only and task-relevant.

Apply a researcher lens to research official protocol/framework documentation, constraints, security guidance, and compatibility considerations:

- Prefer official documentation over blog posts; cite sources with URLs.
- Separate confirmed facts from plausible interpretations; note version requirements.
- Lead with the single most actionable recommendation.

- For APIs spanning module or service boundaries, apply an architect lens to analyze module boundaries, ownership, data flow, and interface contracts for {task}:
  - Map current boundaries, ownership, and dependency direction first.
  - Recommend the smallest API boundary/architecture that preserves invariants.
  - Avoid speculative generality.

Apply a planner lens to design a minimal API contract, including request/response shapes, errors, validation, and tradeoffs:

- Prefer simple, boring solutions; preserve existing project patterns.
- Make tradeoffs and assumptions explicit; scope to the current problem.

Apply a reviewer lens to review the proposed API for correctness, security, compatibility, simplicity, and project-convention risks:

- Ground findings in file paths and line numbers; prioritize the requested lens.
- Distinguish confirmed findings from speculative risks; explain why each issue matters.

### Step 3 - Adjudicate Decisions

- For high-impact or conflicting design choices, apply an oracle lens to adjudicate the conflicting API design recommendations for {task}:
  - Identify the decision; state assumptions and constraints.
  - Pick the smallest safe path that preserves future options.
  - Note what evidence would change the recommendation.

### Step 4 - Audit

- For production-bound changes, apply an auditor lens to audit the API design for {task} for production risks:
  - Contract compatibility, breaking changes, data loss, and rollback safety.
  - Flag only material risk; this is a final gate, not iterative style review.

### Step 5 - Validate Findings

- Read relevant code directly to validate findings.

### Step 6 - Design API

- Design only required resources, operations, fields, and data shapes; prefer flat, simple structures over deeply nested designs.
- Read the `john-ousterhout-software-design` reference and apply deep-modules and "define errors out of existence" — keep the interface surface small relative to behavior; prefer designing errors out over spreading exception handling across callers.
- For APIs crossing a process/network boundary, read the `martin-fowler-eaa-patterns` reference and apply Remote Facade (coarse-grained operations) plus Data Transfer Object (batch data into one round-trip); do not use DTOs within a single process.
- Consider versioning, pagination, error handling, auth, validation, and compatibility.
- Identify security risks and secure API patterns.

### Step 7 - Report

1. **Context Analysis** — existing API structure, patterns, clients/consumers, integration points.
2. **Security Considerations** — auth, authorization, validation, data exposure, abuse risks.
3. **Documentation & Best Practices** — protocol/framework constraints and common pitfalls.
4. **Simplicity Constraint** — minimal resources, operations, fields; over-engineering risks.
5. **API Design**:
   - Resources/operations or service methods.
   - Request/response shapes.
   - Errors, pagination, versioning, auth, validation.
   - Example requests/responses.
6. **Implementation Plan** — numbered concrete steps, file targets, verification strategy.

Prioritize actionable, specific guidance over abstract advice.
