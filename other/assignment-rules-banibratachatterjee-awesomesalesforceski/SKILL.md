---
name: assignment-rules
description: "Use this skill when configuring or troubleshooting Lead or Case assignment rules in Salesforce: creating rule entries, setting filter criteria, assigning records to users or queues, understanding when rules run, and implementing round-robin patterns with Apex. Trigger keywords: lead assignment, case assignment, assignment rule, queue assignment, auto-assign. NOT for approval process routing (use approval-processes). NOT for Omni-Channel routing or Skills-Based Routing (those are separate routing engines). NOT for Flow-triggered field updates unrelated to ownership."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Reliability
tags:
  - assignment-rules
  - lead-management
  - case-management
  - queues
  - routing
triggers:
  - "how do I automatically assign new leads to the right sales rep based on region"
  - "cases are not being assigned to the correct queue when submitted via web form"
  - "how does Salesforce assignment rule work for leads"
  - "lead assignment rule criteria not matching records as expected"
  - "how to assign cases to a queue automatically when created from email-to-case"
  - "round-robin lead assignment between multiple users in Salesforce"
  - "assignment rule not running when I create a record via the API"
inputs:
  - "Object type: Lead or Case (assignment rules only exist for these two objects)"
  - "Assignment target: specific User or Queue to receive matched records"
  - "Criteria fields and values that determine which rule entry applies"
  - "Whether round-robin distribution across multiple users is required"
outputs:
  - "Configured active assignment rule with ordered rule entries"
  - "Queue setup guidance when records should be pooled rather than individually owned"
  - "Apex-based round-robin pattern when equal distribution is required"
  - "Troubleshooting analysis when rules are not firing as expected"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-03
---

# Assignment Rules

This skill activates when an admin needs to create, configure, audit, or troubleshoot Lead or Case assignment rules — including rule entry criteria, queue vs user assignment, API-triggered rule evaluation, and round-robin patterns with Apex when native distribution is insufficient.

---

## Before Starting

Gather this context before working on assignment rules:

- **Which object?** Assignment rules only exist for Lead and Case. Other objects do not have native assignment rules — use Flow or Apex for those.
- **Is there already an active rule?** Only one assignment rule can be active per object at a time. Activating a new rule deactivates the previous one automatically.
- **How will records be created?** Web-to-Lead, Web-to-Case, and Email-to-Case automatically trigger the active assignment rule. UI-created records require the user to check "Assign using active assignment rule." API-created records require an explicit header.
- **Are queues needed?** Queues allow a pool of users to work records collaboratively. Assignment rules can route to a queue instead of a single user. Understand who should own the record before designing criteria.

---

## Core Concepts

### Active Rule Limit and Rule Entry Order

Salesforce enforces a hard limit of **one active assignment rule per object** (Lead and Case each). When you activate a new rule, the previously active rule is automatically deactivated. You cannot have two active rules simultaneously.

Each assignment rule contains multiple **rule entries**. Rule entries are evaluated **in order** — the first entry whose criteria match the incoming record wins, and Salesforce assigns the record to that entry's target. Evaluation stops immediately after the first match. No subsequent entries are evaluated.

This first-match-wins behavior means entry order is critical. More specific criteria should appear earlier in the list than broad catch-all entries.

A rule can have up to **3,000 rule entries**. Each entry specifies:
- Filter criteria (field conditions using standard AND/OR logic)
- Assignment target: a User or a Queue
- An optional email template to send the assigned user or queue a notification

### When Assignment Rules Run

Assignment rules do **not** run automatically in every context. The trigger depends on how the record is created or updated:

| Creation Method | Lead | Case |
|---|---|---|
| Web-to-Lead form | Always (uses active rule automatically) | — |
| Web-to-Case form | — | Always (uses active rule automatically) |
| Email-to-Case | — | Always (uses active rule automatically) |
| Lightning UI (new record) | User must check "Assign using active assignment rule" | User must check "Run assignment rules" |
| REST API | Must include `Sforce-Auto-Assign: true` header, or specify rule ID | Same |
| SOAP API | Must include `AssignmentRuleHeader` element | Same |
| Data Loader (insert/update) | Must set `sfdc.assignmentRule` property to rule ID in settings | Same |
| Apex (Database.insert) | Use `Database.DMLOptions.assignmentRuleHeader` with `useDefaultRule = true` or specific rule ID | Same |

If no active rule is found, or no rule entry criteria match, records go to the **Default Lead Owner** (configured in Lead Settings) for leads, or retain the creating user as owner for cases unless a default case owner is configured in Support Settings.

### Queue Assignment vs User Assignment

An assignment rule entry can target either a **User** or a **Queue**:

- **User assignment** sets that specific user as the record owner. The record appears in their personal "My Open Leads" or "My Cases" views. The assigned user receives an email notification if a template is configured.
- **Queue assignment** sets the queue as the owner. The record appears in the queue's list view, visible to all queue members. Any queue member can accept the record by changing ownership. The queue's email address (if configured) receives a notification, not individual members.

Queues are preferable when multiple agents handle a shared pool of work and first-available assignment is acceptable. User assignment is preferable when specific expertise routing or workload balancing is required.

### Round-Robin Assignment (No Native Support)

Salesforce assignment rules do not natively distribute records in a round-robin pattern across multiple users. Every rule entry targets a single user or queue. To achieve round-robin:

**Approach 1 — Apex Trigger with Counter:**
Use a Custom Setting or Custom Metadata record to track a rotating index. An after-insert Apex trigger reads the current index, assigns the record to the corresponding user from a configured list, and increments (and wraps) the index. This approach is deterministic but requires Apex maintenance.

**Approach 2 — Queue + Omni-Channel:**
Assign all records to a queue via assignment rule, then enable Omni-Channel routing on that queue. Omni-Channel distributes work from the queue to available agents in a configurable pattern (least-active, most-available). This approach handles agent availability and capacity automatically without custom code.

**Approach 3 — Flow with Random Distribution:**
A record-triggered Flow can use a formula to compute a modulo value based on a counter stored in a Custom Setting, then set the Owner field. Less reliable for concurrency under high volume.

For production round-robin, Approach 1 (Apex) or Approach 2 (Omni-Channel) is preferred.

---

## Common Patterns

### Pattern: Region-Based Lead Assignment to Queues

**When to use:** Sales leads should be routed to regional queues (East, West, EMEA) based on State, Country, or Lead Source.

**How it works:**
1. Create a queue for each region. Add appropriate queue members.
2. Navigate to Setup → Lead Assignment Rules → New. Name the rule and mark it Active.
3. Create rule entries in order of specificity. Entry 1: `Lead Country = "Germany" OR Lead Country = "France"` → assign to EMEA Queue. Entry 2: `Lead State IN (NY, NJ, CT, MA)` → assign to East Queue. Continue for other regions. Final catch-all entry: no criteria → assign to Default Queue.
4. Confirm that Web-to-Lead forms use the active rule (they do automatically). Remind the sales team that UI-created leads require the assignment checkbox.

**Why not a single user:** Queues allow any member to accept the lead, providing flexibility when team members are unavailable.

### Pattern: Case Priority Routing with Escalation Queue

**When to use:** High-priority cases should go to a dedicated specialist queue; standard cases go to the general support queue.

**How it works:**
1. Create two queues: `Priority Support Queue` and `General Support Queue`. Add appropriate members.
2. Navigate to Setup → Case Assignment Rules → New. Name the rule and activate it.
3. Entry 1: `Case Priority = High AND Case Type = Technical` → Priority Support Queue.
4. Entry 2: `Case Origin = Email AND Case Subject contains "urgent"` → Priority Support Queue.
5. Entry 3: (no criteria — catch-all) → General Support Queue.
6. For Email-to-Case and Web-to-Case, the active rule runs automatically. For manually created cases, agents must check "Run assignment rules."

### Pattern: Apex Round-Robin for Lead Assignment

**When to use:** Leads must be distributed evenly among a fixed list of sales reps, and a queue-based approach is not suitable.

**How it works:**
```apex
trigger LeadAssignmentRoundRobin on Lead (before insert) {
    // Store the rep list and counter in Custom Metadata or Custom Settings
    Lead_Assignment_Config__mdt config = [
        SELECT Current_Index__c, Rep_Ids__c
        FROM Lead_Assignment_Config__mdt
        WHERE DeveloperName = 'Default' LIMIT 1
    ];
    List<String> repIds = config.Rep_Ids__c.split(',');
    Integer idx = (Integer)config.Current_Index__c;
    for (Lead l : Trigger.new) {
        if (l.OwnerId == null || l.OwnerId == UserInfo.getUserId()) {
            l.OwnerId = repIds[Math.mod(idx, repIds.size())];
            idx++;
        }
    }
    // Increment counter — requires separate DML on Custom Setting instance record
    // Use a queueable job to avoid mixed DML restriction
}
```

Note: Custom Metadata records are read-only at runtime — use a Custom Setting (Hierarchy or List) for the mutable counter. Be aware of concurrency: under high insert volume, parallel transactions may read the same index. Use `FOR UPDATE` or an Apex queueable with serialized updates for production-grade implementations.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Fixed territory routing (geography, account tier) | Assignment rule entries with filter criteria | Declarative, no code maintenance, up to 3,000 entries |
| Equal distribution among available agents | Queue + Omni-Channel routing | Handles availability and capacity; no custom code |
| Equal distribution with no Omni-Channel license | Apex trigger with Custom Setting counter | Deterministic but requires code ownership |
| Records created via API or Data Loader | Verify API header/DMLOptions are set | Rules do not auto-run without explicit trigger |
| High-volume records created in bulk | Queue assignment + Omni-Channel | Avoids Apex CPU limits from complex trigger logic |
| Time-sensitive escalation routing | Combine assignment rule (initial owner) + escalation rules (time-based re-route) | Assignment rules set initial owner; escalation rules handle SLA breach |

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

Run through these before marking assignment rule configuration complete:

- [ ] Confirm only one assignment rule is active for the object (Lead or Case)
- [ ] Rule entries are ordered from most specific to least specific; a catch-all entry is the last entry
- [ ] Each rule entry has been tested with a representative record matching and not matching its criteria
- [ ] All targeted queues exist and have at least one active member
- [ ] Email notifications are configured on rule entries where agents need to be alerted
- [ ] Web-to-Lead / Web-to-Case / Email-to-Case tested end-to-end: confirm records land in the correct queue or with the correct owner
- [ ] API-integration teams are informed that `Sforce-Auto-Assign: true` header (REST) or `AssignmentRuleHeader` (SOAP) is required
- [ ] Data Loader imports have `sfdc.assignmentRule` set if assignment is expected
- [ ] If round-robin Apex is used: test for concurrency behavior and verify no mixed-DML errors

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Only one active rule per object** — Activating a new rule silently deactivates the existing one. If a team maintains two rules (e.g., one for normal business and one for after-hours), they must manually toggle activation. There is no scheduling mechanism for rule activation.
2. **API and Data Loader do NOT trigger rules by default** — The most common integration failure: records imported via REST API, SOAP API, or Data Loader land with the API user as owner because no assignment header was passed. Every integration team must explicitly opt in to rule evaluation.
3. **Lookup filter criteria reference at time of rule entry creation** — Record type and queue picklist values shown in the rule entry criteria UI reflect the org state at the time you edit the entry. If a queue or record type is deleted after entry creation, the entry may produce unexpected behavior. Audit rule entries after deleting queues.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Configured assignment rule | Active rule with ordered, tested rule entries in Setup |
| Queue configuration | Named queues with correct membership, email address, and supported objects |
| Apex round-robin trigger | Trigger + Custom Setting implementation if native routing is insufficient |
| API integration notes | Documentation of required headers for each integration consuming the rule |

---

## Related Skills

- escalation-rules — use alongside assignment rules to handle time-based re-routing when SLA is breached after initial assignment
- user-management — queue membership requires active users; deactivated users should be removed from queue membership
- duplicate-management — assignment rules run before duplicate rules; duplicates may still land in the assigned queue
