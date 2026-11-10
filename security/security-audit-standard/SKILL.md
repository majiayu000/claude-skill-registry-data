---
name: security-audit-standard
description: >
  Security audit methodology and checklist for codebases. Use when performing security
  reviews, auditing a project for vulnerabilities, or hardening an application before
  deployment. Covers secret scanning, input validation, authentication/authorization,
  cryptographic practices, dependency auditing, CSP configuration, rate limiting,
  OWASP Top 10 checks, and audit report format. Derived from production audit work.
---

# Security Audit Standard

Methodology derived from production security audits.

## Audit Process

### Phase 1: Secret Scanning

Scan for hardcoded credentials in tracked source files.

```
Targets:
- API keys, tokens, passwords in source (not .env)
- Webhook URLs with tokens
- Database connection strings
- Private keys, certificates
- obfstr!() usage (Rust): still in binary, just obfuscated
```

Check patterns:
```
grep -rn "sk-" "pk_" "ghp_" "token" "secret" "password" "apikey"
grep -rn "https://discord.com/api/webhooks/"
grep -rn "https://hooks.slack.com/"
grep -rn "mongodb://" "postgresql://" "redis://"
```

Verify `.gitignore` covers: `.env*`, `*.pem`, `*.key`, `credentials*`, `secrets*`, `auth*.json`, `config.json` (if it contains secrets).

### Phase 2: Input Validation

For every endpoint/command that accepts user input:

1. **Where does input enter the system?** (HTTP body, query params, WebSocket messages, IPC commands, CLI args, file uploads)
2. **Is it validated before processing?** (type checking, length limits, format validation)
3. **Is it sanitized before output?** (HTML escaping, SQL parameterization)
4. **Are error messages safe?** (no stack traces, no internal paths, no credential hints)

Checklist:
- [ ] SQL queries use parameterized statements (never string concatenation)
- [ ] HTML output is escaped (no raw user content in templates)
- [ ] File paths are validated (no path traversal `../`)
- [ ] JSON parsing has try/catch (malformed input doesn't crash)
- [ ] Integer inputs have range checks (no overflow/underflow)
- [ ] String inputs have max length limits
- [ ] File uploads validate type, size, and content (not just extension)

### Phase 3: Authentication & Authorization

- [ ] Passwords hashed with bcrypt/argon2 (not MD5/SHA1)
- [ ] JWT tokens have expiration (`exp` claim)
- [ ] JWT secret is strong (>32 bytes, not "secret")
- [ ] Session tokens rotated on privilege change
- [ ] OAuth flows validate `state` parameter (CSRF protection)
- [ ] OAuth flows validate all required response fields
- [ ] API keys transmitted via headers (not query params: logged in access logs)
- [ ] Admin endpoints require authentication + authorization
- [ ] Rate limiting on login/auth endpoints (brute force protection)
- [ ] Account lockout after N failed attempts

### Phase 4: Data Protection

- [ ] Secrets stored in OS keychain / encrypted store (not plain files)
- [ ] Sensitive data not logged (mask tokens, passwords, PII)
- [ ] HTTPS enforced (no mixed content)
- [ ] CORS configured restrictively (not `*` in production)
- [ ] CSP headers set (script-src, connect-src restricted)
- [ ] Cookies: `HttpOnly`, `Secure`, `SameSite` flags set
- [ ] Temp files use unpredictable paths (`tempfile` crate, `mkstemp`)
- [ ] Sensitive data cleared from memory after use

### Phase 5: Dependency Audit

```bash
# Node.js
npm audit
pnpm audit

# Rust
cargo audit
cargo deny check

# Python
pip-audit
safety check

# Go
govulncheck ./...
```

Check for:
- Known CVEs in dependencies
- Outdated dependencies (major versions behind)
- Abandoned packages (no commits in 2+ years)
- Typosquat packages (similar names to popular packages)

### Phase 5b: Supply Chain

| Check | Command / File | Why |
|---|---|---|
| Lockfile committed | `package-lock.json`, `Cargo.lock`, `go.sum`, `Package.resolved` | Pin transitive dep versions |
| GitHub Actions pinned to SHA | `uses: actions/checkout@<sha>` | `@v4` tag can be moved by attacker |
| Install scripts disabled in CI | `npm ci --ignore-scripts` | Prevents postinstall RCE |
| Provenance or signing | `npm publish --provenance`, sigstore for releases | Lets consumers verify origin |
| Allow-list of registries | `.npmrc registry=`, `cargo` index | Blocks dependency confusion |
- Typosquat packages (similar names to popular packages)

### Phase 6: Infrastructure

- [ ] No debug endpoints in production
- [ ] Error pages don't leak stack traces
- [ ] Server headers don't expose technology versions
- [ ] Rate limiting on all public endpoints
- [ ] Process runs as non-root user
- [ ] File permissions are restrictive (600 for secrets, 755 for executables)
- [ ] Firewall rules minimize exposed ports
- [ ] TLS 1.2+ enforced (no SSLv3, TLS 1.0/1.1)
- [ ] Database not accessible from public internet

## OWASP Top 10 Quick Check

| # | Vulnerability | Check |
|---|---|---|
| A01 | Broken Access Control | Every endpoint verifies auth + authz? |
| A02 | Cryptographic Failures | Using strong algorithms? Secrets encrypted at rest? |
| A03 | Injection | All inputs parameterized/escaped? |
| A04 | Insecure Design | Threat model exists? Security requirements documented? |
| A05 | Security Misconfiguration | Default creds removed? Error handling configured? |
| A06 | Vulnerable Components | Dependencies audited? No known CVEs? |
| A07 | Auth Failures | Brute force protected? MFA available? |
| A08 | Data Integrity Failures | Updates verified (checksums)? CI/CD secured? |
| A09 | Logging Failures | Security events logged? Logs don't contain secrets? |
| A10 | SSRF | Server-side requests validated? Internal URLs blocked? |

## Tauri-Specific Security

- [ ] CSP in `tauri.conf.json` restricts `script-src` and `connect-src`
- [ ] IPC commands are enum-constrained (no arbitrary command execution)
- [ ] `dangerous-api` features disabled unless explicitly needed
- [ ] File system access scoped to app directories
- [ ] Shell commands never constructed from user input

## Audit Report Format

```markdown
# Security Audit: [Project Name]
Date: YYYY-MM-DD

## Summary
- Critical: N findings
- High: N findings
- Medium: N findings
- Low: N findings

## Critical Findings

### [CRIT-01] Hardcoded API key in tracked source
- **Location**: `src/config.json:15`
- **Risk**: Key exposure if repo made public or cloned
- **Fix**: Move to .env, add to .gitignore, rotate key
- **Effort**: 5 minutes

## High Findings
...

## Recommendations
1. [Priority-ordered action items]
```

Severity levels:
- **Critical**: Immediate exploitation possible, data breach risk
- **High**: Exploitable with some effort, significant impact
- **Medium**: Requires specific conditions, moderate impact
- **Low**: Minor risk, defense-in-depth improvement
