---
name: designing-tests
description: Use when designing test suites, planning test coverage, choosing which layer (unit/integration/E2E) to test at, writing test cases for microservice chains, state machines, or complex business logic. Use when asking how to scope tests, how to avoid over-testing across service boundaries, or how to apply equivalence partitioning, boundary value analysis, or decision tables.
---

# Designing Tests

Three steps guide effective test design: **read the spec** (derive every test case from requirements, not code), **enumerate a test list** (produce a structured checklist before writing any code), and **execute with focus** (layer and segment each test to the smallest meaningful boundary).

---

## Before Designing Any Tests — Read the Docs First

**Tests must be derived from requirements, not from implementation code.**

Reading the code first means you test what the system *does*, not what it *should do*. Bugs become encoded as expected behavior.

**STOP. Before writing any test case, locate and read:**

1. **Product / feature spec** — acceptance criteria, business rules, edge cases defined by product
2. **API contract / interface spec** — endpoints, request/response schema, error codes, authentication
3. **State machine diagram** — valid states, transitions, guards, invalid transition behavior
4. **Non-functional requirements** — idempotency constraints, SLA, consistency guarantees

**If no documentation exists: ask before proceeding.** Do not infer requirements from code.

**Do NOT read implementation code before writing tests.** Implementation code reveals *how it's built*, not *what it should do*. Tests written from implementation code encode current behavior as truth — including any bugs present. Derive every test case from specs only. If you have already read the implementation, set it aside and go back to the spec before writing assertions.

### Mapping Doc Artifacts to Test Cases

| Documentation artifact | Tests to derive |
|------------------------|----------------|
| Acceptance criteria | Integration test scenarios (one per criterion) |
| Business rule with conditions | Unit tests — apply equivalence partitioning to the rule's conditions |
| API contract (schema + status codes) | Integration tests: valid/invalid inputs, each error code, forbidden fields |
| State transition table | One test per valid transition + one per invalid transition per state |
| Idempotency requirement | Idempotency test cases (repeat same call, assert no duplication) |
| Non-functional requirement | Dedicated test or test tag (e.g., `@pytest.mark.slow` for SLA tests) |

### Common Rationalizations — Do Not Accept These

| Excuse | Reality |
|--------|---------|
| "The code is self-explanatory" | Code shows what it *does*. Docs show what it *should do*. They diverge at every bug. |
| "There are no docs" | Then stop and ask. Tests without specs are guesses that encode current behavior as truth. |
| "I'll check the docs after I draft the tests" | Tests written before reading specs miss requirements and anchor to implementation details. |
| "The existing tests are enough reference" | Existing tests may already be wrong. Always go back to the source. |

---

## Test Case Design Techniques

### Equivalence Partitioning

Divide the input space into classes where all values in a class produce the same behavior. Test **one representative per class** — testing more within the same class adds no value.

Typical classes for any input:
- Valid range / valid format
- Below minimum / above maximum
- Invalid type or format
- Empty / null / zero

### Boundary Value Analysis

Bugs cluster at boundaries. For every valid range `[min, max]`, test:

```
min-1  (just outside lower)
min    (lower boundary)
min+1  (just inside lower)
max-1  (just inside upper)
max    (upper boundary)
max+1  (just outside upper)
```

Always apply alongside equivalence partitioning — boundaries are the edges of equivalence classes.

### Decision Table

For logic controlled by multiple independent conditions, enumerate combinations explicitly to avoid missing cases.

| Condition A | Condition B | Expected Outcome |
|-------------|-------------|-----------------|
| true        | true        | result X        |
| true        | false       | result Y        |
| false       | true        | error Z         |
| false       | false       | error Z         |

When the number of combinations is large, use **pairwise testing** — cover every pair of condition values at least once rather than all N² combinations.

### State Transition (per test)

Each row in the state transition table becomes one test case:

| Current State | Event    | Expected State | Side Effects |
|---------------|----------|----------------|--------------|
| Created       | pay()    | Paid           | payment recorded |
| Paid          | ship()   | Shipped        | shipment created |
| Created       | ship()   | —              | InvalidTransitionError |

### When to Use Which Technique

| Situation | Technique |
|-----------|-----------|
| Input has a range or format constraint | Equivalence Partitioning + Boundary Value Analysis |
| Outcome depends on 2+ independent conditions | Decision Table |
| Entity moves through states | State Transition table |
| Input space is too large to enumerate manually | Pairwise testing (subset of Decision Table) |

---

## From Spec to Test List

After reading the spec, **generate a test list before opening any test file.** A test list is a structured checklist of test cases derived from the spec — it is a deliverable, not a mental note.

### The Process

```
Step 1: List every spec artifact as a separate item
        (each acceptance criterion, each state transition, each business rule, each API endpoint)

Step 2: Map each artifact to its test type
        (use the mapping table in "Before Designing Any Tests")

Step 3: Expand each item — enumerate specific cases using EP / BVA / decision tables
        Do not write "test the happy path". Write the exact scenario.

Step 4: Assign each case a layer (unit / integration / E2E)

Step 5: Write the formatted test list as a checklist (see format below)

Step 6: Review for gaps — for every success case, is there a corresponding error/boundary case?
```

### Test List Format

Write this in a comment block, a doc, or a dedicated file — before any test code.

```
# Test List: [Feature / Endpoint / Component]
# Source: [link or reference to spec]

## Unit Tests
- [ ] <unit>: <condition> → <expected outcome>

## Integration Tests
- [ ] <scenario> → <expected HTTP status / side effect>

## E2E Tests
- [ ] <user journey>
```

### Example: POST /orders

Spec: authenticated user submits items with valid SKUs and qty > 0; max 10 items; idempotency key prevents duplicates within 5 minutes.

```
# Test List: POST /orders
# Source: orders-api-spec.md §3.2

## Unit Tests (OrderService.place_order)
- [ ] valid items list → returns order with generated id
- [ ] empty items list → raises ValidationError
- [ ] item qty = 0 → raises ValidationError          (boundary: just outside)
- [ ] item qty = 1 → succeeds                        (boundary: minimum)
- [ ] 10 items → succeeds                            (boundary: maximum)
- [ ] 11 items → raises ValidationError              (boundary: just outside)
- [ ] invalid SKU format → raises ValidationError

## Integration Tests
- [ ] valid payload, authenticated → 201, order persisted in DB
- [ ] unauthenticated request → 401
- [ ] missing items field → 400
- [ ] item qty = 0 → 400
- [ ] same idempotency key submitted twice → same order_id returned, no duplicate in DB
- [ ] different idempotency keys → two separate orders created
- [ ] 11 items → 400

## E2E Tests
- [ ] authenticated user places order and receives confirmation (happy path)
```

### Review Checklist (Step 6)

Before moving to implementation, verify the list is complete:

| Check | Question |
|-------|----------|
| Error coverage | For every success case, is there an error/rejection case? |
| Boundary coverage | For every numeric range, are min, max, min-1, max+1 present? |
| State coverage | For every valid transition, is there an invalid transition test? |
| Idempotency | If spec mentions idempotency, are duplicate-call cases listed? |
| Auth/authz | Are unauthenticated and unauthorized scenarios covered? |
| Null/empty | Are null, empty, and missing required fields covered? |

---

## The Testing Pyramid

| Layer | Focus | Quantity |
|-------|-------|----------|
| **Unit** | Code implementation logic, boundary values, error paths | Many |
| **Integration** | Business scenarios and interface contracts within one service | Some |
| **E2E** | Critical user journeys through the real system | Few |

### Unit Tests

Test one function/method/class in isolation. Mock **all** external dependencies.

Cover:
- Core logic paths (happy path + variations)
- Boundary values (see Techniques below)
- Error conditions and invalid inputs
- Each branch of conditional logic

### Integration Tests

Test component interactions **within a single service** (e.g., handler → service → repository → DB).

Cover:
- Key business use cases end-to-end within the service
- Interface contracts (what the service accepts and returns)
- Side effects (DB writes, cache invalidation, events emitted)

Mock: external services, downstream APIs. Use real: internal DB, cache (prefer testcontainers).

### E2E Tests

Test user journeys through the real system with no mocks.

Cover: happy paths and primary user journeys only. Keep minimal — one test per critical flow.

---

## Segmentation Principles

### Microservice Chain

For a chain A → B → C → D, test each service independently:

- **Stub** the upstream input (don't trigger A to test B — construct B's input directly)
- **Mock** the downstream dependency (when testing B, mock C)
- Assert only B's behavior

```
❌ Test: trigger A → verify D's state
✅ Test: call B with stubbed input → verify B's output and side effects (C mocked)
```

### Message Queue

- **Producer test**: invoke the action on the service under test → assert the message published matches expected schema/content
- **Consumer test**: publish a test message directly to the queue (or call the handler directly) → assert the resulting side effects
- Never trigger from the upstream service to test a consumer

### State Machine

Test each state transition independently. Never traverse from initial state to final state in one test.

```
❌ Test: order Created → Paid → Shipped → Delivered
✅ Test: given order in Paid state → ship() → assert state is Shipped + shipment record created
✅ Test: given order in Created state → ship() → assert InvalidTransitionError
```

Pattern for each transition:
1. **Given**: set entity directly to source state (bypass prior transitions)
2. **When**: apply the triggering event/action
3. **Then**: assert target state + expected side effects
4. **Also test**: invalid transitions from the same source state

---

## Choosing the Right Layer

```
Is it pure logic with no I/O?
  → Unit

Does it verify a business scenario within one service (with real DB/cache)?
  → Integration

Does it represent a user journey across the full system?
  → E2E

Is it a state machine transition?
  → Unit (transition guard logic) + Integration (full scenario in context)
```

---

## Reference Files

Load when implementing:

| File | When to read |
|------|-------------|
| `references/unit-testing.md` | Writing unit tests: mocking strategy, AAA pattern, test doubles |
| `references/integration-testing.md` | Integration tests: testcontainers, message queue, API contract, DB isolation |
| `references/idempotency-testing.md` | Idempotency test patterns: PUT/DELETE, POST + idempotency key, consumer dedup |
| `references/e2e-testing.md` | E2E tests: Page Object Model, selectors, flaky test prevention |
| `references/test-review-protocol.md` | Test failure investigation, root cause protocol, test design red lines |
| `references/python-pytest.md` | Python/pytest: fixtures, parametrize, marks, mock patterns |
| `references/go-testing.md` | Go: table-driven tests, httptest, testify, testcontainers-go |
