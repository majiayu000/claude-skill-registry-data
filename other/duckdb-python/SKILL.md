---
name: duckdb-python
description: Use for writing, reviewing, debugging, testing, or optimizing Python code that embeds DuckDB, executes analytical SQL, manages DuckDB connections and transactions, builds DuckDB relations, queries Parquet/CSV/Arrow/pandas/Polars inputs, or exports query results. Trigger on connection scope, parameters, replacement scans, materialization, concurrency, extensions, and query plans. Do not use for generic SQL with another engine, DuckDB CLI-only work, server-database administration, dbt-only projects, or dataframe work that does not call DuckDB.
argument-hint: "[DuckDB Python task, SQL, connection, plan, or error]"
---

# DuckDB Python

Produce explicit, injection-safe DuckDB integrations whose connection,
transaction, relation, input registration, result representation, and execution
boundary match the host application.

## Boundary

Use this skill when Python embeds DuckDB or invokes its Python client. SQL
semantics are in scope only for a DuckDB execution target. Do not introduce
DuckDB into a library-neutral dataframe task, and do not apply this skill to a
remote database just because its SQL resembles DuckDB.

## Know the runtime objects

| Object | Meaning | Use it for |
|---|---|---|
| Database | An in-memory catalog/storage instance or a persistent database file. | Choosing persistence, access mode, and process boundaries. |
| `DuckDBPyConnection` | A session with catalog, transaction, configuration, registered objects, and current result state. | All package/library query work; own its lifetime explicitly. |
| `DuckDBPyRelation` | A symbolic relational query associated with a connection. | Composable query construction before a fetch, display, write, or create boundary. |
| DB-API result on a connection | The current executed result consumed by `fetch*` methods. | Immediate parameterized statements and bounded result extraction. |
| Catalog table/view | Durable table or named logical query in the database. | Reuse across statements and connections according to persistence. |
| Registered Python object | A connection-scoped view over Arrow/dataframe input. | Explicitly exposing an in-memory object to SQL while preserving its lifetime. |
| Arrow reader/table or dataframe result | Materialized or batched data crossing out of DuckDB. | Matching the downstream consumer without unnecessary conversion. |

The module-level `duckdb.sql()` family uses a shared global connection. A
relation is lazy in the sense that it represents a query until a fetch, display,
write, or catalog-producing action, but not every relation construction is free
of metadata work. A cursor created from a connection is another handle on the
same connection: it can be thread-local, but queries through sibling handles
serialize instead of running concurrently. Read [the connection
and relation model](references/object-model.md) before changing lifetimes,
transactions, registration, or concurrency.

## Ordered workflow

1. Recover the contract: database location, read/write mode, caller-owned or
   callee-owned connection, transaction boundary, input sources, result object,
   expected cardinality/order, and memory limit.
2. In reusable code, accept or create an explicit connection. Avoid module-level
   query state. For parallel query execution, give each worker an independent
   connection; sharing one explicit connection or its cursor handles serializes
   queries and must be an intentional policy.
3. Parameterize values. For identifiers or SQL structure, use a fixed mapping or
   validated AST/building path; placeholders do not quote identifiers.
4. Choose SQL or the relational API for clarity, then keep one connection and
   one deferred query until the required output boundary.
5. Push filters and projections into file/table scans; avoid materializing an
   input dataframe or full query result merely to continue processing.
6. Choose `fetchone`/`fetchall`, Arrow batches/table, pandas, Polars, NumPy, file
   output, table, or view from the consumer contract.
7. Test values, types, nulls, cardinality, deterministic ordering, transaction
   behavior, and cleanup. Inspect `EXPLAIN` only for a plan claim.

## Choose by intent

| Need | Choose | Rule |
|---|---|---|
| Isolated package operation | Explicit `duckdb.connect(...)` or injected connection | Close only connections you own. |
| Several statements that must commit together | Explicit transaction | Roll back on failure; do not rely on incidental autocommit boundaries. |
| Values from untrusted input | DB-API/connection parameters | Never interpolate or concatenate them into SQL. |
| Dynamic column/table choice | Allowlisted mapping to known SQL fragments | A value placeholder cannot represent SQL identifiers. |
| Composable read-only query | `DuckDBPyRelation` or one SQL statement | Preserve deferral until the consumer boundary. |
| Large Arrow-capable consumer | Record-batch reader/fetch API | Do not fetch a full dataframe first. |
| Persistent result | `CREATE TABLE`, `INSERT`, or `COPY` under an explicit transaction/overwrite policy | Verify the reopened artifact or catalog object. |
| Temporary query over Python data | Explicit `register`/`unregister` | Keep the source alive and avoid accidental name capture. |
| File-backed analytics | Direct `read_parquet`/`read_csv` table function or relation | Keep projection/filter in DuckDB for pushdown. |

Read [the operation map](references/operations.md) for connection, query,
ingestion, export, extension, and plan choices.

## Canonical package boundary

```python
from collections.abc import Sequence
from pathlib import Path

import duckdb


SUMMARY_SQL = """
    SELECT customer_id, sum(amount) AS total_amount
    FROM read_parquet(?)
    WHERE amount >= ?
    GROUP BY customer_id
    ORDER BY total_amount DESC, customer_id ASC
"""


def customer_totals(
    parquet_path: Path,
    minimum_amount: float,
) -> Sequence[tuple[object, ...]]:
    with duckdb.connect(database=":memory:") as connection:
        return connection.execute(
            SUMMARY_SQL,
            [str(parquet_path), minimum_amount],
        ).fetchall()
```

The function owns and closes its connection, treats path and threshold as
values, and defines result ordering including a tie-breaker. If the result is
not proven small, change the public return contract to a batched Arrow reader or
write boundary; do not retain `fetchall()` and hope memory is sufficient.

## High-risk rules

### Connections, transactions, and threads

- Use explicit connection objects in libraries. Module-level calls share hidden
  state and can collide across packages or threads.
- One explicit connection is thread-safe in the current DB-API, but it locks for
  each query. Its `.cursor()` handles share that connection and therefore
  serialize. Give each worker an independent connection when actual parallel
  execution is required; use thread-local cursors only when shared-database,
  serialized access is the intended contract.
- State who owns each connection. A helper must not close an injected
  connection and must not return a relation tied to a connection it just closed.
- Wrap dependent writes in an explicit transaction and test rollback. Do not
  mix irreversible external file effects into a database rollback claim.
- Configure access mode, filesystem/network policy, memory, threads, and
  extension behavior at the intended scope rather than mutating a global
  default invisibly.

### SQL, names, and Python inputs

- Bind data values through parameters. Validate dynamic identifiers against a
  closed mapping; never use f-strings for untrusted SQL.
- Replacement scans can resolve Python variable names from scope. Prefer
  explicit registration in reusable code so dependencies and lifetime are
  visible, then unregister in a `finally` block when the connection continues.
- A registered dataframe/Arrow object is not automatically copied into a
  durable table. Keep its owner alive until the query is consumed.
- Never load unsigned or remote extensions merely to satisfy a prompt. Require
  explicit trust and environment policy; pin or inspect extension availability.

### Results and performance

- A relation or executed query becomes useful only at a consumer boundary.
  Choose the narrowest representation the consumer accepts and avoid dataframe
  round trips between DuckDB operations.
- SQL result order is contractual only with `ORDER BY`. Add stable tie-breakers
  when exact order matters.
- DuckDB can push projections and filters into Parquet scans, but prove the
  specific plan with `EXPLAIN` or profiling when performance is a requirement.
- `CREATE TABLE AS` copies data into DuckDB; a view over an external scan does
  not. Choose persistence intentionally and test reopening when required.
- Schema unification across files can hide drift or insert nulls. Enable it only
  under an explicit union contract and test missing, extra, reordered, and
  incompatible columns.

Run [the installed-API inspector](scripts/inspect_duckdb.py) and read [version and API
grounding](references/version-grounding.md). Test with [the DuckDB verification
matrix](references/testing.md).

## Completion gate

Do not declare completion until connection ownership and cleanup are tested;
values are parameterized and dynamic identifiers allowlisted; required writes
are atomic at the declared boundary; returned relations/readers do not outlive
their connection or source; result columns, DuckDB types, null behavior,
cardinality, and explicit order match the contract; large-result handling is
bounded; persisted output is reopened; and plan/performance claims have direct
evidence. Report unavailable extensions, skipped integration checks, and their
consequences.

## References

- [Query and result recipes](references/recipes-query.md)
- [Resource and persistence recipes](references/recipes-resources.md)
- [Connection and relation model](references/object-model.md)
- [Operation map](references/operations.md)
- [Version and API grounding](references/version-grounding.md)
- [Testing DuckDB integrations](references/testing.md)
