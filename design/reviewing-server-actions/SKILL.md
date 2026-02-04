---
name: reviewing-server-actions
description: Review Server Actions for security, validation, and best practices in React 19. Use when reviewing forms, mutations, or server-side logic.
review: true
allowed-tools: Read, Grep, Glob
version: 1.0.0
---

# Review: Server Actions

## Security Checklist

### Input Validation
- [ ] All inputs validated with schema (zod, yup, etc.)
- [ ] Type coercion handled correctly (FormData.get returns strings)
- [ ] Length limits enforced
- [ ] No SQL injection vulnerabilities

For runtime validation patterns and type safety, use the using-runtime-checks skill from the typescript plugin.

If reviewing Zod schema validation patterns, use the validating-schema-basics skill for type-safe Zod v4 schema patterns.

### Authentication & Authorization
- [ ] Session/auth checked before mutations
- [ ] User permissions verified
- [ ] Resource ownership validated
- [ ] No unauthorized access possible

For secure credential handling, use the SECURITY-credentials skill from the typescript plugin.

### Data Sanitization
- [ ] User input sanitized before storage
- [ ] No XSS vulnerabilities
- [ ] File uploads validated (type, size, content)
- [ ] Dangerous operations require confirmation

## Best Practices

### Error Handling
- [ ] Try-catch blocks for async operations
- [ ] Specific error messages for users
- [ ] No sensitive data in error messages
- [ ] Logging for debugging

### Return Values
- [ ] Return serializable objects only
- [ ] Consistent response format
- [ ] Success and error states handled
- [ ] Field-specific errors when needed

### Performance
- [ ] Database queries optimized
- [ ] No N+1 query problems
- [ ] Appropriate use of transactions
- [ ] Rate limiting where needed

## Anti-Patterns to Flag

- [ ] ❌ No validation (trusting client input)
- [ ] ❌ No authentication checks
- [ ] ❌ Returning non-serializable values (functions, classes)
- [ ] ❌ Missing error handling
- [ ] ❌ Exposing sensitive data
- [ ] ❌ Direct database queries without sanitization
- [ ] ❌ No rate limiting on critical actions

For comprehensive Server Actions security, see: `research/react-19-comprehensive.md` lines 723-729, 1808-1942.
