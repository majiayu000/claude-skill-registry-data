---
name: dcf-model
description: Build institutional-quality DCF valuation models in Excel — revenue projections, FCF build, WACC, terminal value, Bear/Base/Bull scenarios, 5x5 sensitivity tables. Pairs with excel-author. Use for intrinsic-value equity analysis.
version: 1.0.0
author: Anthropic (adapted by Nous Research)
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [finance, valuation, dcf, excel, openpyxl, modeling, investment-banking]
    related_skills: [excel-author, pptx-author, comps-analysis, lbo-model, 3-statement-model]
source: "https://github.com/NousResearch/hermes-agent"
attribution: "NousResearch/hermes-agent by Nous Research"
---

## Environment

This skill assumes **headless openpyxl** — you are producing an .xlsx file on disk.
Follow the `excel-author` skill's conventions for cell coloring, formulas, named ranges, and sensitivity tables.
Recalculate before delivery: `python /path/to/excel-author/scripts/recalc.py ./out/model.xlsx`.

# DCF Model Builder

## Overview

This skill creates institutional-quality DCF models for equity valuation following investment banking standards. Each analysis produces a detailed Excel model (with sensitivity analysis included at the bottom of the DCF sheet).

## Tools

- Default to using all of the information provided by the user and MCP servers available for data sourcing.

## Critical Constraints - Read These First

These constraints apply throughout all DCF model building. Review before starting:

**Formulas Over Hardcodes (NON-NEGOTIABLE):**
- Every projection, margin, discount factor, PV, and sensitivity cell MUST be a live Excel formula — never a value computed in Python and written as a number
- When using openpyxl: `ws["D20"] = "=D19*(1+$B$8)"` is correct; `ws["D20"] = calculated_revenue` is WRONG
- The only hardcoded numbers permitted are: (1) raw historical inputs, (2) assumption drivers (growth rates, WACC inputs, terminal g), (3) current market data (share price, debt balance)
- If you catch yourself computing something in Python and writing the result — STOP. The model must flex when the user changes an assumption.

**Verify Step-by-Step With the User (DO NOT build end-to-end):**
- After data retrieval → show the user the raw inputs block (revenue, margins, shares, net debt) and confirm before projecting
- After revenue projections → show the projected top line and growth rates, confirm before building margin build
- After FCF build → show the full FCF schedule, confirm logic before computing WACC
- After WACC → show the calculation and inputs, confirm before discounting
- After terminal value + PV → show the equity bridge (EV → equity value → per share), confirm before sensitivity tables
- Catch errors at each stage — a wrong margin assumption discovered after sensitivity tables are built means rebuilding everything downstream

**Sensitivity Tables:**
- **Use an ODD number of rows and columns** (standard: 5×5, sometimes 7×7) — this guarantees a true center cell
- **Center cell = base case.** Build the axis values so the middle row header and middle column header exactly equal the model's actual assumptions (e.g., if base WACC = 9.0%, the middle row is 9.0%; if terminal g = 3.0%, the middle column is 3.0%). The center cell's output must therefore equal the model's actual implied share price — this is the sanity check that the table is built correctly.
- **Highlight the center cell** with the medium-blue fill (`#BDD7EE`) + bold font so it's immediately visible which cell is the base case.
- Populate ALL cells (typically 3 tables × 25 cells = 75) with full DCF recalculation formulas
- Use openpyxl loops to write formulas programmatically
- NO placeholder text, NO linear approximations, NO manual steps required
- Each cell must recalculate full DCF for that assumption combination

**Cell Comments:**
- Add cell comments AS each hardcoded value is created
- Format: "Source: [System/Document], [Date], [Reference], [URL if applicable]"
- Every blue input must have a comment before moving to next section
- Do not defer to end or write "TODO: add source"

**Model Layout Planning:**
- Define ALL section row positions BEFORE writing any formulas
- Write ALL headers and labels first
- Write ALL section dividers and blank rows second
- THEN write formulas using the locked row positions
- Test formulas immediately after creation

**Formula Recalculation:**
- Run `python recalc.py model.xlsx 30` before delivery
- Fix ALL errors until status is "success"
- Zero formula errors required (#REF!, #DIV/0!, #VALUE!, etc.)

**Scenario Blocks:**
- Create separate blocks for Bear/Base/Bull cases
- Show assumptions horizontally across projection years within each block
- Use IF formulas: `=IF($B$6=1,[Bear cell],IF($B$6=2,[Base cell],[Bull cell]))`
- Verify formulas reference correct scenario block cells

## DCF Process Workflow

### Step 1: Data Retrieval and Validation

Fetch data from MCP servers, user provided data, and the web.

**Data Sources Priority:**
1. **MCP Servers** (if configured) - Structured financial data from providers like Daloopa
2. **User-Provided Data** - Historical financials from their research
3. **Web Search/Fetch** - Current prices, beta, debt and cash when needed

**Validation Checklist:**
- Verify net debt vs net cash (critical for valuation)
- Confirm diluted shares outstanding (check for recent buybacks/issuances)
- Validate historical margins are consistent with business model
- Cross-check revenue growth rates with industry benchmarks
- Verify tax rate is reasonable (typically 21-28%)

### Step 2: Historical Analysis (3-5 years)

Analyze and document:
- **Revenue growth trends**: Calculate CAGR, identify drivers
- **Margin progression**: Track gross margin, EBIT margin, FCF margin
- **Capital intensity**: D&A and CapEx as % of revenue
- **Working capital efficiency**: NWC changes as % of revenue growth
- **Return metrics**: ROIC, ROE trends

Create summary tables showing:
```
Historical Metrics (LTM):
Revenue: $X million
Revenue growth: X% CAGR
Gross margin: X%
EBIT margin: X%
D&A % of revenue: X%
CapEx % of revenue: X%
FCF margin: X%
```

### Step 3: Build Revenue Projections

**Methodology:**
1. Start with latest actual revenue (LTM or most recent fiscal year)
2. Apply growth rates for each projection year
3. Show both dollar amounts AND calculated growth %

**Growth Rate Framework:**
- Year 1-2: Higher growth reflecting near-term visibility
- Year 3-4: Gradual moderation toward industry average
- Year 5+: Approaching terminal growth rate

**Formula structure:**
- Revenue(Year N) = Revenue(Year N-1) × (1 + Growth Rate)
- Growth %(Year N) = Revenue(Year N) / Revenue(Year N-1) - 1

**Three-scenario approach:**
```
Bear Case: Conservative growth (e.g., 8-12%)
Base Case: Most likely scenario (e.g., 12-16%)
Bull Case: Optimistic growth (e.g., 16-20%)
```

### Step 4: Operating Expense Modeling

**Fixed/Variable Cost Analysis:**

Operating expenses should model realistic operating leverage:
- **Sales & Marketing**: Typically 15-40% of revenue depending on business model
- **Research & Development**: Typically 10-30% for technology companies
- **General & Administrative**: Typically 8-15% of revenue, shows leverage as company scales

**Key principles:**
- ALL percentages based on REVENUE, not gross profit
- Model operating leverage: % should decline as revenue scales
- Maintain separate line items for S&M, R&D, G&A
- Calculate EBIT = Gross Profit - Total OpEx

**Margin expansion framework:**
```
Current State → Target State (Year 5)
Gross Margin: X% → Y% (justify based on scale, efficiency)
EBIT Margin: X% → Y% (result of revenue growth + opex leverage)
```

### Step 5: Free Cash Flow Calculation

**Build FCF in proper sequence:**

```
EBIT
(-) Taxes (EBIT × Tax Rate)
= NOPAT (Net Operating Profit After Tax)
(+) D&A (non-cash expense, % of revenue)
(-) CapEx (% of revenue, typically 4-8%)
(-) Δ NWC (change in working capital)
= Unlevered Free Cash Flow
```

**Working Capital Modeling:**
- Calculate as % of revenue change (delta revenue)
- Typical range: -2% to +2% of revenue change
- Negative number = source of cash (working capital release)
- Positive number = use of cash (working capital build)

**Maintenance vs Growth CapEx:**
- Maintenance CapEx: Sustains current operations (~2-3% revenue)
- Growth CapEx: Supports expansion (additional 2-5% revenue)
- Total CapEx should align with company's growth strategy

### Step 6: Cost of Capital (WACC) Research

**CAPM Methodology for Cost of Equity:**

```
Cost of Equity = Risk-Free Rate + Beta × Equity Risk Premium

Where:
- Risk-Free Rate = Current 10-Year Treasury Yield
- Beta = 5-year monthly stock beta vs market index
- Equity Risk Premium = 5.0-6.0% (market standard)
```

**Cost of Debt Calculation:**

```
After-Tax Cost of Debt = Pre-Tax Cost of Debt × (1 - Tax Rate)

Determine Pre-Tax Cost of Debt from:
- Credit rating (if available)
- Current yield on company bonds
- Interest expense / Total Debt from financials
```

**Capital Structure Weights:**

```
Market Value Equity = Current Stock Price × Shares Outstanding
Net Debt = Total Debt - Cash & Equivalents
Enterprise Value = Market Cap + Net Debt

Equity Weight = Market Cap / Enterprise Value
Debt Weight = Net Debt / Enterprise Value

WACC = (Cost of Equity × Equity Weight) + (After-Tax Cost of Debt × Debt Weight)
```

**Special Cases:**
- **Net Cash Position**: If Cash > Debt, Net Debt is NEGATIVE
  - Debt Weight may be negative
  - WACC calculation adjusts accordingly
- **No Debt**: WACC = Cost of Equity

**Typical WACC Ranges:**
- Large Cap, Stable: 7-9%
- Growth Companies: 9-12%
- High Growth/Risk: 12-15%

### Step 7: Discount Rate Application (5-10 Year Forecast)

**Mid-Year Convention:**
- Cash flows assumed to occur mid-year
- Discount Period: 0.5, 1.5, 2.5, 3.5, 4.5, etc.
- Discount Factor = 1 / (1 + WACC)^Period

**Present Value Calculation:**
```
For each projection year:
PV of FCF = Unlevered FCF × Discount Factor

Example (Year 1):
FCF = $1,000
WACC = 10%
Period = 0.5
Discount Factor = 1 / (1.10)^0.5 = 0.9535
PV = $1,000 × 0.9535 = $954
```

**Projection Period Selection:**
- **5 years**: Standard for most analyses
- **7-10 years**: High growth companies with longer runway
- **3 years**: Mature, stable businesses

### Step 8: Terminal Value Calculation

**Perpetuity Growth Method (Preferred):**

```
Terminal FCF = Final Year FCF × (1 + Terminal Growth Rate)
Terminal Value = Terminal FCF / (WACC - Terminal Growth Rate)

Critical Constraint: Terminal Growth < WACC (otherwise infinite value)
```

**Terminal Growth Rate Selection:**
- Conservative: 2.0-2.5% (GDP growth rate)
- Moderate: 2.5-3.5%
- Aggressive: 3.5-5.0% (only for market leaders)

**Do not exceed**: Risk-free rate or long-term GDP growth

**Exit Multiple Method (Alternative):**
```
Terminal Value = Final Year EBITDA × Exit Multiple

Where Exit Multiple comes from:
- Industry comparable trading multiples
- Precedent transaction multiples
- Typical range: 8-15x EBITDA
```

**Present Value of Terminal Value:**
```
PV of Terminal Value = Terminal Value / (1 + WACC)^Final Period

Where Final Period accounts for timing:
5-year model with mid-year convention: Period = 4.5
```

**Terminal Value Sanity Check:**
- Should represent 50-70% of Enterprise Value
- If >75%, model may be over-reliant on terminal assumptions
- If <40%, check if terminal assumptions are too conservative

### Step 9: Enterprise to Equity Value Bridge

**Valuation Summary Structure:**

```
(+) Sum of PV of Projected FCFs = $X million
(+) PV of Terminal Value = $Y million
= Enterprise Value = $Z million

(-) Net Debt [or + Net Cash if negative] = $A million
= Equity Value = $B million

÷ Diluted Shares Outstanding = C million shares
= Implied Price per Share = $XX.XX

Current Stock Price = $YY.YY
Implied Return = (Implied Price / Current Price) - 1 = XX%
```

**Critical Adjustments:**
- **Net Debt = Total Debt - Cash & Equivalents**
  - If positive: Subtract from EV (reduces equity value)
  - If negative (Net Cash): Add to EV (increases equity value)
- **Use Diluted Shares**: Includes options, RSUs, convertible securities
- **Other adjustments** (if applicable):
  - Minority interests
  - Pension liabilities
  - Operating lease obligations

**Valuation Output Format:**
```csv
Valuation Component,Amount ($M)
PV Explicit FCFs,X.X
PV Terminal Value,Y.Y
Enterprise Value,Z.Z
(-) Net Debt,A.A
Equity Value,B.B
,,
Shares Outstanding (M),C.C
Implied Price per Share,$XX.XX
Current Share Price,$YY.YY
Implied Upside/(Downside),+XX%
```

### Step 10: Sensitivity Analysis

Build **three sensitivity tables** at the bottom of the DCF sheet showing how valuation changes with different assumptions:

1. **WACC vs Terminal Growth** - Shows enterprise value sensitivity to discount rate and perpetuity growth
2. **Revenue Growth vs EBIT Margin** - Shows impact of top-line growth and operating leverage
3. **Beta vs Risk-Free Rate** - Shows sensitivity to cost of equity components

**Implementation**: These are simple 2D grids (NOT Excel's "Data Table" feature) with formulas in each cell. Each cell must contain a full DCF recalculation for that specific assumption combination. See Critical Constraints section for detailed requirements on populating all 75 cells programmatically using openpyxl.


## Correct patterns and common mistakes

Before laying out rows, read [`references/patterns-and-mistakes.md`](references/patterns-and-mistakes.md). It shows the correct scenario blocks, revenue and FCF formulas, cell comments, assumption tables, row planning, and sensitivity tables, followed by the mistakes that break models. The five most common:

1. **Formula row references off** → Define ALL row positions BEFORE writing formulas
2. **Missing cell comments** → Add comments AS cells are created, not at end
3. **Simplified sensitivity tables** → Populate all cells with full DCF recalc formulas, not approximations
4. **Scenario block references wrong** → Ensure IF formulas pull from correct Bear/Base/Bull blocks
5. **No borders** → Add professional section borders for client-ready appearance

## Excel File Creation

**This skill uses the `xlsx` skill for all spreadsheet operations.** The xlsx skill provides:
- Standardized formula construction rules
- Number formatting conventions
- Automated formula recalculation via `recalc.py` script
- Comprehensive error checking and validation

All Excel files created by this skill must follow xlsx skill requirements, including zero formula errors and proper recalculation.

## Quality Rubric

Every DCF model must maximize for:
1. **Realistic revenue and margin assumptions** based on historical performance
2. **Appropriate cost of capital calculation** with proper CAPM methodology
3. **Comprehensive sensitivity analysis** showing valuation ranges
4. **Clear terminal value calculation** with supporting rationale
5. **Professional model structure** enabling scenario analysis
6. **Transparent documentation** of all key assumptions

## Input Requirements

### Minimum Required Inputs
1. **Company identifier**: Ticker symbol or company name
2. **Growth assumptions**: Revenue growth rates for projection period (or "use consensus")
3. **Optional parameters**:
   - Projection period (default: 5 years)
   - Scenario cases (Bear/Base/Bull growth and margin assumptions)
   - Terminal growth rate (default: 2.5-3.0%)
   - Specific WACC inputs if not using CAPM

## Excel Model Structure

Read [`references/excel-model-structure.md`](references/excel-model-structure.md) before writing the workbook. It covers the sheet architecture, **mandatory formula recalculation** with `recalc.py` after every change, formatting and border standards, the row-by-row DCF and WACC sheet layouts, and the sensitivity grids at the bottom of the DCF sheet.

## Case Selector Implementation

The Bear, Base, and Bull assumption blocks and the case-selector formulas are specified at the end of [`references/excel-model-structure.md`](references/excel-model-structure.md).

## Deliverables Structure

**File naming**: `[Ticker]_DCF_Model_[Date].xlsx`

**Two sheets**:
1. **DCF** - Complete model with Bear/Base/Bull cases + three sensitivity tables at bottom (WACC vs Terminal Growth, Revenue Growth vs EBIT Margin, Beta vs Risk-Free Rate)
2. **WACC** - Cost of capital calculation

**Key features**: Case selector (1/2/3), consolidation column with INDEX/OFFSET formulas, color-coded cells, cell comments on all inputs, professional borders

## Best Practices

### Model Construction
1. **Build incrementally**: Complete each section before moving to next
2. **Test as building**: Enter sample numbers to verify formulas
3. **Use consistent structure**: Similar calculations follow similar patterns
4. **Comment complex formulas**: Add notes for unusual calculations
5. **Build in checks**: Sum checks and balance checks where applicable

### Documentation
1. **Document all assumptions**: Explain reasoning behind key inputs
2. **Cite data sources**: Note where each data point came from
3. **Explain methodology**: Describe any non-standard approaches
4. **Flag uncertainties**: Highlight areas with limited visibility

### Quality Control
1. **Cross-check calculations**: Verify math in multiple ways
2. **Stress test assumptions**: Run sensitivity to ensure model is robust
3. **Peer review**: Have someone else check formulas
4. **Version control**: Save versions as work progresses

## Common Variations

### High-Growth Technology Companies
- Longer projection period (7-10 years)
- Higher initial growth rates (20-30%)
- Significant margin expansion over time
- Higher WACC (12-15%)
- Model unit economics (users, ARPU, etc.)

### Mature/Stable Companies
- Shorter projection period (3-5 years)
- Modest growth rates (GDP +1-3%)
- Stable margins
- Lower WACC (7-9%)
- Focus on cash generation and capital allocation

### Cyclical Companies
- Model through economic cycle
- Normalize margins at mid-cycle
- Consider trough and peak scenarios
- Adjust beta for cyclicality

### Multi-Segment Companies
- Separate DCFs for each business unit
- Different growth rates and margins by segment
- Sum-of-parts valuation
- Consider synergies

## Troubleshooting

**If you encounter errors or unreasonable results, read [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for detailed debugging guidance.**

## Workflow Integration

### At Start of DCF Build

1. **Gather market data**:
   - Check for available MCP servers for current market data
   - Use web search/fetch for stock prices, beta, and other market metrics
   - Request from user if specific data is needed

2. **Gather historical financials**:
   - Check for available MCP servers (Daloopa, etc.)
   - Request from user if not available via MCP
   - Manual extraction from 10-Ks if necessary

3. **Begin model construction** using the DCF methodology detailed in this skill

### During Model Construction

1. **Build Excel model** using openpyxl with formulas (not hardcoded values)
2. **Follow xlsx skill conventions** for formula construction and formatting
3. **Apply fill colors only if requested** by user or if specific brand guidelines are provided

### Before Delivering Model (MANDATORY)

1. **Verify structure**:
   - Scenario blocks for Bear/Base/Bull with assumptions across projection years
   - Case selector functional with formulas referencing correct scenario blocks
   - Sensitivity tables at bottom of DCF sheet (not separate sheet)
   - Font colors: Blue inputs, black formulas, green sheet links
   - Cell comments on ALL hardcoded inputs
   - Professional borders around major sections

2. **Recalculate formulas**: Run `python recalc.py model.xlsx 30`

3. **Check output**:
   - If `status` is `"success"` → Continue to step 4
   - If `status` is `"errors_found"` → Check `error_summary` and read [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for debugging guidance

4. **Fix errors and re-run recalc.py** until status is "success"

5. **Spot-check formulas**:
   - Test one FCF formula - does it reference the correct assumption rows?
   - Change case selector - does the consolidation column update properly?
   - Verify revenue formulas reference consolidation column (not nested IF formulas)

6. **Deliver model**

### Available Data Sources

- **MCP servers**: If configured (Daloopa for historical financials)
- **Web search/fetch**: For current stock prices, beta, and market data
- **User-provided data**: Historical financials, consensus estimates
- **Manual extraction**: SEC EDGAR filings as fallback

## Final Output Checklist

Before delivering DCF model:

**Required:**
- Run `python recalc.py model.xlsx 30` until status is "success" (zero formula errors)
- Two sheets: DCF (with sensitivity at bottom), WACC
- Font colors: Blue=inputs, Black=formulas, Green=sheet links
- Cell comments on ALL hardcoded inputs
- Sensitivity tables fully populated with formulas
- Professional borders around major sections

**Validation:**
- OpEx based on revenue (not gross profit)
- Terminal value 50-70% of EV
- Terminal growth < WACC
- Tax rate 21-28%
- File naming: `[Ticker]_DCF_Model_[Date].xlsx`

## Data sources — MCP first, web fallback

Many passages below say "use the S&P Kensho MCP / Daloopa MCP / FactSet MCP". Those are commercial financial-data MCPs from the original Cowork plugin context. In Hermes:

- **If you have any structured financial-data MCP configured** (Hermes supports MCP — see `native-mcp` skill), prefer it for point-in-time comps, precedent transactions, and filings.
- **Otherwise**, fall back to:
  - `web_search` / `web_extract` against SEC EDGAR (`https://www.sec.gov/cgi-bin/browse-edgar`) for US filings
  - Company IR pages for press releases, earnings decks
  - `browser_navigate` for interactive data portals
  - User-provided data (explicitly ask when the context doesn't have it)
- **Never fabricate**. If a multiple, precedent, or filing number can't be sourced, flag the cell as `[UNSOURCED]` and surface it to the user.

## Attribution

This skill is adapted from Anthropic's Claude for Financial Services plugin suite (Apache-2.0). The Office-JS / Cowork live-Excel paths have been removed; this version targets headless openpyxl via the `excel-author` skill's conventions. Original: https://github.com/anthropics/financial-services

## Source Attribution

Imported from NousResearch Hermes Agent optional skills (optional-skills/finance/dcf-model) under the MIT license. Source: https://github.com/NousResearch/hermes-agent/tree/main/optional-skills/finance/dcf-model

Modified for this collection: the correct-pattern, common-mistake, Excel-structure, and case-selector sections were moved unchanged into `references/`.
