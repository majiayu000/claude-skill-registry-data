---
name: incident-postmortem
description: "Write blameless incident postmortems with timeline reconstruction, root cause analysis, action items, and preventive measures"
---

# Incident Postmortem Builder

## Overview

Create blameless incident postmortems that transform operational disruptions into learning opportunities. These documents focus on system failures and process gaps, not individual blame, enabling continuous improvement and preventing recurrence.

## Core Principles

1. **Blameless**: Focus on systems, not people. "Why did this happen?" not "Who screwed up?"
2. **Psychological Safety**: Team members must feel safe discussing root causes without fear
3. **Data-Driven**: Base findings on logs, metrics, and facts; not assumptions
4. **Action-Oriented**: Every finding leads to actionable improvements
5. **Learning Culture**: Treat incidents as valuable learning events, not failures
6. **Transparency**: Share findings broadly; communicate changes to prevent similar incidents

## Timeline Reconstruction

Create a detailed chronology of events:

```
Time (UTC) | Who | What | Evidence | Context
-----------|-----|------|----------|----------
2024-02-15 14:32 | Jenkins | Deploy v2.1.3 (buggy) | Logs | Automated Friday deploy
14:35 | Customer | Website errors | CloudFront | 500 errors reported
14:37 | On-call | PagerDuty alert | Alert | Error rate exceeded threshold
14:42 | Eng team | Investigation starts | Slack #incidents | Identified deploy cause
14:55 | Lead | Rollback initiated | Logs | Reverted to v2.1.2
15:02 | On-call | Error rate normal | Metrics | Customers back to normal
15:30 | Team | Root cause meeting | Notes | Identified root cause
```

**Timeline Template**:
- **T+0 (Alert)**: When first detected
- **T+X (Detection)**: When incident was recognized
- **T+Y (Communication)**: When stakeholders notified
- **T+Z (Mitigation)**: When incident owner took action
- **T+N (Resolution)**: When system returned to normal
- **Duration**: Total time from detection to resolution

## Root Cause Analysis (5 Whys)

Go beyond the obvious cause to find systemic issues:

```
Incident: Website down for 28 minutes

Why 1: Why did website go down?
Answer: Deployment v2.1.3 contained a bug causing infinite loop in auth service

Why 2: Why did the bug reach production?
Answer: Code review missed the issue; test suite didn't catch it

Why 3: Why didn't test suite catch the infinite loop?
Answer: Load/stress tests only run occasionally; not part of standard CI pipeline

Why 4: Why aren't load tests mandatory in CI?
Answer: Historically slow; team prioritized speed over reliability

Why 5: Why does team optimize for deploy speed over testing?
Answer: Pressure to ship features fast; no documented standard for testing rigor

ROOT CAUSE: Process gap - no mandatory load testing in CI; pressure to ship
```

**Avoid**:
- Stopping too early ("operator didn't notice error")
- Human error as root cause ("developer made a mistake")
- Unclear systemic issues

**Focus on**:
- Process failures
- Monitoring gaps
- Communication breakdowns
- Knowledge gaps
- Tool limitations
- Architectural weaknesses

## Contributing Factors (Swiss Cheese Model)

Most incidents involve multiple failures aligning:

```
Incident: Late-night 30-minute outage

Contributing Factors:
1. Code change made Friday afternoon (rush to deploy before weekend)
2. No automated rollback capability (manual process)
3. On-call engineer had weak knowledge of new code (hired 3 weeks ago)
4. No load test coverage for auth service changes (technical debt)
5. Monitoring alert threshold set too high (missed early warning)
6. Deployment not staged; went straight to production (process gap)
7. No change advisory board approval (governance gap)

Any ONE of these alone wouldn't have caused incident. Combined: 28-minute outage.
```

## Root Cause vs. Proximate Cause

**Proximate Cause** (immediate cause):
- Infinite loop in authentication code
- Deployment that shouldn't have happened
- Missing monitor alert

**Root Cause** (systemic failure):
- Code review process insufficient for critical changes
- Deployment process lacked staged/canary deployment
- Testing strategy doesn't include stress tests
- Knowledge gap in on-call team for recent changes

Focus postmortem on root causes, not proximate causes.

## Action Items (Follow-up)

**Structure**: [Priority] | [What] | [Why] | [Owner] | [Due Date] | [Status]

### Immediate Actions (0-7 days)
```
CRITICAL | Deploy hotfix for infinite loop | Prevent recurrence | Sarah | 2024-02-15 | DONE
HIGH | Document code change impact | Knowledge transfer | John | 2024-02-16 | IN PROGRESS
MEDIUM | Post-incident communication to customers | Transparency | PM | 2024-02-15 | DONE
```

### Short-term Actions (1-4 weeks)
```
HIGH | Implement automatic canary deployment | Catch issues pre-production | DevOps | 2024-03-01 | PENDING
HIGH | Add auth load tests to CI pipeline | Catch performance issues early | QA | 2024-03-01 | PENDING
MEDIUM | Onboard new on-call engineer on recent changes | Knowledge gap closure | Tech Lead | 2024-02-28 | IN PROGRESS
```

### Long-term Actions (1-3 months)
```
MEDIUM | Implement automated rollback capability | Faster recovery time | Arch | 2024-04-15 | PENDING
LOW | Review change advisory board process | Governance improvement | Ops | 2024-05-01 | PENDING
LOW | Schedule quarterly load testing for critical services | Proactive risk management | Perf | 2024-06-01 | PENDING
```

**SMART Action Items**:
- **S**pecific: What exactly needs to be done?
- **M**easurable: How will we know it's complete?
- **A**ssignable: Who owns this?
- **R**ealistic: Can it actually be done?
- **T**ime-bound: When is it due?

## Preventive Measures

**Prevention Strategy**: How do we prevent this type of incident?

1. **Process Changes**:
   - Implement staged/canary deployments for critical services
   - Add code review requirement for auth service changes
   - Require load test passing for critical path changes

2. **Monitoring & Alerting**:
   - Lower error rate alert threshold (early warning)
   - Add CPU/memory alerts for auth service
   - Add canary endpoint synthetic monitoring

3. **Automation**:
   - Automatic rollback if error rate >2%
   - Load test gate in CI pipeline (mandatory, not optional)
   - Automated chaos engineering tests weekly

4. **Documentation & Training**:
   - Document architecture of auth service
   - Create runbook for auth service incidents
   - Schedule knowledge transfer session for on-call team

5. **Organizational**:
   - Remove deadline pressure; don't deploy Friday afternoon
   - Add on-call engineer to code reviews of critical services
   - Establish incident SLA: detection to resolution <15 minutes for P0 incidents

## Template Structure

**INCIDENT POSTMORTEM**

Incident ID: INC-2024-047
Date: 2024-02-15
Duration: 28 minutes (14:35 UTC - 15:03 UTC)
Impact: Website unavailable; 0.5M page requests failed
Severity: P1 (Critical)

**INCIDENT SUMMARY**
[1 paragraph overview of what happened and impact]

**TIMELINE**
[Chronological events table]

**ROOT CAUSE ANALYSIS**
Primary Root Cause: [High-level finding]

5 Whys Analysis:
[Why chain]

Contributing Factors:
[List of systemic issues]

**IMPACT ANALYSIS**
- Customers Affected: [Number or percentage]
- Duration: [Minutes]
- Revenue Impact: [If quantifiable]
- Reputation Impact: [Qualitative assessment]
- Data Loss: [Yes/No, details if yes]

**DETECTION & RESPONSE**
- Detection Time: [Minutes to detect]
- Response Time: [Minutes to start mitigation]
- Resolution Time: [Minutes to full recovery]
- Response Quality: [Smooth/Some delays/Chaotic - why?]

**WHAT WENT WELL**
- [Good thing 1]: Enabled [outcome]
- [Good thing 2]: Enabled [outcome]
- [Good thing 3]: Enabled [outcome]

*Recognize excellent work; reinforce good behaviors*

**WHAT COULD BE BETTER**
- [Gap 1]: Impact was [consequence]
- [Gap 2]: Impact was [consequence]
- [Gap 3]: Impact was [consequence]

**ACTION ITEMS**
[Immediate, short-term, long-term actions with owners and dates]

**PREVENTIVE MEASURES**
[How we prevent this incident class in future]

**APPENDICES**
- Error logs (anonymized)
- Customer communication
- Monitoring graphs during incident
- Architecture diagram
- Related incidents (historical patterns)

## Postmortem Facilitation

**Blameless Meeting Principles**:
1. **Start with context, not blame**: "Here's what was happening at 14:30 UTC..."
2. **Use neutral language**: "Code changed" not "Code was broken"
3. **Ask curious questions**: "What were you seeing on your screen?" not "Why didn't you check the logs?"
4. **Encourage storytelling**: Let people describe their experience; narrative flow
5. **Capture assumptions**: "I assumed..." statements reveal knowledge gaps
6. **No hierarchy**: On-call engineer's observations valued same as CTO's
7. **Record decisions**: Why did we choose rollback vs. fix? Document the thinking
8. **Record learnings**: What surprised people? What did they learn?

**Participants**:
- On-call engineer (incident responder)
- Service owner
- DevOps/Infrastructure team
- Product/Business owner
- Facilitator (experienced, neutral party)

**Meeting Duration**: 30-60 minutes maximum

**When to Hold**: Within 48 hours of incident resolution (while details are fresh)

## Distribution & Follow-up

1. **Share Widely**: Postmortem is internal tool for learning; share with full engineering org
2. **Executive Summary**: One-page summary for leadership
3. **Customer Communication**: Transparency about what happened and prevention measures
4. **Process Review**: Monthly review of open action items
5. **Trend Analysis**: Quarterly review - are we preventing incident classes or just firefighting?

## Preventing Similar Incidents

**Incident Class Tracking**:
- Authentication failures
- Database performance degradation
- Memory leaks
- Configuration errors
- Dependency failures
- Deployment failures

If same class happens twice: escalate prevention measures
If same incident happens three times: organizational escalation (management review)

---

**Use this skill to**: Transform incidents into learning opportunities, improve system resilience, and build a psychologically safe incident response culture.
