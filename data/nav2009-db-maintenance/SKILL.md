---
name: nav2009-db-maintenance
description: SQL Server maintenance for a Microsoft Dynamics NAV 2009 database — back up, integrity-check (DBCC CHECKDB), rebuild or reorganize fragmented indexes, and update statistics. The bundled script plans each action and returns the exact T-SQL it would execute, defaulting to a safe dry run that changes nothing; pass -Execute to actually run it. Critically, the script only REBUILDS/REORGANIZES NAV-owned indexes and NEVER creates or drops them — NAV 2009 owns the physical schema through table Keys and SIFT indexed views, and out-of-band DDL is silently lost on key/company changes. Use when the user says "back up the NAV database", "rebuild fragmented indexes on NAV_PROD", "run a maintenance pass on the NAV SQL database", "update statistics on NAV". Do NOT use for diagnosing WHY something is slow — that is nav2009-sql-performance; this skill executes the fixes. Requires PowerShell 7+ and SQL maintenance permissions (see compatibility).
license: MIT
compatibility: Requires PowerShell 7+ and SQL Server maintenance permissions (db_backupoperator/ALTER/db_owner depending on action)
metadata:
  version: "1.0.3"
---

# NAV 2009 DB Maintenance

> Targets the **SQL Server database behind a Dynamics NAV 2009 install**. The bundled script
> `scripts/Invoke-NavDbMaintenance.ps1` **plans maintenance and (only with `-Execute`) runs it**,
> emitting JSON throughout. **Default mode is a DRY RUN** — the script prints the exact T-SQL it
> would execute and changes nothing without `-Execute`. It only rebuilds/reorganizes and updates
> statistics on existing indexes; it **NEVER creates or drops indexes** (NAV owns them). It never
> calls an LLM.
>
> Before running maintenance, diagnose the state first with **nav2009-sql-performance** (fragmentation,
> stale stats, SIFT sizes). Then plan an action here and confirm the T-SQL before executing.

`SCRIPT` = this skill's `scripts/Invoke-NavDbMaintenance.ps1`. Requires **PowerShell 7+** (`pwsh`)
and network access to the SQL Server.

## Permissions & auth

- Default is **Windows integrated auth** (the user running `pwsh`). Pass `-SqlCredential` for SQL
  auth — it is a `PSCredential`; let PowerShell prompt (`-SqlCredential (Get-Credential)`). Never
  put a password on the command line.
- Required permissions by action:
  - **backup** — `db_backupoperator` (or `db_owner`)
  - **index_maintenance** — `db_owner` or `ALTER` permission on the indexes
  - **checkdb** — `db_owner` or `sysadmin`
  - **statistics** — `db_owner` or `UPDATE STATISTICS` permission
- Connections are unencrypted by default (NAV 2009-era instances rarely have TLS certs); add
  `-Encrypt` if the instance supports it.

## How to run

Always run with `pwsh`. Without `-Execute` the script is a **dry run** — it returns planned T-SQL
in each section's `plan` array and sets `executed: false`.

| Want | Pass |
|------|------|
| **Full maintenance plan (dry run)** | `-ServerInstance SQLSRV01 -Database NAV_PROD` |
| **Just back up** | `-Actions backup` |
| **Just index maintenance** | `-Actions index_maintenance` |
| **Just integrity check** | `-Actions checkdb` |
| **Just update statistics** | `-Actions statistics` |
| **Change fragmentation thresholds** | `-ReorganizeThreshold 15 -RebuildThreshold 25` |
| **ONLINE rebuild (Enterprise only)** | `-Online` |
| **Actually execute** | add `-Execute` |
| **SQL auth** | `-SqlCredential (Get-Credential)` |
| **Save report** | `-OutFile C:\ops\maint-report.json` |

```powershell
# Dry run — see the full maintenance plan before committing
pwsh -File SCRIPT -ServerInstance SQLSRV01 -Database 'NAV_PROD'

# Execute a backup only (use a maintenance window for index rebuild / CHECKDB)
pwsh -File SCRIPT -ServerInstance SQLSRV01 -Database 'NAV_PROD' `
    -Actions backup -BackupPath 'D:\Backups\NAV_PROD.bak' -Execute
```

## Output contract

- **Without `-OutFile`** → full JSON on stdout.
- **With `-OutFile`** → full JSON to the file; a **compact** summary (per-section status) on
  stdout. Prefer `-OutFile` for large runs so your context stays small; then read only the
  sections you need.

Top level: `status` (`ok` / `partial` / `error`), `generated_at` (UTC ISO-8601), `executed` (bool),
and `sections` keyed by action name. Each section:

```json
{
  "backup":            { "status": "planned|ok|error|skipped", "plan": ["T-SQL..."], "data": {} },
  "checkdb":           { "status": "planned|ok|error|skipped", "plan": ["T-SQL..."], "data": {} },
  "index_maintenance": { "status": "planned|ok|error|skipped", "plan": ["ALTER INDEX..."], "data": {} },
  "statistics":        { "status": "planned|ok|error|skipped", "plan": ["EXEC sp_updatestats"], "data": {} }
}
```

In **dry run** (`-Execute` absent): each runnable section has `status: planned` and a `plan` array
of the exact T-SQL statements — no database state is changed. With **`-Execute`**: statements run,
`status` becomes `ok` or `error`, and `data` reports the outcome (backup file size, CHECKDB result,
indexes rebuilt/reorganized, stats updated).

## What you (the agent) do with the result

1. **Dry run first, always.** Run the script without `-Execute`, show the user the planned T-SQL
   from each section, and get explicit confirmation before re-running with `-Execute` — especially
   for CHECKDB and index rebuild on a production DB during business hours.
2. **Recommend a maintenance window.** CHECKDB and index rebuild hold locks and can be I/O-heavy.
   Suggest running outside peak NAV posting hours. CHECKDB on a large DB can run for hours.
3. **After execution**, report what changed: which indexes were rebuilt vs reorganized (table name,
   index name, fragmentation before), backup file path and size, CHECKDB pass/fail with any
   messages.
4. **NEVER suggest creating or dropping indexes.** If fragmentation persists after maintenance it
   is a NAV key or SIFT design issue — point the user to **nav2009-development** (to adjust key
   design) and **nav2009-sql-performance** (to see which SIFT views or indexes are candidates for
   `MaintainSIFTIndex`/`MaintainSQLIndex` off).
5. After execution, remind the user that wait stats and index-usage stats **reset on SQL Server
   restart** — re-triage with **nav2009-sql-performance** afterward to see the new baseline.

## Errors

- **Cannot connect** — wrong instance name, SQL Browser off for named instances, firewall, or
  auth mismatch. Check with `Test-NetConnection <server> -Port 1433`.
- **Permission denied on backup** — the SQL service account must have write access to the backup
  path; the login needs `db_backupoperator` or `db_owner`.
- **ONLINE rebuild unsupported** — `ALTER INDEX ... REBUILD WITH (ONLINE=ON)` needs Enterprise
  edition; on Standard/Web/Express the section will error with "ONLINE is not supported". Remove
  `-Online` and schedule an offline rebuild in a maintenance window.
- **CHECKDB permission denied** — needs `db_owner` or `sysadmin`. The other actions still run
  (each section is independent).
- **Backup path not writable by SQL service account** — the path is resolved on the SQL Server,
  not the client machine. Ensure the SQL Server service account has write access to the UNC/local
  path specified.
