---
name: public-equity-research
description: Perform recommendation-grade research on a named listed company using exact security identity, point-in-time primary filings, business/segment economics, earnings quality, balance sheet, cash flow, dilution, management/governance, industry/competition, valuation, what is priced in, catalysts, revisions, risks, and falsifiable thesis criteria. Use for company/hisse fundamental analysis, earnings and valuation, or Turkish intents such as “şirketi/hisseyi derin analiz et”, “bilanço ve değerleme”, “adil değer”, “yatırım tezi”, “KAP/10-K sonuçları”, “bu hisse neden alınır/satılır”. For open-ended “which stock” requests, route through the broad equity funnel first; never infer a market-wide winner from one company analysis.
---

# Public Equity Research

Own deep research on a named public company and its exact listed security. Use the user's language and distinguish business quality, security valuation/readiness and portfolio action.

Read [references/equity-research-protocol.md](references/equity-research-protocol.md). If the installed `$public-equity-investing` plugin is available, use its narrow earnings, valuation, scenario or thesis workflows to deepen this protocol; if unavailable, complete the same evidence categories directly from current primary filings and authoritative sources.

## Workflow

1. **Resolve identity and cutoff.** Confirm legal issuer, ticker, exchange, security/share class, currency, ADR/depositary ratio, fiscal calendar and data cutoff. Separate company value from the exact security claim.
2. **Build the source ledger.** Start with current annual/interim filings, earnings release, notes, investor presentation only as management claims, exchange/regulator disclosures and official share/capital records. Apply `$finance-evidence-guard` to decisive figures.
3. **Understand the business.** Map segments, customers, geography, revenue drivers, unit economics, pricing, cyclicality, competitive position, capital intensity, regulation and key dependencies.
4. **Normalize financials.** Reconcile accounting basis, currency, consolidation, inflation treatment, fiscal periods, acquisitions/disposals, one-offs, stock compensation, leases, capitalized costs and continuing operations. Build revenue, margin, cash conversion, returns on capital, leverage and dilution trends.
5. **Test earnings quality and balance sheet.** Compare profit with operating/free cash flow, working capital, capex, receivables/inventory, provisions, related parties, refinancing, covenants, pension/off-balance-sheet obligations and contingent liabilities.
6. **Estimate what is priced in.** Use at least two compatible valuation frames—such as historical/peer multiples, reverse DCF, unit economics or asset value. Make assumptions visible, use scenario ranges and show the breakpoints that explain the current price.
7. **Define thesis and variant.** State what consensus/price appears to assume, why the evidence differs, dated catalysts/recognition path, KPIs, strongest contradiction and hard kill criteria. Route persistent monitoring to `$investment-thesis-tracker`.
8. **Add market context.** Use `$technical-quant-analysis` for timing, `$market-regime-analysis` for cross-asset context, and `$probabilistic-market-forecast` for outcome ranges. Use `$turkey-markets-analysis` for BIST/KAP/TMS 29/Türkiye rules.
9. **Challenge and decide.** Compare a relevant peer/alternative and doing nothing, then run `$investment-red-team`. Use `$portfolio-risk-and-sizing` for allocation and `$pre-trade-investment-gate` if action is imminent.

## Hard rules

- An open-ended “best stock” claim must start with `$equity-opportunity-funnel`; a named-company report cannot establish a market-wide winner.
- Do not treat management guidance, analyst targets or investor presentations as independent proof.
- Do not mix periods, currencies, consolidated bases, reported/adjusted metrics or nominal/real figures silently.
- Do not hide dilution, leverage, cyclicality, governance, liquidity or valuation sensitivity behind a narrative moat.
- Do not convert a precise spreadsheet output into precise confidence; ranges must reflect model and evidence uncertainty.

## Output

Lead with action or research verdict, horizon, current price/time and confidence. Then show identity, business/segments, normalized financial trends, earnings quality/balance sheet, valuation and what is priced in, bear/base/bull cases, catalysts, contradictions/kill criteria, peer/alternative, technical/regime context when material, portfolio/execution conditions and source ledger.
