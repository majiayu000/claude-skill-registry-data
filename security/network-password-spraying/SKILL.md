---
name: network-password-spraying
description: >
  Low-and-slow credential attacks against exposed auth surfaces — spray one password across many
  users, and stuff known breach creds — without locking accounts. Load on a login portal or
  service auth with valid usernames: OWA/O365/Entra, VPN, Citrix, SSH, RDP, SMB, LDAP, or a web
  login. Signals: a harvested user list, "AzureAD"/"outlook", 401/403 on auth, lockout policy known.
domain: network
type: technique
stability: learning
modes: [pentest]
severity: high
owasp: [A07:2021-Identification-and-Authentication-Failures]
mitre: [T1110.003, T1110.004]
cwe: [CWE-307, CWE-521]
tools: [nxc, kerbrute, hydra, msspray]
schema_version: 1
---

# Password spraying & credential stuffing

## When it applies
You have (or can build) a list of valid usernames and a reachable authentication surface, and the
engagement authorizes credential attacks. Spraying beats brute force whenever a lockout policy
exists — you try *one* password against *every* user, not many passwords against one.

> **Mode gate:** this is `pentest`-only. Nearly every bug-bounty program prohibits brute force,
> credential stuffing, and anything that risks account lockout or DoS — do not spray on a bounty
> target. Confirm the lockout policy and testing window in `roe.md`/`scope.txt` first
> (`tradecraft-scope-roe`).

## Why it works
Organizations enforce complexity but not unpredictability: in any large user set, some accounts
use `Season+Year!`, `Company@123`, or a breach-reused password. Spraying one guess per user per
lockout window stays under the counter, so you get many attempts' worth of coverage without
tripping lockouts.

## Method
1. **Build the user list.** Enumerate/validate names first (OSINT, `recon-*`, Kerbrute against a
   DC, O365 user-enum). Verify the username format (`first.last`, `flast`, UPN) before spraying.
2. **Learn the lockout policy.** Read it from AD (`net accounts`, `nxc smb <dc> --pass-pol`) or
   ask. Stay to **one attempt per user per window**, and leave a margin (e.g. 4 tries if the
   threshold is 5). Track attempt timestamps so you never double-tap a user in a window.
3. **Pick seasonal/contextual candidates**, not a wordlist: `Month+Year!`, `Season+Year!`,
   `<CompanyName>1!`, `Welcome1`, `Password1`. One or two per window, spaced across windows.
4. **Spray the surface** with a tool that throttles and tracks:
   - AD/SMB/LDAP: `nxc smb <dc> -u users.txt -p 'Season2026!' --continue-on-success`
   - Kerberos (pre-auth, quieter, no SMB logon events): `kerbrute passwordspray -d <domain> users.txt 'Season2026!'`
   - O365/Entra: a purpose-built sprayer that handles throttling and MFA responses.
5. **On a hit, stop and pivot** — validate the cred, check where it's valid (SMB/WinRM/VPN/OWA),
   and move to `ad-*` / `privesc-*` rather than continuing to spray.

## Gotchas
- **Lockout is the cardinal risk** — miscounting windows or a retry loop can lock out a whole
  department. Rate is a hard limit, not a suggestion; when unsure, slow down.
- **Smart lockout / conditional access** (Entra) can *look* like a wrong password while silently
  flagging you — watch for changed response timing/codes, not just "failed".
- **MFA**: a valid password against an MFA-gated portal is still a real finding (and may expose
  MFA-fatigue or legacy-protocol bypass) — record it; don't try to defeat MFA unless authorized.
- **Credential stuffing** (breach-list creds) only against accounts/domains in scope; never load
  third-party breach data about people outside the engagement.

## Verify success
A username+password pair authenticates against an in-scope service, confirmed with a benign action
(e.g. `nxc` reports `[+]`, an OWA login, or a VPN session) — with no accounts locked out.

## References
MITRE ATT&CK T1110.003/.004; NetExec (nxc) and Kerbrute docs; NIST SP 800-63B on credential policy.
