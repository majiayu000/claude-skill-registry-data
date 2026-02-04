---
name: code-scoring
description: Provides quantitative rubrics and criteria for scoring code quality on a 1-10 scale. Use when reviewing code, performing code audits, establishing quality baselines, comparing implementations, or providing objective code feedback.
---

# Code Scoring

Systematic, quantitative code quality assessment using weighted categories and standardized deductions.

## Quick Start

**Full code review with score:**
```
Score this code on a 1-10 scale using the code-scoring rubric
```

**Category-specific assessment:**
```
Evaluate the error handling in this module using the scoring rubric
```

**Compare implementations:**
```
Score both implementations and recommend which is better
```

## Scoring Methodology

### The Formula

```
Final Score = 10 - Total Deductions

Where:
Total Deductions = SUM(Category Deductions * Category Weight)
Category Deduction = SUM(Issue Points * Severity Multiplier)
```

### Category Weights

| Category | Weight | Focus Areas |
|----------|--------|-------------|
| **Organization** | 12% | File structure, module boundaries, separation of concerns |
| **Naming** | 10% | Variables, functions, classes, constants, files |
| **Error Handling** | 12% | Try/catch, validation, error propagation, recovery |
| **Testing** | 12% | Coverage, quality, edge cases, maintainability |
| **Performance** | 10% | Efficiency, resource usage, scalability |
| **Security** | 12% | Input validation, auth, data protection, secrets |
| **Documentation** | 8% | Comments, API docs, README, inline explanations |
| **SOLID Principles** | 10% | SRP, OCP, LSP, ISP, DIP adherence |
| **Dependencies** | 6% | Version management, minimal deps, no circular refs |
| **Maintainability** | 8% | Readability, complexity, changeability |

**Total: 100%**

### Severity Multipliers

| Severity | Multiplier | Description |
|----------|------------|-------------|
| **Critical** | 2.0x | Security vulnerabilities, data loss risks, crashes |
| **Major** | 1.5x | Significant bugs, poor patterns, missing core functionality |
| **Minor** | 1.0x | Code smells, style issues, minor inefficiencies |
| **Nitpick** | 0.5x | Preferences, optional improvements |

---

## Quick Scoring Cheat Sheet

| Score | Label | Meaning | Typical Characteristics |
|-------|-------|---------|-------------------------|
| **10** | Exemplary | Production excellence | Minimal issues, well-tested, secure, documented |
| **9** | Excellent | Minor polish needed | 1-2 nitpicks, strong overall quality |
| **8** | Very Good | Ready with small fixes | Few minor issues, solid fundamentals |
| **7** | Good | Acceptable quality | Some improvements needed, no major issues |
| **6** | Satisfactory | Functional but rough | Multiple minor issues, needs cleanup |
| **5** | Adequate | Meets minimum bar | Works but has clear problems |
| **4** | Below Average | Needs significant work | Major issues present, risky to deploy |
| **3** | Poor | Substantial rework | Multiple major issues, architectural problems |
| **2** | Very Poor | Fundamental problems | Barely functional, serious concerns |
| **1** | Critical | Do not deploy | Security vulnerabilities, crashes, data risks |

---

## Common Deductions Table

Quick reference for frequent issues. See [references/deduction-catalog.md](references/deduction-catalog.md) for complete list.

### High-Impact Deductions

| Issue | Base Points | Category |
|-------|-------------|----------|
| SQL injection vulnerability | 2.0 | Security |
| Hardcoded secrets/credentials | 2.0 | Security |
| No error handling in critical path | 1.5 | Error Handling |
| Missing input validation | 1.5 | Security |
| No tests for core functionality | 1.5 | Testing |
| N+1 query pattern | 1.5 | Performance |
| God class (500+ lines) | 1.5 | Organization |

### Medium-Impact Deductions

| Issue | Base Points | Category |
|-------|-------------|----------|
| Inconsistent naming convention | 1.0 | Naming |
| Missing JSDoc/docstrings on public API | 1.0 | Documentation |
| Circular dependency | 1.0 | Dependencies |
| Deeply nested code (4+ levels) | 1.0 | Maintainability |
| Magic numbers without constants | 1.0 | Naming |
| Empty catch blocks | 1.0 | Error Handling |
| Duplicated code blocks | 1.0 | Organization |

### Low-Impact Deductions

| Issue | Base Points | Category |
|-------|-------------|----------|
| Inconsistent formatting | 0.5 | Maintainability |
| Missing edge case tests | 0.5 | Testing |
| Verbose variable names | 0.5 | Naming |
| Outdated dependencies (no CVEs) | 0.5 | Dependencies |
| Missing inline comments in complex logic | 0.5 | Documentation |

---

## Scoring Workflow

### Step 1: Initial Scan

```
1. Count lines of code
2. Identify file/module structure
3. Note language and framework
4. Check for tests presence
5. Scan for obvious red flags
```

### Step 2: Category Assessment

For each of the 10 categories:

```
1. Review relevant code sections
2. Identify issues
3. Classify severity (critical/major/minor/nitpick)
4. Calculate: Issues * Severity Multiplier
5. Apply category weight
```

### Step 3: Calculate Final Score

```
Final Score = 10 - (Sum of weighted deductions)

If score < 1: score = 1
If score > 10: score = 10
```

### Step 4: Generate Report

```markdown
## Code Score: X.X/10

### Score Breakdown
| Category | Weight | Deductions | Weighted |
|----------|--------|------------|----------|
| Organization | 12% | ... | ... |
| ... | ... | ... | ... |

### Critical Issues (Fix Immediately)
- [Issue 1]

### Major Issues (Fix Before Merge)
- [Issue 1]

### Minor Issues (Fix When Convenient)
- [Issue 1]

### Recommendations
- [Improvement 1]
```

---

## Category Quick Guides

### Organization (12%)

**Excellent (0 deductions):**
- Clear module boundaries
- Single responsibility per file
- Logical folder structure
- No circular dependencies

**Red flags:**
- Files > 500 lines: -1.0
- Mixed concerns in module: -1.0
- No clear structure: -1.5
- Circular dependencies: -1.0

### Naming (10%)

**Excellent (0 deductions):**
- Descriptive, intention-revealing names
- Consistent convention (camelCase, snake_case)
- Domain terminology used correctly
- Acronyms handled consistently

**Red flags:**
- Single-letter variables (non-loop): -0.5
- Misleading names: -1.0
- Inconsistent convention: -1.0
- Magic numbers: -1.0

### Error Handling (12%)

**Excellent (0 deductions):**
- All external calls wrapped
- Specific error types used
- Errors logged with context
- Graceful degradation where appropriate

**Red flags:**
- Empty catch blocks: -1.0
- Generic catch-all: -0.5
- Missing validation: -1.5
- Swallowed errors: -1.0

### Testing (12%)

**Excellent (0 deductions):**
- 80%+ coverage on critical paths
- Unit, integration, and E2E tests
- Edge cases covered
- Tests are maintainable

**Red flags:**
- No tests: -2.0
- Only happy path: -1.0
- Flaky tests: -1.0
- Test code duplication: -0.5

### Performance (10%)

**Excellent (0 deductions):**
- Efficient algorithms
- Appropriate caching
- No memory leaks
- Optimized queries

**Red flags:**
- N+1 queries: -1.5
- Blocking operations in hot path: -1.0
- Memory leaks: -1.5
- No pagination on lists: -1.0

### Security (12%)

**Excellent (0 deductions):**
- Input validation on all boundaries
- Parameterized queries
- Secrets in environment variables
- Proper authentication/authorization

**Red flags:**
- SQL/command injection: -2.0
- Hardcoded secrets: -2.0
- Missing auth checks: -1.5
- XSS vulnerabilities: -1.5

### Documentation (8%)

**Excellent (0 deductions):**
- Public API documented
- Complex logic explained
- README with setup instructions
- Changelog maintained

**Red flags:**
- No documentation: -1.5
- Outdated docs: -1.0
- Missing API docs: -1.0
- No README: -0.5

### SOLID Principles (10%)

**Excellent (0 deductions):**
- Single responsibility classes
- Open for extension, closed for modification
- Proper abstractions
- Dependency injection used

**Red flags:**
- God classes: -1.5
- Tight coupling: -1.0
- Violation of LSP: -1.0
- Concrete dependencies: -0.5

### Dependencies (6%)

**Excellent (0 deductions):**
- Minimal dependencies
- Locked versions
- No vulnerabilities
- Clear dependency boundaries

**Red flags:**
- CVE vulnerabilities: -2.0
- Circular dependencies: -1.0
- Excessive dependencies: -0.5
- Unlocked versions: -0.5

### Maintainability (8%)

**Excellent (0 deductions):**
- Low cyclomatic complexity
- DRY principle followed
- Consistent style
- Easy to understand

**Red flags:**
- Cyclomatic complexity > 15: -1.0
- Duplicated code: -1.0
- Deep nesting (4+): -1.0
- Inconsistent style: -0.5

---

## Score Interpretation Guide

### Deployment Readiness

| Score Range | Deployment Decision |
|-------------|---------------------|
| 8-10 | Ready for production |
| 7-7.9 | Ready with minor fixes |
| 5-6.9 | Needs review and fixes |
| 3-4.9 | Significant rework required |
| 1-2.9 | Do not deploy |

### Review Actions

| Score Range | Required Actions |
|-------------|------------------|
| 9-10 | Approve immediately |
| 7-8.9 | Approve with suggestions |
| 5-6.9 | Request changes |
| 3-4.9 | Major revision needed |
| 1-2.9 | Reject with detailed feedback |

---

## Reference Files

- [references/scoring-rubrics.md](references/scoring-rubrics.md) - Detailed rubric for each category
- [references/severity-weights.md](references/severity-weights.md) - How to weight different issue types
- [references/score-descriptors.md](references/score-descriptors.md) - What each score 1-10 means with examples
- [references/deduction-catalog.md](references/deduction-catalog.md) - Common issues and their point deductions
