---
name: gpo-abuse
description: Use when assessing Group Policy security on an authorized
  AD engagement. Covers GPO enumeration, dangerous settings review,
  GPO based privilege escalation paths, and delegation review. Also
  use when hardening AD and need to know which policies are risky.
version: 1.0.0
domain: ad
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [ad-enumeration, bloodhound-methodology, privesc-windows]
tools:
  - name: Python
    version: "3.12"
---

Group Policy controls every domain machine, so whoever can edit a GPO
can push software, scripts, or credentials to the fleet: it is one of
the most powerful escalation paths in AD. This skill covers authorized
assessment: enumerating GPOs, reviewing dangerous settings, finding
who can edit them, and testing the paths. Lab or authorized domains
only.

## Quick Workflow

1. Enumerate GPOs: links, scope, and edit delegations.
2. Find who can edit each GPO: weak delegations are the entry.
3. Review settings for the dangerous ones: scripts, software
   install, credentials in preferences.
4. Check for GPOs linked at the domain level with broad scope.
5. Test the escalation path in the lab: edit, wait for refresh,
   confirm.
6. Check SYSVOL for readable scripts and credentials.
7. Review GPO backup and change monitoring.
8. Report each editable GPO with its blast radius.

## 1. Enumeration and delegation

```bash
# List GPOs and their edit rights (authorized, PowerView/AD module)
# Get-GPO -All | Select DisplayName, Id
# For each: (Get-GPPermission -Guid $id -All).TrusteeName for edit rights
python3 - << 'PY'
print("flag: Authenticated Users or Domain Users with Edit rights")
print("flag: GPOs linked to Domain Controllers OU with weak delegation")
print("flag: disabled GPOs still linked (confusion, not security)")
PY
```

```bash
# SYSVOL hunt: readable scripts and the classic cpasswords
# (cpasswords are decryptable; any remaining is a critical finding)
find /tmp/sysvol -iname "*.xml" | head -10
grep -ri "cpassword" /tmp/sysvol/Policies/ 2>/dev/null | head -5
# Also: logon scripts with hardcoded credentials, installers with keys
grep -ri -E "password\s*=" /tmp/sysvol/Policies/*/Machine/Scripts/ 2>/dev/null | head -10
```

## 2. Dangerous settings checklist

```bash
# Review each GPO's settings for:
# - startup/logon scripts (arbitrary code on every machine in scope)
# - software installation (push anything anywhere in scope)
# - group policy preferences credentials (decryptable cpassword)
# - local admin via restricted groups (who becomes admin where)
# - firewall disabled, Defender disabled, UAC weakened
echo "each dangerous setting x broad scope x weak delegation = escalation path"
```

## Edge cases

- The GPO is a default domain policy. Editing it affects everything;
  verify its delegation is locked down hardest.
- Delegation looks fine but inheritance is blocked oddly. Review the
  effective application with gpresult on a test machine.
- Fine grained password policies live nearby. Review them in the
  same pass.

## Escalation

- Editable GPO confirmed: demonstrate in the lab (push a harmless
  marker), then report the production path without executing it.
- cpassword found: it decrypts to a real credential; rotate it and
  treat as compromise of wherever it was used.

## Detection and defender view

Defenders see GPO abuse as GPO modifications outside change
windows, new scripts in SYSVOL, and machines running unexpected
startup programs. They defend with tight GPO delegations, change
monitoring on SYSVOL, and blocking the dangerous settings by
policy. The durable practice is least privilege on every GPO plus
alerts on any GPO version change.

## Key references

- MITRE ATT&CK T1484 (Domain Policy Modification).
- Microsoft GPO security guidance.
- Related skills: ad-enumeration, bloodhound-methodology.
