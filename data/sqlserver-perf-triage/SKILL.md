---
name: sqlserver-perf-triage
description: Diagnose performance problems on ANY Microsoft SQL Server instance or database. The bundled script collects a read-only DMV snapshot (top queries by CPU/reads, wait statistics, live blocking, deadlock graphs, missing/unused indexes, fragmentation, stale statistics, server/database configuration) as JSON; the agent interprets it and proposes next actions. Use when the user reports a slow SQL Server, a slow database/application, blocking or deadlocks, or wants a SQL Server health check — e.g. "why is SQLSRV01 slow", "check the SQL server behind our app", "are there blocking sessions right now". Do NOT use for Dynamics NAV 2009 or AX 2012 databases — use nav2009-sql-performance / ax2012-sql-performance, which add the application-specific interpretation. Requires PowerShell 7+ and VIEW SERVER STATE.
license: MIT
compatibility: Requires PowerShell 7+ and SQL Server VIEW SERVER STATE / VIEW DATABASE STATE permissions
metadata:
  version: "1.0.2"
---

# SQL Server Performance Triage

> Works against **any SQL Server instance** (2005 → current). The bundled script
> `scripts/Invoke-SqlPerfTriage.ps1` collects a **read-only** diagnostic snapshot and emits
> JSON; **the agent (you) writes the analysis.** The script never modifies server or database
> state.

`SCRIPT` = this skill's `scripts/Invoke-SqlPerfTriage.ps1`. Interpretation guide in
[REFERENCE.md](REFERENCE.md). This script is vendored identically in the NAV 2009 and AX 2012
sibling skills — if the target database belongs to one of those applications, prefer the
sibling skill for its application-specific interpretation.

## Permissions & auth

- Default is **Windows integrated auth**. Pass `-SqlCredential (Get-Credential)` for SQL auth —
  never put a password on the command line.
- Needs **VIEW SERVER STATE** on the instance and **VIEW DATABASE STATE** (or `db_owner`) in the
  target database. The trace-flag sub-check may need sysadmin and degrades gracefully.
- Connections are unencrypted by default; add `-Encrypt` if the instance has a valid certificate.

## How to run

Always run with `pwsh`. Parse the JSON it prints on stdout.

| Want | Pass |
|------|------|
| **Full snapshot of a DB** | `-ServerInstance SQLSRV01 -Database 'AppDB'` |
| **Named instance** | `-ServerInstance 'SQLSRV01\INST01'` |
| **Server-level only (no DB)** | omit `-Database` (DB-scoped sections report `skipped`) |
| **Only some sections** | `-Sections waits,blocking,deadlocks` |
| **SQL auth** | `-SqlCredential (Get-Credential)` |
| **Slow big DB** | `-QueryTimeout 300` (fragmentation scan is the slow one; or drop it from `-Sections`) |
| **Save full report** | `-OutFile C:\path\triage.json` |

Sections: `server`, `database`, `waits`, `top_queries`, `missing_indexes`, `unused_indexes`,
`blocking`, `deadlocks`, `sift`, `fragmentation`, `stats`, `largest_tables` (default `all`).
The `sift` section is NAV-specific and harmlessly reports 0 views on non-NAV databases.

**Examples:**
```powershell
# Full triage of one database
pwsh -File SCRIPT -ServerInstance SQLSRV01 -Database 'AppDB' -OutFile C:\ops\triage.json

# "The server is slow right now" — live picture only
pwsh -File SCRIPT -ServerInstance SQLSRV01 -Sections waits,blocking,deadlocks,top_queries
```

## Output contract

- **Without `-OutFile`** → full JSON on stdout.
- **With `-OutFile`** → full JSON to the file; a compact summary (per-section status + row
  counts) on stdout. Prefer `-OutFile` for full snapshots; read back only what you need.

Top level: `status` (`ok`/`partial`/`error`) and `sections`, each
`{ status: ok|error|skipped, data|error|reason }`. Timestamps in `data` are SQL Server local
time; deadlock timestamps are UTC. Full schema in [REFERENCE.md](REFERENCE.md).

## What you (the agent) do with the result

1. **Run the script**, parse the JSON.
2. **Triage in this order**: live blocking → deadlocks → waits (what is the server actually
   waiting on?) → top queries (who causes it?) → indexes/stats/config (why?). Use the
   interpretation table in [REFERENCE.md](REFERENCE.md).
3. **Lead with the 2–4 findings that matter**, each as: evidence (numbers) → likely cause →
   concrete next action. Don't recite every section.
4. **Fail loud on coverage**: name any `error`/`skipped` section. Wait stats and index usage
   are **cumulative since instance restart** — state the window
   (`server.system.sqlserver_start_time`) before drawing conclusions.
5. **Before recommending index changes**, ask whether an application owns the schema (ERP
   systems like Dynamics NAV/AX drop out-of-band indexes on synchronization) — if yes, switch
   to the application-specific sibling skill.

## Errors

- `Cannot connect` → wrong instance name, SQL Browser off for named instances, firewall, auth.
  Check with `Test-NetConnection <server> -Port 1433`.
- Section `error: VIEW SERVER STATE permission was denied` → request the grant; other sections
  still ran.
- `deadlocks` unsupported on SQL Server 2005 (no Extended Events) — offer trace flag 1222 as
  the manual alternative.
