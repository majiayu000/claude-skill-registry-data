---
name: security-audit
description: "Run a full security audit: OWASP Top 10, secrets detection, input validation, auth, dependency vulnerabilities."
argument-hint: "[file-or-path]"
allowed-tools: Read Write Edit Bash Grep Glob
model: gpt-5.3-codex
---

# /security-audit — Security Scan

Audit: `$ARGUMENTS` (or full project if none). See `agents/security-reviewer.md` and `patterns/security-rules.md`.

1. **Dependency scan** — `npm audit --audit-level=high`
2. **Secrets scan** — Grep for `sk-`, `api_key`, `password`, `secret`, `token`, `Bearer`. Check `.gitignore`.
3. **OWASP Top 10** — Injection, auth, XSS, access control, misconfiguration, deserialization, logging
4. **Code patterns** — Flag critical patterns from security-reviewer agent
5. **Report** — CRITICAL/HIGH/MEDIUM counts + PASS/FAIL verdict
