---
name: apex-managed-sharing
description: "Sharing records programmatically via Apex: Share objects, row cause, sharing recalculation, with/without sharing patterns. NOT for declarative sharing rules (use sharing-and-visibility)."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Reliability
triggers:
  - "how do I share a record with a user programmatically in Apex"
  - "custom object share table insert row cause apex"
  - "sharing recalculation batch apex without sharing"
  - "apex managed sharing cleared after ownership change"
  - "how to create an apex sharing reason for a custom object"
tags:
  - apex-sharing
  - share-objects
  - row-cause
  - sharing-recalculation
  - programmatic-sharing
inputs:
  - Custom or standard object for which programmatic sharing is required
  - User or group IDs that need access
  - Desired access level (Read, Edit)
  - Whether a custom Apex sharing reason (row cause) is needed
outputs:
  - Share record DML (insert/delete of __Share or standard Share objects)
  - Apex sharing reason metadata definition guidance
  - Sharing recalculation batch class implementation
  - Checker report on Apex sharing patterns in existing classes
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# Apex Managed Sharing

This skill activates when a practitioner needs to grant or revoke record-level access programmatically using Apex — by directly inserting or deleting rows in a Share object — rather than through declarative sharing rules, manual sharing, or role hierarchy. Use it for territory-based sharing, dynamic cross-role access, or any scenario where the sharing grant logic belongs in code, not setup.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm the object's OWD (Org-Wide Default). Apex managed sharing only extends access beyond what OWD already grants. If OWD is Public Read/Write, programmatic sharing has no practical effect.
- Identify whether a custom Apex sharing reason is required (required for custom objects when you want the grant to survive manual sharing recalculation or when you need auditable row causes beyond `Manual`).
- Confirm that the Apex sharing reason has been created in Setup (Object Manager > Object > Apex Sharing Reasons) before trying to insert rows that reference it. Referencing a non-existent reason causes a runtime DML exception.
- Know the governor limits in play: 10,000 DML rows per synchronous transaction, 10,000 DML rows per batch execute method. Sharing recalculation frequently requires batch Apex.

---

## Core Concepts

### Share Object Anatomy

Every Salesforce object that supports sharing has a corresponding Share object. For standard objects the name is `<ObjectName>Share` (e.g., `AccountShare`, `OpportunityShare`). For custom objects the name is `<ObjectAPIName>__Share` (e.g., `Territory_Assignment__Share`).

Every Share record has four core fields:

| Field | Type | Description |
|---|---|---|
| `ParentId` | ID | The ID of the record being shared |
| `UserOrGroupId` | ID | The ID of the User, Role, or Group being granted access |
| `AccessLevel` | String | `Read`, `Edit`, or `All` (All = owner-level; rarely granted via Apex) |
| `RowCause` | String | Why the share was granted. `Manual` is the platform default. Custom reasons use the `__c` suffix. |

For custom objects there is also a `RowCause` value of `Owner` (auto-created by the platform) and any Apex sharing reasons you have defined.

### Apex Sharing Reasons (Custom Row Causes)

An Apex sharing reason is a metadata record created in Setup under Object Manager > [Custom Object] > Apex Sharing Reasons. Once created, its API name is available as a string constant on the Share object: `<ObjectAPIName>__Share.rowCause.<ReasonName>__c`.

Using a custom row cause instead of `Manual`:

- The platform preserves the rows during manual sharing recalculation (clicking Recalculate on the sharing reason).
- The rows are still cleared when the object's OWD changes or when a full sharing recalculation is triggered at the org level.
- The reason name becomes auditable — queries on the Share table can filter by `RowCause` to isolate Apex-managed grants.

Standard objects (Account, Opportunity, etc.) do not support custom Apex sharing reasons. For standard objects, use `RowCause = 'Manual'` (constant `Schema.OpportunityShare.rowCause.Manual`).

### with sharing / without sharing / inherited sharing

Apex class sharing keywords control whether the running user's record access is enforced for SOQL and DML inside that class:

- `with sharing` — enforces the user's sharing rules. Use for most user-facing code.
- `without sharing` — bypasses sharing rules. Required in sharing recalculation batch classes because the class must query every record regardless of the running user's access.
- `inherited sharing` — adopts the sharing mode of the calling context. Use in service/utility classes that may be called from both `with sharing` and `without sharing` contexts.

A critical point: inserting Share records does **not** require `without sharing`. Any Apex code that has access to the parent record's ID can insert a share row. The `without sharing` requirement applies specifically to the **query** step inside recalculation — to read all records being reshared.

### Sharing Recalculation

When programmatic sharing logic changes (e.g., territory assignments are restructured), stale share rows that were created with a custom row cause must be deleted and recreated. The platform provides a recalculation hook:

1. Create a class that implements `Database.Batchable<SObject>`.
2. Annotate it with `global class` and implement `start`, `execute`, and `finish`.
3. Declare the class `without sharing` so it can query all records.
4. In `execute`: delete existing share rows for the row cause, then insert fresh ones.
5. Register the class on the Apex Sharing Reason in Setup. This makes a Recalculate button appear on the sharing reason and allows the platform to call the class automatically when triggered.

The `start` method typically returns a `Database.QueryLocator` over the parent records; `execute` processes each batch of parent records, computes the correct users, and performs the share DML.

---

## Common Patterns

### Pattern 1: Insert Share Records from a Trigger

**When to use:** A trigger event (insert or update of a related record) determines which users gain access to a parent record. Example: an Account is shared with a partner when a Partner_Relationship__c record is created.

**How it works:**

1. Collect the `ParentId` values from the triggering records.
2. Query the Share table to determine which grants already exist (avoids duplicates).
3. Build a list of new Share sObjects for rows that do not yet exist.
4. Insert with `Database.insert(shareList, false)` to allow partial success (duplicate rows produce a `DUPLICATE_VALUE` error; using `false` lets other rows succeed).
5. For removals, query the Share table by `RowCause` and `ParentId`, then delete.

**Why not the alternative:** Using declarative Sharing Rules would require a static criteria field. When sharing logic depends on related-object data (junction records, custom metadata), declarative rules cannot model the relationship.

### Pattern 2: Full Sharing Recalculation via Batch Apex

**When to use:** The underlying sharing logic has changed at bulk (e.g., territory reassignment affecting thousands of records) and all existing Apex-managed share rows must be rebuilt.

**How it works:**

1. Implement `Database.Batchable<SObject>` declared `without sharing`.
2. In `start`, return a `Database.QueryLocator` for all parent records: `Database.getQueryLocator('SELECT Id FROM CustomObject__c')`.
3. In `execute`, for the batch scope:
   a. Collect the parent IDs.
   b. Delete all existing `CustomObject__Share` rows where `RowCause = CustomObject__Share.rowCause.TerritoryAccess__c` and `ParentId IN :parentIds`.
   c. Compute the correct users by querying the related assignment records.
   d. Insert new share rows.
4. Register the class as the recalculation class on the Apex Sharing Reason in Setup.

**Why not the alternative:** Running recalculation in a trigger context hits DML row limits immediately for large datasets. A batch job stays within per-execute limits and can run asynchronously.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Need to share a record with a specific user based on a junction record | Apex trigger inserts `__Share` row with custom row cause | Declarative sharing rules cannot model junction-record logic |
| Sharing logic has changed org-wide and all shares need rebuilding | Batch Apex recalculation class registered on sharing reason | Volume exceeds synchronous DML limits; batch stays within per-execute limits |
| Standard object (Account, Opportunity) needs programmatic sharing | Insert share row with `RowCause = 'Manual'` | Standard objects do not support custom Apex sharing reasons |
| A service method must read-then-share records in a mixed calling context | Declare service class `inherited sharing`; sharing class `without sharing` | Preserves caller's context for queries; bypasses for share DML only where needed |
| Share records must survive a manual recalculation run | Use a custom Apex sharing reason (not `Manual`) | `Manual` rows are cleared by manual sharing recalculation; custom row causes are preserved |
| Audit which records a user can access via Apex sharing | Query `__Share` filtered by `RowCause` | Row cause makes grants distinguishable from role-hierarchy or declarative grants |

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

Run through these before marking work in this area complete:

- [ ] OWD for the object is Private or Public Read Only — if OWD is Public Read/Write, Apex sharing has no effect
- [ ] Apex sharing reason is created in Setup before code that references it is deployed
- [ ] Share inserts use `Database.insert(list, false)` to handle `DUPLICATE_VALUE` gracefully
- [ ] Recalculation class is declared `without sharing` so all parent records are queryable
- [ ] Stale share rows are deleted before inserting fresh ones in recalculation (delete then insert, not upsert)
- [ ] Recalculation class is registered on the Apex sharing reason in Setup
- [ ] DML row count is within limits: 10,000 rows per synchronous transaction, 10,000 per batch execute

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Apex managed share rows are cleared on OWD change or full recalculation** — When an administrator changes the OWD for an object or runs a full sharing recalculation from Setup, all Apex-managed share rows for that object are deleted. The recalculation class registered on the Apex sharing reason is then called automatically to rebuild them. If no class is registered, the grants are permanently lost until manually re-triggered.

2. **`without sharing` is required in recalculation classes** — The recalculation class must query all parent records to rebuild shares. If the class runs `with sharing`, records the running user cannot see are silently excluded from the query scope, producing incomplete share coverage with no error thrown.

3. **Custom row causes must exist in Setup before deployment** — The `RowCause` value on a share row is validated at DML time against the Apex sharing reasons defined in Setup. Deploying code that references a custom row cause before the metadata record exists in the target org causes a `DmlException: FIELD_INTEGRITY_EXCEPTION` at runtime. Include the sharing reason in the deployment package or create it manually in Setup first.

4. **AccessLevel must be at least Read; `All` (owner-level) is only grantable via ownership change** — Valid values for `AccessLevel` via Apex are `Read` and `Edit`. `All` is reserved for the record owner and cannot be granted via a Share row insert. Attempting to insert a row with `AccessLevel = 'All'` throws a `DmlException`.

5. **Duplicate share rows cause `DUPLICATE_VALUE` errors** — The platform enforces a unique constraint on `(ParentId, UserOrGroupId, RowCause)`. Inserting a share row for a combination that already exists throws `DUPLICATE_VALUE`. Always query existing rows before inserting, or use `Database.insert(list, false)` and inspect `SaveResult` errors to handle duplicates gracefully.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Share record DML snippet | Apex code to insert or delete share rows for a given object |
| Sharing recalculation batch class | Full `Database.Batchable` implementation for rebuilding Apex-managed shares |
| Apex sharing reason setup guidance | Steps to create the sharing reason metadata in Setup before code deployment |
| `check_apex_managed_sharing.py` report | Static analysis of Apex classes for sharing patterns and common errors |

---

## Related Skills

- sharing-and-visibility — Use for declarative sharing rules, OWD decisions, role hierarchy design, and manual sharing; this skill handles programmatic extension of that foundation
- apex-security-patterns — Use alongside this skill when designing the `with sharing` / `without sharing` / `inherited sharing` class hierarchy for the full feature
- async-apex — Use when sharing recalculation volume requires batch or queueable patterns beyond what triggers can handle
