---
name: tools-sqlmap
description: >
  Operate sqlmap to confirm and exploit SQL injection — target selection from Burp requests, level/risk
  tuning, tamper scripts for WAF evasion, DB enumeration, and safe dump discipline. Load after a manual
  SQLi probe shows promise, or when automating confirmation across parameters. Signals: sqlmap, --batch
  --dbs, --tamper, --os-shell, "parameter is vulnerable", time-based blind, SLEEP(5), sqlmap resume.
domain: tools
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
mitre: [T1190]
cwe: [CWE-89]
tools: [sqlmap]
schema_version: 1
---

# sqlmap injection automation

## When it applies
Manual testing (`web-sqli`) has produced a suspicious parameter on an in-scope target
(`tradecraft-scope-roe`), or you have many in-scope parameters and need automated triage. sqlmap
takes over the tedious part — confirming the injection type, fingerprinting the DBMS, enumerating
schema, and extracting proof data. It is an exploitation accelerator, not a discovery substitute:
feed it a real request, not a bare URL you have never looked at.

## Why it works
sqlmap automates the full injection matrix per parameter — boolean-based, error-based, UNION query,
stacked queries, and time-based blind (`--technique=BEUST`) — with per-DBMS dialects and a tamper
pipeline that rewrites payloads to slip past filters. Because it replays a captured request, it
tests exactly the auth state, headers, and body the app expects.

## Method
1. **Start from a captured request, not a URL** — save a working authenticated request from Burp and
   run `sqlmap -r req.txt --batch`. URL-mode equivalents:
   ```bash
   sqlmap -u "http://target/page?id=1" --batch
   sqlmap -u "http://target/login" --data="user=admin&pass=test" --batch
   sqlmap -u "http://target/page?id=1" --cookie="PHPSESSID=xxx" --batch
   ```
2. **Aim it.** `-p id` to test one parameter; mark the injection point inline with `*` (works in
   `--data` and `--cookie` too): `--data="a=1&b=2*&c=3"`. If you already know the backend,
   `--dbms=mysql` skips fingerprinting.
3. **Turn up coverage deliberately:** `--level=5 --risk=3` tests more (headers at level 3+, heavier
   payloads at higher risk) — but each step multiplies request count and, at risk 3, adds
   OR-based payloads that can UPDATE whole tables. Escalate only after the default pass fails.
4. **Evade filters with tamper scripts** (see `payloads-waf-bypass` for the manual matrix):
   ```bash
   sqlmap -u "http://target/page?id=1" --tamper=space2comment,between --random-agent
   ```
   | Tamper | Effect |
   |--------|--------|
   | `space2comment` | spaces → `/**/` |
   | `between` | `>` → `BETWEEN` |
   | `randomcase` | random keyword casing |
   | `charencode` | URL-encode every char |
   | `equaltolike` | `=` → `LIKE` |
   | `base64encode` | Base64 the payload |
5. **Enumerate only what proves impact:**
   `--dbs` → `-D db --tables` → `-D db -T table --columns` → `-D db -T table -C col1,col2 --dump`.
   Dump the minimum rows that demonstrate access (a few users, not the whole table).
6. **Watch it work** — `--proxy="http://127.0.0.1:8080"` routes everything through Burp so you can
   see exactly what was sent and learn why a run failed.
7. **`--os-shell` only when the engagement explicitly includes code execution** — it writes a file
   to the server (into the webroot); record the path and delete it during cleanup.

## Gotchas
- **No cookies/session = scanning a login page** — if the request needs auth, give sqlmap the exact
  cookie/token from a live session, or every response is the same 302 and it reports nothing.
- **"not injectable" after defaults is not "not vulnerable"** — work the matrix: raise `--level`,
  try `--technique=T` alone for pure time-based, add tamper scripts, test other parameters. Only
  then mark the lead failed (House rules).
- **False positives happen** — confirm the extracted data is real (does the "user" exist in the UI?)
  before writing the finding (`reporting-triage-validation`).
- **WAF/rate-limit bans mid-run** — symptoms: responses suddenly all identical/blocked. Slow down
  (`--delay`), rotate UA (`--random-agent`), and check `roe.md` request-rate limits first.
- **Interrupted runs resume** — sqlmap keeps session state in its output dir; rerun the same command
  instead of starting over.
- **`--risk=3` can modify data** — OR-true payloads against UPDATE contexts rewrite rows. On
  production-scope targets, stay at risk 1–2 unless the RoE says otherwise.

## Verify success
sqlmap names the injection type and DBMS, and you hold minimal extracted proof (e.g. one row from a
table you should not reach) plus the exact `-r` request and flags — enough for another tester to
reproduce the finding verbatim.

## References
sqlmap docs and tamper script list. Detection theory and manual payloads: `web-sqli` and its
cheatsheet; WAF evasion matrix: `payloads-waf-bypass`.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
