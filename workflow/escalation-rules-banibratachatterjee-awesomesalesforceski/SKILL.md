---
name: escalation-rules
description: "Configure and troubleshoot Salesforce Case Escalation Rules: setting up time-based escalation entries, business hours configuration, escalation actions (email alerts and reassignment), and diagnosing why cases are not escalating. NOT for case assignment on creation (use assignment-rules), approval routing (use approval-processes), or SLA milestones in Service Cloud (use entitlement-management)."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Operational Excellence
triggers:
  - "case is not escalating to a manager after the required time has passed"
  - "how do I set up automatic case escalation after X hours"
  - "escalation rule is not firing or not sending email notifications"
  - "how to configure business hours so escalation only counts working hours"
  - "cases are being escalated even on weekends or outside business hours"
  - "how to reassign a case automatically when it is not resolved in time"
tags:
  - escalation-rules
  - case-management
  - business-hours
  - service-cloud
  - time-based-automation
inputs:
  - "The objects involved (always Case)"
  - "SLA requirements: how many hours before escalation fires"
  - "Whether escalation time should respect business hours or run 24/7"
  - "Escalation actions required: email notification targets, reassignment target (user, queue, or manager)"
  - "Case criteria for each escalation tier (priority, type, origin, etc.)"
outputs:
  - "Configured escalation rule with entries and actions"
  - "Business hours setup recommendation"
  - "Escalation configuration review checklist"
  - "Troubleshooting diagnosis for non-firing escalations"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-03
---

# Escalation Rules

This skill activates when you need to configure, review, or troubleshoot Salesforce Case Escalation Rules — the declarative mechanism that automatically notifies stakeholders or reassigns cases when they are not resolved within a specified time window.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Active rule limit:** Only one escalation rule can be active per org. If multiple rule configs exist, only the one marked Active fires. Confirm whether an active rule already exists before creating a new one.
- **Processing cadence:** The time-based workflow engine that drives escalation runs approximately every hour. Escalations are not fired in real time. A case that hits its threshold at 2:05 PM may not escalate until the next engine run — plan SLA commitments accordingly.
- **Business hours dependency:** If an escalation entry is configured to use business hours, those business hours must exist and be assigned to the case. If no business hours are defined at org level, the default is 24/7.

---

## Core Concepts

### How Escalation Rules Differ from Assignment Rules

Assignment rules route cases to users or queues **when a case is created or re-opened**. They fire once on creation.

Escalation rules operate on a **timer**: they fire when a case that matches defined criteria has been open for longer than a configured threshold. If a case is not resolved within X hours, escalation rules send notifications or reassign the case.

The two rules are complementary. Assignment routes the case on arrival; escalation follows up when response time is exceeded.

### Rule Structure: One Rule, Many Entries

A single active escalation rule contains multiple **rule entries**. Each entry defines:

1. **Entry criteria** — which cases this entry applies to (filter logic: field = value, using the same criteria builder as other rule types)
2. **Escalation time** — how many hours must pass before the escalation actions fire
3. **Business hours** — whether the timer counts all hours or only configured business hours
4. **Age-over** field — whether the timer is based on the case's **creation date** or the date the case was **last modified** (default is creation date; choose "last modified" to reset the clock when agents update the case)

Entries are evaluated in order. The **first matching entry** wins — subsequent entries are skipped, just like assignment rule evaluation.

### Escalation Actions

Each rule entry can have up to **5 escalation actions**, which fire at different time thresholds. For example:

- At 4 hours: email the case owner's manager
- At 8 hours: reassign the case to a senior support queue + email the queue

Each action specifies:
- **Notify this user**: a specific user, role, case owner's manager, customer portal user, or no one
- **Reassign case to**: a specific user or queue (optional — notification-only actions are valid)
- **Additional email**: free-form email address notification

### Business Hours Configuration

Business hours define when your team is working. Escalation time is only counted within configured business hours windows when the entry is set to use them.

**Defaults:** The org-level default business hours are 24/7 unless explicitly configured. A case can be assigned a specific business hours record using the `BusinessHoursId` field (or the "Business Hours" field visible in the UI with Service Cloud).

If you want escalation to pause on weekends, you must:
1. Configure business hours under Setup > Business Hours
2. Set the entry to "Use business hours" and point to the correct hours record
3. Ensure cases have the correct Business Hours assignment (either default or case-level)

---

## Common Patterns

### Pattern: Tiered Escalation by Case Priority

**When to use:** Different SLA windows for different priorities. P1 cases escalate in 1 hour; P3 cases escalate in 8 hours.

**How it works:**
1. Create rule entries in priority order: P1 entry first, P2 next, P3 last.
2. Each entry uses field criteria `Priority = "P1"` (or P2, P3).
3. Set escalation times: P1 = 1 hour, P2 = 4 hours, P3 = 8 hours.
4. Add escalation actions for each tier: P1 notifies manager immediately, P2 notifies at 2h and reassigns at 4h.

**Catch:** Rule entries are evaluated top to bottom. Put P1 first, otherwise a P1 case might match a lower-tier entry if that entry has looser criteria.

### Pattern: Business-Hours-Aware Escalation for a Regional Team

**When to use:** A support team works 8 AM–6 PM, Monday–Friday. Escalation should not fire at 2 AM Saturday for a case opened Friday at 5 PM.

**How it works:**
1. Create a Business Hours record: Setup > Business Hours > New. Set Mon–Fri 8:00 AM–6:00 PM in the team's time zone.
2. Set the default business hours or assign per case.
3. In the escalation rule entry, check "Use Business Hours."
4. Set the escalation threshold. A 4-hour escalation clock that started at 5 PM Friday will not expire until 9 AM Monday.

**Why this matters:** Without this configuration, a case created Friday at 5 PM with an 8-hour escalation window would fire at 1 AM Saturday — uselessly sending a notification when no one is working.

### Pattern: Notify and Reassign at Different Thresholds

**When to use:** You want to warn the case owner at hour 2, then escalate to a queue at hour 4 if still unresolved.

**How it works:**
Within a single rule entry, add two escalation actions:
- Action 1: Age over = 2 hours → Notify case owner's manager. No reassignment.
- Action 2: Age over = 4 hours → Reassign to Escalation Queue + email queue.

Both actions are attached to the same entry (same criteria). They fire sequentially as time thresholds are crossed.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Route case to agent on creation | Assignment Rule | Escalation only activates after time passes — it is not a routing tool for new cases |
| Fire when SLA time is exceeded | Escalation Rule | Purpose-built for time-based case follow-up |
| Clock should pause on weekends | Enable Business Hours in rule entry | Without this, the 24/7 clock fires off-hours |
| Reset clock when agent responds | Use "Last Modified Date" as age basis | Clock restarts each time the case is updated |
| Keep original owner but notify manager | Escalation action without reassignment | Set "Notify" target only; leave reassignment blank |
| Multiple SLA tiers by priority | Multiple rule entries, ordered P1 first | First matching entry wins; put most specific criteria at top |
| Escalation every hour until resolved | Add multiple time-stepped actions | Actions at 2h, 4h, 6h on the same entry create progressive escalation |

---


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

Run through these before marking escalation rule work complete:

- [ ] Only one escalation rule is active; no conflicting rules exist in Setup > Escalation Rules
- [ ] Rule entries are ordered correctly — most specific criteria appear first
- [ ] Each entry's escalation time is expressed in hours and matches the agreed SLA
- [ ] Business hours are configured if escalation should respect working hours, and entries reference the correct hours record
- [ ] Escalation actions specify valid targets (active users, populated queues, or valid roles)
- [ ] Test case has been created, aged past the threshold (or time advanced via test tooling), and escalation fired as expected
- [ ] The case criteria used in each entry (Priority, Type, Origin) match the actual field values used in the org
- [ ] Notifications are going to reachable email addresses — not inactive users or empty queues

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **The engine runs approximately every hour — not in real time.** Escalation time is not calculated to the minute. If a threshold is crossed at 10:35 AM and the engine last ran at 10:30 AM, escalation fires around 11:30 AM. Avoid SLAs with sub-one-hour resolution if precision matters.

2. **Deactivating and reactivating a rule does not reset case timers.** Cases already in the pipeline do not restart their clocks when you edit the rule. The engine resumes evaluation based on the original case creation (or last modified) date. This can cause a wave of unexpected escalations immediately after a rule is reactivated.

3. **Business hours = 24/7 if not explicitly configured.** If you leave business hours at the Salesforce default (which is 24 hours every day), checking "Use business hours" on an entry has no practical effect — all hours count. You must explicitly set Mon–Fri windows in the Business Hours setup for off-hours pausing to work.

4. **Only one active rule per org.** You cannot have a "Sales Cases" rule and a "Service Cases" rule both active simultaneously. Use multiple entries within the single active rule, with entry criteria differentiating case types. If you need different SLA structures, implement the differentiation through rule entry criteria, not through separate rules.

5. **Escalation does not fire on closed cases.** If a case is closed before the escalation threshold, no action fires. If it is reopened, the original creation-date clock continues from where it was — meaning reopened cases may escalate almost immediately if significant time has passed. Use "last modified date" as the age basis if you want reopened cases to get a fresh window.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Escalation rule configuration | A configured active rule with entries and actions, ready for test validation |
| Business hours record | A named business hours window that escalation entries can reference |
| Escalation configuration review | Checklist confirming rule order, thresholds, action targets, and business hours setup |

---

## Related Skills

- assignment-rules — use alongside escalation rules to handle initial routing; assignment routes on creation, escalation follows up if unresolved
- approval-processes — time-based routing for human decisions, not SLA escalation
