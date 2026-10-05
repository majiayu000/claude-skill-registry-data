---
name: rds-profile-triage
description: Read-only triage of Remote Desktop Services (RDS) session-host profile & WinRM-host health across one or many servers. The bundled script collects (over WinRM, with a CIM-over-DCOM fallback for hosts whose WinRM host process won't even launch) profile-hive leaks, temp-profile sprawl, ProfileList corruption, the roaming-profile path read RAW, drain state, and User-Profiles-Service failures grouped BY THE ACTUAL USER, then renders a uniform deterministic report the agent relays (JSON optional). Use when a user reports RDS/terminal-server problems like "user gets logged out immediately / logged off right after sign-in", "everyone's getting temporary profiles", "settings don't save on the RDS farm", "the session host won't accept logins", or "can't PowerShell-remote into the RDS server (could not launch a host process)". Do NOT use for generic event-log sweeps (use win-eventlog-triage) or SQL Server issues (sqlserver-perf-triage). Requires PowerShell 7+ and a tier-admin credential (prompted).
license: MIT
compatibility: Requires PowerShell 7+ on the operator machine. WinRM mode needs PowerShell Remoting on the target RDS hosts; DCOM mode needs WMI/DCOM (TCP 135 + dynamic range) reachable. Read-only — makes no changes.
metadata:
  version: "1.0.1"
---

# RDS Profile & WinRM-Host Triage

> Targets **Windows RDS session hosts** over **WinRM** (with a **CIM-over-DCOM** fallback). The bundled `scripts/Invoke-RdsProfileTriage.ps1` collects read-only health data, computes deterministic severity-ranked `findings`, and **renders a uniform triage report itself** — so the output is identical every run and the agent just relays it (and decides remediation). The script never calls an LLM and **changes nothing**.

`SCRIPT` = this skill's `scripts/Invoke-RdsProfileTriage.ps1`. It **requires PowerShell 7+** (`pwsh`).

## Why this skill exists (the gotchas it encodes)

RDS profile triage is a minefield of measurement traps that produce confident-but-wrong root causes. This skill bakes the corrections in — **read the `caveats` array in the output before concluding anything**, and see [REFERENCE.md](REFERENCE.md#gotchas--read-before-you-conclude) for the full list. The big four:

1. **REG_EXPAND_SZ expansion.** Reading the roaming-profile path with `Get-ItemProperty` **expands `%USERNAME%` in the calling account's context**. Read as admin, a perfectly correct `\\FS01\profiles$\%USERNAME%\...` looks **hardcoded to the admin** — a classic false "the GPO is broken" call. The script reads it **raw**; trust `roaming_profile.machine_profile_path_raw`.
2. **Double-hop.** From a **non-domain-joined / workgroup** operator box, WinRM uses NTLM and the host can't delegate to the file server → roaming load fails with **"Access is denied"** — *for your connecting account only*. Those Event 1521s are **your artifact**, not a user outage. The script tags them `user_class=self_or_admin`.
3. **One noisy account ≠ the whole farm.** A single backup/batch service account can mint thousands of temp profiles. The script groups profile-failure events **by the real user** so you don't generalize one service account's churn into a farm-wide outage.
4. **The "Element not found" chain.** Corrupt `ProfileList` entries (empty `ProfileImagePath`, `.bak` pointing at deleted temp dirs) → the user profile can't be built → `wsmprovhost` never registers its COM class → **WinRM "could not launch a host process" (Event 86) + DCOM 10000 "error 0"**. So *a broken WinRM endpoint can be a profile problem.* The script detects the corruption and the host-launch events together.

## How to run

Always run with `pwsh`. The script prompts for the tier-admin credential (reused for all hosts, never stored). Parse the JSON on stdout.

| Want | Pass |
|------|------|
| **One host** | `-ComputerName RDS01` |
| **A farm** | `-ComputerName RDS01,RDS02` or `-ServerListFile C:\ops\rds.txt` |
| **Time window for events** | `-Hours 24` (default) · `-Since '2026-06-15T00:00'` · `-From <dt> -To <dt>` |
| **WinRM host won't launch on a box** | `-Protocol Dcom` (reduced CIM/DCOM collection: uptime, drain, roaming-raw, ProfileList corruption) |
| **Output shape** | `-Format text` (default — uniform human report) · `-Format json` · `-Format both` |
| **Save full JSON** | `-OutFile C:\ops\rds.json` (full detail to file; stdout still follows `-Format`) |
| **Auth/transport** | `-Authentication Negotiate\|Kerberos\|CredSSP` (default `Default`) |
| **Tuning** | `-TempSampleSize 10` · `-MaxCorruptListed 20` · `-MaxMessageLength 400` |

```powershell
# Single host, last 24h
pwsh -File SCRIPT -ComputerName RDS01

# Two-host farm, 48h window, full detail to a file
pwsh -File SCRIPT -ComputerName RDS01,RDS02 -Hours 48 -OutFile C:\ops\rds.json

# The host's own WinRM is dead ("could not launch a host process") — go in over DCOM
pwsh -File SCRIPT -ComputerName RDS01 -Protocol Dcom
```

## Output contract

The script does the formatting so every run looks the same — **the agent does not re-summarize.**

- **`-Format text`** (default) → a deterministic, uniform plain-text report on stdout, with fixed sections: header, `== FINDINGS (ranked) ==`, `== PER-HOST ==`, `== COVERAGE GAPS ==`, `== CAVEATS ==`. This is the output you relay.
- **`-Format json`** → full JSON (or, with `-OutFile`, a compact summary on stdout + full detail in the file).
- **`-Format both`** → the text report, then `--- JSON ---`, then the JSON.
- **`-OutFile`** always writes the full-detail JSON to the file, whatever `-Format` is.

JSON key fields (for `-Format json`/digging): `summary.findings`, `summary.failures` (each with a `hint`), per host `roaming_profile.machine_profile_path_raw`, `hive_leak`, `temp_profiles`, `profilelist`, `profile_events` (grouped by user + `user_class`), `winrm_host_launch`, and the top-level `caveats`. Full schema in [REFERENCE.md](REFERENCE.md#output-schema).

## What you (the agent) do with the result

Keep it minimal — the report is already uniform and complete:

1. **Run the script** (default `-Format text`) and **relay the report as-is.** Do not reformat, re-rank, or re-summarize it — that's the script's job and the whole point of consistent output. At most add a one-line lead.
2. **Act on the one piece of judgement the script can't:** if a host shows `FAILED - ... could not launch a host process`, **re-run that host with `-Protocol Dcom`** (the report's `hint` says so) and relay the second report.
3. **Honor the `== CAVEATS ==` section** when the user asks "so what's the cause" — they are the guardrails (self_or_admin = your double-hop, service_account churn ≠ farm outage, RAW roaming path, the Element-not-found chain). Don't contradict them.
4. **Propose remediation only on request** (reboot to clear leaked hives, back-up-then-remove corrupt ProfileList entries, clean temp sprawl, exclude service accounts from roaming) — and confirm before changing anything. This skill itself changes nothing.

## Errors

- `Get-Credential` cancelled → re-run and supply the tier-admin credential.
- **"could not launch a host process"** on a host → its WinRM endpoint is down (often ProfileList corruption). Re-run that host with `-Protocol Dcom`; check `profilelist` in the result.
- **Workgroup / cross-domain** (`TrustedHosts` message or `0x80090311`) → run from a domain-joined admin host, or add the FQDNs to WinRM `TrustedHosts` (scope to specific hosts, not `*`), or use `-Protocol Dcom`. See [REFERENCE.md](REFERENCE.md#non-domain-joined--workgroup-operator).
- `pwsh` not found → install PowerShell 7 (`winget install Microsoft.PowerShell`); the repo installer auto-installs it.
