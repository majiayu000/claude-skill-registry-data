---
name: financial-statement-analyzer
description: "Performs structured fundamental analysis of annual reports (Form 10-K, Form 10-Q): ratio analysis, quality of earnings, working-capital efficiency, segment decomposition, accounting red flags, and Management's Discussion and Analysis (MD&A) parsing. Use when underwriting an investment; evaluating a competitor; preparing for an earnings call; building peer comparables; or screening for accounting risk."
---

# Financial Statement Analyzer

> A repeatable teardown of public-company financials that produces an institutional-quality analysis.

## What this skill is

A structured workflow that reads the full Form 10-K and Form 10-Q stack - income statement, balance sheet, cash flow, Management's Discussion and Analysis (MD&A), footnotes, risk factors, and proxy statement - and produces a one-page summary with margin waterfalls, quality-of-earnings score, segment decomposition, and an accounting red-flag log. Designed to surface the data that the headline numbers hide.

## What it solves

- Headline Earnings Before Interest, Taxes, Depreciation, and Amortization (EBITDA) reviews that ignore non-Generally Accepted Accounting Principles (non-GAAP) adjustments
- Margin analysis with no waterfall identifying which line item moved
- Missed red flags hiding in footnotes, risk factors, and Cash Conversion Cycle (CCC) trends
- Segment data taken at face value (without checking corporate-overhead allocation)
- Skipping the year-over-year diff of risk factors - the single most under-read disclosure

## When to invoke

- Underwriting a long or short position in a public company
- Benchmarking a private company against the public peer set
- Pre-earnings preparation for management question-and-answer
- Quarterly competitor financial review
- Diligence on a partnership, vendor, or acquisition target

## Phase 1: Source the filings

Confirm the latest:
- Annual report (Form 10-K, or Form 20-F for foreign issuers) - most recent fiscal year
- Quarterly report (Form 10-Q) - trailing 4 quarters
- Current report (Form 8-K) - material events, guidance, restatements (last 12 months)
- Proxy statement (Form DEF 14A) - executive compensation, related-party transactions, board composition
- Earnings release plus supplemental (segment data often only here)
- Earnings call transcript - tone, question-and-answer pressure points

Log filing date and period for each. Note any restatements.

## Phase 2: Quality of revenue

- Revenue recognition policy (Accounting Standards Codification (ASC) 606 adherence)
- Performance obligation timing - ratable versus point-in-time
- Deferred revenue trend (balance sheet liability) - should grow with bookings
- Remaining Performance Obligation (RPO) or backlog - directional read on future revenue
- Customer concentration (top-10 percent of revenue, footnotes)
- Geographic and segment mix - where is growth coming from?
- Channel inventory and sell-in versus sell-through (Consumer Packaged Goods (CPG), hardware) - channel-stuffing risk
- Non-GAAP adjustments - list each and decide if defensible

Compute organic growth = reported growth − Mergers and Acquisitions (M&A) contribution − foreign exchange − accounting policy change.

## Phase 3: Profitability and margin architecture

Margin waterfall year-over-year:

| Line | Y-2 | Y-1 | Y | Δ basis points | Driver |
|------|-----|-----|---|----------------|--------|
| Revenue | $X | $X | $X | not applicable | |
| Gross margin | xx% | xx% | xx% | ± basis points | mix / pricing / cost |
| Research and Development (R&D) percent | xx% | xx% | xx% | ± basis points | innovation intensity |
| Sales and Marketing (S&M) percent | xx% | xx% | xx% | ± basis points | growth investment |
| General and Administrative (G&A) percent | xx% | xx% | xx% | ± basis points | operating leverage |
| Operating margin | xx% | xx% | xx% | ± basis points | |
| Tax rate | xx% | xx% | xx% | ± basis points | mix / one-timers |
| Net margin | xx% | xx% | xx% | ± basis points | |

DuPont decomposition of Return on Equity (ROE):

```
ROE = Net margin × Asset turnover × Equity multiplier
```

Identify which lever moved.

## Phase 4: Working capital and cash conversion

```
Cash Conversion Cycle (CCC) = Days Sales Outstanding (DSO) + Days Inventory Outstanding (DIO) − Days Payable Outstanding (DPO)
```

- DSO rising → collection problems, channel stuffing, or longer-term contracts
- DIO rising → demand softness, obsolescence
- DPO rising → vendor financing, possibly stress

Compare **Cash Flow from Operations (CFO) / Net income**:
- Less than 1× across multiple periods → earnings-quality concern
- Identify the gap (working capital, Stock-Based Compensation (SBC), deferred tax)

Free Cash Flow (FCF) / Adjusted EBITDA conversion: Software as a Service (SaaS) 60-80% healthy; services 80%+.

## Phase 5: Balance sheet and capital structure

- Net debt / Adjusted EBITDA → covenant headroom, refinancing risk
- Interest coverage = Adjusted EBITDA / interest expense
- Maturity wall (footnotes) - concentration in next 18 months?
- Off-balance-sheet items (operating leases on balance sheet under ASC 842, purchase commitments, contingent consideration)
- Goodwill plus intangibles as percent of equity → impairment risk
- Pension and Other Post-Employment Benefits (OPEB) underfunded status
- Tangible book value versus market capitalization → strategic floor

## Phase 6: Accounting red flags

| Red flag | Look for | Severity |
|----------|----------|----------|
| DSO jumping | up more than 20% year-over-year without business-model change | High |
| Cost reclass | Cost of Goods Sold (COGS) moved to operating expense | Medium |
| Asset quality decline | non-current assets up faster than revenue | Medium |
| Soft revenue | revenue growth much greater than cash collection growth | High |
| Selling, General and Administrative (SG&A) growing slower than revenue | possible cost capitalization | Medium |
| Depreciation rate dropping | useful-life extensions | Medium |
| Accruals divided by assets rising | earnings management | High |
| Recurring one-time charges | cookie-jar reserves | Medium |
| Goodwill up without impairment | rolling acquisitions, no test | Medium |
| Restatements in last 3 years | internal control weakness | High |

Cross-check the auditor's report: going concern, Critical Audit Matter (CAM), or auditor change.

## Phase 7: Segment decomposition

- Revenue plus operating earnings (EBIT) by segment with margins
- Inter-segment eliminations
- Allocation of corporate overhead - does management hide losses?
- Segment capital expenditure if disclosed
- Identify the value-driver and the value-destroyer segments
- Sum-of-the-parts cross-check on consolidated multiples

## Phase 8: MD&A and risk factors

- MD&A: specific versus vague year-over-year explanations
- **Year-over-year diff of risk factors** - new risks added are the most revealing single signal in the filing
- Critical accounting estimates - where management has the most judgment
- Earnings call tone - hedging language, Chief Financial Officer (CFO) guidance walk

## Output

- One-page executive summary: bull case, bear case, decisive data point
- Margin and CCC waterfalls with year-over-year drivers
- Quality-of-earnings score (1-10) with reasoning
- Red-flag log with severity and follow-up question
- Peer comparable table: growth, gross margin, operating margin, FCF margin, Return on Invested Capital (ROIC), leverage
- 3 questions to ask the CFO on the next earnings call

## Operating rules

**Always**
- Reconcile non-GAAP to GAAP and judge each adjustment
- Read footnotes - that's where the disclosures live
- Compare CFO to net income across multiple years
- Cross-check segment data against the press release supplemental
- Document data gaps explicitly

**Never**
- Trust headline EBITDA without the bridge
- Treat one quarter as a trend
- Skip the year-over-year risk factors diff
- Use peer multiples without normalizing for accounting policy
- Confuse organic growth with reported growth
