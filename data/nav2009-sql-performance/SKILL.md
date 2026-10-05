---
name: nav2009-sql-performance
description: Diagnose performance problems in Microsoft Dynamics NAV 2009 (Navision) and its SQL Server database. The bundled script collects a read-only DMV snapshot (top queries, waits, blocking, deadlocks, missing/unused indexes, SIFT views, fragmentation, stale stats, config) as JSON; the agent interprets it through a NAV lens — mapping SQL findings back to C/AL anti-patterns, keys, and SIFT design. Use when the user reports NAV/Navision slowness, locking/deadlocks during posting, a slow report/batch job, or wants a SQL Server health check for a NAV 2009 database. Do NOT use to execute maintenance (backup, index rebuild, statistics) — that is nav2009-db-maintenance; this skill is read-only diagnosis. Requires PowerShell 7+ and SQL Server VIEW SERVER STATE permission.
license: MIT
compatibility: Requires PowerShell 7+ and SQL Server VIEW SERVER STATE / VIEW DATABASE STATE permissions
metadata:
  version: "1.0.5"
---

# NAV 2009 SQL Performance Triage

> Targets **SQL Server instances hosting Dynamics NAV 2009 databases**. The bundled script
> `scripts/Invoke-SqlPerfTriage.ps1` collects a **read-only** diagnostic snapshot and emits
> JSON; **the agent (you) writes the analysis.** The script never modifies server or database
> state and never calls an LLM.

`SCRIPT` = this skill's `scripts/Invoke-SqlPerfTriage.ps1`. Requires **PowerShell 7+** (`pwsh`)
and network access to the SQL Server. The full SQL-finding → NAV-action interpretation guide is in
[REFERENCE.md](REFERENCE.md) — read it before writing your analysis.

## Permissions & auth

- Default is **Windows integrated auth** (the user running `pwsh`). Pass `-SqlCredential` for SQL auth —
  it is a `PSCredential`, so let PowerShell prompt (`-SqlCredential (Get-Credential)`); never put a
  password on the command line.
- Needs **VIEW SERVER STATE** on the instance and **VIEW DATABASE STATE** (or `db_owner`) in the NAV
  database. The trace-flag sub-check may need sysadmin and degrades gracefully if denied.
- Connections are unencrypted by default (NAV 2009-era instances rarely have TLS certs); add `-Encrypt`
  if the instance supports it.

## How to run

Always run with `pwsh`. Parse the JSON it prints on stdout.

| Want | Pass |
|------|------|
| **Full snapshot of a NAV DB** | `-ServerInstance SQLSRV01 -Database 'NAV_PROD'` |
| **Named instance** | `-ServerInstance 'SQLSRV01\NAV'` |
| **Server-level only (no DB)** | omit `-Database` (DB-scoped sections report `skipped`) |
| **Only some sections** | `-Sections waits,blocking,deadlocks` |
| **SQL auth** | `-SqlCredential (Get-Credential)` |
| **Bigger/smaller lists** | `-TopN 20` (default) |
| **Slow big DB** | `-QueryTimeout 300` (fragmentation scan is the slow one; or drop it from `-Sections`) |
| **Save full report** | `-OutFile C:\path\triage.json` |

Sections: `server`, `database`, `waits`, `top_queries`, `missing_indexes`, `unused_indexes`,
`blocking`, `deadlocks`, `sift`, `fragmentation`, `stats`, `largest_tables` (default `all`).

**Examples:**
```powershell
# Full triage of a NAV 2009 database
pwsh -File SCRIPT -ServerInstance SQLSRV01 -Database 'Navision_PROD' -OutFile C:\ops\nav-triage.json

# "Users are stuck right now" — live locking picture only
pwsh -File SCRIPT -ServerInstance SQLSRV01 -Database 'Navision_PROD' -Sections blocking,deadlocks,waits
```

## Output contract

- **Without `-OutFile`** → full JSON on stdout.
- **With `-OutFile`** → full JSON to the file; a **compact** summary (per-section status + row counts)
  on stdout. Prefer `-OutFile` for full snapshots so your context stays small; then read only the
  sections you need from the file.

Top level: `status` (`ok` / `partial` / `error`), `generated_at` (UTC), and `sections`, where each
section is `{ status: ok|error|skipped, data|error|reason }`. Timestamps inside `data` are **SQL
Server local time**; deadlock timestamps are UTC. Full schema and per-section notes in
[REFERENCE.md](REFERENCE.md).

## What you (the agent) do with the result

1. **Run the script**, parse the JSON.
2. **Interpret through the NAV lens, not just generic SQL tuning** — use the mapping table in
   [REFERENCE.md](REFERENCE.md). The key NAV 2009 specifics:
   - Top queries full of `FETCH API_CURSOR` / `sp_cursorfetch` are **normal** for the Classic client
     driver — judge them by reads-per-execution, not by their cursor shape.
   - High reads-per-execution usually traces back to C/AL: missing `SETCURRENTKEY` matching the
     filters, `FIND('-')` loops over large tables, or `CALCSUMS`/FlowFields without a supporting
     SIFT key. The fix belongs **in C/AL or NAV key design** more often than in raw SQL indexes.
   - **Never recommend creating/dropping indexes directly in SQL** on a NAV 2009 DB as the first
     option — NAV owns its indexes via table keys (`MaintainSQLIndex`) and SIFT views
     (`MaintainSIFTIndex`); out-of-band SQL indexes are lost when keys/companies change. Say so.
   - Blocking/deadlocks during posting: look at the objects involved (`G/L Entry`, `Item Ledger Entry`,
     dimension tables, `No. Series Line`) — typical fixes are C/AL-side (lock ordering, shorter
     transactions, `MaintainSIFTIndex` off on hot SIFT views), not SQL-side.
3. **Lead with the 2–4 findings that matter**, each as: evidence (numbers from the JSON) → likely
   NAV-level cause → concrete next action. Don't recite every section.
4. **Fail loud on coverage**: name any section with `status: error/skipped` and what that means for
   the analysis (e.g. "deadlocks section unavailable — SQL 2005 has no Extended Events"). Wait stats
   and index usage are **cumulative since instance restart** — state the window
   (`server.system.sqlserver_start_time`) before drawing conclusions from them.
5. For the C/AL side of a finding (which key to add, how to restructure a loop), the
   **nav2009-development** skill holds the coding patterns.

## Errors

- `Cannot connect` → wrong instance name, SQL Browser off for named instances, firewall, or auth.
  Suggest checking with `Test-NetConnection <server> -Port 1433`.
- Section `error: VIEW SERVER STATE permission was denied` → ask for the permission grant; the
  remaining sections still ran.
- `deadlocks` empty/unsupported on SQL Server 2005 → only SQL Profiler / trace flag 1222 can capture
  deadlocks there; offer that as the manual alternative.
