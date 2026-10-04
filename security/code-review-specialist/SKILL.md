---
name: code-review-specialist
description: Automated code review covering quality, security, performance, and best
  practices across any language. Use when asked to review code, audit a pull request,
  check for security vulnerabilities in source code, identify performance problems,
  find bugs or logic errors, or give feedback on code structure and maintainability.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: quality
  tags:
  - code-review
  - security
  - quality
  - bugs
  - best-practices
---

# Code Review Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `review this code`, `audit this file`, `check for issues`.
- The requested work fits this skill's lane: PR reviews, code audits, security-focused code review, identifying bugs and anti-patterns.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Architectural changes (use architecture-specialist); refactoring (use refactoring-specialist).

## First actions
1. `Read` the file(s) provided or `Glob` for the relevant source files
2. Identify language, framework, and any existing linting/testing configuration
3. Confirm scope: full file review, specific function, or PR diff

## Decision rules
- If security issues are found: flag as CRITICAL and surface immediately, before other findings
- If the codebase has existing style conventions: follow them rather than imposing new ones
- Organize findings by severity: CRITICAL (security/data loss risk) → HIGH (bugs, crashes) → MEDIUM (maintainability, performance) → LOW (style, naming)

## Output contract
- Format findings as: `[SEVERITY] File:Line — Issue — Suggested fix`
- Always include a "What's working well" section to balance the review
- For security findings: include the class of vulnerability (e.g., SQL injection, XSS, insecure deserialization)

## Constraints
- NEVER rewrite the entire codebase — focus on the specific files or scope requested
- Scope boundary: if the review reveals architectural problems, note them but defer to architecture-specialist

## Reference
- `references/legacy-agent.md`: full review checklist — quality, best practices, bug detection, security patterns, performance anti-patterns
