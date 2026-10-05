---
name: attack-saml
description: "SAML SSO attacks — XML Signature Wrapping (8 XSW variants), signature exclusion, and assertion injection for authentication bypass"
category: "authentication"
version: "1.0"
author: "bountyreper-official"
tags:
  - saml
  - sso
  - xml
  - authentication
  - xsw
tech_stack:
  - web
  - saml
cwe_ids:
  - CWE-287
  - CWE-347
chains_with:
  - wstg-athn-04
  - attack-oauth
prerequisites: []
---

# SAML SSO Attack Methodology

## Objective

Exploit SAML-based Single Sign-On via XML Signature Wrapping, exclusion, and assertion manipulation to bypass authentication and impersonate arbitrary users.

> **Attribution:** Methodology from [KathanP19/HowToHunt — SAML](https://github.com/KathanP19/HowToHunt/tree/master/SAML) (8 XSW attacks). Licensed GPL-3.0.

## Testing Methodology

### Phase 1: Identify SAML Flow

```http
POST /saml/acs HTTP/1.1
SAMLResponse=PHNhbWxwOlJlc3BvbnNl... (base64 XML)
```
Decode: `echo <value> | base64 -d | xmllint --format -` — look for `<saml:Assertion>`, `<ds:Signature>`.

### Phase 2: XML Signature Wrapping (XSW) — 8 Variants

Use **SAMLRaider** (Burp extension) — intercept SAMLResponse, click "Apply XSW":

| Attack | What It Wraps | Technique |
|--------|---------------|-----------|
| XSW #1 | Response (enveloping) | Copy Response+Assertion, insert original Signature as child of copied Response |
| XSW #2 | Response (detached) | Same as #1 with detached signature |
| XSW #3 | Assertion (sibling) | Clone Assertion as first child of Response, sibling to original |
| XSW #4 | Assertion (child) | Original Assertion becomes child of duplicated Assertion |
| XSW #5 | Assertion (envelopes Signature) | Duplicated Assertion encircles Signature |
| XSW #6 | Assertion (double envelope) | Copy envelopes Signature which envelopes original |
| XSW #7 | Extensions | Insert Extensions element, add copied Assertion as child |
| XSW #8 | Less-restrictive element | Original Assertion as child of less-restrictive element |

**Exploitation:**
1. Login to SSO with your account
2. Intercept SAMLResponse in SAMLRaider
3. Apply XSW #1-8 one by one
4. Change top assertion's `NameID`/`Subject` to victim (`admin@target.com`)
5. Forward — check if logged in as victim

```bash
# Manual decode/edit
echo "PHNhbWxw..." | base64 -d > saml.xml
# Edit NameID, re-encode
cat saml.xml | base64 -w0
```

### Phase 3: XML Signature Exclusion

Remove `<ds:Signature>` entirely:

```xml
<!-- Original has Signature -->
<samlp:Response><ds:Signature>...</ds:Signature><saml:Assertion>...</saml:Assertion></samlp:Response>
<!-- Remove Signature block -->
<samlp:Response><saml:Assertion>...</saml:Assertion></samlp:Response>
```
If SP doesn't enforce signature, you can forge arbitrary assertions.

Test also:
- Empty signature: `<ds:Signature/>`
- Comment out: `<!-- <ds:Signature>... -->`

### Phase 4: Other SAML Attacks

- **Assertion injection** — add second Assertion with victim's NameID alongside your valid signed assertion
- **ID confusion** — duplicate ID attributes to bypass OpenSAML schema validation
- **Time manipulation** — extend `NotBefore`/`NotOnOrAfter` for replay

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| XSW leads to authentication as arbitrary user | Critical (P1) |
| Signature exclusion accepted (any user) | Critical (P1) |
| Assertion injection accepted | Critical (P1) |
| Time window extension allows replay | High (P2) |

## Evidence Requirements

- Original SAMLResponse (base64)
- Modified SAMLResponse that bypasses
- Session as victim (cookie, profile page)

## Tools

- Burp SAMLRaider (XSW automation)
- `xmllint`, `base64`

## References

- [HowToHunt — SAML](https://github.com/KathanP19/HowToHunt/tree/master/SAML)
- [On Breaking SAML — Be Cheap Be Ahead](https://www.usenix.org/system/files/conference/usenixsecurity13/sec13-paper_somorovsky.pdf)
