---
name: ad-delegation-abuse
description: >
  Abuse Kerberos delegation to impersonate users and take over hosts — unconstrained, constrained
  (S4U2Self/S4U2Proxy), and resource-based (RBCD), including the coercion → NTLM-relay-to-LDAP →
  RBCD chain. Load in an AD environment when BloodHound/enum shows delegation rights, a machine
  account you control, GenericWrite/GenericAll over a computer, or coercion is possible. Signals:
  msDS-AllowedToActOnBehalfOfOtherIdentity, TRUSTED_FOR_DELEGATION, msDS-AllowedToDelegateTo, PetitPotam.
domain: ad
type: technique
stability: learning
modes: [pentest]
severity: critical
mitre: [T1558.003, T1550.003, T1187]
cwe: [CWE-284, CWE-269]
tools: [rubeus, impacket, bloodhound, netexec, certipy]
schema_version: 1
---

# Kerberos delegation abuse

## When it applies
An AD engagement where enumeration (BloodHound, `nxc`, LDAP) shows a delegation primitive: a host
trusted for unconstrained delegation, an account with constrained delegation (`msDS-AllowedToDelegateTo`),
or — most commonly — write access over a computer object so you can set RBCD. Coercion + relay turns
"can authenticate a DC" into "control a DC". This is the modern lateral-movement/DA path.

## Why it works
Delegation lets a service act *on behalf of* a user. Kerberos implements it with S4U2Self (get a
ticket to yourself as any user) and S4U2Proxy (forward it to a target service). If you control an
account permitted to delegate — or can write `msDS-AllowedToActOnBehalfOfOtherIdentity` on a target
(RBCD) — you can mint a service ticket as *any* user, including Domain Admin, to that target.

## Method
1. **Enumerate the primitive.** BloodHound edges (`AllowedToDelegate`, `AllowedToAct`,
   `GenericWrite`/`GenericAll` on a computer), or `nxc ldap ... --trusted-for-delegation` /
   LDAP queries for the delegation attributes.
2. **Unconstrained** — on a host trusted for unconstrained delegation, capture TGTs of any user who
   authenticates to it (`Rubeus monitor`), and coerce a DC to authenticate (below) to grab the DC's
   TGT → DCSync.
3. **Constrained (S4U)** — with an account that has `msDS-AllowedToDelegateTo <spn>`:
   `getST.py -spn <spn> -impersonate Administrator '<domain>/<svc>:<pass>'` (or `Rubeus s4u`).
   `altservice`/SPN-substitution lets one allowed SPN pivot to others on the same host.
4. **RBCD (the write-driven path)** — when you control a computer account and can write the target's
   `msDS-AllowedToActOnBehalfOfOtherIdentity`:
   - Set it: `rbcd.py -delegate-to <TARGET$> -delegate-from <YOURMACHINE$> -action write ...`
   - Impersonate: `getST.py -spn cifs/<target> -impersonate Administrator '<domain>/<YOURMACHINE$>:<pass>'`
   - Use the ticket (`KRB5CCNAME=...`) with `psexec.py -k -no-pass`, `secretsdump.py -k`, etc.
5. **Coercion → relay → RBCD (no creds needed to start)** — coerce a target/DC to authenticate to
   you (`PetitPotam.py`, `coercer`), relay that NTLM to LDAP(S) and grant yourself RBCD:
   `ntlmrelayx.py -t ldaps://<dc> --delegate-access`, then S4U as above. (See `network-ntlm-relay`.)

## Gotchas
- **`altservice` only works within the same host's SPNs** — you can swap `cifs`→`host`→`http` on the
  target, not jump machines.
- **`ProtectedUsers` / "Account is sensitive and cannot be delegated"** blocks impersonating that
  principal — pick another admin, or a computer account.
- **Clock skew** breaks every Kerberos step — sync to the DC (`ntpdate`/`faketime`) first.
- **RC4 disabled / AES-only** domains need AES keys in your tooling flags; RC4 tickets get rejected.
- **RBCD needs write on the *target* computer**, and creating a fake computer needs
  `ms-DS-MachineAccountQuota > 0` (or use a machine account you already own).

## Verify success
A service ticket as a privileged user to the target service, used to run a command / dump secrets
(`secretsdump.py -k`) you could not before — e.g. local admin on the target or DCSync from a
coerced DC.

## References
Elad Shamir "Wagging the Dog" (RBCD); Impacket `getST.py`/`rbcd.py`/`ntlmrelayx.py`; Rubeus S4U docs;
MITRE ATT&CK T1558.003. Coercion+relay mechanics: `network-ntlm-relay`.
