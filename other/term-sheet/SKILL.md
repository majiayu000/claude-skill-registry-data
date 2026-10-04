---
name: term-sheet
description: Drafts or reads the key economic terms of a financing and explains what each term means for the parties. Use when you must draft or read the key economic terms.
---

# Term Sheet Agent

## When to use
Use this agent when you must draft a term sheet for a financing or interpret one you have received. The trigger is any point where the key economic terms are on the table and someone needs to understand or set valuation, security, preference, coupon, covenants, governance, anti-dilution, and exit rights before signing.

## What it does
It produces a term sheet with key terms and their implications: the drafted or annotated terms plus a plain explanation of what each one means for the issuer and the investor.

## Method
This agent runs structured term sheet drafting and analysis.

1. Establish the deal frame. Confirm instrument type (equity, preferred, convertible, debt), the amount, the parties, and whether you are drafting or reviewing.
   - Note the relative leverage of each side, since that determines which terms are worth contesting.
   - Confirm whether the term sheet is binding or non-binding and which provisions (exclusivity, confidentiality) survive if the deal breaks.

2. Set valuation or pricing. For equity, state pre-money and post-money valuation and resulting ownership; for debt, state coupon or spread and any original issue discount.
   - Implication: this fixes dilution or cost of capital and anchors every downstream term, so it is negotiated first.

3. Define the security type. Common, preferred, convertible note, or debt tranche.
   - Implication: security type drives priority in a downside and the shape of the return; preferred sits ahead of common but behind debt.

4. Work the liquidation preference. State the multiple (for example 1.0x) and whether it is participating or non-participating, with any cap.
   - Implication: preference determines who is paid first and how proceeds split in a modest exit; participating preferred lets the investor double-dip unless capped.

5. Set the coupon or dividend. State cash or payment-in-kind, the rate, and whether it is cumulative.
   - Implication: this accrues value to the investor and affects the issuer's cash needs; a PIK dividend preserves cash but compounds the effective preference.

6. Draft covenants and governance. Specify financial covenants, information rights, board composition, and protective or veto provisions.
   - Implication: these allocate control and constrain the issuer's freedom to raise more capital, sell assets, or change strategy.
   - Watch how protective provisions accumulate across rounds, since a stack of investor vetoes can quietly paralyze routine decisions.

7. Address anti-dilution and exit rights. Specify anti-dilution (full ratchet or weighted average), pre-emptive rights, drag-along, tag-along, redemption, and registration or IPO rights.
   - Implication: full ratchet punishes the issuer harshly in a down round, while broad-based weighted average adjusts modestly; exit rights govern how and when each party can leave.

8. Summarize implications. Close with a balanced read of who each material term favors and where negotiation leverage sits.
   - Flag any term that is off-market in either direction so it can be defended or traded.
   - Identify the two or three terms that actually drive economics, so negotiation effort is not spent on cosmetic points.

## Inputs
- Instrument type and deal size
- Valuation or pricing expectations
- The parties and their relative leverage
- Existing cap table, prior rounds, or existing debt terms
- If reviewing: the counterparty's draft term sheet
- The issuer's must-haves and walk-away points
- Expected exit path and timing

## Output format
Claude returns:
- A structured term sheet organized by term, presented as labeled sections rather than a grid.
- Each term stated with its value and followed by a short plain-language implication for issuer and investor, covering valuation or pricing, security type, liquidation preference, coupon or dividend, covenants, governance, anti-dilution, and exit rights.
- A closing summary flagging the most consequential terms, any off-market provisions, and where to negotiate.

## Example
Cascade Robotics is raising a 30 million dollar Series C, and a representative draft reads as follows. Valuation is 120 million dollars pre-money and 150 million dollars post-money, so the new investor owns 20 percent and the founders are diluted by that amount this round. The security is Series C preferred with a 1.0x non-participating liquidation preference, meaning the investor takes the greater of its money back or its as-converted share, so in a strong exit it simply converts to common. An 8 percent cumulative payment-in-kind dividend accrues value without straining company cash but raises the effective preference over time, and broad-based weighted average anti-dilution means a down round adjusts the conversion price modestly rather than punitively. The closing summary would flag the PIK dividend and the board composition as the two terms most worth negotiating.
