---
name: behave-testing
description: "Configures Behave for Python BDD scenarios - `pip install behave`, authors `.feature` files in Gherkin, writes step implementations in `features/steps/*.py`, configures via `environment.py` for setup/teardown hooks, organizes via tags, runs via `behave`. Use for Python codebases that want Cucumber-family BDD without Cucumber-Ruby / Cucumber-JS."
---

# behave-testing

## Overview

Per [behave-docs][bd]:

[bd]: https://behave.readthedocs.io/en/latest/

> "**behave is behaviour-driven development, Python style.**" It
> employs "tests written in a natural language style, backed up
> by Python code."

Per [behave-docs][bd]: "Behavior-driven development encourages
collaboration between developers, QA and non-technical or business
participants in a software project."

Per [`cucumber-install`](https://cucumber.io/docs/installation/),
Behave is in the **semi-official** Cucumber tier (uses Cucumber
components but maintained outside the main org).

## When to use

- The codebase is Python and the team uses BDD.
- Acceptance criteria are authored in Gherkin (per
  `gherkin-from-stories`).
- pytest with parametrize isn't sufficient - non-engineers read
  the tests.

## Step 1 - Install

```bash
pip install behave
```

## Step 2 - Project layout

Behave's conventional layout:

```
project/
├── features/
│   ├── cart.feature                # Gherkin features
│   ├── steps/
│   │   ├── cart_steps.py            # step implementations
│   │   └── shared_steps.py
│   └── environment.py               # setup/teardown hooks
└── ...
```

## Step 3 - Author a Feature

```gherkin
# features/cart.feature
Feature: Apply promo code at checkout

  Background:
    Given a logged-in user
    And the cart contains 1 of "BOOK-001" at $24.99

  Scenario: Apply valid promo
    When I enter "WELCOME10" in the promo input
    And I click "Apply"
    Then the subtotal updates to $22.49

  Scenario Outline: Promo validation
    When I enter "<code>" in the promo input
    And I click "Apply"
    Then an error appears: "<error>"

    Examples:
      | code      | error                 |
      | EXPIRED50 | This code has expired |
      | NOTREAL   | Code not found        |
```

## Step 4 - Write step implementations

```python
# features/steps/cart_steps.py
from behave import given, when, then
from app.cart import Cart
from app.checkout import CheckoutPage
from tests.fixtures import login_user

@given('a logged-in user')
def step_logged_in_user(context):
    context.user = login_user()
    context.page = CheckoutPage(context.user)

@given('the cart contains {qty:d} of "{sku}" at ${price:f}')
def step_cart_contains(context, qty, sku, price):
    context.cart = Cart()
    context.cart.add_item(sku, qty, price)
    context.page.set_cart(context.cart)

@when('I enter "{code}" in the promo input')
def step_enter_promo(context, code):
    context.page.enter_promo(code)

@when('I click "{label}"')
def step_click(context, label):
    context.page.click(label)

@then('the subtotal updates to ${expected:f}')
def step_subtotal(context, expected):
    assert abs(context.page.get_subtotal() - expected) < 0.01, \
        f"Expected {expected}, got {context.page.get_subtotal()}"

@then('an error appears: "{message}"')
def step_error(context, message):
    assert message in context.page.get_error_message()
```

The `context` object carries state across steps within a scenario.

## Step 5 - Hooks via `environment.py`

Per [behave-docs][bd], `environment.py` provides "Environmental
Controls":

```python
# features/environment.py
def before_all(context):
    """Once before any scenario runs."""
    context.config.setup_logging()
    context.db = setup_test_database()

def after_all(context):
    """Once after all scenarios finish."""
    context.db.close()

def before_scenario(context, scenario):
    """Before each scenario."""
    context.db.start_transaction()

def after_scenario(context, scenario):
    """After each scenario (use scenario.status to check pass/fail)."""
    context.db.rollback()

def before_tag(context, tag):
    """Before scenarios with a specific tag."""
    if tag == 'requires_browser':
        context.browser = launch_browser()

def after_tag(context, tag):
    if tag == 'requires_browser':
        context.browser.quit()
```

The hook hierarchy: `before_all` > `before_feature` >
`before_scenario` > `before_step` (and the matching `after_*`).

## Step 6 - Tags + filtering

Per [behave-docs][bd], "Controlling Things With Tags" is the
filter mechanism:

```gherkin
@critical @regression
Scenario: Apply valid promo
  ...

@wip
Scenario: New checkout flow (work in progress)
  ...
```

```bash
# Run only critical
behave --tags=critical

# Skip wip
behave --tags=~wip

# Combine
behave --tags=critical --tags=~slow
```

## Step 7 - Reporting

```bash
# Plain text + JUnit XML for CI
behave --junit --junit-directory reports/junit/

# Per-feature output, no colors
behave --format=plain --no-color > test-results.txt
```

The JUnit XML feeds `junit-xml-analysis` (in the qa-test-reporting plugin).

## Step 8 - Run

```bash
behave                         # all features
behave features/cart.feature   # one feature
behave --tags=@critical         # by tag
behave -i cart                  # match file pattern
```

## Step 9 - pytest-bdd alternative

Per [behave-docs][bd], Behave is the canonical Python BDD; the
ecosystem also includes **pytest-bdd** which integrates Gherkin
into pytest. Choose:

| Behave                                    | pytest-bdd                                   |
|-------------------------------------------|----------------------------------------------|
| Standalone runner                          | pytest plugin                                |
| Closer to Cucumber semantics              | Reuses pytest fixtures                        |
| Better for pure-BDD teams                  | Better when mixing BDD + xUnit-style tests   |

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Mixing fixtures across `context` and module-level state               | Hidden coupling; test order matters.                                     | Use `context` only; reset per scenario via `before_scenario` (Step 5). |
| Step regex too greedy                                                  | One step matches multiple Gherkin lines.                                  | Use `{var}` placeholders + type hints (`{qty:d}` per Step 4). |
| `before_all` setup that fails                                           | All scenarios fail; debugging hard.                                       | Quick smoke check in `before_all`; fail fast with clear message. |
| `@wip` scenarios shipping in CI                                         | Test runner counts them as passes.                                       | `behave --tags=~wip` in CI (Step 6). |
| One step file with 200 steps                                            | Hard to navigate; merge conflicts.                                        | Split per-feature: `cart_steps.py`, `checkout_steps.py`, etc. |

## Limitations

- **Slower than pytest.** Behave's parsing + step matching adds
  overhead; pytest is faster for non-BDD use.
- **No native parallel runner.** Use `behave-parallel` plugin OR
  shard at CI level via tag filtering.
- **Gherkin variations.** Some Cucumber features (Rule blocks per
  Gherkin 6+) have spotty Behave support; verify for the version
  pinned.

## References

- [bd][bd] - Behave overview: BDD Python-style; step
  implementations + environment.py + tags; cross-stakeholder
  collaboration framing.
- `cucumber-testing`,
  `reqnroll-testing` - sibling
  language wrappers.
- `bdd-step-library-curator` - keeps step proliferation in check.
