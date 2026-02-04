---
name: risk-management
description: Risk matrices, assessment patterns, and mitigation strategies. Reference this skill when assessing project risks.
---

# Risk Management Skill
# Project Autopilot - Risk assessment and mitigation patterns
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Comprehensive patterns for project risk management.

---

## Risk Framework

### Risk Management Process

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Identify   │ →  │   Analyze   │ →  │   Plan      │
│   Risks     │    │   & Score   │    │  Response   │
└─────────────┘    └─────────────┘    └─────────────┘
       ↑                                     │
       │           ┌─────────────┐           │
       └───────────│   Monitor   │←──────────┘
                   │  & Review   │
                   └─────────────┘
```

### Risk Equation

```
Risk Exposure = Probability × Impact × (1 - Mitigation Effectiveness)
```

---

## Risk Identification

### Technical Risks

| Risk Area | Common Risks | Indicators |
|-----------|--------------|------------|
| Architecture | Scalability limits, coupling | Load tests, complexity metrics |
| Dependencies | Breaking changes, outages | Changelog frequency, uptime |
| Security | Vulnerabilities, data exposure | Audit results, CVE alerts |
| Performance | Bottlenecks, latency | Response times, resource usage |
| Integration | API compatibility, data sync | Error rates, timeout frequency |

### Project Risks

| Risk Area | Common Risks | Indicators |
|-----------|--------------|------------|
| Scope | Creep, unclear requirements | Change requests, backlog growth |
| Schedule | Delays, unrealistic estimates | Burndown variance, velocity |
| Budget | Overruns, unexpected costs | Actual vs estimate, burn rate |
| Quality | Bugs, technical debt | Defect rate, code coverage |
| Communication | Misalignment, silos | Meeting frequency, blockers |

### Resource Risks

| Risk Area | Common Risks | Indicators |
|-----------|--------------|------------|
| Skills | Knowledge gaps, learning curves | Task completion time, questions |
| Availability | Competing priorities, absences | Capacity utilization, PTO |
| Turnover | Key person dependency | Bus factor, documentation |
| Vendors | Reliability, support quality | SLA compliance, response time |

### External Risks

| Risk Area | Common Risks | Indicators |
|-----------|--------------|------------|
| Market | Competition, demand shifts | Market research, analytics |
| Regulatory | Compliance changes | Industry news, legal updates |
| Economic | Budget cuts, funding | Company financials, news |
| Technology | Platform changes, deprecations | Roadmaps, announcements |

---

## Risk Scoring

### Probability Matrix

| Level | Score | Criteria |
|-------|-------|----------|
| Rare | 1 | Has never happened |
| Unlikely | 2 | Has happened once before |
| Possible | 3 | Has happened occasionally |
| Likely | 4 | Happens regularly |
| Almost Certain | 5 | Expected to happen |

### Impact Matrix

| Level | Score | Schedule | Cost | Quality |
|-------|-------|----------|------|---------|
| Minimal | 1 | < 1 day | < $100 | Cosmetic |
| Minor | 2 | 1-3 days | $100-500 | Minor defect |
| Moderate | 3 | 1-2 weeks | $500-2K | Functionality |
| Major | 4 | 2-4 weeks | $2K-10K | Major failure |
| Severe | 5 | > 1 month | > $10K | Project failure |

### Risk Score Matrix

```
                    IMPACT
           1    2    3    4    5
        ┌────┬────┬────┬────┬────┐
      5 │  5 │ 10 │ 15 │ 20 │ 25 │
        ├────┼────┼────┼────┼────┤
P     4 │  4 │  8 │ 12 │ 16 │ 20 │
R       ├────┼────┼────┼────┼────┤
O     3 │  3 │  6 │  9 │ 12 │ 15 │
B       ├────┼────┼────┼────┼────┤
      2 │  2 │  4 │  6 │  8 │ 10 │
        ├────┼────┼────┼────┼────┤
      1 │  1 │  2 │  3 │  4 │  5 │
        └────┴────┴────┴────┴────┘

🟢 1-4:  Low - Accept/Monitor
🟡 5-9:  Medium - Mitigate
🟠 10-15: High - Priority mitigation
🔴 16-25: Critical - Immediate action
```

---

## Response Strategies

### Strategy Selection Guide

| Strategy | When to Use | Cost | Risk Reduction |
|----------|-------------|------|----------------|
| Avoid | Unacceptable risk | High | 100% |
| Mitigate | Reducible risk | Medium | 30-80% |
| Transfer | Outsourceable risk | Medium | 50-90% |
| Accept | Low impact/probability | Low | 0% |

### Avoid

Eliminate the risk by changing approach.

```markdown
**Risk:** Third-party auth service reliability
**Strategy:** Build authentication in-house
**Actions:**
1. Implement JWT-based auth
2. Use proven libraries (Passport.js)
3. Add multi-factor authentication

**Cost:** +2 weeks development
**Risk Reduction:** 100%
```

### Mitigate

Reduce probability or impact.

```markdown
**Risk:** Database performance degradation
**Strategy:** Implement caching and optimization
**Actions:**
1. Add Redis caching layer
2. Optimize slow queries
3. Implement connection pooling
4. Add read replicas

**Cost:** +1 week development
**Risk Reduction:** 70%
```

### Transfer

Shift risk to another party.

```markdown
**Risk:** Server infrastructure management
**Strategy:** Use managed services
**Actions:**
1. Migrate to Vercel/AWS managed
2. Use managed database (Supabase)
3. Implement monitoring (Datadog)

**Cost:** ~$200/month
**Risk Reduction:** 80%
```

### Accept

Acknowledge and prepare contingency.

```markdown
**Risk:** Minor browser compatibility issues
**Strategy:** Accept with monitoring
**Actions:**
1. Document known limitations
2. Monitor analytics for browser usage
3. Create workaround documentation

**Cost:** Minimal
**Risk Reduction:** 0% (accept)
```

---

## Contingency Planning

### Contingency Template

```markdown
## Contingency: [Risk ID] - [Name]

### Trigger Conditions
- Condition 1 that indicates risk is occurring
- Condition 2 that indicates risk is occurring

### Immediate Response (0-1 hour)
1. Acknowledge incident
2. Notify stakeholders
3. Assess severity

### Short-term Response (1-24 hours)
1. Implement workaround
2. Communicate status
3. Begin root cause analysis

### Recovery Actions
1. Fix underlying issue
2. Restore normal operations
3. Document lessons learned

### Communication Plan
| Audience | Channel | Frequency | Owner |
|----------|---------|-----------|-------|
| Team | Slack | Real-time | Lead |
| Stakeholders | Email | 4 hours | PM |
| Users | Status page | As needed | Support |
```

---

## Risk Monitoring

### Key Risk Indicators (KRIs)

| Risk Type | KRI | Warning | Critical |
|-----------|-----|---------|----------|
| Performance | P95 latency | > 500ms | > 1s |
| Availability | Uptime | < 99.9% | < 99% |
| Scope | Backlog growth | +20% | +50% |
| Budget | Cost variance | +15% | +30% |
| Quality | Defect rate | > 5% | > 10% |
| Security | Vulnerability age | > 7 days | > 30 days |

### Monitoring Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│                      RISK DASHBOARD                          │
├─────────────────────────────────────────────────────────────┤
│  Active Risks: 8     │  Critical: 1  │  High: 2  │  Med: 5  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  R1 [API Dep]     🔴 ████████████████████████ Critical      │
│  R2 [Scope]       🟠 ██████████████████░░░░░░ High          │
│  R3 [Skills]      🟠 ████████████████░░░░░░░░ High          │
│  R4 [Schedule]    🟡 ██████████████░░░░░░░░░░ Medium        │
│  R5 [Budget]      🟡 ████████████░░░░░░░░░░░░ Medium        │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  Trend: → Stable   │  Mitigations: 3 active  │  Due: 2     │
└─────────────────────────────────────────────────────────────┘
```

---

## Risk Review Cadence

| Meeting | Frequency | Focus | Attendees |
|---------|-----------|-------|-----------|
| Daily standup | Daily | Blockers, new risks | Team |
| Sprint planning | Bi-weekly | Sprint risks | Team |
| Risk review | Weekly | All active risks | Leads |
| Stakeholder update | Monthly | High/Critical risks | Management |
| Retrospective | Bi-weekly | Lessons learned | Team |

---

## Common Software Project Risks

### Top 10 Risks

1. **Unclear Requirements** - Scope uncertainty
2. **Third-Party Dependencies** - API/service reliability
3. **Technical Debt** - Accumulated shortcuts
4. **Performance Issues** - Scalability problems
5. **Security Vulnerabilities** - Data protection
6. **Resource Availability** - Team capacity
7. **Integration Complexity** - System connections
8. **Schedule Pressure** - Unrealistic deadlines
9. **Technology Changes** - Platform updates
10. **Knowledge Gaps** - Missing expertise
