---
name: code-review
description: Review generated code for style, security, and architecture issues; suggest refactorings and performance improvements. Use after implementation is complete, before merging changes, or when refactoring existing code. Follows OWASP guidelines, SOLID principles, and best practices for maintainable code.
license: MIT
metadata:
  author: AC Framework
  version: "1.0"
---

# Code Review

Comprehensive code analysis for quality, security, maintainability, and performance optimization.

## When to Use This Skill

Use this skill when:
- Reviewing code before merging (pre-merge review)
- After implementation is complete in openspec-apply-change
- Refactoring existing code for improvement
- Auditing code for security vulnerabilities
- Optimizing performance-critical sections
- Ensuring adherence to project standards

## Instructions

### Step 1: Initial Assessment

1. **Read the code** being reviewed
2. **Understand the context**:
   - What problem does this solve?
   - What are the requirements?
   - Are there related files/components?
3. **Identify the scope**:
   - Lines changed
   - Files modified
   - Dependencies introduced

### Step 2: Security Review (OWASP)

Check for common security vulnerabilities:

**Input Validation**:
- [ ] All user inputs are validated/sanitized
- [ ] No SQL injection vulnerabilities
- [ ] No command injection risks
- [ ] Path traversal prevented
- [ ] File uploads restricted

**Authentication & Authorization**:
- [ ] Proper authentication checks
- [ ] Role-based access control (RBAC)
- [ ] Session management secure
- [ ] No hardcoded secrets or credentials
- [ ] API keys not exposed in client code

**Data Protection**:
- [ ] Sensitive data encrypted
- [ ] Proper handling of PII (Personally Identifiable Information)
- [ ] Secure communication (HTTPS/TLS)
- [ ] No sensitive data in logs

**Output Encoding**:
- [ ] XSS prevention (output encoding)
- [ ] CSRF protection
- [ ] Content Security Policy headers

### Step 3: Architecture Review

Evaluate against design principles:

**SOLID Principles**:
- **S**ingle Responsibility: Each class/function has one reason to change
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subtypes are substitutable for base types
- **I**nterface Segregation: Small, focused interfaces
- **D**ependency Inversion: Depend on abstractions, not concretions

**Design Patterns**:
- Appropriate use of patterns
- No over-engineering
- Consistent with project conventions

**Coupling & Cohesion**:
- Low coupling between modules
- High cohesion within modules
- Clear module boundaries

### Step 4: Code Quality Review

**Readability**:
- [ ] Clear naming (variables, functions, classes)
- [ ] Consistent formatting
- [ ] Appropriate comments (why, not what)
- [ ] No magic numbers/strings
- [ ] Functions are focused and small

**Maintainability**:
- [ ] DRY (Don't Repeat Yourself)
- [ ] No code duplication
- [ ] Easy to test
- [ ] Documentation exists
- [ ] Error handling comprehensive

**Error Handling**:
- [ ] Exceptions are caught appropriately
- [ ] Error messages are user-friendly
- [ ] Failures are logged
- [ ] Graceful degradation

### Step 5: Performance Review

**Efficiency**:
- [ ] No unnecessary computations
- [ ] Efficient data structures
- [ ] Database queries optimized
- [ ] No N+1 query problems
- [ ] Caching used appropriately

**Resource Usage**:
- [ ] Memory leaks prevented
- [ ] Large objects disposed properly
- [ ] No blocking operations on main thread
- [ ] Async/await used correctly

### Step 6: Testing Review

- [ ] Unit tests exist for new logic
- [ ] Tests cover edge cases
- [ ] Integration tests for API contracts
- [ ] Test names are descriptive
- [ ] Mocks are appropriate
- [ ] Test coverage is adequate (>80%)

### Step 7: Documentation Review

- [ ] Code comments explain complex logic
- [ ] Public APIs are documented (JSDoc, docstrings)
- [ ] README updated if needed
- [ ] Architecture Decision Records (ADRs) for significant changes
- [ ] Changelog entries added

### Step 8: Compile Findings

Organize issues by severity:

```
## Code Review Report

### Critical (Block Merge)
1. [Security vulnerability description]
   - File: path/to/file.ext:line
   - Issue: [detailed explanation]
   - Fix: [recommended solution]

### High (Should Fix)
1. [Performance or architecture issue]
   ...

### Medium (Nice to Have)
1. [Style or readability improvement]
   ...

### Low (Suggestions)
1. [Minor improvements]
   ...

### Positive Feedback
- [What was done well]
```

### Step 9: Provide Actionable Feedback

For each issue:
1. **Explain the problem** (why it's an issue)
2. **Show the problematic code**
3. **Suggest a fix** (with code example if possible)
4. **Reference best practices** (OWASP, SOLID, etc.)

### Step 10: Follow-up

1. **Track fixes** - Ensure all critical/high issues are addressed
2. **Re-review** if significant changes are made
3. **Update documentation** based on review findings
4. **Share learnings** - Common issues can inform team guidelines

## Integration with OpenSpec

- Run after `openspec-apply-change` completes
- Block merge in `openspec-verify-change` until critical issues resolved
- Link review findings to tasks in tasks.md
- Document architectural decisions in design.md

## Guardrails

- **Be constructive** - Focus on the code, not the person
- **Explain why** - Don't just say "change this", explain the reason
- **Balance thoroughness with pragmatism** - Not everything needs to be perfect
- **Respect existing patterns** - Don't force changes unless there's a good reason
- **Consider the context** - Startup MVP vs. enterprise system have different standards

## Review Checklist Template

```markdown
## Security
- [ ] Input validation
- [ ] Authentication/authorization
- [ ] No secrets in code
- [ ] XSS/CSRF protection

## Architecture
- [ ] SOLID principles
- [ ] Appropriate patterns
- [ ] Low coupling

## Quality
- [ ] Naming clarity
- [ ] No duplication
- [ ] Error handling
- [ ] Comments where needed

## Performance
- [ ] Efficient algorithms
- [ ] No N+1 queries
- [ ] Proper async usage

## Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Edge cases covered

## Documentation
- [ ] Code comments
- [ ] API docs
- [ ] README updated
```

## Requirements

- Access to the codebase
- Understanding of project conventions
- Knowledge of security best practices (OWASP)
- Familiarity with design patterns
- Understanding of performance optimization

## See Also

- `secure-coding-cybersecurity` - Deep security audit
- `performance-optimizer` - Performance analysis
- `code-maintainability` - Maintainability assessment
- `openspec-verify-change` - Verification with review gates
