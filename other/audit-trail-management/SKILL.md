---
name: audit-trail-management
description: >
  Use when creating, maintaining, or reviewing records of actions, decisions, changes,
  and events for compliance, accountability, and investigation purposes. This skill
  provides procedures for managing audit trails across all agent activities.
---

# Audit Trail Management

## Overview
This skill defines how to create and maintain audit trails - chronological records of who did what, when, and why. Audit trails are essential for compliance, investigation, accountability, and understanding system behavior. Every significant action should leave a traceable record.

## When to Use
- When making changes to production systems, configurations, or data
- When making decisions that affect project direction or resource allocation
- When approving, rejecting, or modifying deliverables
- When accessing sensitive systems or data
- When resolving incidents, disputes, or escalations
- **Don't use when:** Recording trivial routine actions that add no compliance or investigative value

## Core Procedures

### Step 1: Identify Recordable Events
Record these event types:
- **Access Events:** Who accessed what system/data and when
- **Change Events:** What was changed, by whom, when, and why
- **Decision Events:** What decision was made, by whom, when, and rationale
- **Approval Events:** What was approved/rejected, by whom, when
- **Incident Events:** What incident occurred, when detected, when resolved
- **Communication Events:** Significant directives or decisions communicated

### Step 2: Structure Audit Entries
Each audit entry must include:
```
AUDIT ENTRY
===========
Timestamp: [ISO 8601 date-time]
Actor: [agent name, company, role]
Event Type: [access/change/decision/approval/incident/communication]
Action: [what was done - specific and objective]
Target: [what system, data, or process was affected]
Reason: [why the action was taken]
Result: [outcome - success, failure, partial]
Reference: [ticket ID, task ID, or related entry]
```

### Step 3: Storage Requirements
- Store entries in tamper-evident storage
- Entries must be immutable once written (append-only)
- Entries must be searchable by timestamp, actor, event type, and target
- Retention period: minimum 1 year, or as required by compliance
- Cross-reference related entries for investigation trails

### Step 4: Audit Trail Review
Periodic review (monthly or per compliance requirement):
1. Check for completeness: are all required events being recorded?
2. Check for anomalies: unexpected patterns, unauthorized access
3. Check for gaps: time periods with no entries (should not happen)
4. Check for stale entries: old unresolved incidents or decisions
5. Generate summary report for governance review

### Step 5: Investigation Support
When audit trails are needed for investigation:
1. Define scope: what time range, actors, and systems?
2. Extract relevant entries in chronological order
3. Correlate entries across systems to build complete timeline
4. Identify gaps or anomalies in the timeline
5. Present findings with evidence trail

## Quality Checklist
- [ ] All significant events are being recorded
- [ ] Entries follow standardized format
- [ ] Entries are stored in tamper-evident, append-only storage
- [ ] Retention policy defined and enforced
- [ ] Entries are searchable and retrievable
- [ ] Periodic review schedule is maintained

## Error Handling
- **Error:** Audit trail storage unavailable
  **Response:** Queue entries locally, retry storage, escalate to infrastructure if persistent
- **Error:** Missing entries discovered (gap in trail)
  **Response:** Document the gap, investigate cause, recreate entries if possible with note about reconstruction
- **Error:** Audit trail shows unauthorized activity
  **Response:** Do NOT modify or delete the entry, immediately notify security agent (Guardian/Sentinel)
- **Error:** Audit trail entries exceed retention period
  **Response:** Archive per retention policy, delete only after confirmed no active investigations

## Cross-Team Integration
**Related Skills:** secrets-handling, data-privacy-check, incident-response, risk-assessment
**Used By:** Compliance agents (Compliance, Auditor, Integrity), security agents (Guardian, Sentinel), ALL agents for significant actions