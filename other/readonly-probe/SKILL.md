---
description: "STUB — not yet hydrated for this project. Investigate a question against real deployed data under an enforced read-only connection, and commit the output for review. Hydrate this file against the project's datastore and credentials setup before invoking it."
---

> ⚠️ **STUB.** This skill has no working procedure yet. Before it can be
> invoked, fill in: which environments can be probed, how a read-only connection
> is _enforced_ (not merely intended), and where the output is written. Delete
> this banner once you have.

## What this skill is for

Answering "what does the data actually look like?" from the data itself, rather
than from the schema, the code, or a plausible guess. Most debugging that stalls
does so because everyone is reasoning about what _should_ be in the database.

## Concerns that hold regardless of stack

Each is something a hydrated version must handle.

### Enforce read-only at the transport

This is the one that matters. Read-only must be a property of the connection — a
read-only transaction, a replica endpoint, a credential with no write grant —
not a promise that the queries will only be `SELECT`s. Convention fails under a
typo; a credential without write permission does not. If the project can't
currently offer such a connection, creating one is part of hydrating this skill,
not a nice-to-have.

### Name the environment out loud

Every report says which environment it read. A finding from staging presented as
production is worse than no finding, and the two are indistinguishable after the
fact unless it's written down.

### Commit the output

Queries and results go in a file someone else can read, not just into the
transcript. The reasoning is reviewable, the numbers are checkable, and the next
person with the same question doesn't re-run it. Put it under
`docs/remove-before-merging/` if it rides a branch, so `/finalize` sweeps it
before merge.

### Sampling honesty

Say how many rows were examined and over what period. "Users often do X" from a
10-row sample is a guess wearing a statistic's clothes.

### PII

Real data contains real people. Aggregate where possible; redact before
committing anything that will outlive the session.

## Related

`/log-review` covers the same "look at reality rather than the code" instinct on
the logging side; the PII concern is identical in both.
