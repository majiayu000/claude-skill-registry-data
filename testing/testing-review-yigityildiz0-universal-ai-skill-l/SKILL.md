---
name: testing-review
description: Assess test coverage, test quality, testing strategy effectiveness, and identify coverage gaps. Use when evaluating test suites, improving test strategy.
---

# Code Review - Testing Review

Evaluate test coverage, quality, and effectiveness. This skill is **Phase 5** of the 6-phase code review methodology.

## When to Use This Skill

Use this skill when you need to:

- Evaluate test suite quality
- Identify coverage gaps
- Assess testing strategy
- Review test maintainability
- Prepare for releases
- Improve test effectiveness

**Trigger phrases**: "testing review", "test coverage", "test quality", "test assessment", "coverage gaps", "test strategy"

## What This Skill Does

### Assessment Areas

| Area | Focus |
|------|-------|
| **Coverage** | Line, branch, function coverage |
| **Quality** | Test clarity, maintainability |
| **Strategy** | Unit, integration, E2E balance |
| **Effectiveness** | Real bug detection ability |
| **Performance** | Test execution time |

### Coverage Targets

- **Line Coverage**: 80%+
- **Branch Coverage**: 75%+
- **Function Coverage**: 90%+
- **Critical Paths**: 95%+

### Severity Classification

| Level | Alias | Description |
|-------|-------|-------------|
| **P0** | CRITICAL | Critical paths completely untested |
| **P1** | HIGH | Significant coverage gaps in important code |
| **P2** | MEDIUM | Test quality issues or moderate gaps |
| **P3** | LOW | Minor test improvements |

## Instructions

### Step 1: Measure Coverage

```bash
# Python
pytest --cov=src --cov-report=html

# JavaScript
npm test -- --coverage

# Java
mvn jacoco:report

# Go
go test -coverprofile=coverage.out ./...

# C# / .NET
dotnet test --collect:"XPlat Code Coverage"
```

### Step 2: Analyze Test Quality

1. **Test Structure**
   - Clear AAA pattern (Arrange-Act-Assert)
   - Descriptive names
   - Single responsibility

2. **Test Isolation**
   - No shared state
   - Independent execution
   - Proper mocking

3. **Test Types Balance**
   - Unit tests (70%)
   - Integration tests (20%)
   - E2E tests (10%)

### Step 3: Identify Gaps

Check for missing tests in:
- Error handling paths
- Edge cases and boundary conditions
- Critical business logic
- Security-sensitive code
- Recently changed code (in git-changes mode)

### Step 4: Document Findings

```markdown
## Testing Review Finding

**Category**: Coverage Gap
**Severity**: P1 (HIGH)
**File**: [src/services/payment.py]

### Issue
Payment processing has 45% coverage, critical path untested

### Missing Tests
- [ ] Failed payment handling
- [ ] Partial refund logic
- [ ] Currency conversion edge cases

### Recommendation
Add tests for error scenarios and edge cases

### Priority
Immediate (before next release)
```

## Test Quality Indicators

### Good Tests
- Clear, descriptive names
- Single assertion focus
- Fast execution (<100ms)
- No flaky behavior
- Proper isolation

### Bad Tests (Anti-patterns)
- Multiple unrelated assertions
- Testing implementation details
- Slow execution
- Shared mutable state
- No assertions (always pass)

## Quality Checklist

- [ ] Coverage metrics collected
- [ ] Coverage gaps identified
- [ ] Test quality assessed (AAA pattern, naming, isolation)
- [ ] Anti-patterns detected
- [ ] Test type balance evaluated (70/20/10)
- [ ] Test performance reviewed
- [ ] Critical path coverage verified (95%+ target)
- [ ] Recommendations documented with severity (P0-P3)

## Related Skills

- `context-analysis` - Context understanding (Phase 1)
- `code-quality` - Code quality + SOLID review (Phase 2)
- `security-review` - Security analysis (Phase 3)
- `performance-review` - Performance analysis (Phase 4)
- `unit-tests` - Unit test generation
- `code-coverage` - Coverage improvement
- `final-report` - Consolidated report (Phase 6)

---

**Version**: 2.0.0
**Last Updated**: February 2026
**Based on**: DevAI-Hub code review methodology + code-review-expert


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
