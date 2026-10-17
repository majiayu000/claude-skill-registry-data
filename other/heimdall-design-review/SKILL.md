---
name: heimdall-design-review
description: Review system designs and API specifications as pre-implementation gates, evaluating alternatives and trade-offs.
---

# Design Review

## Purpose

Review design artifacts — system designs, ADRs, and API specifications — as pre-implementation gates. Evaluate design decisions explicitly with alternatives considered, not just described. This skill reviews specifications and architectural proposals before implementation begins, ensuring the design layer is sound before concrete work starts.

## When to Use

- Before implementing a significant new feature or system.
- When reviewing proposed architectural changes or system designs.
- After a system design document or ADR has been drafted.
- After an API specification has been created or modified.
- Before implementing an API on the server or consuming it on the client.
- To confirm a design is sound before implementation begins.

## Workflow

1. **Identify which sub-domain(s) the brief invokes; apply only those subsections.**

### Architecture

Evaluate architectural decisions and system designs to identify risks and assess trade-offs.

- Assess component boundaries, responsibilities, and coupling.
- Evaluate scalability, maintainability, and extensibility.
- Identify potential failure modes and single points of failure.
- Assess operational complexity and deployment implications.
- Challenge unstated assumptions and hidden constraints.
- Question whether the design solves the right problem.
- Consider alternative approaches and why they were rejected.
- Identify risks with specific scenarios, not general concerns.

### API Contracts

Review API specifications for consistency, correctness, and completeness as a pre-implementation gate.

- Verify endpoints, operations, and paths follow schema conventions.
- Check that naming is consistent across resources, fields, and operations.
- Ensure versioning strategy is clear and applied consistently.
- Verify all required fields are documented and optional fields are explicitly marked.
- Verify data types, formats, and constraints are correct and consistent.
- **Ensure error responses are defined for every failure mode (4xx, 5xx).**
- Verify that similar operations follow the same patterns (pagination, filtering, sorting, authentication, authorization).
- Ensure deprecation policies are documented where applicable.
- Breaking changes are explicitly called out and justified.
- Provide location-specific findings (path, operation, schema).

## Quality Criteria

- Design decisions are explicitly evaluated, not just described.
- Alternatives are considered and trade-offs are acknowledged.
- Risks are identified with specific scenarios, not general concerns.
- Recommendations are actionable and prioritized.
- All endpoints have complete request and response definitions.
- Naming and patterns are consistent across the entire API surface.

## Anti-Patterns

- **Rubber-stamping**: Approving a design without critical evaluation.
- **Ivory tower design**: Evaluating without considering practical implementation constraints.
- **Analysis paralysis**: Demanding perfect architecture instead of good-enough-for-now.
- **One-size-fits-all**: Applying the same patterns regardless of context.
- **Design by implementation**: Letting server internals leak into the API contract.
- **Inconsistent patterns**: Using different approaches for similar operations.
- **Missing error models**: Only defining success responses.
- **Over-fetching/under-fetching**: API responses don't match client needs.
