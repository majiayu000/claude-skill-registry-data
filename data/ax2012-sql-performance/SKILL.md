---
name: ax2012-sql-performance
description: Diagnose performance problems in Microsoft Dynamics AX 2012 (incl. R3) and its SQL Server databases — the AX transaction database, the model store, and the Retail channel database. The bundled script collects a read-only DMV snapshot (top queries, waits, blocking, deadlocks, missing/unused indexes, fragmentation, stale stats, config) as JSON; the agent interprets it through an AX lens — known bloat tables (InventSumLogTTS, batch history, database log, AIF logs), AX-specific SQL configuration (RCSI expected ON, TF4136, MAXDOP guidance), AOT-owned indexes, batch server load, and Retail CDX sync health. Use when the user reports AX/Dynamics AX slowness, slow posting or MRP, a slow Retail channel database, batch jobs piling up, or wants a health check of an AX 2012 SQL Server. Do NOT use for generic (non-AX) SQL Servers — that is sqlserver-perf-triage. Requires PowerShell 7+ and VIEW SERVER STATE.
license: MIT
compatibility: Requires PowerShell 7+ and SQL Server VIEW SERVER STATE / VIEW DATABASE STATE permissions
metadata:
  version: "1.0.2"
---

# AX 2012 SQL Performance Triage

> Targets **SQL Server instances hosting Dynamics AX 2012 / R3 databases** — the main AX
> transaction DB, and the Retail **channel database** behind POS. The bundled script
> `scripts/Invoke-SqlPerfTriage.ps1` collects a **read-only** diagnostic snapshot and emits
> JSON; **the agent (you) writes the analysis** using the AX interpretation guide in
> [REFERENCE.md](REFERENCE.md) — read it before writing your analysis.

`SCRIPT` = this skill's `scripts/Invoke-SqlPerfTriage.ps1` (vendored identically in
`sqlserver-perf-triage` and `nav2009-sql-performance`).

## Permissions & auth

- Default is **Windows integrated auth**; `-SqlCredential (Get-Credential)` for SQL auth.
- Needs **VIEW SERVER STATE** + **VIEW DATABASE STATE** (or `db_owner`) in the AX/channel DB.
- Add `-Encrypt` if the instance has a valid certificate.
- **From a non-domain-joined operator (or an agent-driven, non-interactive shell):** integrated
  auth from a workgroup box to a domain SQL instance fails, and a `-SqlCredential`/`Get-Credential`
  prompt can't render non-interactively. Either run the collector **on the SQL host** over a
  visible remoting window — `Start-Process pwsh -ArgumentList '-NoExit','-Command',"Invoke-Command -ComputerName SQL01.contoso.local -Credential (Get-Credential) -Authentication Negotiate -FilePath '<SCRIPT>' -ArgumentList ..."` — connecting to `localhost` inside the session, or pass `-SqlCredential` for SQL auth. Use the **FQDN** so it matches a `*.domain` WinRM TrustedHosts entry.

## How to run

Always run with `pwsh`. Parse the JSON it prints on stdout.

```powershell
# Full triage of the AX transaction database
pwsh -File SCRIPT -ServerInstance SQLSRV01 -Database 'MicrosoftDynamicsAX' -OutFile C:\ops\ax-triage.json

# The Retail channel database
pwsh -File SCRIPT -ServerInstance SQLSRV02 -Database 'RetailChannelDB' -OutFile C:\ops\channel-triage.json

# "AX is frozen right now" — live locking picture only
pwsh -File SCRIPT -ServerInstance SQLSRV01 -Database 'MicrosoftDynamicsAX' -Sections blocking,deadlocks,waits
```

Sections: `server`, `database`, `waits`, `top_queries`, `missing_indexes`, `unused_indexes`,
`blocking`, `deadlocks`, `sift` (NAV-only; reports 0 on AX — ignore), `fragmentation`,
`stats`, `largest_tables` (default `all`). Same parameters and output contract as the
sibling skills: `-OutFile` for big snapshots, `-QueryTimeout 300` for the fragmentation scan
on a large AX DB, `-TopN`, `-Sections`.

## What you (the agent) do with the result

1. **Run the script** against the relevant database (AX transaction DB and/or channel DB),
   parse the JSON.
2. **Interpret through the AX lens** — the mapping table in [REFERENCE.md](REFERENCE.md).
   Headlines:
   - `largest_tables` dominated by **InventSumLogTTS, SysDatabaseLog, BatchJobHistory,
     AifMessageLog, EventInbox** = missing AX cleanup routines, not a SQL problem. Each has
     a standard in-AX cleanup (REFERENCE lists them).
   - **RCSI ON is EXPECTED** for an AX 2012 database (opposite of NAV) — flag it if OFF.
   - **AX owns its indexes via the AOT** — indexes created directly in SQL are dropped on
     database synchronization. Route index changes through the AOT; raw SQL indexes only as
     documented stopgaps.
   - Trace flag **4136** (disable parameter sniffing) is commonly recommended for AX 2012
     workloads — note its presence/absence.
   - Channel DB findings usually trace to **CDX sync backlog** or unpurged retail
     transactions — check sync job health on the AX (HQ) side, not just SQL.
3. **Lead with the 2–4 findings that matter**: evidence → likely AX-level cause → concrete
   next action (which AX cleanup/configuration, which AOT change, which batch reschedule).
4. **Fail loud on coverage**: name `error`/`skipped` sections; state the counter window
   (`server.system.sqlserver_start_time`) before trusting cumulative stats.

## Errors

Same as the sibling skills: `Cannot connect` → instance name/SQL Browser/firewall/auth;
permission-denied sections → request VIEW SERVER STATE; `deadlocks` needs SQL 2008+.
