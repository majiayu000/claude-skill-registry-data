---
name: wrds
description: Connect to and query WRDS (Wharton Research Data Services) from any research project. Use this skill whenever the user needs to download, query, or explore data from WRDS — including Compustat, CRSP, FactSet, I/B/E/S, or any other WRDS-hosted database. Also trigger when the user mentions WRDS tables, WRDS libraries, or wants to look up variable definitions or coverage in WRDS datasets. Do NOT trigger for general SQL or database questions unrelated to WRDS.
---

# WRDS (Wharton Research Data Services)

Reusable patterns for connecting to WRDS and querying its databases from Python.

## Prerequisites

1. Install the client library:
   ```bash
   pip install wrds
   ```

2. Credentials live in a libpq `.pgpass` file with the line format:
   ```
   wrds-pgdata.wharton.upenn.edu:9737:wrds:your_wrds_username:PASSWORD
   ```
   Point the environment variable `PGPASSFILE` at that file, or place it at the OS-default libpq location (`%APPDATA%\postgresql\pgpass.conf` on Windows, `~/.pgpass` elsewhere). Set `$WRDS_USERNAME` (or `$PGUSER`) to your account.

3. **Never hardcode passwords** in scripts, CLAUDE.md, or any version-controlled file. The `.pgpass` mechanism handles authentication automatically.

## Authentication: fail fast, never retry

WRDS locks an account after a few consecutive failed logins, and unlocking it requires a request to WRDS support. The `wrds` package makes this easy to trigger by accident. `wrds.Connection()` authenticates through the `.pgpass` file, and when that file is missing or its password has expired, the package silently falls back to an interactive `input()`/`getpass()` prompt and then retries. In an unattended agent session the prompt has no human to answer it, so the run either hangs on stdin or the attempt fails and gets repeated, where each repeat is another failed login against the account.

To prevent that, **always connect through the bundled guard `scripts/wrds_connect.py`, and never call `wrds.Connection()` directly.** The guard validates `.pgpass` offline before touching the network, suppresses the interactive prompt, makes at most one connection attempt, and on any authentication problem raises `WRDSAuthError` carrying an explanatory message rather than prompting or retrying.

When a connection raises `WRDSAuthError`, stop. Surface the message to the user and wait for them to refresh the credentials. Do not re-run the script, do not call `wrds.Connection()` as a fallback, and do not enter a password, because every retry moves the account closer to a lockout. Recovery is the user's to perform: they update the password in the file `PGPASSFILE` points to, whose single line has the form `wrds-pgdata.wharton.upenn.edu:9737:wrds:your_wrds_username:PASSWORD`.

An offline credential check, which costs zero login attempts, is worth running before a batch of WRDS work:

```bash
python ~/.claude/skills/wrds/scripts/wrds_connect.py --check
```

## Connection Pattern

```python
import os
import sys
sys.path.insert(0, os.path.expanduser("~/.claude/skills/wrds/scripts"))
from wrds_connect import connect, WRDSAuthError

try:
    db = connect()                 # one guarded attempt; account from $WRDS_USERNAME/$PGUSER
except WRDSAuthError as e:
    print(e)                       # STOP — surface to the user, do not retry
    raise
try:
    df = db.raw_sql("SELECT * FROM comp.funda LIMIT 10")
finally:
    db.close()
```

`connect()` resolves the account and the credentials file at call time, so a different login needs no code change. The account is taken from `username=`, then `$WRDS_USERNAME`, then `$PGUSER` — with none of those set the guard raises `WRDSAuthError` instead of guessing an account; the credentials file is taken from `pgpass=`, then `$PGPASSFILE`, then the OS-default libpq location. A file named explicitly, by the argument or `$PGPASSFILE`, is authoritative, so a missing path fails fast rather than silently falling back to the default account. When a password is supplied through `password=` or `$WRDS_PASSWORD`, `connect()` authenticates with the username and that password directly and the `.pgpass` file is bypassed. The function returns the ordinary `wrds.Connection` object that the rest of this skill documents.

To work as another account or against another credentials file, set the variables in the shell before invoking any WRDS script — no edit to the skill or your analysis code is required:

```powershell
$env:WRDS_USERNAME = "alice"
$env:PGPASSFILE    = "D:\creds\alice.pgpass"
python "$env:USERPROFILE\.claude\skills\wrds\scripts\wrds_connect.py" --check
```

## Using credentials supplied in chat

By default the account comes from `$WRDS_USERNAME`/`$PGUSER` with the `.pgpass` file, and a bare request such as "use the wrds skill" should use that environment unchanged. When the user instead supplies a userid and password in the request — for example, "use the wrds skill with userid `jdoe` and password `…`" — authenticate as that account for the session by passing the credentials through the environment, scoped to the command that runs the WRDS work. Shell state does not persist between separate commands here, so setting the variables inline in the same invocation keeps the password out of any file and confined to that one run:

```powershell
$env:WRDS_USERNAME = "jdoe"; $env:WRDS_PASSWORD = "<the password the user gave>"; python your_wrds_script.py
```

A username on its own, with no password, is looked up in the `.pgpass` file as usual; a supplied password switches `connect()` to direct authentication and the `.pgpass` file is bypassed. The fail-fast contract is unchanged: a wrong password counts as one failed login, and WRDS locks the account after a few, so when `connect()` raises `WRDSAuthError` here, stop and ask the user to confirm the userid and password instead of retrying. Never write the password into a script or any other file, and do not echo it back.

## Schema-peek helper

Before writing a real query against an unfamiliar WRDS table, use the bundled exploration script:

```bash
python ~/.claude/skills/wrds/scripts/peek_tables.py
```

`scripts/peek_tables.py` takes a list of `(library, table)` pairs and prints each table's column list, types, comments, and a few sample rows — far faster than navigating the WRDS web manual. Edit the `TABLES` list at the top of the script for whatever you're exploring. The default list maps the SEC Analytics Suite (DEF 14A + CIK linking tables) that this skill documents.

## Core Operations

| Operation | Method |
|-----------|--------|
| List all databases | `db.list_libraries()` |
| List tables in a database | `db.list_tables(library='comp')` |
| Describe a table's columns | `db.describe_table(library='comp', table='funda')` |
| Raw SQL query | `db.raw_sql("SELECT ...")` |
| Fetch table as DataFrame | `db.get_table(library='comp', table='funda', rows=10)` |

`raw_sql()` and `get_table()` both return pandas DataFrames. Convert to polars downstream if needed for performance.

## Available Libraries

Databases this skill documents (availability depends on your WRDS subscription; non-exhaustive):

| Library | Description |
|---------|-------------|
| `comp` | Compustat (fundamentals, segments, pricing) |
| `crsp` | CRSP (stock prices, returns, events) |
| `factset` | FactSet (ownership, fundamentals, prices) |
| `ibes` | I/B/E/S (analyst estimates, recommendations) |
| `wrdsapps` | WRDS-derived datasets (linking tables, beta suites) |
| `wrds_sec_search`, `wrdssec_all`, `wrdssec_common` | SEC EDGAR filings mirror — see "SEC Analytics Suite" below |

To discover others: `db.list_libraries()`.

## FactSet Ownership Tables

FactSet ownership tables use an `_eq` suffix for equity-specific views. These are the most commonly used:

| Table | Description |
|-------|-------------|
| `factset.own_inst_stakes_detail_eq` | Institutional position-level holdings (columns: factset_entity_id, fsym_id, as_of_date, position, indirect_options, source_code, current_flag) |
| `factset.own_stakes_detail_eq` | All ownership stakes (institutional + insider) |
| `factset.own_fund_detail_eq` | Fund-level holdings detail |
| `factset.own_sec_coverage_eq` | Security identifier concordance (fsym_id to ISIN, SEDOL, CUSIP) |
| `factset.own_sec_entity_eq` | Security-to-entity mapping |
| `factset.own_sec_prices_eq` | Security prices from FactSet |
| `factset.own_ent_institutions` | Institution metadata (name, type, country) |
| `factset.own_ent_funds` | Fund metadata |
| `factset.own_sec_13f_reportable_eq` | 13F-reportable securities |

Other useful FactSet tables (no `_eq` suffix):

| Table | Description |
|-------|-------------|
| `factset.sym_entity` | Entity master (entity names, types) |
| `factset.sym_coverage` | Symbol coverage and identifiers |
| `factset.sym_isin` | ISIN identifiers |
| `factset.sym_cusip` | CUSIP identifiers |
| `factset.sym_sedol` | SEDOL identifiers |
| `factset.sym_sec_entity` | Security-to-entity linkage |
| `factset.edm_standard_entity` | Standardized entity data |

## SEC Analytics Suite (EDGAR filings)

SEC EDGAR filings are mirrored on WRDS, with filing payloads stored in-database for the common form types. Speed comparisons with EDGAR depend on the workload and have not been benchmarked here; the SEC's current fair-access cap is 10 req/sec with a declared user agent. **Use WRDS when** the query is filtered (specific CIKs, date range, form type), you need to join filings to Compustat / CRSP / FactSet in the same database, or you want to avoid building and maintaining a rate-limited scraper. **Use EDGAR directly when** you need every filing of a given form type at scale — pair it with the SEC index files / full-index feed, on-disk caching, and compliant throttling.

| Library | What it has |
|---------|-------------|
| `wrds_sec_search` | Per-form-type tables (`filing_def`, `filing_10_k`, `filing_10_q`, `filing_8_k`, `filing_13f_hr`, `filing_sc_13d`, `filing_sc_13g`, `filing_pre`, `filing_4`, etc.) with the filing payload in a `TEXT` column and a `filing_tsv` `TSVECTOR` GIN index for full-text search. Pre-processing of the `<TEXT>` block varies by era — see warning below. Also includes `registrant` (accession × CIK × role with registrant metadata) and `filing_view` (filing-level view with a `registrants` `JSONB` column) |
| `wrdssec_all` | Master indexes across all ~27M filings. `wrds_forms` has accession-level rows (CIK, form, fdate, **`accession`**) and is the right table for accession joins. `forms` is CIK × fdate × form **without an `accession` column** — useful for time-series counts, not for joining to `filing_*` |
| `wrdssec_common` | Form-code dictionary (`sec_form_descriptions`; column is `form`) and CIK linking (`wciklink_gvkey`, `wciklink_cusip`, `wciklink_ticker`, `wciklink_names`) |

> ⚠️ **HTML preservation in `wrds_sec_search.filing_*` varies by era — sample before parsing.** Modern large filings appear stripped: Tesla 2024 DEF 14A (accession `0001104659-24-053333`, 3.2 MB) has 51 `<DOCUMENT>`/`<TEXT>` SGML wrapper tags and zero `<html>`/`<table>`/`<tr>`/`<td>`/`<p>` tags. Older filings can retain table markup: 1994-era accessions in `filing_def` (`0000890613-94-000001`), `filing_10_k` (`0000912057-94-000263`), `filing_8_k` (`0000088948-94-000001`), and `filing_sc_13d` (`0000899657-94-000005`) still contain `<TABLE>` blocks. The pre-processing rule is **not** corpus-wide. Re-run `scripts/check_html_preservation.py` against the exact table, form, and date range you intend to parse before committing.
>
> Routing by extraction goal:
> - **WRDS `filing` text** for full-text search (use the `filing_tsv` GIN index), keyword filtering, NLP, LLM-based extraction over running prose, and any task tolerant of missing HTML in the modern slice.
> - **EDGAR raw HTML** (e.g. via `edgartools`) when you need DOM structure — Item 403 ownership tables, exec-comp tables, footnote-to-row anchors — and your sample shows the WRDS slice is stripped.
> - **Hybrid**: use WRDS as a filtered accession index (form / date / CIK / FTS), fetch only the filings you actually parse from EDGAR.

**Proxy statements (DEF 14A)** live in `wrds_sec_search.filing_def` — 196K DEF 14A filings, 1994 → present. All DEF variants (DEFA14A additional, DEFM14A merger, DEFC14A contested, DEFR14A revised, DEFS14A special-meeting, DEFN14A non-management) share this table; filter on `form`. Preliminary proxies (PRE 14A and variants) are in `wrds_sec_search.filing_pre`.

```python
# WRDS as filterable index — cheap, fast, joinable to Compustat/CRSP
accessions = db.raw_sql("""
    SELECT f.accession, r.cik, r.role, f.filing_date
    FROM wrds_sec_search.filing_def AS f
    JOIN wrds_sec_search.registrant AS r ON f.accession = r.accession
    WHERE f.form = 'DEF 14A' AND f.filing_date >= '2020-01-01'
""")
# Then fetch raw HTML from EDGAR by accession for each row that needs parsing.
```

`wrds_sec_search.filing_*` tables do not expose `cik` as a SQL column. Three routes to attach CIK, in preference order:
1. **`wrds_sec_search.registrant`** (preferred) — clean `(accession, cik, role)` triples with registrant metadata.
2. **`wrds_sec_search.filing_view.registrants`** — `JSONB` array of registrants per filing; flatten with `jsonb_array_elements`.
3. **`wrdssec_all.wrds_forms`** (fallback) — works syntactically (`TEXT` ↔ `VARCHAR(20)` on `accession`), but is many-to-many for material cases: ~6,000 of ~357K `filing_def` accessions match multiple `wrds_forms` rows (max observed ≈110 CIK rows for a single accession), and ~37 very recent accessions can be missing from `wrds_forms` entirely. Use only if (1) and (2) don't cover the rows you need, and aggregate with `DISTINCT` or pick a single registrant role.

### Linking CIK to firm-level identifiers — `wrdssec_common.wciklink_*`

WRDS maintains the canonical CIK crosswalks. Build your panel against these tables rather than fuzzy-matching company names; they track mergers, name changes, and the historical identifier coverage that pure name matching does not. (CIKs themselves are unique per filer per SEC policy — these tables resolve identifier *changes over time*, not CIK reuse.)

| Table | Maps CIK to | Key columns | Approx. rows (as of 2026-05) |
|-------|-------------|-------------|------------------------------|
| `wciklink_gvkey` | Compustat `gvkey` (+ per-form filing counts: `n10k`, `ndef`, `n8k`, `n13d`, `n13g`, `n13f`, ...) | `cik`, `gvkey`, **`source`**, **`link_desc`**, `sec_start_date` / `sec_end_date`, `link_start_date` / `link_end_date` | ~1.07M rows total — but **many are `link_desc = 'No Link'` with `gvkey IS NULL`**; filter accordingly |
| `wciklink_cusip` | 8- and 9-digit CUSIP (+ `validated` quality flag 0–3) | `cik`, `cusip`, `cusip_full`, `validated`, `cikdate1` / `cikdate2` | ~85K |
| `wciklink_ticker` | Ticker symbol | `cik`, `ticker`, `ftdate` / `ltdate` | ~34K |
| `wciklink_names` | `gvkey`, `cusip`, `ticker`, `company_name` together in one row with per-identifier date ranges | per-identifier `first_*_date` / `last_*_date` | ~1.2M |

Practical gotchas:
- **CIK format**: 10-character zero-padded string (e.g. `'0000001750'`).
- **`wciklink_gvkey` row inflation**: one `(cik, gvkey)` pair can have several rows from different `source` values (sample CIK `0000001750` returns multiple rows on a single date). Aggregate with `DISTINCT` on `(cik, gvkey)` or pick a single `source`/`link_desc` your project trusts. Always require `gvkey IS NOT NULL`.
- **Two date pairs, two meanings**: `link_start_date` / `link_end_date` are the link source's validity window; `sec_start_date` / `sec_end_date` are when the CIK actually filed. For filings-to-fundamentals work, key off the SEC dates so the link covers the actual filing date.

```python
# CIK -> gvkey: distinct valid links covering a filing date
db.raw_sql("""
    SELECT DISTINCT cik, gvkey, source, link_desc,
                    sec_start_date, sec_end_date
    FROM wrdssec_common.wciklink_gvkey
    WHERE cik = '0000001750'
      AND gvkey IS NOT NULL
      AND DATE '2022-06-30' BETWEEN COALESCE(sec_start_date, DATE '1900-01-01')
                              AND COALESCE(sec_end_date, CURRENT_DATE)
""")
```

For CRSP `permno`, go gvkey → permno via the standard CRSP-Compustat link (CCM `lnkhist`).

## Index constituents: `comp.idxcst_his` holds only CURRENT members

Verified 2026-07-21 (Specialist Directors project): on this WRDS deployment,
`comp.idxcst_his` for the S&P 500 (`gvkeyx='000003'`, confirmed via `comp.idx_index`)
returns only the ~503 current constituents — every `thru` is null, so it carries no
historical join/leave spells. For historical index membership use
**`crsp.msp500list`** (~2,064 spells with real start/end dates) and map
permno → gvkey through the CCM link `crsp.ccmxpf_lnkhist`
(`linktype IN ('LU','LC')`, `linkprim IN ('P','C')`, date-window overlap).
CRSP's "still a member" sentinel is an end date equal to the file end — convert it
to null rather than treating it as an exit. Pre-Compustat-era permnos (~176, back
to 1925) have no gvkey link; keep them with null gvkey. Note also:
`comp.company` has **no `tic` column** here — tickers live in `comp.security`
(prefer `iid='01'`, `secstat='A'`).

## Best Practices

- **Filter in SQL, not in Python.** Always push country, date, and identifier filters into the SQL query to minimize data transfer. WRDS queries over the network are slow for large tables — pulling millions of rows and filtering locally wastes time.

- **Cache downloads as parquet.** Save query results to `data/processed/wrds/` (or an equivalent project-specific path) as `.parquet` files. Include a `downloaded_date` column or note in the filename so you know when the data was fetched. Do not re-download data that hasn't changed.

- **Close connections.** Call `db.close()` when finished. WRDS may terminate idle sessions, and leaving connections open ties up limited slots.

- **Use `raw_sql()` for anything non-trivial.** `get_table()` is convenient for quick peeks, but `raw_sql()` gives full control over joins, filters, and aggregation — use it for real queries.

## Example: Download FactSet Institutional Holdings

```python
import os
import sys
import polars as pl
from datetime import date

sys.path.insert(0, os.path.expanduser("~/.claude/skills/wrds/scripts"))
from wrds_connect import connect, WRDSAuthError

try:
    db = connect()
except WRDSAuthError as e:
    print(e)            # STOP — do not retry on auth failure
    raise

try:
    df = db.raw_sql("""
        SELECT a.fsym_id, a.factset_entity_id, a.as_of_date,
               a.position, a.source_code, a.current_flag,
               b.proper_name
        FROM factset.own_inst_stakes_detail_eq AS a
        LEFT JOIN factset.own_ent_institutions AS b
            ON a.factset_entity_id = b.factset_entity_id
        WHERE a.as_of_date >= '2023-01-01'
        LIMIT 1000
    """)
finally:
    db.close()

# Convert to polars and save
result = pl.from_pandas(df).with_columns(
    pl.lit(date.today().isoformat()).alias("downloaded_date")
)
result.write_parquet("data/processed/wrds/factset_inst_holdings.parquet")
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Connection refused / auth error | The guarded `connect()` raises `WRDSAuthError` and stops after one attempt — do not retry, because repeated failed logins can lock the account. Refresh the password in the `.pgpass` file `PGPASSFILE` points to, run `wrds_connect.py --check` to confirm it offline, then re-run once. See "Authentication: fail fast, never retry" above |
| Session timeout | Reconnect — WRDS drops idle connections after a while |
| Permission denied on a table | That table requires a subscription your institution may not have. Check the WRDS web interface to confirm access |
| Slow query | Add tighter date/country filters, or download in chunks by year |
| LIKE pattern fails with `immutabledict is not a sequence` or returns nothing | `pandas.read_sql_query` (used by `raw_sql`) treats `%` as parameter substitution. Two fixes: (a) escape literally in the SQL string as `'%%foo%%'`, or (b) safer — bind the pattern as a parameter: `db.raw_sql("... WHERE x LIKE %(p)s", params={'p': '%foo%'})` |
