---
name: web-file-upload
description: >
  Turn a file upload into RCE or stored XSS/SSRF. Load on any upload: avatars, attachments,
  import CSV/XML, profile images, document processors, "upload your resume". Signals:
  multipart/form-data, filename in response, an uploads/ path, image thumbnailing, PDF/office parsing.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: critical
owasp: [A04:2021-Insecure-Design, A03:2021-Injection]
cwe: [CWE-434]
tools: [burp, exiftool]
schema_version: 1
---

# Malicious file upload

## When it applies
The app accepts a file and later stores, serves, parses, or converts it. Impact depends on
what happens to the file after upload — served from webroot? passed to a parser? rendered?

## Why it works
Validation is usually on the wrong signal (extension or `Content-Type`, both attacker-set)
while the dangerous behaviour is downstream: the web server executes `.php` in the uploads
dir, a parser follows external entities, or the file is served with an HTML content-type.

## Method
> **Payloads & full variation set:** [`cheatsheet.md`](cheatsheet.md) next to this file — work the set, not the first line.
1. **Find the after-upload behaviour**: where is it stored, what URL serves it, what parses it?
2. **RCE via executable extension** when uploads are under a script-executing webroot:
   upload `shell.php`; if blocked, try `.phtml .php5 .phar`, double ext `shell.php.jpg`,
   null byte `shell.php%00.jpg`, case `.pHp`, trailing dot/space, or a polyglot (valid JPEG +
   PHP in a comment) with a `.php` name.
3. **Content-Type / magic-byte bypass**: keep a real image header (`GIF89a;`) then payload;
   change the multipart `Content-Type` to `image/png` while the name stays `.php`.
4. **Parser-based**: SVG upload → XSS/SSRF/XXE (SVG is XML+script); office/PDF → SSRF/XXE via
   external resources; image libraries (ImageMagick) → command exec via crafted files.
5. **Path traversal in filename**: `../../var/www/html/shell.php` to escape the uploads dir.

## Gotchas
- Upload succeeds but stored outside webroot / served as `text/plain` → no RCE; pivot to XSS/SSRF instead.
- Random server-side filenames defeat direct access — look for a predictable/leaked path.
- WAF strips `<?php` → use `<?=` or `<script language="php">`.

## Verify success
Browse to the uploaded script and get command output, or the SVG/XML fires in a victim
context / triggers an OOB callback.

## References
PortSwigger file-upload labs; OWASP Unrestricted File Upload.
