---
name: test-strategy
description: Define a test strategy for a feature, sprint, or release. Apply the test pyramid to balance unit, integration, and E2E tests. Use risk-based testing to focus effort where failures would hurt most. Produce a coverage plan that aligns with team capacity and release timelines.
triggers:
  - "test strategy"
  - "test plan"
  - "test coverage"
  - "what to test"
  - "testing approach"
  - "how much testing"
  - "risk based testing"
  - "test pyramid"
audience:
  - qa
  - engineer
  - manager
---

# Test Strategy

Define *what* to test, *how much*, and *at which layer* — before writing a single test.

---

## The Test Pyramid

Balance test types by speed, cost, and confidence:

```
        ▲  E2E / UI Tests
       ▲▲▲   (slow, expensive, high confidence on user journeys)
      ▲▲▲▲▲  Integration Tests
     ▲▲▲▲▲▲▲  (medium speed, catch contract and wiring bugs)
    ▲▲▲▲▲▲▲▲▲ Unit Tests
   ▲▲▲▲▲▲▲▲▲▲▲ (fast, cheap, catch logic bugs)
```

### Healthy ratios (guidance, not rules)
| Layer | Proportion | What it covers |
|---|---|---|
| Unit | 60-70% | Business logic, algorithms, edge cases, error handling |
| Integration | 20-30% | DB queries, API calls, service wiring, message queues |
| E2E / UI | 5-10% | Critical user journeys only — not every feature |
| Manual / Exploratory | As needed | New features, complex UX, high-risk areas |

**Anti-pattern — Inverted pyramid**: E2E tests for everything. Slow, brittle, expensive to maintain.

---

## Risk-Based Testing

Allocate testing effort proportional to failure impact × likelihood. Don't test everything equally.

### Risk Matrix
```
         │ Low Impact  │ High Impact
─────────┼─────────────┼─────────────
Low      │ Minimal     │ Basic coverage
Likelihood│ coverage   │ + happy path
─────────┼─────────────┼─────────────
High     │ Happy path  │ FULL coverage:
Likelihood│ + error    │ happy + error +
         │ cases       │ edge + regression
```

### Risk Factors to Score
For each feature or component:
- **Business impact**: Revenue, compliance, user data, reputation (1-5)
- **Technical complexity**: New code, untested paths, external dependencies (1-5)
- **Change frequency**: How often does this area change? (1-5)
- **Historical failures**: Has this broken before? (1-5)

`Risk Score = (Business Impact + Technical Complexity) × Change Frequency`

High-scoring areas get E2E + integration + unit. Low-scoring areas may get unit only.

---

## Test Strategy Document

```markdown
## Test Strategy: [Feature / Release Name]

**Author**: [QA name]
**Date**: [date]
**Scope**: [what's being tested — feature, sprint, release]

---

### Risk Assessment

| Component | Business Impact | Complexity | Change Freq | Risk Score | Test Focus |
|---|---|---|---|---|---|
| [component] | 1-5 | 1-5 | 1-5 | [calc] | Unit/Int/E2E |

---

### Test Coverage Plan

#### Unit Tests
- [ ] [Business logic: what conditions/paths to cover]
- [ ] [Error handling: expected failures]
- [ ] [Boundary values: min, max, empty, null]

#### Integration Tests
- [ ] [API contracts: request/response shapes]
- [ ] [Database: read/write/transaction correctness]
- [ ] [External services: stub/mock boundaries]

#### E2E Tests
- [ ] [Critical user journey 1: happy path]
- [ ] [Critical user journey 2: with error recovery]
- [Limit to 3-5 journeys maximum]

#### Manual / Exploratory
- [ ] [Area: why manual is better here]
- [ ] [Session charter: what to investigate]

---

### What We Are NOT Testing
[Explicitly list what's out of scope and why — this is as important as what's in scope]

---

### Test Environment Requirements
- [ ] Test data seeded for [scenarios]
- [ ] Feature flags configured for [state]
- [ ] External service stubs/mocks available
- [ ] CI pipeline can run full suite in < [target time]

---

### Exit Criteria (Definition of Done for Testing)
- [ ] All planned unit and integration tests passing in CI
- [ ] Zero P0/P1 bugs open
- [ ] P2 bugs triaged and accepted by PM
- [ ] E2E tests passing on staging
- [ ] Exploratory testing session completed; findings logged
```

---

## Per-Layer Test Design

### Unit Test Heuristics
- Test behavior, not implementation — if you have to change tests when refactoring internals, your tests are too coupled
- Each test: one concept, one assertion (or a small set of related assertions)
- Name tests as documentation: `should_return_empty_list_when_no_orders_found`
- Cover: happy path, null/empty input, boundary values, error cases

### Integration Test Heuristics
- Test at the seam: test the full stack from the interface to the DB (or mock external dependencies at the network layer)
- Use a real test database — avoid mocking the ORM
- Cover: correct data persisted, correct data returned, constraint violations, concurrency (if relevant)

### E2E Test Heuristics
- Only test critical user journeys — flows a broken version would instantly fail
- Stable selectors: use data-testid attributes, not CSS classes or text
- Idempotent: each test cleans up after itself
- Flakiness = delete or fix immediately; flaky E2E tests destroy trust

---

## Test Strategy for AI / LLM Features

AI features need additional test layers. See `agent-quality-patterns` skill for full detail.

Quick additions to standard strategy:
- **Golden dataset**: 20-50 curated input/output pairs covering happy path + edge cases
- **LLM-as-judge**: Rubric scoring for output quality, not just "did it run"
- **Regression evals**: Run against golden dataset in CI on every prompt change
- **Hallucination tests**: Inputs designed to surface false confident answers

---

## MCP Integration

### Jira MCP
Pull stories and acceptance criteria to inform test scope:
```
# Get all stories in current sprint
jira_search_issues: project = [KEY] AND sprint in openSprints() AND issuetype = Story

# Get story details for test planning
jira_get_issue: [ISSUE-KEY]  → read description, acceptance criteria, linked bugs

# Create test coverage task
jira_create_issue: {
  project: [KEY], issuetype: "Task",
  summary: "Test coverage: [feature]",
  description: [test strategy doc],
  parent: [story key]
}
```

### Confluence MCP
Publish the test strategy doc and link it to the relevant space:
```
# Create test strategy page in QA space
confluence_create_page: {
  space: "QA",
  title: "Test Strategy — [Feature/Sprint]",
  content: [test strategy markdown],
  parent_page: "Test Plans"
}

# Search for existing test plans to avoid duplication
confluence_search: "Test Strategy [feature name] space:QA"
```

---

## References
- Mike Cohn: [Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html) (via Fowler)
- Martin Fowler: [Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- James Bach: [Risk-Based Testing](https://www.satisfice.com/articles/rst.pdf)
- Google Testing Blog: [Just Say No to More End-to-End Tests](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html)
