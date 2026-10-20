---
name: finance-pro-playbooks
description: "\"Comprehensive workflow guide for ANY finance, investing, or company analysis task. MUST read for: (1) General investment research — analyzing stocks/companies, reading earnings/filings, fetching financial data, or researching industries; (2) Professional IB/PE/VC tasks — valuation & modeling (DCF/LBO/comps), deal structuring, due diligence, M&A materials (teaser/CIM), and IC memos. Encodes professional data-sourcing rules (source hierarchy, fiscal-period discipline), silent industry defaults, and deliverable formatting standards; for finance Excel outputs its formats/excel_standards.md supersedes generic spreadsheet skills (e.g., excel-generator). DO NOT use for: quant trading system development, legal dispute calculations, or personal tax filing.\""
compatibility: opencode
---

# Finance Pro Playbooks

Turn any finance request—from a broad "analyze this stock's earnings" to a specific "build an LBO with an earnout"—into an analyst-grade deliverable. This skill enforces correct data sourcing, applies silent industry-standard assumptions, and ensures professional formatting, bridging the gap between general AI and experienced IB/PE/VC analysts.

## Workflow Overview

Every finance task follows this spine:

```
1. Resolve entities → build Entity Card (mandatory first step for any named company/fund)
2. Route the request → look up the task in the ROUTING MAP below → read the matching files
3. Gate if divergent → confirm scope/assumptions with user BEFORE building (TAM boundaries, buyer criteria)
4. Fetch data → anchor the reference date, then follow the data-source routing pipeline + source hierarchy + data-trap rules below
5. Build deliverable → follow formatting standards (if applicable)
6. Verify → run the domain's sanity checks; every hardcoded number must trace to a source
7. Deliver → state which silent defaults were applied so the user can override
```

## Step 1: Entity Resolution (Mandatory)

Before fetching any data for a named company/fund, build an **Entity Card** and save it to a working file (e.g., `entity_card.md`). Reuse it throughout the task.

| Field | Why it matters |
| --- | --- |
| Legal / common name | Disambiguate (Alphabet vs Google; similarly-named companies) |
| Ticker + exchange(s) | Anchor for prices/multiples; note dual listings (ADR/H-share/A-share) |
| Listing status | Public / private / delisted / pre-IPO — determines data routing |
| **Fiscal year end month** | THE anchor against filing-date vs fiscal-period confusion (e.g., NVDA FY ends late Jan; AAPL late Sep) |
| Reporting currency & unit | Prevent currency/scale mismatches ($M vs $B) |
| Industry classification | Drives valuation method and multiple selection |

For IPO/S-1 questions: never trust training memory about listing status — check the regulator's filing database (S-1/F-1/424) directly.

## Step 2: ROUTING MAP (Core)

Match the user's intent to a specific task and read the required files. **Do not guess; read the files exactly as instructed.**

| If the user wants to… | Task (Section) | Read File | Also Read |
| --- | --- | --- | --- |
| **Understand a market / industry** | | | |
| understand an industry, sector overview | Industry Primer | `references/market_research.md` | — |
| size a market ("how big is…", TAM/SAM/SOM) | Top-Down TAM Sizing / Bottom-Up TAM Sizing | `references/market_research.md` | — |
| map competitors / who plays in this space | Market Map | `references/market_research.md` | — |
| catch up on sector news | Industry Primer (news section) or Adverse Media Screen | `references/market_research.md` or `references/company_analysis.md` | — |
| **Understand a company** | | | |
| analyze latest earnings / "how did X do" | Earnings Update | `references/company_analysis.md` | — |
| compile public docs / background pack | Public Information Book (PIB) | `references/company_analysis.md` | — |
| check red flags on a company/person | Adverse Media Screen | `references/company_analysis.md` | — |
| quick company profile / tear sheet | Earnings Update + Public Information Book (PIB) (light) | `references/company_analysis.md` | — |
| assess AI disruption exposure | AI Disruption Assessment | `references/company_analysis.md` | — |
| **Find companies** | | | |
| find/screen private companies by criteria | Private Company Screening | `references/company_analysis.md` | `formats/excel_standards.md` (if Excel out) |
| **Value a company** ("what is X worth") | | | |
| intrinsic valuation, DCF | DCF Model | `references/valuation.md` | `formats/excel_standards.md` + `formats/metric_disambiguation.md` |
| value vs peers, trading multiples | Public Comps | `references/valuation.md` | Same as above |
| value vs past deals, M&A multiples | Precedent Transactions | `references/valuation.md` | Same as above |
| value conglomerate by segments | SOTP Valuation | `references/valuation.md` | Same as above |
| share count, dilution math | Fully Diluted Share Count | `references/valuation.md` | Same as above |
| **Build / fix a financial model** | | | |
| forecast financials, 3-statement model | 3-Statement Model | `references/financial_models.md` | `formats/excel_standards.md` + `formats/metric_disambiguation.md` |
| M&A accretion/dilution, deal math | Merger Model (Accretion/Dilution) | `references/financial_models.md` | Same as above |
| synergy estimate | Synergy Analysis | `references/financial_models.md` | Same as above |
| IPO proceeds / offering model | IPO Model | `references/financial_models.md` | Same as above |
| audit / debug / edit an existing model | Model Audit / Live Model Editing | `references/financial_models.md` | `formats/excel_standards.md` |
| **Structure a buyout** (PE/LBO) | | | |
| LBO, buyout returns | LBO Model | `references/lbo_structuring.md` | `formats/excel_standards.md` + `formats/metric_disambiguation.md` |
| debt tranches, waterfall, revolver | Debt Schedule (LBO) | `references/lbo_structuring.md` | Same as above |
| S&U, funding table | Sources & Uses (S&U) | `references/lbo_structuring.md` | Same as above |
| preferred equity, PIK, convertible sleeve | Structured Equity Modeling | `references/lbo_structuring.md` | Same as above |
| earnout, contingent consideration | Earnout Modeling | `references/lbo_structuring.md` | Same as above |
| roll-up / tuck-in acquisitions | Bolt-On Acquisition Modeling | `references/lbo_structuring.md` | Same as above |
| dividend recap, sale-leaseback | Dividend Recap Modeling / Sale-Leaseback Modeling | `references/lbo_structuring.md` | Same as above |
| **Explain returns** | | | |
| why did the deal make money, IRR bridge | IRR Attribution / Value Creation Bridge | `references/returns_analysis.md` | `formats/excel_standards.md` |
| who gets what at exit, waterfall by class | Liquidation Waterfall | `references/returns_analysis.md` | Same as above |
| management options / incentive pool | MIP Modeling | `references/returns_analysis.md` | Same as above |
| **Run diligence** | | | |
| DD question list / request list / tracker | DD Request List (DRL) / DD Tracker | `references/due_diligence.md` | `formats/excel_standards.md` (for tracker) |
| check data room completeness | VDR Gap Analysis | `references/due_diligence.md` | `formats/document_standards.md` |
| challenge EBITDA add-backs | Buy-Side QoE Review | `references/due_diligence.md` | `formats/excel_standards.md` |
| customer revenue / retention / cohort data | Customer-Level Revenue Analytics / Retention & Cohort | `references/due_diligence.md` | `formats/excel_standards.md` |
| prep management / expert interviews | Management Meeting Questions / Expert Call Guide | `references/due_diligence.md` | `formats/document_standards.md` |
| summarize a credit agreement | Credit Agreement Summary | `references/due_diligence.md` | `formats/document_standards.md` |
| **Sell a company / raise capital** | | | |
| anonymous 1-2 pager to test buyer interest | Deal Teaser | `references/deal_materials.md` | `formats/document_standards.md` |
| CIM / full marketing narrative | CIM Executive Summary | `references/deal_materials.md` | `formats/document_standards.md` |
| who would buy this asset | Buyer List Development | `references/deal_materials.md` | `formats/excel_standards.md` |
| which institutions to target (ECM) | Cross-Holder Analysis | `references/deal_materials.md` | — |
| initiate coverage, stock pitch report | Initiating Coverage Report | `references/deal_materials.md` | `formats/document_standards.md` |
| **Decide internally** | | | |
| scorecard / quality checklist for IC | Business Quality Scorecard | `references/deal_materials.md` | — |
| IC memo | Business Quality Scorecard + assemble prior outputs (thesis, risks & mitigants, valuation, DD findings) | `references/deal_materials.md` | `formats/document_standards.md` |
| **Day-to-day support** | | | |
| meeting prep pack, project status | Project Overview (+ Earnings Update for the counterparty) | `references/deal_materials.md` (+ `references/company_analysis.md`) | — |
| peer benchmarking dashboard | Public Comps (visual summary variant: growth/margin/Rule-of-40 vs median) | `references/valuation.md` | — |

**Multi-Task Rules**:
- List all requested tasks first. Identify unique files needed from the table above. Read them sequentially before starting execution. Do not read file-by-file as you build.
- Do not load format files (`formats/`) for pure-text conversational answers.
- When the deliverable is Excel, `formats/excel_standards.md` is the sole formatting authority — do not blend in generic spreadsheet skills' aesthetics (themes, decorative highlighting); their guidance is for non-finance spreadsheets.

**Out-of-Scope (DO NOT route here)**:
- Quant trading system development (signal engineering, execution algos, live strategy code — treat as general programming). Lightweight historical evaluation of a screen/rule inside a research task stays in scope — follow the Backtesting minimums under Data Rules.
- Legal dispute calculations / contract review (treat as general/legal task).
- Personal banking / tax filing.

## Data Rules (apply to every domain)

### Data-source routing — a pipeline, not a lookup

Data needs are organized by **capability class**, not by provider. Route every data pull through this pipeline. Steps 1–2 run once per session; steps 3–5 run per question.

**Step 1 — Inventory (once per session).** Before the first data pull, check in parallel: (a) any stated source preference — user messages, project instructions, or prior context ("use our CapIQ numbers"); (b) which connectors/MCP/data APIs are attached to this session; (c) the built-in financial data APIs that are always available (see the financial-analysis skill: Massive fundamentals/OHLCV/ratios-screening/options-chains/short-interest/macro, Yahoo quotes/holders/insights, Quartr transcripts/events/IR documents). Never claim "I don't have this data" before completing this inventory; when unsure whether the built-in surface covers a data class, probe the API search channel (`search type=api` with the provider/family name) before concluding the data is unavailable. If a class is truly unavailable, say so and use the fallback path — never fabricate.

**Step 2 — Preference arbitration (asymmetric silence).** If a preferred source is stated and available → use it, and load any usage docs that come with the connector before calling it. If a preferred source is stated but NOT available → do not silently substitute; tell the user, offer the connect/fix step, and only proceed on an alternative basis with explicit disclosure of the basis change (a substituted basis the user believes is their preferred one is silent misinformation). If no preference is stated → choose silently in priority order **connected > built-in > public fallback** and just answer; do not narrate source selection or connection status. When the user expresses a durable preference ("always use FactSet"), record it in the project/task notes so later sessions inherit it.

**Step 3 — Domain gate.** The user's own portfolio, balances, and transactions are personal-finance territory — see Out-of-Scope and the portfolio guardrails in the relevant playbook; market/company data continues below. Mixed questions (e.g. "how do my holdings compare to the sector") combine both: user-side numbers from user-provided data, market-side numbers through this pipeline.

**Step 4 — Class → source (the table below).** Find the capability class, take the highest available tier. Within a class, pick endpoints by grain and time axis: prices → market data (not metric series); full statements → fundamentals; single metric or multiple → metric series; forward metrics (NTM P/E) ≠ trailing; **adjusted/covenant/as-reported figures (Adjusted EBITDA, OIBDA) never come from standardized endpoints — rebuild from disclosure text**.

**Step 5 — Degradation chain (when structured sources don't cover it).** Structured endpoints → earnings transcripts/IR documents → primary filings → open web, in that order. Transcripts before web: guidance, non-GAAP metrics, company KPIs, and segment color usually live there, and they answer many questions that look like they need filings or news. Point-in-time facts that live in filings (officers, compensation, deal terms, share counts at a date) come from a filing lookup, never from memory. When a number does come from the open web (e.g. segment economics narratives, channel/supplier concentration): state its as-of date, prefer the primary source behind the page, and cross-check any decision-relevant figure against a second independent source.

Named providers below are recognition anchors, not availability claims — treat any attached connector of the same class the same way.

| Capability class | Connected — professional providers (use first if attached) | Built-in (always available) | Public fallback |
| --- | --- | --- | --- |
| Market data (price/OHLCV/mkt cap/dividends/splits/short interest) | Bloomberg, FactSet, S&P Capital IQ | Massive OHLCV/snapshots/movers, dividends & splits, FINRA short interest & float; Yahoo charts (incl. non-US tickers) | Exchange websites |
| Options — chains, contracts & flow | Unusual Whales (flow/unusual activity), Bloomberg, FactSet | Massive options: contract search/details/OHLCV history (no flow, no greeks) | OCC & exchange public stats; label flow interpretations as inference |
| Full financial statements | S&P Capital IQ, FactSet, FMP, Daloopa (granular as-reported models) | Massive income/balance/cash-flow statements (US-centric) | SEC EDGAR (or local regulator) filings, parse original |
| Metric & ratio time series; reported actuals | Daloopa, Fiscal.ai (as-reported actuals), FMP | Massive financial_ratios (22 ratios) & statement line items | Compute from statements (state the basis) |
| Segment data (by business/geo) | S&P Capital IQ, FactSet, Daloopa | — (no working built-in segment endpoint) | 10-K/annual-report segment note, parse original |
| Filings search & retrieval | AlphaSense, Bloomberg | Massive EDGAR index & standardized 10-K risk-factor text; Yahoo filing lists; Quartr filing/report PDFs | EDGAR full-text search; company IR page |
| Earnings calls & corporate events (transcripts/slides/calendar) | FactSet, S&P Capital IQ (CallStreet) | Quartr, events-first: company resolve → event list (incl. upcoming = earnings calendar) → transcripts/chapters/slides/reports | Company IR webcast; reputable transcript re-publishers (verify quotes against audio) |
| Ownership, holders & insider activity | Bloomberg, FactSet, S&P Capital IQ | Yahoo holders (institutional/fund holdings, insider transactions); Massive float & short interest | SEC 13F/Form 4 filings via EDGAR, parse original |
| Consensus estimates & sell-side views | S&P Global (Visible Alpha), Morningstar, Bloomberg, FactSet | Yahoo analyst insights (single-source target/ratings — NOT consensus, label it) | Publicly reported analyst views, labeled as second-hand |
| Private / VC / fund data | PitchBook, Crunchbase, Preqin, Forge (pre-IPO secondary marks) | — | Company site + press releases + reputable media, cross-verified; label as secondary estimate |
| News / sentiment | Bloomberg, AlphaSense | Massive news (per-ticker sentiment with reasoning) | Reputable media with date-window filters |
| Screening (find/rank a batch) | Bloomberg (EQS), S&P Capital IQ screener, FactSet | Massive ratio range-filters (22 ratios, `.gte`/`.lte`) | Multi-list intersection + per-company verification |
| Event & macro probabilities | — | — | Prediction-market public APIs (Polymarket: free, no key; live state only) — quote as market-implied probability with liquidity noted, never as forecast |
| Macro / FX / Crypto | Bloomberg, FactSet; CarbonArc (ESG/carbon) | Massive treasury yields (1962+), CPI & inflation expectations, labor market, forex, crypto | World Bank, central banks / statistics offices |

**Provider recognition & basis notes**: when a connected source or a cited webpage traces to a known provider, use it to judge basis and coverage — e.g., consensus from S&P Global (Visible Alpha) vs Morningstar uses different analyst samples (never mix in one series); reported actuals (Fiscal.ai-style) differ from adjusted consensus bases; pre-IPO marks (Forge) are secondary-market transaction data, not fund NAVs; Yahoo analyst insights are single-source, never present them as consensus. When a connected source and a built-in source overlap, prefer the connected one but cross-check decision-relevant figures across tiers — a persistent gap usually means a basis difference worth surfacing. Where a provider's license requires attribution (common for private-market data), name it in the deliverable — per the Compliance element in the Delivery Disclosure.

**Schema drift defense**: trust the columns/fields actually returned, never the documented schema or your assumption of it. The same capability class served by different providers (or the same provider across coverage tiers) can shift naming style (snake_case vs camelCase), units, and adjustment basis. Read the real headers before computing.

### Source hierarchy & web discipline

Primary disclosures (filings/IR/regulator/exchange) > professional databases (incl. the public/free tiers of specialist providers — prediction markets, options-flow sites, transcript services — which outrank general media for their specialty) > authoritative financial media (Reuters/Bloomberg/WSJ/FT) > industry bodies > general news/Wikipedia (context only, never final citation) > blogs/forums/social (lowest; cross-verify and label).

Four rules: (1) **Search is discovery, not citation** — snippets locate leads; fetch and verify the full text before citing. (2) **Always upgrade** — if a webpage says "the filing shows…", pull that filing and cite it, not the webpage. (3) **Conflicts resolve to primary** — present conflicting sources side by side only when the difference is material. (4) **Beware circular references** — multiple secondary sites echoing each other is not corroboration; trace to the common origin. AI-generated content requires extra scrutiny.

### Reference-date protocol (anchor time before touching data)

Every data pull is relative to a **reference date**. Establish it before the first fetch:

1. Default: the actual current date from the runtime environment — never assume your training cutoff is "today". Stale-knowledge errors (old prices, superseded quarters, pre-IPO/delisted status) are the most systematic finance failure mode.
2. If the question implies a period ("Q3 FY25 results", "last year's margins", "the 2023 call"), derive the reference date from that period instead.
3. Map the reference date to fiscal periods **through the Entity Card's FY-end month** (this is where the fiscal-time iron rules below take over).
4. "Latest / current / now" is ambiguous and non-reproducible — resolve it to an explicit date or fiscal period at fetch time, and carry that date into the deliverable (the Delivery Disclosure "Time" element must echo it).

### Fiscal-time discipline (three iron rules)

1. Filing date ≠ fiscal period. Always label data by fiscal period; check the Entity Card's FY-end month before any YoY/QoQ claim.
2. Forward-looking (guidance/estimates) and realized data are labeled separately, never mixed in one series.
3. LTM periods must be dated (LTM as of which quarter-end) and must pre-date any deal announcement when used in comps.

### Cross-cutting data traps (apply to any source)

These are properties of financial data itself, not of any provider — check them whatever the source:

1. **Survivorship bias**: screeners and constituent lists return only currently-listed companies. Any screen or comparison spanning a historical period silently excludes the delisted and bankrupt, inflating apparent returns — flag this whenever a conclusion depends on a historical universe.
2. **Pre-earnings staleness**: "latest reported" financials can be 3+ months old in the weeks before the next release — materially misleading for fast-growing or deteriorating companies. Note the reporting lag when the analysis is time-sensitive.
3. **Constituent lag**: index/ETF/portfolio composition data often lags 30-90 days; rebalances and additions may not be reflected. Date the composition snapshot.
4. **Adjusted vs unadjusted prices**: know which one your source returns. Comparing adjusted prices against news-quoted or historical target prices across a split/dividend boundary produces wrong conclusions.
5. **Correlation regimes shift**: correlations computed from calm markets understate drawdown risk — they spike toward 1.0 exactly when diversification is needed. Label the estimation window of any correlation/beta.
6. **Threshold alerts on returns, not price levels**: any recurring price-watch logic must trigger on percentage return recomputed from freshly adjusted data; fixed price thresholds fire phantom signals after splits and corporate actions.

**Backtesting minimums** (for lightweight historical evaluation inside a research task):
- Insert a censor gap (≥1 trading day; add reporting lag for financials) between information cutoff and evaluation window; compute returns strictly after the censored decision point.
- Never construct a past portfolio or signal with future prices, earnings, or estimate revisions.
- If the censor window cannot be verified, stop and say so — a leaky backtest is worse than none.

## General Delivery Checklist & Disclosure

Before sending your final response, verify:
1. **Domain Sanity Checks**: All pre-delivery checks from the reference file passed.
2. **Traceability**: Inline citations used in reports; source comments attached to all hardcoded Excel cells; web-only or estimated figures explicitly labeled; missing data marked TBD, never invented. **Derived figures in text/markdown deliverables (margins, growth rates, ratios) must be reconstructable — be ready to state the formula and input values behind any derived number; in Excel this lineage lives in the formula chain, in prose it must survive without one.**
3. **Precision & wording**: present tool/database figures at source precision — no "approximately / roughly / around / ~ / nearly" hedging on sourced data ("$21.09", not "about $21"). Do not round intermediate calculations; round once, at the presentation layer, consistently ("$1.23B" and "$2.00B", never mixed with "$2B").

**Delivery Disclosure (Mandatory)**
Your final message to the user MUST include a brief disclosure covering these five elements, ensuring full transparency:
- **Basis**: Which metric definitions were used (e.g., "EBITDA excludes SBC", "TEV includes operating leases").
- **Time**: The as-of date for pricing, LTM cutoff quarter, and fiscal year alignment.
- **Assumptions**: Which silent defaults were applied from the playbook (e.g., "5-year forecast", "Mid-year discounting").
- **Sources & Confidence**: The primary data sources used, and any caveats regarding data quality or estimation.
- **Compliance**: For deliverables containing investment analysis or recommendations, close with: *"This is research and analysis only, not personalized financial advice."* Where a data source's license terms require attribution, name it in the deliverable — and never name a licensed source you did not actually use.
