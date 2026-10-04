---
name: go-security
description: "Security best practices and vulnerability prevention for Golang. Covers injection prevention, cryptography, and secure configuration."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 04:50:00 GMT
---

## Core Security Principles

1. **Defense in Depth** — Protect at multiple layers; validate all inputs.
2. **Trust Boundaries** — Identify where untrusted data enters (HTTP, Files, DB).
3. **Parameterized Queries** — Never concatenate user input into SQL.
4. **Secure Defaults** — Use the Go standard library's secure defaults.
5. **Fail Closed** — Ensure that any failure results in a secure state (e.g., denying access).

## Common Vulnerabilities and Defenses

| Vulnerability | Defense | Standard Library Solution |
| --- | --- | --- |
| **SQL Injection** | Use placeholders | `db.QueryContext(ctx, "SELECT ... WHERE id = $1", id)` |
| **Command Injection** | Separate arguments | `exec.Command("ls", "-l", path)` (no shell) |
| **XSS** | Auto-escaping | Use `html/template` instead of `text/template` |
| **Path Traversal** | Sanitize paths | `filepath.Clean(path)`, use `os.Root` (Go 1.24+) |
| **Timing Attacks** | Constant-time compare | `crypto/subtle.ConstantTimeCompare` |
| **Weak Crypto** | Use vetted algorithms | `crypto/aes` GCM, `crypto/rand` for tokens |

## Sensitive Data Handling

- **Passwords**: Use Argon2id or bcrypt (never MD5/SHA1).
- **Secrets**: Use environment variables or secret managers. Never hardcode.
- **Logging**: Sanitize PII (Personal Identifiable Information) before logging.
- **Errors**: Return generic messages to users; log technical details internally.

## Security Tools

```bash
# Run race detector during tests
go test -race ./...

# Check for known vulnerabilities in dependencies
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./...

# Use gosec for static security analysis
go install github.com/securego/gosec/v2/cmd/gosec@latest
gosec ./...
```

## Anti-patterns

- ❌ **`math/rand` for security tokens** — Output is predictable. Use `crypto/rand`.
- ❌ **`exec.Command("bash", "-c", cmd)`** — Vulnerable to shell injection.
- ❌ **Hardcoded credentials** in source code.
- ❌ **Comparing secrets with `==`** — Vulnerable to timing attacks.
- ❌ **Ignoring `-race` findings** — Race conditions can lead to security bypasses.
- ❌ **MD5/SHA1 for sensitive data** — Collisions and fast brute-forcing make them unsafe.
