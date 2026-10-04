---
name: audit-and-governance
description: >
  Ensure compliance with organizational policies and regulatory standards,
  then generate structured reports and dashboards. Covers license auditing,
  data handling regulations, security standard mapping, and structured
  reporting with actionable recommendations.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
triggers:
  - context: "compliance review"
  - context: "generating reports"
  - context: "quality dashboard"
  - context: "regulatory requirements"
  - command: "/audit"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 2
---

## Overview

Governance has two parts: verify compliance with standards (audit), then communicate findings clearly (reporting). This skill covers both — from license checks and data regulations to generating structured reports with severity-classified findings.

## When to Use

- Before releasing software (license compliance check)
- When handling personal data (GDPR, CCPA, HIPAA)
- After a development session (session report)
- During `/audit` invocation

## Process

### 1. License Compliance

```bash
npx license-checker --production --onlyAllow "MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause;ISC"
```

- Verify all production dependencies use compatible licenses
- Flag GPL dependencies in proprietary projects (viral license)
- Document any license exceptions in `docs/adrs/`

### 2. Data Handling

If the application handles personal data:
- [ ] Data collection minimized (collect only what's needed)
- [ ] User consent obtained before collection
- [ ] Data retention policy defined and deletion mechanism exists
- [ ] Data encrypted in transit and at rest
- [ ] Access logs maintained

### 3. Security Standards Mapping

- **OWASP Top 10** → `codehands:security-and-hardening`
- **OWASP LLM Top 10** → `references/owasp-llm-top10.md`
- **SOC2** → Access controls, audit logs, change management
- **ISO 27001** → Information security management

### 4. Generate Report

Collect data then output in chosen format (Markdown default, JSON for CI, HTML for dashboards):

```markdown
# CodeHands Audit Report — YYYY-MM-DD

## Session Summary
- Skills activated: [list] | Tasks: [count] | Human decisions: [count]

## Code Quality
- Tests: [passed]/[total] | Coverage: [%] | Build: [pass/fail]

## Security
- Vulnerabilities: [critical]/[high]/[medium]/[low]
- Secrets scan: [clean/findings]

## Compliance
- License check: [pass/fail] | Data handling: [compliant/needs review]

## Recommendations
- [Prioritized action items]
```

Save to `.codehands/audit/YYYY-MM-DD-report.md`.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Compliance is just bureaucracy" | Compliance requirements exist because of real incidents. Non-compliance has legal and financial consequences. |
| "Nobody reads audit reports" | Reports are read during incidents, compliance reviews, and retrospectives. They're insurance. |
| "Our project is too small for compliance" | License violations and data handling issues affect projects of all sizes. |

## Red Flags

- No license check on dependencies
- Personal data collected without documented purpose
- No audit trail for sensitive operations
- Session ending without recording outcomes

## Verification

- [ ] License compliance verified (no incompatible licenses)
- [ ] Data handling meets applicable regulations
- [ ] Report generated with all applicable sections
- [ ] Report saved to `.codehands/audit/`
- [ ] Recommendations actionable and prioritized

## See Also

- `codehands:security-and-hardening` — Code-level security
- `codehands:agent-security` — Agent behavior compliance
- `codehands:verification-before-completion` — Quality data source
