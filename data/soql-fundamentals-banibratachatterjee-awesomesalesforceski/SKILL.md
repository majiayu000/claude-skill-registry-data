---
name: soql-fundamentals
description: "Use this skill when writing or debugging SOQL queries: SELECT syntax, WHERE filters, ORDER BY, LIMIT, OFFSET, relationship queries (child-to-parent and parent-to-child), aggregate functions (COUNT, SUM, AVG, MIN, MAX), and date literals. Trigger keywords: soql, query, SELECT FROM WHERE. NOT for SOQL security enforcement (use soql-security), query optimization and index tuning (use soql-query-optimization), or SOSL full-text search."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Reliability
triggers:
  - "how do I write a SOQL query to get related child records"
  - "how to use aggregate functions like COUNT or SUM in SOQL"
  - "my SOQL query returns no results even though records exist"
  - "how to filter by date range using date literals in SOQL"
  - "how to traverse relationships in SOQL using dot notation"
  - "how to use OFFSET and LIMIT for pagination in SOQL"
tags:
  - soql
  - query
  - apex
  - data-access
  - relationship-queries
inputs:
  - "Object name(s) to query"
  - "Fields to retrieve"
  - "Filter criteria (optional)"
  - "Whether the query is inline Apex or dynamic SOQL"
outputs:
  - "Correct SOQL statement with proper syntax"
  - "Explanation of clauses and behavior"
  - "Guidance on known limits and gotchas"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# SOQL Fundamentals

This skill activates when a practitioner needs to write, debug, or understand Salesforce Object Query Language (SOQL) queries — covering SELECT syntax, filtering, sorting, pagination, relationship traversal, and aggregate functions. It does NOT cover SOQL injection prevention (see soql-security) or query plan optimization (see soql-query-optimization).

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm whether the query runs in Apex (requires `[ ]` bracket syntax) or an external API context (REST, SOAP, CLI).
- Identify whether the query needs to traverse a relationship (child-to-parent via dot notation or parent-to-child via subquery).
- Check the governor limit context: synchronous Apex allows 100 SOQL queries per transaction; each query can return up to 50,000 rows.
- SOQL does not support arbitrary SQL JOINs, wildcards in field lists (`SELECT *`), or calculation expressions — operations that are standard in SQL but unavailable in SOQL.

---

## Core Concepts

### 1. SELECT … FROM … WHERE Syntax

SOQL queries follow this structure (clauses in square brackets are optional):

```
SELECT fieldList [subquery] [...]
FROM objectType [,...]
[USING SCOPE filterScope]
[WHERE conditionExpression]
[WITH [DATA CATEGORY] filteringExpression]
[GROUP BY { fieldGroupByList | ROLLUP(...) | CUBE(...) }
  [HAVING havingConditionExpression]]
[ORDER BY fieldOrderByList {ASC|DESC} [NULLS {FIRST|LAST}]]
[LIMIT numberOfRowsToReturn]
[OFFSET numberOfRowsToSkip]
[FOR VIEW | FOR REFERENCE]
[FOR UPDATE]
```

In Apex, inline SOQL is wrapped in square brackets:
```apex
List<Account> accounts = [SELECT Id, Name FROM Account WHERE Industry = 'Media' LIMIT 100];
```

Dynamic SOQL uses `Database.query()`:
```apex
String query = 'SELECT Id, Name FROM Account WHERE Industry = :ind LIMIT 100';
List<Account> accounts = Database.query(query);
```

Key constraint: SOQL statements cannot exceed 100,000 characters in length. The 100,000-character limit does not apply to dynamic SOQL in Apex.

### 2. WHERE Clause — Filters and Date Literals

The WHERE clause supports these comparison operators: `=`, `!=`, `<`, `<=`, `>`, `>=`, `LIKE`, `IN`, `NOT IN`, `INCLUDES`, `EXCLUDES`.

**String filtering with LIKE:** `%` matches zero or more characters; `_` matches exactly one character. Comparisons on standard fields are case-insensitive.

**Date literals** allow relative date filtering without hardcoded dates:

| Date Literal | Meaning |
|---|---|
| `TODAY` | Current day (midnight to midnight) |
| `YESTERDAY` | Previous day |
| `THIS_WEEK` | Current week (locale-dependent start day) |
| `LAST_MONTH` | Calendar month before current month |
| `LAST_N_DAYS:n` | Past n days including today |
| `NEXT_N_DAYS:n` | Next n days, not including today |
| `THIS_FISCAL_QUARTER` | Current fiscal quarter |
| `LAST_FISCAL_YEAR` | Previous fiscal year |

Example — open opportunities closing this quarter:
```sql
SELECT Id, Name, CloseDate FROM Opportunity
WHERE CloseDate = THIS_FISCAL_QUARTER AND IsClosed = false
```

**IN operator** for multi-value filters:
```sql
SELECT Name FROM Account WHERE BillingState IN ('California', 'New York')
```

Strings in WHERE clauses cannot exceed 4,000 characters (this limit does not apply to Apex `IN` clauses).

### 3. Relationship Queries

SOQL supports two types of relationship traversal:

**Child-to-parent (dot notation):** Traverse up to five levels. Use the relationship name with dot notation:
```sql
SELECT Id, Name, Account.Name, Account.BillingCity FROM Contact WHERE Account.Industry = 'Media'
```
For custom relationship fields, append `__r` instead of `__c`:
```sql
SELECT Id, Mother_of_Child__r.FirstName__c FROM Daughter__c
```

**Parent-to-child (subquery):** Query related child records in a nested SELECT. Use the child relationship name (plural for standard, `__r` for custom):
```sql
SELECT Name, (SELECT LastName, Email FROM Contacts) FROM Account WHERE Industry = 'Media'
```
Custom child relationship:
```sql
SELECT Name, (SELECT Name FROM Line_Items__r) FROM Merchandise__c WHERE Name LIKE 'Acme%'
```

Relationship query limits (from SOQL and SOSL Reference):
- Maximum relationship levels in a query: 5 (child-to-parent traversal)
- Maximum parent-to-child subqueries per query: 20
- A subquery cannot itself contain a subquery

### 4. Aggregate Functions and GROUP BY

SOQL aggregate functions: `COUNT()`, `COUNT(fieldName)`, `COUNT_DISTINCT()`, `AVG()`, `MIN()`, `MAX()`, `SUM()`.

All aggregate functions ignore null values, except `COUNT()` and `COUNT(Id)`.

```sql
-- Count records matching criteria
SELECT COUNT() FROM Account WHERE Industry = 'Media'

-- Aggregate by group
SELECT LeadSource, COUNT(Name) FROM Lead GROUP BY LeadSource

-- Filter groups with HAVING (like a WHERE for aggregates)
SELECT LeadSource, COUNT(Name) FROM Lead
GROUP BY LeadSource HAVING COUNT(Name) > 100

-- Find duplicates
SELECT Name, COUNT(Id) FROM Account GROUP BY Name HAVING COUNT(Id) > 1
```

Key rule: you cannot use `LIMIT` in a query that uses an aggregate function without also using `GROUP BY`. `MAX(CreatedDate) FROM Account LIMIT 1` is **invalid**. Adding `GROUP BY SomeField LIMIT 5` is valid.

### 5. ORDER BY, LIMIT, and OFFSET

**ORDER BY** — Results are not guaranteed to be in any consistent order unless you include ORDER BY. For stable pagination, always include a tiebreaker (e.g., `Id`):
```sql
SELECT Name, Industry FROM Account ORDER BY Industry ASC, Id NULLS LAST
```
`NULLS FIRST` (default) and `NULLS LAST` control where null values appear.

**LIMIT** — Returns at most n rows. Maximum 50,000 records per query in most contexts.
```sql
SELECT Name FROM Account WHERE Industry = 'Media' LIMIT 125
```

**OFFSET** — Skips the first n rows for server-side pagination. Maximum offset is 2,000 rows. Always pair with `ORDER BY` for consistent results:
```sql
SELECT Name, Id FROM Merchandise__c ORDER BY Name LIMIT 100 OFFSET 100
```
OFFSET is NOT allowed in Bulk API or Streaming API queries.

---

## Common Patterns

### Pattern 1 — Semi-Join (IN Subquery)

**When to use:** Filter parent records based on a condition on child records, without loading all child data.

```sql
-- Accounts that have at least one closed-lost opportunity
SELECT Id, Name FROM Account
WHERE Id IN (
  SELECT AccountId FROM Opportunity WHERE StageName = 'Closed Lost'
)
```

**Constraint:** The subquery must return a single foreign key or ID field. The selected column cannot use dot notation (no relationship traversal inside a subquery field list).

### Pattern 2 — Anti-Join (NOT IN Subquery)

**When to use:** Find records that do NOT have matching child/related records.

```sql
-- Accounts with no open opportunities
SELECT Id, Name FROM Account
WHERE Id NOT IN (
  SELECT AccountId FROM Opportunity WHERE IsClosed = false
)
```

### Pattern 3 — FIELDS() Keyword for Schema Exploration

**When to use:** Discover all fields on an object without knowing field names. Available since API v51.0.

```sql
SELECT FIELDS(ALL) FROM Account LIMIT 200
SELECT FIELDS(STANDARD) FROM Contact
SELECT FIELDS(CUSTOM) FROM Account LIMIT 200
```

`FIELDS(ALL)` respects FLS — it only returns fields the running user can read. Always pair with `LIMIT` when using `FIELDS(ALL)` or `FIELDS(CUSTOM)` to avoid hitting governor limits.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Need records from one object with fields from parent | Child-to-parent dot notation in SELECT | Flat result set, up to 5 levels |
| Need parent record plus all related child records | Parent-to-child subquery | Returns nested result set |
| Need to count or aggregate for reporting | GROUP BY + aggregate function | Server-side aggregation; no Apex loop needed |
| Need paginated results for UI | LIMIT + OFFSET with ORDER BY tiebreaker | Stable pagination; max offset 2,000 |
| Need records from last N days dynamically | Date literal (LAST_N_DAYS:n) | Avoids hardcoded dates that break across orgs |
| Need records only the current user owns | USING SCOPE mine | Returns only records owned by running user |
| Need cross-object filtering without loading all records | Semi-join (IN subquery) | Efficient server-side filter |

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

Run through these before marking SOQL work complete:

- [ ] Every field in SELECT has at least read-level FLS for the running user (consider WITH USER_MODE in Apex)
- [ ] WHERE clause fields are indexed or selective to avoid full table scans
- [ ] Relationship traversal does not exceed 5 levels (child-to-parent) or 20 subqueries (parent-to-child)
- [ ] LIMIT is present on queries that could return large result sets inside Apex triggers
- [ ] ORDER BY tiebreaker (e.g., Id) added when using OFFSET for pagination
- [ ] Date literals used instead of hardcoded date strings for relative date filtering
- [ ] SOQL injection risk reviewed if any part of the query is dynamically constructed (see soql-security skill)

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Results are unordered without ORDER BY** — The Salesforce query engine does not guarantee a consistent row order unless ORDER BY is specified. Code that relies on "first record returned" without ORDER BY can return different records in different transactions or releases. Always add ORDER BY + Id as a tiebreaker.

2. **OFFSET max is 2,000 rows** — Requesting OFFSET beyond 2,000 raises `NUMBER_OUTSIDE_VALID_RANGE`. For result sets larger than 2,000, use `queryMore()` (SOAP) or `nextRecordsUrl` (REST) instead of incrementing OFFSET. OFFSET is not a replacement for cursor-based pagination on large data sets.

3. **Aggregate functions cannot use LIMIT without GROUP BY** — `SELECT MAX(CreatedDate) FROM Account LIMIT 1` is invalid. The pattern that looks like "get the most recent record" does not work this way in SOQL — use `ORDER BY CreatedDate DESC LIMIT 1` on a full query instead.

4. **FIELDS(ALL) without LIMIT causes row-count failures** — `SELECT FIELDS(ALL) FROM Account` returns all fields for every record. Without LIMIT, this easily blows the 50,000-row limit or produces a QUERY_TOO_LARGE error. Always pair FIELDS() with LIMIT.

5. **Custom relationship names use __r not __c** — Traversing a custom lookup field `Parent__c` in a query uses `Parent__r.FieldName__c`, not `Parent__c.FieldName__c`. Using `__c` in dot notation causes a MALFORMED_QUERY error that is easy to misread.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Validated SOQL statement | A syntactically correct SOQL query ready to use in Apex, REST API, or Developer Console |
| Relationship path diagram | Textual description of how objects connect for relationship query traversal |
| Aggregate query template | GROUP BY + HAVING pattern for the specific reporting need |

---

## Related Skills

- soql-security — Use alongside this skill to add WITH USER_MODE or WITH SECURITY_ENFORCED to enforce FLS and CRUD in Apex queries
- soql-query-optimization — Use when the query is correct but slow or hitting CPU limits due to non-selective filters or missing indexes
- apex-cpu-and-heap-optimization — Use when SOQL governor limits (100 queries, 50,000 rows) are being hit in a transaction
