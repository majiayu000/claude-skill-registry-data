---
name: bdd-writing
description: Guide developers on writing BDD specifications using Gherkin syntax, feature files, and step definitions
license: Complete terms in LICENSE.txt
---

# BDD Writing
**Version:** 0.17.0
**Source:** Skills/bdd-writing/SKILL.md

Guidance for writing Behavior-Driven Development specifications using Gherkin syntax.

## When to Use
- Writing acceptance criteria as executable specs
- Creating feature files
- Defining step definitions
- BDD + TDD integration
- Tool selection (Cucumber, pytest-bdd, etc.)

## What is BDD?
Bridge between technical and non-technical stakeholders using natural language that's also executable tests.

## Gherkin Syntax

| Keyword | Purpose |
|---------|---------|
| **Feature** | Groups related scenarios |
| **Scenario** | Single test case |
| **Given** | Preconditions/context |
| **When** | Action/event |
| **Then** | Expected outcome |
| **And/But** | Continue previous step type |
| **Background** | Shared setup for all scenarios |
| **Scenario Outline** | Parameterized with Examples |

### Basic Structure
```gherkin
Feature: User Authentication
  Scenario: Successful login
    Given a user "alice" exists with password "secret"
    When the user enters valid credentials
    Then the user sees the dashboard
```

### Parameterized Tests
```gherkin
Scenario Outline: Login variations
  Given a user "<username>" exists
  When login with "<input>"
  Then result is "<outcome>"

  Examples:
    | username | input   | outcome |
    | alice    | valid   | success |
    | alice    | invalid | failure |
```

## Step Definitions

Connect Gherkin steps to executable code.

**Pattern:** Match step text to function parameters
```python
@given('a user "{username}" exists')
def create_user(username):
    User.create(username=username)
```

**Best Practices:**
1. Keep steps reusable
2. Use parameters (avoid duplicate definitions)
3. Declarative over imperative (what, not how)

## Best Practices

| Do | Don't |
|----|-------|
| One behavior per scenario | Multiple behaviors per scenario |
| Business language | Technical jargon |
| 3-7 steps | 10+ steps |
| Independent scenarios | Dependencies between scenarios |
| Focus on behavior | Focus on UI mechanics |

## Anti-Patterns
- UI-focused steps (`click button id="submit"`)
- Too many steps (split into focused scenarios)
- Coupled steps (shared state between steps)
- Inconsistent language (customer/user/client)

## BDD + TDD Integration (Double Loop)
```
OUTER LOOP: BDD (Acceptance Tests)
  1. Write failing acceptance scenario

  INNER LOOP: TDD (Unit Tests)
    2. RED: Write failing unit test
    3. GREEN: Minimal code to pass
    4. REFACTOR: Improve
    5. Repeat until feature complete

  6. Acceptance scenario passes
  7. Next scenario
```

## Tool Selection

| Tool | Language |
|------|----------|
| Cucumber | JS, Java, Ruby |
| pytest-bdd | Python (with pytest) |
| SpecFlow | C#/.NET |
| Behave | Python |
| Karate | Java (API testing) |

---

**End of BDD Writing Skill**
