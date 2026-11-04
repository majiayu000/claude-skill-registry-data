---
name: security-review
description: Security audit checklist for code changes. Run before committing to catch vulnerabilities.
---

# Security Review

Automated security review checklist for code changes. Covers OWASP Top 10,
dependency vulnerabilities, secret exposure, and injection vectors.

## Checklist

Run against all modified files before commit:

### 1. Input Validation
- [ ] All user inputs validated and sanitized
- [ ] SQL queries use parameterized statements (no string concatenation)
- [ ] Shell commands use safe argument passing (no interpolation)
- [ ] Path traversal prevented (no `../` in user paths)
- [ ] File uploads validated (type, size, name)

### 2. Authentication & Authorization
- [ ] Auth checks on all protected endpoints
- [ ] Session tokens are cryptographically random
- [ ] Password hashing uses bcrypt/argon2 (not MD5/SHA1)
- [ ] API keys not hardcoded in source

### 3. Secrets Management
- [ ] No secrets in source code (API keys, passwords, tokens)
- [ ] `.env` files in `.gitignore`
- [ ] Environment variables used for configuration
- [ ] No secrets in log output or error messages

### 4. Dependency Security
- [ ] Dependency audit passes
- [ ] No known CVEs in dependencies
- [ ] Lock files committed and up to date
- [ ] Minimal dependency footprint

### 5. Error Handling
- [ ] Error messages don't leak internal details
- [ ] Stack traces not exposed to users
- [ ] Graceful degradation on failure
- [ ] Timeouts configured for external calls

### 6. Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] HTTPS enforced for all external communication
- [ ] PII handling follows minimum exposure principle
- [ ] Logs don't contain sensitive user data

### 7. Injection Prevention
- [ ] XSS: Output encoding applied
- [ ] CSRF: Tokens used for state-changing operations
- [ ] Command injection: Safe argument passing, no shell interpolation with user data
- [ ] SSRF: External URL validation

### 8. Configuration
- [ ] Debug mode disabled in production
- [ ] CORS configured restrictively
- [ ] Security headers set (CSP, HSTS, X-Frame-Options)
- [ ] Rate limiting on sensitive endpoints

## Severity Levels

- **CRITICAL**: Must fix before commit (secrets exposure, SQL injection)
- **HIGH**: Should fix before merge (missing auth, XSS)
- **MEDIUM**: Fix in same sprint (missing rate limiting, verbose errors)
- **LOW**: Track and fix later (minor header issues)
