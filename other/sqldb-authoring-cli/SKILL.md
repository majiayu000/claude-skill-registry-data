---
name: sqldb-authoring-cli
description: >
  Create and manage SQL database in Fabric items, author T-SQL DDL/DML with constraints, foreign keys, triggers,
  indexes, and vector columns. Deploy schema via SqlPackage (.dacpac/.bacpac), configure source control,
  CI/CD, and GraphQL APIs.
  Triggers: "sql database in Fabric create table sqlcmd ddl",
  "sql database in Fabric primary key default getdate sqlcmd",
  "create sqldb item", "create table sqldb ddl", "sqldb foreign key constraint",
  "sqldb stored procedure", "sqldb trigger create", "sqldb vector column",
  "SqlPackage dacpac deploy sqldb", "bacpac sqldb", "sqldb source control",
  "graphql api sqldb", "sqldb collation set", "sp_invoke_external_rest_endpoint".
---

> **Update Check — ONCE PER SESSION (mandatory)**
> The first time this skill is used in a session, run the **check-updates** skill before proceeding.
> - **GitHub Copilot CLI / VS Code**: invoke the `check-updates` skill.
> - **Claude Code / Cowork / Cursor / Windsurf / Codex**: compare local vs remote package.json version.
> - Skip if the check was already performed earlier in this session.

> **CRITICAL NOTES**
> 1. To find the workspace details (including its ID) from workspace name: list all workspaces and, then, use JMESPath filtering
> 2. To find the item details (including its ID) from workspace ID, item type, and item name: list all items of that type in that workspace and, then, use JMESPath filtering

# SQL Database Authoring — CLI Skill

Create and manage **SQL database in Fabric** items, author T-SQL DDL/DML, deploy schema via SqlPackage, configure source control, CI/CD, and GraphQL APIs using `sqlcmd` and `az rest`.

## Table of Contents

| Topic | Reference |
|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md § Finding Workspaces and Items in Fabric](../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) — **read first** |
| Authentication & token acquisition | [COMMON-CORE.md § Authentication](../../common/COMMON-CORE.md#authentication--token-acquisition) and [COMMON-CLI.md § Authentication Recipes](../../common/COMMON-CLI.md#authentication-recipes) |
| SQL / TDS Data-Plane Access (sqlcmd) | [COMMON-CLI.md § SQL / TDS Data-Plane Access](../../common/COMMON-CLI.md#sql--tds-data-plane-access) |
| CLI Gotchas (audience, escaping, expiry) | [COMMON-CLI.md § Gotchas & Troubleshooting](../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) |
| SQL Database item definitions (`dacpac`/`sqlproj`) | [ITEM-DEFINITIONS-CORE.md § Per-Item-Type Definitions](../../common/ITEM-DEFINITIONS-CORE.md#per-item-type-definitions) |
| **SQL Database vs DW capability matrix** | [SQLDB-AUTHORING-CORE.md § SQL Database vs Data Warehouse](../../common/SQLDB-AUTHORING-CORE.md#sql-database-vs-data-warehouse--authoring-capability-matrix) |
| **Database Lifecycle, Table DDL, Temporal, Views, DML, BCP, Procs/Functions/Triggers, SqlPackage, Source Control, GraphQL, Mirroring, Auditing, CMK, Permissions, Gotchas, Patterns, Decision Guide** | [SQLDB-AUTHORING-CORE.md](../../common/SQLDB-AUTHORING-CORE.md) (all sections) |
| T-SQL Anti-Patterns | [SQLDB-AUTHORING-CORE.md § T-SQL Anti-Patterns](../../common/SQLDB-AUTHORING-CORE.md#t-sql-anti-patterns) |
| Schema Design Guidance | [SQLDB-AUTHORING-CORE.md § Schema Design Guidance](../../common/SQLDB-AUTHORING-CORE.md#schema-design-guidance) |
| **Limitations Reference** (unsupported features, resource limits) | [SQLDB-AUTHORING-CORE.md § Limitations Reference](../../common/SQLDB-AUTHORING-CORE.md#limitations-reference) |
| Endpoint Selection | [SQLDB-CONSUMPTION-CORE.md § Endpoint Selection](../../common/SQLDB-CONSUMPTION-CORE.md#endpoint-selection) |
| Metadata and Schema Discovery | [SQLDB-CONSUMPTION-CORE.md § Metadata and Schema Discovery](../../common/SQLDB-CONSUMPTION-CORE.md#metadata-and-schema-discovery) |
| Deep Performance Diagnostics | [sqldb-operations-cli](../sqldb-operations-cli/SKILL.md) |

For Fabric topology, capacity, OneLake, auth, control-plane REST, jobs see [COMMON-CORE.md](../../common/COMMON-CORE.md) and [COMMON-CLI.md](../../common/COMMON-CLI.md).

---

## Tool Stack

| Tool | Role | Setup Reference |
|---|---|---|
| `sqlcmd` (Go) | **Primary**: Execute DDL/DML T-SQL. Standalone binary, no ODBC, built-in Entra ID auth. | See [COMMON-CLI.md](../../common/COMMON-CLI.md) for installation and authentication prerequisites. |
| `sqlpackage` | Schema deployment (.dacpac), database portability (.bacpac). | See [COMMON-CLI.md](../../common/COMMON-CLI.md) for installation and environment setup prerequisites. |
| `az` CLI | Fabric REST for endpoint discovery and database creation. | See [COMMON-CLI.md](../../common/COMMON-CLI.md) for Azure CLI authentication and token setup. |
| `jq` | Parse JSON from `az rest`. | See [COMMON-CLI.md](../../common/COMMON-CLI.md) for shared CLI/tooling prerequisites. |

> **Agent check** — before first operation, confirm the required CLI tools and authentication are already configured by following the shared setup guidance in [COMMON-CLI.md](../../common/COMMON-CLI.md). Do not duplicate install or `az login` steps in this skill.

---

## Connection

### Discover the SQL Database TDS Endpoint

For workspace/item resolution, SQL Database endpoint discovery, and CLI connection patterns, use the shared guidance in `common/COMMON-CLI.md` and `common/COMMON-CORE.md` instead of embedding `az rest` or `sqlcmd` recipes here.

> Follow the SQL Database endpoint discovery steps in [COMMON-CLI.md](../../common/COMMON-CLI.md), then bring the discovered server FQDN and database name back into this skill for SQLDB-specific authoring and deployment tasks.

- Use the SQL Database endpoint values returned by Fabric for the target item; do not hardcode endpoint domains or database names.
- When generating deployment or authoring steps, treat connectivity details as inputs discovered via the shared common guidance.
- Focus this skill on schema authoring, DDL/DML design, constraints, indexing, source control, SqlPackage deployment, and GraphQL/API behaviors rather than connection bootstrapping.

### Connection guidance

If the user needs help connecting interactively or from CI/CD, refer them to `common/COMMON-CLI.md` for the shared `sqlcmd` setup, authentication, and invocation patterns.

For SQLDB-specific authoring in this skill, assume the connection inputs are already known:
- `serverFqdn`
- `databaseName`

---

## Agentic Workflows

### Schema Discovery Before Authoring

Before any write operation, discover the target schema:

```bash
# 1. List tables
$SQLCMD -Q "SELECT table_schema, table_name FROM information_schema.tables WHERE table_type='BASE TABLE' ORDER BY 1,2" -W

# 2. Check columns
$SQLCMD -Q "SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name='Orders' ORDER BY ordinal_position" -W

# 3. Sample data
$SQLCMD -Q "SELECT TOP 5 * FROM dbo.Orders" -W

# 4. Check constraints
$SQLCMD -Q "SELECT tc.constraint_name, tc.constraint_type, kcu.column_name FROM information_schema.table_constraints tc JOIN information_schema.key_column_usage kcu ON tc.constraint_name=kcu.constraint_name WHERE tc.table_name='Orders' ORDER BY tc.constraint_type" -W

# 5. Check indexes
$SQLCMD -Q "SELECT i.name, i.type_desc, STRING_AGG(c.name,', ') WITHIN GROUP (ORDER BY ic.key_ordinal) AS cols FROM sys.indexes i JOIN sys.index_columns ic ON i.object_id=ic.object_id AND i.index_id=ic.index_id JOIN sys.columns c ON ic.object_id=c.object_id AND ic.column_id=c.column_id WHERE i.object_id=OBJECT_ID('dbo.Orders') GROUP BY i.name, i.type_desc" -W

# 6. Row counts
$SQLCMD -Q "SELECT s.name AS [schema], t.name AS [table], SUM(p.rows) AS row_count FROM sys.tables t JOIN sys.schemas s ON t.schema_id=s.schema_id JOIN sys.partitions p ON t.object_id=p.object_id AND p.index_id IN (0,1) GROUP BY s.name, t.name ORDER BY row_count DESC" -W

# 7. Programmability objects
$SQLCMD -Q "SELECT name, type_desc FROM sys.objects WHERE type IN ('V','FN','IF','P','TF','TR') ORDER BY type_desc, name" -W
```

### Workflow

1. **Discover** → Run steps 1–5 to understand available tables/columns.
2. **Sample** → `SELECT TOP 5` on relevant tables.
3. **Formulate** → Select pattern from [SQLDB-AUTHORING-CORE.md](../../common/SQLDB-AUTHORING-CORE.md) (Table DDL, Temporal Tables, Data Virtualization, Views, DML, etc.).
4. **Execute** → `$SQLCMD -Q "..."` or `$SQLCMD -i file.sql` for multi-statement.
5. **Verify** → Query affected table (`SELECT COUNT(*)`, `SELECT TOP 5`).
6. **Deploy (optional)** → Extract with `sqlpackage /Action:Extract` for .dacpac; set up source control.

---

## Gotchas, Rules, Troubleshooting

For full authoring gotchas: [SQLDB-AUTHORING-CORE.md](../../common/SQLDB-AUTHORING-CORE.md) Authoring Gotchas and Troubleshooting.
For CLI-specific issues: [COMMON-CLI.md](../../common/COMMON-CLI.md) Gotchas & Troubleshooting (CLI-Specific).

### MUST DO

- **Verify workspace has capacity before creating database** — call `GET /v1/workspaces/{id}` and check `capacityId`.
- **Always `-d <DatabaseName>`** — FQDN alone is insufficient.
- **Always `-G` or `--authentication-method`** — SQL auth not supported on Fabric.
- **Follow [COMMON-CLI.md](../../common/COMMON-CLI.md) authentication guidance first** — `ActiveDirectoryDefault` depends on an authenticated CLI session.
- **Specify collation at creation** — cannot be changed after the database is created.
- **Use SqlPackage for repeatable deployments** — extract .dacpac → publish for incremental schema changes.
- **Use `-i file.sql`** for multi-statement batches (CREATE PROCEDURE, transactions with GO separators).
- **`SET NOCOUNT ON;`** in scripts — suppresses row-count messages that corrupt output.

### AVOID

- **ODBC sqlcmd** (`/opt/mssql-tools/bin/sqlcmd`) — use the Go version.
- **Omitting `-W`** in scripts — trailing spaces corrupt CSV.
- **Hardcoded FQDNs** — discover via REST API.
- **MARS** — not supported. Remove `MultipleActiveResultSets`.
- **`CREATE LOGIN` / SQL authentication** — Entra users only.
- **Modifying tables with CCI / `ALTER INDEX ALL` while mirroring is active** — stop mirroring or alter individual indexes.
- **`vector` / `json` columns on tables that must mirror** — cannot be mirrored to OneLake.
- **Special characters in DB / column names** — see [Limitations Reference](../../common/SQLDB-AUTHORING-CORE.md#limitations-reference).
- **Modifying `.sqlproj` in source-controlled repo** — reset on next sync.
- **Unsupported features** (CDC, Always Encrypted, in-memory, ledger, full-text GA, partition SWITCH, `EXECUTE AS`, `hierarchyid`/`sql_variant`/`timestamp` PKs, CTAS, COPY INTO) — see [Limitations Reference](../../common/SQLDB-AUTHORING-CORE.md#limitations-reference) for the full list.
- **Exceeding resource limits** (32 vCores, 4 TB, 1024 GB tempdb, 150 DBs/workspace).

### PREFER

- **`az rest`** for database creation over portal — scriptable and repeatable.
- **SqlPackage publish (.dacpac)** over manual DDL for schema evolution — tracks incremental changes.
- **Enforced constraints** (PK, FK, CHECK, DEFAULT) — SQL Database supports them fully, unlike DW.
- **Temporal tables** for audit trails and slowly-changing dimensions — full system-versioning available. Note: history table is excluded from mirroring.
- **Data virtualization** (external tables / OPENROWSET) to query OneLake without ETL. Note: external tables themselves are not mirrored.
- **`INSERT ... SELECT`** for bulk data movement within the database.
- **BCP** for high-performance bulk import/export.
- **Native AI functions / sp_invoke_external_rest_endpoint** for embedding generation in T-SQL.
- **`sqlcmd (Go) -G`** over curl+token for SQL queries.
- **`-Q`** (non-interactive exit) for agentic use.
- **`-i file.sql`** over `-Q "..."` for anything beyond simple one-liners.
- **`-F vertical`** for exploration of wide tables.
- **Env vars** (`FABRIC_SERVER`, `FABRIC_DB`) for script reuse.
- **Auto-tuning** — let the engine manage indexes; check `sys.dm_db_tuning_recommendations` periodically.
- **Optimized locking** — enabled by default; reduces lock memory and eliminates lock escalation.

### TROUBLESHOOTING

| Symptom | Fix |
|---|---|
| SqlPackage auth error | Use `Authentication=Active Directory Default` in connection string |
| `Login failed for user` | Verify `-d` matches database display name exactly (case-sensitive) |
| `Cannot open server` / `Login timeout expired` | Re-discover FQDN via REST API; check port 1433 / firewall |
| `ActiveDirectoryDefault` failure | `az login` session may be expired — refresh Azure CLI authentication per `common/COMMON-CLI.md` |
| Collation error after creation | Cannot change — must recreate database with desired collation |
| Foreign key violation on INSERT | Check referenced table has matching row; verify column types |
| Vector insert dimension mismatch | Ensure vector literal has exactly the declared dimensions |
| CCI creation fails on existing table | Stop mirroring, create index, restart mirroring. CCI created inline with CREATE TABLE also prevents mirroring of that table |
| Table not mirrored after DDL change | DDL changes trigger a full data reseed; table with unsupported PK type or >1000 tables are skipped |
| Vector/json column prevents mirroring | Tables with `vector` or `json` columns cannot be mirrored; use OLTP endpoint to query these |
| Computed columns missing from analytics endpoint | Computed columns are skipped during mirroring |
| LOB data truncated on analytics endpoint | LOB columns > 1 MB are truncated in OneLake |
| `ALTER INDEX ALL` fails | Not allowed while mirroring is active; alter individual indexes by name |
| Garbled CSV / `(N rows affected)` in file | Add `-W -s"," -w 4000`; prepend `SET NOCOUNT ON;` |
| `sp_invoke_external_rest_endpoint` 401 | Create/verify database-scoped credential for target URL |
| `sqlcmd` not found | Ensure `sqlcmd` is installed and on `PATH`; follow the shared CLI setup guidance in `common/COMMON-CLI.md` |
| Connection fails on redirect ports | Connection policy requires ports 11000–11999 open in addition to 1433 |
