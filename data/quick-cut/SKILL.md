---
name: svp-quick-cut
description: "Generates a complete SVP Quick-Cut credit memo for any issuer. Orchestrates ten sections (Subject, The Trade, Capital Structure, Valuation & Entry Create, Business Overview, Financials, Comparable Company Analysis, Return Scenarios, Key Investment Considerations, Company Background) using available MCP data connectors, SEC EDGAR, and web search. Triggers on: Quick-Cut, quick cut, QC memo, credit memo, issuer overview, tearsheet, 'write up [company]', 'run a quick cut on [company]', 'SVP memo for [company]', 'pull together a QC on [issuer]', or any mention of Quick-Cut in a credit research context. Also triggers when the user provides an ISIN, CUSIP, FIGI, BBG ticker, or LXID and asks for a credit memo or analysis."
---

# SVP Quick-Cut Orchestrator

Produces a complete SVP Quick-Cut credit memo. Every memo includes all mandatory sections -- The Trade is never optional. Writing phases are ordered so each section builds on prior ones, culminating in The Trade (which synthesizes everything) and the Subject Line (which distills it into one line).

> See `_shared/plugin-context.md` for domain vocabulary, source hierarchy, and quality standards.

## Prerequisites

### MCP Connections

| # | Provider | Required? | Purpose | Fallback |
|---|----------|-----------|---------|----------|
| 1 | **Nexus MCP** | Optional | Platform data, deal pipeline, proprietary analytics | Manual input or uploaded documents |
| 2 | **BigData.com** | Recommended | Company research, news, SEC filing search, tearsheets | Web search + uploaded documents |
| 3 | **Credit data provider** (Databricks Genie if connected) | Recommended | Capital structure, market pricing, credit fundamentals | Manual input, uploaded materials |
| 4 | **Internal document search** (Glean if connected) | Optional | Prior memos, IC notes, deal files | Skip prior work integration |
| 5 | **SEC EDGAR** | Available via web | Public company filings, XBRL financials | Always available (public API) |

**Minimum requirement**: At least one identifier (company name, ISIN, CUSIP, FIGI, BBG ticker) OR uploaded documents. The skill adapts to whatever tools are available -- it produces the best memo possible with connected sources and flags gaps for anything missing.

---

## Final Output Order

1. **Subject** -- One-line subject with company, instrument, and catalyst
2. **The Trade** -- Investment thesis with bull/bear narrative (<125 words)
3. **Capital Structure** -- Enhanced table with market values, subtotals, net create at par & market
4. **Valuation & Entry Create** -- Standalone valuation box: entry price, EV, create multiples
5. **Business Overview** -- 120-160 word bullet-point summary including ownership
6. **Financials** -- Compact financial summary table (fits one portrait PDF page)
7. **Comparable Company Analysis** -- Side-by-side comp table (2-3 comps)
8. **Return Scenarios** *(optional)* -- Bear/Base/Bull scenario table with MoM
9. **Key Investment Considerations** -- Expanded bull case drivers and key risks (bullets)
10. **Company Background** -- Founded, HQ, brands, scale, CEO

## Writing Order (draft sequence -- differs from output order)

1. Company Background -> 2. Capital Structure -> 3. Valuation & Entry Create -> 4. Business Overview -> 5. Financial Summary -> 6. Comparable Company Analysis -> 7. Return Scenarios (if applicable) -> 8. Key Investment Considerations -> 9. The Trade -> 10. Subject Line

Company Background is drafted first because ownership, scale, and history inform everything else. The Trade is written second-to-last because it synthesizes all prior sections. Subject Line is always last.

---

## Source Hierarchy (highest to lowest)

**#1 Uploaded investor materials** (CIM, financials, credit agreements, offering memos, investor presentations) > **#2 Credit data provider** (capital structure, market pricing, credit fundamentals) > **#3 SEC EDGAR** (10-K, 10-Q, 8-K, XBRL -- public companies only) > **#4 BigData.com** (company research, news, filing search) > **#5 Internal document search** (prior memos, IC notes, deal files) > **#6 Web search**

- **Uploaded materials are king.** If the user provides a CIM, financials deck, or credit agreement, those numbers override everything else.
- **SEC EDGAR is public-company only.** For private / sponsor-owned issuers, skip EDGAR and rely on #1 > #2 > #4 > #5 > #6.
- **Internal documents** (prior firm work) are institutional opinion, not primary data. Incorporate the prior analytical framing, but always validate numbers against higher-ranked sources.
- Never estimate or extrapolate missing data -- use "--" instead.

---

## Inputs

The user may provide any combination of the following. At minimum, one identifier is needed:

- A **company name** or **security identifier** (ISIN, CUSIP, FIGI, BBG ticker, LXID)
- A **target instrument** (e.g., "the 1L TL", "the reorg equity", "the 2029 senior unsecured notes")
- **Uploaded documents** (10-K, CIM, credit agreement, offering memo, investor presentation)
- Specific instructions (e.g., "focus on refinancing risk", "comp to Cinemark and AMC")

**Identifier resolution**: If given a security identifier instead of a company name, resolve it via the credit data provider (if connected), BigData.com `find_companies`, or SEC EDGAR CIK lookup.

---

## Orchestration Workflow

### Phase 0: Preflight & Data Collection

**0a. Check tool availability.** Test each connected MCP tool. Present a status table showing which sources are live. If no tools are connected, confirm the user will provide data manually or via uploads.

**0b. Identify the company.** Use available tools to resolve the company: credit data provider for identifier lookup, BigData.com `find_companies` / `bigdata_tearsheet`, or SEC EDGAR submissions API (`https://efts.sec.gov/LATEST/search-index?q=COMPANY&dateRange=custom&startdt=YYYY-MM-DD&enddt=YYYY-MM-DD`). If multiple matches, pick the active entity or ask the user.

**0c. Search for prior firm work** (if internal document search is connected). Look for prior Quick-Cuts, IC memos, and credit analyses on this issuer. Use the most recent 1-3 results. Incorporate prior trade theses (updated with current data). Reference in footer: `*Prior coverage: [title], [date]*`. Do NOT copy verbatim.

**0d. Fire parallel research queries.** Launch all available data collection simultaneously:

- **Credit data provider**: annual financials, quarterly financials, capital structure instruments, market pricing, intelligence articles
- **BigData.com** (from financial-analysis plugin): `find_companies` / `bigdata_tearsheet` for profile; `bigdata_search` for news and filings; `bigdata_events_calendar` for catalysts
- **SEC EDGAR** (public companies only): company submissions via `https://data.sec.gov/submissions/CIK{padded_cik}.json`, XBRL facts via `https://data.sec.gov/api/xbrl/companyfacts/CIK{padded_cik}.json`, full-text search via `https://efts.sec.gov/LATEST/search-index?q=QUERY`
- **Web searches**: company website, sponsor ownership/acquisition, comparable transaction multiples, market cap
- **Uploaded documents**: Read and extract. These take #1 source precedence.

**Graceful degradation**: If a tool is unavailable, skip it and proceed with remaining sources. If critical data is missing (e.g., no capital structure from any source), prompt the user to provide it manually before continuing.

---

### Phase 1: Company Background

Draft first because ownership, scale, and history inform all other sections. Cover:
- Founded date, headquarters, CEO
- Brands, subsidiaries, business lines
- Scale metrics (revenue, employees, locations/sites, geographic footprint)
- Ownership history: who owns it, acquisition date, purchase price/multiple, seller (or: publicly listed, ticker, largest shareholders)

---

### Phase 2: Capital Structure (Enhanced)

Build the full capital structure table with:

- **Instrument rows**: Security Name, Security Type, Amount Outstanding (Par), Coupon/Term, Maturity, Market Price (% PAR), Market Value, Currency
- **Currency normalization**: base currency (USD or EUR) for all amounts; original currency in brackets if different
- **Subtotals**: Secured Debt subtotal, Unsecured Debt subtotal
- **Total Gross Debt** (sum of all debt instruments)
- **Cash** line (negative)
- **Net Debt** = Total Gross Debt - Cash
- **Equity** line (market cap for public; sponsor equity value if known)
- **Total Enterprise Value** = Net Debt + Equity
- **Derived metrics**: Net Create at Par (Net Debt / EBITDA), Net Create at Market ((Market Value of Debt - Cash) / EBITDA)

Seniority order: least senior (top) to most senior; equity below net debt.

---

### Phase 3: Valuation & Entry Create

Standalone valuation box:

| Metric | Value |
|---|---|
| Entry Price | $X.xx / share or bond price |
| Shares / Face Outstanding | X |
| Implied Equity Value (entry) | $Xbn |
| Enterprise Value (create) | $Xbn |
| LTM EBITDA | $Xm |
| EV / LTM EBITDA | X.Xx |
| Forward EBITDA (estimate) | $Xm |
| EV / Forward EBITDA | X.Xx |

Sources: Capital Structure (Phase 2) for debt/EV, Financials (Phase 5) for EBITDA, web search or BigData.com for market cap/share price.

---

### Phase 4: Business Overview (with Ownership)

Write **120-160 words** as **non-indented bullet points**. Content priorities:
1. Core business model, products/services, customers, geography
2. **Ownership**: who owns the business, acquisition date, purchase price/multiple, seller (or: publicly listed, ticker, largest shareholders)
3. End markets with percentage breakdowns
4. Key suppliers, raw materials, competitors
5. Operational or restructuring initiatives
6. Scale metrics (revenue, EBITDA, employees, segment/geographic mix)

---

### Phase 5: Financial Summary

Compact markdown table: 4 quarters + LTM + 3 fiscal years. Rows: Revenue, Revenue Growth YoY, Gross Profit, Gross Margin, Adj. EBITDA, EBITDA YoY, EBITDA Margin, Capex, Cash Interest, (EBITDA-Capex), (EBITDA-Capex-Cash Interest). If segment data is available, include a segment breakdown sub-table.

---

### Phase 6: Comparable Company Analysis

Side-by-side comp table with 2-3 comparable companies. Identify comps via sector classification, BigData.com, or web search. If the user specifies comps, use those.

Comp metrics (adapt to sector): Status, Scale, Geography, Revenue, EBITDA, EBITDA Margin, Net Debt, Net Debt / EBITDA, EV / EBITDA, Market Share, Credit Rating, Dividend/Buybacks, FCF, Key Risk.

---

### Phase 7: Return Scenarios (OPTIONAL)

Include **only when the data supports it** -- typically for equity positions or situations with a clear key driver that can be sensitized (e.g., commodity price, occupancy, box office).

For debt positions where scenario analysis depends on restructuring dynamics rather than EBITDA, skip unless the user specifically requests it.

When included: Bear / Base / Bull scenario table with columns for the key driver, EBITDA, EV (@Xx), Net Debt, Equity Value, Per Share (if applicable), MoM.

---

### Phase 8: Key Investment Considerations

Two sub-sections with 5-8 bullets each:

**Bull Case**: post-reorg capital structure, liquidity, market share gains, operational momentum, upcoming catalysts, rating trajectory, FCF growth, exit optionality.

**Key Risks**: revenue/volume volatility, geographic drags, secular headwinds, illiquidity, macro exposure, operational execution, regulatory.

Draw from all available sources: credit data provider intelligence, BigData.com news, SEC filings (risk factors section), prior firm work, web search.

---

### Phase 9: The Trade (MANDATORY)

By this point all other sections are complete. Write **<125 words** covering:
- Ownership context
- LTM EBITDA - Capex - Cash Interest
- Current create at market price vs. acquisition multiple and comps
- Bull case (<75 words)
- Bear case (<75 words)

If prior firm work was found in Phase 0c, weave in institutional perspective. Note where current view aligns or diverges.

---

### Phase 10: Subject Line (written last)

Format: `"[Company] -- [Instrument] (Key Catalyst / Situation Summary)"` -- max 15 words.

---

### Phase 11: Assemble & Output

Combine in **output order**:

```
**Subject:** [subject line]

---

## The Trade
[paragraph]

---

## Capital Structure
[enhanced table with subtotals, cash, net debt, equity, net create]

---

## Valuation & Entry Create
[valuation box table]

---

## Business Overview
[bullet points with ownership]

---

## Financials
(USD in millions)
[financial summary table]

---

## Comparable Company Analysis
[comp table]

---

## Return Scenarios  *(if included)*
[scenario table]

---

## Key Investment Considerations
### Bull Case
[bullets]
### Key Risks
[bullets]

---

## Company Background
[Founded, HQ, brands, scale, CEO]
```

If prior firm work was found: `*Prior coverage: [title(s)], [date(s)]*`

---

## Mid-Run Error Handling

If a tool fails after passing preflight: retry once, then continue with remaining sources. Append a `Data Gaps` footer listing what is missing and which section is affected. Always tell the user what happened. If the user can supply missing data manually, prompt them before finalizing.

---

## Quality Checks

1. **All mandatory sections present**: Subject, The Trade, Capital Structure, Valuation & Entry Create, Business Overview, Financials, Comps, Key Investment Considerations, Company Background
2. **Return Scenarios**: included only when data supports it; absence is fine
3. **Word counts**: Business Overview 120-160; The Trade <125; Subject <=15 words
4. **Cap structure math**: subtotals add up; Net Debt = Gross Debt - Cash; Market Value = Price x Par; Net Create at Market is correct
5. **Currency normalization**: all amounts in base currency with original in brackets
6. **Source hierarchy respected**: Uploaded > Credit data > EDGAR (public only) > BigData.com > Internal docs > Web
7. **No hallucination**: every number traces to a source; "--" for unavailable
8. **Comp relevance**: comps are in the same sector/geography; metrics are appropriate
9. **Ownership covered**: Business Overview includes who owns it, when, for how much
10. **Prior work integration**: if internal search returned prior memos, confirm incorporated
11. **Tool coverage**: all available sources queried; gaps flagged in Data Gaps footer

---

## Confidence Calibration

Every Quick-Cut output must conclude with a calibrated confidence assessment. This is mandatory -- it appears after the Company Background section and before any Data Gaps footer.

```
## Confidence Assessment
- **Score**: 0.XX (0.0 = no confidence, 1.0 = full confidence)
- **Calibration**: conservative | neutral | optimistic
- **Confidence Drivers**: [list what supports the score -- e.g., "audited 10-K financials available", "current market pricing from credit data provider", "3 prior firm memos on file"]
- **Data Gaps**: [list what is missing that would improve confidence -- e.g., "no current loan axes pricing", "private company -- no EDGAR filings", "no prior firm coverage found"]
```

### Scoring Guidelines

| Score Range | Interpretation | Typical Scenario |
|-------------|----------------|------------------|
| 0.85-1.00 | High confidence | Uploaded CIM + audited financials + live market pricing + prior firm work |
| 0.65-0.84 | Moderate confidence | Public company with EDGAR + BigData.com + web, but no proprietary data |
| 0.45-0.64 | Low-moderate confidence | Limited to web search + partial uploads, several data gaps |
| 0.00-0.44 | Low confidence | Minimal data, many sections use "--", flag for heavy manual review |

### Three-Pass Calibration

For scores in the 0.45-0.75 range (ambiguous zone), apply three-pass calibration:
1. **Conservative pass**: assume worst-case for missing data, stress negatives
2. **Neutral pass**: take data at face value
3. **Optimistic pass**: assume favorable resolution of unknowns

High consistency across passes = higher confidence. Significant divergence = flag for human review and note which assumptions drive the spread.

---

## Key Principles

- **Adapt to available tools**: produce the best memo possible with connected sources; never block on missing tools.
- **Parallel execution**: fire all available data queries simultaneously.
- **Institutional memory**: always check internal docs first if connected. Prior views are an asset.
- **SVP voice**: factual, analytical, direct -- no filler.
- **Specificity over completeness**: fewer accurate data points beat padded vague statements.
- **Market-aware**: always try for current pricing; flag stale prices with date.
- **Build-up logic**: each section informs the next; The Trade synthesizes all.
- **Fail loud**: if a tool breaks mid-run, flag exactly what is missing.
- **Manual input welcome**: if tools are unavailable, accept pasted financials, typed cap structures, or uploaded PDFs as primary data.
