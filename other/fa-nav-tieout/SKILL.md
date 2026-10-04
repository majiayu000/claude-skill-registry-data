---
name: fa-nav-tieout
version: 1.0.0
description: Tie out a fund NAV package end to end — assets, liabilities, capital, and per-share/per-unit price — proving the accounting equation, the price, and the day-over-day movement before the NAV is released.
author: matrixx0070
tags: [fund-accounting, nav, tie-out, net-asset-value, price-per-share, close, review]
capabilities: []
---

# NAV Tie-Out

## When to use
Use this to review and prove a struck NAV before release — confirming total assets less liabilities equals net assets, net assets divided by units equals the published price, and the movement since the prior NAV is fully explained. This is the final control gate over the whole package, sitting above the individual account reconciliations.

**Not for:** reconciling a single GL account to its source (use fa-gl-recon) or drilling one difference to the transaction (fa-break-trace). This ties the *whole NAV* together and blesses the price.

## Method
1. **Assemble the package.** Trial balance, investment valuation, cash, accruals, capital activity, and the prior-period NAV. Confirm the valuation point and date.
2. **Prove the accounting equation.** Total assets − total liabilities = net assets = partners'/shareholders' capital. Decision point: if net assets ≠ capital, a P&L or capital posting is off — stop and reconcile before pricing.
3. **Confirm each major line ties to its source.** Investments to the valuation/subledger, cash to custodian, accruals to schedules, capital to the investor register. Each should already carry a signed rec; confirm, don't re-do.
4. **Price the NAV.** Net assets ÷ units (or per class, using that class's net assets and units). Recompute independently and match the struck price to the stated precision.
5. **Explain the movement.** Bridge prior NAV per share to current: market P&L + income − expenses ± FX ± capital-activity dilution/accretion ± other. Decision point: an unexplained residual per share is a red flag — do not release until named.
6. **Run reasonableness checks.** Compare the daily/periodic return to a benchmark or the portfolio's known moves; flag any per-share change beyond an expected band.
7. **Sign off.** State NAV, price per share/class, movement explained, exceptions, and reviewer. Preparer ≠ reviewer.

## Example
Single-class fund, 3/31. Total assets $500.2M (investments $492.0M + cash $7.8M + receivables $0.4M); liabilities $2.2M (accrued fees $1.0M + payables $1.2M); net assets $498.0M. Capital per the investor register = $498.0M — equation ties. Units 10,000,000 → NAV/unit $49.80. Prior NAV/unit $49.10. Bridge: market P&L +$0.78, income +$0.04, expenses −$0.11, net capital activity −$0.01 dilution = +$0.70 → $49.80, fully explained. Daily return +1.43% vs benchmark +1.38%, within band. Released.

## Pitfalls
- **Net assets not equal to capital.** The surest sign a P&L, unrealized, or capital entry is misposted; pricing before this ties publishes a wrong NAV.
- **Per-class pricing with fund-level figures.** Multi-class funds must price each class on *its own* net assets and units — shared expenses and class-specific fees split differently; a single blended price is wrong for every class.
- **Unexplained per-share movement.** A residual in the roll bridge means income, expense, pricing, or capital is off; "close enough" on a per-share basis is often a large gross error.
- **Rounding the price the wrong way.** Publish to the fund's stated precision (often 2–4 decimals) with the documented rounding convention; a systematic rounding bias leaks value between investors over time.
- **Capital activity struck at the wrong price.** Subscriptions/redemptions must transact at the NAV of the correct dealing date; mixing dealing dates dilutes or accretes existing holders.

## Output format
```
Fund / class: <...> | Valuation date & point: <date/time>
Accounting equation:
  Total assets <$> − total liabilities <$> = net assets <$>
  Net assets <$>  ==  capital per register <$>   [ties: Y/N]
Line ties: investments <ok> | cash <ok> | accruals <ok> | capital <ok>
Units: <#> | NAV per unit: <$>  (independently recomputed: <$>)  [match: Y/N]
Movement bridge (prior → current NAV/unit):
  prior <$> + mkt P&L <> + income <> − expenses <> ± fx <> ± cap activity <> = current <$>
Reasonableness: period return <%> vs benchmark <%>  [within band: Y/N]
Exceptions: <...>
Sign-off: NAV <$> | price <$> | preparer / reviewer: <who/date>
```

## Reference

### The NAV identity
`NAV (net assets) = total assets − total liabilities`, and `price per share = net assets ÷ shares outstanding`. Independently, `net assets must equal total capital` (contributed capital ± retained earnings/P&L ± distributions). These are two views of the same number; if they disagree the package is not internally consistent and cannot be released.

### What each component contains
- **Assets:** investments at fair value, cash and equivalents, receivables (unsettled sales, income accrued, subscriptions receivable), prepaids.
- **Liabilities:** accrued expenses (mgmt/admin/audit fees), payables (unsettled purchases), redemptions payable, distributions payable, leverage/borrowings.
- **Capital:** contributed capital, accumulated realized and unrealized P&L, income less expenses, distributions. For partnerships, allocated per the LPA and reduced by carry/incentive.

### The NAV movement (attribution) bridge
Explain price per share period over period:
`ΔNAV/share = market P&L + investment income − expenses ± realized/unrealized ± FX ± capital-activity effect ± other`. Every cent should map to a driver. Capital activity affects *total* net assets and units but, when transacted at NAV, should be price-neutral to existing holders — a per-share dilution/accretion term appears only when subs/reds are struck at a stale or wrong price, which is itself a finding.

### Multi-class / series funds
Each share class has its own net assets and units and often its own fee schedule; price each class separately. Series accounting (used by some hedge funds for equalization) issues a new series each subscription period to isolate performance-fee crystallization, then may roll series into a lead series after the fee is booked. Never blend classes/series into one price.

### Valuation point, dealing, and pricing errors
The **valuation point** is the time as of which prices are taken; all positions must use the same point. Subscriptions and redemptions transact at the NAV of their **dealing date** — forward pricing (the next NAV struck after the order cut-off) is standard to prevent late trading. A **NAV error** is typically deemed material above a threshold (commonly ~0.5% of NAV for many funds, tighter for money-market/bond funds); material errors trigger investor compensation and restatement per the fund's error policy.

### Independent review and reasonableness
The tie-out is a preventive control: an independent reviewer recomputes the price, confirms the equation, and challenges the movement before release. Reasonableness checks — return vs benchmark, per-share change vs expected range, expense ratio vs prior period — catch errors the arithmetic alone won't. Segregation is mandatory: whoever struck the NAV cannot be the one who signs it off.
