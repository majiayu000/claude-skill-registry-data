---
name: sf-soql-sosl-optimization
description: Diagnoses and rewrites slow or non-selective SOQL and SOSL on Salesforce, covering the Lightning Platform query optimizer, standard and custom index selectivity thresholds, skinny tables, two-column indexes, external IDs, the Query Plan and REST explain tools, SOQL_EXECUTE log analysis, relationship query depth limits, aggregate queries with GROUP BY ROLLUP and CUBE, FOR UPDATE row locks, LIMIT and OFFSET caps, SOQL for loops, query locators and Apex cursors, injection-safe dynamic SOQL with Database.queryWithBinds, SOSL search semantics, and large-data-volume strategies such as PK chunking and Bulk API 2.0 query. Use this skill when a query times out or throws QUERY_TIMEOUT, OPERATION_TOO_LARGE, NUMBER_OUTSIDE_VALID_RANGE, QUERY_TOO_COMPLICATED, or "Aggregate query has too many rows for direct assignment", when a trigger or batch start method must be made selective, when planning an index or skinny table, or when choosing between SOQL, SOSL, and Bulk API for a large read.
---

# SOQL and SOSL Optimization

## When to use

Use this skill whenever a read is the problem: a query that times out, a batch `start` method that
fails to launch, a list view or report that hangs, an unindexed `WHERE` clause on a multi-million-row
object, or a decision between SOQL, SOSL, and the Bulk API. It also owns safe dynamic SOQL
construction.

Related skills: `sf-governor-limits` (full per-transaction limit tables),
`sf-async-apex-patterns` (query locators, cursors, batch chunking),
`sf-security-model` (`WITH USER_MODE`, `AccessLevel`, `stripInaccessible`, sharing),
`sf-data-management` (Bulk API 2.0 loads and extracts, data seeding),
`sf-debugging-logs` (capturing and reading `SOQL_EXECUTE_*` log lines),
`sf-apex-development` (where queries belong in a trigger handler).

## Selectivity quick reference

The Lightning Platform query optimizer picks the driving index and join order. It consults an internal
statistics table with a pre-query before deciding whether an index helps.

| Index kind | Used when the filter matches | Worked example |
| --- | --- | --- |
| Standard indexed field | < 30% of the first million records **and** < 15% of each additional million | 2M-row table: 450,000 rows or fewer. 5M-row table: 900,000 rows or fewer |
| Custom indexed field | < 10% of the first million records **and** < 5% of each additional million | 500K-row table: 50,000 rows or fewer. 5M-row table: 300,000 rows or fewer |
| `AND` of several filters | indexes are used unless one of them returns more than 20% of the object's records | also selective if each filter is under twice its own threshold, or the intersection is under the single threshold |
| `OR` of several filters | indexes are used unless **all** of them return more than 10% of the object's records; **every** field in the `OR` must be indexed for any index to be used | each filter must clear the threshold individually |
| `LIKE` | the optimizer samples up to 100,000 actual records instead of using the statistics table | |
| `CONTAINS` | a custom index is typically not used once the scan exceeds 333,333 rows, because `CONTAINS` requires a full index scan | threshold subject to change |

Apex Developer Guide rule of thumb: a query is selective when a filter on an indexed field matches
**less than 10% of total rows**.

Indexed by default on most objects: `Id` (primary key), `Name`, `OwnerId`, `CreatedDate`,
`SystemModstamp` / `LastModifiedDate`, `RecordTypeId`, `Division`, `Email` on Contact and Lead, every
lookup and master-detail foreign key, and every custom field marked External ID or Unique. Salesforce
also auto-indexes fields when the optimizer sees that an index would help frequently run queries.

Cannot be custom-indexed: text area (long), text area (rich), non-deterministic formula fields,
encrypted text, multi-select picklists, currency fields in a multi-currency org, binary fields (blob,
file), and formula fields that call `TEXT()` on a picklist.

## Core patterns

### 1. Measure selectivity before you tune

```bash
# Value distribution for a picklist filter, plus the object total, in one query
sf data query --target-org vf-dev --query "SELECT StageName, COUNT(Id) FROM Opportunity GROUP BY ROLLUP(StageName)"

# Date distribution by week and year
sf data query --target-org vf-dev --query "SELECT WEEK_IN_YEAR(CloseDate), CALENDAR_YEAR(CloseDate), COUNT(Id) FROM Opportunity GROUP BY ROLLUP(WEEK_IN_YEAR(CloseDate), CALENDAR_YEAR(CloseDate)) ORDER BY CALENDAR_YEAR(CloseDate), WEEK_IN_YEAR(CloseDate)"

# Exclude soft-deleted rows from the statistics
sf data query --target-org vf-dev --query "SELECT StageName, COUNT(Id) FROM Opportunity WHERE IsDeleted = false GROUP BY StageName"
```

`GROUP BY ROLLUP` returns the per-value counts **and** the grand total, which is exactly the pair of
numbers a selectivity decision needs. `IsDeleted` exists on every standard and custom object; soft
deleted records sit in the Recycle Bin for 15 days and still cost query time.

### 2. Get the execution plan

```bash
# REST Query Performance Feedback (Beta), API 30.0 and later
sf api request rest "/services/data/v67.0/query/?explain=SELECT+Name+FROM+Merchandise__c+WHERE+CreatedDate+%3D+TODAY+AND+Price__c+%3E+10.0" --target-org vf-dev
```

The response returns `plans[]`, sorted most to least optimal; the first plan is the one that runs.

| Field | Read it as |
| --- | --- |
| `leadingOperationType` | `Index` (uses an index on the query object), `Sharing` (uses a sharing-rule-based index), `Other` (internal optimization), `TableScan` (no index - the thing to fix) |
| `relativeCost` | cost relative to the selective-query threshold. **Greater than 1.0 means non-selective** |
| `cardinality` | estimated rows the query returns |
| `sobjectCardinality` | approximate total rows for the object in this org |
| `fields` | the index fields used when `leadingOperationType` is `Index`, otherwise null |
| `notes[]` | `description`, `fields`, `tableEnumOrId` - explains optimizations that could not be used and why |

The Developer Console Query Editor exposes the same data through its Query Plan panel.

### 3. Read the debug log

| Log event | Category / level | Payload |
| --- | --- | --- |
| `SOQL_EXECUTE_BEGIN` | DB, INFO and above | line number, number of aggregations, query source |
| `SOQL_EXECUTE_END` | DB, INFO and above | line number, **number of rows**, **duration in milliseconds** |
| `SOQL_EXECUTE_EXPLAIN` | DB, **FINEST** | Query Plan details for the executed query |
| `SOSL_EXECUTE_BEGIN` | DB, INFO and above | line number, query source |
| `SOSL_EXECUTE_END` | DB, INFO and above | line number, number of rows, duration in milliseconds |

`SOQL_EXECUTE_EXPLAIN` needs the DB category at `FINEST`, so a default trace flag will not show it.
See skill `sf-debugging-logs` for trace-flag setup.

In-transaction counters:

```apex
System.debug('Queries: ' + Limits.getQueries() + '/' + Limits.getLimitQueries());
System.debug('Rows: ' + Limits.getQueryRows() + '/' + Limits.getLimitQueryRows());
```

### 4. Keep the row set out of the heap

```apex
// WRONG - heap blowout on a large object
Account[] accts = [SELECT Id FROM Account];

// RIGHT when no DML is involved
for (Account a : [SELECT Id, Name FROM Account WHERE Name LIKE 'Acme%' WITH USER_MODE]) {
    // per-record work
}

// RIGHT when DML is involved: the list form batches 200 records per iteration
for (List<Account> chunk : [SELECT Id, Name FROM Account WHERE Name LIKE 'Acme%' WITH USER_MODE]) {
    for (Account a : chunk) {
        a.Name = a.Name.toUpperCase();
    }
    update as user chunk;
}
```

The SOQL for loop uses internal `query`/`queryMore` chunking, which avoids the 10 MB (synchronous) or
25 MB (asynchronous) heap limit at the cost of extra CPU. For genuine mass updates prefer Batch Apex
or Apex cursors; see skill `sf-async-apex-patterns`.

### 5. Injection-safe dynamic SOQL

```apex
public with sharing class ContactSearch {
    public static List<Contact> byLastName(String lastName, Integer pageSize) {
        Map<String, Object> binds = new Map<String, Object>{
            'lastName' => lastName,
            'pageSize' => pageSize
        };
        return (List<Contact>) Database.queryWithBinds(
            'SELECT Id, FirstName, LastName FROM Contact ' +
            'WHERE LastName = :lastName ORDER BY LastName LIMIT :pageSize',
            binds,
            AccessLevel.USER_MODE
        );
    }
}
```

`Database.queryWithBinds` (API 57.0 and later) resolves bind variables from a `Map` instead of from
Apex scope. Map-key rules: keys are compared **case-insensitively** and duplicate case-insensitive
keys throw `System.QueryException: The bindMap consists of duplicate case-insensitive keys: [...]`;
keys must start with an ASCII letter, must not start with a number, must not be reserved words, and
dot notation is discouraged.

Companion dynamic methods: `Database.query`, `Database.countQuery`, `Database.countQueryWithBinds`,
`Database.getQueryLocator`, `Database.getQueryLocatorWithBinds`, `Database.getCursor`,
`Database.getCursorWithBinds`.

When a value must be concatenated rather than bound - an object or field API name, or a sort
direction - never interpolate raw user input. Bind what you can, and pass the rest through
`String.escapeSingleQuotes()` after validating it against an allowlist derived from
`Schema.getGlobalDescribe()`.

### 6. Enforce security in the query

```apex
// Preferred from API version 67.0 onward
List<Account> accounts = [SELECT Id, Name FROM Account WITH USER_MODE LIMIT 100];
List<Account> systemScope = [SELECT Id, Name FROM Account WITH SYSTEM_MODE LIMIT 100];
List<Account> dynamic =
    Database.query('SELECT Id, Name FROM Account LIMIT 100', AccessLevel.USER_MODE);
```

From API version 67.0 Apex runs in **user context by default**, classes without an explicit sharing
declaration run as `with sharing`, and `WITH SECURITY_ENFORCED` is **no longer allowed** in Apex SOQL
`SELECT` statements - use `WITH USER_MODE`. `WITH USER_MODE` respects FLS, object permissions, and
sharing rules; it also has fewer limitations than the old `WITH SECURITY_ENFORCED` clause, which
Salesforce explicitly recommends against. `Security.stripInaccessible()` remains the tool for
scrubbing fields from records that were fetched in system mode. Details in skill `sf-security-model`.

### 7. Choose SOQL or SOSL deliberately

| Dimension | SOQL | SOSL |
| --- | --- | --- |
| Executes against | the database | the search indexes |
| API call | `query()` | `search()` |
| Use when | you know the object and field; you need counts, sorting, relationship traversal, or number/date/checkbox filters | you do not know which object or field holds the value; you want an efficient cross-object text hit |
| Text matching | `LIKE` with wildcards, no tokenisation | tokenises words within a field, so `John` matches `Paul and John Company` |
| Speed on `CONTAINS`-style searches | slower | generally faster |
| Per-transaction limit | 100 queries sync / 200 async, 50,000 rows | 20 queries, 2,000 rows per query |

```apex
// SOSL: the RETURNING clause is REQUIRED in Apex
List<List<SObject>> hits = [
    FIND :searchTerm IN NAME FIELDS
    RETURNING Account(Id, Name WHERE BillingCountry = 'USA' ORDER BY Name LIMIT 50),
              Contact(Id, Name)
    LIMIT 100
];
List<Account> accounts = (List<Account>) hits[0];
```

SOSL result stages: the engine matches up to 2,000 records; a single-object query returns up to 250
records unless a `WHERE` or `ORDER BY` clause is present, in which case up to 2,000; a multi-object
query returns up to `min(2000/n, 250)` per object; then user permission filters are applied, so
result sets vary per user and over time. Users with View All Data see the unfiltered set.

## Anti-patterns

**Negative and empty-value operators on large objects.** `!=`, `NOT CONTAINS`, `NOT STARTS WITH`, and
`Name != ''` all defeat the index.

```apex
// WRONG - non-selective on a multi-million-row object
[SELECT Id FROM Account WHERE Name != '' AND CustomField__c = 'ValueA' WITH USER_MODE];
// RIGHT - drop the useless filter, keep the selective indexed one
[SELECT Id FROM Account WHERE CustomField__c = 'ValueA' WITH USER_MODE];
```

**Filtering on null for picklists and foreign keys.** Index tables exclude null rows by default, so
`WHERE Contact__c != null` forces a scan. Design the data model so null is not a meaningful value:
substitute a sentinel such as `'NA'` or `'Default'` and filter on that. Salesforce Support can build
a custom index that includes nulls, but existing indexes must be explicitly enabled and rebuilt.

**Running the query at all when the bind is null.** Guard in Apex instead.

```apex
// WRONG - if acctId is null this scans the whole table
List<Account> found = [SELECT Name FROM Account WHERE Account_Id__c = :acctId WITH USER_MODE];
// RIGHT
if (acctId == null) { return null; }
List<Account> found = [SELECT Name FROM Account WHERE Account_Id__c = :acctId WITH USER_MODE];
```

**Leading wildcards.** `LIKE '%term'` cannot use an index. Anchor the pattern (`LIKE 'term%'`) or move
the search to SOSL.

**Filtering on formula fields.** Formula fields are computed at query time and non-deterministic
formulas can never be indexed. Filter the underlying fields, or use cross-object notation
(`CrossObject1__r.CrossObject2__r.IndexedField__c`), which the optimizer does use as long as the
referenced field is indexed.

**Two indexed fields joined by `OR` on a large object.** Both filters must independently clear the
10% threshold. Decompose into two queries and merge the results in Apex.

**Relationship subquery inside a batch `QueryLocator`.** It forces the slow non-chunking batch
implementation. Query children inside `execute` instead. See skill `sf-async-apex-patterns`.

**Paging by incrementing `OFFSET` by `LIMIT`.** A query with `OFFSET` and `LIMIT` can return fewer
rows than `LIMIT`. Check the returned count and adjust `OFFSET` from it. The maximum `OFFSET` is
**2,000 rows**; above that the query fails with `NUMBER_OUTSIDE_VALID_RANGE`. For deep paging use a
keyset filter on an indexed, monotonically increasing field.

```apex
// WRONG - breaks past 2,000 and can silently skip rows
String q = 'SELECT Id FROM Account ORDER BY Id LIMIT 200 OFFSET ' + (page * 200);
// RIGHT - keyset pagination
List<Account> page = [
    SELECT Id FROM Account WHERE Id > :lastSeenId ORDER BY Id LIMIT 200 WITH USER_MODE
];
```

**Assigning an aggregate query straight to a list.** `AggregateResult` queries do not support
`queryMore`, so more than 2,000 rows in a for loop raises a runtime exception, and accessing 200 or
more child records of a retrieved sObject raises `QueryException: Aggregate query has too many rows
for direct assignment, use FOR loop`. Iterate the child relationship with a nested for loop instead
of calling `.size()` or assigning `acct.Contacts` to a list.

**`ORDER BY` together with `FOR UPDATE`.** Not allowed in any SOQL query that locks rows. Also,
`FOR UPDATE` in a batch `start` query has no effect - requery with `FOR UPDATE` inside `execute`.

## Verification

```bash
# Local static gate: Code Analyzer flags unselective and unbound SOQL patterns
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" analyzer --changed

# Full local gate before deploying a query change
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed

# Org test run: query-row and CPU regressions surface as test failures
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex --target-org vf-dev

# Time the rewritten query against real data volume
sf data query --target-org vf-uat --query "SELECT COUNT(Id) FROM Opportunity WHERE StageName = 'Closed Won' AND CloseDate = THIS_WEEK"

# Confirm the plan is index-driven and relativeCost < 1.0
sf api request rest "/services/data/v67.0/query/?explain=SELECT+Id+FROM+Opportunity+WHERE+StageName%3D%27Closed+Won%27" --target-org vf-uat

# Capture SOQL_EXECUTE_EXPLAIN (needs DB at FINEST)
sf apex run --target-org vf-dev --file scripts/apex/probe-query.apex
sf apex log get --target-org vf-dev --number 1
```

Acceptance for a tuning change: `leadingOperationType` is `Index` (or `Sharing`), `relativeCost` is
below 1.0, `SOQL_EXECUTE_END` duration has dropped, and `Limits.getQueryRows()` in the affected
transaction is materially lower. `vf-check analyzer` fails at `gates.analyzerFailSeverity` from
`.vibeforce/config.json`.

## References

- [references/selectivity-and-indexes.md](references/selectivity-and-indexes.md) - optimizer
  internals, threshold arithmetic, index tables, skinny tables, two-column indexes, divisions.
- [references/soql-syntax-reference.md](references/soql-syntax-reference.md) - clause-by-clause
  table with every documented limit, aggregate functions, `TYPEOF`, `USING SCOPE`, SOSL grammar.
- [references/large-data-volumes.md](references/large-data-volumes.md) - LDV best-practice tables,
  Bulk API 2.0 query, PK chunking, archiving, deletion, search indexing.
- [references/query-tuning-playbook.md](references/query-tuning-playbook.md) - symptom to
  measurement to rewrite, with before and after queries and error-code triage.

Official documentation used for this skill:

- [SOQL and SOSL Reference](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_sosl_intro.htm)
- [SOQL SELECT Syntax](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_select.htm)
- [Understanding Relationship Query Limitations](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_relationships_query_limits.htm)
- [OFFSET](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_select_offset.htm)
- [FOR UPDATE](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_select_for_update.htm)
- [SOSL Limits on Search Results](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_sosl_limits.htm)
- [Working with Very Large SOQL Queries](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/langCon_apex_SOQL_VLSQ.htm)
- [SOQL For Loops](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/langCon_apex_loops_for_SOQL.htm)
- [Dynamic SOQL](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_dynamic_soql.htm)
- [Apex Cursors](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_cursors.htm)
- [Execution Governors and Limits](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_gov_limits.htm)
- [Best Practices for Deployments with Large Data Volumes](https://developer.salesforce.com/docs/atlas.en-us.salesforce_large_data_volumes_bp.meta/salesforce_large_data_volumes_bp/ldv_deployments_introduction.htm)
- [Query Performance Feedback (Beta)](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_query_performance_feedback.htm)
- [Get Feedback on Query Performance](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_query_explain.htm)
