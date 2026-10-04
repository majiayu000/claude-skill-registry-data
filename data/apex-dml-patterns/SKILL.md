---
name: apex-dml-patterns
description: "Use when choosing between DML statements and Database class methods, handling partial success, or using Database.DMLOptions for assignment rules and duplicate handling. Trigger keywords: 'Database.insert allOrNone false', 'partial DML success apex', 'SaveResult isSuccess', 'database merge apex', 'DML exception handling'. NOT for savepoint placement and rollback after a failure — use apex/apex-savepoint-and-rollback. NOT for SOQL query patterns — use apex/soql-fundamentals."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - Performance
triggers:
  - "partial DML success apex Database.insert allOrNone false"
  - "SaveResult isSuccess getErrors loop apex bulk insert"
  - "database class vs DML statement apex exception handling"
  - "DmlOptions assignment rule header duplicate rule allow save"
  - "savepoint rollback apex multi-step DML transaction"
tags:
  - apex-dml
  - database-class
  - saveresult
  - partial-success
  - governor-limits
  - dml-options
  - savepoint
inputs:
  - "List of SObjects to insert/update/delete/upsert"
  - "Whether partial success (allOrNone=false) is required"
  - "Whether assignment rules, email headers, or duplicate suppression are needed"
outputs:
  - "List of SaveResult/UpsertResult/DeleteResult with per-row success/failure details"
  - "Merged or converted record references for Database.merge/convertLead"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-19
---

# Apex DML Patterns

Use this skill when selecting between DML statements (`insert`/`update`/`delete`/`upsert`) and `Database` class methods for bulk data operations — especially when partial success, savepoints, duplicate suppression, or assignment rule triggering is needed.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm whether partial success is acceptable: if any row failure must roll back all rows, use DML statements; if individual row failures should be tolerated, use `Database.insert(list, false)`.
- Check the 150 DML operations limit: one `Database.insert(list)` call with 200 records counts as **1 DML operation**, not 200.
- Identify whether assignment rules, email headers, or duplicate rules need to be controlled — these require `Database.DMLOptions`.

---

## Core Concepts

### DML statements vs. Database class methods

DML statements (`insert list`) use `allOrNone = true` by default: any row failure throws `DmlException` and rolls back the entire batch. `Database.insert(list, false)` enables partial success: failures on individual rows do **not** roll back the successful rows, but you must check each `SaveResult.isSuccess()` to determine which rows failed.

The governor limit is 150 DML **operations** per transaction — not rows. One `Database.insert(200-record list)` = 1 DML operation. This is the single most common misconception.

### SaveResult, UpsertResult, and error collection

`Database.insert(list, false)` returns `List<Database.SaveResult>`. For each result:

```apex
List<Database.SaveResult> results = Database.insert(records, false);
List<String> errors = new List<String>();
for (Database.SaveResult sr : results) {
    if (!sr.isSuccess()) {
        for (Database.Error err : sr.getErrors()) {
            errors.add(err.getMessage() + ' [' + err.getStatusCode() + ']');
        }
    }
}
```

`Database.upsert` returns `List<Database.UpsertResult>` with an additional `isCreated()` method distinguishing inserts from updates. `Database.delete` returns `List<Database.DeleteResult>`.

### Savepoint and rollback

`Savepoint sp = Database.setSavepoint()` creates a named rollback point. `Database.rollback(sp)` undoes all DML since that savepoint. Use this for multi-step operations where you want to rollback a logical unit without aborting the entire transaction:

```apex
Savepoint sp = Database.setSavepoint();
try {
    Database.insert(headersRecords);
    Database.insert(lineItemRecords);
} catch (DmlException e) {
    Database.rollback(sp);
    throw e;
}
```

Savepoints count against the DML statement limit.

### Database.DMLOptions

`Database.DMLOptions` controls side-effect behavior on a DML operation:

- `opt.assignmentRuleHeader.useDefaultRule = true` — fires the active assignment rule
- `opt.emailHeader.triggerAutoResponseEmail = false` — suppresses auto-response emails
- `opt.duplicateRuleHeader.allowSave = true` — bypasses duplicate rules (use with care)
- `opt.optAllOrNone = false` — equivalent to `allOrNone = false` flag

Pass options as the second argument: `Database.insert(list, opt)`.

---

## Common Patterns

### Bulk insert with partial success and error logging

**When to use:** Mass-creating records (e.g., from an external feed) where some rows may have invalid data and individual failures should not stop valid rows.

**How it works:**

```apex
List<Contact> contacts = buildContactsFromFeed(feedRows);
List<Database.SaveResult> results = Database.insert(contacts, false);

List<ProcessingError__c> errorLog = new List<ProcessingError__c>();
for (Integer i = 0; i < results.size(); i++) {
    if (!results[i].isSuccess()) {
        for (Database.Error err : results[i].getErrors()) {
            errorLog.add(new ProcessingError__c(
                SourceRow__c = feedRows[i].externalId,
                Message__c = err.getMessage(),
                StatusCode__c = String.valueOf(err.getStatusCode())
            ));
        }
    }
}
if (!errorLog.isEmpty()) {
    Database.insert(errorLog, false);
}
```

**Why not DML statement:** `insert contacts` throws on the first bad row and rolls back all successfully validated rows.

### Upsert with external ID field

**When to use:** Syncing records from an external system using a known external identifier.

**How it works:**

```apex
List<Account> accounts = buildAccountsFromSource(sourceData);
// ExternalId__c must be an indexed, external-ID-marked custom field
List<Database.UpsertResult> results =
    Database.upsert(accounts, Account.ExternalId__c, false);

for (Database.UpsertResult ur : results) {
    if (ur.isSuccess()) {
        System.debug(ur.isCreated() ? 'Inserted: ' : 'Updated: ' + ur.getId());
    }
}
```

**Why not insert:** Upsert atomically handles both new and existing records without a pre-query, saving SOQL and DML operations.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Any row failure must roll back all | `insert list` / DML statement | allOrNone=true (default) |
| Partial success acceptable | `Database.insert(list, false)` | Per-row error collection without rollback |
| Need assignment rule on insert | `Database.DMLOptions` with `assignmentRuleHeader` | DML statement does not expose this control |
| Suppress duplicate rule | `DMLOptions.duplicateRuleHeader.allowSave = true` | Bypass without disabling org-wide rule |
| Match on external Id for sync | `Database.upsert(list, ExternalId__c, false)` | Avoids pre-query, atomic insert/update |
| Hard delete (bypass Recycle Bin) | `Database.emptyRecycleBin(ids)` | Permanent delete, not a DML operation |
| Merge duplicate records | `Database.merge(master, duplicateIds)` | Account/Contact/Lead only |

---

## Recommended Workflow

1. **Determine allOrNone policy**: decide whether partial success is acceptable and choose DML statement (allOrNone=true) or `Database.insert(list, false)` accordingly.
2. **Build bulk list**: collect all records to process into a single list — never call DML inside loops.
3. **Select method**: use `Database` class if you need partial success, DMLOptions, or explicit result inspection; use DML statement for simpler all-or-nothing cases.
4. **Collect errors**: iterate `SaveResult`/`UpsertResult` list and collect failures into an error log or exception list.
5. **Apply savepoints** where multi-step DML must be atomically rolled back on failure.
6. **Set DMLOptions** if assignment rules, email suppression, or duplicate bypass is needed.
7. **Validate DML count**: confirm total DML operations in the transaction stay within 150; each `Database.insert(list)` call = 1 operation regardless of list size.

---

## Review Checklist

- [ ] No DML inside loops — all records collected into lists first
- [ ] DML operation count (not row count) verified under 150
- [ ] `SaveResult.isSuccess()` checked per row when `allOrNone=false`
- [ ] `DmlException` caught and re-thrown or logged at appropriate level
- [ ] `Database.DMLOptions` used where assignment rules or duplicate suppression is needed
- [ ] `Database.merge` only called for Account, Contact, or Lead
- [ ] Savepoints used when multi-step DML must be transactionally consistent

---

## Salesforce-Specific Gotchas

1. **DML limit counts operations, not rows** — one `Database.insert(200Records)` = 1 DML operation, not 200. The 150 limit applies to the number of distinct DML calls, not the total records processed. Confusion here leads to over-splitting lists unnecessarily.
2. **Partial success does NOT roll back successful rows** — when using `allOrNone=false`, rows that succeed are committed immediately. If you later discover you need to undo them, you must delete them explicitly; `Database.rollback()` only works within the same transaction.
3. **`Database.merge` is restricted to three objects** — `Database.merge` only supports Account, Contact, and Lead. Attempting to merge any other object type throws a `DmlException` at runtime with no compile-time warning.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| `List<Database.SaveResult>` | Per-row success/failure details from `Database.insert/update/delete` |
| Error log records | Custom error object populated with failure messages for audit trail |
| `check_apex_dml_patterns.py` | Validator confirming required method coverage in SKILL.md |

---

## Related Skills

- soql-fundamentals — for query patterns that precede DML in lookup-and-update flows
- apex-transaction-finalizers — for cleanup logic after Queueable DML failures
- apex-batch-chaining — for chaining batch jobs that each perform bulk DML
- callout-and-dml-transaction-boundaries — for the callout-before-DML restriction
