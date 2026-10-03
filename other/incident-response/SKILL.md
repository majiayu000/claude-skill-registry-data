---
name: incident-response
description: >
  Use when detecting, responding to, or recovering from system failures, outages,
  security breaches, or critical errors. This skill provides a structured incident
  response process for any type of failure, ensuring consistent handling, communication,
  and post-incident learning.
---

# Incident Response

## Overview
This skill defines how to respond to incidents (failures, outages, errors, breaches) in a structured way. Consistent incident response minimizes impact, ensures proper communication, and captures learning to prevent recurrence.

## When to Use
- When detecting a system failure, outage, or degraded performance
- When discovering a security breach or unauthorized access
- When encountering a critical error affecting users or deliverables
- When a deployment or change causes unexpected failures
- When receiving reports of issues from users, agents, or monitoring systems
- **Don't use when:** Bug is minor, non-urgent, or part of normal testing workflow

## Core Procedures

### Step 1: Detect and Classify
Determine incident severity:

| Severity | Description | Response Time | Examples |
|----------|-------------|---------------|---------|
| SEV-1 | Complete system outage, data breach | IMMEDIATE | Production down, credentials leaked |
| SEV-2 | Major feature unavailable | 15 minutes | Critical API failure, database locked |
| SEV-3 | Partial degradation, workaround exists | 1 hour | Slow performance, non-critical bug |
| SEV-4 | Minor issue, cosmetic or inconvenience | 4 hours | UI glitch, minor typo in documentation |

### Step 2: Contain
1. **Isolate** the affected system/component if possible
2. **Stop** any ongoing harm (disable failing processes, revoke compromised credentials)
3. **Preserve** evidence for investigation (logs, state, artifacts)
4. **Communicate** initial status to stakeholders (CEO, monitoring team)

### Step 3: Diagnose
1. Identify root cause using systematic-debugging skill
2. Determine scope: what systems, users, or data are affected?
3. Estimate time to resolution based on diagnosis
4. Document findings for incident record

### Step 4: Resolve
1. Implement fix or workaround
2. Test fix thoroughly before production deployment
3. Deploy fix following standard deployment procedures
4. Verify system is fully restored and stable
5. Monitor for recurrence for at least 15 minutes

### Step 5: Communicate
Send incident summary to stakeholders:
```
INCIDENT SUMMARY
================
Severity: [SEV-1/2/3/4]
Start time: [when incident began]
Detection time: [when it was discovered]
Resolution time: [when it was fixed]
Duration: [total impact time]

IMPACT:
- Affected systems: [which components]
- Affected users: [who was impacted]
- Data impact: [any data loss or corruption]

ROOT CAUSE:
[brief explanation of what went wrong]

RESOLUTION:
[what was done to fix it]

FOLLOW-UP:
[what's being done to prevent recurrence]
```

### Step 6: Post-Incident
1. Capture lessons learned using knowledge-capture skill
2. Update monitoring/alerting if incident wasn't detected promptly
3. Update documentation if procedures need changes
4. Schedule preventive action items

## Quality Checklist
- [ ] Incident severity correctly classified
- [ ] Containment actions stopped further harm
- [ ] Root cause identified and documented
- [ ] Fix tested before deployment
- [ ] System verified stable after resolution
- [ ] Stakeholder communication sent with complete information
- [ ] Post-incident review completed with actionable items

## Error Handling
- **Error:** Cannot determine root cause
  **Response:** Document what's known, escalate to diagnostics specialist or domain expert, continue monitoring
- **Error:** Fix doesn't resolve the issue
  **Response:** Roll back fix, re-diagnose, try alternative approach
- **Error:** Incident scope larger than expected
  **Response:** Upgrade severity level, notify additional stakeholders, request additional help
- **Error:** Multiple simultaneous incidents
  **Response:** Prioritize by severity, handle SEV-1 first, queue others

## Cross-Team Integration
**Related Skills:** escalation-management, handoff-protocol, secrets-handling, systematic-debugging, knowledge-capture
**Used By:** ALL agents as primary response procedure for any failure