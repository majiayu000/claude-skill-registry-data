---
name: purple-team-report
description: >
  Synthesize red team findings and blue team fixes into a structured security report.
  Use when the user wants a consolidated security report after red-team-check and
  blue-team-fix have been run, or when presenting security findings to stakeholders.
  Produces: executive summary, finding table with evidence, fix status, and open items.
origin: yamtam
version: 1.0.0
compatibility: >
  Expects red-team-check output and blue-team-fix output as input.
  Report is text-based (Markdown). Does not write to external systems.
---

<!-- Concept inspired by Strix (Apache 2.0) — security report synthesis pattern.
     All content written original for YAMTAM. No code ported. -->

## When to Use

- After red-team-check AND blue-team-fix have completed for a session
- When user asks for a security report, security summary, or pentest report
- Before a production release that had security review as a requirement
- When sharing security status with a team or stakeholder

Do NOT use:
- Without red-team-check output — the report is only as good as the scan input
- As a substitute for showing actual evidence — evidence must be present in the report

## How It Works

### Step 1 — Collect Inputs

Gather from the current session:
- Full finding list from red-team-check (including category coverage table)
- Fix status from blue-team-fix (fixed / proposed / skipped per finding)
- Scan mode used (quick / targeted / deep)
- Target confirmed via security-scope-gate

If any input is missing, note it explicitly:
```
⚠ INPUT INCOMPLETE: blue-team-fix output not found.
  Report will show findings but fix status will be UNKNOWN for all items.
  Run blue-team-fix first for complete report.
```

### Step 2 — Build the Report

Output the report in this exact structure:

---

```markdown
# Security Report — [Target Name]

**Date:** YYYY-MM-DD
**Scan Mode:** quick / targeted / deep
**Scope Confirmed:** yes (logged to .claude/state/security-scope-confirmations.log)
**Scanned by:** red-team-check v1.0.0 + blue-team-fix v1.0.0

---

## Executive Summary

[2–4 sentences. Non-technical. Cover: what was scanned, how many findings,
overall risk level, how many are fixed. Example:]

A [mode] security scan of [target] identified [N] vulnerabilities across
[M] OWASP categories. [X] findings are CRITICAL or HIGH severity.
[Y] findings have been fixed with tests added. [Z] remain open.
Overall risk: HIGH / MEDIUM / LOW.

---

## Category Coverage

| OWASP Category | Status | Findings |
|----------------|--------|---------|
| A01 Broken Access Control | SCANNED | N |
| A02 Cryptographic Failures | SCANNED | N |
| A03 Injection | SCANNED | N |
| A04 Insecure Design | SCANNED | N |
| A05 Security Misconfiguration | SCANNED | N |
| A06 Vulnerable Components | SCANNED / SKIPPED | N |
| A07 Auth Failures | SCANNED | N |
| A08 Data Integrity Failures | SCANNED | N |
| A09 Logging Failures | SCANNED | N |
| A10 SSRF | SCANNED | N |

---

## Finding Table

| # | Severity | Category | Title | Fix Status | Evidence |
|---|----------|----------|-------|-----------|---------|
| 1 | CRITICAL | A02 | Hardcoded DB password | FIXED | diff shown in session |
| 2 | HIGH | A01 | IDOR on /api/users/:id | FIXED | diff shown in session |
| 3 | MEDIUM | A05 | Debug mode in prod config | OPEN | test not yet written |
| 4 | LOW | A09 | Auth failures not logged | OPEN — backlog | — |

Evidence column MUST reference where evidence was shown.
MUST NOT be empty for FIXED items.

---

## Open Items

Items that are not yet fixed:

| # | Severity | Title | Reason not fixed | Recommended action |
|---|----------|-------|-----------------|-------------------|
| 3 | MEDIUM | Debug mode in prod config | Skipped by user | Fix before next deploy |
| 4 | LOW | Auth failures not logged | Deferred to backlog | Create tracking issue |

---

## Fix Evidence Summary

For each FIXED item, confirm evidence exists:

**Finding #1 — Hardcoded DB password (CRITICAL)**
- Fix: moved to environment variable
- Diff: shown in blue-team-fix output above
- Test: test/security/test_secrets.py — assertion: `assert "password" not in source_code`
- Status: FIXED — evidence present

**Finding #2 — IDOR on /api/users/:id (HIGH)**
- Fix: added ownership check before returning resource
- Diff: shown in blue-team-fix output above
- Test: test/api/test_users_auth.py — assertion: `assert response.status_code == 403`
- Status: FIXED — evidence present

---

## Recommendations

1. [Specific action from highest severity open item]
2. [Second recommendation]
3. Add `red-team-check` to CI pipeline to catch regressions (see docs/security-scan-modes.md)
```

---

### Step 3 — Anti-Fake-Pass Checklist

Before outputting the report, verify:

- [ ] Category coverage table is complete (all 10 categories listed)
- [ ] Every FIXED item has an evidence reference
- [ ] Evidence column is not empty for any FIXED item
- [ ] Open items table includes reason and recommended action
- [ ] Executive summary numbers match the finding table counts

## Gotchas

- If blue-team-fix was not run, mark all fix statuses as UNKNOWN — do not guess
- Evidence column must reference where in the session the evidence appeared — "see above" is acceptable if it's clear; "shown earlier" without context is not
- Do not include raw credentials, tokens, or PII in the report even if found in scan
- Severity counts in executive summary must match the finding table exactly

## Anti-Fake-Pass Rules

Before claiming the report is complete, you MUST show:
- [ ] Category coverage table with status for all 10 OWASP categories
- [ ] Finding table with evidence column populated for FIXED items
- [ ] Open items table (even if empty — show "No open items")
- [ ] Executive summary numbers match finding table

MUST NOT say "report complete" if evidence column has empty cells for FIXED items.
MUST NOT say "all fixed" if open items table has any rows.
MUST NOT omit the category coverage table even for quick scans.
