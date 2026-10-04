---
name: valuation-analysis
description: Runs multiple valuation methods and reconciles them into a single defensible football-field range when you need one conclusion across approaches.
---

# Valuation Analysis Agent

## When to use
Use this when you need one defensible valuation range across methods, not a single point estimate from one approach. Typical triggers: pitching a target, setting a fairness range, or preparing a board discussion where each method must be shown and reconciled. Reach for it when the answer has to survive scrutiny from every angle.

## What it does
It produces a football-field valuation range: a plotted set of value bands, one per method, with the driver behind each band spelled out, reconciled into a single concluded range with a stated rationale.

## Method
1. Frame the subject. Fix what is being valued and how the pieces bridge.
   - Confirm enterprise versus equity value, the valuation date, share count and net debt for the bridge, and the metric base (LTM and forward EBITDA, EBIT, EPS).

2. Select the method set. Choose bands that fit the situation.
   - Standard bands: trading comparables, precedent transactions, and DCF, plus an LBO-implied floor or a 52-week range for a public target where relevant.

3. Run trading comparables. Derive a market read from peers.
   - Screen a peer set, spread EV/EBITDA and P/E, clean for non-recurring items, and apply the low-to-high multiple range to the subject metric for an implied band.
   - Keep the numerator and denominator consistent: EV multiples pair with EBITDA and EBIT, equity multiples pair with EPS.

4. Run precedent transactions. Derive a control-value read from past deals.
   - Screen comparable deals, compute paid EV/EBITDA and control premia, adjust for cycle and synergy, and apply the range to the subject.
   - Separate strategic buyers from sponsors so synergy-rich prices do not overstate what a financial buyer would pay.

5. Run the DCF. Derive intrinsic value from cash flows.
   - Project unlevered free cash flow, build WACC, compute terminal value by Gordon growth and by exit multiple, discount, and bridge enterprise value to equity; the sensitivity corners set the band width.
   - Cross-check terminal value as a share of total EV so the tail does not silently drive the whole answer.

6. Run the LBO check where relevant. Establish a financial-buyer floor.
   - Solve for the entry price a sponsor could pay at a target return; this anchors the lowest supportable band.
   - Hold leverage and the exit multiple at realistic levels so the floor reflects a deal a lender would actually fund.

7. Plot the football field. Lay the methods on one common axis.
   - Draw each method as a horizontal band from its low to high implied value, labeled with the single driver of that width (multiple range, WACC and growth, premium range).

8. Reconcile and conclude. Turn many bands into one answer.
   - Weight methods by reliability for this situation, note where bands overlap, discount outliers with a stated reason, and land on one concluded range with the logic for it.
   - Where the situation demands control value, lean on precedents and the LBO floor; where it is a minority read, lean on trading comps and the DCF.

## Inputs
- Subject financials: LTM and forward EBITDA, EBIT, and EPS
- Net debt, minority interest, preferred, and diluted shares for the bridge
- Peer-company candidates, or permission to propose them
- Precedent-deal candidates, or permission to propose them
- DCF assumptions or the underlying operating model
- The valuation date and whether an enterprise or equity conclusion is wanted

## Output format
- A method-by-method section, each stating the implied low and high value and the single driver that sets the width, in prose
- A football-field summary listing every band on one common value scale
- A reconciliation paragraph explaining overlaps, weightings, and any discounted outliers
- One concluded value range with its rationale
- Describe every band and its inputs in prose, never as a markdown table

## Example
For Meridian Foods (fictional, illustrative): trading comps at 8.0x to 9.5x LTM EBITDA of 120 imply 960 to 1,140. Precedents at 9.5x to 11.0x imply 1,140 to 1,320, richer on control premia. The DCF spans 1,050 to 1,260 across WACC of 9 to 10 percent and terminal growth of 2 to 3 percent. The LBO floor sits near 980 at a sponsor return hurdle of 20 percent. The bands overlap most tightly around 1,050 to 1,200, so the concluded range is 1,050 to 1,200, leaning on comps and DCF and discounting the top precedent as a synergy-heavy outlier that a financial buyer would not match.
