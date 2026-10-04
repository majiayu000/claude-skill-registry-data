---
name: simple-code-review
description: Review code for security, accessibility, code quality, and performance. Reports findings by severity, does not fix unless asked.
disable-model-invocation: true
metadata:
  author: denniemok
  version: "1.0.0"
license: MIT
---

# Simple Code Review

Review the code by module. The checklists cover common issues, not everything. Use judgment on what applies to this codebase, and report any obvious issue you find even if it is not listed.

## Scope

Review what the user points at. If nothing is specified, review the current diff, or the files changed in this session. Ask before reviewing the whole codebase.

## Modules

Ask which to run, unless the user already said:

- Security
- Accessibility
- Code Quality
- Performance

If the user has no preference, run all four.

## 1. Security

Goal: find serious security holes.

Frontend:
- XSS (`dangerouslySetInnerHTML`, unescaped user input)
- Sensitive data exposed in client code
- Hardcoded secrets, tokens, or API keys

Backend:
- SQL injection, especially raw queries built with string interpolation
- Command injection in subprocess or shell calls
- SSRF in server-side HTTP calls that use user-supplied URLs
- Insecure deserialization (`pickle`, `yaml.load` without a safe loader)
- Path traversal in file operations
- Missing authentication or authorization on protected endpoints
- Insecure direct object references, such as queries not scoped to the current user
- Hardcoded secrets or credentials

## 2. Accessibility

Goal: find obvious issues that hurt users. Frontend only.

- Missing labels on interactive elements
- No keyboard navigation or visible focus
- Non-semantic HTML where a proper element exists
- Poor color contrast in custom styling
- Images without alt text

## 3. Code Quality

Goal: keep the code maintainable and consistent.

- Duplication, extract at 3 or more identical uses
- Functions or components doing too much, if you need "and" to describe it, split it
- Deep nesting, prefer early returns and guard clauses
- Magic numbers and strings without named constants
- Poor naming: vague names (`data`, `temp`), misleading names, booleans without `is`/`has`/`can`/`should`
- Missing error handling or error boundaries
- Boolean parameters that switch behavior, prefer two functions or components
- Files over about 500 lines
- `console.log` or debug leftovers in production code
- Code written for future needs with no present use (YAGNI)

## 4. Performance

Goal: find issues that seriously affect users.

- N+1 queries, especially DB calls inside loops
- Missing indexes on frequently queried columns
- Large result sets loaded without pagination
- Blocking operations in async code
- Memory leaks, such as unbounded caches or retained references
- Missing caching for repeated expensive work
- Frontend: unnecessary re-renders, oversized bundles, unoptimized images

## Output

Give the total issue count, then list each issue with:

- Severity: Critical, High, Medium, Low, or Optional
- Category and `file:line`
- What is wrong, and why it matters
- Suggested fix

Only report issues you can point to in the code. Do not change code unless the user asks.
