---
name: escrow-and-indemnity
description: Sizes escrow and indemnity against the diligence risk register, with caps, baskets, and survival periods, for use when post-close risk has to be allocated in the purchase agreement.
---

# Escrow and Indemnity Agent

## When to use
Use this when diligence has produced findings and someone must turn them into contractual protection. The trigger is the first mark-up of the indemnity article, or a seller resisting how much consideration is held back at close. Reach for it when the argument has become "what is market" and nobody has tied the numbers to the findings.

## What it does
It produces a risk-allocation position: each finding mapped to an instrument, a general cap, a basket with its threshold and de minimis, survival periods by rep category, a sized escrow, and the insured versus uninsured comparison.

## Method
1. Start from the diligence register, then split it. Known and unknown risk take different instruments.
   - Take every material finding with its exposure and rough probability; a number with no finding behind it is a negotiating position, not a risk.
   - A quantified known issue belongs in a price cut or a specific indemnity with its own cap and escrow; the general indemnity covers what diligence missed.
   - Never let a known issue sit inside the general cap; it eats cover the buyer needs for the unknown.

2. Set the general cap. Express it against enterprise value.
   - Mid-market caps run 10 to 20 percent of value; fundamental reps — title, authority, capitalization — and fraud sit outside it, up to full consideration.
   - State the sandbagging position: whether the buyer keeps a claim for a breach it knew about at signing.

3. Choose the basket. Tipping or deductible, never both.
   - A tipping basket pays from the first dollar once claims pass the threshold; a deductible pays only the excess. The same threshold moves very different money.
   - Add a de minimis so small claims cannot be aggregated to tip the basket.

4. Set survival, then size the escrow. Match the period to the risk; the escrow is security, not the cap.
   - General reps 12 to 24 months, long enough to clear one audit cycle; tax and fundamental reps to the statute of limitations plus a tail; specifics to the life of the exposure.
   - Escrow is a fraction of the cap, often 5 to 10 percent of value, released at the survival date or in two tranches, and is not the same instrument as a holdback or a seller note with set-off.

5. Test representation and warranty insurance. It moves who pays, not what is covered.
   - A limit at 10 percent of value costs 2 to 4 percent of the limit, with retention near 0.5 to 1 percent of value that often halves after twelve months; it is worth most where the seller cannot stand behind the reps.
   - The insurer excludes known matters, so a policy retires the general escrow but never the specific indemnity behind a register finding.

## Inputs
- Enterprise value, the consideration mix, and the diligence findings register with severity and estimated exposure
- The draft rep package, and which reps the parties treat as fundamental
- Seller profile: single corporate, fund with a fixed life, or many holders
- RWI indications: limit, premium, retention, and the exclusions

## Output format
- Each finding mapped to an instrument: price, specific indemnity, escrow, condition, or insurance
- The general cap as a percentage of value, with the items outside it named
- Basket type, threshold, de minimis, and the sandbagging position
- Survival periods by rep category, and the escrow amount, term, and release schedule
- The insured versus uninsured comparison, and what the policy will not cover
- Present all terms in prose, never as markdown tables

## Example
For Verity Labs (fictional, illustrative) at an enterprise value of 250, the general cap is 10 percent, or 25, secured by an escrow of 5 percent, or 12.5, for eighteen months, behind a deductible of 1.25. Diligence found roughly 6 of unremitted sales tax across three states, so it sits outside both the basket and the cap: a specific indemnity capped at 9, or 1.5 times the estimate, with its own 6 of escrow running to the statute of limitations plus sixty days. Insurance changes the shape, not that item. A limit of 25 costs about 0.75 in premium, at 3 percent of the limit, with retention of 1.875, or 0.75 percent of value, halving after a year; the general escrow then falls to 1.25, freeing 11.25 of consideration at close. The sales-tax indemnity and its 6 survive, because the insurer will not cover what the register already names.
