---
name: sqldb-consumption-cli
description: >
  Query SQL database in Fabric via sqlcmd: interactive exploration, vector similarity, JSON, temporal queries,
  and security policy inspection on the OLTP and SQL analytics endpoints. For schema changes see the sqldb-authoring-cli skill.
  Triggers: "sql database in Fabric query sys.tables sqlcmd",
  "sql database in Fabric system view list user tables sqlcmd",
  "list user tables sqldb", "sys.tables sqldb", "explore sqldb schema",
  "vector similarity sqldb", "RAG embedding sqldb", "row level security sqldb inspect",
  "audit log sqldb inspect", "chat with sqldb", "export sqldb rows",
  "temporal as of sqldb", "json openrowset sqldb".
---

> **Update Check — ONCE PER SESSION (mandatory)**
> The first time this skill is used in a session, run the **check-updates** skill before proceeding.
> - **GitHub Copilot CLI / VS Code**: invoke the `check-updates` skill.
> - **Claude Code / Cowork / Cursor / Windsurf / Codex**: compare local vs remote package.json version.
> - Skip if the check was already performed earlier in this session.

> **CRITICAL NOTES**
> 1. To find the workspace details (including its ID) from workspace name: list all workspaces and, then, use JMESPath filtering
> 2. To find the item details (including its ID) from workspace ID, item type, and item name: list all items of that type in that workspace and, then, use JMESPath filtering

# SQL Database Consumption — CLI Skill

Query **SQL database in Fabric** and its **SQL analytics endpoint** using `sqlcmd` and `az rest`. Supports interactive exploration, cross-database joins, vector / AI-RAG patterns, JSON, temporal queries, and security inspection.

> **READ-ONLY SKILL — REFUSE WRITES.** This is a consumption (read-only) skill. You **MUST NOT** execute any statement that modifies data or schema — `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `TRUNCATE`, or any DDL (`CREATE` / `ALTER` / `DROP`). If the user asks to change data or schema, **do not run it**. Instead, tell the user this is a read-only skill and route the request to **[sqldb-authoring-cli](../sqldb-authoring-cli/SKILL.md)**. Relying on database permissions is not sufficient — refuse the write at the skill level.

## Table of Contents

| Topic | Reference |
|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md § Finding Workspaces and Items in Fabric](../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) — **read first** |
| Authentication & token acquisition | [COMMON-CORE.md § Authentication](../../common/COMMON-CORE.md#authentication--token-acquisition) and [COMMON-CLI.md § Authentication Recipes](../../common/COMMON-CLI.md#authentication-recipes) |
| SQL / TDS Data-Plane Access (sqlcmd) | [COMMON-CLI.md § SQL / TDS Data-Plane Access](../../common/COMMON-CLI.md#sql--tds-data-plane-access) |
| CLI Gotchas (audience, escaping, expiry) | [COMMON-CLI.md § Gotchas & Troubleshooting](../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) |
| **Endpoint Selection** (OLTP vs analytics) | [SQLDB-CONSUMPTION-CORE.md § Endpoint Selection](../../common/SQLDB-CONSUMPTION-CORE.md#endpoint-selection) — **read first** |
| **Supported T-SQL, Cross-DB, JSON, Vector/RAG, Metadata, Security, Best Practices, Gotchas, Quick Reference** | [SQLDB-CONSUMPTION-CORE.md](../../common/SQLDB-CONSUMPTION-CORE.md) (all sections) |
| Temporal Tables / Data Virtualization | [SQLDB-AUTHORING-CORE.md § Temporal](../../common/SQLDB-AUTHORING-CORE.md#temporal-tables-system-versioned), [§ Data Virtualization](../../common/SQLDB-AUTHORING-CORE.md#data-virtualization-external-tables-and-openrowset) |
| Limitations Reference (mirroring, unsupported, resource limits) | [SQLDB-AUTHORING-CORE.md § Limitations Reference](../../common/SQLDB-AUTHORING-CORE.md#limitations-reference) |
| Discovery Queries (schemas, tables, indexes, security, settings, sessions) | [references/discovery-queries.md](references/discovery-queries.md) |
| **Deep Performance Diagnostics** | [sqldb-operations-cli](../sqldb-operations-cli/SKILL.md) |

For Fabric topology, capacity, OneLake, auth, control-plane REST, jobs see [COMMON-CORE.md](../../common/COMMON-CORE.md) and [COMMON-CLI.md](../../common/COMMON-CLI.md).

---

## Tool Stack

Prerequisites, installation, and CLI authentication/setup belong in [COMMON-CLI.md](../../common/COMMON-CLI.md). Use that guide before running the commands in this skill.

| Tool | Role |
|---|---|
| `sqlcmd` (Go) | **Primary**: Execute T-SQL queries. Standalone binary, no ODBC driver, built-in Entra ID auth via `DefaultAzureCredential`. |
| `az` CLI | Use Fabric REST for endpoint discovery and related control-plane lookups referenced by this skill. |
| `jq` | Parse JSON returned from `az rest` and related CLI output. |

---

## Connection

### Discover the SQL Database Endpoint

For workspace/item resolution, endpoint discovery, and shared `sqlcmd` connection guidance, use:

- [COMMON-CLI.md](../../common/COMMON-CLI.md) for finding workspaces/items and resolving endpoint details
- [COMMON-CORE.md](../../common/COMMON-CORE.md) for shared CLI/auth/connection guidance

> **Two endpoints exist** — see [SQLDB-CONSUMPTION-CORE.md](../../common/SQLDB-CONSUMPTION-CORE.md) Endpoint Selection:
> - **SQL Database endpoint** (OLTP): live transactional data, vector search, stored procedures.
> - **SQL Analytics Endpoint**: replicated read-only data, cross-database queries, BI.

### Connection guidance

For `sqlcmd` connection setup, authentication modes, connection-string patterns, and CI/CD auth examples, use the shared guidance in `common/COMMON-CLI.md` instead of copying setup templates into this skill.

For SQLDB-specific consumption in this skill, assume the connection inputs are already known:
- `serverFqdn`
- `databaseName`

```bash
# One-shot query against the discovered SQL database
sqlcmd <connection/auth args from common/COMMON-CLI.md> \
  -Q "SELECT TOP 10 * FROM dbo.Orders"

# Run a saved query file for sqldb exploration
sqlcmd <connection/auth args from common/COMMON-CLI.md> \
  -i my_query.sql
```

---

## Agentic Exploration ("Chat With My Data")

### Schema Discovery Sequence

Run these in order to understand what's in the database. See [discovery-queries.md](references/discovery-queries.md) for extended discovery queries.

```bash
# 1. List schemas
$SQLCMD -Q "SELECT schema_name FROM information_schema.schemata ORDER BY schema_name" -W

# 2. List tables with row counts
$SQLCMD -Q "SELECT s.name AS [schema], t.name AS [table], SUM(p.rows) AS row_count FROM sys.tables t JOIN sys.schemas s ON t.schema_id=s.schema_id JOIN sys.partitions p ON t.object_id=p.object_id AND p.index_id IN (0,1) GROUP BY s.name, t.name ORDER BY s.name, t.name" -W

# 3. Columns for a table
$SQLCMD -Q "SELECT column_name, data_type, character_maximum_length, is_nullable, column_default FROM information_schema.columns WHERE table_schema='dbo' AND table_name='Orders' ORDER BY ordinal_position" -W

# 4. Preview rows
$SQLCMD -Q "SELECT TOP 5 * FROM dbo.Orders" -W

# 5. Constraints (PK, FK, UNIQUE, CHECK)
$SQLCMD -Q "SELECT tc.constraint_name, tc.constraint_type, kcu.column_name FROM information_schema.table_constraints tc JOIN information_schema.key_column_usage kcu ON tc.constraint_name=kcu.constraint_name WHERE tc.table_schema='dbo' AND tc.table_name='Orders' ORDER BY tc.constraint_type" -W

# 6. Indexes
$SQLCMD -Q "SELECT i.name, i.type_desc, STRING_AGG(c.name,', ') WITHIN GROUP (ORDER BY ic.key_ordinal) AS cols FROM sys.indexes i JOIN sys.index_columns ic ON i.object_id=ic.object_id AND i.index_id=ic.index_id JOIN sys.columns c ON ic.object_id=c.object_id AND ic.column_id=c.column_id WHERE i.object_id=OBJECT_ID('dbo.Orders') GROUP BY i.name, i.type_desc" -W

# 7. Programmability objects (views, functions, procedures, triggers)
$SQLCMD -Q "SELECT name, type_desc FROM sys.objects WHERE type IN ('V','FN','IF','P','TF','TR') ORDER BY type_desc, name" -W
```

### Agentic Workflow

1. **Discover** → Run Steps 1–7 to understand available tables/columns.
2. **Sample** → `SELECT TOP 5` on relevant tables.
3. **Formulate** → Write T-SQL using [SQLDB-CONSUMPTION-CORE.md](../../common/SQLDB-CONSUMPTION-CORE.md) Supported T-SQL Surface Area. Most Azure SQL syntax is supported (temporal queries, JSON, data virtualization, IQP). Check AVOID section for exceptions (EXECUTE AS, CDC, Always Encrypted not available).
4. **Execute** → `$SQLCMD -Q "..."`.
5. **Iterate** → Refine based on results.
6. **Present** → Show results or generate a reusable script.

---

## Gotchas, Rules, Troubleshooting

For full consumption gotchas: [SQLDB-CONSUMPTION-CORE.md](../../common/SQLDB-CONSUMPTION-CORE.md) Gotchas and Troubleshooting Reference.
For CLI-specific issues: [COMMON-CLI.md](../../common/COMMON-CLI.md) Gotchas & Troubleshooting (CLI-Specific).

### MUST DO

- **Refuse all writes** — this is a read-only skill. Never run `INSERT` / `UPDATE` / `DELETE` / `MERGE` / `TRUNCATE` or any DDL (`CREATE` / `ALTER` / `DROP`). Inform the user it is read-only and route write/schema requests to [sqldb-authoring-cli](../sqldb-authoring-cli/SKILL.md).
- **Always `-d <DatabaseName>`** — FQDN alone is insufficient.
- **Always `-G` or `--authentication-method`** — SQL auth not supported on Fabric.
- **Follow [COMMON-CLI.md](../../common/COMMON-CLI.md) authentication guidance first** — keep Microsoft Entra / CLI auth prerequisites centralized there instead of repeating `az` login steps here.
- **Use SQL analytics endpoint for cross-database queries** — three-part naming fails on the OLTP endpoint.
- **Respect RLS** — query as end-user identity to test row-level security policies.
- **`SET NOCOUNT ON;`** in scripts — suppresses row-count messages that corrupt output.

### AVOID

- **ODBC sqlcmd** — use the Go version.
- **Omitting `-W`** in scripts — trailing spaces corrupt CSV.
- **Heavy analytical queries on the OLTP endpoint** — use the SQL analytics endpoint.
- **DML on the SQL analytics endpoint** — it is read-only.
- **MARS / `CREATE LOGIN` / SQL auth / `EXECUTE AS`** — not supported.
- **`CONTAINS` / `FREETEXT`** — full-text is preview only; use `LIKE`, `CHARINDEX`, or vector search.
- **Assuming the SQL analytics endpoint mirrors everything** — RLS/DDM/OLS, `vector`/`json` columns, computed columns, views, procedures, and functions are NOT propagated. See [Limitations Reference](../../common/SQLDB-AUTHORING-CORE.md#limitations-reference) and [Mirroring Considerations](../../common/SQLDB-AUTHORING-CORE.md#mirroring-considerations).
- **Hardcoded FQDNs** — discover via REST API.

### PREFER

- **`sqlcmd (Go) -G`** over curl+token for SQL queries.
- **`-Q`** (non-interactive exit) for agentic use.
- **SQL analytics endpoint** for heavy aggregation and BI queries (avoids OLTP impact). Note: max 1000 tables mirrored; RLS/DDM/OLS not propagated; vector/json columns excluded.
- **SQL database endpoint** for vector search, stored procedures, temporal queries, and any data requiring security policy enforcement.
- **Temporal queries** (`FOR SYSTEM_TIME AS OF`) for point-in-time analysis and audit.
- **OPENROWSET / external tables** to query OneLake files without import.
- **FOR JSON PATH** to export results as JSON; **OPENJSON** to parse JSON columns.
- **Copilot** — use `--` comments to guide code completion; use chat pane for NL-to-SQL.
- **Piped input** for multi-statement batches or queries with quotes.
- **`-i file.sql`** for complex queries — avoids shell escaping.
- **`-F vertical`** for exploration of wide tables.
- **Env vars** (`FABRIC_SERVER`, `FABRIC_DB`) for script reuse.

### TROUBLESHOOTING

| Symptom | Cause | Fix |
|---|---|---|
| `Login failed for user` | Wrong DB name or no access | Verify `-d` matches the REST `properties.databaseName` value (see COMMON-CLI.md "Discovering Connection Parameters via REST"), and that you have permission |
| `Cannot open server` | Wrong FQDN or network | Re-discover via REST API; check port 1433 |
| `Login timeout expired` | Port 1433 blocked | `nc -zv <endpoint>.database.fabric.microsoft.com 1433`; check firewall/VPN |
| `ActiveDirectoryDefault` failure | `az login` expired or wrong tenant | Re-authenticate using the Azure CLI troubleshooting/auth guidance in [COMMON-CLI.md](../../common/COMMON-CLI.md) |
| Cross-database query fails | Using OLTP endpoint | Switch to SQL analytics endpoint for three-part naming |
| Data appears stale in analytics endpoint | Mirroring replication lag | Wait for replication; check status via `sys.dm_change_feed_log_scan_sessions` |
| Table missing from analytics endpoint | Table exceeds 1000-table mirror limit, or has unsupported PK type, or uses CCI/in-memory/Always Encrypted | Check `sys.dm_change_feed_errors`; see [mirroring limitations](https://learn.microsoft.com/en-us/fabric/database/sql/mirroring-limitations) |
| Column missing from analytics endpoint | Computed column, or unsupported type (image, text, xml, sql_variant, geometry, geography, hierarchyid, vector, json) | Query the OLTP endpoint for these columns |
| LOB data truncated on analytics endpoint | LOB columns > 1 MB are truncated in OneLake | Query the OLTP endpoint for full LOB data |
| datetime2(7) precision loss on analytics endpoint | Delta Lake supports only 6 digits of precision | 7th fractional digit is trimmed; use OLTP endpoint if precision is critical |
| RLS/DDM not enforced on analytics endpoint | Security policies not propagated to OneLake | Query the OLTP endpoint to enforce security policies |
| Vector search returns no results | NULL embeddings or dimension mismatch | Verify `WHERE Embedding IS NOT NULL`; check dimensions |
| RLS not filtering as expected | Wrong security predicate or user context | Check `USER_NAME()` value; verify policy with `sys.security_policies` |
| `sys.fn_get_audit_file_v2` returns no rows | Auditing not enabled | Enable auditing via REST API (`PATCH .../settings/sqlAudit`) or Fabric portal |
| Garbled CSV output | Missing `-W` or wrong `-s` | Add `-W -s"," -w 4000` |
| `(N rows affected)` in file | No `SET NOCOUNT ON` | Prepend `SET NOCOUNT ON;` |
| `sqlcmd` not found | `sqlcmd` is not installed or not on `PATH` | See `common/COMMON-CLI.md` for `sqlcmd` installation and setup guidance |
| `Login timeout expired` on redirect | Connection policy requires ports 11000–11999 | Allow outbound to Azure SQL IPs on ports 11000–11999 in addition to 1433 |
