---
name: bdd-acceptance-tests
description: Generate executable BDD test files from Given/When/Then acceptance criteria using pytest-bdd (Python) or Cucumber.js (JavaScript). Bridges the gap between.
---

# BDD Acceptance Test Generator

Transform natural-language acceptance criteria (Given/When/Then format) into executable Behavior-Driven Development test files. This skill takes acceptance criteria produced by the `requirement-enhancer` skill (or written manually) and generates runnable BDD tests using pytest-bdd for Python projects or Cucumber.js for JavaScript projects.

## When to Use This Skill

Use this skill when:

- Acceptance criteria exist in Given/When/Then format but are not automated
- You want to bridge the gap between specifications and executable tests
- The team uses BDD as a development methodology
- You need to automate acceptance testing for a feature before implementation
- You want to verify that AI-generated code meets human-defined specifications
- You are implementing an intent-based review workflow and need test evidence for each criterion

**Trigger phrases**: "BDD tests", "acceptance tests", "Given When Then tests", "cucumber tests", "pytest-bdd", "feature file", "step definitions", "behavior-driven", "automate acceptance criteria", "gherkin"

## What This Skill Does

- **Feature File Generation**: Creates `.feature` files in Gherkin syntax from acceptance criteria
- **Step Definition Scaffolding**: Generates step definition files with implementation stubs
- **Fixture Setup**: Creates shared fixtures and test data builders for common patterns
- **Multi-Scenario Coverage**: Generates scenarios for happy path, error cases, and edge cases from a single criterion
- **Framework Integration**: Produces files compatible with pytest-bdd (Python) or Cucumber.js (JavaScript)

## Instructions

### Step 1: Parse Acceptance Criteria

Extract acceptance criteria from the source document. Accepted formats:

**Format A: Structured Given/When/Then (preferred)**

```
Given a registered user with a valid subscription
When the user requests a premium feature
Then the system grants access and logs the usage event
```

**Format B: Checklist style (convert to Given/When/Then)**

```
- User with valid subscription can access premium features
- Access is logged as a usage event
```

Convert checklist items to Given/When/Then:

| Checklist Item | Converted |
|---------------|-----------|
| User with valid subscription can access premium features | Given a registered user with a valid subscription / When the user requests a premium feature / Then the system grants access |
| Access is logged as a usage event | (extend the Then clause above) / And the system logs the usage event |

### Step 2: Generate Feature Files

Create a `.feature` file for each functional area. Group related scenarios together.

**Python (pytest-bdd) file structure:**

```
tests/
  features/
    payment_processing.feature
    user_registration.feature
  step_defs/
    test_payment_processing.py
    test_user_registration.py
    conftest.py
```

**JavaScript (Cucumber.js) file structure:**

```
features/
  payment_processing.feature
  user_registration.feature
  step_definitions/
    payment_processing.steps.js
    user_registration.steps.js
  support/
    world.js
```

**Feature file template:**

```gherkin
Feature: [Feature Name]
  As a [role]
  I want [capability]
  So that [benefit]

  Background:
    Given [common precondition shared by all scenarios]

  Scenario: [Happy path description]
    Given [precondition]
    When [action]
    Then [expected outcome]
    And [additional verification]

  Scenario: [Error case description]
    Given [precondition]
    When [invalid action]
    Then [error handling behavior]

  Scenario Outline: [Parameterized test description]
    Given [precondition with <parameter>]
    When [action with <input>]
    Then [outcome with <expected>]

    Examples:
      | parameter | input | expected |
      | value1    | in1   | out1     |
      | value2    | in2   | out2     |
```

### Step 3: Generate Step Definitions

#### Python (pytest-bdd)

```python
"""Step definitions for payment processing feature."""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Link feature file
scenarios("../features/payment_processing.feature")


# --- Fixtures ---

@pytest.fixture
def payment_context():
    """Shared context for payment scenarios."""
    return {"user": None, "result": None, "error": None}


# --- Given steps ---

@given(
    parsers.parse("a registered user with balance {amount:d}"),
    target_fixture="payment_context",
)
def given_user_with_balance(amount):
    """Set up a user with the specified balance."""
    user = create_test_user(balance=amount)
    return {"user": user, "result": None, "error": None}


# --- When steps ---

@when(parsers.parse("the user submits a payment of {amount:d}"))
def when_user_submits_payment(payment_context, amount):
    """Execute the payment action."""
    try:
        payment_context["result"] = process_payment(
            payment_context["user"], amount
        )
    except Exception as e:
        payment_context["error"] = e


# --- Then steps ---

@then("the payment is processed successfully")
def then_payment_succeeds(payment_context):
    """Verify payment succeeded."""
    assert payment_context["result"] is not None
    assert payment_context["result"].status == "success"
    assert payment_context["error"] is None


@then(parsers.parse("the user's balance is {expected:d}"))
def then_balance_is(payment_context, expected):
    """Verify the user's balance after payment."""
    assert payment_context["user"].balance == expected
```

**conftest.py setup:**

```python
"""Shared fixtures for BDD tests."""
import pytest


@pytest.fixture
def app_client():
    """Create a test client for the application."""
    # Replace with your application's test client setup
    from myapp import create_app
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client
```

**pytest configuration (pyproject.toml):**

```toml
[tool.pytest.ini_options]
markers = ["bdd: BDD acceptance tests"]
bdd_features_base_dir = "tests/features/"
```

#### JavaScript (Cucumber.js)

```javascript
// step_definitions/payment_processing.steps.js
const { Given, When, Then } = require("@cucumber/cucumber");
const assert = require("assert");

Given(
  "a registered user with balance {int}",
  function (amount) {
    this.user = createTestUser({ balance: amount });
    this.result = null;
    this.error = null;
  }
);

When(
  "the user submits a payment of {int}",
  async function (amount) {
    try {
      this.result = await processPayment(this.user, amount);
    } catch (error) {
      this.error = error;
    }
  }
);

Then(
  "the payment is processed successfully",
  function () {
    assert.strictEqual(this.result !== null, true);
    assert.strictEqual(this.result.status, "success");
    assert.strictEqual(this.error, null);
  }
);

Then(
  "the user's balance is {int}",
  function (expected) {
    assert.strictEqual(this.user.balance, expected);
  }
);
```

**World setup (support/world.js):**

```javascript
const { setWorldConstructor } = require("@cucumber/cucumber");

class CustomWorld {
  constructor() {
    this.user = null;
    this.result = null;
    this.error = null;
  }
}

setWorldConstructor(CustomWorld);
```

### Step 4: Expand Scenarios for Edge Cases

For each acceptance criterion, generate additional scenarios covering:

| Category | What to Generate |
|----------|-----------------|
| **Boundary values** | Minimum, maximum, zero, negative values |
| **Error conditions** | Invalid input, missing data, unauthorized access |
| **Concurrency** | Simultaneous actions, race conditions (if applicable) |
| **State transitions** | Before/after state, idempotency |
| **Empty/null inputs** | Empty strings, null values, missing optional fields |

**Example: expanding a single criterion into multiple scenarios:**

Original criterion:
> Given a user with a valid subscription, When they request a premium feature, Then the system grants access

Expanded scenarios:

```gherkin
Scenario: User with active subscription accesses premium feature
  Given a user with an active "premium" subscription
  When the user requests the "analytics-dashboard" feature
  Then access is granted
  And the response includes the feature content

Scenario: User with expired subscription is denied access
  Given a user with an expired "premium" subscription
  When the user requests the "analytics-dashboard" feature
  Then access is denied
  And the response includes a renewal prompt

Scenario: User with no subscription is denied access
  Given a user with no subscription
  When the user requests the "analytics-dashboard" feature
  Then access is denied
  And the response includes subscription options

Scenario: User with wrong subscription tier is denied access
  Given a user with an active "basic" subscription
  When the user requests the "analytics-dashboard" feature
  Then access is denied
  And the response explains the required tier
```

### Step 5: Validate and Run

#### Python

```bash
# Install pytest-bdd if not present
pip install pytest-bdd

# Run BDD tests
pytest tests/step_defs/ -v --tb=short

# Run only BDD tests with marker
pytest -m bdd -v
```

#### JavaScript

```bash
# Install Cucumber.js if not present
npm install --save-dev @cucumber/cucumber

# Run BDD tests
npx cucumber-js

# Run with specific feature
npx cucumber-js features/payment_processing.feature
```

Verify that:
1. All feature files parse without syntax errors
2. All step definitions are linked to feature file steps (no undefined steps)
3. Tests that should pass do pass
4. Tests that should fail (error cases) correctly verify the error behavior

## Best Practices

- **One feature file per functional area**: do not combine unrelated features; keep files focused and navigable
- **Reuse step definitions**: write generic steps (e.g., "Given a registered user") that work across multiple feature files via shared fixtures
- **Keep scenarios independent**: each scenario must be runnable in isolation without depending on another scenario's side effects
- **Use Background for shared preconditions**: if every scenario in a feature shares the same Given step, move it to a Background block
- **Avoid implementation details in feature files**: write scenarios in business language, not code; "When the user clicks the submit button" is better than "When a POST request is sent to /api/payments"
- **Use Scenario Outlines for data-driven tests**: if the same logic applies to multiple inputs, use a Scenario Outline with an Examples table rather than duplicating scenarios
- **Generate step stubs first, then implement**: write the feature file and step definition skeleton before implementing the actual logic; this validates the structure before investing in implementation
- **Map every acceptance criterion to at least one scenario**: if a criterion has no scenario, it has no automated verification

## Related Skills

- `requirement-enhancer` - Generate Given/When/Then acceptance criteria from requirements
- `intent-based-review` - Review code by checking acceptance criteria pass/fail status
- `unit-tests` - Generate unit tests (more granular than BDD tests)
- `test-cases` - Generate test case specifications
- `test-structure` - Set up test directory structure and configuration
- `e2e-testing-automation` - End-to-end tests that complement BDD acceptance tests

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: BDD methodology, Cucumber/Gherkin patterns, pytest-bdd documentation
