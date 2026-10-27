---
name: macro-monitor
description: What is moving in the macro picture? Geopolitical/macro market indicators. Use when (1) China/US Treasury dynamics, (2) dollar-yield divergence, (3) Brent crude oil / energy price spikes, (4) geopolitical market risk, (5) one-command crisis check. NOT for stock analysis or fundamentals.
---

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.

# Macro Monitor - Geopolitical Financial Checklist

## Purpose

Structured monitoring of macro/geopolitical financial indicators using **free public data sources**.

## Quick Checklist

### 1. Foreign Treasury Holdings (Monthly)

**Source:** Treasury TIC Data (https://ticdata.treasury.gov/Publish/mfh.txt)

**What to check:**
- China holdings level (normal: $700B-$1.3T)
- Japan holdings level (normal: $1.0T-$1.3T)
- Month-over-month change
- Trend direction over 6 months

**Red flags:**
- Drop >$50B in single month
- China drops below $600B
- Coordinated selling (China + Japan both selling)
- A drop is consistent with selling *and* with relocation to a custodian this series cannot see — read "Before Reading a Trend" below before escalating.

### 2. Dollar Index vs 10Y Yield (Daily)

**Sources:**
- DXY: FRED series DTWEXBGS (https://fred.stlouisfed.org/series/DTWEXBGS)
- 10Y: FRED series DGS10 (https://fred.stlouisfed.org/series/DGS10)

**Normal behavior:** Higher yields → stronger dollar

**Red flag patterns:**
| Yields | Dollar | Interpretation |
|--------|--------|----------------|
| Up | Down | Confidence crisis - foreign selling |
| Down | Down | Flight from US assets |
| Up | Up | Normal - higher rates attract capital |

**Critical divergence:** Yields rising + Dollar falling = investigate immediately

### 3. Central Bank Gold (Monthly)

**Source:** World Gold Council or PBOC announcements

**What to check:**
- PBOC monthly gold purchases
- Cumulative central bank buying
- Gold price trend vs dollar

**Red flags:**
- PBOC buying >20 tonnes/month sustained
- Multiple central banks buying simultaneously
- Gold rising despite dollar strength

### 4. Yield Curve (Daily)

**Source:** FRED series T10Y2Y (https://fred.stlouisfed.org/series/T10Y2Y)

**What to check:**
- 10Y-2Y spread
- Inversion status
- Duration of inversion

**Warning levels:**
| Spread | Status |
|--------|--------|
| >100bp | Normal, healthy |
| 0-50bp | Flattening, watch closely |
| <0bp | Inverted - recession signal |

## Data Retrieval

### Automated Scripts

**FRED data:** `python3 scripts/fred_fetcher.py [series_id|snapshot|divergence|crisis]`
- `snapshot` — all 7 macro series (Treasury, dollar, VIX, Fed funds, Brent, EUR, yield curve)
- `divergence` — yield-dollar divergence check with interpretation
- `crisis` — red flag alert check (Brent >$120, VIX >35, 10Y >5%, yield curve inverted, USD/EUR >1.20)
- `[SERIES_ID]` — latest value for any FRED series

**TIC data:** `python3 scripts/tic_parser.py`

### Manual Quick Check

```bash
# Get latest 10Y yield
curl -s "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10" | tail -5

# Get latest dollar index
curl -s "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTWEXBGS" | tail -5
```

## Interpretation Framework

### Before Reading a Trend

- **What can this instrument not see, and is the claim exactly that?** A
  network's own share counts only traffic on that network; a custodian's
  holdings count only what sits with that custodian. A fall in either is
  consistent with retreat and with migration — the instrument cannot separate
  the readings (observed twice: 2026-09-16, SWIFT's RMB share; 2026-09-25, NY
  Fed foreign-official custody, flat through a yield spike).
- **Whose records could separate them, and in what language?** Name the party
  and the language in the report's limits even when unreached — the SWIFT case
  was partly resolved only by PBoC/SAFE settlement data, in Chinese.
- **Did the series' definition move?** Before reading a level shift as a trend,
  check the method notes for threshold, perimeter, unit or base changes
  (iterative-verification, Definition-Drift Check).

### Growth vs Value Sensitivity

**Growth stocks** (tech, high P/E):
- More sensitive to rate increases
- Future cash flows discounted at higher rates
- Sell on yield spikes

**Value stocks** (utilities, banks):
- Less rate-sensitive
- Banks may benefit from higher rates
- More defensive in rate environment

### Sector Impact Matrix

| Indicator | Tech Impact | Bank Impact | Utility Impact |
|-----------|-------------|-------------|----------------|
| Yields up | Negative | Positive | Negative |
| Dollar up | Mixed (int'l) | Positive | Neutral |
| Gold up | Neutral | Neutral | Defensive signal |
| TIC selling | Negative | Negative | Defensive demand |

## When to Escalate

**Immediate attention required if:**
1. Dollar-yield divergence >3 days
2. China TIC drop >$50B in month
3. Multiple indicators red simultaneously
4. Pattern resembles April 2025 event

## Reference Materials

See `reference/` subdirectory for:
- Historical divergence patterns
- Detailed indicator documentation
- Source URLs and update schedules

---

**Update frequency:** Check TIC monthly (mid-month release), FRED daily for divergence monitoring.
