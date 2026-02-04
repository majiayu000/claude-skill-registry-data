---
name: implement-step-definitions
description: Implement step definitions for Gherkin scenarios, translating Given/When/Then into executable test code. Use after write-scenario when scenarios are defined but step definitions are missing.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# implement-step-definitions

**Skill Type**: Actuator (BDD Workflow)
**Purpose**: Translate Given/When/Then scenarios into executable test code
**Prerequisites**:
- Feature file exists with Gherkin scenarios
- BDD framework available (Cucumber, Behave, etc.)

---

## Agent Instructions

You are in the **STEP DEFINITIONS** phase of BDD (SCENARIO → STEP DEFINITIONS → IMPLEMENT → REFACTOR).

Your goal is to translate **Given/When/Then steps** into **executable test code** (step definitions).

---

## Workflow

### Step 1: Read Feature File

**Parse the Gherkin scenarios**:
- What Given/When/Then steps exist?
- Which steps are reusable across scenarios?
- What test fixtures are needed?

**Example**:
```gherkin
# features/authentication.feature

Scenario: Successful login
  Given I am a registered user with email "user@example.com"
  And my password is "SecurePassword123!"
  When I enter email "user@example.com"
  And I enter password "SecurePassword123!"
  And I click the "Login" button
  Then I should see "Welcome back"

# Unique steps needed:
# - Given I am a registered user with email {email}
# - And my password is {password}
# - When I enter email {email}
# - And I enter password {password}
# - And I click the {button} button
# - Then I should see {message}
```

---

### Step 2: Determine Step Definition File Location

**Follow BDD framework conventions**:

**Cucumber (JavaScript/TypeScript)**:
```
features/step_definitions/authentication_steps.js
features/step_definitions/authentication_steps.ts
```

**Behave (Python)**:
```
features/steps/authentication_steps.py
```

**Cucumber (Java)**:
```
src/test/java/steps/AuthenticationSteps.java
```

---

### Step 3: Write Step Definitions

**Template for Python (Behave)**:

```python
# features/steps/authentication_steps.py

# Validates: <REQ-ID>
# Business Rules: BR-001, BR-002, BR-003

from behave import given, when, then
from src.auth.authentication import login
from test_helpers import create_test_user, get_ui_element

# Test fixtures
_test_users = {}
_login_result = None
_ui_state = {}


@given('I am a registered user with email "{email}"')
def step_impl(context, email):
    """Create a test user with specified email"""
    # Validates: <REQ-ID>
    user = create_test_user(email=email)
    _test_users[email] = user
    context.user = user


@given('my password is "{password}"')
def step_impl(context, password):
    """Set user's password"""
    context.user.set_password(password)


@when('I enter email "{email}"')
def step_impl(context, email):
    """User enters email in login form"""
    _ui_state['email_input'] = email


@when('I enter password "{password}"')
def step_impl(context, password):
    """User enters password in login form"""
    _ui_state['password_input'] = password


@when('I click the "{button}" button')
def step_impl(context, button):
    """User clicks a button"""
    if button == "Login":
        # Perform login action
        global _login_result
        email = _ui_state.get('email_input')
        password = _ui_state.get('password_input')
        _login_result = login(email, password)


@then('I should see "{message}"')
def step_impl(context, message):
    """Verify user sees expected message"""
    # This would check UI in real implementation
    # For now, check login result
    if message == "Welcome back":
        assert _login_result.success == True
    else:
        assert _login_result.error == message


@then('I should be redirected to the dashboard')
def step_impl(context):
    """Verify user is redirected"""
    assert _login_result.success == True
    # In real implementation, check URL or page content
```

**Key elements**:
- ✅ Tag with REQ-* key in comments
- ✅ One step definition per unique step
- ✅ Parameterized step definitions (use `{parameter}`)
- ✅ Reusable across scenarios
- ✅ Clear docstrings explaining step purpose

---

**Template for JavaScript (Cucumber)**:

```javascript
// features/step_definitions/authentication_steps.js

// Validates: <REQ-ID>
// Business Rules: BR-001, BR-002, BR-003

const { Given, When, Then } = require('@cucumber/cucumber');
const { login } = require('../../src/auth/authentication');
const assert = require('assert');

let testUser;
let loginResult;
let uiState = {};

Given('I am a registered user with email {string}', function(email) {
  // Validates: <REQ-ID>
  testUser = createTestUser(email);
});

Given('my password is {string}', function(password) {
  testUser.setPassword(password);
});

When('I enter email {string}', function(email) {
  uiState.email = email;
});

When('I enter password {string}', function(password) {
  uiState.password = password;
});

When('I click the {string} button', function(button) {
  if (button === 'Login') {
    loginResult = login(uiState.email, uiState.password);
  }
});

Then('I should see {string}', function(message) {
  if (message === 'Welcome back') {
    assert.strictEqual(loginResult.success, true);
  } else {
    assert.strictEqual(loginResult.error, message);
  }
});
```

---

### Step 4: Run Scenarios (Expect FAILURE)

**Run BDD framework**:

```bash
# Behave (Python)
behave features/authentication.feature

# Cucumber (JavaScript)
npm run cucumber

# Cucumber (Java)
mvn test -Dcucumber.options="features/authentication.feature"
```

**Expected output**:
```
Feature: User Login

  Background:
    Given the application is running           PASSED
    And I am on the login page                PASSED

  Scenario: Successful login
    Given I am a registered user              PASSED
    And my password is "SecurePassword123!"   PASSED
    When I enter email "user@example.com"     PASSED
    And I enter password "SecurePassword123!" PASSED
    And I click the "Login" button            FAILED
      AttributeError: 'NoneType' object has no attribute 'success'
      (login function doesn't exist yet)
```

**✅ This is GOOD!** Steps execute but implementation doesn't exist yet.

---

### Step 5: Commit Step Definitions

**Create commit**:

```bash
git add features/steps/authentication_steps.py
git commit -m "STEP DEF: Add step definitions for <REQ-ID>

Implement step definitions for user login scenarios.

Step definitions:
- Given steps: Set up test users and state
- When steps: Simulate user actions
- Then steps: Verify expected outcomes

Steps: 12 step definitions (scenarios fail - no implementation yet)

Validates: <REQ-ID>
"
```

---

## Output Format

When you complete the STEP DEFINITIONS phase, show:

```
[STEP DEFINITIONS Phase - <REQ-ID>]

Feature File: features/authentication.feature

Step Definitions Created:
  Given steps (4):
    ✓ I am a registered user with email {email}
    ✓ my password is {password}
    ✓ the application is running
    ✓ I am on the login page

  When steps (5):
    ✓ I enter email {email}
    ✓ I enter password {password}
    ✓ I click the {button} button
    ✓ I attempt to login with email {email} and password {password}

  Then steps (3):
    ✓ I should see {message}
    ✓ I should be redirected to the dashboard
    ✓ my account should be locked

Step Definition File: features/steps/authentication_steps.py (12 steps, 142 lines)

Running scenarios...
  Scenario: Successful login              FAILED (no implementation)
  Scenario: Login fails invalid email     FAILED (no implementation)
  Scenario: Login fails short password    FAILED (no implementation)
  Scenario: Account locks after 3 fails   FAILED (no implementation)

Result: 5 scenarios FAILED ✓ (expected - implementation missing)

Commit: STEP DEF: Add step definitions for <REQ-ID>

✅ STEP DEFINITIONS Phase Complete!
   Next: Invoke implement-feature skill to implement functionality
```

---

## Prerequisites Check

Before invoking this skill, ensure:
1. Feature file exists (from write-scenario)
2. BDD framework available
3. Step definitions directory exists

If prerequisites not met:
- No feature file → Invoke `write-scenario` skill first
- No BDD framework → Ask user which to install

---

## Next Steps

After STEP DEFINITIONS phase completes:
1. **Do NOT implement feature yet** (that's next phase)
2. Invoke `implement-feature` skill to implement functionality
3. Scenarios should PASS after implementation

---

## Step Definition Patterns

### Parameterized Steps

**✅ Good** (reusable):
```python
@given('I am a user with email "{email}"')
def step_impl(context, email):
    context.user = create_user(email)
```

**❌ Bad** (hard-coded):
```python
@given('I am a user with email user@example.com')
def step_impl(context):
    context.user = create_user('user@example.com')
```

### Shared Context

**Use `context` object** to share state between steps:
```python
@given('I am logged in')
def step_impl(context):
    context.user = login()

@when('I view my profile')
def step_impl(context):
    context.profile = get_profile(context.user)  # Uses user from Given

@then('I should see my email')
def step_impl(context):
    assert context.profile.email == context.user.email
```

### Test Helpers

**Extract common logic** to helpers:
```python
# test_helpers.py

def create_test_user(email, password="DefaultPass123!"):
    """Create a user for testing"""
    user = User(email=email)
    user.set_password(password)
    user.save()
    return user

def cleanup_test_users():
    """Delete all test users"""
    User.delete_where(email__startswith="test_")
```

---

## Notes

**Why step definitions separate from implementation?**
- Step definitions = test automation code
- Implementation = production code
- Separation of concerns (test vs production)
- Step definitions can test multiple implementations

**Step definition reusability**:
- Same step definitions can test multiple features
- Parameterized steps increase reusability
- Keep step definitions simple and focused

**Homeostasis Goal**:
```yaml
desired_state:
  all_steps_defined: true
  steps_reusable: true
  scenarios_executable: true
```

**"Excellence or nothing"** 🔥
