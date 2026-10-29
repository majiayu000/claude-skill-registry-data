---
name: ad-enumeration
description: Use when mapping an authorized Active Directory environment during an internal assessment or assumed breach exercise. AD enumeration with kerbrute for Kerberos user discovery, ldapsearch for direct LDAP queries, NetExec modules for SMB, LDAP, and WinRM enumeration, and BloodHound with SharpHound for attack path analysis. Covers domain trusts, SPNs, group memberships, and misconfiguration spotting that feeds Kerberoasting and AS-REP roasting later, with account lockout discipline and OPSEC so enumeration stays quiet and audit-clean.
version: 1.0.0
domain: ad
lifecycle: stable
last_verified: "2026-10-23"
requires:
  - recon-active
extends: []
relates: []
tools:
  - name: kerbrute
    version: 1.0.3
  - name: ldapsearch
    version: 2.6.x
  - name: NetExec
    version: 1.4.0
  - name: BloodHound
    version: 4.3
  - name: SharpHound
    version: 2.x
  - name: nmap
    version: "7.98"
---

Active Directory is the keys to most Windows networks, and enumeration is how
you learn where the keys are. This skill covers mapping a domain you are
authorized to test: finding users without credentials, querying LDAP,
enumerating services with NetExec, and collecting the full graph with
BloodHound and SharpHound. It assumes you have a network foothold (see
recon-active and network-pivoting) and written authorization. Enumeration is
not exploitation, but it is noisy: every technique here includes the
discipline to avoid account lockouts and needless alerts.

## Quick Workflow

1. Confirm the domain name, domain controllers, and the account lockout policy before touching anything.
2. Enumerate valid usernames with kerbrute over Kerberos, no password needed.
3. Query LDAP with ldapsearch, anonymously first, then with any credentials you hold.
4. Run NetExec enumeration modules across SMB, LDAP, and WinRM.
5. Collect with SharpHound and analyze attack paths in BloodHound.
6. Record trusts, SPNs, privileged groups, and misconfigurations as leads for the next phase.

## 1. Baseline: domain, controllers, lockout policy

Start by identifying the domain and its controllers with DNS, then learn the
lockout policy so you never trigger it. SRV records point at domain
controllers directly:

```bash
dig +short _ldap._tcp.example.com SRV
dig +short _kerberos._tcp.example.com SRV
nmap -sV -p 88,389,445,636 203.0.113.10 -oN dc-ports.txt
```

Port 88 is Kerberos, 389 and 636 are LDAP and LDAPS, 445 is SMB. If you have
any domain credential, read the lockout policy first; it dictates how
aggressive you may be:

```bash
nxc smb 203.0.113.10 -u user -p 'Password1' --pass-pol
```

Note the lockout threshold and observation window. A threshold of 5 with a
30 minute window means you never try more than a couple of guesses per user
without waiting. When in doubt, assume the strictest policy.

## 2. Kerberos user enumeration with kerbrute

Kerberos pre-authentication fails differently for valid and invalid users,
which lets kerbrute enumerate accounts without a single password attempt.
This generates no failed logons, so it does not lock accounts, but it is
loud on the wire.

```bash
kerbrute userenum -d example.com --dc 203.0.113.10 \
  /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt \
  -o kerbrute-users.txt -t 20
```

Use a smaller list for the first pass (top 10k names) and expand only if
needed. kerbrute distinguishes "valid user" from "invalid user" by the
error code the KDC returns; some hardened domains return identical errors
for both, in which case user enumeration fails closed and you move on.
Save every valid username: the list feeds password spraying (with strict
discipline) and AS-REP roasting checks later.

## 3. LDAP queries with ldapsearch

LDAP is the directory itself. Try anonymous binding first; many domains
still allow it and it reveals the naming context:

```bash
ldapsearch -x -h 203.0.113.10 -s base -b "" "(objectclass=*)" namingContexts
```

With the base DN (for example `DC=example,DC=com`), pull users and groups:

```bash
ldapsearch -x -h 203.0.113.10 -b "DC=example,DC=com" \
  "(objectClass=user)" sAMAccountName description | grep -i sAMAccountName
ldapsearch -x -h 203.0.113.10 -b "DC=example,DC=com" \
  "(objectClass=group)" cn member | head -60
```

With credentials, the whole directory opens up. Look for high value
attributes: `servicePrincipalName` (Kerberoastable accounts), users with
`userAccountControl` flags for unconstrained delegation or "do not require
Kerberos preauthentication" (AS-REP roastable), and `description` fields
where admins famously leave passwords:

```bash
ldapsearch -x -h 203.0.113.10 -D "user@example.com" -w 'Password1' \
  -b "DC=example,DC=com" "(servicePrincipalName=*)" \
  sAMAccountName servicePrincipalName
ldapsearch -x -h 203.0.113.10 -D "user@example.com" -w 'Password1' \
  -b "DC=example,DC=com" "(userAccountControl:1.2.840.113556.1.4.803:=4194304)" \
  sAMAccountName
```

That bitmask filter finds accounts with pre-authentication disabled.
Always use LDAPS (port 636, `-ZZ` or `ldaps://`) when credentials are
involved so you do not send passwords in cleartext.

## 4. NetExec enumeration modules

NetExec (the maintained successor to CrackMapExec) enumerates SMB, LDAP,
WinRM, and more from one tool. Start with anonymous and guest access checks,
then authenticated enumeration:

```bash
nxc smb 203.0.113.10 -u '' -p '' --shares
nxc smb 203.0.113.10 -u 'guest' -p '' --shares --users
nxc smb 203.0.113.10 -u user -p 'Password1' --shares --sessions --disks
```

Shares with null or guest read access often hold scripts, installers, and
notes with credentials. Enumerate users, groups, and password policy over
LDAP and SMB:

```bash
nxc ldap 203.0.113.10 -u user -p 'Password1' --users --groups
nxc ldap 203.0.113.10 -u user -p 'Password1' --password-not-required --admin-count
nxc winrm 203.0.113.0/24 -u user -p 'Password1'
```

`--password-not-required` and `--admin-count` surface misconfigurations fast:
accounts that can log in with no password and users with the adminCount
flag set (a sign of past or present privilege). The winrm sweep shows where
your credential actually gives command execution, which scopes the next
phase honestly.

## 5. BloodHound and SharpHound collection

SharpHound collects the domain graph (users, groups, computers, sessions,
ACLs, trusts) and BloodHound visualizes attack paths to Domain Admins.
Run the collector from any domain-joined context or with credentials:

```bash
SharpHound.exe -c All -d example.com --domaincontroller 203.0.113.10
```

From Linux, the Python collector works with credentials:

```bash
bloodhound-python -d example.com -u user -p 'Password1' \
  -dc 203.0.113.10 -c All -o bloodhound-out/
```

Import the resulting zip or JSON files into BloodHound and start with the
built-in queries: "Shortest Path to Domain Admins", "Shortest Path to
Unconstrained Delegation Systems", and "All Kerberoastable Users". Read
each path hop by hop and verify every edge manually; BloodHound shows what
the ACLs allow, not what will actually work, and stale data (old sessions,
removed group members) creates phantom paths. Collection touches every
domain computer, so run it once, during the agreed window, not repeatedly.

## 6. Reading the results into leads

Turn the graph into a prioritized lead list: Kerberoastable service
accounts, AS-REP roastable users, unconstrained and constrained delegation,
nested group memberships reaching privileged groups, domain trusts (and
their direction and transitivity), and readable shares with interesting
files. For each lead, note the exact object name, why it matters, and what
phase consumes it. Leads without this context rot in the notes.

## Edge cases

- Kerberos user enumeration fails closed on hardened domains (identical
  errors for valid and invalid users). Accept it and pivot to LDAP and
  NetExec instead of hammering the KDC.
- LDAP signing and channel binding requirements can break older tools. If
  ldapsearch binds but queries fail, retry over LDAPS or check the tool's
  signing support.
- BloodHound data goes stale fast in large domains. Timestamp your
  collection and re-collect before acting on session-based paths older than
  a day.
- NetExec modules against many hosts in parallel can look like a password
  spray to the SOC. Throttle with `--threads 1` style limits when the
  engagement calls for quiet.
- Non-English or renamed built-in accounts (Administrator renamed) break
  scripts that assume default names. Enumerate by SID endings (-500 for the
  built-in admin, -512 for Domain Admins) instead of by name.
- Read-only domain controllers and child domains change what your
  credential can see. Map trusts early so you know which domains are even
  reachable.

## Escalation

When anonymous LDAP is closed and you have no credentials: kerbrute
userenum still works without passwords, and RID brute forcing over SMB
(`nxc smb --rid-brute`) enumerates users from the RID pool. When one domain
controller refuses, try the others; replication lag and per-DC policies
differ. When BloodHound collection is blocked by EDR, fall back to targeted
ldapsearch queries for the specific questions you need (group membership,
delegation, SPNs) instead of full collection. When the domain uses fine
grained password policies, enumerate them (`--pass-pol` per OU) because the
effective lockout threshold may differ from the domain default. If every
enumeration path needs credentials you do not have, stop: that is a finding
about the domain's posture, not a failure, and the report should say so.

## Detection and defender view

Defenders watch AD enumeration closely. Kerberos user enumeration floods
the KDC with pre-auth requests and is a classic early warning. LDAP
queries for the whole directory, especially `servicePrincipalName=*` and
delegation flags, match attacker reconnaissance patterns in SIEM rules.
BloodHound collection is extremely noisy: it contacts every computer and
pulls sessions and ACLs, and there are dedicated detections for SharpHound
binaries. NetExec scans trigger SMB and WinRM alerting. The professional
approach is coordination: agree on an enumeration window with the defensive
contact, use the provided test accounts where possible, and never run
collection tools outside the window. Your logs of what ran, when, and from
where let the blue team separate your activity from a real intruder.

## Key references

- MITRE ATT&CK T1087.002 Domain Account
- MITRE ATT&CK T1069.002 Domain Groups
- MITRE ATT&CK T1018 Remote System Discovery
- MITRE ATT&CK T1482 Domain Trust Discovery
- MITRE ATT&CK T1135 Network Share Discovery
- MITRE ATT&CK T1558.003 Kerberoasting
- MITRE ATT&CK T1558.004 AS-REP Roasting
- MITRE ATT&CK T1110 Brute Force
- CWE-200 Exposure of Sensitive Information to an Unauthorized Actor
- BloodHound docs: https://bloodhound.readthedocs.io
- NetExec docs: https://www.netexec.wiki
- kerbrute docs: https://github.com/ropnop/kerbrute
