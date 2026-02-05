---
name: review-scoring-rubric
description: Provides the complete code review scoring rubric with 10 weighted categories, severity multipliers, and deduction calculations. Use when performing quantified code reviews, calculating quality scores, or creating improvement roadmaps.
---

# Review Scoring Rubric

Complete scoring system for quantified code reviews with weighted categories and severity-based deductions.

## Quick Start

**Calculate score:**
```
Calculate a score for this codebase using the 10-category weighted rubric.
```

**Specific category audit:**
```
Analyze the Testing category and calculate its weighted contribution to the score.
```

## The Formula

```
Final Score = 10 - Total Weighted Deductions

Where:
Total Weighted Deductions = SUM(Category Deduction * Category Weight)
Category Deduction = SUM(Issue Points * Severity Multiplier)
```

**Maximum Deduction per Category:** 10 points (caps at 0 for category)

---

## Severity Multipliers

| Severity | Multiplier | Description | Example Issues |
|----------|------------|-------------|----------------|
| **Critical** | 2.0x | Active danger, data loss, security holes | SQL injection, RCE, hardcoded secrets |
| **Major** | 1.5x | Significant problems, high bug potential | God classes, no tests, N+1 queries |
| **Minor** | 1.0x | Code smells, maintainability issues | Long functions, magic numbers |
| **Nitpick** | 0.5x | Style, preferences, minor polish | Naming conventions, formatting |

---

## Category Weights

| Category | Weight | Focus Areas |
|----------|--------|-------------|
| Organization | 12% | File structure, module boundaries, separation of concerns |
| Naming | 10% | Variables, functions, classes, constants clarity |
| Error Handling | 12% | Try/catch, validation, error propagation, recovery |
| Testing | 12% | Coverage, test quality, edge cases, mocking |
| Performance | 10% | Efficiency, N+1 queries, memory leaks, scalability |
| Security | 12% | Input validation, auth, secrets, injection |
| Documentation | 8% | Useful comments, API docs, README |
| SOLID/DRY | 10% | SRP, OCP, LSP, ISP, DIP, no duplication |
| Dependencies | 6% | Minimal deps, no circular refs, versions |
| Maintainability | 8% | Complexity, readability, nesting depth |
| **Total** | **100%** | |

---

## Category 1: Organization (12%)

### What to Evaluate

- File and folder structure
- Module boundaries and cohesion
- Separation of concerns
- Entry points and flow clarity

### Deduction Reference

| Issue | Base Points | Severity |
|-------|-------------|----------|
| God file (500+ lines) | 1.5 | Critical |
| God file (300-500 lines) | 1.0 | Major |
| No clear folder structure | 1.0 | Major |
| Mixed concerns in file | 0.75 | Major |
| Files in wrong directory | 0.5 | Minor |
| Inconsistent file naming | 0.5 | Minor |
| Too many files in one folder (20+) | 0.5 | Minor |
| Unclear entry point | 0.25 | Minor |

### Detection Commands

```bash
# Files over 300 lines
find src -name "*.ts" -exec wc -l {} \; | awk '$1 > 300 {print}'

# File count per directory
find src -type d -exec sh -c 'echo -n "{}: "; ls -1 "{}" 2>/dev/null | wc -l' \;

# Files in src root (should be minimal)
ls -la src/*.ts 2>/dev/null | wc -l
```

### Grade Thresholds

| Grade | Criteria |
|-------|----------|
| A | Clean feature-based structure, clear boundaries, <300 line files |
| B | Mostly organized, few large files, clear flow |
| C | Some structure issues, mixed concerns |
| D | Disorganized, many large files, unclear flow |
| F | No structure, god files everywhere |

---

## Category 2: Naming (10%)

### What to Evaluate

- Variable name clarity
- Function name accuracy
- Class name appropriateness
- Constant documentation

### Deduction Reference

| Issue | Base Points | Severity |
|-------|-------------|----------|
| Misleading names | 1.0 | Major |
| Single-letter variables (non-loop) | 0.75 | Major |
| Generic names (data, temp, result, item) | 0.5 | Minor |
| Inconsistent casing style | 0.5 | Minor |
| Magic numbers without constants | 0.5 | Minor |
| Abbreviated names (unclear) | 0.25 | Minor |
| Boolean without is/has/can prefix | 0.25 | Nitpick |

### Detection Commands

```bash
# Single letter variables
grep -rn "const [a-z] =\|let [a-z] =\|var [a-z] =" src/

# Generic names
grep -rn "const data =\|let data =\|const result =\|let temp =" src/

# Magic numbers
grep -rn "[^0-9\.][0-9]\{2,\}[^0-9\.]" src/ | grep -v "test\|spec"
```

---

## Category 3: Error Handling (12%)

### What to Evaluate

- Try/catch placement
- Error messages quality
- Error recovery strategies
- Validation completeness

### Deduction Reference

| Issue | Base Points | Severity |
|-------|-------------|----------|
| No error handling in critical path | 2.0 | Critical |
| Empty catch blocks | 1.5 | Critical |
| Catching and ignoring | 1.5 | Critical |
| Generic error messages | 0.75 | Major |
| No input validation | 0.75 | Major |
| console.error without proper handling | 0.5 | Minor |
| Missing error types/classes | 0.5 | Minor |
| Inconsistent error patterns | 0.25 | Minor |

### Detection Commands

```bash
# Empty catch blocks
grep -rn "catch.*{\s*}" src/
grep -rA2 "catch" src/ | grep -B1 "^\s*}"

# console.error without throw
grep -rn "console.error" src/ | wc -l

# Missing try/catch around async
grep -rn "await" src/ | head -20
```

---

## Category 4: Testing (12%)

### What to Evaluate

- Test coverage percentage
- Test quality (not just quantity)
- Edge case coverage
- Mock/stub appropriateness

### Deduction Reference

| Issue | Base Points | Severity |
|-------|-------------|----------|
| 0% test coverage | 3.0 | Critical |
| No tests for critical paths | 2.0 | Critical |
| <50% coverage | 1.5 | Major |
| 50-70% coverage | 1.0 | Major |
| Tests that don't assert | 1.0 | Major |
| No edge case tests | 0.75 | Major |
| 70-80% coverage | 0.5 | Minor |
| Missing integration tests | 0.5 | Minor |
| Flaky tests | 0.5 | Minor |

### Detection Commands

```bash
# Test file count
find . -name "*.test.*" -o -name "*.spec.*" | wc -l

# Source file count (for ratio)
find src -name "*.ts" | wc -l

# Coverage report
npm test -- --coverage 2>/dev/null
npx jest --coverage 2>/dev/null
```

### Coverage Thresholds

| Coverage | Grade | Deduction |
|----------|-------|-----------|
| 90%+ | A | 0 |
| 80-89% | B | 0.5 |
| 70-79% | C | 1.0 |
| 50-69% | D | 1.5 |
| <50% | F | 2.0+ |

---

## Category 5: Performance (10%)

### What to Evaluate

- Algorithm efficiency
- Database query patterns
- Memory management
- Async/blocking operations

### Deduction Reference

| Issue | Base Points | Severity |
|-------|-------------|----------|
| N+1 query in hot path | 1.5 | Critical |
| Memory leak pattern | 1.5 | Critical |
| Blocking operation in async | 1.0 | Major |
| O(n^2) in hot path | 1.0 | Major |
| Missing pagination | 0.75 | Major |
| No caching strategy | 0.5 | Minor |
| Sequential instead of parallel | 0.5 | Minor |
| Missing indexes | 0.5 | Minor |

### Detection Commands

```bash
# N+1 patterns (loop with query)
grep -rn "for.*await\|forEach.*await" src/
grep -rn "\.findAll\|\.findMany" src/ | head -10

# Sync operations in async
grep -rn "readFileSync\|writeFileSync" src/
grep -rn "execSync" src/
```

See [references/performance-detection.md](references/performance-detection.md) for detailed patterns.

---

## Category 6: Security (12%)

### What to Evaluate

- Input validation
- Authentication/authorization
- Secrets management
- Injection prevention

### Deduction Reference

| Issue | Base Points | Severity |
|-------|-------------|----------|
| SQL injection | 2.0 | Critical |
| Command injection | 2.0 | Critical |
| Hardcoded secrets | 2.0 | Critical |
| XSS vulnerability | 1.5 | Critical |
| Missing auth on endpoint | 1.5 | Critical |
| IDOR vulnerability | 1.5 | High |
| No input validation | 1.0 | Major |
| Weak cryptography | 0.75 | Major |
| Missing security headers | 0.5 | Minor |
| Verbose error messages | 0.25 | Minor |

### Detection Commands

```bash
# Injection patterns
grep -rn "\`SELECT.*\${" src/
grep -rn "exec\|eval" src/

# Secrets
grep -rn "password.*=.*['\"]" src/
grep -rn "api_key.*=.*['\"]" src/

# npm audit
npm audit --json 2>/dev/null | jq '.metadata.vulnerabilities'
```

See [security-audit-checklist skill](../security-audit-checklist/SKILL.md) for comprehensive coverage.

---

## Category 7: Documentation (8%)

### What to Evaluate

- README completeness
- API documentation
- Code comments (why, not what)
- Type definitions

### Deduction Reference

| Issue | Base Points | Severity |
|-------|-------------|----------|
| No README | 1.0 | Major |
| No API documentation | 0.75 | Major |
| Missing setup instructions | 0.5 | Minor |
| Outdated documentation | 0.5 | Minor |
| Comments explaining "what" | 0.25 | Nitpick |
| TODO comments without issues | 0.25 | Nitpick |
| Missing JSDoc on public API | 0.25 | Nitpick |

### Detection Commands

```bash
# Check README exists
ls README.md 2>/dev/null

# Count TODO comments
grep -rn "TODO\|FIXME\|XXX\|HACK" src/ | wc -l

# Check for JSDoc
grep -rn "/\*\*" src/ | wc -l
```

---

## Category 8: SOLID/DRY (10%)

### What to Evaluate

- Single Responsibility adherence
- Open/Closed design
- Liskov Substitution
- Interface Segregation
- Dependency Inversion
- Code duplication

### Deduction Reference

| Issue | Base Points | Severity |
|-------|-------------|----------|
| God class (1000+ lines) | 2.0 | Critical |
| SRP violation (multi-domain class) | 1.0 | Major |
| Switch on type (multiple places) | 0.75 | Major |
| OCP violation (modify to extend) | 0.75 | Major |
| LSP violation (broken substitution) | 0.75 | Major |
| Large interface (10+ methods) | 0.5 | Minor |
| Concrete dependencies | 0.5 | Minor |
| Duplicated code blocks | 0.5 | Minor |

### Detection Commands

```bash
# Duplicate code
npx jscpd src/ --min-lines 10

# Large classes
grep -A 500 "^class" src/**/*.ts | head -100

# Switch statements on type
grep -rn "switch.*type\|switch.*kind" src/
```

See [code-smell-detector skill](../code-smell-detector/SKILL.md) for comprehensive patterns.

---

## Category 9: Dependencies (6%)

### What to Evaluate

- Dependency count
- Circular dependencies
- Version management
- Security vulnerabilities

### Deduction Reference

| Issue | Base Points | Severity |
|-------|-------------|----------|
| Critical CVE in dependency | 2.0 | Critical |
| Circular dependencies | 1.0 | Major |
| Excessive dependencies (50+) | 0.75 | Major |
| High CVE in dependency | 0.5 | Major |
| Outdated major versions | 0.5 | Minor |
| No lockfile | 0.5 | Minor |
| Unused dependencies | 0.25 | Minor |

### Detection Commands

```bash
# Dependency count
cat package.json | jq '.dependencies | length'

# Circular dependencies
npx madge --circular src/

# Security audit
npm audit --json

# Unused dependencies
npx depcheck

# Outdated packages
npm outdated
```

---

## Category 10: Maintainability (8%)

### What to Evaluate

- Cyclomatic complexity
- Nesting depth
- Code readability
- Cognitive load

### Deduction Reference

| Issue | Base Points | Severity |
|-------|-------------|----------|
| Function complexity >30 | 1.5 | Critical |
| Function complexity 20-30 | 1.0 | Major |
| Nesting depth 5+ | 1.0 | Major |
| Function complexity 15-20 | 0.5 | Minor |
| Function >100 lines | 0.5 | Minor |
| Nesting depth 4 | 0.25 | Minor |
| any types everywhere | 0.5 | Minor |
| Inconsistent formatting | 0.25 | Nitpick |

### Detection Commands

```bash
# Complexity analysis
npx escomplex src/ --format json | jq '.aggregate.cyclomatic'

# TypeScript any usage
grep -rn ": any\|as any" src/ | wc -l

# Type coverage
npx type-coverage --detail 2>/dev/null
```

---

## Score Calculation Example

```
Category: Security (Weight: 12%)

Issues Found:
1. SQL Injection (src/api/users.ts:45)
   - Base: 2.0, Severity: Critical (2.0x)
   - Deduction: 2.0 * 2.0 = 4.0

2. Hardcoded API key (src/config.ts:12)
   - Base: 2.0, Severity: Critical (2.0x)
   - Deduction: 2.0 * 2.0 = 4.0

3. Missing input validation (5 endpoints)
   - Base: 1.0, Severity: Major (1.5x)
   - Deduction: 1.0 * 1.5 = 1.5

Category Raw Deduction: 4.0 + 4.0 + 1.5 = 9.5 (capped at 10)
Category Raw Score: 10 - 9.5 = 0.5/10
Weighted Contribution: 0.5 * 0.12 = 0.06 (out of 1.20 max)
Grade: F
```

---

## Score Interpretation

| Score | Verdict | Reality Check |
|-------|---------|---------------|
| **10** | Exemplary | You actually did everything right. Rare. |
| **9** | Excellent | Minor polish. Ship it. |
| **8** | Very Good | Few small fixes. Solid work. |
| **7** | Good | Acceptable. Some cleanup needed. |
| **6** | Satisfactory | Works but rough. Needs attention. |
| **5** | Adequate | Barely meets the bar. Clear problems. |
| **4** | Below Average | Significant issues. Risky to deploy. |
| **3** | Poor | Major rework needed. Architectural problems. |
| **2** | Very Poor | Fundamental issues. Barely functional. |
| **1** | Critical | Do not deploy. Security holes. Will crash. |

---

## Report Template

```markdown
## Score Breakdown

| Category | Weight | Raw Score | Deductions | Weighted | Grade |
|----------|--------|-----------|------------|----------|-------|
| Organization | 12% | X.X/10 | -X.X | X.XX/1.20 | {A-F} |
| Naming | 10% | X.X/10 | -X.X | X.XX/1.00 | {A-F} |
| Error Handling | 12% | X.X/10 | -X.X | X.XX/1.20 | {A-F} |
| Testing | 12% | X.X/10 | -X.X | X.XX/1.20 | {A-F} |
| Performance | 10% | X.X/10 | -X.X | X.XX/1.00 | {A-F} |
| Security | 12% | X.X/10 | -X.X | X.XX/1.20 | {A-F} |
| Documentation | 8% | X.X/10 | -X.X | X.XX/0.80 | {A-F} |
| SOLID/DRY | 10% | X.X/10 | -X.X | X.XX/1.00 | {A-F} |
| Dependencies | 6% | X.X/10 | -X.X | X.XX/0.60 | {A-F} |
| Maintainability | 8% | X.X/10 | -X.X | X.XX/0.80 | {A-F} |
| **TOTAL** | **100%** | | **-X.X** | **X.XX/10.00** | |

### Grade Scale
- A: 9.0-10.0 (Excellent)
- B: 7.0-8.9 (Good)
- C: 5.0-6.9 (Acceptable)
- D: 3.0-4.9 (Poor)
- F: 0.0-2.9 (Failing)
```

## Reference Files

- [references/performance-detection.md](references/performance-detection.md) - Performance issue detection patterns
- [references/quick-reference-card.md](references/quick-reference-card.md) - One-page scoring summary
