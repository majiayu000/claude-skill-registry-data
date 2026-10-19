---
name: bb-rce
description: Hunt Remote Code Execution and injection-to-RCE chains — command injection, SSTI, deserialization, archive/VCS-import pipelines, file-upload-to-RCE, path traversal to file read/write, and framework-specific exploits (Spring, Jinja2, log4shell-class). Use whenever the user mentions RCE, command injection, SSTI, template injection, deserialization, file upload leading to code execution, zip/tar import bugs, path traversal, or "get a shell" on an authorized bug bounty target.
---

# RCE Hunter

The rarest, highest-paid class (397 records in the corpus, top payouts $33.5k). On bug bounties, RCE almost never arrives as a naked `?cmd=` — it arrives in an archive, a template, a filename, a parser, or a deserialized blob. WARNING: proving RCE on production is risky — programs forbid destructive proof. Prove with a harmless marker (sleep, DNS lookup of your own domain, `id`/`whoami` output), never drop shells, reverse connections, or persistent payloads.

## Real-bug anchors (what actually paid — query bb-disclosures for more)
- **$33,510** RCE via the **DecompressedArchiveSizeValidator** + project BulkImports — archive handling in import pipelines.
- **$33,510** RCE via **GitHub import** — VCS import features execute with service privileges.
- **$25,000** **Exposed Kubernetes API** — RCE/exposed creds. Control planes with real access = RCE-tier money; login-page-only = $0.
- **$20,160** Pre-auth RCE on a corporate **VPN** appliance — perimeter appliances, unauthenticated.
- **$29,000 / $20,000 / $16,000** **Arbitrary file read** via bulk imports / upload rewriters / project import (path traversal family — see below).
Delta lesson: **import/export pipelines processing archives and VCS data** are the modern RCE front door. Pairs with file-read payouts in the same features.

## Where RCE hides (target list)

| Feature | Class | Probe |
|---|---|---|
| **Import from URL / GitHub / zip / tar** | SSRF→parser→RCE chain | symlink members, decompression quirks, path members (`../../`) |
| **Archive validators/extractors** (zip/tar/tar.gz/rar) | parser bugs, zip-slip | `../` entry names, symlink entries, nested archives |
| PDF generators, invoice renderers, email templates | SSTI | `{{7*7}}`, `${7*7}`, `<%= 7*7 %>`, `#{7*7}` |
| File name / title / comment fields passed to shell | command injection | backticks, `$(id)`, `;id`, `|id`, `\nid` |
| Import/export (XML, YAML, serialized blobs) | deserialization | crafted payloads per stack (see below) |
| Image/document processing pipelines | parser CVEs, ImageMagick | version fingerprint first |
| URL fetch + render (see bb-ssrf) | SSRF→internal admin→RCE chain | chain, don't claim directly |
| Uploads (avatar, import, attachment) | upload→webroot→execute | polyglot + extension handling |
| Legacy headers (X-Forwarded-For logged to shell-outs) | log/param injection | `$(sleep 5)` in headers that get logged server-side |
| User-Agent / Referer in server logs + admin log viewer | stored XSS→admin→RCE chain | chain via bb-chains |

## Path traversal to arbitrary file read (same features, quieter, pays big)
`filename="../../etc/passwd"`, `?path=`, `attachment_url` members, "move/copy issue/project" flows rewriting upload paths. The $16k–$29k examples were all upload/import pipelines resolving user-controlled paths. Non-destructive proof: read a known harmless file and show the bytes.

## SSTI engine fingerprints
`{{7*7}}`→49: Jinja2/Twig/Liquid · `${7*7}`→49: Freemarker/Velocity/Thymeleaf · `<%= 7*7 %>`→49: ERB/EJS · `#{7*7}`→49: Ruby/PEB · `{{7*'7'}}`→7777777: Jinja2 (vs 49: Twig). Then engine-specific harmless proof: Jinja2 `{{config}}` (config leak = already High), never jump straight to `os.popen`.

## Command injection ladders
- Separator set: `;`, `|`, `&&`, `\n`, backticks, `$()`
- Blind: `sleep 5` (time delta), DNS marker `$(nslookup marker.your-oob-domain)` — time and OOB both required for a credible blind PoC.
- Filtered: quote-wrapping breaks (`a";id;"`), IFS tricks (`cat</etc/passwd`), encoding.

## Deserialization quick map
Java: `ac ed 00 05` magic / base64 `rO0AB`; ysoserial-style payloads only on staging or with explicit program permission. PHP: `O:N:"Class"` in cookies/params → gadget chains. .NET: `ViewState` without MAC → ysoserial.net. Python pickle in session cookies: base64 blob → `pickle.loads` proof with harmless opcode.

## Upload-to-RCE path
1. Extension handling: `.php`, `.phtml`, `.php5`, `.jsp`, `.jspx`, `.asp`, `.aspx`, `.cfm` + double (`a.php.jpg`), null byte, case (`.PhP`).
2. Polyglots: GIF89a header + PHP; EXIF comment injection.
3. Path control: `filename="../../webroot/x.php"` in multipart (path traversal + write).
4. Content-type confusion: SVG with embedded script (also XSS), HTA, HTML uploads.
5. Prove execution, not upload: an uploaded `.php` that isn't executed is Low (arbitrary file upload) — execution is the RCE.

## Product / binary targets (desktop agents, appliances, panels, mobile)
When the target ships software rather than just a web app, read `references/product-0day-patterns.md` first — paid patterns for .NET wholesale decompilation (Veeam, $30k), pre-auth ODBC/DSN injection (Adminer), vendor forks of dead OSS (cPanel), localhost WebSocket hijacking → zero-click RCE, Frida mobile RE with DNS-tunnel exfil, and exported Android components. Also: ASN→CIDR origin discovery to find forgotten panels behind CDNs.

## Rules
- Marker-based proof only on production: `id`, `whoami`, hostname, sleep, OOB DNS. NO shells, NO reverse TCP, NO file writes outside temp, NO crypto miners (obviously).
- Program scope for RCE often excludes DoS-ish probes (sleep on busy endpoints) — keep it to one request.
- Chain incomplete RCE (LFI with include, SSRF to internal service) into bb-chains for full impact write-up; report the achieved step with the chain path documented.
