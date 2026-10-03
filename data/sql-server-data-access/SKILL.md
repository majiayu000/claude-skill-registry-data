---
name: sql-server-data-access
description: SQL Server data access standards for .NET systems — T-SQL coding rules, stored procedure contracts, EF Core and Dapper coexistence per module recipe, expand/contract migrations, index design, SARGability, parameter sniffing, isolation levels, RCSI, deadlocks, and execution plan review. Use for any .sql file, migration, stored procedure, Dapper query, EF Core query performance issue, schema change, locking/deadlock problem, or when deciding where SQL logic is allowed.
user-invocable: false
---
# SQL Server Data Access

## 1. Where logic may live (from the profile)
| Module domain_logic | Business rules in SQL | SPs for writes | SPs for reads |
|---|---|---|---|
| domain-model | ❌ (constraints as last line of defense only) | ❌ (except bulk/maintenance) | ✅ |
| transaction-script | ✅ if covered by integration tests | ✅ | ✅ |
| table-module | ✅ natural home | ✅ | ✅ |

## 2. T-SQL rules
- `SET NOCOUNT ON; SET XACT_ABORT ON;` at the top of every procedure.
- Schema-qualify every object; explicit column lists; no `SELECT *` outside `EXISTS`.
- `BEGIN TRY / BEGIN TRAN … COMMIT / END TRY BEGIN CATCH IF @@TRANCOUNT > 0 ROLLBACK; THROW; END CATCH`.
- Types: `datetime2(3)` (or `datetimeoffset` when offset matters), `date` for dates, `decimal(19,4)` money,
  `bit` flags, `uniqueidentifier` with sequential generation (v7 from app) or `bigint` identity, sized `nvarchar(n)`.
- SARGable predicates: no functions on indexed columns, no implicit conversions (match parameter types exactly),
  date ranges as `>= @From AND < @ToExclusive`.
- Set-based over cursors/loops; `MERGE` only with `HOLDLOCK` and a reason — prefer explicit `UPDATE` + `INSERT … WHERE NOT EXISTS`.
- No `NOLOCK`. Use RCSI (database-level) for read/write contention.
- Temp tables for multi-step processing with statistics needs; table variables only for tiny sets.
- Dynamic SQL only via `sp_executesql` with parameters; whitelist identifiers with `QUOTENAME`.

## 3. Stored procedure contract
- Name `{schema}.{Entity}_{Verb}` (e.g. `reporting.SaftD406_GenerateSalesInvoices`).
- Inputs typed exactly as target columns; table-valued parameters for sets.
- One result shape per procedure (or documented multiple result sets in fixed order).
- Error signaling: `THROW 50000 + <code>` with codes documented; the app maps codes to `Error`.
- Grant `EXECUTE` to the module's DB role only.

## 4. EF Core + Dapper coexistence
- Writes via EF (domain-model) share the connection/transaction with Dapper when needed:
  `db.Database.GetDbConnection()` + `db.Database.CurrentTransaction?.GetDbTransaction()`.
- Reads: EF `AsNoTracking().Select()` for simple shapes; Dapper for complex SQL. Never materialize entities to map to DTOs.
- Compiled queries or `EF.CompileAsyncQuery` for hot paths; `AsSplitQuery` when cartesian explosion appears.
- Command timeout set per use case for reports; never globally huge.

## 5. Migrations — expand / migrate / contract
1. **Expand:** add nullable column / new table / new index `ONLINE = ON` (edition permitting); deploy app writing both.
2. **Migrate:** backfill in batches (`TOP (5000)` loops with `WAITFOR DELAY` if needed), verifiable counts.
3. **Contract:** make NOT NULL / drop old column in a later release after all readers moved.
- Large-table changes: estimate row count and lock impact; schedule; avoid size-of-data operations in peak hours.
- Every migration idempotent (`IF NOT EXISTS`) for DbUp/sqlproj; EF migrations reviewed as SQL (`dotnet ef migrations script`).

## 6. Indexing
- Clustered key: narrow, static, ever-increasing when possible.
- Nonclustered for each important read predicate: equality columns first, then range, `INCLUDE` for covered columns.
- Filtered indexes for status-based queues (`WHERE Status = 'Pending'`).
- Every new index states its write cost and the queries it serves. Remove unused ones (sys.dm_db_index_usage_stats) via ADR-less maintenance plan.

## 7. Performance investigation procedure
Read `references/performance-playbook.md`. Summary: reproduce with real parameters → actual plan +
`STATISTICS IO, TIME` → look for scans with high reads, key lookups, implicit conversions, bad
estimates → Query Store for regressions/parameter sniffing → fix query first, index second, hints last.

## 8. Concurrency
- Default `READ COMMITTED` + RCSI enabled at DB level.
- Optimistic concurrency via `rowversion` on aggregate roots; map conflicts to a domain-level error.
- Sequences needing no gaps (fiscal numbering): dedicated row per series updated with `UPDLOCK, HOLDLOCK` in the same transaction as the insert; document serialization impact.
- Deadlocks: capture from `system_health` XE; fix access order and indexing before retry logic; retries only for idempotent operations.
