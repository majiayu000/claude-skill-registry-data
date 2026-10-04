---
name: testing:test-coverage
description: |
  Analyze and expand test coverage using intelligent prioritization.
  Use when checking coverage status, finding testing opportunities, or expanding coverage systematically.
disable-model-invocation: false
allowed-tools: Bash Read Grep Glob
---

# Test Coverage Management

Track and expand test coverage systematically.

## Usage

- `/testing:test-coverage status` - Current coverage metrics
- `/testing:test-coverage opportunities` - Find high-impact files
- `/testing:test-coverage expand [area]` - Expand specific area

## Priority Matrix

**High Priority (Zero Coverage)**
- Core business logic files
- Utility functions
- Data stores

**Medium Priority (Partial Coverage)**
- Modules with < 50% coverage

**Lower Priority**
- Well-covered files needing edge cases

## Workflow

1. Run coverage report to identify targets
2. Pick 2-3 high-priority files
3. Create tests using appropriate patterns (see `testing:unit-tests` skill)
4. Verify coverage improvement
5. Repeat

## Reports

```bash
# HTML report
<test-coverage-command> --reporter=html

# JSON data
<test-coverage-command> --reporter=json

# Summary only
<test-coverage-command> --reporter=text-summary
```

## Expansion Process

1. Identify files with zero or low coverage
2. Prioritize by: business impact, change frequency, complexity
3. Create tests covering: happy path, edge cases, error conditions
4. Verify improvement
5. Track progress over time
