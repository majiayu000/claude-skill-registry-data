---
name: web-search-finance
description: Fetch public financial data using Python requests from SEC EDGAR, Yahoo Finance, and other free sources. Use when tasks require online lookup of financial statements, stock data, or market figures.
---

# Web Search for Finance Data

The container has internet access. Use Python `requests` to fetch data. Do NOT use fake URLs like `api.example.com`.

## WebFetch is disabled

**Do not use WebFetch.** It is blocked in this environment because Claude Code's WebFetch can hang forever with no timeout (upstream bug). Use **Bash + Python `requests`** with explicit `timeout=10` (or `curl --max-time 30`) instead. WebSearch is still available for discovery, but prefer direct API calls below once you know the data source.

## 1. SEC EDGAR — Financial Statements (US public companies)

```python
import requests, json

# Step 1: Get company CIK from ticker
ticker = "HD"  # The Home Depot
r = requests.get(
    f"https://efts.sec.gov/LATEST/search-index?q=%22{ticker}%22&dateRange=custom&startdt=2024-01-01&enddt=2025-01-01&forms=10-K",
    headers={"User-Agent": "research@example.com"}
)

# Better: use the company tickers JSON
r = requests.get("https://www.sec.gov/files/company_tickers.json",
                 headers={"User-Agent": "research@example.com"})
tickers = r.json()
# Find by ticker symbol
cik = None
for entry in tickers.values():
    if entry['ticker'].upper() == ticker.upper():
        cik = str(entry['cik_str']).zfill(10)
        break
print("CIK:", cik)

# Step 2: Get company facts (all financial data)
r = requests.get(
    f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json",
    headers={"User-Agent": "research@example.com"}
)
facts = r.json()

# Step 3: Extract specific metric, e.g. Cost of Goods Sold
cogs = facts['facts']['us-gaap'].get('CostOfGoodsSoldAndServicesSold') or \
       facts['facts']['us-gaap'].get('CostOfRevenue') or \
       facts['facts']['us-gaap'].get('CostOfGoodsSold')
if cogs:
    for entry in sorted(cogs['units']['USD'], key=lambda x: x.get('end',''), reverse=True):
        if entry.get('form') == '10-K' and entry.get('fp') == 'FY':
            print(entry['end'], entry['val'])
            break

# Common GAAP tags:
# Revenues / RevenueFromContractWithCustomerExcludingAssessedTax
# CostOfGoodsSoldAndServicesSold / CostOfRevenue
# InventoryNet
# NetIncomeLoss
# OperatingIncomeLoss
# Assets / Liabilities / StockholdersEquity
```

## 2. Yahoo Finance — Quick price/fundamentals lookup

```python
import requests

def yf_get(ticker, module="incomeStatementHistory"):
    url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}"
    r = requests.get(url, params={"modules": module},
                     headers={"User-Agent": "Mozilla/5.0"})
    return r.json()["quoteSummary"]["result"][0][module]

# Income statement (annual)
income = yf_get("HD", "incomeStatementHistory")
for stmt in income["incomeStatementHistory"]:
    print(stmt["endDate"]["fmt"],
          "Revenue:", stmt.get("totalRevenue", {}).get("raw"),
          "Net Income:", stmt.get("netIncome", {}).get("raw"))

# Balance sheet
balance = yf_get("HD", "balanceSheetHistory")
for stmt in balance["balanceSheetStatements"]:
    print(stmt["endDate"]["fmt"],
          "Inventory:", stmt.get("inventory", {}).get("raw"))

# Key stats (market cap, P/E, etc.)
stats = yf_get("HD", "defaultKeyStatistics")
```

## 3. World Bank — Macro data (GDP, CPI, gross savings, etc.)

```python
import requests

# GDP current USD: NY.GDP.MKTP.CD | CPI: FP.CPI.TOTL.ZG | Gross savings % GDP: NY.GNS.ICTR.ZS
def wb_get(country, indicator, start=2020, end=2024):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
    r = requests.get(
        url,
        params={"format": "json", "date": f"{start}:{end}", "per_page": 100},
        timeout=10,
    )
    r.raise_for_status()
    data = r.json()[1]
    return {d["date"]: d["value"] for d in data if d["value"] is not None}

gdp = wb_get("US", "NY.GDP.MKTP.CD")
cpi = wb_get("US", "FP.CPI.TOTL.ZG")
savings = wb_get("CN", "NY.GNS.ICTR.ZS", start=2001, end=2010)

# Multi-country scan (e.g. "savings > 35% every year 2001-2010"):
def wb_countries_above_threshold(indicator, years, threshold):
    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
    r = requests.get(
        url,
        params={
            "format": "json",
            "date": f"{min(years)}:{max(years)}",
            "per_page": 20000,
        },
        timeout=30,
    )
    r.raise_for_status()
    rows = r.json()[1]
    by_country = {}
    for row in rows:
        if row["value"] is None:
            continue
        by_country.setdefault(row["country"]["value"], {})[row["date"]] = row["value"]
    year_set = {str(y) for y in years}
    hits = []
    for name, series in by_country.items():
        if year_set <= set(series.keys()) and all(series[y] > threshold for y in year_set):
            hits.append(name)
    return sorted(hits)

# wb_countries_above_threshold("NY.GNS.ICTR.ZS", range(2001, 2011), 35)
```

## 4. FRED (Federal Reserve) — Interest rates, economic series

```python
import requests

# Free API, no key needed for most series
def fred_get(series_id, start="2020-01-01"):
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
    r = requests.get(url, params={"id": series_id, "vintage_date": start})
    lines = r.text.strip().split('\n')
    return dict(line.split(',') for line in lines[1:] if '.' in line.split(',')[1])

# Common series: FEDFUNDS, DGS10, CPIAUCSL, GDP, UNRATE, T10Y2Y
rates = fred_get("FEDFUNDS")
```

## 5. When data is unavailable — use reasonable estimates

If all sources fail for a specific number (e.g. private market size data):
```python
# State the source and use a published estimate
market_data = {
    "us_home_improvement_market_2023_usd_bn": 567,   # HIRI / Statista estimate
    "us_home_improvement_market_2024_usd_bn": 589,
    "source": "Home Improvement Research Institute (HIRI) 2024 report estimate"
}
```

## Quick Reference: Common Tickers & CIKs

| Company | Ticker | Common use |
|---------|--------|-----------|
| Home Depot | HD | Retail, inventory |
| Apple | AAPL | Tech, cash flow |
| Microsoft | MSFT | SaaS metrics |
| Tesla | TSLA | Auto, capex |
| Micron | MU | Semiconductor |

## Error Handling

```python
try:
    r = requests.get(url, headers={"User-Agent": "research@example.com"}, timeout=10)
    r.raise_for_status()
    data = r.json()
except Exception as e:
    print(f"Fetch failed: {e}")
    # Fall back to hardcoded estimate with source citation
```
