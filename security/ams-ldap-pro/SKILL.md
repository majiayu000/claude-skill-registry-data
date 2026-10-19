---
name: ldap-pro
description: Secure LDAP and Active Directory integrations — LDAPS, bind hardening, injection defense, and directory hygiene.
category: security
---

## Overview

LDAP (and Active Directory, its most common implementation) is the directory backbone of most enterprises: authentication, group membership, and authorization decisions all flow through it. That centrality makes its security critical — cleartext binds, anonymous access, and injection flaws in LDAP-integrated apps are perennial findings.

This skill covers defensive directory practice: encrypted binds, least-privilege service accounts, LDAP injection defense in applications, and directory hygiene. It does not cover offensive AD techniques.

The directory is the identity backbone — compromise it and every downstream system falls. Yet directory security is chronically underinvested because 'it just works.' The defensive program is unglamorous and high-leverage: encrypt the binds, shrink the privileges, clean the cruft, and watch the change logs like the crown-jewel telemetry they are.

## When to use

- Integrating applications with AD/LDAP for authentication or group lookup.
- Remediating findings: cleartext LDAP, anonymous binds, over-privileged service accounts.
- Hardening domain controllers and directory infrastructure.
- Reviewing application code that builds LDAP queries or filters.

## Core concepts

- **LDAPS / StartTLS everywhere:** LDAP on port 389 is cleartext — credentials and queries visible on the wire. Use LDAPS (636) or StartTLS, with proper certificate validation. Disable unsigned/cleartext binds.
- **Bind account least privilege:** application bind accounts need read access to exactly the users/groups they serve — not domain admin, not broad read. One bind account per application, with a documented owner.
- **No anonymous binds:** disable anonymous LDAP binds unless a specific, documented need exists; audit for them.
- **LDAP injection defense:** applications must escape or parameterize all user input placed into LDAP filters/DNs (proper escaping per RFC 4515, or parameterized APIs). Treat it with the same seriousness as SQL injection.
- **Directory hygiene:** stale computer accounts, dormant users, overly broad groups (e.g., "Domain Users" with unexpected rights), and unconstrained delegation — the classic AD weaknesses. Review regularly.
- **Protect the DCs:** domain controllers are tier-0 assets — patched first, admin access via PAM with MFA, no internet browsing or email from DCs, monitored intensely.

- **LDAP channel binding and signing.** Beyond encryption, enforce channel binding tokens and LDAP signing to defeat relay and man-in-the-middle attacks against the directory itself.
- **Fine-grained password policies.** One policy for all users is a blunt tool — privileged accounts deserve longer minimums and stricter lockout, applied via fine-grained policy.
- **Read-only domain controllers (RODCs).** For branch offices and DMZ-adjacent placements, RODCs limit what a compromised site exposes — no writable directory data to steal.

## Practical workflow

1. **Inventory integrations:** list every application binding to the directory: bind account, permissions, protocol (LDAP vs LDAPS), and owner. You will find surprises.
2. **Enforce encryption:** migrate all binds to LDAPS/StartTLS; enable "require signing/sealing" policies; verify with packet captures that no cleartext binds remain.
3. **Right-size bind accounts:** strip each to minimum read permissions; rotate their passwords on a schedule (or better, use managed service accounts where the platform supports it); alert on interactive logons by bind accounts.
4. **Fix application code:** review LDAP filter construction in integrated apps; enforce escaping/parameterization; add LDAP injection to the SAST rules and code-review checklist.
5. **Hygiene program:** quarterly reviews — dormant users/computers disabled, stale groups cleaned, delegation constrained, privileged-group membership minimized and monitored.
6. **Monitor:** alert on anomalous directory activity — mass account changes, new privileged-group members, unexpected replication, cleartext-bind attempts, and bind-account misuse.

### Directory hardening checklist

- [ ] All binds encrypted (LDAPS/StartTLS); cleartext and anonymous binds disabled
- [ ] Bind accounts least-privilege, one per app, with owners and rotation
- [ ] Application LDAP filters escaped/parameterized; injection in review checklist
- [ ] Privileged groups minimized; membership changes alerted
- [ ] Dormant/stale accounts and computers cleaned quarterly
- [ ] Delegation constrained; DCs treated as tier-0 (PAM, MFA, hardened)
- [ ] Directory change and bind-failure logging to SIEM

### Sustaining the practice

- Review privileged-group membership monthly — it is the highest-leverage five minutes in directory security
- Audit bind-account permissions semi-annually against least privilege
- Reconcile computer accounts against actual assets quarterly
- Test directory recovery (authoritative restore) annually — backups you cannot restore are fiction

### Metrics that prove it works

- % of binds over LDAPS/StartTLS (target: 100%)
- Bind-account permission reviews completed per cycle
- Dormant account/computer cleanup counts per quarter
- Anomalous directory-activity alerts triaged within SLA

## Common pitfalls

- **Cleartext LDAP "because it's internal."** Internal networks are where attackers operate after initial access. Encrypt it.
- **God-mode bind accounts.** One compromised app credential should not mean directory-wide read (or write). Least privilege per bind account.
- **String-concatenated LDAP filters.** LDAP injection is real and under-tested. Escape or parameterize, and test it.
- **Set-and-forget integrations.** Bind accounts from decommissioned apps linger for years with directory access. Tie bind-account lifecycle to app lifecycle.
- **Ignoring delegation.** Unconstrained delegation on service accounts is a classic privilege-escalation path. Constrain it deliberately.
- **DCs treated like regular servers.** They are the keys to the kingdom — patch, isolate, and monitor them as tier-0.
- **LDAPS certificate expiry breaking authentication.** The encrypted bind depends on a valid cert — monitor DC certificate expiry like any production dependency.
- **Service accounts with interactive logon rights.** Bind accounts should never log on interactively. Alert on it; it is either misconfiguration or misuse.
- **Extending the directory to the cloud without a plan.** Syncing AD to cloud identity without scoping (password hash sync vs federation vs pass-through) creates confusion about where authentication actually happens. Decide deliberately.
- **Letting schema extensions accumulate.** Every schema extension is permanent and expands attack surface. Gate them behind security review.
