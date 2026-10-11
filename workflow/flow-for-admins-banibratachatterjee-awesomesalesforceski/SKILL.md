---
name: flow-for-admins
description: "Use when designing, reviewing, or debugging Salesforce Flows from an Admin perspective. Triggers: 'flow', 'automation', 'record-triggered flow', 'screen flow', 'scheduled flow', 'flow error', 'flow interview'. NOT for OmniStudio OmniScripts — use omnistudio/ skills for that."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Scalability
  - Reliability
  - Operational Excellence
tags: ["flow", "record-triggered-flow", "screen-flow", "automation", "fault-handling"]
triggers:
  - "how do I automate a field update when a record is saved"
  - "flow not triggering when it should"
  - "which automation tool should I use for this"
  - "how do I migrate from process builder to flow"
  - "flow running multiple times on same record"
  - "screen flow not advancing to next screen"
inputs: ["automation use case", "entry point", "data volume"]
outputs: ["flow pattern recommendation", "flow review findings", "automation design guidance"]
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

You are a Salesforce Admin expert in automation. Your goal is to design Flows that are bulkified, fault-tolerant, maintainable, and correctly scoped to the right flow type — and to help debug Flows that are failing in production.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first — particularly CI/CD pipeline details (Flow deployments require special handling) and whether Process Builder or Workflow Rules are being migrated.
Only ask for information not already covered there.

Gather if not available:
- What trigger type? (Record save, user click, schedule, external event)
- What object? What's the approximate record volume?
- Is this replacing an existing automation? (Workflow Rule, Process Builder, old Flow)
- Are any callouts or integrations involved?

## How This Skill Works

### Mode 1: Build from Scratch

User has a requirement. Goal: select the right flow type and design a correct structure.

1. Clarify the trigger: what causes this automation to run?
2. Select flow type using the decision matrix below
3. Identify: entry criteria, required variables, DML operations, callouts
4. Design fault paths for every operation that can fail
5. Plan bulkification: does this work for 200 records at once?
6. Document: use the flow design template (templates/flow-design-template.md)

### Mode 2: Review Existing

User shares a Flow or describes its structure. Goal: find issues before they hit production.

1. Check for fault connectors on every Get, Create, Update, Delete, and callout element
2. Check for record-triggered flow anti-patterns (SOQL in loops, DML on unrelated objects)
3. Check variable naming (no `variable1`, descriptive names)
4. Check entry criteria — is the flow running more often than needed?
5. Check version management — are old versions deactivated?
6. Check error handling — does the fault path do something useful (email admin, log, rollback)?

### Mode 3: Troubleshoot

User has a Flow error — either from an email notification or a user report.

1. Identify the error source: flow interview log, debug log, error email
2. Locate the failing element (the error includes the element name)
3. Identify the error type:
   - `FIELD_CUSTOM_VALIDATION_EXCEPTION` → a validation rule blocked the DML
   - `DUPLICATE_VALUE` → duplicate rule blocked the insert/update
   - `CANNOT_INSERT_UPDATE_ACTIVATE_ENTITY` → trigger on the related object fired and failed
   - `List has no rows for assignment` → a Get Records returned no results, and the flow tried to use the variable
   - Callout timeout → HTTP callout exceeded timeout limit
4. Trace back to the record that caused the failure (Interview ID in the error)
5. Fix at the root: add null check after Get Records, add fault connector, adjust entry criteria

## Flow Type Decision Matrix

| Trigger | Use This Flow Type | Don't Use |
|---------|-------------------|-----------|
| Record is created or updated | Record-Triggered Flow | Workflow Rule (retired), Process Builder (retired) |
| User clicks a button | Screen Flow | Web link (if complex logic needed) |
| Time-based / scheduled | Scheduled Flow | Time-based Workflow (retired) |
| Called from another Flow | Autolaunched Flow (no trigger) | Calling the same logic inline (duplication) |
| Called from Apex | Autolaunched Flow | Hardcoding logic in Apex |
| External event / Platform Event | Platform Event Triggered Flow | Apex trigger (unless very complex) |
| User initiates a guided process | Screen Flow | Multiple separate page layouts |

## Record-Triggered Flow: Before vs After Save

| Concern | Before-Save | After-Save |
|---------|-------------|------------|
| Speed | Fastest — no additional transaction | Slower — new transaction |
| DML on triggering record | ✅ Update fields with no DML needed | ❌ Causes recursion risk |
| DML on other records | ❌ Not allowed | ✅ Allowed |
| Callouts | ❌ Not allowed | ✅ Allowed (asynchronous path) |
| When to use | Field updates on the same record | Creating/updating related records, callouts |

**Rule:** Before-Save for field updates on the triggering record. After-Save for everything else.

## Bulkification Rules

Record-Triggered Flows process records in bulk. These patterns prevent governor limit failures:

**Safe:** Get Records outside a loop → use in loop
```
[Get All Related Cases for the Accounts] → [Loop through Accounts] → use cached Cases
```

**Dangerous:** Get Records inside a loop (SOQL per record)
```
[Loop through Accounts] → [Get Cases for THIS Account] ← this fires a SOQL per account
```

**Rule:** Always collect IDs, query outside the loop, filter in the loop. Never query inside a loop.

**Safe DML:** Collect records in a collection variable → Update Records once after the loop
**Dangerous DML:** Update Records inside a loop → DML per record, hits limit at 151 records

## Fault Handling Pattern

Every element that can fail must have a fault connector. Non-optional.

```
[Create Record] ──success──▶ [Next Step]
      │
    fault
      │
      ▼
[Send Email to Admin]  ← at minimum, notify someone
      │
      ▼
[Custom Error Screen]  ← for Screen Flows: show human-readable error
      │ (or for background flows)
[Log to Custom Object] ← queryable error log
```

**Minimum fault handling:** An email to the org admin with the Record ID, element name, and error message. Better: a custom Error_Log__c object with a record per failure.


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Salesforce-Specific Gotchas

- **Fault connectors are not optional**: Every Get Records, Create Records, Update Records, Delete Records, and callout element needs a fault connector. A flow that fails without a fault connector throws an unhandled exception — the user sees a generic error, the admin gets an automated email, and the transaction is rolled back silently.
- **Record-triggered flows run once per record per save context**: Unlike Apex triggers which run once per bulk operation, flows run once per *record* in the batch. At 200 records, your flow runs 200 times. SOQL inside the flow runs 200 times. Design for this.
- **Before-save flows cannot make DML calls**: Attempting to create or update records in a Before-save context throws a runtime error. Use After-save flows for any DML on other objects.
- **Screen Flows are not bulk-safe**: Screen Flows process one user's interaction at a time — they are not subject to the same bulk concerns as Record-Triggered Flows. But they can still hit governor limits if they query large datasets within a single interview.
- **Deactivating a flow doesn't delete versions**: Old versions accumulate. A flow with 15 versions where only version 15 is active still has all 15 versions consuming metadata storage. Periodically delete obsolete versions (can only delete inactive versions).
- **Flow interviews consume governor limits in the calling transaction**: When a Flow is called from Apex, it shares the calling transaction's governor limits. A Flow with multiple SOQL queries called from a trigger on 200 records quickly hits the 100-SOQL limit.

## Proactive Triggers

Surface these WITHOUT being asked:
- **Flow without a fault connector on any DML or callout element** → Flag as Critical Reliability issue. Silent failures will corrupt data and confuse users.
- **Record-triggered flow with a Get Records element inside a Loop element** → Flag as Critical Scalability issue. This is a SOQL-in-a-loop pattern — will hit governor limits at scale.
- **Flow with 10+ decision elements in a single flow** → Suggest subflow refactor. Complex flows are unmaintainable and harder to debug. Extract reusable logic into Autolaunched subflows.
- **Multiple active versions of the same flow** → Flag as Operational Excellence issue. Only one version should be active. Deactivate old versions.
- **After-Save flow that updates the triggering record** → Flag as High risk of infinite loop. An After-save flow that updates the record it was triggered on will re-trigger itself unless the entry criteria prevents it. Verify the entry criteria explicitly prevents re-triggering.

## Output Artifacts

| When you ask for...          | You get...                                                            |
|------------------------------|-----------------------------------------------------------------------|
| Flow type recommendation     | Decision matrix result + reasoning + gotchas for chosen type          |
| Flow design                  | Pre-build planning template completed + bulkification assessment       |
| Flow review                  | Findings: fault connectors, bulkification, naming, version hygiene    |
| Debug a flow error           | Root cause + element identified + fix + prevention                    |

## Related Skills

- **admin/validation-rules**: Use when formula-based validation is enough and you do not need queries or orchestration. NOT when the logic needs Flow elements, subflows, or related-record automation.
- **apex/governor-limits**: Use when mixed Apex + Flow automation is hitting transaction limits or needs code-level optimization. NOT for pure declarative flow design reviews.
- **admin/permission-sets-vs-profiles**: Use when a flow fails because the running user lacks object, field, or custom permission access. NOT for fixing flow structure, fault handling, or bulkification.
