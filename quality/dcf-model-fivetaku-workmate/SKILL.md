---
name: dcf-model
description: Real DCF (Discounted Cash Flow) model creation for equity valuation. Retrieves financial data from SEC filings and analyst reports, builds comprehensive cash flow projections with proper WACC calculations, performs sensitivity analysis, and outputs professional Excel models with executive summaries. Use when users need to value a company using DCF methodology, request intrinsic value analysis, or ask for detailed financial modeling with growth projections and terminal value calculations.
---

# DCF Model Builder

## Overview
Institutional-quality DCF models for equity valuation.
Each analysis produces a detailed Excel model with sensitivity analysis at the bottom of the DCF sheet.

## Preflight: Dependency Check

Before starting, verify required libraries and tools are installed and install any that are missing.

```bash
python3 -c "import openpyxl" 2>/dev/null || python3 -m pip install openpyxl
python3 -c "import xlwings" 2>/dev/null && echo "xlwings: OK" || (
  ls "/Applications/Microsoft Excel.app" 2>/dev/null && echo "macOS Excel: OK" ||
  ls "/mnt/c/Program Files/Microsoft Office/root/Office16/EXCEL.EXE" 2>/dev/null && echo "Windows Excel (WSL): OK" ||
  echo "WARNING: MS Office not detected. Install MS Excel or run: pip install xlwings. Required for scripts/recalc.py."
)
```

**Important**: Do not skip this step — `scripts/recalc.py` and `scripts/validate_dcf.py` need these tools to verify sensitivity tables and TV-as-%-of-EV sanity checks.

## Scripts

- `scripts/recalc.py` — Force formula recalculation via MS Office (xlwings/Windows COM/macOS AppleScript). Run after building: `python scripts/recalc.py <model.xlsx>`
- `scripts/validate_dcf.py` — DCF-specific validation (terminal growth < WACC, WACC in 5-20% range, TV as 40-80% of EV, formula errors). Run after recalc: `python scripts/validate_dcf.py <model.xlsx>`

## Tools
- Default to using all information provided by the user and MCP servers available for data sourcing.

## Critical Constraints - Read These First

### Environment: Office JS vs Python/openpyxl
- Office JS: Use range.formulas = [["=D19*(1+$B$8)"]] — never range.values for derived cells
- Python/openpyxl: Write ws["D15"] = "=D14*(1+Assumptions!$B$5)", then run recalc.py
- Office JS merged cell pitfall: Write value to top-left cell alone, then merge + format

### Formulas Over Hardcodes (NON-NEGOTIABLE)
- Every projection/margin/discount factor/PV/sensitivity cell MUST be live Excel formula
- Only permitted hardcodes: (1) raw historical inputs, (2) assumption drivers, (3) current market data
- "If you catch yourself computing something in Python and writing the result — STOP"

### Verify Step-by-Step With the User (DO NOT build end-to-end)
1. After data retrieval → confirm raw inputs
2. After revenue projections → confirm top line + growth rates
3. After FCF build → confirm FCF schedule logic
4. After WACC → confirm calculation + inputs
5. After terminal value + PV → confirm equity bridge
6. After sensitivity tables → final review

### Sensitivity Tables
- Use ODD number of rows/columns (5×5 or 7×7)
- Center cell = base case (must equal model's actual implied share price)
- Highlight center cell with #BDD7EE + bold
- Populate ALL cells with full DCF recalculation formulas (75 total for 3 tables)
- NO placeholder text, NO linear approximations

### Cell Comments
- Add AS each hardcoded value is created
- Format: "Source: [System/Document], [Date], [Reference], [URL]"
- Never defer to end or write "TODO: add source"

### Model Layout Planning
- Define ALL section row positions BEFORE writing formulas
- Write ALL headers → section dividers → THEN formulas

## DCF Process Workflow

### Step 1: Data Retrieval and Validation
- Priority: MCP Servers → User-Provided Data → Web Search/Fetch
- Validation: net debt vs net cash, diluted shares, historical margins, growth rates, tax rate

### Step 2: Historical Analysis (3-5 years)
- Revenue growth trends (CAGR), margin progression, capital intensity, WC efficiency, return metrics

### Step 3: Build Revenue Projections
- Revenue(Year N) = Revenue(Year N-1) × (1 + Growth Rate)
- Three-scenario approach: Bear/Base/Bull
- Growth rates: Year 1-2 higher → Year 3-4 moderate → Year 5+ approaching terminal

### Step 4: Operating Expense Modeling
- S&M, R&D, G&A — ALL percentages based on REVENUE, not gross profit
- Model operating leverage: % should decline as revenue scales

### Step 5: Free Cash Flow Calculation
- EBIT → (-)Taxes → NOPAT → (+)D&A → (-)CapEx → (-)ΔNWC → Unlevered FCF

### Step 6: Cost of Capital (WACC) Research
- CAPM: Cost of Equity = Risk-Free Rate + Beta × ERP
- After-Tax Cost of Debt = Pre-Tax × (1 - Tax Rate)
- WACC = (Ke × We) + (Kd × Wd)

### Step 7: Discount Rate Application
- Mid-year convention: periods 0.5, 1.5, 2.5...
- Discount Factor = 1 / (1 + WACC)^Period

### Step 8: Terminal Value Calculation
- Perpetuity Growth: TV = Terminal FCF / (WACC - g)
- Exit Multiple: TV = Final Year EBITDA × Exit Multiple
- Sanity check: TV should be 50-70% of EV

### Step 9: Enterprise to Equity Value Bridge
- Sum PV FCFs + PV Terminal Value = EV
- EV - Net Debt = Equity Value
- Equity Value / Diluted Shares = Implied Price per Share

### Step 10: Sensitivity Analysis
Three tables: (1) WACC vs Terminal Growth, (2) Revenue Growth vs EBIT Margin, (3) Beta vs Risk-Free Rate

## <correct_patterns> section
- Scenario Block Selection: INDEX/consolidation column approach (not scattered IF statements)
- Revenue Projection: Reference consolidation column
- FCF Formula: Use consolidation columns with INDEX
- Cell Comment Format: exact source with date/URL
- Assumption Table Structure: 3 elements per block (header + column headers + data rows)
- Row Planning Process: headers first → dividers → formulas
- Sensitivity Table: 5×5 grid, symmetric axes, center = base case, formula in every cell

## <common_mistakes> section
- WRONG: Linear approximations in sensitivity tables
- WRONG: Placeholder text instead of formulas
- WRONG: Missing cell comments
- WRONG: Formula row references off (write formulas before headers)
- WRONG: Single row per assumption across scenarios
- WRONG: No borders
- WRONG: Wrong font colors
- WRONG: OpEx based on Gross Profit instead of Revenue
- TOP 5 ERRORS: row references, comments, sensitivity, scenario references, borders

## Excel Model Structure
### Sheet Architecture: 2 sheets — DCF + WACC
### Formatting Standards
- Font Colors: Blue=#0000FF (inputs), Black (formulas), Green=#008000 (cross-sheet)
- Fill Colors: Dark blue #1F4E79 (headers), Light blue #D9E1F2 (sub-headers), Light grey #F2F2F2 (inputs), White (formulas), Medium blue #BDD7EE (outputs)
- Borders: Thick 1.5pt (major sections), Medium 1pt (sub-sections), Thin 0.5pt (data tables)
- Number Formats: Years as text, % as 0.0%, Currency $#,##0, Negatives in parentheses

### DCF Sheet Detailed Structure (Sections 1-5 + Sensitivity)
[Detailed row-by-row layout with formula patterns]

(-) Δ NWC,(XX),(XX),(XX),(XX),[=(E29-D29)*$E$23],[=(F29-E29)*$E$23],[=(G29-F29)*$E$23]
    % of ΔRev,XX%,XX%,XX%,XX%,[=$E$23],[=$E$23],[=$E$23]
,,,,,,
Unlevered FCF,XXX,XXX,XXX,XXX,[=E57+E58-E60-E62],[=F57+F58-F60-F62],[=G57+G58-G60-G62]
    FCF Margin,XX%,XX%,XX%,XX%,[=E64/E29],[=F64/F29],[=G64/G29]
Key Formula Pattern (FCF):

NOPAT = EBIT - Taxes: =E45
(+) D&A: =E29*$E$21 (consolidation column for D&A %)
(-) CapEx: =E29*$E$22 (consolidation column for CapEx %)
(-) Δ NWC: =(E29-D29)*$E$23 (consolidation column for NWC %)
Unlevered FCF: =E57+E58-E60-E62 (NOPAT + D&A - CapEx - ΔNWC)
Section 6: Discount Factors & Present Value

**Section 6: Discount Rate & Present Value**

Discount Period,,,,,0.5,1.5,2.5,3.5,4.5
Discount Factor,,,,,=[=1/(1+$E$25)^E67],[=1/(1+$E$25)^F67],[=1/(1+$E$25)^G67],[=1/(1+$E$25)^H67],[=1/(1+$E$25)^I67]
PV of FCF,,,,,=[=E64*E68],[=F64*F68],[=G64*G68],[=H64*H68],[=I64*I68]
Formula Structure:

Discount Period: 0.5, 1.5, 2.5, 3.5, 4.5 (mid-year convention)
WACC reference: $E$25 = consolidation column pulling from scenario block via INDEX
Discount Factor: =1/(1+$E$25)^[Period]
PV of FCF: =[Unlevered FCF]*[Discount Factor]
Sum of PV FCFs: =SUM(E69:I69)
Section 7: Terminal Value

**Section 7: Terminal Value Calculation**

Terminal Value Section:
Final Year FCF (Year 5),[=I64]
Terminal Growth Rate,[=$E$24] (consolidation column)
Terminal FCF,[=I64*(1+$E$24)]

Perpetuity Growth Method:
Terminal Value,[=E74/($E$25-$E$24)]
  TV as % of EV,[=E75/E82] (sanity check: should be 50-70%)

Exit Multiple Method:
Final Year EBITDA,[=I41] (Year 5 EBIT + D&A, or direct EBITDA)
Exit Multiple,[from assumptions]
Terminal Value (Exit),[=E78*E79]

PV of Terminal Value:
Discount Factor (final period),[=1/(1+$E$25)^4.5]
PV Terminal Value (Perpetuity),[=E75*E81]
PV Terminal Value (Exit),[=E80*E81]
Terminal Value Sanity Check:

TV as % of EV should be 50-70%
If >75%: over-reliant on terminal assumptions
If <40%: terminal assumptions may be too conservative
Section 8: Valuation Summary

**Section 8: Enterprise to Equity Value Bridge**

VALUATION SUMMARY:
(+) Sum of PV of Projected FCFs,[=SUM(E69:I69)]
(+) PV of Terminal Value (Perpetuity),[=E82]
(=) Enterprise Value (Perpetuity),[=E85+E86]

(+) PV of Terminal Value (Exit Multiple),[=E83]
(=) Enterprise Value (Exit Multiple),[=E85+E89]

(-) Net Debt,[=$B$[net_debt_row]] (from Market Data section, blue input)
(=) Equity Value (Perpetuity),[=E87-E91]
(=) Equity Value (Exit Multiple),[=E90-E91]

(÷) Diluted Shares Outstanding (M),[=$B$[shares_row]] (from Market Data section)
(=) Implied Price per Share (Perpetuity),[=E92/E94]
(=) Implied Price per Share (Exit Multiple),[=E93/E94]

Current Stock Price,[=$B$[price_row]] (blue input)
Implied Upside/(Downside) (Perpetuity),[=E95/E97-1]
Implied Upside/(Downside) (Exit Multiple),[=E96/E97-1]
Output Formatting:

Key output rows (EV, Equity Value, Implied Price): Medium blue fill #BDD7EE, bold
Net Debt/Shares/Current Price: Blue font (hardcoded inputs)
All calculated values: Black font
Sensitivity Tables (Bottom of DCF Sheet)

**Sensitivity Analysis — Three Tables**

TABLE 1: WACC vs Terminal Growth Rate → Implied Share Price (Perpetuity)
- Row headers: WACC values [base-2Δ, base-Δ, base, base+Δ, base+2Δ] (e.g., 8.0%, 8.5%, 9.0%, 9.5%, 10.0%)
- Column headers: Terminal growth [base-2Δ, base-Δ, base, base+Δ, base+2Δ] (e.g., 2.0%, 2.5%, 3.0%, 3.5%, 4.0%)
- Each cell formula recalculates: Sum PV FCFs (using row WACC) + PV TV (using col growth & row WACC) - Net Debt / Shares
- Center cell = base case implied price, highlighted #BDD7EE + bold

TABLE 2: Revenue Growth vs EBIT Margin → Implied Share Price
- Row headers: Revenue growth rates (Year 1)
- Column headers: EBIT margins
- Each cell recalculates full DCF with substituted assumptions

TABLE 3: Beta vs Risk-Free Rate → Implied Share Price
- Row headers: Beta values
- Column headers: Risk-free rate values
- Each cell recalculates WACC → full DCF
Implementation (programmatic loop):

# Pseudocode for all 3 tables × 5×5 = 75 cells
wacc_range = [base_wacc - 0.01, base_wacc - 0.005, base_wacc, base_wacc + 0.005, base_wacc + 0.01]
tg_range = [base_tg - 0.01, base_tg - 0.005, base_tg, base_tg + 0.005, base_tg + 0.01]

for r, wacc in enumerate(wacc_range):
    for c, tg in enumerate(tg_range):
        # Formula references row header ($A$row) for WACC, column header (col$header_row) for TG
        formula = "=(<sum_pv_fcfs_using_$A${row}_as_wacc> + <tv_using_{col}${header}_as_growth_and_$A${row}_as_wacc> - <net_debt>) / <shares>"
        ws.cell(row=start_row+r, column=start_col+c).value = formula
WACC Sheet Structure

## WACC Sheet Layout

**Section 1: Cost of Equity (CAPM)**
Risk-Free Rate (10Y Treasury),[blue input, with source comment]
Equity Risk Premium,[blue input, typically 5.0-6.0%]
Beta (5-year monthly),[blue input, with source comment]
Cost of Equity,[formula: =Risk_Free + Beta × ERP]

**Section 2: Cost of Debt**
Pre-Tax Cost of Debt,[blue input or =Interest Expense / Total Debt]
Tax Rate,[blue input]
After-Tax Cost of Debt,[formula: =Pre_Tax × (1 - Tax_Rate)]

**Section 3: Capital Structure**
Current Share Price,[blue input]
Diluted Shares Outstanding,[blue input]
Market Cap,[formula: =Price × Shares]
Total Debt,[blue input]
Cash & Equivalents,[blue input]
Net Debt,[formula: =Total Debt - Cash]
Enterprise Value,[formula: =Market Cap + Net Debt]

Equity Weight,[formula: =Market Cap / EV]
Debt Weight,[formula: =Net Debt / EV]

**Section 4: WACC Calculation**
WACC,[formula: =(Cost_of_Equity × Equity_Weight) + (After_Tax_Cost_of_Debt × Debt_Weight)]
Formatting:

All inputs: Blue font #0000FF with cell comments
All formulas: Black font
Cross-sheet references from DCF sheet: Green font #008000
Section headers: Dark blue fill #1F4E79, white text
WACC output: Medium blue fill #BDD7EE, bold
Special Cases:

Net Cash Position (Cash > Debt): Net Debt is negative, Debt Weight may be negative, WACC adjusts accordingly
No Debt: WACC = Cost of Equity
Quality Rubric (Full)

## Quality Rubric

Every DCF model must maximize for:
1. **Realistic revenue and margin assumptions** based on historical performance
   - Growth rates justified by industry trends and company-specific drivers
   - Margin progression consistent with scale economics
2. **Appropriate cost of capital calculation** with proper CAPM methodology
   - Risk-free rate = current 10Y Treasury
   - Beta from reliable source (5-year monthly)
   - ERP within standard range (5.0-6.0%)
3. **Comprehensive sensitivity analysis** showing valuation ranges
   - Three 5×5 tables, all 75 cells with live formulas
   - Center cell = base case, highlighted
4. **Clear terminal value calculation** with supporting rationale
   - Both perpetuity and exit multiple methods
   - TV as % of EV sanity check
5. **Professional model structure** enabling scenario analysis
   - Bear/Base/Bull with consolidation columns
   - Clean cell references, no scattered IF statements
6. **Transparent documentation** of all key assumptions
   - Cell comments on every hardcoded input
   - Source citations with dates and URLs
