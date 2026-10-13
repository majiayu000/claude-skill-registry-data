---
name: privesc-windows-tokens
description: >
  Windows privilege escalation via token impersonation privileges — SeImpersonate/SeAssignPrimaryToken
  (the Potato family) and related token abuse to SYSTEM. Load with a Windows shell as a service/web
  account, on "SeImpersonate", "whoami /priv", IIS/MSSQL service context, or "got a shell on Windows".
domain: privesc
type: technique
stability: learning
modes: [pentest]
severity: high
mitre: [T1134.001, T1068]
cwe: [CWE-269, CWE-250]
tools: [PrintSpoofer, GodPotato, JuicyPotatoNG]
schema_version: 1
---

# Windows token-impersonation privesc (Potato family)

## When it applies
You have code execution on Windows as a service or web account (IIS `iis apppool`, MSSQL, a service)
that holds **`SeImpersonatePrivilege`** (or `SeAssignPrimaryTokenPrivilege`). These accounts can't
do much directly but can impersonate a token — and coax SYSTEM into handing one over.

## Why it works
`SeImpersonate` lets a process act with any token it can obtain. The "Potato" technique tricks a
SYSTEM service (via a local RPC/named-pipe/COM authentication) into authenticating to an attacker-controlled
pipe; the low-priv process impersonates that SYSTEM token and spawns a process as SYSTEM.

## Method
1. **Confirm the privilege**: `whoami /priv` — look for `SeImpersonatePrivilege` (or `SeAssignPrimaryTokenPrivilege`) **Enabled**.
2. **Pick the right Potato for the OS/build**:
   - **PrintSpoofer** — modern, uses the print spooler named pipe: `PrintSpoofer.exe -i -c cmd`.
   - **GodPotato** — works across Windows 8–11 / Server 2012–2022 via DCOM: `GodPotato -cmd "cmd /c whoami"`.
   - **JuicyPotatoNG** / RoguePotato — where applicable.
3. **Get SYSTEM**: run the tool to spawn a SYSTEM shell or run a command (add a user, drop a beacon).
4. **If no SeImpersonate**: pivot to other Windows vectors — unquoted service paths, weak service
   perms (`PowerUp`/winPEAS), AlwaysInstallElevated, DLL hijacking, autoruns.

## Gotchas
- The right Potato depends on Windows version/patch — if one fails, try GodPotato (widest coverage).
- Print Spooler disabled → PrintSpoofer won't work; use a DCOM-based one.
- Service accounts (IIS/MSSQL) almost always have SeImpersonate — check `whoami /priv` first, always.

## Verify success
A shell/command running as `NT AUTHORITY\SYSTEM` (`whoami` = SYSTEM), from the impersonation.

## References
itm4n PrintSpoofer; GodPotato; "Rotten/Juicy Potato" lineage; winPEAS/PowerUp for the alternatives.
