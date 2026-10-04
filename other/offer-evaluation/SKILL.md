---
name: offer-evaluation
description: Compares competing bids on more than price by scoring each on certainty of close, financing, conditionality, terms, and fit, for use when choosing among offers.
---

# Offer Evaluation Agent

## When to use
Use this agent when you have received more than one offer and must compare them on dimensions beyond the headline price. It is essential in a competitive sale process where a higher nominal bid may carry more financing risk, more conditionality, or worse terms than a lower one, and the seller needs a clear-eyed, apples-to-apples view.

## What it does
It produces a bid comparison: each offer scored across price, certainty of close, financing, conditionality, deal terms, and strategic or cultural fit, rolled into a weighted score and a risk-adjusted view of value.

## Method
This agent runs a bid comparison and offer scoring process.

1. Normalize the price. Restate every bid on a common basis before anything else.
   - Reconcile enterprise value, treatment of cash and debt, and the working capital peg so headline numbers are comparable.
   - Discount a stock component for volatility and risk-adjust an earnout for the probability it is actually paid, so contingent value is not counted at face.

2. Define the scoring dimensions. Use six: price, certainty of close, financing, conditionality, deal terms, and strategic or cultural fit.
   - Keep the definitions fixed across all bids so scores mean the same thing for each.

3. Assess certainty of close for each bid. Judge how likely a signed deal is to actually close.
   - Weigh regulatory or antitrust risk, board and shareholder approvals, and the counterparty's track record of closing what it signs.

4. Assess financing. Establish whether the money is real and committed.
   - Distinguish committed financing from best-efforts, cash on balance sheet from new debt, and flag any financing condition that lets the buyer walk.

5. Assess conditionality. Score how easily the buyer can escape or renegotiate.
   - Count the number and severity of closing conditions, diligence outs, and material-adverse-change provisions; fewer and narrower is better.

6. Assess deal terms. Weigh the terms that shift value after price is agreed.
   - Compare escrow and holdback size, indemnity caps and survival, the reps and warranties package, non-competes, and employee and management commitments.

7. Assess strategic and cultural fit where it matters to the seller.
   - Consider continuity for employees, the brand, and the customer base, especially for a founder-led or mission-driven seller.

8. Apply weights and score. Turn the assessment into a single comparable figure.
   - Assign each dimension a weight reflecting the seller's priorities, score each bid, compute a weighted total, then state the risk-adjusted value, which can reorder the bids versus headline price.

9. Recommend. Name the leading bid, the key trade-off against the runner-up, and the specific points to negotiate up before signing.

## Inputs
- The full terms of each competing offer, not just the price
- The seller's priorities, for example maximum value versus speed and certainty
- Financing details for each bidder and their acquisition history
- Known regulatory, approval, or diligence risks
- The relative weight the seller places on each dimension
- The seller's tolerance for contingent or deferred consideration
- Any non-negotiable terms such as employee retention or brand continuity

## Output format
Claude returns a bid comparison with these sections:
- Normalized price: for each offer, the common-basis value and how it was derived, including the discount applied to stock or earnout.
- A dimension scorecard: each bid scored across the six dimensions with a short rationale per score, expressed in prose such as "Bid A scores high on price but low on financing certainty," never as a table grid.
- Weighted and risk-adjusted results: the weighted total and the risk-adjusted value for each bid, with the resulting ranking.
- A recommendation: the leading bid, the main trade-off versus the runner-up, and the terms to push before signing.

## Example
For Northwind Logistics, three bids arrive. Bid A: 320 million all cash, committed financing, 10 percent escrow, no financing out. Bid B: 340 million, 70 percent cash and 30 percent acquirer stock, best-efforts financing, a regulatory condition. Bid C: 335 million with a 30 million earnout over two years. Normalized: Bid B's stock is discounted for volatility to an effective 332 million, and Bid C's earnout is risk-adjusted at 60 percent probability to an effective 318 million. On certainty of close, Bid A leads because it carries no financing or regulatory out, while Bid B's antitrust condition adds real risk. Weighting certainty heavily, as the seller wants a clean exit, Bid A ranks first on a risk-adjusted basis despite the lower headline. The recommendation: pursue Bid A, and push the escrow from 10 to 7 percent and shorten indemnity survival to eighteen months before signing.
