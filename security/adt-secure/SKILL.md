---
name: secure
description: Shortcut for security review on current change set. Runs layered checks (secret-scan, dep-audit, semgrep, OWASP patterns, prompt-injection review).
triggers:
  - "secure this"
  - "security check"
  - "scan for vulns"
  - "run security review"
---

# Secure

Shortcut for security review on current change set. Runs a layered check: secret-scan (trufflehog), dep-audit, semgrep, OWASP top-10 pattern sweep, and prompt-injection review if agent-touching code.

## Purpose

Gate changes for security before shipping. Thin wrapper around existing `security-review` / `security-audit` skills, orchestrated into a single invocation.

## What Gets Scanned

| Layer | Tool | Detects |
|-------|------|---------|
| Secrets | trufflehog | API keys, credentials, private keys |
| Dependencies | npm audit, pip audit | Known vulns in transitive deps |
| Code patterns | semgrep | OWASP Top 10, injection flaws, unsafe DOM |
| Prompt injection | Custom rules | Template injection, prompt stuffing, jailbreak patterns |

## Invocation

```bash
secure                           # Scan staged changes
secure --staged                  # Explicit staged
secure --branch <branch>         # Scan diff vs main
secure --file <path>             # Single file
secure --fix                     # Attempt auto-fix (secrets rotate, deps upgrade)
```

## Example Output

```
Running secure check...

[OK]  Secrets: 0 findings
[OK]  Dependencies: 1 high vuln detected in lodash (fixed in v4.17.21, yours: v4.17.20)
[WARN] Semgrep: 2 findings
      - CWE-79 (XSS): unsafe innerHTML in auth-form.tsx:42
      - CWE-89 (SQL Injection): dynamic query in db-service.ts:105
[OK]  Prompt injection: 0 findings

Summary: 2 warnings, 0 errors
Next: Fix findings or run `secure --fix` for suggestions
```

## Interpretation Guide

| Severity | Action |
|----------|--------|
| **Error** | Block merge; fix before shipping |
| **High** | Fix or document exception with JIRA ticket |
| **Medium** | Plan fix; merge with caution |
| **Low** | Log for backlog; merge OK |

## AI Agent Code Special Rules

If changes touch `src/agents/`, `packages/core/kit/core/agents/`, or prompt-building logic, ALWAYS run extra prompt-injection scan:

```bash
secure --agents-mode
```

Detects:
- User-controlled input fed directly to LLM prompts
- Unescaped template variables in agent instructions
- Jailbreak patterns in example payloads

## References

- Full security audit: `security-audit` skill
- Best practices: `packages/core/best-practices/security.md`
- Prompt defense: `packages/core/patterns/prompt-injection-defense.md`
- OWASP Top 10: [owasp.org](https://owasp.org)
