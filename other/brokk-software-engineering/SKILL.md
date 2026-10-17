---
name: brokk-software-engineering
description: Design and implement APIs, backend services, databases, frontends, and refactoring with testing discipline across the full software stack.
---

# Software Engineering

## Purpose

Design and implement software across the full stack — APIs, backend services, databases, user interfaces, and refactoring — with testing discipline and quality standards that ensure correctness, maintainability, and reliability.

## When to Use

- **API Design**: When creating new API endpoints or services; before implementing server logic to ensure the contract is sound first.
- **Backend Development**: When implementing new server-side features, endpoints, business logic, or integrations.
- **Database Development**: When designing schemas, creating migrations, implementing data access logic, or optimizing performance.
- **Frontend Development**: When implementing UI components, pages, features, or integrating with backend APIs.
- **Testing**: Before or alongside implementing features; when fixing bugs; when refactoring code lacking coverage.
- **Refactoring**: When code is difficult to understand, modify, or extend; when preparing to add features to complex areas.
- **Deployment, infrastructure, or automation tasks**: Apply general engineering judgment (no dedicated sub-workflow; see Anti-Patterns).

## Workflow

**Step 1: Identify which sub-domain(s) the brief invokes; apply only those subsections below.**

### API Design

1. **Design the contract first.**
   - Define endpoints, operations, and their signatures before writing implementation code.
   - Model request and response schemas with clear types, constraints, and examples.
   - Use consistent naming conventions across the entire API surface.

2. **Apply API design principles.**
   - Design for evolvability: use versioning, avoid breaking changes, add fields rather than modifying existing ones.
   - Keep responses focused — include what clients need, not everything from the data model.

3. **Document and verify.**
   - Ensure the contract is self-documenting with clear descriptions and examples.
   - Validate the specification against schema standards (e.g., OpenAPI validation).

### Backend Development

1. **Implement the logic.**
   - Write the server-side code: handlers, services, data access, middleware.
   - Separate transport concerns (HTTP, messaging) from business logic.
   - Handle errors consistently and informatively — errors are part of the contract.

2. **Verify the implementation.**
   - Test endpoints and logic manually or through automated tests.
   - Check error responses, edge cases, and input validation.
   - Ensure the implementation matches the API contract.

### Database Development

1. **Implement migrations.**
   - Create reversible migrations (up and down).
   - Handle data backfills and transformations carefully.
   - Test migrations against realistic data volumes.

2. **Write data access logic.**
   - Implement queries, repositories, or data access objects.
   - Use parameterized queries to prevent injection.
   - Optimize for the access patterns (eager loading, batching, pagination).

3. **Verify correctness and performance.**
   - Test queries against realistic data.
   - Check query plans for full table scans or missing indexes (N+1 detection).
   - Verify data integrity constraints are enforced.
   - Ensure schema changes are backward-compatible where required.

### Frontend Development

1. **Identify states and plan state management.**
   - Enumerate all states the UI must handle: loading, empty, error, edge cases.
   - Decide on a deliberate state-management strategy (local, shared, server state).

2. **Implement the interface.**
   - Build components with semantic, accessible markup (keyboard navigation, screen reader basics).
   - Handle user interactions, validation, and feedback.
   - Integrate with backend APIs and services.

3. **Verify the implementation.**
   - Test across relevant screen sizes and browsers.
   - Check accessibility basics (keyboard navigation, screen reader).
   - Verify error and loading states are handled.

### Testing

1. **Analyze what to test.**
   - Identify the behavior to verify: happy path, error cases, edge cases, boundary conditions.
   - Build an edge-case catalog: empty inputs, null values, large data, concurrency.
   - Determine the appropriate test level (unit, integration, end-to-end).

2. **Structure the tests.**
   - Keep tests independent — no shared mutable state.
   - Test one behavior per test case.
   - Use descriptive names that explain the scenario and expected outcome.

3. **Run and verify.**
   - Run the full test suite to confirm nothing is broken.
   - Verify that tests are deterministic (same result every run).
   - Check that tests fail meaningfully when the code breaks.

4. **Bug-fix discipline.**
   - When fixing a bug, write a test that reproduces it first, then fix.

5. **Characterization tests for coverage gaps.**
   - For uncovered code, write characterization tests that capture current behavior before refactoring.

### Refactoring

1. **Establish a safety net.**
   - Understand what the code does, including edge cases.
   - Create characterization tests to capture current behavior before making changes.

2. **Make targeted changes.**
   - Change one thing at a time — keep each commit or change focused.
   - Preserve existing interfaces and behavior.
   - Improve naming, extract methods, simplify conditionals, reduce duplication.

3. **Verify behavior is preserved.**
   - Run existing tests to confirm nothing is broken.
   - Check edge cases and error paths.

## Quality Criteria

### Shared

- **Correctness, not just style.** Every change is justified by a requirement or a concrete quality improvement.
- **Behavior preservation (refactoring).** All existing tests pass; observable behavior is unchanged.
- **Determinism and independence (testing).** Tests are deterministic and isolated from each other.
- **Characterization tests for coverage gaps.** Uncovered code has characterization tests before refactoring.

### API Design

- The contract is designed before implementation begins.
- All endpoints have defined request and response schemas with types and constraints.
- Error responses are consistent across all endpoints.
- Breaking changes are avoided or explicitly versioned.
- The specification passes schema validation.

### Backend Development

- The implementation matches the API contract or specification.
- Error handling is consistent and informative.
- Business logic is testable and separated from transport concerns.

### Database Development

- Migrations are reversible and tested.
- Queries use indexes effectively and avoid common pitfalls (N+1, full scans).
- Data integrity is enforced at the database level where appropriate.
- Schema changes are backward-compatible where required.

### Frontend Development

- Components match the design and acceptance criteria.
- The UI handles loading, empty, error, and edge case states.
- Keyboard navigation and basic accessibility are in place.
- State management is consistent and predictable.

### Testing

- Each test verifies a single behavior or scenario.
- Tests fail with clear, descriptive messages.
- Coverage includes happy path, error cases, and edge cases.
- Assertions are specific enough to catch regressions ("would this catch a regression?").

### Refactoring

- Each change is small enough to be reviewed and understood.
- The code is measurably cleaner (less duplication, better naming, simpler structure).

## Anti-Patterns

### Shared

- **Over-engineering, gold-plating, over-abstraction**: Adding abstractions, patterns, or features before they are needed. Implement what is required; refactor when patterns emerge.
- **Applying subsections the brief does not invoke**: If the brief is "implement a backend endpoint," do not refactor the entire codebase or redesign the database schema. Stay focused.

### API Design

- **Implementation-first**: Letting server code define the API, resulting in inconsistent or leaky contracts.
- **Under-specification**: Omitting types, constraints, or examples from the contract.
- **Copy-paste APIs**: Repeating similar patterns instead of designing shared models.

### Backend Development

- **Fat controllers**: Putting business logic in request handlers instead of dedicated service layers.
- **Leaky abstractions**: Exposing implementation details through the API.
- **Silent failures**: Swallowing errors without logging or reporting.

### Database Development

- **God table**: Creating overly broad tables with many nullable columns instead of normalized designs.
- **Migration fear**: Avoiding schema changes because migrations are risky or untested.

### Frontend Development

- **Logic in components**: Putting business logic in UI components instead of separating concerns.
- **State sprawl**: Managing state in too many places without a clear strategy.
- **Accessibility afterthought**: Adding accessibility after the UI is built instead of during.

### Testing

- **Testing implementation details**: Writing tests that break when the code is refactored without changing behavior.
- **Over-mocking**: Mocking everything so the test doesn't actually test real interactions.
- **Coverage theater**: Aiming for a coverage percentage instead of meaningful assertions.
- **Flaky tests**: Tests that pass or fail nondeterministically, eroding trust in the suite.

### Refactoring

- **Big bang refactoring**: Trying to rewrite everything at once instead of incremental changes.
- **Refactoring without tests**: Making structural changes without a safety net.
- **Changing behavior**: Fixing bugs or adding features during a refactoring (mix concerns).
