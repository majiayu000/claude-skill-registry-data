---
name: playbook-ad
description: AD attack decision tree — which attacks need creds, delegation types, ADCS, key paths to DA. Load when a Windows domain / DC is found. Triggers - domain controller, Kerberos, LDAP, BloodHound, kerberoast, AS-REP, NTLM, ADCS ESC1-8.
---

# Active Directory — Decision Tree

## Without credentials
- **AS-REP Roasting**: accounts with "Do not require Kerberos preauthentication" → offline crack (hashcat -m 18200). No creds needed.
- **Null session**: `enum4linux-ng -A DC` → user list for spray.
- **Password spraying**: one password, many users. Lockout-safe: 1 attempt per 30+ min. Try `Season2024!`, `Company1!`.
- **NTLM relay**: only if SMB signing disabled.

## With any valid user
- **Kerberoasting**: any domain user can request TGS for SPN accounts → offline crack (hashcat -m 13100). Service accounts often have weak passwords.
- **BloodHound**: `bloodhound-python -u USER -p PASS -d DOMAIN -c all` → shortest path to DA.
- **GPP passwords**: `netexec smb DC -u USER -p PASS --gpp-passwords` — legacy, still found.

## Delegation abuse
- **Unconstrained**: machine impersonates ANY user to ANY service. Coerce DC auth (PrinterBug/PetitPotam) → capture TGT → DCSync.
- **Constrained**: impersonate users to SPECIFIC services via S4U2Self + S4U2Proxy.
- **RBCD**: if you can write `msDS-AllowedToActOnBehalfOfOtherIdentity` → impersonate admin.
Discover: `impacket-findDelegation DOMAIN/USER:PASS -dc-ip DC`

## ADCS — check IMMEDIATELY if present
ESC1–ESC8, many give instant DA:
- **ESC1**: enrollable template with SAN override → request cert as DA
- **ESC4**: template owner → modify template → create ESC1
- **ESC8**: HTTP enrollment → NTLM relay to ADCS web endpoint
Tool: `certipy find -u USER@DOMAIN -p PASS -dc-ip DC -vulnerable`

## Four classic paths to DA
1. AS-REP → crack → Kerberoast → crack SPN → ACL path → DA
2. Spray → creds → BloodHound → ACL abuse (GenericAll/WriteDACL) → DA
3. Null session → user list → spray → delegation abuse → DA
4. NTLM relay → local admin → cred dump → lateral → DCSync

## DCSync (endgame)
Requires "Replicating Directory Changes" rights:
`impacket-secretsdump DOMAIN/USER:PASS@DC` → all domain hashes + krbtgt.
With krbtgt hash → Golden Ticket → persistent DA.
