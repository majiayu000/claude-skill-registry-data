---
skill_id: studio-operations
name: Studio Operations & Agency Ops
description: "Agency and studio operations — operations, analytics, finance, infrastructure, support, reporting, dashboards, KPIs, budget. Multi-office domain where CTO, CEO and CSO agents converge."
version: 1.0.0
category: studio-operations
office: COO
lead_agent: planner
triggers:
  - operations
  - studio
  - analytics
  - finance
  - infrastructure
  - support
  - reporting
  - dashboard
  - KPI
  - budget
  - customer success
  - partnership
collaborates_with:
  - analytics-reporter
  - financial-modeler
  - infrastructure-maintainer
  - legal-compliance-checker
  - compliance
  - security-analyst
  - enterprise-architect
---

# Studio Operations & Agency Ops -- Domain Dispatcher

> Office: COO | Lead: planner
> Sub-skills: 6 | Frameworks: Value Stream Mapping, ITIL, FinOps

## Purpose

The multi-office operational domain -- agents from CTO, CEO, and CSO offices converge here for agency-wide operational tasks. This skill covers business operations, analytics reporting, financial tracking, infrastructure maintenance, legal compliance, and customer support. Maxim applies behavioral science to operational efficiency, proactively routes to the right specialist, and ensures all financial and legal outputs pass through appropriate governance gates.

## Sub-Skill Routing

| Task Signal | Routes To | SKILL.md Path |
|---|---|---|
| analytics dashboards, KPI tracking, data insights, anomaly detection | analytics-reporter | analytics-reporter/SKILL.md |
| budget tracking, expense management, financial forecasting | finance-tracker | finance-tracker/SKILL.md |
| system uptime, incident management, IaC maintenance | infrastructure-maintainer | infrastructure-maintainer/SKILL.md |
| contract review, regulatory affairs, terms of service | legal-compliance-checker | legal-compliance-checker/SKILL.md |
| studio workflow, project coordination, agency production | studio-producer | studio-producer/SKILL.md |
| tier-1 support, support documentation, escalation routing | support-responder | support-responder/SKILL.md |

## Activation

This domain activates when:
- User invokes `/mxm-coo`
- Task contains keywords: operations, studio, analytics, finance, infrastructure, support, reporting, dashboard, KPI, budget, customer success, partnership, agency operations
- Executive router detects operational, financial, or infrastructure signals
- Other Maxim skills proactively loop here: engineering (infrastructure ops), compliance (legal and financial compliance), security (infrastructure security)

## Behavioral Layer

- Confidence: 🟢 HIGH (Maxim skill + external knowledge merged)
- Compliance: reads project-manifest.json before decisions
- Handoff: writes .mxm-skills/agents-handoff.md on completion
- Ethics gate: `ethics_required: true` on `legal-compliance-checker` -- contract and regulatory review outputs require human sign-off before execution
- Frameworks: Value Stream Mapping, ITIL (service management), FinOps (cloud financial management), OKR (operational goal tracking)

## External Sources

- Primary: community-packs/claude-skills-library/engineering-team/google-workspace-cli (workspace automation, ops tooling)
- Secondary: community-packs/claude-skills-library/documentation/ (documentation standards, knowledge management)
- Secondary: community-packs/claude-skills-library/orchestration/ (multi-agent operational workflow patterns)
- Secondary: community-packs/claude-skills-library/finance/ (financial modeling templates, budget frameworks)
- Conflict resolution: Maxim ALWAYS WINS

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
