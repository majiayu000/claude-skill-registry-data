---
name: LAYER_12_TESTING
description: Expert knowledge for Testing Layer modeling in Documentation Robotics
triggers:
  [
    "testing",
    "test coverage",
    "test case",
    "input partition",
    "ISP",
    "test strategy",
    "coverage model",
  ]
version: 0.7.0
---

# Testing Layer Skill

**Layer Number:** 12
**Specification:** Metadata Model Spec v0.7.0
**Purpose:** Defines test coverage using ISP (Input Space Partitioning) Coverage Model, specifying coverage requirements, test cases, and input partitions.

---

## Layer Overview

The Testing Layer captures **test coverage strategy**:

- **COVERAGE MODELS** - Overall test coverage requirements
- **COVERAGE TARGETS** - What needs testing (APIs, features, data)
- **INPUT PARTITIONS** - Partition input space for systematic coverage
- **TEST CASES** - Concrete test case sketches
- **CONTEXT VARIATIONS** - Environmental and contextual variations
- **COVERAGE GAPS** - Identified gaps in coverage

This layer uses **ISP Coverage Model** (systematic input space partitioning).

**Central Entity:** The **TestCoverageModel** is the core modeling unit.

---

## Entity Types

### Core Testing Entities (17 entities)

| Entity Type                 | Description                              |
| --------------------------- | ---------------------------------------- |
| **TestCoverageModel**       | Root coverage model for system/component |
| **TestCoverageTarget**      | What needs testing (API, feature, data)  |
| **InputSpacePartition**     | Partition of input space                 |
| **PartitionValue**          | Value/range within partition             |
| **InputPartitionSelection** | Selected partition values for coverage   |
| **CoverageRequirement**     | Specific coverage requirement            |
| **TestCaseSketch**          | High-level test case description         |
| **OutcomeCategory**         | Expected outcome categories              |
| **ContextVariation**        | Environmental/contextual variation       |
| **EnvironmentFactor**       | Environment-specific factor              |
| **PartitionDependency**     | Dependencies between partitions          |
| **CoverageGap**             | Identified gap in coverage               |
| **CoverageExclusion**       | Explicitly excluded coverage             |
| **CoverageSummary**         | Summary of coverage status               |
| **TargetCoverageSummary**   | Coverage summary for target              |
| **TargetInputField**        | Input field for target                   |

---

## When to Use This Skill

Activate when the user:

- Mentions "testing", "test coverage", "test cases", "ISP"
- Wants to define test strategy or coverage requirements
- Asks about input partitioning or systematic testing
- Needs to model test cases for APIs, features, or data
- Wants to link testing to requirements or business goals

---

## Cross-Layer Relationships

**Outgoing (Testing → Other Layers):**

- `motivation.supports-goals` → Motivation Layer (quality goals)
- `motivation.fulfills-requirements` → Motivation Layer (test requirements)
- `business.covers-process` → Business Layer (process coverage)
- `api.tests-operation` → API Layer (API endpoint testing)
- `data.validates-schema` → Data Model Layer (data validation)
- `ux.tests-view` → UX Layer (UI testing)

**Incoming (Other Layers → Testing):**

- Motivation Layer → Testing (requirements drive coverage)
- API Layer → Testing (operations need test coverage)
- Business Layer → Testing (processes need testing)

---

## Testing Best Practices

1. **Systematic partitioning** - Use ISP to partition input space
2. **Coverage criteria** - Define clear coverage criteria
3. **Context variations** - Test across different contexts
4. **Traceability** - Link tests to requirements and features
5. **Gap analysis** - Identify and document coverage gaps
6. **Exclusions** - Explicitly document what's not tested
7. **Outcome categories** - Define expected outcomes clearly

---

## Common Commands

```bash
# Add coverage model
dr add testing test-coverage-model --name "API Coverage Model"

# Add coverage target
dr add testing test-coverage-target --name "Login API Coverage"

# Add test case sketch
dr add testing test-case-sketch --name "Valid Login Test"

# List coverage models
dr list testing test-coverage-model

# Validate testing layer
dr validate --layer testing

# Export coverage report
dr export --layer testing --format markdown
```

---

## Example: Login API Coverage Model

```yaml
id: testing.coverage-model.login-api
name: "Login API Coverage Model"
type: test-coverage-model
properties:
  targets:
    - testing.target.login-endpoint
  coverageCriteria: each-choice
  contextVariations:
    - browser: [Chrome, Firefox, Safari]
    - network: [high-speed, low-speed, offline]
    - device: [desktop, mobile, tablet]
  motivation:
    supports-goals:
      - motivation.goal.quality-assurance
    fulfills-requirements:
      - motivation.requirement.comprehensive-testing
```

---

## Example: Login Test Coverage Target

```yaml
id: testing.target.login-endpoint
name: "Login Endpoint Coverage"
type: test-coverage-target
properties:
  targetRef: api.operation.login
  inputFields:
    - name: email
      partitions:
        - valid-email: [user@example.com]
        - invalid-format: [notanemail, @example.com]
        - missing: [null, empty]
    - name: password
      partitions:
        - valid-password: [StrongPass123!]
        - weak-password: [123, abc]
        - missing: [null, empty]
        - too-long: [1000-char-string]
  outcomeCategories:
    - success: 200 OK with auth token
    - invalid-credentials: 401 Unauthorized
    - validation-error: 400 Bad Request
    - rate-limited: 429 Too Many Requests
  testCases:
    - testing.test-case.valid-login
    - testing.test-case.invalid-email
    - testing.test-case.invalid-password
    - testing.test-case.missing-credentials
```

---

## Example: Test Case Sketch

```yaml
id: testing.test-case.valid-login
name: "Valid Login Test Case"
type: test-case-sketch
properties:
  target: testing.target.login-endpoint
  description: "Test successful login with valid credentials"
  inputSelection:
    email: valid-email
    password: valid-password
  contextSelection:
    browser: Chrome
    network: high-speed
    device: desktop
  expectedOutcome: success
  expectedResponse:
    status: 200
    body:
      token: JWT token present
      user: User object with id and email
  motivation:
    supports-goals:
      - motivation.goal.secure-authentication
```

---

## Pitfalls to Avoid

- ❌ Ad-hoc testing without systematic partitioning
- ❌ Missing context variations (only testing happy path)
- ❌ Not documenting coverage gaps
- ❌ No traceability to requirements
- ❌ Missing cross-layer links to tested elements
- ❌ Incomplete outcome categories
