---
name: grey-haven-code-quality-analysis
description: "Multi-mode code quality analysis covering security reviews (OWASP Top 10), clarity refactoring (readability rules), and synthesis analysis (cross-file issues). Use when reviewing code for security vulnerabilities, improving code readability, conducting quality audits, pre-deployment checks, or when user mentions 'code quality', 'code review', 'security review', 'refactoring', 'code smell', 'OWASP', 'code clarity', or 'quality audit'."
# v2.0.43: Skills to auto-load for quality analysis subagents
skills:
  - grey-haven-code-style
  - grey-haven-security-practices
  - grey-haven-documentation-alignment
# v2.0.74: Restrict tools for analysis-focused work
allowed-tools:
  - Read
  - Grep
  - Glob
  - TodoWrite
  - Write
  - Edit
---

# Code Quality Analysis Skill

Multi-mode code quality specialist with security review, clarity refactoring, and synthesis analysis.

## Description

Comprehensive code quality analysis including security vulnerability detection, readability improvements, and cross-file issue synthesis.

## What's Included

- **Examples**: Security reviews, refactoring patterns, quality improvements
- **Reference**: OWASP Top 10, code smells, refactoring catalog
- **Templates**: Code review templates, security audit structures
- **Checklists**: Quality verification, security compliance

## Modes

1. **Security Review** - Find vulnerabilities (OWASP Top 10)
2. **Clarity Refactoring** - Improve readability (10 rules)
3. **Synthesis Analysis** - Cross-file issues

## Use This Skill When

- Reviewing code for security issues
- Improving code readability
- Comprehensive quality audits
- Pre-deployment checks

## Related Agents

- `code-quality-analyzer` - Automated quality analysis
- `security-analyzer` - Deep security audits

---

**Skill Version**: 1.0
