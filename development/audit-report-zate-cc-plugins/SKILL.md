---
name: audit-report
description: Template and formatting guidelines for security audit reports. Provides consistent structure for findings, severity classification, ASVS mapping, and remediation recommendations.
---

# Audit Report Template

Standardized format for security audit reports to ensure consistency, completeness, and actionability.

## When to Use This Skill

- **Generating audit reports** - After completing security audits
- **Formatting findings** - When documenting individual security issues
- **Writing recommendations** - When providing remediation guidance
- **Comparing audits** - Consistent format enables tracking over time

## When NOT to Use This Skill

- **Quick bug reports** - Use simpler format for individual issues
- **Non-security documentation** - Use appropriate templates for other docs
- **Real-time alerts** - Use concise format for live notifications

---

## Report Structure

### Full Report Template

```markdown
# Security Audit Report

**Project**: [Project Name]
**Date**: [YYYY-MM-DD]
**Auditor**: Claude Security Plugin
**Version**: [Plugin Version]

---

## Executive Summary

### Overview
[2-3 sentence summary of the audit scope and overall findings]

### Risk Level
**Overall Risk**: [Critical | High | Medium | Low | Minimal]

### Key Metrics
| Metric | Value |
|--------|-------|
| Total Findings | [N] |
| Critical | [N] |
| High | [N] |
| Medium | [N] |
| Low | [N] |
| Info | [N] |

### Top Concerns
1. [Most critical finding - one line summary]
2. [Second most critical]
3. [Third most critical]

---

## Audit Scope

### Target
- **Project Type**: [web-api | web-app | cli | library | mobile]
- **Languages**: [List]
- **Frameworks**: [List]

### Coverage
- **ASVS Level**: [L1 | L2 | L3]
- **Chapters Audited**: [List of V1-V17]
- **Auditors Run**: [List of domain auditors]

### Exclusions
[Any directories, files, or areas explicitly excluded]

---

## Findings

### Critical Findings

#### [FINDING-001] [Title]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **ASVS** | V[X].[Y].[Z] |
| **CWE** | CWE-[ID] |
| **Location** | `path/to/file.ext:line` |
| **Status** | Open |

**Description**
[Clear explanation of the vulnerability]

**Evidence**
```[language]
[Code snippet showing the issue]
```

**Impact**
[What could happen if exploited]

**Remediation**
[Specific steps to fix]

```[language]
[Fixed code example]
```

**References**
- [ASVS Link]
- [CWE Link]
- [Additional resources]

---

[Repeat for each finding, grouped by severity]

---

## Recommendations

### Immediate Actions (Critical/High)
1. [ ] [Action item with specific file/code reference]
2. [ ] [Action item]

### Short-term Improvements (Medium)
1. [ ] [Action item]
2. [ ] [Action item]

### Long-term Enhancements (Low/Best Practices)
1. [ ] [Action item]
2. [ ] [Action item]

---

## Appendix

### A. ASVS Coverage Matrix

| Chapter | Requirements | Checked | Passed | Failed | N/A |
|---------|--------------|---------|--------|--------|-----|
| V1 | 28 | [N] | [N] | [N] | [N] |
| V2 | 15 | [N] | [N] | [N] | [N] |
[... continue for all chapters ...]

### B. Methodology

**Approach**: Automated static analysis with manual verification

**Limitations**:
- [Any known limitations of the audit]
- [Areas requiring manual testing]

### C. Tool Information

- **Plugin**: Claude Code Security Plugin v[X.Y.Z]
- **ASVS Version**: 5.0
- **Audit Date**: [Date]
- **Duration**: [Time]
```

---

## Severity Classification

### Criteria

| Severity | CVSS Range | Criteria |
|----------|------------|----------|
| **Critical** | 9.0-10.0 | Remote code execution, authentication bypass, complete data breach |
| **High** | 7.0-8.9 | Privilege escalation, significant data exposure, account takeover |
| **Medium** | 4.0-6.9 | Information disclosure, business logic bypass, limited data exposure |
| **Low** | 0.1-3.9 | Best practice violations, theoretical issues, minor information leak |
| **Info** | 0.0 | Observations, recommendations, hardening suggestions |

### Severity Decision Tree

```
Is it exploitable without authentication?
├── Yes → Is it remotely exploitable?
│   ├── Yes → Can it lead to RCE or full compromise?
│   │   ├── Yes → CRITICAL
│   │   └── No → HIGH
│   └── No → Can it lead to data breach?
│       ├── Yes → HIGH
│       └── No → MEDIUM
└── No → Can authenticated users escalate privileges?
    ├── Yes → HIGH
    └── No → Does it expose sensitive data?
        ├── Yes → MEDIUM
        └── No → LOW or INFO
```

---

## Finding Format

### Individual Finding Template

```markdown
#### [ID] [Short descriptive title]

| Attribute | Value |
|-----------|-------|
| **Severity** | [Critical/High/Medium/Low/Info] |
| **ASVS** | V[chapter].[section].[requirement] |
| **CWE** | CWE-[id] ([name]) |
| **OWASP** | [Top 10 category if applicable] |
| **Location** | `file:line` |
| **Confidence** | [High/Medium/Low] |
| **Status** | [Open/Verified/Fixed/False Positive] |

**Description**
[What is the issue? Be specific and technical.]

**Evidence**
[Code snippet, configuration, or proof]

**Impact**
[What could an attacker do? What's the business impact?]

**Remediation**
[How to fix it. Include code examples when possible.]

**References**
[Links to relevant documentation, CVEs, or standards]
```

### Minimal Finding Format (for summaries)

```markdown
- **[Severity]** [Title] - `file:line` (ASVS V[X].[Y].[Z])
```

---

## Common Finding Categories

### By ASVS Chapter

| Chapter | Common Finding Types |
|---------|---------------------|
| V1 | SQL injection, command injection, XSS, deserialization |
| V2 | Missing validation, business logic bypass, mass assignment |
| V3 | Missing CSP, insecure cookies, missing HSTS |
| V4 | API rate limiting, GraphQL introspection, content-type issues |
| V5 | Unrestricted upload, path traversal, insecure storage |
| V6 | Weak passwords, insecure hashing, no lockout |
| V7 | Predictable sessions, no timeout, insecure cookies |
| V8 | IDOR, missing access control, privilege escalation |
| V9 | JWT algorithm confusion, no expiration, weak secrets |
| V10 | Missing PKCE, open redirect, token leakage |
| V11 | Weak crypto, hardcoded keys, insecure random |
| V12 | TLS misconfiguration, certificate issues |
| V13 | Debug enabled, secrets in code, outdated dependencies |
| V14 | Unencrypted PII, data retention issues |
| V15 | Buffer overflow, dependency vulnerabilities |
| V16 | Missing logging, PII in logs, verbose errors |
| V17 | WebRTC security issues |

---

## JSON Output Format

For machine-readable output alongside the markdown report:

```json
{
  "audit": {
    "project": "project-name",
    "date": "2024-12-15T10:30:00Z",
    "duration_seconds": 120,
    "plugin_version": "1.0.0",
    "asvs_version": "5.0"
  },
  "scope": {
    "level": "L2",
    "chapters": ["V1", "V2", "V4", "V6", "V7", "V8"],
    "auditors": ["encoding-auditor", "validation-auditor", "api-auditor"]
  },
  "summary": {
    "total": 15,
    "critical": 1,
    "high": 3,
    "medium": 5,
    "low": 4,
    "info": 2,
    "risk_level": "high"
  },
  "findings": [
    {
      "id": "FINDING-001",
      "title": "SQL Injection in User Query",
      "severity": "critical",
      "asvs": "V1.2.1",
      "cwe": "CWE-89",
      "location": {
        "file": "src/api/users.js",
        "line": 42,
        "column": 15
      },
      "confidence": "high",
      "description": "...",
      "evidence": "...",
      "impact": "...",
      "remediation": "...",
      "references": ["..."]
    }
  ],
  "coverage": {
    "V1": {"total": 28, "checked": 28, "passed": 25, "failed": 2, "na": 1}
  }
}
```

---

## Report Generation Guidelines

### Writing Effective Descriptions

**Good**:
> The `getUserById` function at line 42 constructs a SQL query using string concatenation with user-supplied input (`userId`), allowing an attacker to inject arbitrary SQL commands.

**Bad**:
> SQL injection vulnerability found.

### Writing Actionable Remediation

**Good**:
> Replace the string concatenation with parameterized queries:
> ```javascript
> // Before (vulnerable)
> const query = `SELECT * FROM users WHERE id = '${userId}'`;
>
> // After (secure)
> const query = 'SELECT * FROM users WHERE id = $1';
> const result = await db.query(query, [userId]);
> ```

**Bad**:
> Fix the SQL injection.

### Evidence Best Practices

1. Include relevant code snippets (not entire files)
2. Highlight the vulnerable line or pattern
3. Include enough context to understand the issue
4. Sanitize any actual credentials or sensitive data

---

## See Also

- `Skill: asvs-requirements` - ASVS chapter details
- `Skill: remediation-library` - Fix patterns (future)
- `Agent: audit-orchestrator` - Report generation workflow
