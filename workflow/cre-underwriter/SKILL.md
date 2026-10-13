---
name: cre-underwriter
description: "Full CRE underwriting workflow. Process offering memorandums through underwriting engine to produce ICM-ready analysis. Covers NOI analysis, cap rate comps, DSCR, LTV, sensitivity tables, return projections. Use when underwriting CRE deals, running deal analysis, or preparing investment committee materials."
---

# /cre-underwriter -- CRE Deal Underwriting Engine

Execute the full CRE underwriting workflow from OM ingestion through ICM-ready analysis output.

> Before executing, read `_shared/plugin-context.md` for Nexus domain vocabulary, MCP tool references, and quality standards.

## Prerequisites

**Required**: Property financial data -- T12 operating statement, rent roll, and acquisition assumptions. Can come from MCP tools, `/om-parser` output, or manual input.

**Optional MCP Connections** (enhance automation):
- **Nexus MCP** (`nexus.syntari-ai.com/api/mcp`) -- `nexus_get_cre_asset`, `nexus_underwrite_cre` for automated underwriting pipeline
- **BigData.com MCP** (via `financial-analysis` plugin) -- market data for cap rate comps and rent growth assumptions
- **Box MCP** -- data room documents (T12 statements, rent rolls, environmental reports)
- **Egnyte MCP** -- alternative data room access

**Graceful Degradation**: If MCP tools are not connected, provide property data manually (paste T12, upload rent roll, describe assumptions). All underwriting calculations, sensitivity matrices, and return analysis work identically with manual input.

## When to Use
- Underwriting a new CRE acquisition opportunity from an OM or broker package
- Running sensitivity analysis on deal assumptions (cap rate, rent growth, exit timing)
- Preparing financial analysis for investment committee presentation
- Comparing multiple deal scenarios (base, upside, downside) for IC memo
- Re-underwriting an existing deal after assumption changes (rate movement, new comps)
- Validating a broker's pro forma against independent market assumptions

## Underwriting Checklist

### Income Analysis
- [ ] Gross Potential Rent (in-place vs market)
- [ ] Vacancy & credit loss (actual vs market)
- [ ] Other income (parking, laundry, fees)
- [ ] Rent growth assumptions (year-by-year)
- [ ] Mark-to-market opportunity

### Expense Analysis
- [ ] Operating expenses by line item
- [ ] Real estate taxes (current + projected)
- [ ] Insurance
- [ ] Management fee (% of EGI)
- [ ] Replacement reserves (per unit/SF)
- [ ] Expense growth assumptions

### Capital Markets
- [ ] Acquisition cap rate vs market comps
- [ ] Exit cap rate assumption
- [ ] Loan terms (rate, term, amortization, IO period)
- [ ] LTV and DSCR constraints
- [ ] Equity requirement

### Return Metrics
- [ ] Levered IRR (5-year, 7-year, 10-year hold)
- [ ] Equity multiple
- [ ] Cash-on-cash return (Year 1, stabilized)
- [ ] Sensitivity matrix (cap rate x rent growth)

## Data Shapes

### Underwriting Input

```typescript
interface UnderwritingInput {
  propertyName: string
  propertyType: 'Multifamily' | 'Office' | 'Retail' | 'Industrial' | 'Mixed-Use'
  acquisitionPrice: number      // Total purchase price ($)
  capRate: number               // Going-in cap rate (decimal, e.g., 0.0525)
  noiYear1: number              // Year 1 NOI ($)
  rentGrowthPct: number         // Annual rent growth (decimal, e.g., 0.03)
  expenseGrowthPct: number      // Annual expense growth (decimal, e.g., 0.03)
  loanLTV: number               // Loan-to-value (decimal, e.g., 0.65)
  loanRate: number              // Interest rate (decimal, e.g., 0.055)
  loanTermYears: number         // Loan term in years
  loanAmortYears: number        // Amortization period in years
  ioYears: number               // Interest-only period in years
  exitCapRate: number           // Exit cap rate (decimal)
  holdPeriodYears: number       // Hold period in years
}
```

### Underwriting Result

```typescript
interface UnderwritingResult {
  proForma: {
    year: number
    noi: number
    debtService: number
    cashFlow: number
    cashOnCash: number          // Percentage
  }[]
  returnMetrics: {
    leveredIRR: number          // Percentage
    unleveredIRR: number        // Percentage
    equityMultiple: number      // Multiple (x)
    cashOnCashYear1: number     // Percentage
    cashOnCashStabilized: number // Percentage
  }
  sensitivity: {
    rows: {
      exitCap: number
      irr5yr: number
      irr7yr: number
      irr10yr: number
    }[]
  }
  dscr: number                  // Debt service coverage ratio
  ltv: number                   // Loan-to-value
  equityRequired: number        // Total equity investment ($)
  debtYield: number             // NOI / Loan Amount
}
```

## Workflow

### Step 1: Ingest Data
- **With Nexus MCP**: Use `nexus_get_cre_asset` for existing assets or `nexus_underwrite_cre` for the full automated pipeline.
- **From /om-parser**: Accept the `OMExtractedData` output as input.
- **Without MCP**: Ask the user for property financials, T12, rent roll, and acquisition assumptions.

### Step 2: Build Pro Forma
Construct year-by-year pro forma projections:
- Revenue schedule with rent growth
- Expense schedule with inflation
- NOI by year
- Debt service schedule (interest-only period then amortizing)

### Step 3: Run Return Analysis
Calculate for each hold period scenario:
- IRR (levered and unlevered) using XIRR / Newton-Raphson
- Equity multiple (total distributions / total equity invested)
- Cash-on-cash by year
- Residual value at exit cap rate

### Step 4: Sensitivity Analysis
Generate matrices varying:
- Entry cap rate vs exit cap rate
- Rent growth vs expense growth
- Interest rate scenarios
- Hold period variations

### Step 5: Generate Output
Produce underwriting summary matching the ICM financial analysis section format.

## CRE Formula Reference

### Income Waterfall (P&L Cascade)

```
Gross Potential Rent (GPR)
  = Sum(unit_count_i * market_rent_i * 12) for all unit types i
  (Multifamily: by unit type -- Studio, 1BR, 2BR, 3BR)
  (Office/Retail/Industrial: by tenant lease -- base_rent_psf * leased_sf)

- Loss to Lease (LTL)
  = GPR - Sum(unit_count_i * in_place_rent_i * 12)

- Physical Vacancy
  = GPR * physical_vacancy_rate
  (Typical: 3-5% stabilized MF, 5-10% office, 3-8% industrial)

- Concessions
  = Sum(free_rent_months_i * monthly_rent_i) amortized over lease_term

- Credit Loss / Bad Debt
  = EGI * credit_loss_rate (typically 0.5-1.5%)

+ Other Income
  = parking + laundry + pet_fees + late_fees + application_fees
    + storage_income + utility_reimbursements + antenna/rooftop_income

= Effective Gross Income (EGI)

- Operating Expenses:
    Payroll & Benefits.............. ($1,200-2,500/unit/yr MF)
    Repairs & Maintenance.......... ($800-1,500/unit/yr)
    Utilities (owner-paid)......... ($600-1,200/unit/yr)
    Contract Services.............. ($300-600/unit/yr)
    Marketing & Advertising........ ($150-400/unit/yr)
    General & Administrative....... ($300-600/unit/yr)
    Management Fee................. EGI * mgmt_fee_pct (3-5%)
    Insurance...................... ($400-800/unit/yr)
    Real Estate Taxes.............. market-specific
    Replacement Reserves........... units * reserves_per_unit ($250-500/unit/yr)

= Net Operating Income (NOI)

- Annual Debt Service

= Before-Tax Cash Flow (BTCF)

- Capital Expenditures (non-recurring)

= Net Cash Flow (NCF)
```

**RE Tax Note -- Prop 13 States (CA):** Assessment resets to purchase price on change of ownership. Budget for: Purchase_Price * local_millage_rate.

### Mark-to-Market / Loss-to-Lease (3 Methods)

**Default: Method 2 -- Lease Tradeout**

```
Method 1 -- Linear (Industry Standard):
  LTL_per_unit = market_rent - in_place_rent
  Total_LTL = Sum(LTL_per_unit_i * 1) for all occupied units
  MTM_pct = Total_LTL / GPR

Method 2 -- Lease Tradeout (Default):
  For each lease signed in trailing 12 months:
    tradeout_delta = new_lease_rent - prior_lease_rent
    organic_growth = prior_rent * submarket_annual_growth_rate / 12
    renovation_premium = reno_cost_per_unit * target_reno_roi / (lease_term_months * 12)
    pure_mtm = tradeout_delta - organic_growth - renovation_premium

  Portfolio_MTM = weighted_avg(pure_mtm_i, weight=unit_count_per_type)
  Embedded_Upside = Portfolio_MTM * occupied_units * 12

  Advantage: Uses ACTUAL lease data, not external market assumptions.
  Isolates organic growth and renovation premiums from true mark-to-market.

Method 3 -- Exponential Catch-Up:
  For units with below-market rents:
    gap = market_rent - in_place_rent
    years_remaining = remaining_lease_months / 12
    annual_bump = gap * (1 - (1 - catch_up_rate)^years_remaining)
```

### Concession Burn-Off

```
For each unit with active concessions:
  concession_monthly_value = (free_months * monthly_rent) / lease_term_months
  effective_rent = gross_rent - concession_monthly_value

Three burn-off methods:
  Linear (default): evenly distributes capture over stabilization period
  Exponential: faster capture in early months, decelerating
  Discrete: jumps at specific lease renewal dates

Conversion: "1 month free" = monthly_rent / lease_term * 12 = X% annual discount
  12-month lease, 1 month free = 8.3% effective discount
  13-month lease, 1 month free = 7.7% effective discount
```

### Debt Service & Amortization

```
Loan_Amount = Purchase_Price * LTV

Monthly Payment (amortizing):
  PMT = P * [r(1+r)^n] / [(1+r)^n - 1]
  Where: P = loan_principal, r = annual_rate / 12, n = amortization_years * 12

Monthly Payment (interest-only period):
  PMT_IO = P * r (interest only, no principal reduction)

Annual_Debt_Service = PMT * 12

DSCR = NOI / Annual_Debt_Service
  Minimum: 1.20x (aggressive) | Standard: 1.25x | Conservative: 1.35x

LTV = Loan_Amount / Property_Value
  Maximum: 65% (conservative) | 70% (standard) | 75% (aggressive)

Debt_Yield = NOI / Loan_Amount
  Minimum: 8% (aggressive) | 10% (standard) | 12% (conservative)
```

### Return Metrics

```
XIRR (Newton-Raphson):
  Find r such that: Sum(CF_i / (1 + r)^((date_i - date_0) / 365)) = 0

  Cash flow timeline:
    t=0: -Equity_Invested (negative -- outflow)
    t=1..n: BTCF per year (positive -- inflow)
    t=n: + Net_Sale_Proceeds (positive -- exit)

Equity_Multiple (MOIC) = Total_Distributions / Total_Equity_Invested

Cash_on_Cash = Annual_BTCF / Initial_Equity * 100
  Year 1 CoC: often 3-6% for value-add, 5-8% for core
  Stabilized CoC: should trend higher as NOI grows and debt is constant

Unlevered_IRR = XIRR on cash flows BEFORE debt service
Levered_IRR = XIRR on cash flows AFTER debt service
  Levered > Unlevered when positive leverage (cap rate > cost of debt)

Residual_Value = NOI_at_exit / Exit_Cap_Rate
Net_Sale_Proceeds = Residual_Value - Disposition_Costs - Loan_Balance - Prepay_Penalty

Yield_on_Cost = Stabilized_NOI / Total_Project_Cost
  (Used for value-add and development)

Development_Spread = Yield_on_Cost - Market_Cap_Rate
  (Positive spread = value creation; target 100-200bps)
```

### Sources & Uses Template

```
SOURCES:                              USES:
Senior Debt........... $XX.XM (XX%)   Purchase Price....... $XX.XM
Mezzanine Debt........ $XX.XM (XX%)   Closing Costs........ $XX.XM (1.5-2.5%)
Preferred Equity...... $XX.XM (XX%)   Acquisition Fee...... $XX.XM (0.5-1.0%)
GP Equity............. $XX.XM (XX%)   Title/Recording...... $XX.XM
LP Equity............. $XX.XM (XX%)   Legal/Due Diligence.. $XX.XM
                                       Capex Reserve........ $XX.XM
                                       Working Capital...... $XX.XM
TOTAL SOURCES......... $XX.XM         TOTAL USES........... $XX.XM
```

### Sensitivity Matrix Defaults

Generate 4 standard matrices:
1. **Exit Cap Rate x Rent Growth -> Levered IRR** (primary)
2. **Entry Cap Rate x Exit Cap Rate -> Equity Multiple**
3. **Hold Period x Exit Cap Rate -> Levered IRR**
4. **LTV x Interest Rate -> DSCR**

Each matrix: 5x5 grid, +/-2 increments around base case, color-coded (green > target, yellow = marginal, red < hurdle).

## Customization Points

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mark_to_market_method` | enum | `"lease_tradeout"` | MTM method: linear, lease_tradeout, exponential |
| `default_vacancy_rate` | object | `{"multifamily":0.05,"office":0.08,"industrial":0.05,"retail":0.07}` | Default physical vacancy by type |
| `default_expense_growth` | number | `0.03` | Annual operating expense inflation rate |
| `default_mgmt_fee_pct` | number | `0.04` | Management fee as % of EGI |
| `default_reserves_per_unit` | number | `300` | Annual replacement reserves per unit |
| `credit_loss_rate` | number | `0.01` | Bad debt / credit loss as % of EGI |
| `disposition_cost_pct` | number | `0.025` | Transaction costs on sale |
| `exit_cap_spread` | number | `0.0025` | Exit cap = entry cap + this spread (25bps default) |
| `irr_hurdle_rates` | array | `[0.08, 0.12, 0.15, 0.18]` | IRR hurdles for sensitivity color-coding |
| `sensitivity_matrix_dimensions` | number | `5` | Grid size for sensitivity tables (5x5 default) |
| `concession_burnoff_method` | enum | `"linear"` | Concession burn-off: linear, exponential, discrete |
| `reno_roi_target` | number | `0.20` | Target renovation ROI (20%) for premium isolation |

Users can override any of these defaults by specifying values when invoking the skill.

## Sample Output

```
CRE UNDERWRITING SUMMARY -- 245 Park Avenue, Office
================================================================
Acquisition: $185,000,000 | Cap Rate: 5.25% | NOI (T12): $9,712,500

PRO FORMA (5-YEAR):
Year    NOI          Debt Service   Cash Flow    CoC
  1     $9,712,500   $6,843,750     $2,868,750   4.4%
  2     $10,004,875  $6,843,750     $3,161,125   4.8%
  3     $10,305,021  $6,843,750     $3,461,271   5.3%
  4     $10,614,172  $6,843,750     $3,770,422   5.8%
  5     $10,932,597  $6,843,750     $4,088,847   6.3%

RETURN METRICS:
  Levered IRR (5yr):     14.8%    Unlevered IRR: 8.2%
  Equity Multiple:       1.92x    DSCR: 1.42x
  LTV: 65.0%             Equity Required: $64,750,000

SENSITIVITY -- Levered IRR by Exit Cap Rate:
  Exit Cap   5yr IRR   7yr IRR   10yr IRR
  4.75%      18.2%     16.1%     14.5%
  5.00%      16.4%     14.8%     13.6%
  5.25%      14.8%     13.7%     12.8%
  5.50%      13.3%     12.6%     12.0%
  5.75%      11.9%     11.6%     11.3%
================================================================
```

## Workflow Chain

This skill is step 3 in the CRE deal chain: `/om-parser` -> `/deal-screener` -> **`/cre-underwriter`** -> ICM drafting.

## Related Skills
- `/om-parser` -- Parse offering memorandums to extract CRE deal data for underwriting
- `/deal-screener` -- Screen and score CRE deals before or after underwriting
- `/deal-memo-writer` -- Write CRE investment memos from underwriting output
- `/financial-modeling` -- LBO, DCF, M&A models for PE-style analysis of CRE deals
- `/portfolio-analyzer` -- Analyze CRE portfolio-level metrics across multiple assets

## Confidence Calibration

Every underwriting output must include a calibrated confidence assessment:

```
## Confidence Assessment
- **Score**: 0.XX (0.0 = no confidence, 1.0 = full confidence)
- **Calibration**: conservative | neutral | optimistic
- **Confidence Drivers**: [what supports the score -- e.g., "complete T12 provided", "rent roll with lease expiries", "market comps available"]
- **Data Gaps**: [what's missing that would improve confidence -- e.g., "no environmental report", "market rent assumptions unverified", "cap rate comps limited"]
```

**Three-pass calibration**: Generate underwriting from conservative, neutral, and optimistic perspectives. High consistency across passes = high confidence. Divergence on return metrics = flag specific assumptions for IC discussion.

Typical confidence ranges:
- **0.85+**: Complete T12 + rent roll + environmental + market comps + site visit notes
- **0.65-0.84**: T12 and rent roll available, market assumptions from broker OM (unverified)
- **0.40-0.64**: OM-only data, no independent market validation, assumptions largely from broker
- **Below 0.40**: Partial or missing financials -- flag as preliminary estimate only, not suitable for IC presentation
