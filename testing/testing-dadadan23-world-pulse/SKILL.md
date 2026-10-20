---
name: "testing"
description: 'Apply testing strategies including test pyramid, unit/integration/e2e testing, and coverage requirements. Use when writing unit tests, designing integration test suites, implementing end-to-end tests, measuring test coverage, or setting up continuous testing pipelines.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# Testing

> **Purpose**: Language-agnostic testing strategies ensuring code quality and reliability. 
> **Goal**: 80%+ coverage with 70% unit, 20% integration, 10% e2e tests. 
> **Note**: For language-specific examples, see [C# Development](../csharp/SKILL.md) or [Python Development](../python/SKILL.md).

---

## When to Use This Skill

- Writing unit tests for new code
- Designing integration test suites
- Implementing end-to-end test automation
- Measuring and improving test coverage
- Setting up continuous testing in CI/CD pipelines

## Prerequisites

- Testing framework installed (pytest, Jest, xUnit, etc.)
- CI/CD pipeline for automated test execution

## Decision Tree

```
Writing or reviewing tests?
+- New feature/story?
| +- Has acceptance criteria? -> Write e2e test first, then unit tests
| - No criteria? -> Write unit tests for public API surface
+- Bug fix?
| - Write regression test FIRST (red), then fix (green)
+- Refactoring?
| - Ensure existing tests pass -> refactor -> verify green
+- What type of test?
| +- Pure logic, no I/O? -> Unit test (70% of total)
| +- Database/API/file I/O? -> Integration test (20%)
| - Full user workflow? -> E2E test (10%)
- Coverage below 80%?
 - Run: scripts/check-coverage.ps1 -> add tests for uncovered paths
```

## Test Pyramid

```
 /\
 /E2E\ 10% - Few (expensive, slow, brittle)
 /------\
 / Intg \ 20% - More (moderate cost/speed)
 /----------\
 / Unit \ 70% - Many (cheap, fast, reliable)
 /--------------\
```

**Why**: Unit tests catch bugs early, run fast, provide precise feedback. E2E tests validate workflows but are slow and flaky.

---

## Test Coverage

### Coverage Metrics

```
Coverage Types:
 - Line Coverage: % of code lines executed
 - Branch Coverage: % of if/else branches taken
 - Function Coverage: % of functions called
 - Statement Coverage: % of statements executed

Target: 80%+ overall coverage
```

**Coverage Tools by Language:**
- **.NET**: Coverlet, dotCover
- **Python**: coverage.py, pytest-cov
- **Node.js**: Istanbul (nyc), Jest
- **Java**: JaCoCo, Cobertura
- **PHP**: PHPUnit --coverage

### What to Test

**[PASS] Always Test:**
- Business logic and algorithms
- Data transformations
- Validation rules
- Error handling paths
- Edge cases and boundary conditions
- Security-critical code

**[FAIL] Don't Test:**
- Third-party library internals
- Framework code
- Simple getters/setters (unless logic involved)
- Configuration files
- Auto-generated code

---

## Testing Best Practices

### Write Testable Code

**Testable Code Characteristics:**
```
[PASS] Single Responsibility Principle
[PASS] Dependency Injection
[PASS] Pure Functions (no side effects)
[PASS] Small, focused methods
[PASS] Minimal global state
[PASS] Clear interfaces

[FAIL] Tightly coupled code
[FAIL] Hidden dependencies
[FAIL] God classes
[FAIL] Hard-coded dependencies
[FAIL] Static methods everywhere
```

### Test Fixtures

**Setup and Teardown:**
```
class UserServiceTests:
 # Run once before all tests
 beforeAll():
 testDatabase.connect()
 
 # Run before each test
 beforeEach():
 testDatabase.clear()
 seedTestData()
 
 # Run after each test
 afterEach():
 testDatabase.clear()
 
 # Run once after all tests
 afterAll():
 testDatabase.disconnect()
 
 test "getUser returns correct user":
 # Test uses clean database state
 user = service.getUser(1)
 assert user.name == "Test User"
```

### Parameterized Tests

**Data-Driven Testing:**
```
testCases = [
 {input: 0, expected: 0},
 {input: 1, expected: 1},
 {input: -1, expected: -1},
 {input: 100, expected: 100}
]

for each testCase in testCases:
 test "abs({testCase.input}) returns {testCase.expected}":
 result = abs(testCase.input)
 assert result == testCase.expected
```

---

## Testing Frameworks

**Unit Testing:**
- **.NET**: xUnit, NUnit, MSTest
- **Python**: pytest, unittest
- **Node.js**: Jest, Mocha, Vitest
- **Java**: JUnit, TestNG
- **PHP**: PHPUnit

**Integration Testing:**
- **API Testing**: REST Assured, Supertest, Postman/Newman
- **Database Testing**: Testcontainers, DbUnit

**E2E Testing:**
- **Browser**: Playwright, Cypress, Selenium, Puppeteer
- **Mobile**: Appium, Detox

---

## Resources

**Testing Guides:**
- [Test Pyramid - Martin Fowler](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Testing Best Practices](https://testingjavascript.com)
- [Google Testing Blog](https://testing.googleblog.com)

**Books:**
- "xUnit Test Patterns" by Gerard Meszaros
- "The Art of Unit Testing" by Roy Osherove
- "Growing Object-Oriented Software, Guided by Tests" by Steve Freeman

---

**See Also**: [Skills.md](../../../../Skills.md) - [AGENTS.md](../../../../AGENTS.md)

**Last Updated**: January 27, 2026

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [`check-coverage.ps1`](scripts/check-coverage.ps1) | Check test coverage against threshold (80% default) | `./scripts/check-coverage.ps1 [-Threshold 90]` |
| [`check-coverage.sh`](scripts/check-coverage.sh) | Cross-platform coverage checker (bash) | `./scripts/check-coverage.sh --threshold 80` |
| [`check-test-pyramid.ps1`](scripts/check-test-pyramid.ps1) | Verify test distribution matches pyramid ratios | `./scripts/check-test-pyramid.ps1` |
| [`scaffold-playwright.py`](scripts/scaffold-playwright.py) | Generate Playwright e2e test scaffold (TS or Python) | `python scripts/scaffold-playwright.py --lang typescript --url http://localhost:3000` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Flaky tests in CI | Remove timing dependencies, use deterministic test data, add retries for known flaky tests |
| Low coverage despite many tests | Focus on branch coverage not just line coverage, test edge cases |
| Integration tests too slow | Use test containers, parallelize test suites, mock external services |

## References

- [Test Type Examples](references/test-type-examples.md)
- [Test Org Ci Pitfalls](references/test-org-ci-pitfalls.md)