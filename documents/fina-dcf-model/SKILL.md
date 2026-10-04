---
name: fina-dcf-model
version: 1.0.0
description: Value a business by discounting unlevered free cash flow at WACC with mid-year convention, a dual-method terminal value, and a full enterprise-to-equity-to-per-share bridge plus WACC-versus-growth sensitivity.
author: matrixx0070
tags: [finance, dcf, valuation, wacc, terminal-value, unlevered-fcf, capm, sensitivity, excel]
capabilities: []
---

# Discounted Cash Flow Model

## When to use
Use this when you need an intrinsic valuation of a business by projecting unlevered free cash flow, discounting it at the weighted average cost of capital, and bridging enterprise value to equity value and a per-share price. It consumes the operating forecast and produces a value range plus sensitivities.

**Not for:** building the underlying integrated forecast and schedules — use `fina-3-statement-model`; a leveraged buyout with tranche-level debt and IRR/MOIC returns — use `fina-lbo-model`; market-based valuation off trading or deal multiples — use `fina-comps-analysis`; verifying an existing model's links and formulas — use `fina-audit-xls`; or formatting the output workbook — use `fina-xlsx-author`.

## Method
1. **Pull unlevered free cash flow from the operating model.** You start from EBIT, tax it at the marginal rate, add back D&A, subtract capex, and subtract the change in net working capital — deliberately excluding interest so the cash flow is capital-structure-neutral. UFCF = EBIT × (1 − tax) + D&A − Capex − ΔNWC.
2. **Set the explicit forecast horizon.** You forecast UFCF for 5 to 10 years, long enough that the business reaches a steady state (stable margins, capex ≈ D&A, normalized reinvestment) before terminal value begins.
3. **Build WACC from its components.** You compute cost of equity via CAPM (risk-free + beta × equity risk premium), the after-tax cost of debt (pretax rate × (1 − tax)), and weight them by target market-value capital weights. Decision point: use a target/optimal capital structure rather than the current one if the current mix is temporary or clearly off-peer, because WACC should reflect the long-run financing of the assets, not a transient snapshot.
4. **Discount with the mid-year convention.** You apply discount factors assuming cash flows arrive mid-period (period 0.5, 1.5, 2.5, …) rather than at year-end, since cash is generated throughout the year. Factor = 1 / (1 + WACC)^(t − 0.5).
5. **Compute terminal value two ways and reconcile them.** You calculate a Gordon growth (perpetuity) TV and an exit-multiple TV, then cross-check. Decision point: if the exit-multiple TV implies a perpetuity growth rate above long-run GDP (roughly 2–3%), your exit multiple is too aggressive; if the perpetuity-growth TV implies an exit EV/EBITDA far off trading comps, your growth or WACC is off — reconcile before trusting the number.
6. **Discount the terminal value to present.** You apply the terminal-year discount factor (using the same mid-year or year-end convention consistently) to the undiscounted TV.
7. **Sum to enterprise value.** You add the PV of explicit UFCF and the PV of terminal value to get enterprise value.
8. **Bridge enterprise value to equity value and per share.** You subtract net debt (total debt − cash), subtract preferred and minority interest, add non-operating assets, to reach equity value; divide by diluted shares (treasury-stock method) for per-share value.
9. **Build the sensitivity table.** You lay out a two-way data table of per-share value across WACC (rows) and perpetuity growth or exit multiple (columns), so the reader sees the value range rather than a false-precision point estimate.

## Example
A company's steady-state UFCF grows to 120 in the terminal year. WACC is built as: risk-free 4.0%, beta 1.2, ERP 5.5% → cost of equity 10.6%; pretax cost of debt 6.0% × (1 − 25%) = 4.5% after-tax; weights 80% equity / 20% debt → WACC ≈ 9.4%. With perpetuity growth of 2.5%, Gordon TV = 120 × (1.025) / (0.094 − 0.025) = 123 / 0.069 ≈ 1,783. Discounting at the year-5 mid-year factor 1 / 1.094^4.5 ≈ 0.665 gives a PV of TV ≈ 1,186. Adding PV of explicit UFCF of ~360 gives EV ≈ 1,546. Less net debt of 300 gives equity value 1,246; over 100 diluted shares that is 12.46 per share. The exit-multiple cross-check: 1,783 / terminal EBITDA of ~200 implies an 8.9x exit — in line with comps, so the two methods reconcile.

## Pitfalls
- **Mismatched cash flow and discount rate.** Discounting unlevered FCF at cost of equity (instead of WACC) double-charges for leverage. Unlevered FCF pairs with WACC; levered FCF pairs with cost of equity — never cross them.
- **Terminal value tail wagging the dog.** When TV is 80%+ of EV (common), a 25-basis-point WACC or growth tweak swings the value massively. Always show the TV-as-percent-of-EV and the sensitivity grid.
- **Perpetuity growth above GDP.** A terminal growth rate that exceeds long-run nominal GDP implies the company eventually becomes the whole economy. Cap g at 2–3% and cross-check the implied exit multiple.
- **Inconsistent mid-year convention.** Applying mid-year to explicit flows but year-end to the terminal value (or vice versa) mis-times the largest cash flow. Pick one convention and apply it to both.
- **Nominal-versus-real mismatch.** Discounting nominal cash flows at a real rate (or the reverse) systematically distorts value. Keep cash flows and WACC both nominal.
- **Stale net debt and share count.** Using book debt instead of market net debt, or basic instead of diluted shares, corrupts the equity bridge. Use latest net debt and the treasury-stock diluted count.

## Output format
```
UNLEVERED DCF                                   ($ in 000s)
                        Yr1    Yr2    Yr3    Yr4    Yr5
UFCF                     80     92    103    112    120
Mid-year factor (WACC 9.4%)
                      0.955  0.873  0.798  0.729  0.667
PV of UFCF               76     80     82     82     80   -> Sum 400

TERMINAL VALUE
  Perpetuity (g=2.5%)  1,783   |  Exit multiple (8.5x)  1,700
  PV of TV             1,186
  Implied exit multiple (perp method)     8.9x
  Implied perp growth (exit method)       2.3%   [cross-check OK]

VALUE BRIDGE
  Enterprise value            1,586
  (-) Net debt                 (300)
  (-) Preferred / minority       (0)
  Equity value                1,286
  / Diluted shares              100
  Value per share             12.86

SENSITIVITY: per share (WACC x g)
            2.0%    2.5%    3.0%
   8.9%    12.10   12.86   13.75
   9.4%    11.30   12.00   12.80
   9.9%    10.60   11.24   11.96
```

## Reference

### WACC formula table
| Component | Formula |
|---|---|
| Cost of equity (Ke) | Rf + β × ERP (CAPM) |
| Levered beta | βu × [1 + (1 − tax) × D/E] (relever peer unlevered beta to target structure) |
| Pretax cost of debt (Kd) | Yield to maturity on comparable debt, or risk-free + credit spread |
| After-tax cost of debt | Kd × (1 − tax) |
| Equity weight (We) | E / (D + E) at market values |
| Debt weight (Wd) | D / (D + E) at market values |
| WACC | We × Ke + Wd × Kd × (1 − tax) |

### Terminal value formulas
| Method | Formula | Notes |
|---|---|---|
| Gordon growth (perpetuity) | TV = UFCF_final × (1 + g) / (WACC − g) | g must be < WACC and ≤ long-run GDP |
| Exit multiple | TV = terminal EBITDA × exit EV/EBITDA | multiple from `fina-comps-analysis` |
| Implied exit multiple | Gordon TV / terminal EBITDA | sanity vs comps |
| Implied perpetuity growth | g = WACC − (UFCF_final × (1+g)) / exit-multiple TV (solve) | sanity vs GDP |

### Enterprise value to equity bridge
| Line | Sign |
|---|---|
| PV of explicit UFCF | + |
| PV of terminal value | + |
| = Enterprise value | = |
| Total debt | − |
| Cash and equivalents | + |
| Preferred stock | − |
| Minority (non-controlling) interest | − |
| Non-operating / investment assets | + |
| = Equity value | = |
| ÷ Diluted shares (treasury method) | ÷ |
| = Value per share | = |

### Mid-year convention factor
| Period t | Year-end factor | Mid-year factor |
|---|---|---|
| 1 | 1/(1+WACC)^1 | 1/(1+WACC)^0.5 |
| 2 | 1/(1+WACC)^2 | 1/(1+WACC)^1.5 |
| t | 1/(1+WACC)^t | 1/(1+WACC)^(t−0.5) |
| Terminal | discounted at year-t factor consistent with explicit flows |

### Sanity checks
| Check | Passes when |
|---|---|
| Cash flow / rate consistency | Unlevered FCF discounted at WACC (not Ke) |
| TV method reconciliation | Implied exit multiple ≈ comps AND implied g ≤ GDP |
| TV concentration | TV % of EV disclosed; sensitivity shown if > ~75% |
| Nominal consistency | Both cash flows and WACC nominal (or both real) |
| Steady state reached | Terminal year: capex ≈ D&A, margins stable, ΔNWC normalized |
| Net debt currency | Market net debt and diluted shares as of valuation date |

Feed the exit multiple from `fina-comps-analysis`, take UFCF drivers from `fina-3-statement-model`, and finalize the workbook with `fina-xlsx-author`.
