---
name: assignment-rules
description: "Use this skill when configuring or troubleshooting Lead or Case assignment rules in Salesforce: creating rule entries, setting filter criteria, assigning records to users or queues, understanding when rules run, and implementing round-robin patterns with Apex. Trigger keywords: lead assignment, case assignment, assignment rule, queue assignment, auto-assign. NOT for creating the queue or public group a rule routes into — use admin/queues-and-public-groups. NOT for Omni-Channel or skills-based routing — use admin/omni-channel-routing-setup. NOT for approval routing — use admin/approval-processes."
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
  - "assignment rules isn't working"
  - "we're having issues with assignment rules"
  - "deploy lead assignment rules from sandbox to production"
  - "assignmentRules-meta.xml example for case assignment"
  - "assignment rules metadata xml example to deploy with sf cli"
  - "write an Apex test that checks the assignment rule set the owner"
  - "should I use assignment rules or omni-channel or flow to route cases"
  - "auto-response sender same as email-to-case routing address loop"
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
version: 1.1.2
author: Pranav Nagrecha
updated: 2026-09-12
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

## Questions to Ask Before Configuring

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "How do Leads or Cases arrive: web form, email, UI, API, Data Loader, Flow?" | Only the web and email intake channels invoke the rule by default; every other channel must opt in | The channel matrix and the header each integration must send |
| "Is there an active rule today, and who owns it?" | Activating yours silently deactivates theirs | A cutover plan instead of a surprise |
| "Which field values decide the owner, and are they set at save time?" | Criteria read values at save; formulas and after-save Flows are not there yet | Routing on plain fields the intake populates |
| "Queue or person, and what happens when nobody matches?" | Person targets break on leave and departures; unmatched records go to the default owner silently | Queue targets and a catch-all entry |
| "Does anything else write `OwnerId` after save?" | After-save Flows, triggers, Omni-Channel and escalation all overwrite the rule's result | One authoritative writer |
| "Should the customer get an acknowledgement?" | Auto-response fires only when the assignment rule fires, from a verified org-wide address | Auto-response wired to the same channels, not bolted on later |

A proper assignment configuration adds deterministic ownership on every creation channel, a visible fallback for unmatched records, and a rule file that deploys between orgs; "just creating a rule" routes web forms and leaves the API and UI paths unrouted. Comparison with the other routing mechanisms: `references/routing-selector.md`.

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

**When to use:** Leads must be distributed evenly among a fixed rep list, Omni-Channel is not licensed or not wanted for Leads, and the rotation must survive concurrent inserts.

**Ask first:** who maintains the rep list (Custom Metadata is admin-editable and deployable; the counter must be writable at run time, so it lives in a List Custom Setting); what happens when a rep is inactive or on leave (skip inactive users, and keep a "pause" flag per rep); which creation paths should rotate (usually only records that arrived owned by the integration or default user).

**How it works:**

```apex
// Trigger delegates; keep the logic in a handler you can unit-test.
trigger LeadTrigger on Lead (before insert) {
    LeadRoundRobin.assign(Trigger.new);
}

public with sharing class LeadRoundRobin {

    // Rep list: Custom Metadata (deployable, admin-editable, read-only at run time).
    // Counter: List Custom Setting, one record, writable and lockable.
    public static void assign(List<Lead> leads) {
        List<Lead> toRoute = new List<Lead>();
        for (Lead l : leads) {
            // Only rotate records nobody routed on purpose.
            if (l.OwnerId == null || l.OwnerId == UserInfo.getUserId()) {
                toRoute.add(l);
            }
        }
        if (toRoute.isEmpty()) return;

        List<Id> reps = activeReps();
        if (reps.isEmpty()) return;   // leave the default owner; do not throw in a trigger

        // FOR UPDATE serialises concurrent transactions on the counter row.
        Round_Robin_Counter__c counter = [
            SELECT Id, Last_Index__c FROM Round_Robin_Counter__c
            WHERE Name = 'Lead' LIMIT 1 FOR UPDATE
        ];
        Integer idx = counter.Last_Index__c == null ? 0 : counter.Last_Index__c.intValue();

        for (Lead l : toRoute) {
            l.OwnerId = reps[Math.mod(idx, reps.size())];
            idx++;
        }
        counter.Last_Index__c = Math.mod(idx, reps.size());
        update counter;   // one DML for the whole batch; custom settings are not setup objects, so no mixed-DML
    }

    private static List<Id> activeReps() {
        Set<Id> configured = new Set<Id>();
        for (Round_Robin_Rep__mdt r : [
            SELECT User_Id__c FROM Round_Robin_Rep__mdt WHERE Object__c = 'Lead' AND Paused__c = false ORDER BY Sort_Order__c
        ]) {
            configured.add((Id) r.User_Id__c);
        }
        List<Id> reps = new List<Id>();
        for (User u : [SELECT Id FROM User WHERE Id IN :configured AND IsActive = true ORDER BY Id]) {
            reps.add(u.Id);
        }
        return reps;
    }
}
```

**What to expect:** the counter row is locked for the duration of each transaction, so parallel bulk loads queue up briefly instead of double-assigning; the update is one DML per transaction regardless of batch size; a rep removed from the metadata or deactivated drops out of the rotation on the next insert. Records that already carry a deliberate owner are left alone.

**Why not the alternatives:** an assignment rule cannot rotate (one target per entry, see `references/llm-anti-patterns.md`); a Flow counter has no row lock and double-assigns under concurrent inserts; Custom Metadata cannot hold the counter because it is read-only at run time.

**Test it:** insert 10 leads in one transaction and assert the owners cycle through the rep list; insert one lead with an explicit owner and assert it is unchanged; deactivate a rep and assert they are skipped (`references/testing.md` has the assignment-header tests to sit alongside).

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

For the full comparison against Omni-Channel, Flow, Apex, Enterprise Territory Management, lead scoring, and third-party routing products, read `references/routing-selector.md` before choosing.

---


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the object (Lead or Case), how records are created, the currently active rule, and whether anything else writes `OwnerId`
2. Choose the mechanism — confirm with `references/routing-selector.md` that an assignment rule is the right layer, and check the official sources in `references/well-architected.md`
3. Design the entries — most specific first, catch-all last, queue targets over user targets; capture them in `templates/assignment-rules-template.md`
4. Build as metadata — shape the file from `references/metadata-examples.md` and run `scripts/check_assignment_rules.py` on the folder
5. Test — the Apex test and channel matrix in `references/testing.md`; every creation channel gets one record
6. Deploy and hand over — follow `references/migration-and-sandbox.md` for deploy order and the post-deploy checklist; when a rule "didn't fire" later, start at `references/troubleshooting.md`

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
- [ ] Auto-response `senderEmail`/`replyToEmail` is a distinct OrgWideEmailAddress, never an Email-to-Case routing address — run `scripts/check_assignment_rules.py` (`AR-LOOP-01`/`AR-LOOP-02`) to confirm

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Only one active rule per object** — Activating a new rule silently deactivates the existing one. If a team maintains two rules (e.g., one for normal business and one for after-hours), they must manually toggle activation. There is no scheduling mechanism for rule activation.
2. **API and Data Loader do NOT trigger rules by default** — The most common integration failure: records imported via REST API, SOAP API, or Data Loader land with the API user as owner because no assignment header was passed. Every integration team must explicitly opt in to rule evaluation.
3. **Lookup filter criteria reference at time of rule entry creation** — Record type and queue picklist values shown in the rule entry criteria UI reflect the org state at the time you edit the entry. If a queue or record type is deleted after entry creation, the entry may produce unexpected behavior. Audit rule entries after deleting queues.
4. **Auto-response `senderEmail` equal to the Email-to-Case routing address loops mail** — reusing the intake address as the acknowledgement sender routes every reply straight back into a new Case (`references/gotchas.md` #6; checked by `scripts/check_assignment_rules.py` rule `AR-LOOP-01`).

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Configured assignment rule | Active rule with ordered, tested rule entries in Setup |
| Queue configuration | Named queues with correct membership, email address, and supported objects |
| Apex round-robin trigger | Trigger + Custom Setting implementation if native routing is insufficient |
| API integration notes | Documentation of required headers for each integration consuming the rule |
| Deployable metadata | `assignmentRules/<Object>.assignmentRules-meta.xml` (plus auto-response and escalation files) shaped per `references/metadata-examples.md` |
| Test evidence | Apex test class and channel matrix results from `references/testing.md` |

---

## Reference Files

| File | Read it when |
|---|---|
| `references/routing-selector.md` | Deciding between assignment rules, Omni-Channel, Flow, Apex, territories, scoring |
| `references/metadata-examples.md` | Writing or reviewing the deployable XML for assignment, auto-response, and escalation rules |
| `references/troubleshooting.md` | A rule or auto-response "didn't fire" |
| `references/testing.md` | Proving the rule routes correctly from Apex and from every channel |
| `references/migration-and-sandbox.md` | Moving rules between orgs, sandbox refresh, deploy order |
| `references/gotchas.md` | The five platform behaviours that cause most production incidents |

---

## Related Skills

- admin/escalation-rules — time-based re-routing after initial assignment when an SLA is breached
- admin/queues-and-public-groups — the queues rule entries route into; queue membership requires active users
- admin/omni-channel-routing-setup — distributing queued work to available agents by presence and capacity
- admin/case-management-setup and admin/email-to-case-configuration — Case intake channels and the auto-response dependency
- admin/lead-management-and-conversion — Web-to-Lead, lead auto-response, and conversion ownership
- apex/apex-dml-patterns — `Database.DMLOptions` and the assignment header from Apex
- flow/flow-record-save-order-interaction — where the rule sits relative to before-save and after-save automation
- devops/sandbox-refresh-and-templates — what a refresh does to usernames and sandbox-only rules
- admin/duplicate-management — assignment rules run before duplicate rules; duplicates may still land in the assigned queue
