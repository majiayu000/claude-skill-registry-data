---
name: sf-governor-limits
description: Apex per-transaction governor limits and how to stay inside them - the full synchronous and asynchronous limit table for API 67.0 (100/200 SOQL, 150 DML, 50k query rows, 6/12 MB heap, 10s/60s CPU), the Limits and OrgLimits classes, bulkification of DML and SOQL, heap control with SOQL for loops and Database.QueryLocator, CPU-time reduction, Test.startTest/stopTest limit isolation, certified managed package and cross-namespace limits, platform limits for async executions and concurrent long-running transactions, and a symptom-to-fix remediation playbook. Use when writing triggers, batch or queueable Apex, bulk data processing, or when a run fails with a LimitException, a CPU time error, or a heap error, and when running vf-check apex or vf-check analyzer.
---

# Apex Governor Limits

## When to use

- Writing or reviewing any trigger, trigger handler, batch, queueable, future or scheduled class.
- A run failed with `System.LimitException`, `Apex CPU time limit exceeded`, or `Apex heap size too large`.
- Sizing a bulk job: deciding batch scope, chunking a load, or choosing sync versus async.
- Wave 1 and wave 2 of the vibe-force workflow: `sf-apex-engineer` sizes the work against these
  numbers, `sf-quality-gate` reads the Code Analyzer findings that map to them.

All numbers below come from the Apex Developer Guide for Summer '26 / API version 67.0, the
version pinned in `config/vibe-force.defaults.json`. Limits are per transaction unless the table
says otherwise.

## The numbers you must know by heart

| Limit | Synchronous | Asynchronous |
| --- | --- | --- |
| SOQL queries issued | 100 | 200 |
| Records retrieved by SOQL | 50,000 | 50,000 |
| Records retrieved by `Database.getQueryLocator` | 10,000 | 10,000 |
| SOSL queries issued | 20 | 20 |
| Records per SOSL query | 2,000 | 2,000 |
| DML statements issued | 150 | 150 |
| Records processed by DML, `Approval.process`, `Database.emptyRecycleBin` | 10,000 | 10,000 |
| Stack depth for recursive trigger-firing DML | 16 | 16 |
| Callouts per transaction | 100 | 100 |
| Cumulative callout timeout | 120 s | 120 s |
| `@future` methods per invocation | 50 | 0 in batch and future, 50 in queueable |
| Jobs added with `System.enqueueJob` | 50 | 1 |
| `sendEmail` calls | 10 | 10 |
| Heap size | 6 MB | 12 MB |
| CPU time on Salesforce servers | 10,000 ms | 60,000 ms |
| Transaction execution time | 10 min | 10 min |
| `EventBus.publish` for publish-immediately events | 150 | 150 |

Scheduled Apex is asynchronous but **synchronous limits apply to it**. For Bulk API and Bulk
API 2.0 transactions the effective limit is the higher of the two columns.

The full tables - certified managed package and cross-namespace limits, platform limits, static
limits, size-specific limits, miscellaneous limits, email limits - are in
[references/limit-tables.md](references/limit-tables.md).

## What counts, and what does not

| Operation | Counts against |
| --- | --- |
| `Database.query`, `Database.queryWithBinds`, `Database.countQuery`, `Database.countQueryWithBinds`, `Database.getQueryLocator`, `Database.getQueryLocatorWithBinds` | SOQL query count |
| A parent-child subquery inside a SOQL query | one extra query; subqueries get 3x the top-level number, reported by `Limits.getLimitAggregateQueries()` |
| SOQL against a custom metadata type | nothing - custom metadata records have unlimited SOQL per transaction |
| `insert`, `update`, `upsert`, `delete`, `undelete`, `merge` and their `Database.*` forms, `Approval.process`, `Database.convertLead`, `Database.emptyRecycleBin`, `Database.rollback`, `Database.setSavePoint`, `System.runAs`, `EventBus.publish` for publish-after-commit events | DML statement count |
| Time in the database for DML, SOQL and SOSL | **not** CPU time |
| Waiting for a callout | **not** CPU time |
| Application-server CPU spent inside DML | CPU time |
| HTTP request and response bodies | heap size |

That "not CPU time" row is the one people get wrong. A slow query does not burn CPU time; a loop
over its results does.

## Core patterns

### 1. One DML per collection, never one per record

```apex
public with sharing class LineItemUpdater {
    public static void markHighVolume(List<Line_Item__c> items) {
        List<Line_Item__c> toUpdate = new List<Line_Item__c>();
        for (Line_Item__c li : items) {
            if (li.Units_Sold__c > 10) {
                li.Description__c = 'New description';
                toUpdate.add(li);
            }
        }
        if (!toUpdate.isEmpty()) {
            update as user toUpdate;
        }
    }
}
```

The `if (!toUpdate.isEmpty())` guard is not decoration. An empty-list DML still consumes one of
the 150 statements.

### 2. Query once, key by Id, look up in the loop

```apex
public with sharing class InvoiceRollup {
    public static void apply(List<Invoice_Statement__c> invoices) {
        Map<Id, Invoice_Statement__c> byId = new Map<Id, Invoice_Statement__c>(invoices);

        Map<Id, Decimal> totals = new Map<Id, Decimal>();
        for (AggregateResult ar : [
            SELECT Invoice_Statement__c inv, SUM(Value__c) total
            FROM Line_Item__c
            WHERE Invoice_Statement__c IN :byId.keySet()
            WITH USER_MODE
            GROUP BY Invoice_Statement__c
        ]) {
            totals.put((Id) ar.get('inv'), (Decimal) ar.get('total'));
        }

        for (Invoice_Statement__c inv : invoices) {
            inv.Total__c = totals.containsKey(inv.Id) ? totals.get(inv.Id) : 0;
        }
    }
}
```

One query, one map, no query inside the loop. `GROUP BY` moves the arithmetic into the database,
where it costs no CPU time and no heap.

### 3. SOQL for loop when the result set is large

```apex
public with sharing class ContactSweeper {
    public static void touchAll(Id accountId) {
        List<Contact> batch = new List<Contact>();
        for (List<Contact> chunk : [
            SELECT Id, Description
            FROM Contact
            WHERE AccountId = :accountId
            WITH USER_MODE
        ]) {
            for (Contact c : chunk) {
                c.Description = 'swept';
                batch.add(c);
            }
            update as user batch;
            batch.clear();
        }
    }
}
```

The list form of the SOQL for loop hands you 200 records at a time and lets the previous chunk be
garbage collected. That is the difference between 6 MB of heap and a `LimitException`. The
single-sObject form (`for (Contact c : [SELECT ...])`) also chunks internally at 200.

### 4. Batch Apex when 50,000 rows is not enough

```apex
public with sharing class ExpireQuotesBatch implements Database.Batchable<SObject> {
    public Database.QueryLocator start(Database.BatchableContext ctx) {
        return Database.getQueryLocator([
            SELECT Id, Status__c FROM Quote__c WHERE Expires_On__c < TODAY AND Status__c != 'Expired'
        ]);
    }

    public void execute(Database.BatchableContext ctx, List<Quote__c> scope) {
        for (Quote__c q : scope) {
            q.Status__c = 'Expired';
        }
        update as system scope;
    }

    public void finish(Database.BatchableContext ctx) {}
}
```

`Database.QueryLocator` in `start` returns up to 50 million records, and **the per-transaction
limits reset for every `execute` call**. That reset is the whole point of Batch Apex. Note that
`Database.getQueryLocator` called as an ordinary method inside a transaction is capped at 10,000
records instead - the 50 million figure applies to the `start` method of a batch job.

Pick the scope size deliberately: `Database.executeBatch(new ExpireQuotesBatch(), 100)` when each
record is expensive, the default 200 otherwise. Smaller scope means more executions, and
executions count against the daily async limit.

### 5. Measure, do not guess

```apex
System.debug(LoggingLevel.INFO, 'SOQL ' + Limits.getQueries() + '/' + Limits.getLimitQueries());
System.debug(LoggingLevel.INFO, 'DML ' + Limits.getDmlStatements() + '/' + Limits.getLimitDmlStatements());
System.debug(LoggingLevel.INFO, 'Rows ' + Limits.getQueryRows() + '/' + Limits.getLimitQueryRows());
System.debug(LoggingLevel.INFO, 'Heap ' + Limits.getHeapSize() + '/' + Limits.getLimitHeapSize());
System.debug(LoggingLevel.INFO, 'CPU ' + Limits.getCpuTime() + '/' + Limits.getLimitCpuTime());
```

Every consumption method `getX()` has a ceiling twin `getLimitX()`. The full list is in
[references/limits-class-api.md](references/limits-class-api.md).

### 6. Assert the budget in a test

```apex
@IsTest
private class InvoiceRollupTest {
    @IsTest
    static void rollupIsBulkSafe() {
        List<Invoice_Statement__c> invoices = TestDataFactory.invoices(200);
        insert invoices;

        Test.startTest();
        Integer queriesBefore = Limits.getQueries();
        InvoiceRollup.apply(invoices);
        Integer used = Limits.getQueries() - queriesBefore;
        Test.stopTest();

        Assert.isTrue(used <= 2, 'Rollup must stay at 2 queries for any volume, used ' + used);
    }
}
```

`Test.startTest()` resets the governor limits once per test method and gives the code under test a
fresh budget; `Test.stopTest()` restores the test context and forces queued async work to run.
Limits apply individually to each test method. A test that asserts a *constant* query count for a
200-record input is the only reliable proof that code is bulk safe - coverage percentage proves
nothing about limits.

### 7. Check org-level capacity before starting a big job

```apex
Map<String, System.OrgLimit> limits = OrgLimits.getMap();
System.OrgLimit async = limits.get('DailyAsyncApexExecutions');
System.debug(async.getValue() + ' of ' + async.getLimit() + ' async executions used today');
```

Batch Apex pre-checks the required async capacity when `Database.executeBatch` is called. If the
job needs more executions than remain in the rolling 24-hour window, it throws before it starts
and the remaining allowance is left unchanged.

## Anti-patterns

### DML inside a loop

```apex
// wrong - 151st record throws
for (Line_Item__c li : liList) {
    li.Description__c = 'New description';
    update li;
}
```

Fix: collect into a list, one `update` after the loop (pattern 1).

### SOQL inside a loop

```apex
// wrong - one query per iteration
for (Invoice_Statement__c inv : Trigger.new) {
    List<Line_Item__c> items = [SELECT Id FROM Line_Item__c WHERE Invoice_Statement__c = :inv.Id];
}
```

Fix: one query with `IN :ids`, results keyed into a `Map` (pattern 2). Code Analyzer reports this
as `DbInLoop` (Flow) and as the SOQL-in-loop Apex rules; `vf-check analyzer` fails on it.

### Holding every record in one list

```apex
// wrong - 50,000 fat records will not fit in 6 MB
List<Contact> all = [SELECT Id, Description, Big_Text__c FROM Contact];
for (Contact c : all) { ... }
```

Fix: a SOQL for loop (pattern 3), fewer fields in the `SELECT`, or Batch Apex (pattern 4).
Querying only the fields you use is the cheapest heap fix there is.

### Nested loops over two collections

```apex
// wrong - 200 x 200 = 40,000 iterations of body, CPU time dies
for (Account a : accounts) {
    for (Contact c : contacts) {
        if (c.AccountId == a.Id) { ... }
    }
}
```

Fix: build a `Map<Id, List<Contact>>` once, then a single loop. CPU time is the limit that
bulkification alone does not fix - algorithmic shape does.

### Calling `Limits.getHeapSize()` inside a loop

Code Analyzer flags this as its own rule. The call itself is cheap but doing it per iteration is
noise; sample it once before and once after the loop.

### Recursive trigger without a guard

Stack depth for recursive trigger-firing DML is 16, and a trigger that updates its own object can
re-enter. Use a static `Set<Id>` of processed ids, or the bypass mechanism in skill
`sf-fflib-operations`.

### Assuming a certified managed package shares your budget

Certified managed packages get their own copy of most per-transaction limits. Non-certified
packages do **not** - their usage counts against your org's limits. When a limit blows up in a
transaction that touches managed code, find out which kind of package it is before you refactor
your own code.

## Verification

```bash
# Static detection of loop-bound SOQL/DML before anything runs
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" analyzer --changed

# Run the Apex tests, including the bulk-safety assertions
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex --target-org <alias>

# Limit consumption of a single operation, from the log
sf apex run --file scripts/apex/probe.apex --target-org <alias>
sf apex get log --number 1 --target-org <alias> | grep -E "LIMIT_USAGE_FOR_NS|CUMULATIVE_LIMIT_USAGE" -A 20

# Current org-level capacity
sf org list limits --target-org <alias>
```

The `LIMIT_USAGE_FOR_NS` block at the end of a debug log is the authoritative per-namespace
consumption report for a transaction. Set the `APEX_CODE` category to `FINEST` and the `SYSTEM`
category to at least `FINE` to get it - see skill `sf-debugging-logs`.

## References

- [references/limit-tables.md](references/limit-tables.md) - every official limit table for API 67.0
- [references/limits-class-api.md](references/limits-class-api.md) - `Limits` and `OrgLimits` methods
- [references/remediation-playbook.md](references/remediation-playbook.md) - symptom to fix, per limit

Sibling skills: `sf-soql-sosl-optimization` (selectivity, indexes, large data volumes),
`sf-async-apex-patterns` (batch, queueable, future, platform events), `sf-apex-development`
(trigger shape and order of execution), `sf-apex-testing` (test mechanics and coverage gates),
`sf-code-analyzer-quality` (the rules that detect these statically), `sf-debugging-logs`
(reading `LIMIT_USAGE_FOR_NS`), `sf-data-management` (loading volume without a transaction at all).

Source: Apex Developer Guide, "Execution Governors and Limits", Summer '26 / API 67.0
(`atlas.en-us.262.0.apexcode.meta`); Apex Reference Guide, `Limits` and `OrgLimits` classes.
