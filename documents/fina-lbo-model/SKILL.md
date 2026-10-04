---
name: fina-lbo-model
version: 1.0.0
description: Model a leveraged buyout end to end — sources and uses, tranche-level debt with amortization and cash sweep, levered free cash flow, and sponsor returns (IRR and MOIC) with returns attribution and credit-stat tracking.
author: matrixx0070
tags: [finance, lbo, private-equity, irr, moic, leverage, debt-schedule, cash-sweep, returns-attribution, excel]
capabilities: []
---

# Leveraged Buyout Model

## When to use
Use this when a financial sponsor is acquiring a business with debt and you need to size the capital structure, project debt paydown, and compute equity returns (IRR and MOIC) at exit, plus the attribution of those returns and the credit statistics lenders will test. It answers "what return does the sponsor earn and can the company carry the debt."

**Not for:** an intrinsic, capital-structure-neutral valuation — use `fina-dcf-model`; the underlying integrated operating forecast — use `fina-3-statement-model`; market multiple benchmarking for entry/exit assumptions — use `fina-comps-analysis`; checking an existing model's mechanics — use `fina-audit-xls`; or formatting the deliverable — use `fina-xlsx-author`.

## Method
1. **Set entry valuation and build sources and uses.** You set the entry EV as entry EV/EBITDA × LTM EBITDA, then list uses (purchase equity, refinanced debt, transaction fees, financing fees) and sources (each debt tranche plus the sponsor equity plug). Sources must equal uses; sponsor equity is the balancing item.
2. **Size the debt tranches against leverage capacity.** You layer a revolver, term loan(s), and possibly mezzanine/subordinated notes, each sized to a leverage multiple lenders will accept. Decision point: if total debt/EBITDA exceeds the market-clearing leverage ceiling for the sector, you cut a tranche or raise more sponsor equity rather than assume debt that will not fund.
3. **Project levered free cash flow.** You take the operating model's EBITDA, subtract cash interest, cash taxes, capex, and the change in net working capital, to get cash available for debt repayment.
4. **Build the debt schedule with mandatory amortization and a cash sweep.** You roll each tranche: opening balance less mandatory amortization, then apply excess cash via a sweep against tranches in priority order (revolver first, then term loans by seniority), with the revolver drawing to cover any minimum-cash shortfall. Interest is computed on average balances, creating a circularity you resolve with iterative calc and a circuit-breaker switch.
5. **Track credit statistics each period.** You compute total and senior leverage (debt/EBITDA), interest coverage (EBITDA/interest), and fixed-charge coverage, checking them against covenant thresholds every year. Decision point: if projected leverage or coverage breaches a covenant in any forecast year, you reduce entry leverage or revise operating assumptions before finalizing, because a modeled breach means the deal as structured defaults.
6. **Set exit assumptions and compute exit equity value.** You apply an exit EV/EBITDA multiple to exit-year EBITDA for exit EV, subtract remaining net debt, to get exit equity value to the sponsor.
7. **Compute returns.** You calculate MOIC as exit equity / initial sponsor equity, and IRR as the annualized return over the hold period, accounting for any interim dividends or dividend recaps.
8. **Attribute the returns.** You decompose the equity value creation into EBITDA growth, multiple expansion (or contraction), and debt paydown (deleveraging), so the sponsor sees what actually drove the return rather than just the headline IRR.

## Example
A sponsor buys a company with 100 LTM EBITDA at an 8.0x entry multiple, so entry EV is 800. Uses: 800 purchase plus 20 fees = 820. Sources: term loan 400 (4.0x) + mezz 100 (1.0x) = 500 debt, so sponsor equity is 320. Over a 5-year hold, EBITDA grows to 150 and the company sweeps cash to pay down 250 of debt, leaving 250 net debt at exit. Exit at the same 8.0x on 150 EBITDA is EV of 1,200; less 250 net debt gives exit equity of 950. MOIC = 950 / 320 = 3.0x; IRR = 3.0^(1/5) − 1 ≈ 24.5%. Attribution: EBITDA growth of 50 at 8.0x = 400 of value; multiple expansion is 0 (flat 8.0x); deleveraging contributed the 250 debt paydown. The credit stats: entry leverage 5.0x total falls to ~1.7x by exit, coverage rises well above covenant.

## Pitfalls
- **Sources not equal to uses.** If the two sides do not foot, the sponsor equity plug is wrong and every return metric is corrupt. Force sources = uses with equity as the single balancing line.
- **Circular interest with no breaker.** Average-balance interest creates a loop (interest → FCF → sweep → balance → interest); without iterative calc and a circuit-breaker switch, the file fills with errors. Ship the switch to charge interest on opening balances when isolating a break.
- **Sweep exceeding the balance or ignoring priority.** A sweep that pays more than a tranche's balance drives it negative, and one that ignores seniority mis-orders paydown. Cap each sweep at the tranche balance and repay in priority order.
- **Ignoring covenant breaches.** A model that shows a covenant breach but reports a clean IRR is fiction — a breach means default. Flag any leverage/coverage covenant violation before quoting returns.
- **Fees left out of uses.** Omitting transaction and financing fees understates the equity check and overstates returns. Capture both in uses.
- **Double-counting cash at exit.** Netting cash against debt at exit while also having swept it away double-counts. Reconcile the exit balance sheet to the debt schedule.

## Output format
```
LBO MODEL SUMMARY                               ($ in 000s)

SOURCES & USES
  Uses                          Sources
  Purchase EV     800           Revolver         0
  Fees             20           Term loan      400   (4.0x)
                                Mezzanine      100   (1.0x)
                                Sponsor equity 320
  Total uses      820           Total sources  820

RETURNS
  Entry equity              320
  Exit equity (Yr5)         950
  MOIC                      3.0x
  IRR                      24.5%

CREDIT STATS            Entry   Yr3    Exit
  Total debt / EBITDA     5.0x   3.0x   1.7x
  EBITDA / interest       3.3x   5.5x   9.0x

RETURNS ATTRIBUTION (of equity value creation)
  EBITDA growth            +400
  Multiple expansion         +0
  Debt paydown (delever)   +230
  Total value created      +630
```

## Reference

### Sources and uses table
| Uses | Sources |
|---|---|
| Purchase enterprise value | Revolver draw at close |
| Refinance existing debt | Term loan A / B |
| Transaction fees (advisory, legal) | Second lien / mezzanine |
| Financing fees (OID, arrangement) | High-yield / sub notes |
| Minimum cash to balance sheet | Sponsor equity (plug) |
| Total uses | Total sources (must equal uses) |

### Returns formulas
| Metric | Formula |
|---|---|
| Entry equity | Total uses − total debt raised |
| Exit EV | Exit EV/EBITDA × exit-year EBITDA |
| Exit equity | Exit EV − net debt at exit (+ interim dividends) |
| MOIC | Total cash to sponsor / initial sponsor equity |
| IRR (no interim flows) | (MOIC)^(1 / hold years) − 1 |
| IRR (with interim flows) | rate solving Σ CFt / (1 + IRR)^t = 0 |

### Credit ratio table
| Ratio | Formula | Lender focus |
|---|---|---|
| Total leverage | Total debt / EBITDA | maximum leverage covenant |
| Senior leverage | Senior debt / EBITDA | first-lien capacity |
| Net leverage | (Debt − cash) / EBITDA | headline deleveraging |
| Interest coverage | EBITDA / cash interest | ability to service |
| Fixed-charge coverage | (EBITDA − capex) / (interest + mandatory amort) | maintenance covenant |

### Cash sweep mechanics
| Step | Formula |
|---|---|
| Cash available for debt | EBITDA − cash interest − cash taxes − capex − ΔNWC |
| After mandatory amort | Cash available − scheduled amortization |
| Sweep to tranche (priority) | MIN(remaining cash × sweep %, tranche opening balance) |
| Revolver draw | MAX(0, minimum cash − cash before revolver) |
| Ending tranche balance | Opening − mandatory amort − sweep + draw |
| Interest | Rate × AVERAGE(opening, closing) → circular; use iterative calc + `CIRC_SWITCH` |

### Returns attribution
| Driver | Formula |
|---|---|
| EBITDA growth | (Exit EBITDA − entry EBITDA) × entry multiple |
| Multiple expansion | (Exit multiple − entry multiple) × exit EBITDA |
| Debt paydown (delever) | Entry net debt − exit net debt |
| Sum | equals total equity value created (exit equity − entry equity) |

### Sanity checks
| Check | Passes when |
|---|---|
| Sources = uses | difference = 0 |
| Debt continuity | opening − amort − sweep + draw − ending = 0 per tranche |
| Sweep bounded | 0 ≤ sweep ≤ tranche opening balance |
| No covenant breach | every period's leverage/coverage within thresholds |
| Attribution ties | growth + multiple + delever = exit equity − entry equity |
| IRR/MOIC consistency | IRR sign matches MOIC (MOIC > 1 ⇒ IRR > 0) |

Pull entry/exit multiples from `fina-comps-analysis`, draw the operating forecast from `fina-3-statement-model`, and format the final book with `fina-xlsx-author`.
