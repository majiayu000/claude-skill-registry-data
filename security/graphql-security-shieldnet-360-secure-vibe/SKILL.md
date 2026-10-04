---
id: graphql-security
version: "2.0.0"
title: "GraphQL Security"
description: "Bound and control a GraphQL endpoint: operation cost budgets, cost-based rate limiting, pre-registered operations, alias and batch abuse on authentication paths, introspection, cache keying, and untyped scalar inputs. Use when generating schemas, resolvers, or server config, wiring limits or persisted operations, or reviewing a public /graphql endpoint."
category: prevention
severity: high
applies_to:
  - "when generating GraphQL schemas, resolvers, or server config"
  - "when configuring depth, complexity, batching, or persisted-operation limits"
  - "when wiring authentication or rate limiting to a GraphQL endpoint"
  - "when reviewing /graphql endpoint exposure"
languages: ["javascript", "typescript", "python", "go", "java", "kotlin", "csharp", "ruby"]
token_budget:
  minimal: 1200
  compact: 1600
  full: 2000
rules_path: "rules/"
related_skills: ["api-security", "auth-security", "error-handling-security", "file-upload-security"]
last_updated: "2026-08-12"
sources:
  - "OWASP GraphQL Cheat Sheet"
  - "GraphQL specification (validation rules)"
  - "CWE-400: Uncontrolled Resource Consumption"
  - "graphql-armor (Escape technologies)"
---

# GraphQL Security

## Rules (for AI agents)

### ALWAYS
- Enforce a **cost budget** on every operation: a maximum depth, plus a complexity
  score that weights list fields by the page size they can request. Derive the numbers
  from your own schema and measure them — a depth of 7 is generous for a flat schema
  and far too permissive for one with a many-to-many edge, where five levels of
  nesting can address billions of nodes. `references/graphql-limits.md` covers how to
  derive them and where each server configures them.
- Rate-limit by **cost consumed**, not by request count. Every operation arrives at
  the same URL, so the per-route limit `api-security` specifies cannot tell a trivial
  query from one costing a thousand times more. Charge the complexity score against
  the caller's budget.
- For a public or high-traffic API, restrict it to **pre-registered operations** — a
  build-time allowlist of the documents the client bundle actually contains, keyed by
  hash. Automatic Persisted Queries are **not** this: APQ lets a client register any
  operation it likes and then send its hash, which is a bandwidth optimization.
  Turning on APQ and believing the API is now allowlisted is a common and expensive
  mistake.
- Cap aliases per operation and operations per batch, and apply that counting to
  **authentication and other rate-limited paths**. One request carrying a hundred
  aliased `login` fields is a hundred attempts against any counter that increments
  once per request — this is the mechanism behind the account-takeover-by-batching
  incidents, not a bandwidth concern.
- Batch resolver fetches with a DataLoader or a join. An N+1 resolver turns one
  cheap-looking query into a database round trip per parent row — the same
  amplification the cost limit exists to bound, except it happens below the cost
  analysis where that limit cannot see it.
- Key any response cache on the operation hash, the variables, **and** the caller's
  authorization claims. `POST /graphql` is one URL for every request, so a cache keyed
  on the URL serves one tenant's data to another.
- Validate the contents of `JSON`, custom scalar, and loosely-typed `input` arguments
  inside the resolver. The schema's type checking is what makes GraphQL inputs feel
  safe, and a `JSON` scalar opts straight out of it: whatever arrives is handed
  through unexamined.
- Disable introspection and the in-browser playground (GraphiQL, Apollo Sandbox) on
  production endpoints — and understand what that buys. It raises the cost of
  reconnaissance and nothing more: field suggestions in error messages still leak
  names, tools reconstruct schemas from them, and every field stays callable whether
  or not it can be listed. Schema obscurity is never the authorization.
- Consult `auth-security` for authorization, and run it **per field** rather than at
  the endpoint. One HTTP response aggregates many resolvers, so a single unguarded
  sensitive field leaks through any query that reaches it.
- Consult `error-handling-security` for what an error may carry. The `errors` array is
  GraphQL's public contract and field-level validation detail belongs in it; what must
  not appear there is the stack trace, the SQL, or resolver internals. Flattening a
  validation failure to a bare `INTERNAL_SERVER_ERROR` is hostile to callers without
  being safer.
- Consult `file-upload-security` for GraphQL multipart uploads. Arriving over GraphQL
  changes nothing about the rules there — quarantine, type validation, expansion
  limits, and scanning policy all still apply.

### NEVER
- Trust a query's shape because "our clients only send well-formed queries". Anyone
  can post to `/graphql`.
- Let `@skip` / `@include` decide whether an authorization check runs. They are
  execution directives evaluated before resolvers, which makes them a **probe
  channel** — an attacker toggles a field and reads the difference in the response —
  not a place to put a security decision.
- Rely on a hand-rolled executor to reject a cyclic fragment. The specification
  requires the `NoFragmentCycles` validation rule and conforming servers enforce it
  during validation; an executor that skips the validation phase does not.

### KNOWN FALSE POSITIVES
- Pre-registered operations are already bounded, so depth and complexity checks on
  them are redundant. Keep the checks for anything arriving outside the allowlist.
- A public, read-only data API may run deliberately high cost limits with aggressive
  CDN caching. That is a documented per-endpoint trade-off, not an oversight.
- Introspection left on for an internal developer tool is acceptable only where the
  endpoint's authorization would be acceptable with introspection both on and off.
  Network placement — a VPN, a private subnet — is not the justification;
  reachability is not authentication.

## Context (for humans)

GraphQL is not more powerful than a REST API in the computational sense. The query
language has no loops, no recursion — the specification's validation rules forbid
fragment cycles — and no arbitrary branching. What it has is **amplification**: one
request can address an enormous amount of work, and one URL carries all of it.

That combination is what defeats controls built for REST. A per-route rate limit sees
one route. A URL-keyed cache sees one key. A request counter sees one request, even
when it carries a hundred aliased login attempts. Each of those controls is doing
exactly what it was designed to do, against a shape it was not designed for — which
is why the GraphQL-specific answer is almost always to move the unit of accounting
from *the request* to *the cost of the operation*.

The second recurring failure is a control that sounds stronger than it is.
Introspection off is reconnaissance cost, not access control. Automatic Persisted
Queries are a bandwidth feature, not an allowlist. A schema type is a parser
guarantee, not validation, once a `JSON` scalar is in play.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/graphql-limits.md` — deriving depth and complexity from your schema,
  where each server configures limits, and APQ versus trusted documents
- `rules/graphql_safe_config.json`
- [OWASP GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html).
- [GraphQL specification — validation](https://spec.graphql.org/).
- [CWE-400](https://cwe.mitre.org/data/definitions/400.html).
- [graphql-armor](https://escape.tech/graphql-armor/).
