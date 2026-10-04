---
name: debt-sourcing
description: Sizes a company's debt need, maps the lender universe, and returns a shortlist of lenders with indicative terms. Use when you need lenders and indicative debt terms for a financing.
---

# Debt Sourcing Agent

## When to use
Use this agent when a company or sponsor needs to raise debt and you must identify who can provide it and on what terms. The trigger is a live or near-term financing need where the borrower wants a realistic view of the lender universe and indicative pricing before formally launching a process.

## What it does
It produces a lender shortlist with indicative terms: the credible providers for the situation, the structure each is likely to offer, and the pricing, leverage, covenant, and tenor ranges to expect from each.

## Method
This agent runs a structured debt financing sourcing process.

1. Size the debt need. Establish uses (acquisition, refinancing, growth capex, dividend recap) and the funding gap after equity.
   - Anchor capacity to EBITDA, free cash flow, and asset base, and compute target leverage as total debt to EBITDA.
   - Sanity-check serviceability with interest coverage (EBITDA to interest) and fixed-charge coverage; a deal that prices tightly on leverage can still fail on coverage.

2. Assess the borrower credit profile. Score scale, margin stability, cash conversion, cyclicality, and existing debt or intercreditor constraints.
   - Form an explicit view on where the credit sits: investment-grade-like, crossover, or clearly leveraged.
   - Pitfall: ignoring seasonality or customer concentration, which lenders will price for even if the trailing numbers look clean.

3. Map the lender universe. Group candidates into commercial and bulge-bracket banks, direct lenders and private credit funds, and institutional buyers of syndicated paper.
   - Note each group's typical check size, risk appetite, and speed to close; banks are cheaper but slower and more covenant-heavy, direct lenders are faster and more flexible at a premium.
   - Screen for relationship fit and sector familiarity; a lender that already knows the industry underwrites faster and holds larger.

4. Tranche the structure. Decide the shape: senior secured term loan and revolver, unitranche, second lien, mezzanine, or a combination.
   - Match each tranche to the lender type most likely to hold it and to the borrower's cost versus flexibility priorities.
   - What good looks like: the blended cost of capital is minimized subject to the borrower's certainty and covenant constraints, not just the headline spread.

5. Gather indicative terms per candidate. For each lender collect pricing spread over the reference rate, achievable leverage, covenant posture, tenor, amortization, call protection, and fees.
   - Distinguish maintenance covenants (tested each period) from incurrence covenants (tested only on action); the difference materially changes borrower freedom.

6. Score and rank candidates. Weight cost of capital, certainty of close, flexibility of terms, relationship value, and hold size.
   - Flag any lender whose appetite depends on syndicating the paper rather than holding it, since that adds execution risk.
   - Separate the all-in cost (spread plus fees plus original issue discount) from the headline spread, since fees can flip the ranking.

7. Shortlist. Recommend a focused set of lenders to approach, the structure to run with each, and the sequencing of outreach.
   - Lead with the highest-certainty provider when timing is tight, even at a small cost premium.
   - Keep a credible backup in a different lender category so the borrower retains negotiating leverage on terms.

## Inputs
- Company financials: revenue, EBITDA, free cash flow, and existing debt schedule
- Purpose and target size of the raise
- Timeline and any certainty-of-funds requirement
- Sponsor or ownership context and appetite for covenants versus cost
- Collateral, guarantees, or intercreditor constraints
- Any rating (public or shadow) and recent trading levels of existing debt
- Reference rate environment and hedging preferences

## Output format
Claude returns:
- A brief credit summary stating scale, leverage capacity, coverage, and where the credit sits on the risk spectrum.
- A recommended structure by tranche, naming each facility, its size, and its intended holder.
- A lender shortlist as ranked entries, one per lender, each stating lender type, the tranche it would provide, indicative pricing spread, achievable leverage, covenant posture, tenor, and a one-line rationale (described in prose, not a table).
- A closing section with the recommended outreach sequence and the key risks to certainty of close.

## Example
Northwind Logistics needs to raise 220 million dollars to refinance existing debt and fund a bolt-on acquisition. EBITDA is 55 million dollars, so the ask implies about 4.0x leverage, with interest coverage holding above 2.5x at indicative pricing. The credit reads as solidly leveraged but cash-generative, with some freight-cycle sensitivity. Recommended structure: a 180 million dollar senior secured term loan plus a 40 million dollar revolver. A representative shortlist entry is a direct lender offering a 220 million dollar unitranche at a spread of roughly 550 basis points, leverage up to 4.25x, incurrence-based covenants, a 6-year tenor, and soft call protection for 12 months; the rationale is single-provider certainty and speed at a modest premium to a bank-led senior deal, which is why it is recommended first given the acquisition timeline.
