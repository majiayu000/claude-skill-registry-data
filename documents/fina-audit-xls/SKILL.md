---
name: fina-audit-xls
version: 1.0.0
description: Audit an existing financial model workbook for correctness (formula tracing, hardcode and error detection, sign and consistency checks, tie-outs, and sensitivity stress) before you rely on its outputs.
author: matrixx0070
tags: [finance, model-audit, excel, xlsx, formula-tracing, hardcodes, tie-outs, sensitivity, quality-control]
capabilities: []
---

# Audit an Existing Model Workbook (.xlsx)

## When to use
Use this to review a spreadsheet financial model you did not build, or one you are about to base a decision on, and confirm its formulas, structure, and outputs are correct before you trust them.

**Not for:** authoring a new workbook from scratch (fina-xlsx-author), cleaning or normalizing a raw data extract before it enters a model (fina-clean-data-xls), building the projection logic (fina-3-statement-model), or judging whether the valuation method is right (fina-dcf-model, fina-comps-analysis).

## Method
1. **Map the workbook.** List tabs, identify inputs (assumptions), calculations, and outputs, and confirm the intended flow (assumptions -> calc engine -> statements -> outputs). Note where circularity is expected (interest on average debt, cash sweep).
2. **Sweep for errors first.** Scan every sheet for error values (#REF!, #DIV/0!, #VALUE!, #NAME?, #N/A, #NUM!, #NULL!). Decision point: if any #REF! exists, stop the audit and resolve it first - a broken reference means the dependency chain is already wrong and downstream checks are meaningless.
3. **Trace the formulas.** Follow precedents and dependents on key output cells back to the input drivers. Confirm each output is actually a live formula chain to the assumptions, not a disconnected or overwritten cell.
4. **Hunt hardcodes inside formulas.** Find numeric constants embedded in formula cells (e.g. a tax rate typed as 0.21 inside a formula rather than referenced from an input cell). These are the most common silent errors because they do not flow when assumptions change.
5. **Check consistency across rows and columns.** A formula should copy uniformly across a projection row; find the cell that breaks the pattern. Decision point: if one cell in a copied row differs, decide whether it is an intentional override (should be flagged/colored) or an accidental break (must be fixed) - never assume it is intentional.
6. **Verify sign conventions.** Confirm costs, capex, and cash outflows carry the model's chosen sign consistently, and that subtotals sum signed inputs correctly (a cost entered positive but subtracted, then also entered negative, double-counts).
7. **Confirm tie-outs and checks rows exist and pass.** Balance sheet balances (A = L + E), cash-flow ending cash equals balance-sheet cash, sources = uses, roll-forwards reconcile. If the model has no checks row, add the audit's own.
8. **Verify circularity handling.** Where circular references are intended, confirm iterative calculation is enabled and a circuit breaker (a switch that zeroes the circular term) exists to recover from #REF!/divergence.
9. **Stress-test with edge inputs.** Push key drivers to extremes (0% growth, 0 revenue, high rate, negative case) and watch whether checks still tie and outputs stay sane. A model that only balances at the base case is fragile.
10. **Report findings by severity.** Blockers (wrong outputs, broken ties) first, then structural risks (hardcodes, inconsistent rows), then hygiene, each with cell address and fix.

## Example
Model with a 5-year projection. Error sweep: one #DIV/0! in the DSO row at year 1 (revenue cell blank). Tracing revenue -> found a hardcode: EBIT margin cell =Revenue*0.20 instead of referencing the 20% assumption cell, so the margin scenario toggle does nothing. Consistency check: year 3 capex =C10*0.05 while years 1,2,4,5 reference the capex-% input row - year 3 is an accidental break. Sign check: capex entered positive and subtracted in CFS (correct), but also subtracted again in the PP&E roll-forward as a positive add - PP&E overstated. Tie-out: balance sheet off by $4.2M in year 2, traced to the double-counted capex. Stress: set growth to 0% -> ending cash goes negative and the interest circularity throws #REF! because no circuit breaker exists. Findings: 1 blocker (BS imbalance from sign error), 2 structural (hardcode margin, inconsistent capex row), 1 resilience gap (no circuit breaker).

## Pitfalls
- **Trusting a green checks row.** A checks row can itself be hardcoded to "OK" or reference the wrong cells; verify the check formula, not just its result.
- **Skipping the error sweep.** Auditing logic while a live #REF! sits upstream wastes the pass - the chain is already broken.
- **Missing embedded constants.** A hardcoded 0.21 tax rate inside a formula passes every visual scan but silently ignores the input toggle.
- **Assuming a broken row is intentional.** Treating an accidental one-cell override as a deliberate exception ships the error forward.
- **Base-case-only testing.** A model that balances at base but breaks at 0% growth or peak rate is not validated; stress the extremes.
- **Ignoring circularity switches.** Iterative calc left off, or no circuit breaker, means one bad input corrupts the whole workbook with #REF! and you cannot recover it.

## Output format
```
Model: <file> | Tabs: <n> | Audited: <date>
Structure: inputs [<tabs>] -> calc [<tabs>] -> outputs [<tabs>] | intended circularity: <where>

Error sweep: | Error | Cell | Sheet | Cause |
Tie-outs:    | Check | Formula/cells | Result | Pass/Fail |
  A = L + E | ... | ... | pass/fail
  CF ending cash = BS cash | ... | pass/fail
  Sources = Uses | ... | pass/fail

Findings:
| # | Severity | Cell | Issue | Fix |
| 1 | BLOCKER  | ..   | ..    | ..  |
| 2 | HIGH     | ..   | ..    | ..  |
| 3 | MED      | ..   | ..    | ..  |

Stress tests: | Input pushed to | Checks tie? | Output sane? |
Verdict: <safe to rely / fix blockers first / do not use>
```

## Reference

### Error types
| Error | Means | Common cause |
|---|---|---|
| #REF! | Reference no longer exists | Deleted row/column/sheet a formula pointed to |
| #DIV/0! | Division by zero or blank | Denominator cell empty or zero (rates, ratios) |
| #VALUE! | Wrong argument type | Text where a number is expected in arithmetic |
| #NAME? | Unrecognized name | Typo'd function or undefined named range |
| #N/A | Value not available | Failed lookup (VLOOKUP/MATCH/XLOOKUP no match) |
| #NUM! | Invalid numeric operation | IRR/rate with no solution; overflow |
| #NULL! | Empty intersection | Space instead of comma between ranges |
| Circular ref warning | Formula depends on itself | Intended (interest on avg debt) or accidental |

### Audit checklist
| Area | Check |
|---|---|
| Structure | Inputs, calcs, outputs separated; flow one-directional |
| Errors | Zero #REF!/#DIV0!/#VALUE! across all sheets |
| Live chains | Every output traces to an input via formulas |
| Hardcodes | No numeric constants buried in formula cells |
| Consistency | Copied rows uniform; overrides flagged |
| Signs | Costs/capex/outflows signed consistently |
| Tie-outs | BS balances; CF cash = BS cash; roll-forwards reconcile |
| Checks row | Exists, references correct cells, and passes |
| Circularity | Iterative calc on; circuit breaker present |
| Resilience | Ties hold under stress inputs |

### Formula-consistency tests
- A projection row should be one formula copied across columns; the anomaly is the cell whose formula text differs from its neighbors.
- Growth/ratio rows should reference a single input row, not re-type the rate per column.
- Subtotals should sum an unbroken contiguous range; a SUM that skips or overlaps rows is a structural defect.
- Cross-tab references should point at the labeled output cell of the source tab, not an arbitrary offset.

### Hardcode detection
- A calculation cell should contain references and operators, not literals; a bare number inside a formula (0.21, 12, 1000) is a hardcode unless it is a true mathematical constant.
- The exception is the inputs/assumptions area, where literals belong - hardcodes are only defects when they sit in the calc/output layer.
- Colour or flag inputs distinctly (convention: blue font = input, black = formula) so a stray black-font literal in a formula sheet stands out.

### Sign-convention rules
| Item | Convention (state and enforce one) |
|---|---|
| Revenue, cash inflows | Positive |
| Costs, capex, outflows | Either all-positive-then-subtracted, or all-negative-then-added - never mixed |
| Depreciation | Expense on P&L, add-back on CFS, contra on BS - same magnitude, consistent sign in each |
| Debt repayment | Financing outflow; principal reduces debt balance |
| Rule | A signed item must not be both negated in the formula and entered negative (double negation) |

### Tie-out and checks conventions
| Tie-out | Rule |
|---|---|
| Balance sheet | Assets = Liabilities + Equity, every period; build a check = A - (L+E), must be 0 |
| Cash articulation | CF ending cash = BS cash line |
| Sources = Uses | In any funding/transaction schedule |
| Roll-forwards | PP&E, debt, equity: begin + adds - reductions = end |
| Checks row | One row that flags TRUE/0 only when every tie holds; verify the check formula itself |

### Sensitivity stress tests
| Input pushed | What to watch |
|---|---|
| Revenue growth 0% / negative | Cash goes negative gracefully; checks still tie |
| Interest rate high | Interest circularity converges, no #REF! |
| Margin to 0 | No #DIV/0! in downstream ratios |
| Terminal growth >= WACC | Model should trap it (DCF gives absurd/negative value) - confirm a guard |
| Blank a key driver | Errors are contained, not cascaded workbook-wide |
| Circuit breaker toggled | Circular terms zero out and the model recovers from a bad state |
