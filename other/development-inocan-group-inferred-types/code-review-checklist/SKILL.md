---
name: code-review-checklist
description: Code review criteria covering security, performance, quality standards, and issue prioritization for thorough code analysis.
---

# Code Review Checklist

## Issue Prioritization

### Critical (Must Fix Before Merge)
- Security vulnerabilities
- Data loss risks
- Breaking changes without migration
- Test failures
- Build failures

### Warnings (Should Fix)
- Performance issues
- Code quality violations
- Missing error handling
- Incomplete documentation
- Test coverage gaps

### Suggestions (Nice to Have)
- Refactoring opportunities
- Code style improvements
- Additional test cases
- Documentation enhancements

## Security Review (OWASP Top 10)

### Injection (SQL, Command, XSS)
- [ ] Parameterized queries or ORM (no string concatenation in SQL)
- [ ] Input sanitization before rendering in templates
- [ ] Command arguments properly escaped
- [ ] User input never directly in file paths

### Authentication & Authorization
- [ ] Endpoints protected with `@PreAuthorize` or equivalent
- [ ] Role checks at service layer, not just controller
- [ ] Session management follows best practices
- [ ] Password handling uses secure hashing (bcrypt)

### Sensitive Data Exposure
- [ ] No secrets in code or logs
- [ ] PII protected in transit (HTTPS) and at rest
- [ ] Error messages don't leak internal details
- [ ] Debug endpoints disabled in production

### CSRF & CORS
- [ ] CSRF tokens required for state-changing operations
- [ ] CORS policy restricts allowed origins
- [ ] SameSite cookie attribute set appropriately

## Performance Review

### Backend
- [ ] N+1 query patterns avoided (use `JOIN FETCH` or `@EntityGraph`)
- [ ] Pagination for list endpoints
- [ ] Appropriate indexes on frequently queried columns
- [ ] Caching for expensive computations
- [ ] Async processing for long-running tasks

### Frontend
- [ ] Large lists virtualized
- [ ] Images optimized and lazy-loaded
- [ ] Bundle size not significantly increased
- [ ] Memoization for expensive renders (`useMemo`, `React.memo`)
- [ ] No unnecessary re-renders (check dependency arrays)

### Database
- [ ] Migrations are reversible
- [ ] New indexes don't impact write performance excessively
- [ ] Large data operations batched

## Code Quality Standards

### DRY (Don't Repeat Yourself)
- [ ] No copy-pasted logic that should be abstracted
- [ ] Shared utilities extracted appropriately
- [ ] Configuration centralized

### SOLID Principles
- [ ] Single Responsibility: Classes/functions do one thing
- [ ] Open/Closed: Extensible without modification
- [ ] Liskov Substitution: Subtypes substitutable for base types
- [ ] Interface Segregation: Interfaces are focused
- [ ] Dependency Inversion: Depend on abstractions

### Readability
- [ ] Clear, descriptive naming
- [ ] Functions are reasonably sized (<50 lines)
- [ ] Complex logic has comments explaining "why"
- [ ] Consistent code style (enforced by formatters)

### Error Handling
- [ ] Errors caught and handled appropriately
- [ ] User-facing error messages are helpful
- [ ] Errors logged with sufficient context
- [ ] Recovery paths where appropriate

## Test Coverage Assessment

### Unit Tests
- [ ] New public methods have tests
- [ ] Edge cases covered (null, empty, boundary values)
- [ ] Error paths tested
- [ ] Mocks used appropriately (not over-mocked)

### Integration Tests
- [ ] API endpoints tested with realistic data
- [ ] Database interactions verified
- [ ] External service integrations stubbed

### E2E Tests
- [ ] Critical user flows covered
- [ ] Happy path and main error cases
- [ ] Cross-browser testing for UI changes

## Review Output Format

```
## Code Quality Findings

### Critical Issues (Must Fix)
- [File:Line] Issue description
  - Why it's critical
  - Suggested fix

### Warnings (Should Fix)
- [File:Line] Issue description
  - Impact
  - Suggested fix

### Suggestions (Nice to Have)
- [File:Line] Improvement opportunity
  - Benefit
  - How to implement
```
