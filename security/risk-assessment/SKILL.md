---
name: risk-assessment
description: >
  Use when evaluating potential risks before making decisions, starting initiatives,
  or implementing changes. This skill provides a structured risk assessment framework
  for identifying, analyzing, and responding to risks across all domains.
---

# Risk Assessment

## Overview
This skill defines a systematic approach to identifying, analyzing, and responding to risks. Proactive risk assessment prevents surprise failures, enables informed decision-making, and ensures risks are managed at acceptable levels.

## When to Use
- Before starting a new project, feature, or initiative
- Before making significant changes to existing systems or processes
- When a new threat, vulnerability, or concern is identified
- When evaluating alternatives or choosing between approaches
- Before deploying to production or releasing to users
- **Don't use when:** Changes are trivial with no identifiable risk (minor bug fixes, typo corrections)

## Core Procedures

### Step 1: Identify Risks
Brainstorm potential risks across these categories:
- **Technical:** System failures, integration issues, performance problems
- **Security:** Vulnerabilities, unauthorized access, data breaches
- **Operational:** Process failures, capacity issues, dependencies
- **Compliance:** Regulatory violations, policy breaches, audit failures
- **Business:** Missed deadlines, cost overruns, stakeholder dissatisfaction
- **External:** Vendor failures, market changes, regulatory changes

For each risk, document:
```
RISK: [brief description]
Category: [technical/security/operational/compliance/business/external]
Source: [what causes this risk]
```

### Step 2: Assess Each Risk
Rate each risk on two dimensions:

**Likelihood** (probability of occurring):
- 1: Rare (<5%)
- 2: Unlikely (5-25%)
- 3: Possible (25-50%)
- 4: Likely (50-75%)
- 5: Almost certain (>75%)

**Impact** (severity if it occurs):
- 1: Negligible (minor inconvenience, easily fixed)
- 2: Minor (small delay or cost, contained impact)
- 3: Moderate (significant delay/cost, limited scope)
- 4: Major (serious delay/cost, broad scope)
- 5: Critical (project/system failure, widespread impact)

**Risk Score = Likelihood × Impact** (range 1-25)

### Step 3: Prioritize and Respond
| Score | Level | Response |
|-------|-------|----------|
| 15-25 | CRITICAL | Must mitigate before proceeding, escalate to leadership |
| 10-14 | HIGH | Mitigation plan required, accept with controls |
| 5-9 | MEDIUM | Monitor and manage, accept with awareness |
| 1-4 | LOW | Accept, document for tracking |

### Step 4: Define Response Strategy
For each risk, choose one response:
- **AVOID:** Change plan to eliminate the risk entirely
- **MITIGATE:** Reduce likelihood or impact through controls
- **TRANSFER:** Shift risk to another party (insurance, vendor)
- **ACCEPT:** Acknowledge risk, monitor, have contingency ready

Document:
```
RISK RESPONSE
=============
Risk: [description]
Score: [likelihood × impact = score]
Response: [avoid/mitigate/transfer/accept]
Actions: [specific steps to manage this risk]
Owner: [who monitors and responds]
Contingency: [what to do if risk materializes]
Trigger: [signs that risk is becoming reality]
```

### Step 5: Monitor and Review
- Track risk status (open, mitigated, materialized, closed)
- Review risks at regular intervals or milestones
- Update scores as conditions change
- Report CRITICAL/HIGH risks to leadership regularly

## Quality Checklist
- [ ] Risks identified across all relevant categories
- [ ] Each risk has assessed likelihood and impact
- [ ] CRITICAL and HIGH risks have mitigation plans
- [ ] Contingencies defined for all risks above MEDIUM
- [ ] Owners assigned for monitoring each risk
- [ ] Risk register maintained and updated

## Error Handling
- **Error:** Risk materializes during project
  **Response:** Execute contingency plan, escalate if beyond contingency scope
- **Error:** Risk score changes as project progresses
  **Response:** Reassess, adjust response strategy if score moved to different level
- **Error:** New risks discovered mid-project
  **Response:** Assess immediately, integrate into risk register

## Cross-Team Integration
**Related Skills:** incident-response, escalation-management, threat-modeling, conflict-resolution
**Used By:** Predictor agents, project managers, CEOs, security agents (Guardian, Sentinel, Watchtower), Oracle, Catalyst, Strategos