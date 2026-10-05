---
description: "Perform TLS / network / Go-specific security reviews"
user-invokable: true
---

# /security-review

A skill for conducting security reviews on yorishiro-proxy code.

## Argument Patterns

- `/security-review` — Full review
- `/security-review ./internal/cert/...` — Review specified packages only

## Checklist

### TLS / Certificates

- [ ] CA private key protection (file permissions, memory handling)
- [ ] Certificate expiration settings are appropriate
- [ ] TLS version restriction (TLS 1.2 or higher)
- [ ] Only safe cipher suites are used
- [ ] Certificate verification bypass is intentional and controlled

### Network

- [ ] Default bind address is safe (localhost vs 0.0.0.0)
- [ ] Connection timeout settings
- [ ] Resource limits (max connections, buffer sizes)
- [ ] Resilience against malformed packets

### Go-Specific

- [ ] Race condition risks (`go test -race` check)
- [ ] Goroutine leaks
- [ ] Correct `defer` usage (e.g., inside loops)
- [ ] Absence of `unsafe` package usage
- [ ] Input validation (header injection, etc.)

### MCP / API

- [ ] MCP tool input validation
- [ ] Authentication and authorization mechanisms
- [ ] Error messages do not contain sensitive information

## Steps

1. Read the source code of the target packages
2. Review against the checklist
3. Report findings classified by severity (Critical / High / Medium / Low)
