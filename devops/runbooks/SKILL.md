---
name: runbooks
description: |
  Pre-built scenario configurations for common multi-agent workflows.
  Quick-start templates for MVPs, features, campaigns, incidents, and audits.

  Triggers: runbook, playbook, scenario, launch, mvp, incident response,
  marketing campaign, security audit, feature build, startup.
---

# Runbooks — Pre-Built Scenarios

## Startup MVP (4-6 weeks, Sprint mode)

```
Activate enterprise-orchestrator in Sprint mode.

Team:
- PM: product-manager (spec + sprint planning)
- Design: ui-designer (design system + components)
- Engineering: fullstack-engineer or backend-engineer + frontend-engineer
- QA: qa-engineer (task-level) + reality-checker (final gate)
- Infra: devops-engineer (CI/CD + deploy)

Pipeline:
1. product-manager creates task list from spec
2. ui-designer creates design tokens + component sketches
3. [Dev ↔ QA loop] for each task (max 3 retries per task)
4. reality-checker final integration check
5. devops-engineer deploys to staging
```

## Enterprise Feature (2-4 weeks, Sprint mode)

```
Activate enterprise-orchestrator in Sprint mode.

Team:
- PM: product-manager (requirements)
- Arch: solutions-architect (design review)
- Dev: backend-engineer + frontend-engineer
- Security: security-engineer (review)
- QA: qa-engineer + reality-checker
- Infra: devops-engineer (feature flags + deploy)

Pipeline:
1. solutions-architect reviews architecture impact
2. security-engineer reviews auth/data implications
3. [Dev ↔ QA loop] for each task
4. security-engineer final security review
5. reality-checker final integration
6. devops-engineer deploys behind feature flag
```

## Marketing Campaign (1-2 weeks, Micro mode)

```
Activate enterprise-orchestrator in Micro mode.

Team:
- Lead: growth-marketer (strategy + channels)
- Content: content-marketer (copy + blog)
- Social: social-media-manager (distribution)
- Design: graphic-designer (assets)
- Analytics: data-analyst (tracking + reporting)

Pipeline:
1. growth-marketer defines campaign strategy + channels
2. content-marketer creates copy, graphic-designer creates assets
3. brand-marketer reviews for brand consistency
4. social-media-manager schedules distribution
5. data-analyst sets up tracking and reports weekly
```

## Incident Response (hours, Micro mode)

```
Activate enterprise-orchestrator in Micro mode — INCIDENT.

Severity: [P0/P1/P2]
Team:
- Lead: sre (incident commander)
- Debug: backend-engineer or frontend-engineer (root cause)
- Infra: devops-engineer (rollback/mitigation)
- Comms: communications-specialist (stakeholder updates)

Pipeline:
1. sre assesses impact and declares severity
2. devops-engineer checks for recent deploys (rollback candidate?)
3. backend/frontend-engineer investigates root cause
4. Fix → qa-engineer validates → devops-engineer deploys hotfix
5. sre writes post-mortem with timeline and action items
6. communications-specialist sends stakeholder update

MTTR target: P0 < 30 min, P1 < 2 hours, P2 < 1 day
```

## Security Audit (3-5 days, Micro mode)

```
Activate enterprise-orchestrator in Micro mode.

Team:
- Lead: security-auditor (assessment + report)
- Code: security-engineer (code review)
- Infra: devops-engineer (infrastructure review)
- Legal: compliance-officer (regulatory check)

Pipeline:
1. security-auditor defines scope and creates threat model
2. security-engineer reviews code (OWASP Top 10)
3. devops-engineer reviews infrastructure (secrets, access, configs)
4. compliance-officer checks regulatory requirements
5. security-auditor compiles final report with severity ratings
6. engineering-orchestrator assigns fixes by severity
```

## SOC2 Compliance (4-8 weeks, Full mode)

```
Activate enterprise-orchestrator in Full mode.

Cross-functional team:
- compliance-officer (requirements matrix)
- security-engineer (technical controls)
- devops-engineer (infrastructure hardening)
- technical-writer (policy documentation)
- legal-counsel (legal review)

Pipeline:
Phase 1: compliance-officer maps SOC2 requirements to current state
Phase 2: security-engineer + devops-engineer implement controls
Phase 3: technical-writer documents policies and procedures
Phase 4: compliance-officer validates all controls
Phase 5: legal-counsel reviews documentation
Phase 6: reality-checker final audit
```
