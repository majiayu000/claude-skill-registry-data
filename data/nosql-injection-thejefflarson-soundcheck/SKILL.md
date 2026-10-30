---
name: nosql-injection
description: Detects MongoDB and other NoSQL queries that mix user input into operators or
  filters without validation. Use when writing MongoDB queries, Elasticsearch
  queries, or other NoSQL database operations that include user-supplied
  input. Also invoke when building query filters from request parameters or
  constructing aggregation pipelines with dynamic values.
---

# NoSQL Injection Security Check (CWE-943)

## What this checks

Protects against NoSQL injection where user input manipulates query operators or
structure. Unlike SQL injection, NoSQL injection exploits operator injection
(`$gt`, `$ne`, `$regex`) and JavaScript execution in database engines. Exploitation
leads to authentication bypass, data exfiltration, and denial of service.

## Vulnerable patterns

- Query filter built by passing a deserialized request body or query object straight into the database client, letting the caller smuggle operators in place of values
- Use of `$where`, `$expr`, or `$function` with a string that incorporates user input
- Filter value that is allowed to be an object or array when the schema expects a primitive, enabling operator injection like a not-equal match against a credential field
- Aggregation pipeline stage built from raw caller-supplied data with no field allowlist

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties:

1. **Every value destined for a query filter is type-checked as a primitive.**
   Reject anything that is not a string, number, or boolean before it reaches the
   query builder. The classic not-equal-empty-string auth bypass works because
   the deserialized payload was allowed to be an object; enforcing a primitive
   type turns operator keys into literal values that cannot match.
2. **Server-side evaluation operators never receive user-supplied values.**
   Operators like `$where`, `$expr`, and `$function` accept JavaScript or
   expression strings that the database engine evaluates; with user input in
   them, the database becomes an interpreter running attacker code.
3. **Raw request bodies and query objects are not passed directly as filters.**
   Build the query object explicitly from validated, named fields — the same
   allowlist discipline that defeats mass assignment (see the `mass-assignment`
   skill for ORM-side details).

Translate these principles to the NoSQL client library and validator of the audited
file. Use the driver's documented parameterization or query-builder API — do not
build filters from untyped caller-supplied objects.

## Verification

- [ ] Every value in a NoSQL query filter derived from user input is explicitly type-checked as a primitive (string, number) — not an object or array that could contain query operators
- [ ] `$where`, `$expr`, and `$function` are never used with user-supplied values
- [ ] Raw request bodies or query parameters are never passed directly as database query filters

## References

- CWE-943 ([Improper Neutralization of Special Elements in Data Query Logic](https://cwe.mitre.org/data/definitions/943.html))
