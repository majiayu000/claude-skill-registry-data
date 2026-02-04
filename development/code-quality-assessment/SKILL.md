---
name: code-quality-assessment
description: Activate when analyzing code quality through linting, formatting, testing, coverage analysis, and maintainability metrics
license: MIT
---

# Code Quality Assessment

Guide for comprehensive code quality analysis through automated linting, formatting verification, test execution, coverage analysis, and maintainability assessment.

## When to Use This Skill

Activate when:
- Running code quality checks across a codebase
- Analyzing test coverage and identifying gaps
- Measuring code complexity and maintainability
- Enforcing coding standards and style guides
- Generating quality reports for CI/CD pipelines
- Assessing technical debt and prioritizing improvements

## Quality Assessment Process

### Phase 1: Tool Discovery
1. Analyze project structure for technology stack
2. Detect configuration files (eslint, prettier, pytest, etc.)
3. Identify available quality tools
4. Plan execution order and dependencies

### Phase 2: Linting and Static Analysis
1. Execute available linting tools
2. Parse output for errors, warnings, style violations
3. Categorize issues by severity
4. Identify patterns in violations
5. Generate recommendations

### Phase 3: Code Formatting
1. Run formatting tools
2. Identify inconsistencies
3. Assess auto-fix impact
4. Generate formatting reports

### Phase 4: Test Suite and Coverage
1. Execute test suites (unit, integration, e2e)
2. Analyze results for failures and performance
3. Generate coverage reports:
   - Line coverage
   - Branch coverage
   - Function coverage
   - Statement coverage
4. Identify coverage gaps
5. Prioritize missing test scenarios

### Phase 5: Complexity Analysis
1. Calculate cyclomatic complexity
2. Identify functions exceeding thresholds
3. Assess maintainability metrics
4. Calculate technical debt estimates
5. Detect code duplication

## Tool Detection by Project Type

### JavaScript/TypeScript
- Linting: ESLint, TSLint
- Formatting: Prettier
- Testing: Jest, Vitest, Mocha
- Complexity: plato, jscpd

### Python
- Linting: pylint, flake8, ruff
- Formatting: Black, isort
- Testing: pytest
- Complexity: radon, mccabe

### Rust
- Linting: clippy
- Formatting: rustfmt
- Testing: cargo test
- Coverage: tarpaulin, llvm-cov

### Elixir
- Linting: credo
- Static Analysis: dialyzer
- Formatting: mix format
- Testing: ExUnit
- Security: sobelow

### Go
- Linting: golint, staticcheck
- Formatting: gofmt
- Testing: go test
- Complexity: gocyclo

## Quality Report Structure

```markdown
# Code Quality Assessment Report

**Project**: [Name]
**Date**: [Date]
**Overall Score**: [Score/Grade]

## Executive Summary
- **Critical Issues**: [Number]
- **Test Coverage**: [Percentage]%
- **Quality Gate**: [Pass/Fail]

## Linting Results
### Critical Issues (Errors)
- [Issue with file:line]
- [Recommended fix]

### Warnings
- [Warning description]
- [Severity assessment]

## Test Results
### Execution Summary
- **Total Tests**: [Number]
- **Passed**: [Number] ([%])
- **Failed**: [Number] ([%])

### Coverage Analysis
- **Overall**: [%]%
- **Line**: [%]%
- **Branch**: [%]%
- **Function**: [%]%

### Critical Coverage Gaps
- [Uncovered critical functionality]
- [Security-sensitive code without tests]

## Complexity Metrics
### Cyclomatic Complexity
- **Average**: [X]
- **Max**: [Y]
- **Functions >10**: [Number]

### Maintainability
- **Index**: [Score]/100
- **Duplication**: [%]%
- **Technical Debt**: [Hours]

## Action Items
### Critical (Immediate)
1. [Fix with instructions]

### High Priority (This Sprint)
1. [Improvement]

### Medium Priority (Next Sprint)
1. [Enhancement]

## Quality Gate Status
- [ ] Linting: Passed
- [ ] Coverage: >80%
- [ ] Security: Passed
```

## Complexity Thresholds

- **Simple (1-5)**: Acceptable complexity
- **Moderate (6-10)**: Monitor for growth
- **Complex (11-20)**: Consider refactoring
- **Very Complex (>20)**: Refactor required

## Key Principles

- **Tool-Agnostic**: Detect and use available tools
- **Actionable Results**: Provide specific recommendations
- **Prioritized Output**: Organize by criticality
- **Context-Aware**: Consider project type and stage
- **Trend Analysis**: Compare against baselines
- **CI/CD Ready**: Generate machine-readable outputs
