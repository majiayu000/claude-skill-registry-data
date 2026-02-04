---
name: review-code-quality
description: Use when reviewing code for quality, security vulnerabilities, and best practices
---

# Code Quality & Security Review

Guidelines for comprehensive code review covering quality, security, and best practices.

## When to Use

- Code review before merge
- Security assessment of changes
- After implementing authentication/authorization
- When handling sensitive data
- Dependency updates

## Review Methodology

1. **Identify** questionable or improvable areas
2. **Dig deeper** - Examine ripple effects, dependencies, related code
3. **Play devil's advocate** - Consider invalidating evidence
4. **Document reasoning** before conclusions
5. **Surface only high-confidence** suggestions

## Quality Checklist

### Code Quality
- [ ] Logic correctness and error handling
- [ ] Resource management and cleanup
- [ ] Naming conventions and readability
- [ ] Function complexity < 10 cyclomatic
- [ ] No duplication (DRY principle)
- [ ] Code coverage > 80%

### Security Review
- [ ] Input validation and sanitization
- [ ] Authentication/authorization checks
- [ ] No injection vulnerabilities (SQL, XSS, command)
- [ ] Proper cryptographic practices
- [ ] Sensitive data handled securely
- [ ] Dependencies scanned for vulnerabilities

### Performance
- [ ] Algorithm efficiency appropriate
- [ ] No N+1 query problems
- [ ] Memory usage reasonable
- [ ] Async patterns used correctly
- [ ] Caching considered where beneficial

### Design
- [ ] SOLID principles followed
- [ ] Appropriate abstraction levels
- [ ] Low coupling, high cohesion
- [ ] Interface contracts clear

## Security Principles

1. **Defense in Depth** - Multiple redundant controls
2. **Least Privilege** - Minimum necessary access
3. **Never Trust Input** - Validate all external input
4. **Fail Securely** - Default to secure state on error
5. **Secure Error Handling** - No sensitive info in errors

## Common Vulnerabilities

### Injection
- SQL: Use parameterized queries
- XSS: Sanitize output, use CSP
- Command: Avoid shell; use safe APIs

### Authentication
- Session fixation: Regenerate on login
- Credential storage: Use bcrypt/argon2
- Token handling: Validate expiry, signature

### Data Exposure
- Encrypt at rest and in transit
- Mask sensitive data in logs
- Implement proper access controls

## Output Format

Number all suggestions. Each entry:

1. **Reasoning**: Step-by-step exploration with references to files/functions, including counterarguments considered
2. **Conclusion**: If justified, state the actionable recommendation

### Example

```
1.
   - Reasoning: Examined calculateTotal() null-safety. Traced usages
     in services/baz.ts. Constructor always sets value.
   - Conclusion: No change needed; code is safe.

2.
   - Reasoning: Observed duplicate logic in calculateTotal() and
     sumOrderAmounts(). Confirmed identical logic, abstraction viable.
   - Conclusion: Refactor into shared helper function.
```

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| Critical | Exploitable vulnerability, data loss risk | Block merge |
| High | Significant security/quality issue | Must fix |
| Medium | Should be addressed | Fix recommended |
| Low | Improvement opportunity | Optional |

## Language-Specific Checks

- **TypeScript**: Strict mode, no `any`, proper null handling
- **Python**: Type hints, PEP 8, no mutable defaults
- **Nix**: No `with` statements, nixfmt-rfc-style
- **Go**: Idiomatic error handling, proper defer
- **Rust**: Ownership patterns, lifetime management
- **Shell**: Proper quoting, safe practices

## Feedback Style

- **Specific**: Reference exact lines with examples
- **Actionable**: Suggest concrete improvements
- **Prioritized**: Critical issues first
- **Constructive**: Acknowledge good practices
- **Educational**: Explain the "why"
