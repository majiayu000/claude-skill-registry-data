---
name: ad-dacl-abuse
description: >
  Abuse Active Directory object ACLs/DACLs for lateral movement and escalation — GenericAll,
  WriteDACL, GenericWrite, WriteOwner, AddMember, ForceChangePassword, and DCSync rights. Load with
  domain creds + BloodHound showing an ACL edge, on "GenericAll", "WriteDACL", "DCSync", "abuse this edge".
domain: ad
type: technique
stability: learning
modes: [pentest]
severity: high
mitre: [T1222, T1098, T1003.006]
cwe: [CWE-284, CWE-269]
tools: [bloodhound, netexec, impacket, powerview]
schema_version: 1
---

# AD ACL / DACL abuse

## When it applies
You have domain creds and BloodHound shows your principal (or one you control) has a dangerous
**ACL edge** over another object — a user, group, computer, GPO, or the domain. These edges chain
into a path to Domain Admin without any CVE.

## Why it works
AD access control is a web of object permissions. Over-permissive ACLs let you *modify* other
principals: reset a password, add yourself to a privileged group, take ownership then rewrite the
DACL, or grant yourself DCSync — each turning a small right into control.

## Method — abuse per edge (BloodHound names the edge; it also shows the command)
1. **ForceChangePassword** over a user → reset their password: `net rpc password` / `bloodyAD set password`.
2. **GenericWrite / GenericAll over a user** → set an SPN and Kerberoast, or set `msDS-KeyCredentialLink`
   (shadow credentials, `certipy shadow`/`pywhisker`) → auth as them.
3. **AddMember / GenericAll over a group** → add yourself to it (e.g. a privileged group): `net group ... /add`.
4. **WriteDACL / WriteOwner over an object** → take ownership, grant yourself GenericAll, then abuse as above.
5. **DCSync rights** (GetChanges/GetChangesAll on the domain) → `impacket-secretsdump -just-dc` to
   dump all hashes incl. krbtgt (→ golden ticket).
6. **GPO edit rights** → push a scheduled task/immediate task to hosts the GPO applies to → RCE.

## Gotchas
- Let BloodHound plan the *path* — abuse edges in order; each step unlocks the next.
- Shadow credentials (KeyCredentialLink) need a 2016+ DC with PKINIT — often cleaner than a password reset (less noisy, reversible).
- Clean up: remove added group memberships / added creds after proving impact.

## Verify success
Control of the target principal (password/hash/TGT), membership in a privileged group, or a hash
dump via DCSync — advancing the path toward DA.

## References
SpecterOps BloodHound docs (edge abuse); harmj0y "ACL attacks"; impacket/bloodyAD.
