---
name: web-saml
description: >
  Attack SAML SSO — signature exclusion/wrapping (XSW), unsigned assertions, and comment/XXE tricks
  to forge authentication. Load on SAML SSO (SAMLResponse, ACS URL, IdP/SP), enterprise login, or
  "SAML". Signals: SAMLResponse base64 in POST, /saml/acs, <saml:Assertion>, Shibboleth/ADFS/Okta SSO.
domain: web
type: technique
stability: learning
modes: [bugbounty, pentest]
severity: critical
owasp: [A07:2021-Auth-Failures]
cwe: [CWE-347, CWE-287]
tools: [burp, SAMLRaider]
schema_version: 1
---

# SAML authentication attacks

## When it applies
The app authenticates via SAML SSO — the browser POSTs a base64 `SAMLResponse` (an XML assertion
signed by the IdP) to the SP's ACS endpoint. Break the signature validation and you forge login as anyone.

## Why it works
SAML security rests entirely on the SP correctly validating the XML signature over the assertion.
XML signature validation is notoriously error-prone: SPs accept unsigned assertions, validate the
wrong element, or can be tricked by **XML Signature Wrapping (XSW)** — where a signed element is
kept for validation but an injected unsigned assertion is what the app actually reads.

## Method
1. **Capture & decode** the `SAMLResponse` (Burp + **SAML Raider** extension). Identify what's
   signed (Response vs Assertion) and the `NameID`/attributes that set the user.
2. **Signature exclusion**: strip the `<ds:Signature>` and send — some SPs accept unsigned assertions.
3. **XSW**: wrap/inject a second assertion (or move the signature) so the validator checks the
   original signed blob but the app consumes your forged assertion with `NameID=admin` (SAML Raider automates the XSW variants).
4. **Comment injection**: `admin@corp.com<!---->.evil` in `NameID` — some parsers read it as `admin@corp.com` post-canonicalization → login as admin.
5. **Other**: key confusion (SP trusts attacker cert), XXE in the SAML parser (→ `web-xxe`), replay
   if no `NotOnOrAfter`/`InResponseTo` checks, `Recipient`/`Audience` not validated.

## Gotchas
- Identify the exact signed element first — XSW works by satisfying the validator while changing what's *used*.
- If signatures are properly validated over the assertion with no wrapping bug, pivot to replay/audience/comment issues.
- Prove with two accounts you own: forge from a low-priv login into a privileged `NameID`.

## Verify success
Authentication as a different/privileged user via a forged or manipulated SAMLResponse the SP accepts.

## References
PortSwigger SAML; SAML Raider; "On Breaking SAML" (XSW, Somorovsky et al.).
