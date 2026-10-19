---
name: bb-sqli
description: Hunt SQL injection on authorized targets — boolean, time-based, error-based, and UNION SQLi in APIs, filters, sort params, array parameters, legacy PHP/report endpoints, and JSON/GQL inputs, plus safe confirmation without sqlmap on production. Use whenever the user mentions SQL injection, SQLi, database injection, or wants to test parameters that hit a database on an authorized bug bounty.
---

# SQLi Hunter

Modern ORMs killed the easy SQLi; survivors hide in ORDER BY columns, search filters, IN-lists, array params, and raw query escape hatches. On production: proof must be non-destructive (boolean diff or sleep ≤3s, once), never `sqlmap --batch` against the live target without explicit program permission — most programs allow it only throttled, some ban it outright.

## Real-bug anchors (what actually paid — query bb-disclosures for more)
- **$25,000** SQLi in `report_xml.php` through the **`countryFilter[]` array parameter** — legacy report/XML endpoints with array-style params are the top survivor.
- **$4,500** plain SQLi on a marketing site (`www.drivegrab.com`) — forgotten microsites run old code.
- **$4,263** CVE-2024-42005 Django ORM bypass in `QuerySet.values()` — even framework "safe" paths leak.
- **$4,134** **Blind SQLi** on `id.indrive.com` — blind confirmed by timing/oracle is full-price.
Delta lesson: array/suffixed params (`param[]`), legacy `.php` report endpoints, and forgotten microsites carry the class. Blind is not cheaper.

## Where SQLi survives (target list)
- **Array/suffixed parameters**: `countryFilter[]`, `ids[]`, `filter[status]` — implode-into-IN() builders.
- **Sort/order params**: `?sort=name` → `ORDER BY name` — can't be parameterized → classic survivor. Test column-name injection.
- **Filter builders**: `?filter[status]=x&filter[created]=y` frameworks building raw WHERE.
- **Legacy PHP/report/XML endpoints** (`report_xml.php`-style, export endpoints, cron-facing pages) — wayback CDX finds these forgotten paths.
- **Search**: `?q=`, autocomplete, faceted search backends (sometimes NoSQL/Lucene instead — fingerprint first).
- **IN-lists / batch params**: `?ids=1,2,3` string-concatenated.
- **Legacy/second-order**: values stored then used in a later raw query (import file names, report generators).
- **JSON/GraphQL inputs**: string fields that reach raw SQL in resolvers (`filter`, `search` args).

## Wordlist (bundled)
`assets/sql-wordlist.txt` — 1,080-entry SQLi payload list (orwagodfather/SQL-Wordlist), URL-encoded, spanning boolean/error/time-based/UNION across MySQL/Postgres/MSSQL/Oracle. Grep by technique instead of replaying the whole file:
```bash
grep -i 'sleep'   <path-to-skill>/assets/sql-wordlist.txt   # time-based (PG_SLEEP, waitfor delay, sleep())
grep -i 'union'   <path-to-skill>/assets/sql-wordlist.txt   # UNION extraction
grep -iE "or.2\+|=0\+" <path-to-skill>/assets/sql-wordlist.txt  # boolean arithmetic
```
Standout entry that beat strict filters in a paid hunt (Bugcrowd, $20.3k campaign — worked where classic `AND SLEEP()` was blocked): `1'XOR(SELECT CASE WHEN(1234=1234) THEN SLEEP(7) ELSE 0 END)XOR'Z` — XOR/CASE wraps the sleep in arithmetic context, no AND/OR keywords.

## Where to aim first (targeting heuristics from paid campaigns)
- **Legacy fields populated FROM the database** — country/state select dropdowns, sort labels: old columns, old code, often unprotected. Time-based first, value differs from modern API params.
- Forgotten microsites and origin IPs behind CDNs (ASN → CIDR recon) run old PHP where classic `' OR 1=1` still lands.

## Detection ladder (cheap → expensive, per parameter)
1. **Error probing** (free): `'` `"` `)` `` ` `` `\`` — response 500/changed error = candidate. Grep responses for SQL fragments (MySQL/Postgres/MSSQL/Oracle error signatures).
2. **Boolean diff**: `AND 1=1` vs `AND 1=2` — response length/content differs deterministically (send each twice to rule out noise).
3. **Time-based** (blind confirmation): `AND SLEEP(2)` / `pg_sleep(2)` / `WAITFOR DELAY '0:0:2'` — one request, measure; compare to a control request. Cap at 2-3s, never stack.
4. **UNION** (only after confirming): `ORDER BY n--` column count, then `UNION SELECT NULL,NULL,...` — extraction stops at proving read access (`version()`, `current_user`). Do NOT dump user tables on production — one `version()` is the full PoC; anything more risks program violations.

## Context escaping cheat sheet
- In string: `' AND '1'='1` / close-quote strategies. In numeric: ` AND 1=1-- `. In JSON string value: same payloads, watch double-encoding. In ORDER BY: `name)--`/`(SELECT 1)` boolean via sort error. In array params: `countryFilter[]=x' AND '1'='1`.
- WAF-filtered: case (`SeLeCt`), comments (`SE/**/LECT`), URL/double-encoding, unicode homoglyphs — one variation at a time, logged (bb-chains bypass discipline).

## NoSQL & friends (fingerprint before assuming SQL)
Mongo: `{"$gt":""}` / `$ne` in JSON params. Elasticsearch/Lucene: `*`-wildcard injection in search. GraphQL: filter-arg injection. Fingerprint via error strings before choosing payloads.

## Verdict + evidence
- Confirmed = boolean diff (two clean pairs of requests) OR one time-based hit with control OR `version()` output. All three: request + response saved verbatim.
- "500 on quote" alone = weak; must reach a deterministic oracle before reporting.
- Impact statement: read access (what tables/schemas visible via `version()` + information_schema count if allowed) — but do not enumerate real customer rows. State capability, not loot.
- Never: `DROP`, `UPDATE`, `INSERT`, `LOAD_FILE`, `xp_cmdshell`, mass extraction. On sensitive programs, ask permission before even time-based tests if rules are strict.

## Tooling note
sqlmap only: (a) with explicit program allowance, (b) throttled (`--delay=1 --threads=1`), (c) targeted at ONE confirmed parameter with `--technique=B` (boolean) preferred over time-based, never `--risk=3 --level=5` blind on prod.
