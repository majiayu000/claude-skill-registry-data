---
id: code-review
name: Code Review Best Practices
description: Systematic approach to reviewing code for quality, security, and maintainability
skill_type: workflow
version: 1.0.0
author: Example
requires_tools: [analyze_code]
tags: [code, review, development, security]
icon: code
enabled_by_default: false
---

# Code Review Skill

When reviewing code, follow this comprehensive checklist:

## 1. Correctness
- Does the code do what it's supposed to do?
- Are edge cases handled?
- Is the logic correct?
- Are there any off-by-one errors?

## 2. Security
- Input validation present?
- No SQL injection vulnerabilities?
- No XSS vulnerabilities?
- Secrets not hardcoded?
- Proper authentication/authorization?

## 3. Performance
- No unnecessary loops or iterations?
- Efficient data structures used?
- Database queries optimized?
- No N+1 query problems?

## 4. Maintainability
- Code is readable and self-documenting?
- Functions/methods are focused (single responsibility)?
- Appropriate naming conventions?
- No magic numbers/strings?

## 5. Testing
- Unit tests included?
- Edge cases tested?
- Tests are meaningful (not just for coverage)?

## 6. Documentation
- Public APIs documented?
- Complex logic explained?
- README updated if needed?

## Review Feedback Guidelines
- Be constructive and specific
- Explain the "why" behind suggestions
- Distinguish between required changes and suggestions
- Acknowledge good practices
