---
name: web-xxe
description: >
  XML External Entity injection → file read, SSRF, sometimes RCE. Load when the app parses XML
  you supply: SOAP, SAML, XML APIs, SVG/DOCX/XLSX upload, RSS import, `Content-Type:
  application/xml`. Signals: XML request bodies, "<?xml", SAML responses, file parsers.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A05:2021-Security-Misconfiguration]
cwe: [CWE-611]
tools: [burp, collaborator]
schema_version: 1
---

# XML External Entity (XXE)

## When it applies
The server parses attacker-supplied XML with external entities enabled. Any XML sink counts —
SOAP, SAML, REST-with-XML, and file formats that are XML underneath (SVG, DOCX, XLSX).

## Why it works
XML DTDs can declare entities that the parser resolves — including `SYSTEM` entities that read
local files or fetch URLs. If the parser doesn't disable external entities (the insecure
default in many libs), your entity is expanded server-side.

## Method
> **Payloads & full variation set:** [`cheatsheet.md`](cheatsheet.md) next to this file — work the set, not the first line.
1. **Detect**: inject a DOCTYPE with an external entity and reference it:
   `<!DOCTYPE r [<!ENTITY x SYSTEM "file:///etc/passwd">]>` then `<r>&x;</r>` — file contents in the response = in-band XXE.
2. **Blind / OOB**: no reflection → use an external DTD on your server that exfils via a
   parameter entity to your Collaborator (`file:///` → your URL). DNS/HTTP hit confirms.
3. **SSRF via XXE**: point the entity at internal URLs / `169.254.169.254` (→ `cloud-imds-ssrf`).
4. **File formats**: unzip a DOCX/XLSX, inject XXE into an inner XML part, rezip, upload; SVG upload → XXE.
5. **Error-based**: force a parse error that echoes file content in the message when output is suppressed.

## Gotchas
- Modern parsers disable external entities by default — a null result may mean patched, not absent; try OOB + error-based.
- `php://filter` base64 wrapper reads files that break XML (binary/`<`).
- SAML XXE is high-impact but often behind signature checks — test the pre-validation parse.

## Verify success
Local file contents returned/exfiltrated, or an OOB callback proving the parser fetched your URL.

## References
PortSwigger XXE labs; OWASP XXE Prevention Cheat Sheet.
