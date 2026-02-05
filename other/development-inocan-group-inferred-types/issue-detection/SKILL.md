---
name: issue-detection
description: Static analysis issue detection patterns and rules
---

# Issue Detection Methodology

## Objective

Identify code issues across security, quality, performance, and maintainability dimensions.

## Security Issues

### Injection Vulnerabilities

**SQL Injection**
- Pattern: String concatenation in SQL queries
- Detection: Look for query strings built with + operator
- Fix: Use parameterized queries

**Command Injection**
- Pattern: User input passed to shell execution functions
- Detection: Look for subprocess/exec calls with dynamic arguments
- Fix: Use subprocess with shell=False, validate inputs

**XSS**
- Pattern: Unescaped user input in HTML output
- Detection: Template variables without escaping filters
- Fix: HTML escape all user content

### Authentication Issues

**Hardcoded Credentials**
- Pattern: password/secret/key assignments with string literals
- Detection: Regex for common credential variable names
- Fix: Use environment variables

**Weak Crypto**
- Pattern: MD5, SHA1 for passwords, ECB mode
- Fix: Use bcrypt/argon2 for passwords, AES-GCM

## Quality Issues

### Complexity Violations

**High Cyclomatic Complexity**
- Threshold: > 20
- Impact: Hard to test, prone to bugs
- Fix: Extract methods, reduce conditions

**Deep Nesting**
- Threshold: > 5 levels
- Impact: Hard to read and maintain
- Fix: Early returns, guard clauses

### Code Smells

**Long Method**
- Threshold: > 50 lines
- Fix: Extract smaller methods

**Large Class**
- Threshold: > 500 lines or > 20 methods
- Fix: Split into focused classes

**Long Parameter List**
- Threshold: > 5 parameters
- Fix: Use parameter object

## Performance Issues

### Algorithm Efficiency

**N+1 Queries**
- Pattern: Loop containing database query
- Detection: ORM calls inside for/while loops
- Fix: Use eager loading/joins

**Quadratic Algorithms**
- Pattern: Nested loops over same collection
- Impact: O(n^2) scaling
- Fix: Use sets, maps, or better algorithms

### Resource Management

**Unclosed Resources**
- Pattern: File/connection open without close or context manager
- Fix: Use `with` statement

**Memory Issues**
- Pattern: Growing collections without bounds
- Fix: Use bounded caches, weak references

## Maintainability Issues

### Documentation Gaps

**Missing Docstrings**
- Pattern: Public functions without documentation
- Standard: All public APIs documented

**Outdated Comments**
- Pattern: Comments contradicting code
- Fix: Update or remove

### Test Coverage

**Untested Code**
- Pattern: No corresponding test file
- Threshold: < 60% coverage is concern

**Missing Edge Case Tests**
- Pattern: Only happy path tested
- Fix: Add boundary and error tests

## Issue Reporting Format

```
[SEVERITY] [CATEGORY] in [file:line]
Description: [what is wrong]
Impact: [why it matters]
Fix: [how to resolve]
Confidence: [High/Medium/Low]
```

## Severity Classification

| Severity | Criteria |
|----------|----------|
| Critical | Security vulnerability, data loss risk |
| High | Performance blocker, major quality issue |
| Medium | Code smell, minor security concern |
| Low | Style issue, improvement suggestion |
