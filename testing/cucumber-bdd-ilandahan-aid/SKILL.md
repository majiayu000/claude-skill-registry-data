---
name: cucumber-bdd
description: Cucumber BDD integration for AID methodology. Gherkin-first acceptance criteria with executable specifications. Use for writing feature files, step definitions, and running acceptance tests.
---

# Cucumber BDD Skill

Turn acceptance criteria into executable tests: `.feature` files (Gherkin) → step definitions → HTML report.

## Phase Integration

| Phase | Cucumber Activity | Deliverable |
|-------|-------------------|-------------|
| **1 PRD** | Write acceptance criteria as .feature files | `features/*.feature` |
| **2 Tech Spec** | Define step definition architecture | Step definition plan |
| **3 Impl Plan** | Plan step implementation tasks | Task breakdown |
| **4 Development** | Implement step definitions (TDD) | `features/step-definitions/*.ts` |
| **5 QA & Ship** | Execute scenarios, verify all pass | `reports/cucumber-report.html` |

## Quick Start

```bash
# Phase 1: write feature file, e.g. features/auth/login.feature
# Phase 4: see undefined steps, then implement features/step-definitions/auth.steps.ts
npm run cucumber:dry
# Phase 5: execute and generate report
npm run test:bdd
```

## Gherkin Keywords

| Keyword | Purpose | Example |
|---------|---------|---------|
| `Feature` | Describes the feature being tested | `Feature: User Authentication` |
| `Scenario` | A single test case | `Scenario: Successful login` |
| `Given` | Precondition/context | `Given I am on the login page` |
| `When` | Action being tested | `When I enter valid credentials` |
| `Then` | Expected outcome | `Then I should see the dashboard` |
| `And` / `But` | Additional steps | `And I should see a welcome message` |
| `Background` | Shared preconditions | Runs before each scenario |
| `Scenario Outline` | Parameterized scenarios | With `Examples` table |

## Feature File Template

Emit traceability comments, tags, a WHY/BUSINESS VALUE docstring, the As a/I want/So that role block, `Background`, then scenarios.

```gherkin
# Research: PROJECT-A-INT-001, PROJECT-A-JTBD-002
# PRD: US-001 User Login
@auth @critical
Feature: User Authentication
  """
  WHY: Users need secure access to personal data
  BUSINESS VALUE: Reduces support tickets by 40%
  """

  As a registered user
  I want to log in with my credentials
  So that I can access my personalized dashboard

  Background:
    Given the authentication service is running
    And I am on the login page

  @smoke @happy-path
  Scenario: Successful login with valid credentials
    Given I have a registered account with email "user@example.com"
    When I enter email "user@example.com"
    And I enter password "SecurePass123!"
    And I click the login button
    Then I should be redirected to the dashboard
    And I should see "Welcome back, User"

  @error-handling
  Scenario: Failed login shows helpful error message
    When I enter email "unknown@example.com"
    And I enter password "wrongpassword"
    And I click the login button
    Then I should see error message "Invalid email or password"
    And I should remain on the login page
    And the password field should be cleared

  @security
  Scenario Outline: Account lockout after failed attempts
    Given I have a registered account with email "<email>"
    When I enter incorrect password <attempts> times
    Then my account should be <status>
    And I should see "<message>"

    Examples:
      | email              | attempts | status  | message                           |
      | user@example.com   | 3        | active  | 2 attempts remaining              |
      | user@example.com   | 5        | locked  | Account locked. Reset password.   |
```

## Step Definition Patterns

Given sets up preconditions (test data factories, navigation), When performs actions, Then asserts outcomes. Use `{string}` parameters instead of hardcoding values.

```typescript
// features/step-definitions/auth.steps.ts
import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from 'expect';

Given('I am on the login page', async function() {
  await this.page.goto('/login');
});

Given('I have a registered account with email {string}', async function(email: string) {
  this.testUser = await createTestUser({ email });
});

When('I enter email {string}', async function(email: string) {
  await this.page.fill('#email', email);
});

When('I click the login button', async function() {
  await this.page.click('#login-button');
  await this.page.waitForNavigation();
});

Then('I should be redirected to the dashboard', async function() {
  expect(this.page.url()).toContain('/dashboard');
});

Then('I should see error message {string}', async function(message: string) {
  const error = await this.page.textContent('.error-message');
  expect(error).toBe(message);
});
```

Share state across steps via a custom World class (`page`, `testUser`, `response`) in `features/support/world.ts` — see `references/cucumber-js-guide.md` for the `CustomWorld` implementation and hooks.

## Tag Standards

| Tag | When to Use | CI Behavior |
|-----|-------------|-------------|
| `@critical` | Must pass for release | Blocks deployment |
| `@smoke` | Quick sanity checks | Runs on every PR |
| `@regression` | Full test suite | Runs nightly |
| `@wip` | Work in progress | Excluded from CI |
| `@skip` | Temporarily disabled | Excluded (document reason!) |
| `@manual` | Cannot be automated | Excluded |
| `@security` | Security-related tests | Runs on security review |
| `@performance` | Performance tests | Runs on performance review |
| `@flaky` | Known flaky tests | Retried automatically |

### Tag Filtering

```bash
npx cucumber-js --tags "@critical"
npm run test:smoke
npx cucumber-js --tags "not @wip and not @manual"
npx cucumber-js --tags "@critical and @security"
npx cucumber-js --tags "@smoke or @critical"
```

## Commands

| Command | Purpose |
|---------|---------|
| `npm run cucumber` | Run all features with default profile |
| `npm run cucumber:dry` | Validate syntax without executing |
| `npm run test:bdd` | Run and generate HTML report |
| `npm run test:smoke` | Run @smoke scenarios only |
| `npm run test:critical` | Run @critical scenarios only |

## Related Skills

- `aid-prd` - PRD writing (where Gherkin acceptance criteria are created)
- `test-driven` - TDD methodology (Cucumber at the top of test pyramid)
- `aid-qa-ship` - QA verification (running Cucumber scenarios before release)

## Resources

- [Cucumber.js Documentation](https://cucumber.io/docs/cucumber/)
- [Gherkin Reference](https://cucumber.io/docs/gherkin/reference/)
- Language setup guides: `references/cucumber-js-guide.md`, `references/cucumber-python-guide.md`, `references/cucumber-java-guide.md`, `references/cucumber-go-guide.md`, `references/cucumber-ruby-guide.md`
