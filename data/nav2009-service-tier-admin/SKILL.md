---
name: nav2009-service-tier-admin
description: Inventory and administer Microsoft Dynamics NAV 2009 Service Tiers (NST / NAV Server) and NAS/Job Queue on Windows. The bundled script enumerates every MicrosoftDynamicsNavServer* Windows service (status, start mode, service account, executable path) and parses CustomSettings.config to surface the database target, client/SOAP/management ports, credential type, and NAS startup codeunit. Output is structured JSON; the agent writes the narrative. Use when the user says "list the NAV service tiers on this server", "what database is this NAV instance pointing at", "is the Job Queue NAS configured", "restart the NAV service tier", "which port is the RTC client using", or wants a health check of all NST instances. Inventory is read-only; restart is explicit opt-in (-Restart with -Instance) and disconnects active RTC clients. Local machine by default; remote inventory via -ComputerName (CIM/WinRM + admin).
license: MIT
compatibility: Requires PowerShell 7+; local admin on the NST host, or CIM/WinRM admin access for remote inventory
metadata:
  version: "1.0.3"
---

# NAV 2009 Service Tier Admin

> Targets **Microsoft Dynamics NAV 2009 (incl. R2) Service Tiers** (NST = NAV Server) and
> **NAS (NAV Application Server / Job Queue)** running as Windows services. The bundled script
> `scripts/Get-NavServiceTier.ps1` enumerates services, parses **CustomSettings.config**, and
> emits JSON; **the agent (you) writes the narrative.** Inventory is **read-only**; the
> `-Restart` action stops/starts a service in the correct order and is **opt-in** — always
> confirm with the user before using it. The script never calls an LLM.

`SCRIPT` = this skill's `scripts/Get-NavServiceTier.ps1`. Requires **PowerShell 7+** (`pwsh`).
Reads the local machine by default; use `-ComputerName` for remote targets (requires admin +
WinRM/CIM access on the target). Full parameter and schema reference in
[REFERENCE.md](REFERENCE.md).

## Permissions & auth

- **Local inventory**: any account with rights to query Win32_Service (typically local admin).
  Reading CustomSettings.config in `Program Files\Microsoft Dynamics NAV\...\Service` usually
  requires local admin or membership in the local Administrators group.
- **Remote inventory** (`-ComputerName`): needs CIM/WinRM connectivity (`Test-WSMan` or
  `winrm quickconfig` on the target) and an account with admin rights on the target machine.
- **Restart**: local admin (or `SeServiceLogonRight`-equivalent) on the machine hosting the
  service. For remote restart the same WinRM/admin requirements apply.
- If the Service folder belongs to a different account (e.g. MSA), the config file may not be
  readable; the instance will surface an `error` field rather than aborting the whole inventory.

## How to run

Always run with `pwsh`. Parse the JSON it prints on stdout.

| Want | Pass |
|------|------|
| **Inventory all instances on this server** | _(no extra params)_ |
| **Inventory a named instance** | `-Instance NAVPROD` |
| **Inventory a remote server** | `-ComputerName NAVSRV01` |
| **Include every config key, not just curated ones** | `-IncludeFullConfig` |
| **Restart a named instance (opt-in)** | `-Instance NAVPROD -Restart` |
| **Save full JSON to file** | `-OutFile C:\ops\nav-tiers.json` |

```powershell
# Full inventory of all NAV service tiers on the local machine
pwsh -File SCRIPT -OutFile C:\ops\nav-tiers.json

# Check what database a specific instance is pointing at
pwsh -File SCRIPT -Instance NAVPROD

# Inventory all instances on a remote server
pwsh -File SCRIPT -ComputerName NAVSRV01 -OutFile C:\ops\navsrv01-tiers.json

# Restart the NAVTEST instance (confirm with user first — disconnects all clients)
pwsh -File SCRIPT -Instance NAVTEST -Restart
```

## Output contract

- **Without `-OutFile`** → full JSON on stdout.
- **With `-OutFile`** → full JSON to the file; a compact summary (instance names + status) on
  stdout. Prefer `-OutFile` for multi-instance inventories so context stays small.

Top level: `status` (`ok` / `partial` / `error`), `generated_at` (UTC ISO-8601), `computer`,
and `instances` — one entry per discovered service:

```json
{
  "status": "ok",
  "generated_at": "2026-06-10T09:00:00.0000000Z",
  "computer": "NAVSRV01",
  "instances": [
    {
      "serviceName":  "MicrosoftDynamicsNavServer$NAVPROD",
      "instanceName": "NAVPROD",
      "status":       "Running",
      "startMode":    "Auto",
      "account":      "DOMAIN\\svc-nav",
      "exePath":      "C:\\Program Files\\Microsoft Dynamics NAV\\60\\Service\\Microsoft.Dynamics.Nav.Server.exe",
      "configPath":   "C:\\Program Files\\Microsoft Dynamics NAV\\60\\Service\\Instances\\NAVPROD\\CustomSettings.config",
      "settings": {
        "DatabaseServer":               "SQLSRV01",
        "DatabaseInstance":             "",
        "DatabaseName":                 "Navision_PROD",
        "ServerInstance":               "NAVPROD",
        "ClientServicesPort":           "7046",
        "SOAPServicesPort":             "7047",
        "ManagementServicesPort":       "7045",
        "ClientServicesCredentialType": "Windows",
        "SOAPServicesEnabled":          "true",
        "ServicesCertificateThumbprint": ""
      },
      "nas": {
        "codeunit": "450",
        "method":   "JOBQUEUE",
        "argument": "",
        "enabled":  true
      },
      "ports": {
        "client":     7046,
        "soap":       7047,
        "management": 7045
      },
      "error": null
    }
  ]
}
```

When `-Restart` is passed the top level also contains:

```json
"restart": {
  "requested": "2026-06-10T09:05:00.0000000Z",
  "instance":  "NAVPROD",
  "before":    "Running",
  "after":     "Running",
  "ok":        true
}
```

`status` is `partial` when at least one instance has a non-null `error` field. With `-OutFile`,
stdout instead carries a compact object: `{ status, out_file, instances: [{ instanceName, status }] }`.

## What you (the agent) do with the result

1. **Run the script**, parse the JSON.
2. **Report each instance**: name, running/stopped, service account, DB target
   (`settings.DatabaseServer` + `settings.DatabaseName`), and the three ports.
3. **Flag a Stopped instance** — ask whether it should be running and offer to restart (with the
   user's explicit consent, using `-Restart`).
4. **Flag NAS configured but service stopped**: if `nas.enabled = true` and `status != Running`,
   the Job Queue is not processing — this is usually urgent.
5. **"Users can't connect"**: cross-check `status = Running`, `ClientServicesPort` (must match
   what the client profile has), and `ClientServicesCredentialType`. If status and port look
   correct, the issue may be network/firewall or Kerberos/SPN — point to
   **nav2009-troubleshooting** for the next step.
6. **Before restarting**: confirm with the user ("this will disconnect all active RTC clients on
   NAVPROD — proceed?") then run with `-Restart`. Verify `restart.after.status = Running` and
   `restart.ok = true` in the output.
7. **For the database this instance points at**: the **nav2009-sql-performance** skill can triage
   that SQL Server instance using the `DatabaseServer` and `DatabaseName` values from the output.

## Errors

- **No NAV services found**: service-name pattern is `MicrosoftDynamicsNavServer*`; single-instance
  NAV 2009 SP1 may be exactly `MicrosoftDynamicsNavServer` (no `$` suffix). Default config path:
  `C:\Program Files\Microsoft Dynamics NAV\60\Service\CustomSettings.config`.
- **CustomSettings.config not found or unparseable**: the instance entry will have an `error` field
  with the message; `settings`, `nas`, and `ports` will be `null`. Suggest locating the config
  manually in the Service folder next to the NAV Server executable.
- **Remote CIM access denied**: check WinRM is enabled on the target (`winrm quickconfig`) and
  that the running account has admin rights there.
- **Restart timed out**: the `-RestartTimeoutSec` (default 60) elapsed before the service reached
  `Running`; `restart.ok` will be `false` and `restart.after` will show the actual state. Check
  Windows Event Log on the target for service start failures.
