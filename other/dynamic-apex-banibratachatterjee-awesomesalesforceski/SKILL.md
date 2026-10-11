---
name: dynamic-apex
description: "Use when building or reviewing code that constructs SOQL/SOSL at runtime, inspects schema metadata via Schema.describe methods, accesses fields dynamically on sObjects, or performs runtime type inspection. Triggers: 'Database.query', 'Schema.getGlobalDescribe', 'Schema.describeSObjects', 'dynamic field access', 'SObjectType', 'DescribeFieldResult'. NOT for static SOQL queries or query performance tuning — use soql-fundamentals or soql-query-optimization."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Scalability
triggers:
  - "how do I build a SOQL query with fields chosen at runtime"
  - "how do I check field-level security before accessing a field dynamically"
  - "how do I use Schema.getGlobalDescribe or describeSObjects to inspect metadata"
  - "dynamic field access on sObject record using get and put"
  - "SOQL injection risk in dynamic query string"
tags:
  - dynamic-soql
  - dynamic-sosl
  - schema-describe
  - sobjetype
  - fls
  - runtime-type-inspection
inputs:
  - "target sObject API name (standard or custom)"
  - "list of field API names or Field Set members to access dynamically"
  - "whether the query string includes any user-supplied values"
  - "whether FLS enforcement is required (user-facing vs. system context)"
outputs:
  - "safe dynamic SOQL or SOSL query builder implementation"
  - "FLS-checked field access utility"
  - "Schema describe caching pattern to avoid governor limit pressure"
  - "runtime type inspection example for polymorphic record processing"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-04
---

# Dynamic Apex

Use this skill when Apex code must construct queries or access fields whose names are not known at compile time, or when code must inspect the schema at runtime to validate permissions, enumerate picklist values, or process multiple object types generically. The skill covers safe patterns for dynamic SOQL and SOSL, Schema describe APIs, runtime type inspection, and dynamic field get/put.

---

## Before Starting

Gather this context before working on anything in this domain:

- Is the object API name or field list coming from user input, stored configuration, or code logic? User-supplied values require injection defenses; admin-configured values still need allowlist validation.
- Does the code run in a user-facing context (AuraEnabled, LWC wire, REST endpoint) where FLS must be enforced, or a system context (Batch, Scheduled, admin utility) where that enforcement may be intentionally relaxed?
- Is the schema inspection happening inside a loop? Describe calls count against governor limits and must be cached.

---

## Core Concepts

### Dynamic SOQL: Database.query() vs Static SOQL

Static SOQL (`[SELECT ...]`) is parsed and validated at compile time. Dynamic SOQL uses `Database.query(String queryString)` to execute a query built at runtime. The method accepts a complete SOQL string and returns `List<SObject>`. Because the compiler cannot validate a runtime string, the developer is responsible for correctness, safety, and governor compliance.

Use dynamic SOQL when the object, fields, filters, or ordering must vary based on runtime conditions — for example, a generic export utility, admin-configured field lists via Field Sets, or multi-object handlers. Never use it just to avoid writing out field names.

### SOQL Injection Prevention

SOQL injection is the Apex equivalent of SQL injection: an attacker supplies a string fragment that alters the query's logic. The attack vector is string concatenation of unvalidated user input into the query string.

Three defenses, in order of strength:

1. **Bind variables** — use `:variableName` syntax in the query string. Bind variables are evaluated by the Apex runtime, not string-interpolated, so special characters are inert. This is the preferred defense for user-supplied filter values.
2. **`String.escapeSingleQuotes()`** — escapes single quotes in a string before concatenation. Use when bind variables are not syntactically available (for example, the value belongs in a `LIKE` clause with wildcards that must be concatenated). Apply on every user-supplied string.
3. **Allowlist validation** — for object and field API names, validate against `Schema.getGlobalDescribe()` results before interpolating. Field names come from trusted config or Schema metadata; they are never user-free-text.

Combining all three for their respective input types is the safe approach.

### Schema.describe Methods and the Describe Result Hierarchy

Salesforce exposes schema metadata through several describe APIs:

- `Schema.getGlobalDescribe()` — returns `Map<String, Schema.SObjectType>` for all accessible sObjects in the org. Use to validate that an object name is real and accessible before building a query.
- `Schema.describeSObjects(List<String>)` — more efficient for batch inspection of multiple objects; returns `List<Schema.DescribeSObjectResult>`.
- `Schema.SObjectType.getDescribe()` — returns `Schema.DescribeSObjectResult` for a single type token. Includes `isAccessible()`, `isCreateable()`, `isUpdateable()`, `isDeletable()`.
- `DescribeSObjectResult.fields.getMap()` — returns `Map<String, Schema.SObjectField>` of all fields on the object.
- `Schema.SObjectField.getDescribe()` — returns `Schema.DescribeFieldResult`. Includes `isAccessible()`, `isCreateable()`, `isUpdateable()`, `getType()`, `getPicklistValues()`, `getReferenceTo()`, `getName()`.

Each `getDescribe()` call counts as one describe call and Salesforce enforces a governor limit of 100 describe calls per transaction. Cache results in `static` maps or class-level variables to avoid burning through this limit.

### SObjectType and Runtime Type Inspection

To determine the sObject type of a record at runtime:

```apex
SObjectType recordType = record.getSObjectType();
String apiName = recordType.getDescribe().getName();
```

You can also use `instanceof` to check for specific types in polymorphic lists:

```apex
for (SObject rec : records) {
    if (rec instanceof Contact) {
        // ...
    }
}
```

`getSObjectType()` on a `Schema.SObjectType` token returns the token itself; on an sObject instance it returns the type descriptor for that record.

### Dynamic Field Access: record.get() and record.put()

sObjects support dynamic field read and write without compile-time field references:

```apex
Object fieldValue = record.get('Field_API_Name__c');
record.put('Field_API_Name__c', newValue);
```

`get()` returns `Object` — cast explicitly to the expected type. `put()` accepts any Object but the runtime will throw a `System.SObjectException` if the type is wrong. Always validate the field API name against Schema describe before calling get/put when the name comes from configuration or external data.

### Performance: Caching Describe Calls

Describe calls are not free. In a transaction that processes multiple objects or iterates over records, a naive implementation that calls `getDescribe()` per field per record will exhaust the 100-describe-call limit or introduce excessive CPU time.

Cache pattern:

```apex
private static final Map<String, Schema.SObjectType> GLOBAL_DESCRIBE =
    Schema.getGlobalDescribe();

private static final Map<String, Map<String, Schema.SObjectField>> FIELD_MAP_CACHE =
    new Map<String, Map<String, Schema.SObjectField>>();

private static Map<String, Schema.SObjectField> getFieldMap(String objectName) {
    if (!FIELD_MAP_CACHE.containsKey(objectName)) {
        FIELD_MAP_CACHE.put(
            objectName,
            GLOBAL_DESCRIBE.get(objectName).getDescribe().fields.getMap()
        );
    }
    return FIELD_MAP_CACHE.get(objectName);
}
```

Declare the cache at the class level as `static final` so it is populated once per transaction.

---

## Common Patterns

### Pattern 1: FLS-Enforced Dynamic Update Utility

**When to use:** A generic service needs to update a configurable set of fields on any sObject, and FLS must be respected because the service runs in a user context.

**How it works:**
1. Receive the object API name, a list of field names, and a map of values.
2. Validate the object exists via `Schema.getGlobalDescribe()`.
3. Retrieve `DescribeSObjectResult` and confirm `isUpdateable()`.
4. For each field, retrieve `DescribeFieldResult` and confirm `isUpdateable()`.
5. Build the sObject dynamically, call `put()` for each validated field, then DML.

**Why not the alternative:** Skipping FLS checks here means a caller can update fields the current user has no permission to edit — this is both a security vulnerability and a compliance risk.

### Pattern 2: Runtime-Safe Dynamic Query Builder

**When to use:** An admin-configurable reporting component or export utility must query fields defined in a Field Set or custom metadata record.

**How it works:**
1. Retrieve field names from Field Set (`Schema.FieldSet.getFields()`) or custom metadata — these are trusted sources, not user input.
2. Validate each field name against `DescribeSObjectResult.fields.getMap()` to ensure it still exists on the schema.
3. Build the SELECT clause by joining validated names.
4. Use bind variables for any filter values; use `String.escapeSingleQuotes()` for string literals in LIKE clauses.
5. Execute with `Database.query()`.

**Why not the alternative:** Concatenating unchecked field names from configuration can fail at runtime if a field is deleted, and concatenating user filter values without escaping enables SOQL injection.

### Pattern 3: Multi-Object Polymorphic Processor

**When to use:** A single trigger handler or utility method processes records from different sObject types and routes logic per type.

**How it works:**
1. Accept `List<SObject>` as the method parameter.
2. Call `getSObjectType()` on each record (or on the first record to determine the batch type).
3. Use `instanceof` or a `switch` on the type token to route to type-specific processing.
4. Access fields using `record.get('ApiName')` with types resolved from cached describe metadata.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| User enters a search term used in a SOQL WHERE clause | Bind variable (`:searchTerm`) | Runtime evaluation prevents injection; simplest defense |
| Field API names come from a Field Set | Validate against field map, then concatenate | Field Sets are trusted but fields may be deleted; validate on each run |
| Object name comes from custom metadata | Allowlist via `Schema.getGlobalDescribe()` lookup before use | Detects stale or invalid names before query is executed |
| Inspecting picklist values or field type | `DescribeFieldResult.getType()` / `getPicklistValues()` | Only reliable runtime source; do not hard-code schema knowledge |
| Processing thousands of records of multiple types | Cache describe results in static maps | 100-describe-call limit can be hit quickly without caching |
| Reading a field value whose type is unknown | `record.get()` with explicit cast after `getType()` check | Prevents `SObjectException` at runtime |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. Confirm the source of object and field names — user input, admin-entered config, or code-driven schema introspection — and apply the correct defense for each category.
2. Validate object names against `Schema.getGlobalDescribe()` and field names against the object's field map before including them in any query string or `put()` call.
3. Apply SOQL injection defenses: bind variables for filter values, `String.escapeSingleQuotes()` for LIKE-clause strings, allowlists for field and object names.
4. Enforce FLS via `DescribeFieldResult.isAccessible()` / `isUpdateable()` for every field in user-facing code; document explicitly if a system-context caller intentionally skips this.
5. Cache describe results in static maps at class level — never call `getDescribe()` inside a loop.
6. Test with both accessible and inaccessible fields using `System.runAs()` to verify FLS enforcement paths.
7. Review against the checklist below before merging.

---

## Review Checklist

- [ ] Every object name used in a dynamic query is validated against `Schema.getGlobalDescribe()` before use.
- [ ] Every field name used in a dynamic query or `put()` call is validated against the object's field map.
- [ ] User-supplied filter values use bind variables or `String.escapeSingleQuotes()`.
- [ ] FLS is checked via `DescribeFieldResult.isAccessible()` or `isUpdateable()` for every field in user-facing code paths.
- [ ] Describe calls are cached in static maps and never called inside a loop.
- [ ] `record.get()` return values are explicitly cast and type is verified via `getType()` when the type is not guaranteed.
- [ ] Tests cover permission-denied paths using `System.runAs()` with restricted profiles or permission sets.

---

## Salesforce-Specific Gotchas

1. **`getGlobalDescribe()` is expensive when called repeatedly** — it returns metadata for every accessible sObject in the org. Call it once per transaction and store in a `static final` map. Calling it inside a loop or per-record is a common performance antipattern that can spike CPU time.
2. **`String.escapeSingleQuotes()` is not sufficient alone for object and field names** — it escapes string delimiters but does not prevent injection of valid SOQL keywords (e.g., `LIMIT 1 UNION...`). Field and object names must be allowlisted through Schema describe, not just escaped.
3. **`WITH USER_MODE` in dynamic SOQL does not exist — use `WITH SECURITY_ENFORCED` or explicit FLS checks** — `WITH USER_MODE` is only valid in static SOQL as of Spring '25. Dynamic SOQL queries must enforce FLS via explicit `DescribeFieldResult` checks or `Security.stripInaccessible()` on results.
4. **`record.put()` silently accepts wrong types until DML** — the runtime does not always throw on `put()` with a mismatched type; the error surfaces at the DML statement, making the bug hard to trace. Always validate field type with `DescribeFieldResult.getType()` before calling `put()` with a dynamically built value.
5. **Deleted fields in Field Sets cause runtime exceptions** — if a field referenced in a Field Set is deleted from the object, `Schema.FieldSet.getFields()` can still return the field name but the describe will fail or the query will throw a `QueryException`. Validate all Field Set members against the live field map before building queries.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Safe dynamic query builder | Apex method that accepts an object name and field list, validates schema, applies injection defenses, and returns `List<SObject>` |
| FLS-checked update utility | Generic Apex service that validates object and field permissions before performing dynamic DML |
| Schema describe cache | Static map pattern for caching `getGlobalDescribe()` and per-object field maps across a transaction |

---

## Related Skills

- `apex/soql-security` — use when the primary concern is SOQL injection hardening or query-level field access in static SOQL.
- `apex/apex-security-patterns` — use when the design decision is about sharing keywords, CRUD enforcement, or overall execution context security.
- `apex/soql-fundamentals` — use for static SOQL patterns, query syntax, and relationship queries.
- `data/soql-query-optimization` — use for query performance, selective filters, and avoiding large data volume pitfalls.
