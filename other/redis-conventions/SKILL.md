---
name: redis-conventions
description: "Use when writing or reviewing code or configuration that talks to Redis (or a compatible server): key design, expiry and eviction, atomic updates, client pooling and batching, persistence, access control, cluster key placement. Redis is a cache or a fast structure store, never the only copy of data you cannot rebuild."
---

# redis-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames any code that reads or writes an in-memory key-value
server: a cache in front of a database, a counter, a session store, a rate limiter, a short-lived queue.
The rules hold in a repo with nothing installed (`CONVENTIONS.md`, rule A). The decision that comes first is
in §1: what happens to the application when this data is gone, because that answer sets the eviction,
persistence and failure behaviour of everything else.

**Special status.** New technology for this framework, no in-house production experience behind it yet: the
content comes from the vendor's own published development skills and documentation, read on 2026-10-02.
A solid base to confront with the first real project, not proven doctrine. Behaviour tied to a server
version is marked with the version and must be re-read against the version actually deployed.

## When
A key is named or a command is added, a client is configured, a cache is introduced in front of a
slower source, a script or transaction is written, or a server configuration (memory limit, persistence,
users, network) is created or reviewed.

## Steps

**Read §1 first, every time**, then the rows whose trigger the task meets, not the table.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Role of the data and choice of structure; key names | always, before the first key | [`01-role-structures-keys.md`](./references/01-role-structures-keys.md) |
| 2 | Expiry, eviction, memory limit, persistence | a cache is added, a value is stored with no expiry, a server config is written | [`02-expiry-eviction-persistence.md`](./references/02-expiry-eviction-persistence.md) |
| 3 | Atomic updates: single commands, transactions, scripts, messaging limits | two clients can touch the same key, a script is written, pub/sub is used | [`03-atomicity-scripts-messaging.md`](./references/03-atomicity-scripts-messaging.md) |
| 4 | Clients: pooling, pipelining, scanning, timeouts, client-side caching | a client is configured, a loop makes many calls, a key listing is written | [`04-clients-and-calls.md`](./references/04-clients-and-calls.md) |
| 5 | Security: network, authentication, least-privilege users, TLS | a server is deployed or reviewed, credentials are created | [`05-security.md`](./references/05-security.md) |
| 6 | Cluster and replicas: key placement, multi-key commands, stale reads | the deployment is sharded or reads go to replicas | [`06-cluster-and-replicas.md`](./references/06-cluster-and-replicas.md) |
| 7 | Operating it: what to watch and which commands to reach for | a dashboard, an alert or an incident | [`07-operating.md`](./references/07-operating.md) |

## Output / checkpoint
Every key written has a named owner, a stated role (§1), an expiry or a stated reason for having none (§2),
and no command in the diff walks a whole keyspace or a whole large container (§4). Nothing here writes a
pipeline checkpoint.

## Guardrails
- Never store the only copy of data that cannot be rebuilt in a server configured as a cache (§1.1, §2.4).
- Never open a connection per request (§4.1) and never run a full-keyspace listing in application code (§4.3).
- Never expose the server port beyond the application's network (§5.1).
- A rule that depends on a server version is stated with the version; confirm it against the deployed one.
- This block has no in-house production experience yet.

## Origin
The vendor's published development skills for the server (MIT) and its official documentation, read
2026-10-02, mechanisms rewritten. Full provenance, licence handling and the freshness stamp are in
[`references/origin.md`](./references/origin.md).
