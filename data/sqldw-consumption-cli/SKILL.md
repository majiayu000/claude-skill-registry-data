---
name: sqldw-consumption-cli
description: >
  Execute read-only T-SQL queries against Fabric Data Warehouse, Lakehouse SQL Endpoints, and Mirrored Databases
  via CLI. Default skill for any lakehouse data query (row counts, SELECT, filtering, aggregation) unless the user
  explicitly requests PySpark or Spark DataFrames. Use when the user wants to: (1) query warehouse/lakehouse data,
  (2) count rows or explore lakehouse tables, (3) discover schemas/columns, (4) generate T-SQL scripts,
  (5) monitor SQL performance, (6) export results to CSV/JSON.
  Triggers: "warehouse", "SQL query", "T-SQL", "query warehouse", "show warehouse tables",
  "show lakehouse tables", "query lakehouse", "lakehouse table", "how many rows", "count rows",
  "SQL endpoint", "describe warehouse schema", "generate T-SQL script", "warehouse performance",
  "export SQL data", "connect to warehouse", "lakehouse data", "explore lakehouse".
---

> **Update Check — ONCE PER SESSION (mandatory)**
> The first time this skill is used in a session, run the **check-updates** skill before proceeding.
> - **GitHub Copilot CLI / VS Code**: invoke the `check-updates` skill.
> - **Claude Code / Cowork / Cursor / Windsurf / Codex**: compare local vs remote package.json version.
> - Skip if the check was already performed earlier in this session.

> **CRITICAL NOTES**
> 1. To find the workspace details (including its ID) from workspace name: list all workspaces and, then, use JMESPath filtering
> 2. To find the item details (including its ID) from workspace ID, item type, and item name: list all items of that type in that workspace and, then, use JMESPath filtering

# SQL Endpoint Consumption — CLI Skill

## Table of Contents

| Task | Reference | Notes |
|---|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md § Finding Workspaces and Items in Fabric](../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) | **Mandatory** — *READ link first* [needed for finding workspace id by its name or item id by its name, item type, and workspace id]|
| Fabric Topology & Key Concepts | [COMMON-CORE.md § Fabric Topology & Key Concepts](../../common/COMMON-CORE.md#fabric-topology--key-concepts) ||
| Environment URLs | [COMMON-CORE.md § Environment URLs](../../common/COMMON-CORE.md#environment-urls) ||
| Authentication & Token Acquisition | [COMMON-CORE.md § Authentication & Token Acquisition](../../common/COMMON-CORE.md#authentication--token-acquisition) | Wrong audience = 401; read before any auth issue |
| Core Control-Plane REST APIs | [COMMON-CORE.md § Core Control-Plane REST APIs](../../common/COMMON-CORE.md#core-control-plane-rest-apis) | Includes pagination, LRO polling, and rate-limiting patterns |
| OneLake Data Access | [COMMON-CORE.md § OneLake Data Access](../../common/COMMON-CORE.md#onelake-data-access) | Requires `storage.azure.com` token, not Fabric token |
| Job Execution | [COMMON-CORE.md § Job Execution](../../common/COMMON-CORE.md#job-execution) ||
| Capacity Management | [COMMON-CORE.md § Capacity Management](../../common/COMMON-CORE.md#capacity-management) ||
| Gotchas, Best Practices & Troubleshooting | [COMMON-CORE.md § Gotchas, Best Practices & Troubleshooting](../../common/COMMON-CORE.md#gotchas-best-practices--troubleshooting) ||
| Tool Selection Rationale | [COMMON-CLI.md § Tool Selection Rationale](../../common/COMMON-CLI.md#tool-selection-rationale) ||
| Authentication Recipes | [COMMON-CLI.md § Authentication Recipes](../../common/COMMON-CLI.md#authentication-recipes) | `az login` flows and token acquisition |
| Fabric Control-Plane API via `az rest` | [COMMON-CLI.md § Fabric Control-Plane API via az rest](../../common/COMMON-CLI.md#fabric-control-plane-api-via-az-rest) | **Always pass `--resource`**; includes pagination and LRO helpers |
| OneLake Data Access via `curl` | [COMMON-CLI.md § OneLake Data Access via curl](../../common/COMMON-CLI.md#onelake-data-access-via-curl) | Use `curl` not `az rest` (different token audience) |
| SQL / TDS Data-Plane Access | [COMMON-CLI.md § SQL / TDS Data-Plane Access](../../common/COMMON-CLI.md#sql--tds-data-plane-access) | `sqlcmd` (Go) connect, query, CSV export |
| Job Execution (CLI) | [COMMON-CLI.md § Job Execution](../../common/COMMON-CLI.md#job-execution) ||
| OneLake Shortcuts | [COMMON-CLI.md § OneLake Shortcuts](../../common/COMMON-CLI.md#onelake-shortcuts) ||
| Capacity Management (CLI) | [COMMON-CLI.md § Capacity Management](../../common/COMMON-CLI.md#capacity-management) ||
| Composite Recipes | [COMMON-CLI.md § Composite Recipes](../../common/COMMON-CLI.md#composite-recipes) ||
| Gotchas & Troubleshooting (CLI-Specific) | [COMMON-CLI.md § Gotchas & Troubleshooting (CLI-Specific)](../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) | `az rest` audience, shell escaping, token expiry |
| Quick Reference | [COMMON-CLI.md § Quick Reference](../../common/COMMON-CLI.md#quick-reference) | `az rest` template + token audience/tool matrix |
| Item-Type Capability Matrix | [SQLDW-CONSUMPTION-CORE.md § Item-Type Capability Matrix](../../common/SQLDW-CONSUMPTION-CORE.md#item-type-capability-matrix) | **Read first** — shows what's read-only (SQLEP) vs read-write (DW) |
| Connection Fundamentals | [SQLDW-CONSUMPTION-CORE.md § Connection Fundamentals](../../common/SQLDW-CONSUMPTION-CORE.md#connection-fundamentals) | TDS, port 1433, Entra-only, no MARS |
| Supported T-SQL Surface Area (Consumption Focus) | [SQLDW-CONSUMPTION-CORE.md § Supported T-SQL Surface Area](../../common/SQLDW-CONSUMPTION-CORE.md#supported-t-sql-surface-area-consumption-focus) | **Read before writing T-SQL** — includes data types (no `nvarchar`/`datetime`/`money`) |
| Read-Side Objects You Can Create | [SQLDW-CONSUMPTION-CORE.md § Read-Side Objects You Can Create](../../common/SQLDW-CONSUMPTION-CORE.md#read-side-objects-you-can-create) | Views, TVFs, scalar UDFs, procedures |
| Temporary Tables | [SQLDW-CONSUMPTION-CORE.md § Temporary Tables](../../common/SQLDW-CONSUMPTION-CORE.md#temporary-tables) | Use `DISTRIBUTION = ROUND_ROBIN` for INSERT INTO SELECT support |
| Cross-Database Queries | [SQLDW-CONSUMPTION-CORE.md § Cross-Database Queries](../../common/SQLDW-CONSUMPTION-CORE.md#cross-database-queries) | 3-part naming, same workspace |
| Security for Consumption | [SQLDW-CONSUMPTION-CORE.md § Security for Consumption](../../common/SQLDW-CONSUMPTION-CORE.md#security-for-consumption) | GRANT/DENY, RLS, CLS, DDM |
| Monitoring and Diagnostics | [SQLDW-CONSUMPTION-CORE.md § Monitoring and Diagnostics](../../common/SQLDW-CONSUMPTION-CORE.md#monitoring-and-diagnostics) | Includes query labels; DMVs (live) + `queryinsights.*` (30-day history) |
| Performance: Best Practices and Troubleshooting | [SQLDW-CONSUMPTION-CORE.md § Performance: Best Practices and Troubleshooting](../../common/SQLDW-CONSUMPTION-CORE.md#performance-best-practices-and-troubleshooting) | Statistics, caching, clustering, query tips |
| REST API: Refresh SQL Endpoint Metadata | [SQLDW-CONSUMPTION-CORE.md § REST API: Refresh SQL Endpoint Metadata](../../common/SQLDW-CONSUMPTION-CORE.md#rest-api-refresh-sql-endpoint-metadata) | Force metadata sync when SQLEP data is stale after ETL |
| System Catalog Queries (Metadata Exploration) | [SQLDW-CONSUMPTION-CORE.md § System Catalog Queries](../../common/SQLDW-CONSUMPTION-CORE.md#system-catalog-queries-metadata-exploration) | `sys.tables`, `sys.columns`, `sys.views`, `sys.stats` |
| Common Consumption Patterns (End-to-End Examples) | [SQLDW-CONSUMPTION-CORE.md § Common Consumption Patterns](../../common/SQLDW-CONSUMPTION-CORE.md#common-consumption-patterns-end-to-end-examples) | Reporting views, cross-DB analytics, temp table staging |
| Gotchas and Troubleshooting Reference | [SQLDW-CONSUMPTION-CORE.md § Gotchas and Troubleshooting Reference](../../common/SQLDW-CONSUMPTION-CORE.md#gotchas-and-troubleshooting-reference) | 18 numbered issues with cause + resolution |
| Quick Reference: Consumption Capabilities by Scenario | [SQLDW-CONSUMPTION-CORE.md § Quick Reference: Consumption Capabilities](../../common/SQLDW-CONSUMPTION-CORE.md#quick-reference-consumption-capabilities-by-scenario) | Scenario → approach lookup |
| Schema and Object Discovery | [discovery-queries.md § Schema and Object Discovery](references/discovery-queries.md#schema-and-object-discovery) | Tables, columns, views, functions, procedures, cross-DB |
| Security Discovery | [discovery-queries.md § Security Discovery](references/discovery-queries.md#security-discovery) ||
| Statistics and Performance Metadata | [discovery-queries.md § Statistics and Performance Metadata](references/discovery-queries.md#statistics-and-performance-metadata) ||
| Bash — Data Export | [script-templates.md § Bash — Data Export](references/script-templates.md#bash--data-export) | Query to CSV + parameterized date range export |
| Bash — Schema Discovery Report | [script-templates.md § Bash — Schema Discovery Report](references/script-templates.md#bash--schema-discovery-report) ||
| Bash — Performance Investigation | [script-templates.md § Bash — Performance Investigation](references/script-templates.md#bash--performance-investigation) ||
| PowerShell Templates | [script-templates.md § PowerShell Templates](references/script-templates.md#powershell-templates) | Query to CSV + schema discovery |
| Tool Stack | [SKILL.md § Tool Stack](#tool-stack) ||
| Connection | [SKILL.md § Connection](#connection) ||
| Agentic Exploration ("Chat With My Data") | [SKILL.md § Agentic Exploration](#agentic-exploration-chat-with-my-data) | **Start here** for data exploration |
| Script Generation | [consumption-cli-quickref.md § Script Generation](references/consumption-cli-quickref.md#script-generation) | Formatting flags, piped input, parameterized queries |
| Monitoring and Performance | [consumption-cli-quickref.md § Monitoring and Performance](references/consumption-cli-quickref.md#monitoring-and-performance) | Active queries DMV, KILL syntax |
| Gotchas, Rules, Troubleshooting | [SKILL.md § Gotchas, Rules, Troubleshooting](#gotchas-rules-troubleshooting) | **MUST DO / AVOID / PREFER** checklists |
| Agent Integration Notes | [consumption-cli-quickref.md § Agent Integration Notes](references/consumption-cli-quickref.md#agent-integration-notes) | Per-agent CLI tips |

---

## Tool Stack

| Tool | Role | Install |
|---|---|---|
| `sqlcmd` (Go) | **Primary**: Execute T-SQL. Standalone binary, no ODBC driver, built-in Entra ID auth via `DefaultAzureCredential`. | `winget install sqlcmd` / `brew install sqlcmd` / `apt-get install sqlcmd` |
| `az` CLI | Auth (`az login`), token acquisition, Fabric REST for endpoint discovery. | Pre-installed in most dev environments |
| `jq` | Parse JSON from `az rest` | Pre-installed or trivial |

> **Agent check** — verify before first SQL operation:
> ```bash
> sqlcmd --version 2>/dev/null || echo "INSTALL: winget install sqlcmd OR brew install sqlcmd"
> ```

---

## Connection

### Discover the SQL Endpoint FQDN

Per [COMMON-CLI.md](../../common/COMMON-CLI.md) Discovering Connection Parameters via REST:

```bash
WS_ID="<workspaceId>"
ITEM_ID="<warehouseOrLakehouseId>"

# Warehouse
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/warehouses/$ITEM_ID" \
  --query "properties.connectionString" --output tsv

# Lakehouse SQL endpoint
az rest --method get \
  --resource "https://api.fabric.microsoft.com" \
  --url "https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/lakehouses/$ITEM_ID" \
  --query "properties.sqlEndpointProperties.connectionString" --output tsv
```

Result: `<uniqueId>.datawarehouse.fabric.microsoft.com`

### Connect with sqlcmd (Go)

```bash
# Interactive session (Entra login via browser if needed)
sqlcmd -S "<endpoint>.datawarehouse.fabric.microsoft.com" -d "<DatabaseName>" -G

# Non-interactive one-shot query
sqlcmd -S "<endpoint>.datawarehouse.fabric.microsoft.com" -d "<DatabaseName>" -G \
  -Q "SELECT TOP 10 * FROM dbo.FactSales"

# Explicit ActiveDirectoryDefault (uses az login session)
sqlcmd -S "<endpoint>.datawarehouse.fabric.microsoft.com" -d "<DatabaseName>" \
  --authentication-method ActiveDirectoryDefault \
  -Q "SELECT TOP 10 * FROM dbo.FactSales"

# Service principal (CI/CD)
SQLCMDPASSWORD="<clientSecret>" \
sqlcmd -S "<endpoint>.datawarehouse.fabric.microsoft.com" -d "<DatabaseName>" \
  --authentication-method ActiveDirectoryServicePrincipal \
  -U "<appId>" \
  -Q "SELECT COUNT(*) FROM dbo.FactSales"
```

### Reusable Connection Variables

```bash
# Set once at script top
FABRIC_SERVER="<endpoint>.datawarehouse.fabric.microsoft.com"
FABRIC_DB="<DatabaseName>"
SQLCMD="sqlcmd -S $FABRIC_SERVER -d $FABRIC_DB -G"

# Use throughout
$SQLCMD -Q "SELECT TOP 5 * FROM dbo.DimProduct"
$SQLCMD -i myscript.sql
```

### PowerShell / Windows CMD

```powershell
# PowerShell
$s = "<endpoint>.datawarehouse.fabric.microsoft.com"; $db = "<DatabaseName>"
sqlcmd -S $s -d $db -G -Q "SELECT TOP 10 * FROM dbo.FactSales"
# CMD: use set S=... and %S% / %DB% instead of $variables
```

---

## Agentic Exploration ("Chat With My Data")

### Schema Discovery Sequence

Run these in order to understand what's in the endpoint. See [references/discovery-queries.md](references/discovery-queries.md) for extended discovery queries.

```bash
# 1. List schemas
$SQLCMD -Q "SELECT schema_name FROM information_schema.schemata ORDER BY schema_name" -W

# 2. List tables and views
$SQLCMD -Q "SELECT table_schema, table_name, table_type FROM information_schema.tables ORDER BY table_schema, table_name" -W

# 3. Columns for a table
$SQLCMD -Q "SELECT column_name, data_type, character_maximum_length, is_nullable FROM information_schema.columns WHERE table_schema='dbo' AND table_name='FactSales' ORDER BY ordinal_position" -W

# 4. Preview rows
$SQLCMD -Q "SELECT TOP 5 * FROM dbo.FactSales" -W

# 5. Row counts
$SQLCMD -Q "SELECT s.name AS [schema], t.name AS [table], SUM(p.rows) AS row_count FROM sys.tables t JOIN sys.schemas s ON t.schema_id=s.schema_id JOIN sys.partitions p ON t.object_id=p.object_id AND p.index_id IN (0,1) GROUP BY s.name, t.name ORDER BY row_count DESC" -W

# 6. Programmability objects (views, functions, procedures)
$SQLCMD -Q "SELECT name, type_desc FROM sys.objects WHERE type IN ('V','FN','IF','P','TF') ORDER BY type_desc, name" -W
```

### Agentic Workflow

1. **Discover** → Run Steps 1–3 to understand available tables/columns.
2. **Sample** → `SELECT TOP 5` on relevant tables.
3. **Formulate** → Write T-SQL using [SQLDW-CONSUMPTION-CORE.md](../../common/SQLDW-CONSUMPTION-CORE.md) Supported T-SQL Surface Area.
4. **Execute** → `$SQLCMD -Q "..."`.
5. **Iterate** → Refine based on results.
6. **Present** → Show results or generate a reusable script (Script Generation section).

---

## Gotchas, Rules, Troubleshooting

For full T-SQL/platform gotchas: [SQLDW-CONSUMPTION-CORE.md](../../common/SQLDW-CONSUMPTION-CORE.md) Gotchas and Troubleshooting Reference and [COMMON-CLI.md](../../common/COMMON-CLI.md) Gotchas & Troubleshooting (CLI-Specific).

### MUST DO

- **Always `-d <DatabaseName>`** — FQDN alone is insufficient.
- **Always `-G` or `--authentication-method`** — SQL auth not supported on Fabric.
- **`az login` first** — `ActiveDirectoryDefault` uses az session. No session → cryptic failure.
- **`SET NOCOUNT ON;`** in scripts — suppresses row-count messages that corrupt output.
- **Label queries** with `OPTION (LABEL = 'AGENTCLI_...')` for Query Insights tracing.

### AVOID

- **ODBC sqlcmd** (`/opt/mssql-tools/bin/sqlcmd`) — requires ODBC driver. Use Go version.
- **Omitting `-W`** in scripts — trailing spaces corrupt CSV.
- **DML on SQLEP** — Lakehouse/Mirrored DB endpoints are read-only. DML only on Warehouse.
- **MARS** — not supported. Remove `MultipleActiveResultSets` from connection strings.
- **Hardcoded FQDNs** — discover via REST API (Discover the SQL Endpoint FQDN).

### PREFER

- **`sqlcmd (Go) -G`** over curl+token for SQL queries.
- **`-Q`** (non-interactive exit) for agentic use.
- **Piped input** for multi-statement batches or queries with quotes.
- **`-i file.sql`** for complex queries — avoids shell escaping.
- **`-F vertical`** for exploration of wide tables.
- **Env vars** (`FABRIC_SERVER`, `FABRIC_DB`) for script reuse.
- **`az rest`** for Fabric REST API — use sqlcmd only for T-SQL.

### TROUBLESHOOTING

| Symptom | Cause | Fix |
|---|---|---|
| `Login failed for user '<token-identified principal>'` | Wrong DB name or no access | Verify `-d` matches item name exactly (case-sensitive) |
| `Cannot open server` | Wrong FQDN or network | Re-discover via REST API; check port 1433 |
| `Login timeout expired` | Port 1433 blocked | `nc -zv <endpoint> 1433`; check firewall/VPN |
| `ActiveDirectoryDefault` failure | `az login` expired or wrong tenant | `az login --tenant <tenantId>` |
| Garbled CSV output | Missing `-W` or wrong `-s` | Add `-W -s"," -w 4000` |
| `(N rows affected)` in file | No `SET NOCOUNT ON` | Prepend `SET NOCOUNT ON;` |
| `Invalid object name 'queryinsights...'` | New warehouse < 2 min old | Wait ~2 minutes |
| No rows but data exists | RLS filtering | Check `USER_NAME()`, verify RLS policies |
| `sqlcmd` not found | Go version not installed | `winget install sqlcmd` / `brew install sqlcmd` |

