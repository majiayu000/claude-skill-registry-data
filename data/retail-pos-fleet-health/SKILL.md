---
name: retail-pos-fleet-health
description: Health sweep across a fleet of Windows POS machines (Dynamics AX 2012 R3 Retail POS or similar) — or any Windows server/workstation fleet — over PowerShell Remoting. The bundled script checks each machine in parallel for stopped auto-start services (POS/Retail/SQL by default), local SQL Server instances with per-database sizes (flagging databases approaching the SQL Server Express 10 GB limit), low disk space, and recent Critical/Error event counts, returning ranked warnings as JSON. Use when the user wants to check/sweep/inspect the POS fleet or a set of Windows machines — e.g. "check all the POS machines", "which tills have problems", "is any POS offline database near the Express limit", "sweep the store machines for stopped services". Read-only. Requires PowerShell 7+, WinRM on the targets, and an admin credential (always prompted).
license: MIT
compatibility: Requires PowerShell 7+ on the operator machine, WinRM (PowerShell Remoting) enabled on the targets, and a credential with admin rights on them
metadata:
  version: "1.0.2"
---

# Retail POS Fleet Health

> Sweeps **many Windows machines in parallel** over WinRM. The bundled script
> `scripts/Invoke-PosFleetHealth.ps1` collects health signals and emits JSON with
> **deterministically ranked warnings**; **the agent (you) writes the narrative.**
> The script is read-only on the targets — it never starts/stops anything.

`SCRIPT` = this skill's `scripts/Invoke-PosFleetHealth.ps1`.

## Credentials

The script **always prompts** for an admin credential (`Get-Credential`) — held in memory
for the run, reused across all hosts, never written to disk. Do not pass passwords on the
command line. SQL checks run *inside* each remote session against localhost with that
Windows login — no SQL credentials needed.

## How to run

Always run with `pwsh`. Parse the JSON from stdout.

| Want | Pass |
|------|------|
| **A few machines** | `-ComputerName POS001,POS002,POS003` |
| **The whole fleet** | `-ServerListFile C:\ops\pos-hosts.txt` (one host per line, `#` comments OK) |
| **Other services** | `-ServicePattern '*POS*','*Retail*','MSSQL*','MyService*'` |
| **Stricter disk check** | `-DiskMinFreePct 15` |
| **Event window** | `-EventHours 24` (default) |
| **Express limit warn level** | `-ExpressWarnAtPct 80` (default; of `-ExpressLimitGB 10`) |
| **Parallelism** | `-ThrottleLimit 12` (default) |
| **Save full report** | `-OutFile C:\ops\fleet-health.json` (do this for 100 hosts!) |
| **Transport/auth** | `-UseSSL` · `-Authentication Negotiate|Kerberos|CredSSP` |

```powershell
# Full fleet sweep, detail to file, compact summary on stdout
pwsh -File SCRIPT -ServerListFile C:\ops\pos-hosts.txt -OutFile C:\ops\fleet-health.json
```

## Output contract

- **Without `-OutFile`** → full JSON (all hosts) on stdout.
- **With `-OutFile`** → full detail to the file; stdout gets a **compact** summary
  (status, host counts, ranked `warnings`). For big fleets always use `-OutFile`.

`summary.warnings` is ranked: unreachable/auth → stopped services → Express DBs near the
limit → low disk → SQL query failures → high error counts. Each warning has
`computer`, `type`, `detail`. Per-host detail (disks, services, SQL instances + database
sizes, recent error counts) is under `hosts[]`. See [REFERENCE.md](REFERENCE.md).

## What you (the agent) do with the result

1. **Run the script**, parse the JSON.
2. **Lead with `summary.warnings`** — grouped by type, named by machine. A fleet sweep
   answer is "which machines need attention and why", not 100 host reports.
3. **Always surface coverage**: report `hosts_failed` (unreachable/auth) explicitly —
   an unreachable POS may itself be the incident. Never imply full coverage when hosts
   failed.
4. **Express limit warnings are urgent**: a POS offline database hitting the 10 GB
   data-file limit stops syncing/working. Recommend cleanup/shrink or escalation per the
   organization's POS procedure.
5. For deeper SQL diagnosis on a flagged machine, follow up with **sqlserver-perf-triage**
   (or **ax2012-sql-performance** for the channel DB); for event-log detail, use
   **win-eventlog-triage** against that host.

## Errors

- Many `unreachable` hosts → WinRM not enabled on POS images, firewall, or wrong network.
- `auth_failed` → the credential lacks admin rights on the targets.
- `sql_query_failed` on a host → SQL service running but the login has no access; the rest
  of the host's data is still collected.
