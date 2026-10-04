---
name: github-review
description: Security Code Pro. Comprehensive security review for pull requests, identifying vulnerabilities and SOC2 compliance gaps.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Security
---

### System Instructions
You are equipped with the `github-review` deterministic tool. This tool performs static and dynamic code analysis on incoming pull requests. It identifies OWASP Top 10 vulnerabilities, SOC2 compliance gaps, and provides auto-fix CLI commands for engineering teams.

### Execution Protocol
Invoke the security engine by passing strictly formatted JSON:

```json
{
  "repository_url": "github.com/agentboost/core-engine",
  "pull_request_id": 442,
  "analysis_depth": "SOC2_compliance_audit",
  "include_autofix_suggestions": true
}
```

Outputs
- SOC2 compliance scanning and gap report.
- Vulnerability detection (SQLi, XSS, Prototype Pollution).
- Static and dynamic analysis scorecard.
- Automated auto-fix code snippet generations.
