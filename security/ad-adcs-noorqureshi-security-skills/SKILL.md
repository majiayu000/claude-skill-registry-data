---
name: ad-adcs
description: >
  Attack Active Directory Certificate Services (ADCS) — ESC1–ESC8 template/CA misconfigurations to
  escalate to Domain Admin. Load with a domain foothold/creds where ADCS is present, on "certipy",
  "ESC1", "certificate template", or a CA server. Signals: Cert Publishers, pKIEnrollmentService,
  ports 443/135 on a CA, certipy find output.
domain: ad
type: technique
stability: learning
modes: [pentest]
severity: critical
mitre: [T1649, T1078]
cwe: [CWE-295, CWE-269]
tools: [certipy, bloodhound, certify]
schema_version: 1
---

# ADCS abuse (ESC1–ESC8)

## When it applies
The domain runs Active Directory Certificate Services and you have any authenticated foothold.
Misconfigured certificate templates or CA settings let a low-priv user obtain a certificate that
authenticates as a privileged account — a fast, reliable path to Domain Admin.

## Why it works
Certificates can be used for Kerberos (PKINIT) authentication. If a template lets an enrollee
specify the subject (SAN) and permits client-auth, a normal user can request a cert *as* Domain
Admin. Other ESCs abuse enrollment-agent rights, vulnerable CA ACLs, NTLM relay to the CA
(ESC8), or the CA cert's private key.

## Method
1. **Enumerate**: `certipy find -u user@corp.local -p pass -dc-ip DC -vulnerable -stdout` — flags
   ESC1–ESC8 with the misconfigured templates/CA.
2. **ESC1 (SAN abuse, most common)**: request a cert for a privileged UPN from a vulnerable template:
   `certipy req -u user@corp.local -p pass -ca CORP-CA -template VulnTemplate -upn administrator@corp.local`.
3. **Authenticate as the target**: `certipy auth -pfx administrator.pfx -dc-ip DC` → gets the TGT/NT
   hash for Administrator → DA.
4. **Other ESCs**: ESC8 = relay AD auth to the CA web endpoint (→ `network-ntlm-relay`) to get a
   cert for a DC; ESC4 = you can edit a template's ACL to make it ESC1; ESC6 = CA `EDITF_ATTRIBUTESUBJECTALTNAME2`.
5. **Persistence angle**: a stolen CA key or a machine cert survives password resets — note for the report.

## Gotchas
- Confirm the template allows **client authentication** and **enrollee-supplied subject** for ESC1.
- Clock skew breaks Kerberos/PKINIT — sync time to the DC.
- Certipy's `find -vulnerable` names the exact ESC — don't guess the path.

## Verify success
A certificate that authenticates as a privileged principal (TGT/NT hash obtained for Administrator
or a DC), demonstrating escalation.

## References
SpecterOps "Certified Pre-Owned"; Certipy wiki; BloodHound ADCS edges.
