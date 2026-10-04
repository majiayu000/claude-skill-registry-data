---
name: evo-sec13f-analyzer
description: Toolkit for parsing SEC Form 13F-HR quarterly TSV datasets. Loads COVERPAGE/INFOTABLE/SUMMARYPAGE with safe dtypes (CUSIPs as zero-padded strings, VALUE as numeric dollars), fuzzy-matches fund manager names with RapidFuzz, retrieves fund AUM, deduplicates equity holdings (filtering options), compares holdings across quarters, and ranks top holders of a given CUSIP. Use whenever working with /root/2025-qN 13F TSV files.
---

# evo-sec13f-analyzer

Utilities for SEC Form 13F-HR quarterly TSV analytics.

## Key facts
- SEC EDGAR Release 22.4.1 (Jan 3, 2023): VALUE column is in **exact dollars** (multiplier = 1) for all filings from 2023 onward. Use `value_multiplier=1` for the 2025-q2 / 2025-q3 data in this task.
- CUSIP is a 9-char alphanumeric. Always load as string and zero-pad to length 9 to preserve leading zeros (Apple = `037833100`).
- TSV columns: tab-delimited, UTF-8.
- `PUTCALL` blank = equity; `PUT` / `CALL` = options. Exclude options when counting equity positions.
- AUM (gross portfolio value) lives in `SUMMARYPAGE.TABLEVALUETOTAL`. Number of equity positions (unique CUSIPs) is computed from INFOTABLE.
- Fund manager names vary in casing/punctuation. Use RapidFuzz `process.extract` with `fuzz.WRatio` and `utils.default_process` for entity resolution against `COVERPAGE.FILINGMANAGER_NAME`.

## Importing

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-sec13f-analyzer/scripts')
from utils import (
    load_coverpage, load_infotable, load_summarypage,
    fuzzy_find_manager, get_fund_aum, get_fund_holdings,
    compare_holdings, top_holders_of_cusip, find_cusip_for_issuer,
)
```

## Typical workflow

```python
cp_q3 = load_coverpage('/root/2025-q3/COVERPAGE.tsv')
it_q3 = load_infotable('/root/2025-q3/INFOTABLE.tsv')
sp_q3 = load_summarypage('/root/2025-q3/SUMMARYPAGE.tsv')

# Q1: fund AUM via fuzzy match
matches = fuzzy_find_manager(cp_q3, 'renaissance technologies', top_n=5)
accn = matches.iloc[0]['ACCESSION_NUMBER']
aum = get_fund_aum(sp_q3, accn)

# Q2: number of stocks held
holdings = get_fund_holdings(it_q3, accn)
n_stocks = len(holdings)

# Q3: top buys delta
holdings_q2 = get_fund_holdings(it_q2, accn_q2)
holdings_q3 = get_fund_holdings(it_q3, accn_q3)
deltas = compare_holdings(holdings_q2, holdings_q3)
top_buys_cusips = deltas.head(5)['CUSIP'].tolist()

# Q4: top holders of a CUSIP
plt_cusip = '69608A108'  # Palantir Class A
top3 = top_holders_of_cusip(it_q3, cp_q3, plt_cusip, n=3)
```

## Functions (scripts/utils.py)
- `load_coverpage(filepath)` — read COVERPAGE.tsv as strings; uppercase column names.
- `load_infotable(filepath, value_multiplier=1)` — read INFOTABLE.tsv; zero-pad CUSIP; coerce VALUE/SSHPRNAMT.
- `load_summarypage(filepath, value_multiplier=1)` — read SUMMARYPAGE.tsv; coerce TABLEVALUETOTAL.
- `fuzzy_find_manager(coverpage_df, query, top_n=5)` — RapidFuzz WRatio entity resolution.
- `get_fund_aum(summarypage_df, accession_number)` — TABLEVALUETOTAL for accession.
- `get_fund_holdings(infotable_df, accession_number, exclude_options=True)` — deduped CUSIP-level holdings.
- `compare_holdings(h_q1, h_q2)` — outer-merge on CUSIP; compute VALUE_DELTA, SHARES_DELTA.
- `top_holders_of_cusip(infotable_df, coverpage_df, cusip, n=3)` — top filers by aggregate VALUE for that CUSIP.
- `find_cusip_for_issuer(infotable_df, issuer_substr)` — substring search for CUSIPs by issuer name.
