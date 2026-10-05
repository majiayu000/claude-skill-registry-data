---
name: padosoft-tenant-isolation
description: >-
  Use this skill when more than one organisation, customer, workspace or project shares a system, and
  whenever a boundary between them is being written or reviewed: a scoped query, a list endpoint, an update
  or delete, a background job, a cache or storage key, an idempotency key, a provisioning or admin route. It
  also applies when the user reports that one account can see or overwrite another's data, that a count or a
  page leaks records, that a job ran for the wrong tenant, or that a legacy record is visible to everyone.
  It checks that the scope is carried by the key and re-checked at every boundary, not applied as a filter
  on the way out. Do not use it for authentication or login flows, for role and permission design inside a
  single tenant, or for database sharding and capacity work.
license: MIT
compatibility: >-
  Stack-agnostic. Examples assume a relational store and an HTTP API; the reasoning applies to queues,
  object storage, caches and search indexes equally.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: The scope belongs to the key, not to the filter.
  profiles: core
  scope: global
  repository: https://github.com/padosoft/skills
  keywords: multi-tenant, isolation, authorization, scope, idempotency, pagination, leak, saas
---

# Tenant isolation

Filtering by tenant is what you do on the way **out**. Isolation is what the key carries on the way **in**.
Every leak below happened in a system that filtered correctly.

**The rule: the scope is part of the identity of the record, not a predicate applied to it.**

---

## 1. A filter protects reads. It does not protect writes

```text
❌  WHERE org = :org        → then  UPDATE ... WHERE id = :id
✅  the key IS (org, id)    → an update names the tenant, or it names nothing
```

Two records with the same name in different tenants are two records. If the storage key does not carry the
authenticated scope, a `PUT` or a `DELETE` on a familiar name overwrites the other tenant's copy — and the
list endpoint that "proved" isolation was never involved.

This holds for every store, not just the database: an object-storage prefix, a cache key, a search document
id, a file path. **Derive the prefix from the authenticated scope**, never from something the caller sent.

## 2. Filter first, then paginate

```text
❌  LIMIT 20 ... then filter by tenant      → the page is short, or empty, and the count is wrong
✅  tenant + predicate → count → slice
```

Computing a total before the scope is applied leaks **counts and identities** through page boundaries: the
caller learns how many records exist that they cannot see. The same ordering bug appears without tenancy —
applying a limit before a selective predicate is a correctness defect, not a performance one, because a
newer row of another kind can consume the page and hide what you were looking for.

## 3. One identifier is not a tenant key

A project slug, a customer-visible code, a directory user id: **two organisations can legitimately reuse the
same one**. Persist the owning organisation alongside it and check *both* dimensions on every scoped read.

Users are data too. A shared external id from an identity provider does not identify the tenant, and a
provisioning protocol must reject cross-tenant ids rather than resolving them.

## 4. Legacy compatibility must not outrank isolation

A transparent fallback — "if there is no namespaced record, read the global one" — is convenient during a
migration and unsafe at an API boundary: a missing namespace then looks like a valid record and crosses the
boundary silently.

- Scoped stores return **only** scoped records, and fail closed otherwise.
- Legacy data moves through an explicit, **privileged** migration path that derives its destination from the
  authenticated scope, preflights every target key and refuses a partial move.
- The migration boundary gets a narrow resource allowlist, so operational configuration cannot accidentally
  become an identity import.

## 5. Everything asynchronous crosses the boundary again

The request was authorised. The job that runs three seconds later was not.

| Boundary | What it needs |
|---|---|
| Enqueue | scope derived from the authenticated request, never from the payload |
| Dequeue | the worker's own identity, **and** the tenants it may process |
| Acknowledge / fail | the same check again — route authentication cannot prevent cross-tenant completion |
| Cancellation | scoped mutation, lease cleared, late acknowledgements rejected |

**Never let a payload choose a filesystem root, a pack path or an execution option.** Decode only narrow
selectors from the job body; roots, credentials and execution controls belong to deployment configuration.
Otherwise a legitimate run request becomes arbitrary local file access.

## 6. Idempotency keys need an owner

An idempotency key on its own is a replay waiting to happen: the same client token, sent in a different
project or with a different body, returns the wrong result to the wrong caller.

Qualify the key by the authorised scope, persist a **canonical fingerprint of the payload**, and compare it
after the unique-key conflict — see **`padosoft-atomic-invariants`** for why the comparison belongs inside
the same atomic step.

## 7. Quotas and limits are shared state

A per-tenant quota read as a snapshot and then written can oversubscribe under concurrent replicas. Keep the
backpressure response and its bounded error shape, but serialise the read and the insert in one transaction,
or use a durable counter. Key the limit on the tenant or the credential — **never on a client-supplied
address header**.

## 8. Wildcards are declared, never inferred

A configuration parser must not read a missing segment as "all tenants". Require the full pair, or a visibly
intentional wildcard, and fail before the process connects to anything. The same applies to a permissive
cross-origin default on a control plane: absence of a restriction is not a decision anybody made.

---

## Gotchas

- **The list endpoint is the one that gets tested**, and it is the only one that was never the problem.
- **A mock or read-only mode hides every scoping bug**, because nothing is ever attributed. Exercise the
  live path, with the tenant and the principal both bound, before believing the screen.
- **An adapter cannot infer tenancy from a key.** Object-lock, retention and encryption are capabilities of
  a storage provider, not an authorisation model; the API derives the scope, the adapter is told.
- **"Bounded parallelism" is not isolation.** Limiting the number of workers does not stop two of them
  mutating the same record. Declare a serialisation policy and record which one was in effect.
- **Two tenants with the same external user id** is the test nobody writes. Write it.

## Checklist

- [ ] The storage key carries the authenticated scope — database, object store, cache, index, filesystem
- [ ] Writes and deletes are scoped by key, not by a preceding filter
- [ ] Pagination and totals computed **after** the scope and the predicate
- [ ] No single identifier used as a tenant key; the owning organisation is persisted and checked
- [ ] No transparent fallback to unscoped records; migration is explicit and privileged
- [ ] Jobs: scope at enqueue, identity **and** scope at dequeue, re-checked at acknowledge
- [ ] Payloads cannot choose roots, paths or execution options
- [ ] Idempotency keys qualified by scope, with a canonical payload fingerprint
- [ ] Quotas serialised or durable; limits keyed on tenant or credential
- [ ] Wildcards explicit; no permissive default inferred from a missing value
- [ ] A test with two tenants sharing a name **and** an external id

## Final report

```
Boundary reviewed: <endpoint / job / store>
Scope source: <authenticated claim> → carried by: <key shape>
Reads: scoped | filtered (why)      Writes: scoped by key | at risk
Pagination after scope: yes | no
Async path: enqueue <…> · dequeue <…> · ack <…>
Idempotency: key + scope + payload fingerprint | partial | absent
Legacy fallback: none | <where, and the migration plan>
Leaks found: none | <what crosses, and how>
```
