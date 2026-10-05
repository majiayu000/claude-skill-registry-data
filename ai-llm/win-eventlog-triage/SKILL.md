---
name: win-eventlog-triage
description: Triage Windows Event Logs across one or many servers. Pulls Critical/Error events (System + Application by default; Security opt-in) over a time window via PowerShell Remoting (WinRM), groups them deterministically, and returns JSON the agent turns into a short, critical-first summary. Use when the user wants to check/triage/investigate Windows server event logs — e.g. "what happened on SRV01 overnight", "triage the event logs on these servers", or "any errors across the file servers in the last 12 hours". Requires PowerShell 7+ and a tier-admin credential (always prompted).
license: MIT
compatibility: Requires PowerShell 7+ on the operator machine and WinRM (PowerShell Remoting) enabled on the target servers
metadata:
  version: "1.2.0"
---

# Windows Event Log Triage

> Targets **Windows servers** over **PowerShell Remoting (WinRM)**. The bundled script `scripts/Invoke-EventLogTriage.ps1` collects + groups events and emits JSON; **the agent (you) writes the triage narrative.** The script never calls an LLM.

`SCRIPT` = this skill's `scripts/Invoke-EventLogTriage.ps1`. It **requires PowerShell 7+** (`pwsh`) and WinRM enabled on the targets.

## Credentials (important)

The script **always prompts** for a tier-admin credential via `Get-Credential` — held in memory for that run only, reused across all servers, never written to disk. The user's normal account does not need server access; the prompted credential authenticates the remoting session. Do **not** try to pass a password on the command line. (A `-Credential` parameter exists only as a testing/automation seam.)

> **Agent/non-interactive runners:** `Get-Credential` needs an interactive console. If you drive this from a tool that runs PowerShell non-interactively (an AI agent's shell, CI, a background job) the prompt cannot render and the run hangs. Launch it in a **visible** window and then read the `-OutFile` — e.g. `Start-Process pwsh -ArgumentList '-NoExit','-File','SCRIPT','-ComputerName','SRV01.contoso.local','-OutFile','C:\ops\triage.json'`. From a **non-domain-joined** client, use the **FQDN** (so it matches a `*.domain` TrustedHosts entry — a short name won't) plus `-Authentication Negotiate`. See REFERENCE.md → *Gotchas*.

## How to run

Always run with `pwsh`. Parse the JSON it prints on stdout.

| Want | Pass |
|------|------|
| **One server** | `-ComputerName SRV01` |
| **Several inline** | `-ComputerName SRV01,SRV02,SRV03` |
| **A list from a file** | `-ServerListFile C:\path\hosts.txt` (one host per line; `#` comments + blank lines ignored) |
| **Time window** | `-Hours 24` (default) · `-Since '2026-06-08T00:00'` · `-From <dt> -To <dt>` |
| **Severity** | default Critical+Error · `-IncludeWarning` · `-Level 1,2,3` |
| **More logs** | default System+Application · `-IncludeSecurity` · `-Logs System,Application,'Microsoft-Windows-...'` |
| **Noise control** | `-SuppressList C:\path\suppress.json` (`{ "eventIds": [..], "providers": [".."] }`) |
| **Save full report** | `-OutFile C:\path\triage.json` |
| **Transport/auth** | `-UseSSL` (HTTPS/5986) · `-Authentication Negotiate\|Kerberos\|CredSSP` (default `Default`) |
| **Tuning** | `-MaxEvents 5000` (cap/log) · `-MaxMessageLength 1000` · `-ThrottleLimit 8` · `-TopCritical 20` |

**Examples** (the user will be prompted for the credential when the script starts):
```powershell
# Single server, last 24h
pwsh -File SCRIPT -ComputerName SRV01

# Server list, last 12h, save full detail to a file
pwsh -File SCRIPT -ServerListFile C:\ops\hosts.txt -Hours 12 -OutFile C:\ops\triage.json

# Include warnings + the Security log for one box
pwsh -File SCRIPT -ComputerName DC01 -IncludeWarning -IncludeSecurity
```

## Output contract

- **Without `-OutFile`** → full JSON (all hosts + groups) on stdout.
- **With `-OutFile`** → full detail JSON to the file; a **compact** JSON (summary + `top_critical`, no per-host groups) on stdout. For big sweeps, prefer `-OutFile` so your context stays small.

Key JSON fields: `status` (ok/partial/error), `summary.top_critical` (deterministically ranked: Critical→Error, then count, then recency), `summary.failures` (per-host problems), and `hosts[].groups` (each group = computer+log+provider+event_id+level with `count`, `first_seen`/`last_seen` in **UTC**, and one truncated `sample_message`). `truncated: true` on a host means the `MaxEvents` cap was hit — coverage was capped, say so. See [REFERENCE.md](REFERENCE.md) for the full schema.

## What you (the agent) do with the result

1. **Run the script**, parse the JSON.
2. **Always give a short, critical-first summary in chat** — even when full detail went to `-OutFile`. Lead with `summary.top_critical`: the most severe / highest-count / most recent issues, named by server + event id + provider, with a one-line plain-English read of likely cause and a suggested next action. Group related events (e.g. a service crash + dependent failures) rather than listing them flat.
3. **Surface coverage gaps loudly** (Karpathy fail-loud): list any host in `summary.failures` (unreachable / auth_failed / error) and any host with `truncated: true`. Never imply full coverage if some servers failed or were capped.
4. **Only dig into `hosts[].groups`** when the user wants detail beyond the top criticals.

## Errors

- `Get-Credential` cancelled → script aborts with a clear message; ask the user to re-run and enter the tier-admin credential.
- Per-host `auth_failed` → the credential lacks rights on that box (or wrong tier), **or** an auth-transport config issue. `unreachable` → WinRM/DNS/firewall. Each failure carries a `hint` field — relay it. These are per-host and do not stop the sweep — report them, continue with the rest.
- **Non-domain-joined client** (error `0x80090311` or a `TrustedHosts` message): Kerberos is unavailable. Run from a domain-joined admin host, or add the targets to WinRM TrustedHosts and retry, or use `-UseSSL`. See [REFERENCE.md](REFERENCE.md#non-domain-joined--cross-domain-clients).
- `pwsh` not found → PowerShell 7 isn't installed; the repo installer auto-installs it, or install manually: `winget install Microsoft.PowerShell`.
