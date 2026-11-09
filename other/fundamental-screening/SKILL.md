---
name: fundamental-screening
description: |
  Fundamental and governance screening of Indian listed companies in the style of Screener.in:
  valuation (P/E, P/B, EV/EBITDA, PEG vs history and peers), quality (ROCE, ROE, cash conversion,
  debt), growth, sector-specific metrics (banks, NBFCs, IT, FMCG, manufacturing), shareholding pattern
  (promoter, FII, DII, pledge), quarterly results reading, and India-specific red flags (promoter
  pledging, related-party transactions, auditor exits, surveillance lists, SME and operator stocks).

  Use when the user asks: "is X fundamentally strong", "valuation of X", "should I invest long term in
  X", "compare X vs Y", "analyse quarterly results", "promoter pledge / holding", "red flags in X", or
  wants a quality filter before a positional trade.
---

# Fundamental Screening (India)

Technicals decide **when**; fundamentals decide **whether to hold for long**. Screen for quality and
red flags first. Valuation only matters once those pass.

## Where to get data

- **Company filings** on nseindia.com and bseindia.com: quarterly results (due within 45 days of
  quarter end, 60 days for Q4), shareholding pattern (within 21 days of quarter end), annual reports,
  investor presentations, concall transcripts, and SAST/pledge disclosures.
- **Aggregators:** Screener.in (ratios, 10-year financials, peer tables), Trendlyne, Tickertape,
  Moneycontrol. Fetch with WebFetch and cite the page and date.
- **Broker MCPs** generally give prices and holdings, not financials.
- Always state the period: TTM, FY26, or Q2 FY27 (India's FY runs April–March; Q2 FY27 = Jul–Sep 2026).

## 1. Quality (pass at least 4 of 6 for a "quality" tag)

| Metric | Good | Notes |
|---|---|---|
| ROCE (5-yr avg) | > 15% | Use ROE for banks/NBFCs |
| Operating cash flow / net profit (5-yr) | > 80% | Low means profits aren't converting to cash |
| Debt / equity | < 0.5 (non-financials) | Interest coverage > 4× |
| Sales growth (5-yr CAGR) | > 10% | Compare with India's nominal GDP growth |
| Profit growth (5-yr CAGR) | ≥ sales growth | Watch "other income"-driven profits |
| Promoter holding | Stable/rising, pledge ≈ 0% | Pledge > 20% of promoter stake is a red flag |

## 2. Valuation (relative, never absolute)

- P/E vs the company's own 5- and 10-year median and vs 3–5 listed peers. PEG = P/E ÷ EPS growth (%).
- **Banks/NBFCs:** P/B and P/ABV with ROA > 1.2%, GNPA/NNPA trend, credit cost, NIM, CASA ratio
  (banks), capital adequacy > 15%.
- **IT services:** constant-currency revenue growth, EBIT margin, deal TCV, attrition, US exposure.
- **FMCG/consumer:** volume growth vs price growth, gross margin vs raw materials, distribution reach.
- **Capital goods/infra:** order book ÷ revenue (years of visibility), working-capital days, execution.
- **Cyclicals (metals, cement, chemicals):** use EV/EBITDA through the cycle. Low P/E at peak earnings
  is a trap.

## 3. Shareholding pattern (quarterly)

| Signal | Reading |
|---|---|
| Promoter stake rising (open-market buys) | Insider confidence |
| Promoter stake falling via OFS/blocks | Check the reason: debt repayment vs exit |
| **Pledged shares rising** | Margin-call risk on a price fall; forced selling spirals |
| FII + DII (MF) stake rising | Institutional accumulation |
| Retail/public share rising while price rises | Late-stage retail chase; caution |

## 4. Red flags (any one is serious)

- Promoter **pledge** above about 20%, or pledge invocations.
- **Auditor resignation** or qualified opinion, or frequent changes of auditor or CFO.
- Large **related-party transactions**, loans to promoter entities, complex subsidiary webs.
- Receivables or "other current assets" growing much faster than sales. Repeated "exceptional items".
- Persistent negative operating cash flow with reported profits.
- Frequent equity dilution: preferential allotments, warrants to promoters at low prices.
- Inclusion in **ASM/GSM/ESM** surveillance, trade-for-trade series (BE/BZ), or a 2%/5% price band.
- SEBI, ED, SFIO or tax actions. Delayed results filings.
- **Operator/tip-stock pattern:** tiny free float, upper-circuit streaks, volume spikes with no news,
  Telegram/WhatsApp promotion, an SME listing at an extreme multiple.

## 5. Reading quarterly results

1. YoY first (seasonality), then QoQ. Separate revenue growth into volume and price where disclosed.
2. EBITDA margin trend and its drivers: raw materials, employee cost, pricing.
3. Strip out one-offs (exceptional items, tax write-backs, other income spikes).
4. Compare with consensus if available (news), management guidance, and the previous concall.
5. Note the price reaction. A good result with a falling price means expectations were higher.

## Output

```markdown
# [Company] — fundamental screen ([data period], sources)
Verdict: [Quality compounder | Fair | Cyclical | Speculative | Avoid] — one line why
| Quality | Value | Pass? |
...
Valuation: P/E x vs 5-yr median y, peers z → [cheap/fair/rich]
Shareholding: promoter a% (pledge b%), FII c%, DII d% — trend
Red flags: none / [list]
What to watch: next results date, guidance items, risks
```
State that this is not investment advice, and that fundamentals inform long-term holding, not
short-term price moves.
