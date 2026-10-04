---
name: valuation-triangulator
description: Build a defensible valuation range across DCF, trading comps, precedent transactions, LBO, and premiums paid. Use when pricing a sell-side mandate, framing a buy-side bid, preparing a fairness-style readout, or pressure-testing an IC valuation page. Built around methodology triangulation, the football field, and the bridge from enterprise value to equity value per share.
---

# Valuation Triangulator

## Purpose

Produce a valuation range that survives a senior banker's review and a sophisticated counterparty's diligence — anchored in multiple methodologies, reconciled where they disagree, and translated cleanly from enterprise value down to equity value per share.

The output is not a number. It is a defended range, a football field, and a written view on which methodology should carry the most weight in this specific situation.

## Governing Principle

**Every valuation methodology is wrong on its own. The triangulation is the answer.**

A single methodology produces a number. Triangulation produces a thesis. Senior bankers do not pick a method; they reconcile across methods and explain the gaps.

## The Five Lenses Every Valuation Must Triangulate

Each lens answers a different question. Run all five, then weight by deal context.

1. **DCF** — what is the business worth based on its own cash flows and risk?
2. **Trading comps** — what would the public market pay for this business as a minority stake?
3. **Precedent transactions** — what have control buyers actually paid for similar businesses?
4. **LBO / sponsor view** — what could a financial buyer pay and still hit return thresholds?
5. **Premiums paid / 52-week high** (for public targets) — what does the market reaction-and-history floor look like?

A control sale lands between precedents and LBO. A minority recap lands closer to comps. A take-private clears the LBO floor and the 52-week high. The triangulation point depends on the deal, not on a template.

## Workflow

### Step 1 — Lock the valuation date, the perimeter, and the bridge

Before any number is built, fix the three inputs that every downstream calculation depends on:

- **Valuation date:** the as-of date for share price, net debt, share count, and projections. Do not mix dates.
- **Perimeter:** what is in the deal? Carve-outs, JVs, minority interests, unconsolidated investments — explicitly in or out, with the financial impact named.
- **EV-to-equity bridge:** the line items that convert enterprise value to equity value per share. Build it once, apply it consistently across all five methods.

```
Enterprise Value
  − Total debt (face value, drawn revolver included)
  − Preferred equity (at liquidation value)
  − Minority interest (at fair value, not book)
  − Underfunded pension / OPEB
  − Out-of-the-money management options (treasury method)
  + Cash and marketable securities (less restricted / trapped cash)
  + Tax assets monetizable in deal (NOLs at present value)
  = Equity Value
  ÷ Fully diluted shares (treasury method, in-the-money options + RSUs + converts)
  = Equity Value per Share
```

A wrong bridge silently breaks every methodology. Build it before anything else.

### Step 2 — Build the DCF with explicit forecast, terminal, and WACC discipline

Run a 5–10 year explicit forecast, terminal value via both Gordon growth and exit multiple, discounted at WACC.

For the explicit period, anchor to:
- Revenue build by segment / volume × price
- EBITDA margin trajectory tied to operating leverage and mix
- Capex separated into maintenance and growth
- Working capital change as a % of revenue change (not absolute)
- Cash taxes (not book taxes — apply NOLs, deferred items, cash tax rate)

For the terminal:
- **Gordon growth:** terminal growth no higher than long-run GDP unless explicitly defended
- **Exit multiple:** use the implied exit multiple as a sanity check on Gordon — if they differ by more than ~15%, one of them is wrong
- **Terminal as % of total EV:** if >75%, the explicit period is too short and the DCF is essentially a multiple in disguise

For WACC:
- Cost of equity via CAPM with peer-derived re-levered beta, not historical own-stock beta
- Cost of debt at marginal cost of new issuance, not weighted-average cost of existing debt
- Capital structure at target weights, not current weights
- Sensitize WACC ±100bps and growth ±50bps — the resulting range is the real DCF answer

### Step 3 — Pull trading comps and precedents, then take the right slice

Trading comps and precedents are inputs from separate skills (see `trading-comps-builder` and `precedent-transaction-screener`). Here, the job is to select which multiples to apply and why:

- **Trading multiples:** for minority valuation. Apply on forward metrics (NTM EBITDA, NTM EBIT, NTM revenue if growth-stage). Trailing multiples only as a sanity check.
- **Precedent multiples:** for control valuation. Apply on LTM at announcement, calibrated to current cycle position.
- **Range selection:** 25th–75th percentile is the default working range. Mean is rarely useful. Median anchors the midpoint.

Do not "apply the median." Pick a defensible range and write the sentence that explains *why this target sits where it sits within the range*. Common drivers: growth premium, margin profile, scale, capital intensity, customer concentration, geographic mix.

### Step 4 — Run the LBO floor

A sponsor bid sets the floor on most control transactions, even when no sponsor is in the process. Build the LBO with realistic assumptions:

- **Capital structure:** total leverage at the credit-market reality for this sector (not a stretched memo number). 5.0–6.5x is typical for stable cash flow businesses; cyclicals get less.
- **Sources & uses:** sponsor equity, term loan, high yield / unitranche, mezzanine if needed, rollover equity if relevant
- **Hold period:** 5 years standard
- **Exit multiple:** typically the entry multiple — paying for multiple expansion is a thesis, not an assumption
- **Required return:** 2.5x MOIC and 20%+ IRR as the minimum for a sponsor to engage; 3.0x and 25%+ for a competitive process

Solve for the maximum entry price that delivers the required return. That is the LBO floor. If the LBO clears the trading comps level, the public market is mispricing the business — or the LBO is being run with hero assumptions. Find out which.

### Step 5 — For public targets, layer in premiums paid and the 52-week high

For any public-target situation:

- **Premiums paid:** pull the 1-day, 30-day, and 90-day premium distributions from recent precedents in this sector. The median premium is a market-tested input.
- **52-week high:** any control bid below the 52-week high faces a recency anchor problem with the board and the long-term holder base
- **Unaffected share price:** if there has been deal-related run-up, use the unaffected price (typically 30 days pre-leak) as the base for the premium calculation

The premium framework is not a valuation methodology. It is a reality check on what the board, the proxy advisors, and the institutional holders will accept.

### Step 6 — Build the football field

Plot all five methodologies on a single page, each as a horizontal bar with low / high / midpoint:

```
                      $/share
                      ─────────────────────────────────────────
DCF (WACC ±, g ±)           ████████████████
Trading comps (25–75)              ████████████████
Precedent transactions                  ██████████████████
LBO (returns-constrained)     ██████████
52-wk high                                         │
Premiums paid (30-day)                ██████████████
Current share price                          │
                      ─────────────────────────────────────────
```

For each methodology, label:
- The metric used (EV / NTM EBITDA, EV / LTM EBITDA, etc.)
- The multiple range applied
- The implied equity value per share

The football field is the page a senior banker scans first. It either tells a coherent story or it doesn't.

### Step 7 — Reconcile the methodologies and take a view

The methodologies will disagree. The disagreements are the insight:

- **DCF > comps:** market is discounting something the DCF assumes away (cycle, execution risk, mix shift, capital intensity coming)
- **Precedents > comps:** control premium is real and consistent with cycle; defensible
- **Precedents >> comps:** either the precedent set is stale, the cycle has shifted, or specific synergy / scarcity premiums are doing the work — diagnose which
- **LBO floor > trading comps:** public market is leaving money on the table OR the sponsor case is heroic
- **DCF < LBO:** the DCF is missing the leverage tax shield, the cost-out, or the exit assumption a sponsor would underwrite

Write the reconciliation paragraph. Pick the methodology that should carry the most weight in this specific situation and defend why. A valuation page without a written view is a data dump.

### Step 8 — Translate to the recommendation

End on the number that gets used:

- **Sell-side:** the asking range to anchor the process — typically the 50th–75th percentile of the football field, with the high-end justified by the buyer profile most likely to pay it
- **Buy-side:** the walk-away price (top of what you can defend), the opening bid (bottom of the defensible range), and the negotiation room between
- **Fairness-style readout:** the range within which the consideration falls, with explicit methodology weighting
- **IC memo:** the valuation, the implied multiples on entry and exit, and the sensitivity ranges that matter most

## Hypotheses to Pressure-Test

1. **"The DCF is doing the work, but the assumptions are unsupported."** Strip out the terminal value — does the explicit period stand on its own? If not, the DCF is a multiple in disguise.
2. **"The precedent set is too old to inform the current cycle."** Have credit conditions, sector multiples, or strategic logic shifted materially since these precedents printed?
3. **"The LBO is being run with hero assumptions."** Is the entry-equals-exit multiple defended? Are synergies and cost-outs realistic for a financial sponsor, not a strategic?
4. **"The comp set is right, but the multiple applied to our target is wrong."** Is the target's growth, margin, and risk profile justifying a discount or premium to the peer median? Write the sentence.
5. **"The premium offered looks generous, but the unaffected price is the wrong base."** Has there been leak-driven run-up that is inflating the apparent premium?

## Quality Checks Before Sharing

- [ ] EV-to-equity bridge is built once and applied identically across every methodology
- [ ] Valuation date, share count, and net debt are all as of the same date
- [ ] DCF terminal value is <75% of total EV, or the explicit period is extended
- [ ] WACC sensitivity ±100bps and terminal growth ±50bps are run, with the implied range shown
- [ ] Trading multiples are applied to forward metrics; precedent multiples to LTM at announcement
- [ ] LBO floor is solved for return thresholds, not assumed at a multiple
- [ ] Football field shows all relevant methodologies on one page with consistent units
- [ ] Reconciliation paragraph explains the gaps between methodologies, not just shows them
- [ ] Recommended range is tied to a specific use case (asking price / bid / fairness range)
- [ ] No methodology is shown without the multiple range, the metric, and the source labeled

## Common Failure Modes

- **Picking the answer first, building the range around it.** The football field always lands right where the MD already promised the client. This is reverse engineering, not valuation.
- **Averaging the methodologies.** Producing "the average of DCF, comps, and precedents" is intellectually empty. Each method answers a different question. Triangulate, do not average.
- **Stale precedents.** Using deals from a different credit cycle, a different sector regime, or a different geography without adjustment.
- **DCF as a multiple in disguise.** Terminal value carries 90% of EV and is built off an exit multiple that itself comes from comps. The DCF is just multiplying the comp.
- **Heroic LBO.** A sponsor case that requires three turns of multiple expansion, 400bps of margin improvement, and a doubling of revenue to clear returns. That is a strategic case, not an LBO floor.
- **Ignoring the bridge.** Showing enterprise value ranges in a deck where the client cares about per-share. The bridge is not a footnote.
- **Premium of premium.** Applying a control premium to multiples that already came from precedent (control) transactions. Double-counting.

## Deliverable

A football field on one page with all relevant methodologies plotted in equity value per share, the EV-to-equity bridge as a separate page, sensitized DCF and LBO output, a reconciliation paragraph explaining the gaps between methodologies, and a recommended valuation range tied to the specific use case (asking price, bid, fairness range, or IC submission).
