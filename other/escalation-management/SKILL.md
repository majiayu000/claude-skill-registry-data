---
name: escalation-management
description: >
  Use when encountering blockers, unresolved issues, or problems beyond your authority
  or capability. This skill provides a structured escalation process ensuring issues
  are escalated to the right level with proper context, and tracked through resolution.
---

# Escalation Management

## Overview
This skill defines how to properly escalate issues when you cannot resolve them independently. Clear escalation prevents issues from stalling indefinitely and ensures problems reach agents with appropriate authority or expertise to resolve them.

## When to Use
- When blocked by something outside your capability or authority
- When a decision is needed that's above your pay grade
- When repeated attempts to resolve an issue have failed
- When a security, compliance, or ethical concern is identified
- When cross-company coordination is needed and you lack the authority
- **Don't use when:** Issue can be resolved with standard procedures or knowledge retrieval

## Core Procedures

### Step 1: Assess Escalation Level
Determine the appropriate escalation level based on issue type:

| Issue Type | Escalate To | Timeframe |
|-----------|------------|-----------|
| Technical blocker in your division | Division lead or team manager | 1 hour |
| Cross-team coordination failure | Company CEO/orchestrator | 2 hours |
| Security or compliance concern | Security agent + CEO | IMMEDIATE |
| Resource/capacity shortage | CEO + infrastructure | 4 hours |
| Quality rejection of deliverable | Receiving agent's lead | 1 hour |
| Ethical or policy concern | Council + CEO | 2 hours |
| Enterprise-wide impact | All affected CEOs + Orchestrator | 1 hour |

### Step 2: Prepare Escalation Package
Structure escalation communication:

```
ESCALATION
==========
Level: [immediate / urgent / standard]
From: [your agent name, company]
To: [target escalation agent]
Issue: [one-line description]

BLOCKER DETAIL:
- What's blocked: [specific description]
- Impact: [what work cannot proceed because of this]
- When discovered: [timestamp]

ATTEMPTS MADE:
1. [what you tried, result]
2. [what you tried, result]
3. [what you tried, result]

WHAT'S NEEDED:
- Specific decision or action required from escalation target
- Information or resources that would unblock you
- Deadline by which resolution is needed

URGENCY JUSTIFICATION:
- Work affected: [which tasks, projects, or deliverables]
- Business impact: [cost, delay, risk if not resolved]
- Suggested resolution: [if you have a recommendation]
```

### Step 3: Send and Track
- Send escalation using handoff-protocol to target agent
- Set a timer based on escalation level timeframe
- If no response within timeframe, escalate ONE level higher
- Do NOT escalate to multiple levels simultaneously (follow chain of command)

### Step 4: Resolution
- When resolution is received, confirm it resolves the blocker
- If resolution is insufficient, provide specific feedback and re-escalate
- Capture lessons learned from the escalation for future knowledge

## Quality Checklist
- [ ] Escalation level is appropriate for issue severity
- [ ] All attempted resolutions documented
- [ ] Specific ask is clearly stated
- [ ] Impact and urgency are justified with facts
- [ ] Escalation sent to correct agent (not skipped levels)
- [ ] Follow-up timer is set

## Error Handling
- **Error:** No response within escalation timeframe
  **Response:** Escalate one level higher with note about delayed response
- **Error:** Escalation target sends you back to handle it yourself
  **Response:** Accept with specific guidance, execute, re-escalate only if STILL blocked with new information
- **Error:** Multiple escalations for same issue (churning)
  **Response:** Flag to governance (Council/Governor) as systemic issue needing policy change
- **Error:** Emergency escalation but target agent unavailable
  **Response:** Escalate to backup agent, then to CEO if both unavailable

## Cross-Team Integration
**Related Skills:** handoff-protocol, incident-response, conflict-resolution, status-reporting
**Used By:** ALL agents when blocked or encountering issues beyond their capability