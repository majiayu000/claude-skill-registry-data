---
name: refactor-bdd
description: Refactor BDD implementation (scenarios, step definitions, feature code) to improve quality and eliminate tech debt while keeping scenarios passing. Use after implement-feature when scenarios are green.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# refactor-bdd

**Skill Type**: Actuator (BDD Workflow)
**Purpose**: Refactor BDD implementation and eliminate tech debt (Principle #6)
**Prerequisites**:
- Scenarios are PASSING
- Step definitions exist
- Feature implementation exists

---

## Agent Instructions

You are in the **REFACTOR** phase of BDD (SCENARIO → STEP DEFINITIONS → IMPLEMENT → REFACTOR).

Your goal is to improve code quality **and eliminate technical debt** in:
1. Feature implementation (production code)
2. Step definitions (test code)
3. Scenarios (Gherkin files)

**Critical**: Scenarios must STILL PASS after refactoring.

---

## Workflow

### Step 1: Refactor Feature Implementation

**Apply same tech debt elimination as TDD refactor-phase**:

1. **Delete Unused Imports** (same as TDD)
2. **Remove Dead Code** (same as TDD)
3. **Delete Commented Code** (same as TDD)
4. **Simplify Complex Logic** (same as TDD)
5. **Remove Duplication** (same as TDD)

**See**: `refactor-phase` skill (TDD) for detailed pruning instructions.

---

### Step 2: Refactor Step Definitions

**Improve step definition quality**:

#### 2.1 Extract Reusable Steps

**Before** (duplication):
```python
@given('I am a registered user with email "user1@example.com"')
def step_impl(context):
    context.user = create_user("user1@example.com")

@given('I am a registered user with email "user2@example.com"')
def step_impl(context):
    context.user = create_user("user2@example.com")
```

**After** (parameterized):
```python
@given('I am a registered user with email "{email}"')
def step_impl(context, email):
    context.user = create_user(email)
```

#### 2.2 Extract Test Helpers

**Before** (logic in step definitions):
```python
@given('I am a logged in user')
def step_impl(context):
    user = User(email="test@example.com")
    user.set_password("TestPass123!")
    user.save()
    token = authenticate(user.email, "TestPass123!")
    context.user = user
    context.token = token
```

**After** (extracted to helper):
```python
# test_helpers.py
def create_logged_in_user(email="test@example.com"):
    user = create_test_user(email)
    token = authenticate(user.email, user.password)
    return user, token

# Step definition
@given('I am a logged in user')
def step_impl(context):
    context.user, context.token = create_logged_in_user()
```

#### 2.3 Simplify Step Logic

**Before** (complex step):
```python
@when('I submit the login form')
def step_impl(context):
    email = context.email_input if hasattr(context, 'email_input') else None
    password = context.password_input if hasattr(context, 'password_input') else None
    if email is None or password is None:
        raise ValueError("Email and password must be set first")
    try:
        result = login(email, password)
        context.login_result = result
    except Exception as e:
        context.login_error = str(e)
```

**After** (simplified):
```python
@when('I submit the login form')
def step_impl(context):
    context.login_result = login(
        context.email_input,
        context.password_input
    )
```

#### 2.4 Delete Unused Steps

**Scan for step definitions with zero usage**:
```python
# This step is defined but never used in any scenario
@given('I have a premium account')
def step_impl(context):
    context.user.upgrade_to_premium()
# USAGE: 0 scenarios → DELETE
```

---

### Step 3: Refactor Scenarios (Gherkin)

**Improve scenario quality**:

#### 3.1 Extract Duplicate Preconditions to Background

**Before** (duplication):
```gherkin
Scenario: Login succeeds
  Given I am on the login page
  And the application is running
  When I enter valid credentials
  Then I should see "Welcome"

Scenario: Login fails
  Given I am on the login page
  And the application is running
  When I enter invalid credentials
  Then I should see "Error"
```

**After** (Background):
```gherkin
Background:
  Given the application is running
  And I am on the login page

Scenario: Login succeeds
  When I enter valid credentials
  Then I should see "Welcome"

Scenario: Login fails
  When I enter invalid credentials
  Then I should see "Error"
```

#### 3.2 Improve Scenario Names

**Before** (vague):
```gherkin
Scenario: Test login
Scenario: Error case
```

**After** (descriptive):
```gherkin
Scenario: Successful login with valid credentials
Scenario: Login fails with invalid email format
```

#### 3.3 Remove Unused Scenarios

**Delete scenarios that**:
- Test features no longer in scope
- Are duplicates of other scenarios
- Test implementation details (not behavior)

---

### Step 4: Run Scenarios (Verify Still Passing)

**After EVERY refactoring change**:

```bash
behave features/authentication.feature -v
```

**Expected**: All scenarios STILL PASSING ✓

**If scenarios fail**: Undo refactoring and try different approach.

---

### Step 5: Before Committing Checklist

You **MUST** verify:
- ✅ All scenarios passing
- ✅ No unused imports (feature code + step definitions)
- ✅ No dead code (no unused step definitions)
- ✅ No commented-out code
- ✅ Max cyclomatic complexity ≤ 10
- ✅ No duplicated steps
- ✅ Scenarios use Background for common preconditions

**If ANY checklist item fails, DO NOT COMMIT. Fix it first.**

---

### Step 6: Commit Refactoring

**Create commit**:

```bash
git add features/ src/auth/ steps/
git commit -m "REFACTOR: Clean up <REQ-ID> (BDD)

Refactor BDD implementation for user login.

Feature Implementation:
  - Deleted 2 unused imports
  - Simplified login() complexity (8 → 5)
  - Added type hints to all functions

Step Definitions:
  - Extracted 3 steps to reusable helpers
  - Removed 2 unused step definitions
  - Simplified step logic

Scenarios:
  - Extracted common preconditions to Background
  - Improved scenario names for clarity
  - Removed 1 duplicate scenario

Scenarios: 5 scenarios still passing ✓
Tech Debt: 0 violations (Principle #6)
"
```

---

## Output Format

When you complete the REFACTOR phase, show:

```
[REFACTOR Phase - <REQ-ID> (BDD)]

Feature Implementation Refactored:
  ✓ Deleted 2 unused imports
  ✓ Simplified login() - complexity 8 → 5
  ✓ Added type hints to 4 functions
  ✓ Improved docstrings

Step Definitions Refactored:
  ✓ Extracted 3 steps to test_helpers.py
  ✓ Removed 2 unused step definitions
  ✓ Simplified complex step logic
  ✓ Parameterized 2 hard-coded steps

Scenarios Refactored:
  ✓ Extracted Background (2 common steps)
  ✓ Improved 3 scenario names
  ✓ Removed 1 duplicate scenario
  ✓ Better organized scenario order

Tech Debt Pruning (Principle #6):
  ✓ Deleted 2 unused imports
  ✓ Removed 2 unused step definitions (18 lines)
  ✓ Simplified 1 complex function (complexity 8 → 5)

File size changes:
  - src/auth/authentication.py: 167 lines → 142 lines (-15%)
  - steps/authentication_steps.py: 98 lines → 76 lines (-22%)
  - features/authentication.feature: 89 lines → 72 lines (-19%)

Running scenarios...
  ✓ All 5 scenarios still passing

Before Commit Checklist:
  ✓ All scenarios passing
  ✓ No unused imports
  ✓ No dead code (unused steps)
  ✓ No commented-out code
  ✓ Max complexity ≤ 10 (current: 5)
  ✓ Background used for common steps
  ✓ Scenarios well-named

Ready to commit!

Commit: REFACTOR: Clean up <REQ-ID> (BDD)

✅ REFACTOR Phase Complete!
```

---

## Prerequisites Check

Before invoking this skill, ensure:
1. Scenarios are PASSING
2. Step definitions exist
3. Feature implementation exists

If prerequisites not met:
- Scenarios failing → Go back to IMPLEMENT phase
- No step definitions → Go back to STEP DEFINITIONS phase
- No scenarios → Go back to SCENARIO phase

---

## Next Steps

After refactoring complete:
1. Verify all scenarios still pass
2. Create final commit (optional - or use REFACTOR commit as final)
3. Move to next requirement (start new BDD workflow)

---

## Configuration

This skill respects configuration in `.claude/plugins.yml`:

```yaml
plugins:
  - name: "@aisdlc/code-skills"
    config:
      bdd:
        extract_background: true      # Auto-extract common steps
        max_scenario_length: 10       # Max steps per scenario
        require_scenario_tagging: true # Require REQ-* tags
      tech_debt:
        auto_detect_on_refactor: true
        max_complexity: 10
```

---

## BDD-Specific Refactoring

### Scenario Organization

**Group related scenarios** with Scenario Outline:

**Before**:
```gherkin
Scenario: Login with Visa card
  Given I have a Visa card
  When I pay
  Then payment succeeds

Scenario: Login with Mastercard
  Given I have a Mastercard
  When I pay
  Then payment succeeds
```

**After**:
```gherkin
Scenario Outline: Login with supported cards
  Given I have a <card_type> card
  When I pay
  Then payment succeeds

  Examples:
    | card_type  |
    | Visa       |
    | Mastercard |
```

### Step Definition Organization

**Group by feature** in separate files:
```
steps/
├── authentication_steps.py  # Login, logout, registration
├── payment_steps.py         # Payment processing
└── common_steps.py          # Shared steps (navigation, etc.)
```

---

## Notes

**Why refactor BDD?**
- Step definitions accumulate over time (pruning needed)
- Scenarios can become verbose (Background helps)
- Production code needs same quality as TDD code
- Principle #6 applies to ALL code (test code too)

**What makes BDD different from TDD refactoring**:
- Refactor 3 layers: scenarios, steps, implementation
- Scenarios should stay business-focused
- Step definitions should be reusable
- Feature code follows same rules as TDD

**Homeostasis Goal**:
```yaml
desired_state:
  scenarios_passing: true
  tech_debt: 0  # In all 3 layers
  step_definitions_reusable: true
  scenarios_concise: true
```

**"Excellence or nothing"** 🔥
