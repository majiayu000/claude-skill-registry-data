---
name: financial-modeling
description: "Use this skill for any financial modeling, valuation, or investment analysis task. This includes: building or reviewing LBO models, DCF valuations, merger/M&A models, comparable company analysis (comps), precedent transaction analysis, accretion/dilution analysis, three-statement financial models, waterfall distributions, IRR/MOIC calculations, sensitivity/scenario analysis, football field valuations, and any Wall Street or PE-grade financial deliverable. Trigger when the user mentions terms like LBO, leveraged buyout, DCF, discounted cash flow, comps, comparable companies, trading multiples, M&A, merger model, accretion dilution, WACC, terminal value, enterprise value, equity value, cap table, sources and uses, debt schedule, IRR, MOIC, returns analysis, purchase price allocation, goodwill, synergies, pro forma, or financial model. Also trigger when the user asks for investment banking, private equity, or hedge fund style analysis, or references Wall Street formatting standards, blue/black font conventions, or banker-grade spreadsheets. Trigger even if the user is casual about it — e.g., 'build me a quick LBO', 'value this company', 'run comps on these names', 'what's the IRR on this deal'. Do NOT trigger for basic accounting questions, simple budgeting, or personal finance tasks unless they explicitly involve the model types above."
---

# Financial Modeling Skill

Build investment banking, private equity, and Wall Street-grade financial models with professional formatting, rigorous methodology, and auditable formulas.

> For shared Nexus domain context, MCP tool references, and quality standards, see [`_shared/plugin-context.md`](../_shared/plugin-context.md).

## Prerequisites

This skill works with or without MCP connections. Check availability at the start of execution.

| Dependency | Required? | Purpose |
|------------|-----------|---------|
| **Nexus MCP Server** | Optional | `nexus_run_model` for automated model execution, `nexus_get_deal` / `nexus_get_cre_asset` for deal data |
| **Financial data connectors** | Optional | BigData.com, PitchBook, S&P/Kensho for company financials and market data |
| **User-provided data** | Fallback | Paste financials, upload documents, or type deal parameters manually |

**Graceful degradation**: If MCP tools are unavailable, prompt the user to provide financial data directly. All analytical logic works regardless of data source.

## Before You Start

Read the relevant reference file(s) for the model type requested:

| Model Type | Reference File | When to Use |
|---|---|---|
| LBO / Leveraged Buyout | `references/lbo.md` | PE acquisitions, returns analysis, debt paydown |
| DCF / Valuation | `references/dcf.md` | Intrinsic value, WACC, terminal value |
| M&A / Merger Model | `references/merger.md` | Accretion/dilution, synergies, pro forma |
| Comps & Precedents | `references/comps.md` | Trading multiples, transaction multiples |
| Formatting Standards | `references/formatting.md` | Always read this — applies to every model |

For complex requests (e.g., "full LBO with comps-based entry"), read multiple reference files.

## Core Principles

### 1. Formula Integrity
Every financial model must be formula-driven, not hardcoded. The model should recalculate dynamically when any input changes.

- ALL assumptions go in clearly labeled assumption cells (blue font)
- ALL calculations reference assumption cells (black font)
- ZERO hardcoded values inside formulas
- ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)

### 2. Wall Street Color Coding
This is non-negotiable for professional models:

- **Blue font (0,0,255)**: Hardcoded inputs and assumptions
- **Black font (0,0,0)**: Formulas and calculations
- **Green font (0,128,0)**: Cross-sheet references within the workbook
- **Red font (255,0,0)**: External links to other files
- **Yellow highlight**: Key assumptions requiring attention

### 3. Number Formatting
- Currency: `$#,##0` or `$#,##0.0` with units in headers (e.g., "Revenue ($mm)")
- Percentages: `0.0%` (one decimal default)
- Multiples: `0.0x` (e.g., EV/EBITDA, P/E, debt/EBITDA)
- Years: Plain text, never comma-formatted
- Negatives: Parentheses `(123)` not minus `-123`
- Zeros: Display as dash `"-"` using custom format `$#,##0;($#,##0);"-"`

### 4. Sheet Architecture
Standard tab order for multi-sheet models:

1. **Cover / Summary** — Key outputs, returns, valuation range
2. **Assumptions** — All inputs consolidated
3. **Income Statement** — P&L build (historical + projected)
4. **Balance Sheet** — Assets, liabilities, equity
5. **Cash Flow Statement** — CFO, CFI, CFF, FCF
6. **Supporting Schedules** — Debt schedule, depreciation, working capital, etc.
7. **Valuation / Returns** — DCF, LBO returns, comps output
8. **Sensitivity Tables** — Data tables on key variables

### 5. Time Axis Convention
- Historical periods: labeled as actuals (e.g., "FY2022A", "FY2023A")
- Projected periods: labeled as estimates (e.g., "FY2024E", "FY2025E")
- Consistent left-to-right chronological flow
- Column A reserved for line item labels

### 6. Sign Convention
Choose one convention and apply it consistently:
- **Recommended**: Revenue positive, expenses positive, net income = revenue - expenses
- Clearly label any sign-flipped items (e.g., "D&A (add back)" or use parentheses)
- Cash outflows in cash flow statement should be negative or clearly labeled

## Model Construction Workflow

### Step 1: Clarify Scope
Before building, confirm:
- What model type(s) are needed?
- What level of detail? (Quick-and-dirty vs. full bank-grade)
- What are the key outputs? (IRR, valuation range, accretion/dilution, etc.)
- Are there specific assumptions or data points provided?
- What's the audience? (IC memo, client pitch, internal analysis)

### Step 2: Gather Data
Use the source hierarchy defined in `_shared/plugin-context.md`:
1. **Uploaded materials** (CIM, financials, credit agreements) — highest authority
2. **Nexus MCP tools** — use `nexus_get_deal` or `nexus_get_cre_asset` for platform data, or `nexus_run_model` for automated execution
3. **Financial data connectors** — BigData.com tearsheets, PitchBook data, S&P/Kensho financials
4. **SEC EDGAR** — public filings (10-K, 10-Q)
5. **User-provided data** — manual input as fallback

If no automated sources are available, ask the user to provide: revenue, EBITDA, growth rates, capital structure, and any deal-specific assumptions.

### Step 3: Build the Assumptions Sheet First
Always start with assumptions. This forces discipline and makes the model auditable.

### Step 4: Construct the Model
Follow the methodology in the relevant reference file. Build formulas that chain cleanly from assumptions through calculations to outputs.

### Step 5: Add Sensitivity Analysis
Every model should include at least one sensitivity table on the key value drivers. Use Excel DATA TABLE functionality or manual two-way tables.

### Step 6: Format to Wall Street Standards
Apply the formatting standards from `references/formatting.md`. The model should look like it came from a bulge bracket bank.

### Step 7: Verify and Validate
- Run formula error check (zero errors required)
- Verify balance sheet balances (Assets = L + E, every period)
- Check that cash flow statement reconciles to change in cash on B/S
- Confirm circular reference handling if model has circularity (e.g., interest on average debt)
- Test with extreme assumptions to ensure no broken formulas

## Data Retrieval Patterns

### With Nexus MCP Connected
```
Use nexus_run_model MCP tool with:
  - modelType: "lbo" | "dcf" | "merger" | "comps"
  - dealId: [Nexus deal ID if modeling an existing deal]
  - assumptions: { ... override defaults ... }

Use nexus_get_deal for deal-specific financials and scoring.
Use nexus_get_cre_asset for property-level T12, rent roll, and lease data.
Use nexus_search_market for comparable company identification.
```

### Without MCP (Manual Mode)
Prompt the user for:
- Company name and industry
- Historical financials (revenue, EBITDA, net income, assets, liabilities)
- Growth assumptions and margin targets
- Capital structure (debt levels, interest rates)
- Deal-specific parameters (entry multiple, hold period, exit assumptions)

### LBO Model Example (TypeScript)

```typescript
// Quick LBO returns calculation for deal screening

interface LBOAssumptions {
  entryEVMultiple: number    // e.g., 8.0x EBITDA
  exitEVMultiple: number     // e.g., 9.0x EBITDA
  ltmEBITDA: number          // e.g., 62_500_000
  revenueGrowth: number      // e.g., 0.08 (8%)
  ebitdaMargin: number       // e.g., 0.20
  seniorDebtMultiple: number // e.g., 3.5x
  mezzDebtMultiple: number   // e.g., 1.5x
  holdPeriod: number         // e.g., 5 years
}

function calculateLBOReturns(a: LBOAssumptions) {
  const entryEV = a.entryEVMultiple * a.ltmEBITDA
  const totalDebt = (a.seniorDebtMultiple + a.mezzDebtMultiple) * a.ltmEBITDA
  const sponsorEquity = entryEV - totalDebt

  // Project exit EBITDA (simplified: grow revenue, apply margin)
  const ltmRevenue = a.ltmEBITDA / a.ebitdaMargin
  const exitRevenue = ltmRevenue * Math.pow(1 + a.revenueGrowth, a.holdPeriod)
  const exitEBITDA = exitRevenue * a.ebitdaMargin
  const exitEV = a.exitEVMultiple * exitEBITDA

  // Assume 50% debt paydown over hold period (simplified)
  const remainingDebt = totalDebt * 0.5
  const exitEquity = exitEV - remainingDebt

  const moic = exitEquity / sponsorEquity
  const irr = Math.pow(moic, 1 / a.holdPeriod) - 1

  return { entryEV, sponsorEquity, exitEV, exitEquity, moic, irr }
}

// Example: $500M deal at 8.0x entry, 9.0x exit, 5-year hold
// Returns: { moic: 2.8x, irr: 22.9% }
```

### DCF Model Example (TypeScript)

```typescript
// DCF valuation with WACC and terminal value

function calculateDCF(params: {
  projectedFCF: number[]  // e.g., [45, 49, 53, 58, 63] ($M, years 1-5)
  wacc: number            // e.g., 0.10 (10%)
  terminalGrowthRate: number // e.g., 0.025 (2.5%)
  netDebt: number         // e.g., 200_000_000
  sharesOutstanding: number // e.g., 50_000_000
}) {
  const { projectedFCF, wacc, terminalGrowthRate, netDebt, sharesOutstanding } = params

  // PV of projected cash flows
  const pvFCF = projectedFCF.map((fcf, i) =>
    fcf / Math.pow(1 + wacc, i + 1)
  )
  const sumPVFCF = pvFCF.reduce((sum, pv) => sum + pv, 0)

  // Terminal value (Gordon Growth Model)
  const lastFCF = projectedFCF[projectedFCF.length - 1]
  const terminalValue = (lastFCF * (1 + terminalGrowthRate)) / (wacc - terminalGrowthRate)
  const pvTerminal = terminalValue / Math.pow(1 + wacc, projectedFCF.length)

  const enterpriseValue = sumPVFCF + pvTerminal
  const equityValue = enterpriseValue - netDebt
  const impliedSharePrice = equityValue / sharesOutstanding

  return { enterpriseValue, equityValue, impliedSharePrice, terminalValue, pvTerminal }
}

// Example: 5-year FCF projection, 10% WACC, 2.5% terminal growth
// Returns: { enterpriseValue: $840M, impliedSharePrice: $12.80 }
```

### Quick Reference: Key Formulas

| Metric | Formula |
|---|---|
| Enterprise Value | Equity Value + Net Debt + Minority Interest + Preferred |
| Equity Value | Share Price x Diluted Shares Outstanding |
| FCF (Unlevered) | EBIT(1-t) + D&A - CapEx - deltaWC |
| FCF (Levered) | Net Income + D&A - CapEx - deltaWC - Debt Repayment |
| WACC | (E/V) x Re + (D/V) x Rd x (1-t) |
| Terminal Value (Gordon) | FCF1 / (WACC - g) |
| Terminal Value (Exit Multiple) | EBITDA_terminal x Exit Multiple |
| IRR | Solve for r: sum of CFt/(1+r)^t = 0 |
| MOIC | Total Distributions / Total Invested Capital |
| Accretion/Dilution | (Pro Forma EPS - Standalone EPS) / Standalone EPS |

## Output Expectations

Every financial model deliverable should include:
1. **Executive summary** — Key outputs in 3-5 bullet points at the top
2. **Assumption transparency** — Every input clearly labeled and sourced
3. **Sensitivity analysis** — At minimum, a 2-way table on the most impactful variables
4. **Clean formatting** — Wall Street color coding, proper number formats, frozen panes
5. **No errors** — Zero formula errors, balanced balance sheet, reconciled cash flows

## Confidence Calibration

Every model output must include a calibrated confidence assessment per the AGI protocol in `_shared/plugin-context.md`:

```
## Confidence Assessment
- **Score**: 0.XX (0.0 = no confidence, 1.0 = full confidence)
- **Calibration**: conservative | neutral | optimistic
- **Confidence Drivers**: [data quality, assumption defensibility, model complexity]
- **Data Gaps**: [missing inputs, stale data, unverified assumptions]
```

**Model-specific confidence factors**:
- **Data freshness**: Are financials from latest filings or stale?
- **Assumption basis**: Management guidance vs. analyst consensus vs. estimated?
- **Comparable quality**: How tight is the comp set? How recent are precedent transactions?
- **Sensitivity range**: Wide output range = lower confidence in point estimate
- **Balance sheet integrity**: Does B/S balance? Does CF reconcile?

**Three-pass calibration**: Run the model at conservative, base, and optimistic assumptions. Report all three scenarios. High consistency across passes = high confidence.

## Excel Generation

For Excel output, use openpyxl patterns defined in `references/formatting.md`. When building spreadsheets:
- Apply named ranges for key assumptions to improve auditability
- Use `freeze_panes` to lock headers and row labels
- Apply print areas and page setup for clean printing
- Use conditional formatting for sensitivity heat maps

## Related Skills
- `/fund-benchmarker` — Benchmark fund IRR, MOIC, DPI vs vintage year, strategy, and geography peers
- `/comps` — Detailed comparable company and precedent transaction analysis
- `/deal-memo-writer` — Structure IC-ready deal memos with financial analysis
- `/quick-cut` — SVP Quick-Cut credit memo with 10-agent ensemble
- `/cre-underwriter` — CRE-specific underwriting and pro forma modeling
- `/scenario-modeler` — Build base, bull, and bear investment scenarios
