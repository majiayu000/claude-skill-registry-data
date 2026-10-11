---
name: sqlserver
description: SQL Server — T-SQL, indexes, Always On AG, CDC, columnstore.
---

# SQL Server Reference

## When to Load
Load when the project uses SQL Server or Azure SQL (signal: `mssql`, `tedious`, `pyodbc`, `sqlserver` in connection string, `SQL_SERVER` env var, `mcr.microsoft.com/mssql` in docker-compose).

## CLI Connection

```bash
# sqlcmd (installed with SQL Server tools):
sqlcmd -S "$DB_HOST,$DB_PORT" -U "$DB_USER" -P "$DB_PASSWORD" -d "$DB_NAME"
# with Azure AD:
sqlcmd -S "$DB_HOST" -G -d "$DB_NAME"

# mssql-cli (cross-platform, pip install mssql-cli):
mssql-cli -S "$DB_HOST" -U "$DB_USER" -P "$DB_PASSWORD" -d "$DB_NAME"

# Docker-hosted SQL Server:
docker exec -it <container> /opt/mssql-tools/bin/sqlcmd \
  -S localhost -U sa -P "$SA_PASSWORD" -d "$DB_NAME"
```

Key inspection queries:
```sql
SELECT @@VERSION;                                          -- version
SELECT * FROM sys.dm_exec_requests WHERE status = 'running'; -- active queries
SELECT * FROM sys.dm_os_wait_stats ORDER BY waiting_tasks_count DESC; -- waits
EXEC sp_who2;                                             -- connections + blocking
```

## T-SQL Specifics

- `TOP n` replaces `LIMIT`: `SELECT TOP 10 * FROM orders ORDER BY created_at DESC`
- `ISNULL(col, default)` vs standard `COALESCE` — prefer `COALESCE` for portability
- `@@ROWCOUNT` / `@@ERROR` after DML (use `TRY…CATCH` for error handling)
- `NOCOUNT ON` in stored procedures to suppress row-count messages
- `OUTPUT` clause: capture inserted/deleted rows in a single statement

```sql
INSERT INTO orders (user_id, total)
OUTPUT INSERTED.id, INSERTED.created_at
VALUES (@user_id, @total);
```

## Indexes

| Type | Use when |
|------|----------|
| Clustered | Physical row order; one per table; choose a sequential, narrow key (INT identity or sequential GUID) |
| Non-clustered | Additional access paths; up to 999 per table |
| Columnstore (clustered) | OLAP / data warehouse; batch-mode execution; 5–10× compression |
| Columnstore (non-clustered) | HTAP: add on OLTP table without changing clustered index |
| Filtered | Index a subset: `WHERE deleted_at IS NULL` |
| Full-text | `CONTAINS`, `FREETEXT` search on varchar/nvarchar columns |

- Avoid `NEWID()` as a clustered key — causes page fragmentation; use `NEWSEQUENTIALID()` or `INT IDENTITY`
- Check fragmentation: `sys.dm_db_index_physical_stats`; rebuild if > 30%, reorganize if 10–30%

## Transactions & Isolation

Default isolation: `READ COMMITTED` with shared locks (blocking reads).

| Isolation | Behaviour |
|-----------|-----------|
| `READ COMMITTED SNAPSHOT` (RCSI) | Row versioning instead of shared locks; set at DB level; recommended for OLTP |
| `SNAPSHOT` | Full transaction-level read consistency; may get `3960` update conflicts |
| `SERIALIZABLE` | Full locking; use only for strict invariant enforcement |

Enable RCSI: `ALTER DATABASE db SET READ_COMMITTED_SNAPSHOT ON;` — eliminates most reader/writer blocking with no application code change.

## Always On Availability Groups

- Primary replica handles reads and writes; secondary replicas are readable (with `READ_INTENT_ONLY`)
- Synchronous commit: zero data loss, slight latency; asynchronous: no latency, potential data loss on failover
- Connection string: `ApplicationIntent=ReadOnly` routes to readable secondary
- Monitor: `sys.dm_hadr_availability_replica_states`, `sys.dm_hadr_database_replica_states`

## Change Data Capture (CDC)

```sql
-- Enable CDC on database:
EXEC sys.sp_cdc_enable_db;

-- Enable CDC on a table:
EXEC sys.sp_cdc_enable_table
  @source_schema = N'dbo',
  @source_name   = N'orders',
  @role_name     = NULL;

-- Query changes:
SELECT * FROM cdc.fn_cdc_get_all_changes_dbo_orders(
  @from_lsn, @to_lsn, N'all');
```

CDC capture job runs every 5 s by default; cleanup job purges after 3 days.

## Common Gotchas

| Gotcha | Fix |
|--------|-----|
| `NVARCHAR` vs `VARCHAR` — implicit conversion blocks index use | Match parameter type to column type; use `N'...'` for nvarchar literals |
| Statistics not updated → bad query plans | `UPDATE STATISTICS` or enable `AUTO_UPDATE_STATISTICS` |
| `SELECT INTO` does not preserve indexes | Create indexes explicitly after `SELECT INTO` |
| Implicit transactions in some drivers | Set `SET IMPLICIT_TRANSACTIONS OFF`; or use explicit `BEGIN TRAN` |
| Parameter sniffing causes slow plans after data distribution changes | Use `OPTION (RECOMPILE)` or `OPTIMIZE FOR UNKNOWN` on affected queries |
| `GETDATE()` vs `GETUTCDATE()` | Always store in UTC; use `GETUTCDATE()` or `SYSUTCDATETIME()` |
