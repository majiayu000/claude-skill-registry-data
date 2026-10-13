---
name: ad-kerberoasting
description: >
  Kerberoasting & AS-REP roasting — request/crack Kerberos tickets to recover service/user
  passwords offline. Load with any domain foothold or valid domain creds, on "kerberoast",
  "AS-REP", SPNs, service accounts, ports 88/389. Signals: domain creds in hand, SPNs set,
  accounts with pre-auth disabled.
domain: ad
type: technique
stability: learning
modes: [pentest]
severity: high
mitre: [T1558.003, T1558.004]
cwe: [CWE-262]
tools: [impacket, hashcat, netexec, rubeus]
schema_version: 1
---

# Kerberoasting & AS-REP roasting

## When it applies
You have valid domain credentials (kerberoasting) or just a username list (AS-REP). Both recover
plaintext passwords offline by cracking Kerberos-issued material — no lockout risk.

## Why it works
- **Kerberoasting**: any authenticated user can request a service ticket (TGS) for any account
  with an SPN; part of it is encrypted with the service account's password hash. Crack it offline.
- **AS-REP roasting**: accounts with "do not require Kerberos preauth" hand out an AS-REP
  encrypted with the user's key to *anyone* — no creds needed, just the username.

## Method
1. **Kerberoast** (need creds): `impacket-GetUserSPNs corp.local/user:pass -dc-ip DC -request`
   (or `nxc ldap DC -u user -p pass --kerberoasting out.txt`). Service accounts are prime targets.
2. **AS-REP roast** (no creds needed): `impacket-GetNPUsers corp.local/ -usersfile users.txt
   -no-pass -request` — pulls hashes for pre-auth-disabled accounts.
3. **Crack offline**: `hashcat -m 13100` (TGS) / `-m 18200` (AS-REP) with `rockyou` + rules.
4. **Use the creds**: service accounts are often privileged → lateral movement / DA path
   (`ad-pivot-arsenal`, `network-pivoting-tunneling`).

## Gotchas
- Offline cracking = no account lockout, but a weak-password dependency; strong passwords resist.
- Target high-value SPNs (SQL, web, admin service accounts) first.
- Clock skew breaks Kerberos — sync time to the DC (`ntpdate`/`faketime`) if you get KRB_AP_ERR_SKEW.

## Verify success
A cracked plaintext password for a domain account, then authenticated access with it.

## References
impacket GetUserSPNs/GetNPUsers; hashcat modes 13100/18200; "Kerberoasting" (Harmj0y).
