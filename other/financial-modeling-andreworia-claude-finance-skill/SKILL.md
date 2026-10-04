---
name: financial-modeling
description: Builds an integrated three-statement financial model with drivers, linkages, and checks when you need a working model of a business.
---

# Financial Modeling Agent

## When to use
Use this when you need an integrated model of the business rather than a single isolated schedule. Typical triggers: you are underwriting a company for a deal, refreshing a client model, or you need a base for a DCF or LBO. Reach for it when the income statement, balance sheet, and cash flow must move together off shared drivers.

## What it does
It produces a three-statement financial model: a projected income statement, balance sheet, and cash flow statement, built from explicit operating drivers, fully linked, with the cash and debt circularity resolved and a balance-sheet check that must tie to zero.

## Method
1. Set the model spine. Lock the historical period, the forecast horizon, and the periodicity.
   - Restate historicals into one clean, consistent format before projecting anything, so mappings and formulas carry across every column.
   - Standardize on 3 years of history and a 5-year forecast unless the deal calls for more.

2. Build the income statement from drivers. Work top to bottom off explicit assumptions.
   - Revenue from volume times price or a growth rate; COGS and gross margin; opex as a percent of revenue or split fixed plus variable; D&A from the asset schedule; interest from the debt schedule; taxes at the effective rate; land on net income.
   - Good practice: keep every line a formula off an assumption cell, never a hardcode inside the statement.

3. Build supporting schedules. These feed the statements, not the other way around.
   - Fixed-asset roll-forward: opening PP&E, plus capex, less depreciation, equals closing PP&E.
   - Working-capital schedule off days ratios (receivable days, inventory days, payable days); debt schedule with opening, draws, mandatory and optional repayment, closing.

4. Build the balance sheet. Roll every line from its driver or schedule.
   - Cash from the cash flow statement; working capital from its schedule; PP&E from the asset schedule; debt from the debt schedule; equity as prior equity plus net income less dividends.
   - Pitfall: never plug the balance sheet directly; a plug hides a broken link.

5. Build the cash flow statement. Reconcile net income to the change in cash.
   - Operating: net income plus D&A, less the increase in net working capital. Investing: less capex. Financing: debt draws and repayments, less dividends.
   - The net change in cash must flow into the balance-sheet cash line.

6. Close the circularity. Interest depends on debt, debt depends on the cash sweep, the sweep depends on interest.
   - Resolve with a revolver plug plus iterative calculation, and add a circuit-breaker toggle so a broken circuit can be reset without corrupting the file.

7. Enforce the balance check. Assets minus liabilities minus equity must equal zero every period.
   - Add a visible check row; any nonzero value signals a broken link, not rounding, and must be traced before the model is trusted.

8. Layer scenarios and sanity checks. Make the model decision-ready.
   - Add a base, upside, and downside toggle, and validate margins, growth, and returns against history for reasonableness.

## Inputs
- Historical income statement, balance sheet, and cash flow statement, ideally 3 years
- Revenue drivers (volume and price, or a growth rate by segment)
- Margin and cost assumptions (gross margin, opex behavior, D&A policy)
- Capital-structure detail (existing tranches, rates, maturities) and dividend policy
- Working-capital assumptions (receivable, inventory, and payable days)
- Capex plan and the effective and marginal tax rates
- Any one-off items to normalize out of the base

## Output format
- An assumptions block listing every operating and financing driver by forecast year
- A projected income statement as labeled line items per year
- A projected balance sheet as labeled line items per year
- A projected cash flow statement reconciling net income to the change in cash
- The supporting schedules described in prose: asset roll-forward, debt schedule, working capital
- A checks section stating the balance-sheet tie per year and any circularity notes
- Present all statements as labeled line-item lists per year, never as raw grids

## Example
For Northwind Logistics (fictional, illustrative numbers): revenue grows from 500 to 545 in year 1 at 9 percent, gross margin holds at 32 percent, and EBITDA lands near 78. Capex of 40 and depreciation of 30 flow through the asset schedule, so PP&E rises from 210 to 220. A working-capital build of 8 draws 12 on the revolver, interest ticks to 9, and net income reaches 34. On the cash flow statement, net income of 34 plus D&A of 30 less the 8 working-capital build gives operating cash of 56, less capex of 40 and a dividend of 4 leaves the revolver draw to balance. The balance check reads 0.0 in every year, confirming the links hold.
