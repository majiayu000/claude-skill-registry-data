---
name: security-audit
description: Security review checklist for code and infrastructure
phases: [R, V]
---

# Security Audit

## When to Use
Use this skill when reviewing code for security or performing security audits.

## OWASP Top 10 Checklist

### 1. Injection
- [ ] SQL queries use parameterized statements
- [ ] OS commands avoid user input
- [ ] LDAP queries are sanitized

### 2. Broken Authentication
- [ ] Passwords hashed with bcrypt/argon2
- [ ] Session tokens are secure random
- [ ] MFA available for sensitive operations

### 3. Sensitive Data Exposure
- [ ] Data encrypted at rest
- [ ] TLS for data in transit
- [ ] Secrets not in code/logs

### 4. XML External Entities (XXE)
- [ ] XML parsing disables external entities
- [ ] JSON preferred over XML

### 5. Broken Access Control
- [ ] Authorization checked on every request
- [ ] Direct object references validated
- [ ] CORS configured correctly

### 6. Security Misconfiguration
- [ ] Debug mode disabled in production
- [ ] Default credentials changed
- [ ] Security headers set

### 7. Cross-Site Scripting (XSS)
- [ ] Output encoding applied
- [ ] Content Security Policy set
- [ ] Input validation present

### 8. Insecure Deserialization
- [ ] User input not deserialized directly
- [ ] Integrity checks on serialized data

### 9. Using Components with Known Vulnerabilities
- [ ] Dependencies up to date
- [ ] Vulnerability scanning in CI
- [ ] SBOM maintained

### 10. Insufficient Logging & Monitoring
- [ ] Security events logged
- [ ] Logs don't contain sensitive data
- [ ] Alerting configured

## Report Format
```markdown
## Security Audit: [Component]

### Scope
[What was reviewed]

### Findings
| ID | Severity | Issue | Remediation |
|----|----------|-------|-------------|
| S1 | Critical | [Issue] | [Fix] |

### Recommendations
1. [Priority recommendation]
2. [Secondary recommendation]
```