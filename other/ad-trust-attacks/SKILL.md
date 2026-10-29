---
name: ad-trust-attacks
description: Use when assessing Active Directory trust relationships
  on an authorized engagement. Covers trust enumeration, SID history
  abuse, cross forest Kerberos attacks, and trust direction review.
  Also use when a multi domain or multi forest environment needs its
  trust boundaries tested.
version: 1.0.0
domain: ad
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [ad-enumeration, bloodhound-methodology, kerberoasting, golden-ticket]
tools:
  - name: Python
    version: "3.12"
---

AD trusts let users from one domain access another, and each trust is
a path an attacker can walk: SID history, cross forest tickets, and
misconfigured trust directions. This skill covers authorized
assessment: enumerating trusts, reviewing their configuration, and
testing the abuse paths. Lab or authorized enterprise only, with
care for production domains.

## Quick Workflow

1. Enumerate all trusts: domains, direction, type, and transitivity.
2. Review each trust's purpose: is it still needed.
3. Check SID filtering status: the main defense against SID history
   abuse.
4. Test cross trust Kerberos: what a compromised account in one
   domain can reach in another.
5. Look for the classic abuses: SID history injection, golden
   tickets across trusts.
6. Check trust account passwords and their age.
7. Review selective authentication where used.
8. Report each trust with its attack paths.

## 1. Trust enumeration

```bash
# Enumerate trusts (domain joined host, authorized)
nltest /trusted_domains 2>/dev/null || echo "use powerview equivalent"
# PowerShell (authorized):
# Get-ADTrust -Filter * | Select Name,Direction,TrustType,SelectiveAuthentication
python3 - << 'PY'
print("record per trust: name, direction (in/out/bidirectional),")
print("type (forest/external/shortcut), transitive?, SID filtering?")
PY
```

```bash
# BloodHound already maps trusts; check the attack paths view
# for: shortest path from owned principal to target across trusts
echo "in BloodHound: map trusts, then query cross domain paths"
```

## 2. SID history and filtering review

```bash
# Check SID filtering (quarantine) on each trust: it blocks SID history
# abuse across the trust. Verify in the trust properties or:
# netdom trust TRUSTING /domain:TRUSTED /quarantine:yes
echo "verify: quarantine enabled on every external and forest trust"
```

```bash
# Hunt SID history abuse indicators (authorized):
# accounts with SIDHistory pointing at privileged SIDs of another domain
# PowerShell: Get-ADUser -Filter * -Properties SIDHistory | ? {$_.SIDHistory}
echo "any SIDHistory on non migration accounts is suspicious"
```

## Edge cases

- The trust is legacy and undocumented. Treat it as hostile until
  reviewed; legacy trusts are the classic forgotten path.
- Selective authentication is on. Test whether it is actually
  enforced or just configured.
- One way trust assumed safe. Inbound trusts still leak information
  and enable some attacks; review both directions.

## Escalation

- Trust abuse path confirmed: demonstrate the cross domain reach
  with a test account, then stop; domain hopping is sensitive.
- Trust cannot be removed for business reasons: harden it
  (filtering, selective auth) and monitor the trust traffic.

## Detection and defender view

Defenders see trust attacks as cross domain ticket requests,
SIDHistory anomalies, and authentication from unexpected domains.
They defend with SID filtering on all trusts, selective
authentication for sensitive resources, and monitoring of trust
traffic. The durable practice is trust minimization: remove what
is not needed, filter what remains.

## Key references

- MITRE ATT&CK T1482 (Domain Trust Discovery), T1134 (Access Token
  Manipulation): SID history.
- Microsoft trust documentation: SID filtering.
- Related skills: ad-enumeration, golden-ticket.
