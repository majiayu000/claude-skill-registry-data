---
name: case-trigger-patterns
description: "Use when writing Apex triggers on the Case object — specifically for invoking assignment rules programmatically, auto-associating entitlements in a trigger, handling merge trigger behavior on losing records, or understanding why milestone completion does not fire automatically when a case closes. Trigger keywords: 'case trigger', 'case assignment rule apex', 'entitlement auto-association trigger', 'case merge trigger', 'MasterRecordId case', 'Database.DmlOptions AssignmentRuleHeader', 'milestone not completing on case close'. NOT for generic trigger framework architecture — use apex/trigger-framework for that. NOT for configuring assignment rules in Setup — use admin/assignment-rules. NOT for SLA configuration or entitlement process design — use admin/entitlements-and-milestones."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Operational Excellence
  - Security
triggers:
  - "case assignment rule not firing when I insert a case from Apex"
  - "how do I auto-associate an entitlement when a case is created from Apex"
  - "case merge trigger behavior — which records fire and what is MasterRecordId"
  - "milestone is not completing when I close a case in Apex"
  - "Database.DmlOptions AssignmentRuleHeader case trigger"
tags:
  - case-trigger
  - assignment-rules
  - entitlement
  - milestones
  - merge-trigger
  - Database.DmlOptions
  - MasterRecordId
  - service-cloud
inputs:
  - "Case record context (insert, update, merge, or close operation being performed)"
  - "Whether assignment rules exist and which rule Id should be invoked"
  - "Whether entitlements are enabled and EntitlementContact junction records are used"
  - "Whether a trigger framework is already present in the org"
outputs:
  - "Apex trigger and handler code for Case with correct assignment rule invocation"
  - "Before-insert/update handler for entitlement auto-association"
  - "Guidance on merge trigger firing order and MasterRecordId behavior"
  - "Guidance on the milestone completion gap when closing cases"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-06
---

# Case Trigger Patterns

This skill activates when a practitioner needs Apex trigger logic specific to the Case object, covering four non-obvious platform behaviors: DML from Apex bypasses case assignment rules by default; entitlement auto-association requires an explicit Before Insert/Update query; merge operations fire delete triggers on losing records with a populated `MasterRecordId`; and closing a case does not automatically complete open milestones.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm whether case assignment rules exist in the org and whether you need the active rule or a specific rule by Id. `Database.DmlOptions.AssignmentRuleHeader` accepts either the active rule flag or a specific rule Id.
- Verify whether Entitlements are enabled (Setup > Entitlement Settings). If enabled, check whether EntitlementContact junction records are being used to restrict which accounts or contacts are covered by each entitlement.
- Identify whether a case merge operation is in scope. Merge fires `before delete` and `after delete` on losing records, not a dedicated merge event. `MasterRecordId` on the losing record identifies the winner.
- Determine whether Entitlement Process milestones are active on cases in scope. Milestones do not auto-complete when a case is closed — any process requiring milestone completion at case close needs explicit Apex or a Flow.

---

## Core Concepts

### Assignment Rule Bypass by Default

When Apex performs DML on Case records — `insert`, `update`, or `upsert` — Salesforce does **not** invoke case assignment rules. This is documented behavior: DML operations issued programmatically bypass assignment rule evaluation unless you explicitly opt in via `Database.DmlOptions`.

To invoke the active rule, create a `Database.DmlOptions` instance, set `assignmentRuleHeader.useDefaultRule = true`, and pass the options to the DML call. To invoke a specific rule by Id, set `assignmentRuleHeader.assignmentRuleId` to the rule's 18-character Id instead.

This differs from UI behavior: a user saving a Case via the Lightning record page can choose to trigger assignment rules. Apex does not replicate that behavior automatically.

### Entitlement Auto-Association Pattern

When an Account-based entitlement process is in place, Salesforce can auto-associate an entitlement at case creation only if the org is configured to do so and the correct entitlement covers the account. However, when granular EntitlementContact junction records are used — where entitlement coverage is contact-specific, not account-wide — the platform cannot determine the correct entitlement automatically.

The trigger-based pattern for this situation is a `Before Insert` (and optionally `Before Update`) trigger that queries `EntitlementContact` for the junction records linking the case's contact to an active entitlement, then sets `Case.EntitlementId` before the record is saved. Doing this in a `Before` trigger avoids an extra update DML operation.

### Merge Trigger Behavior and MasterRecordId

When two Case records are merged in Salesforce (via the UI or via Apex `merge` DML), the platform fires:

- `before delete` and `after delete` on the **losing** record(s), not a "merge" event
- `before update` and `after update` on the **winning** (master) record

Inside a `before delete` or `after delete` trigger on Case, `Trigger.new` and `Trigger.newMap` are null. Use `Trigger.old` and `Trigger.oldMap`. On the losing record, `MasterRecordId` is populated with the Id of the winning record. A merge trigger can use this field to determine whether the delete is a merge (non-null `MasterRecordId`) or a true delete (null `MasterRecordId`).

The Apex Developer Guide explicitly states: "In a merge operation, triggers fire on the losing record (as a delete) and on the winning record (as an update)."

### Milestone Completion Gap at Case Close

Entitlement Process milestones attached to a case do not automatically reach `Completed` status when the case's `Status` is set to a closed value. Each milestone has its own completion criteria defined in the entitlement process, but if those criteria are met by closing the case, the platform evaluates the entitlement process asynchronously. In practice, reporting on milestone completion in the same transaction as the case close will see milestones still open.

If business requirements demand that all open milestones are completed when a case closes, the correct approach is an `After Update` trigger (or Flow) that detects the case transitioning to a closed status, then queries `CaseMilestone` records for that case where `IsCompleted = false` and updates `CaseMilestone.CompletionDate` to the current datetime.

---

## Common Patterns

### Pattern 1: Invoking Case Assignment Rules from an Apex Trigger or Service

**When to use:** A trigger, Batch Apex job, or integration service inserts or updates Case records and the assignment rule must fire to route the case to the correct queue or user.

**How it works:** Set `Database.DmlOptions.assignmentRuleHeader.useDefaultRule = true` and pass the options to the DML call. This can be done either directly in the trigger (less common) or in the service class / handler that performs the DML.

```apex
// In a service class or trigger handler performing the insert
Database.DmlOptions opts = new Database.DmlOptions();
opts.assignmentRuleHeader.useDefaultRule = true;

List<Case> casesToInsert = new List<Case>{ /* ... */ };
Database.insert(casesToInsert, opts);
```

To use a specific rule Id:
```apex
Database.DmlOptions opts = new Database.DmlOptions();
opts.assignmentRuleHeader.assignmentRuleId = '01Q000000000001AAA'; // 18-char rule Id
Database.insert(casesToInsert, opts);
```

Note: `Database.DmlOptions` cannot be passed to the Apex `insert` DML keyword. Use `Database.insert()` to supply options.

**Why not the alternative:** Relying on the `insert` keyword (without DML options) silently skips assignment rules. Cases end up unassigned or assigned to the default owner. The failure is silent — no error, no warning, no log.

---

### Pattern 2: Entitlement Auto-Association in a Before Insert Trigger

**When to use:** The org uses contact-specific entitlement coverage (`EntitlementContact` junction records) and the platform cannot determine the correct entitlement automatically at case creation.

**How it works:** In `Before Insert`, query `EntitlementContact` for active entitlements linked to the case's `ContactId`, then set `Case.EntitlementId` on the record before it is committed.

```apex
trigger CaseTrigger on Case (before insert, before update, after update, after delete) {
    if (Trigger.isBefore && Trigger.isInsert) {
        CaseTriggerHandler.associateEntitlements(Trigger.new);
    }
    // ... other context routing
}
```

```apex
public with sharing class CaseTriggerHandler {

    public static void associateEntitlements(List<Case> newCases) {
        // Collect ContactIds for cases that have no entitlement yet
        Set<Id> contactIds = new Set<Id>();
        for (Case c : newCases) {
            if (c.ContactId != null && c.EntitlementId == null) {
                contactIds.add(c.ContactId);
            }
        }
        if (contactIds.isEmpty()) return;

        // Query EntitlementContact for active entitlements linked to these contacts
        Map<Id, Id> contactToEntitlement = new Map<Id, Id>();
        for (EntitlementContact ec : [
            SELECT ContactId, EntitlementId
            FROM EntitlementContact
            WHERE ContactId IN :contactIds
              AND Entitlement.Status = 'Active'
              AND Entitlement.EndDate >= TODAY
            LIMIT 1000
        ]) {
            // Take the first active entitlement per contact
            if (!contactToEntitlement.containsKey(ec.ContactId)) {
                contactToEntitlement.put(ec.ContactId, ec.EntitlementId);
            }
        }

        // Stamp EntitlementId before insert DML commits
        for (Case c : newCases) {
            if (c.EntitlementId == null && contactToEntitlement.containsKey(c.ContactId)) {
                c.EntitlementId = contactToEntitlement.get(c.ContactId);
            }
        }
    }
}
```

**Why not the alternative:** Doing this in `After Insert` requires a follow-up `update` DML call on the same cases, which consumes extra DML statements and can re-trigger downstream logic. `Before Insert` field assignment avoids the extra DML.

---

### Pattern 3: Distinguishing Merge Deletes from True Deletes in a Case Trigger

**When to use:** Logic in a `before delete` or `after delete` trigger on Case must behave differently for merged records (which have a surviving master) versus permanently deleted records.

**How it works:** Check `MasterRecordId` on the losing record. A non-null `MasterRecordId` indicates a merge; a null value indicates a true delete.

```apex
trigger CaseTrigger on Case (before delete, after delete) {
    if (Trigger.isBefore && Trigger.isDelete) {
        CaseTriggerHandler.onBeforeDelete(Trigger.old);
    }
    if (Trigger.isAfter && Trigger.isDelete) {
        CaseTriggerHandler.onAfterDelete(Trigger.old, Trigger.oldMap);
    }
}
```

```apex
public with sharing class CaseTriggerHandler {

    public static void onBeforeDelete(List<Case> oldCases) {
        for (Case c : oldCases) {
            if (c.MasterRecordId != null) {
                // This is a merge — c is a losing record being absorbed by c.MasterRecordId
                // Example: copy attachments or related records to the master before the delete commits
            } else {
                // True delete — run permanent deletion logic
            }
        }
    }

    public static void onAfterDelete(List<Case> oldCases, Map<Id, Case> oldMap) {
        // Similar pattern: MasterRecordId != null means merge, null means true delete
    }
}
```

**Why not the alternative:** Without checking `MasterRecordId`, merge-delete logic runs the same path as permanent deletes, potentially purging data that should have been migrated to the master record or triggering cleanup workflows on records that still have a surviving counterpart.

---

### Pattern 4: Completing Open Milestones When a Case Closes

**When to use:** Business rules require all open entitlement process milestones to be marked complete when a case is set to a closed status.

**How it works:** In `After Update`, detect cases transitioning to `IsClosed = true`, query their open `CaseMilestone` records, and set `CompletionDate` to close them.

```apex
public with sharing class CaseTriggerHandler {

    public static void completeMilestonesOnClose(
            List<Case> newCases, Map<Id, Case> oldMap) {
        Set<Id> closingCaseIds = new Set<Id>();
        for (Case c : newCases) {
            if (c.IsClosed && !oldMap.get(c.Id).IsClosed) {
                closingCaseIds.add(c.Id);
            }
        }
        if (closingCaseIds.isEmpty()) return;

        List<CaseMilestone> toComplete = [
            SELECT Id, CompletionDate
            FROM CaseMilestone
            WHERE CaseId IN :closingCaseIds
              AND IsCompleted = false
        ];

        if (toComplete.isEmpty()) return;

        Datetime now = Datetime.now();
        for (CaseMilestone cm : toComplete) {
            cm.CompletionDate = now;
        }
        update toComplete;
    }
}
```

**Why not the alternative:** Leaving milestones open after a case closes breaks SLA reporting, causes milestone violation alerts on closed cases, and produces inaccurate entitlement process statistics. The platform's asynchronous milestone evaluation does not guarantee completion in the same transaction.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Need assignment rules to fire when inserting cases from Apex | `Database.DmlOptions` with `useDefaultRule = true` | DML keyword silently bypasses rules; `Database.insert()` with options is required |
| Need a specific assignment rule, not the active one | `assignmentRuleHeader.assignmentRuleId` | Allows pinning to a rule by Id; useful in multi-rule orgs |
| Entitlement coverage is account-wide | Rely on platform auto-association | Platform can resolve entitlement by Account without a trigger |
| Entitlement coverage is contact-specific (EntitlementContact) | Before Insert trigger querying EntitlementContact | Platform cannot resolve without the junction query |
| Delete trigger must distinguish merge from true delete | Check `MasterRecordId` on `Trigger.old` records | Only reliable way; no dedicated merge event exists |
| Milestones must be completed when case closes | After Update trigger setting `CaseMilestone.CompletionDate` | Platform does not auto-complete milestones in the same transaction as case close |
| Existing trigger framework in org | Add new Case logic to existing handler | One trigger per object; do not create a second `CaseTrigger` |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Audit the org context** — Check whether a Case trigger already exists. If one does, add new logic inside the existing handler. Confirm whether assignment rules, entitlements, and entitlement processes are active. Identify which of the four patterns (assignment rules, entitlement association, merge handling, milestone completion) are in scope.
2. **Implement assignment rule invocation** — If cases are inserted or updated via Apex and must respect assignment rules, switch from the `insert`/`update` keyword to `Database.insert()`/`Database.update()` with `Database.DmlOptions` set to `useDefaultRule = true` (or a specific rule Id). Apply this in the service or handler layer, not in the trigger body itself.
3. **Implement entitlement association** — If contact-specific entitlement coverage is required, add a `Before Insert` (and optionally `Before Update`) handler that queries `EntitlementContact` for the case's `ContactId` and stamps `Case.EntitlementId` before the DML commits. Guard with a null check to avoid overwriting existing entitlement assignments.
4. **Implement merge delete handling** — If delete-trigger logic must treat merged records differently from permanent deletes, add a null check on `MasterRecordId` in the `before delete` or `after delete` context. Document this guard explicitly with a comment so future maintainers understand the intent.
5. **Implement milestone completion** — If milestones must complete at case close, add an `After Update` handler that detects the `IsClosed` flip, queries open `CaseMilestone` records for the affected cases, and sets `CompletionDate` to `Datetime.now()`.
6. **Write test coverage** — Test each pattern independently: insert a case and assert the owner changed (assignment rule); insert a case with a ContactId linked to an EntitlementContact and assert `EntitlementId` is set; perform a merge and assert `MasterRecordId` behavior in delete context; close a case and assert `CaseMilestone.IsCompleted` is true.
7. **Run validation** — Execute `python3 scripts/skill_sync.py --skill skills/apex/case-trigger-patterns` and confirm no errors before marking work complete.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] All Case DML that requires assignment rules uses `Database.insert()`/`Database.update()` with `Database.DmlOptions`, not the `insert`/`update` keyword
- [ ] Entitlement association logic runs in `Before Insert` to avoid extra update DML
- [ ] Merge delete handler checks `MasterRecordId` to distinguish merge from true delete
- [ ] Milestone completion logic queries `CaseMilestone` with `IsCompleted = false` and sets `CompletionDate`
- [ ] No second `CaseTrigger` has been created if one already exists — logic is in the existing handler
- [ ] All handler methods are bulkified — no SOQL or DML inside loops
- [ ] Test class covers all four patterns with positive and guard-condition assertions

---

## Salesforce-Specific Gotchas

1. **Apex DML silently bypasses case assignment rules** — Using the `insert` or `update` keyword (rather than `Database.insert()`/`Database.update()` with options) does not invoke assignment rules. The case is created without routing. There is no error or warning — the silent failure only surfaces when cases remain unassigned in production. Always use `Database.DmlOptions` when assignment rule evaluation is required.

2. **Closing a case does not auto-complete its milestones** — When `Case.Status` transitions to a closed value, open `CaseMilestone` records for that case are not automatically set to `IsCompleted = true`. The entitlement process evaluates milestones asynchronously; in the same transaction as the close, milestones remain open. Any logic that reads milestone completion status in the same transaction as the close will see stale data unless the trigger explicitly updates `CaseMilestone.CompletionDate`.

3. **Merge fires delete triggers, not a merge event** — There is no `ismerge` or `mergeResult` context in an Apex trigger. The only way to detect a merge inside a delete trigger is to check `MasterRecordId` on the losing record. Triggers that perform cleanup or archival on delete without this check will incorrectly process merged records as permanently deleted.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| `CaseTrigger.trigger` | Minimal trigger body routing to handler by context |
| `CaseTriggerHandler.cls` | Handler class with methods for each pattern: `associateEntitlements`, `completeMilestonesOnClose`, `onBeforeDelete`/`onAfterDelete` with merge guard |
| `CaseService.cls` | Optional service class encapsulating `Database.insert()` with `DmlOptions` for cases requiring assignment rule invocation |
| `CaseTriggerHandlerTest.cls` | Test class covering all four patterns with assertions on owner, entitlement, merge behavior, and milestone completion |

---

## Related Skills

- `apex/trigger-framework` — Use when a trigger framework is already in the org or when deciding how to structure the handler. This skill assumes framework selection is done; it focuses on Case-specific logic inside the handler.
- `admin/assignment-rules` — Use for configuring lead or case assignment rule criteria and rule entries in Setup. This skill assumes rules exist and covers only the Apex invocation.
- `admin/entitlements-and-milestones` — Use for setting up entitlement processes, milestone criteria, and entitlement fields in Setup. This skill covers only the Apex trigger patterns for associating entitlements and completing milestones.
- `apex/opportunity-trigger-patterns` — A parallel skill covering non-obvious trigger behaviors on Opportunity (forecast category recalculation, split handling). Same structural pattern.
