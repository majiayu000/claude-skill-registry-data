---
name: domain-contract-validator
description: Define and enforce business rule assertions as automated checks using contract testing, schema validation, and invariant verification. Covers API contract.
---

# Domain Contract Validator

Define, generate, and enforce business rule assertions as automated checks that run independently of unit tests. While unit tests verify individual functions, domain contracts verify that the system as a whole respects business rules, API agreements, data schemas, and cross-service invariants. Contracts are deterministic, produce pass/fail results, and can be integrated into CI/CD pipelines as quality gates.

## When to Use This Skill

Use this skill when:

- You need to enforce API contracts between services (consumer-driven contract testing)
- Database schema changes must be validated against application expectations
- Event schemas (Kafka, RabbitMQ, SNS) must conform to agreed formats
- Business rules span multiple modules and cannot be verified by a single unit test
- You want to catch contract violations early in CI, not in production
- You are defining deterministic guardrails for an AI agent workflow

**Trigger phrases**: "contract testing", "domain contracts", "schema validation", "API contract", "consumer-driven contracts", "business rule enforcement", "invariant checking", "pact testing", "schema registry"

## What This Skill Does

- **API Contract Definition**: Generate consumer-driven contract tests using Pact or similar frameworks
- **Schema Validation**: Create JSON Schema, Avro, or Protobuf validators for data structures
- **Invariant Assertion**: Define business invariants that must hold across operations
- **Database Contract Testing**: Verify that database schemas match application model expectations
- **Event Contract Validation**: Ensure event payloads conform to agreed schemas
- **CI Integration**: Produce pass/fail artifacts suitable for quality gates

## Instructions

### Step 1: Identify Contract Boundaries

Map the boundaries where contracts are needed:

| Boundary Type | Where | Example |
|--------------|-------|---------|
| **API boundary** | Between services or between frontend and backend | REST/GraphQL endpoint contracts |
| **Database boundary** | Between application code and database schema | Column types, constraints, indexes |
| **Event boundary** | Between event producers and consumers | Message payload schemas |
| **Module boundary** | Between internal modules with stable interfaces | Public function signatures and return types |
| **External service boundary** | Between your code and third-party APIs | Expected response formats |

### Step 2: Define Contracts

#### API Contracts (Consumer-Driven)

**Python (Pact):**

```python
"""Consumer-driven contract test for the User Service API."""
import atexit
import unittest
from pact import Consumer, Provider

pact = Consumer("OrderService").has_pact_with(
    Provider("UserService"),
    pact_dir="./pacts",
)
pact.start_service()
atexit.register(pact.stop_service)


class TestUserServiceContract(unittest.TestCase):
    def test_get_user_returns_expected_fields(self):
        """Contract: GET /users/{id} returns id, name, email."""
        expected = {
            "id": 123,
            "name": "Jane Doe",
            "email": "jane@example.com",
        }

        (
            pact.given("a user with ID 123 exists")
            .upon_receiving("a request for user 123")
            .with_request("GET", "/users/123")
            .will_respond_with(
                200,
                body=expected,
            )
        )

        with pact:
            result = user_client.get_user(123)
            self.assertEqual(result["id"], 123)
            self.assertIn("name", result)
            self.assertIn("email", result)
```

**JavaScript (Pact):**

```javascript
const { Pact } = require("@pact-foundation/pact");
const { like } = require("@pact-foundation/pact").Matchers;

const provider = new Pact({
  consumer: "OrderService",
  provider: "UserService",
  port: 1234,
});

describe("User Service Contract", () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  it("returns expected user fields", async () => {
    await provider.addInteraction({
      state: "a user with ID 123 exists",
      uponReceiving: "a request for user 123",
      withRequest: {
        method: "GET",
        path: "/users/123",
      },
      willRespondWith: {
        status: 200,
        body: {
          id: like(123),
          name: like("Jane Doe"),
          email: like("jane@example.com"),
        },
      },
    });

    const result = await userClient.getUser(123);
    expect(result).toHaveProperty("id");
    expect(result).toHaveProperty("name");
    expect(result).toHaveProperty("email");
  });
});
```

#### Schema Contracts (JSON Schema)

```python
"""Schema validation contract for order events."""
import jsonschema

ORDER_EVENT_SCHEMA = {
    "type": "object",
    "required": ["order_id", "customer_id", "items", "total", "created_at"],
    "properties": {
        "order_id": {"type": "string", "format": "uuid"},
        "customer_id": {"type": "string", "format": "uuid"},
        "items": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["product_id", "quantity", "unit_price"],
                "properties": {
                    "product_id": {"type": "string"},
                    "quantity": {"type": "integer", "minimum": 1},
                    "unit_price": {"type": "number", "minimum": 0},
                },
            },
        },
        "total": {"type": "number", "minimum": 0},
        "created_at": {"type": "string", "format": "date-time"},
    },
    "additionalProperties": False,
}


def validate_order_event(event: dict) -> None:
    """Validate an order event against the contract schema.

    Raises jsonschema.ValidationError on contract violation.
    """
    jsonschema.validate(instance=event, schema=ORDER_EVENT_SCHEMA)


# Contract test
def test_order_event_schema_contract():
    valid_event = {
        "order_id": "550e8400-e29b-41d4-a716-446655440000",
        "customer_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
        "items": [{"product_id": "SKU-001", "quantity": 2, "unit_price": 29.99}],
        "total": 59.98,
        "created_at": "2026-03-06T12:00:00Z",
    }
    validate_order_event(valid_event)  # should not raise


def test_order_event_rejects_missing_fields():
    invalid_event = {"order_id": "550e8400-e29b-41d4-a716-446655440000"}
    try:
        validate_order_event(invalid_event)
        assert False, "Should have raised ValidationError"
    except jsonschema.ValidationError:
        pass  # contract enforced
```

#### Business Invariant Contracts

```python
"""Business invariant checks that must hold across all operations."""


def check_account_balance_invariant(account):
    """Invariant: account balance must never be negative."""
    assert account.balance >= 0, (
        f"INVARIANT VIOLATION: Account {account.id} has negative balance "
        f"{account.balance}"
    )


def check_order_total_invariant(order):
    """Invariant: order total must equal sum of item prices * quantities."""
    computed_total = sum(
        item.unit_price * item.quantity for item in order.items
    )
    assert abs(order.total - computed_total) < 0.01, (
        f"INVARIANT VIOLATION: Order {order.id} total {order.total} "
        f"does not match computed total {computed_total}"
    )


def check_audit_trail_invariant(entity, audit_log):
    """Invariant: every mutation must have a corresponding audit entry."""
    mutations = entity.get_mutation_count()
    audit_entries = audit_log.count_entries_for(entity.id)
    assert mutations == audit_entries, (
        f"INVARIANT VIOLATION: Entity {entity.id} has {mutations} mutations "
        f"but only {audit_entries} audit entries"
    )
```

### Step 3: Integrate into CI/CD

Add contract tests as a dedicated CI step that runs after unit tests but before deployment.

**GitHub Actions example:**

```yaml
- name: Run contract tests
  run: |
    pytest tests/contracts/ -v --tb=short --junitxml=contract-results.xml
  continue-on-error: false
```

**Quality gate integration:**

```markdown
## Gate: contracts-pass
**Type**: Testing Gate
**Automation**: Fully automatic

### Required Criteria
| # | Criterion | Command |
|---|-----------|---------|
| R1 | All API contract tests pass | `pytest tests/contracts/api/` |
| R2 | All schema contract tests pass | `pytest tests/contracts/schemas/` |
| R3 | All invariant checks pass | `pytest tests/contracts/invariants/` |

### On Fail
Fix the contract violation. Do not weaken the contract to make tests pass.
```

### Step 4: Maintain Contracts

Contracts must evolve with the system but should be treated as versioned agreements:

- **Adding a new optional field**: non-breaking; no contract change needed
- **Adding a new required field**: breaking; update contract, notify all consumers
- **Removing a field**: breaking; deprecate first, then remove after consumers migrate
- **Changing a field type**: breaking; create a new contract version

## Best Practices

- **Contracts are agreements, not implementation details**: a contract describes what a boundary promises, not how it works internally; keep contracts stable even as implementations change
- **Test contracts from the consumer's perspective**: consumer-driven contracts ensure the provider delivers what consumers actually need, not what the provider thinks they need
- **Version your contracts**: when a breaking change is necessary, create a v2 contract and support both until all consumers migrate
- **Run contract tests in CI, not just locally**: contract violations caught locally can be ignored; violations in CI block the merge
- **Keep contracts close to the boundary**: contract test files should live near the boundary they protect (e.g., `tests/contracts/api/`, `tests/contracts/events/`)
- **Do not weaken contracts to make tests pass**: if a contract test fails, fix the code, not the contract (unless the contract itself is wrong)

## Related Skills

- `behavior-preservation-checker` - Verify contracts are preserved during refactoring
- `quality-gate-definitions` - Define gates that include contract checks
- `api-design` - Design APIs with contracts in mind
- `integration-test-generator` - Generate integration tests that complement contract tests
- `intent-based-review` - Use contract test results as verification evidence

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: Consumer-driven contract testing, JSON Schema validation, design-by-contract principles
