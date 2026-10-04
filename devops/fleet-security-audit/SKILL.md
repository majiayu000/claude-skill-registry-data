---
name: fleet-security-audit
description: How to conduct a security review of code or infrastructure
user-invocable: false
---

# Fleet Security Audit Skill

You are conducting a security review.

## 1. Scope
- What are you reviewing? (PR, deployment, configuration, dependencies)
- What project? What component?

## 2. Check Areas

### Code Review:
- [ ] No secrets in code (tokens, keys, passwords)
- [ ] No hardcoded credentials
- [ ] Input validation at boundaries
- [ ] No SQL injection / command injection patterns
- [ ] No XSS patterns in output
- [ ] Dependencies checked for known CVEs
- [ ] No world-writable permissions (chmod 777)

### Infrastructure Review:
- [ ] Default credentials changed
- [ ] Ports properly restricted
- [ ] Network isolation between services
- [ ] TLS/encryption for external connections
- [ ] Secrets in .env (gitignored), not in code
- [ ] Container images from trusted registries

### Supply Chain:
- [ ] Dependencies from official sources
- [ ] No unnecessary dependencies
- [ ] Lock files present and up to date

## 3. Report Findings
```
fleet_alert(
  severity="critical|high|medium|low",
  title="Finding title",
  details="What was found + evidence + recommendation",
  category="security"
)
```

## 4. Security Hold (Critical)
For critical findings, request security hold:
```
fleet_notify_human(
  title="Security hold: {finding}",
  message="Details + recommendation",
  priority="urgent"
)
```