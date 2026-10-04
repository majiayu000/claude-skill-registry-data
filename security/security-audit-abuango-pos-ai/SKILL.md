---
name: security-audit
description: Perform security audits on codebases for projects. Use when checking for vulnerabilities, security review, or when user mentions "security audit", "security review", "check security", "vulnerability scan", or "security assessment".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Security Audit

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Perform security audits following OWASP Top 10 methodology.

## Process

1. **Identify Target**
   - Get workspace path from project.yaml
   - Understand technology stack
   - Identify sensitive areas (auth, payments, data)

2. **Systematic Review**
   - Follow OWASP Top 10: See [references/owasp-top10.md](references/owasp-top10.md)
   - Check for common vulnerability patterns
   - Review security configurations

3. **Document Findings**
   - Save to: `teams/{team}/projects/{project}/reviews/security-audit-{date}.md`

## Quick OWASP Reference

| ID | Category | Key Check |
|----|----------|-----------|
| A01 | Broken Access Control | Auth on all endpoints |
| A02 | Cryptographic Failures | No hardcoded secrets |
| A03 | Injection | Parameterized queries |
| A04 | Insecure Design | Rate limiting |
| A05 | Security Misconfiguration | Debug mode off |
| A06 | Vulnerable Components | `npm audit` / `pip-audit` |
| A07 | Authentication Failures | Strong passwords, lockout |
| A08 | Data Integrity | Safe serialization |
| A09 | Logging & Monitoring | Security events logged |
| A10 | SSRF | URL validation |

For detailed checklists and search patterns: [references/owasp-top10.md](references/owasp-top10.md)

## Critical Search Commands

```bash
# Hardcoded secrets
grep -rE "(password|secret|key|token)\s*=\s*['\"][^'\"]+['\"]"

# SQL injection risks
grep -rE "whereRaw|selectRaw|DB::raw|execute\(" --include="*.php" --include="*.py"

# Command injection
grep -rE "exec\(|system\(|shell_exec"

# XSS risks
grep -rE "innerHTML|v-html|dangerouslySetInnerHTML"
```

## Report Template

```markdown
# Security Audit Report

**Project:** {project-name}
**Date:** {YYYY-MM-DD}
**Risk Level:** CRITICAL / HIGH / MEDIUM / LOW

## Summary
- {X} Critical, {Y} High, {Z} Medium, {N} Low findings

## Critical Findings

### Finding 1: {Title}
- **Severity:** CRITICAL
- **Location:** {file:line}
- **Description:** {What's wrong}
- **Impact:** {What could happen}
- **Fix:** {How to fix}

## OWASP Compliance

| Category | Status |
|----------|--------|
| A01-A10  | PASS/FAIL |

## Recommendations

### Immediate (Critical/High)
1. {Action}

### Short-term (Medium)
1. {Action}
```

## Severity Levels

| Severity | Response |
|----------|----------|
| CRITICAL | Immediate |
| HIGH | 24-48 hours |
| MEDIUM | 1 week |
| LOW | Next release |

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
