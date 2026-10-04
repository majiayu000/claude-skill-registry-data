---
name: Returns Sensitivity
description: Isolates the two or three variables a return genuinely depends on, presents the return surface across them, and states the entry price at which the base case stops clearing the hurdle -- when you need a walk-away price rather than a range of hopes.
---

# Returns Sensitivity

## When to use

Use this skill once a base case exists and the question turns to how much of the return is assumption. It is the discipline that runs before a final bid, and again whenever someone proposes stretching for the asset. Its output is a single number the deal team commits to in advance: the price above which the base case no longer clears the fund's own hurdle.

## What it does

Produces a sensitivity note: a one-at-a-time elasticity test that separates the variables that move the return from the ones that decorate it, a return surface across the two that survive, a note of which of them the sponsor actually controls, and a stated walk-away price in both multiple and enterprise value.

## Method

### Step 1 -- Strip the collinear variables before flexing anything

Revenue growth, margin and exit-year EBITDA are one variable arriving three ways: flex the terminal one only, or the surface double-counts and no one can read it. Entry leverage is not a function of price -- lenders size off EBITDA, not off what you agreed to pay -- so hold debt fixed in dollars while entry multiple moves.

### Step 2 -- Run the elasticity test with comparable increments

Move each candidate one realistic increment either way, everything else at base: a turn of exit multiple, ten per cent of exit-year EBITDA, half a turn of entry, a hundred basis points of rate, fifteen million of cumulative cash generation. Increments must be equally likely, or the ranking is an artefact of how far you pushed each one. Keep what moves the IRR by more than a point or two; say which you discarded and why.

### Step 3 -- Build the surface across the survivors

Cross the two dominant variables on a three-by-three or five-by-five grid with the base case at the centre, and report the IRR in every cell -- in prose, one line per row, never as a table. Then count the cells that clear the hurdle. That count is the finding; the individual cells are the evidence for it.

### Step 4 -- Mark what the sponsor controls

Of the dominant variables, one is usually the entry price and the others are usually not: the exit multiple belongs to the market, exit EBITDA to management and the market together, entry price to you alone. If every cell that clears the hurdle requires multiple expansion or a beat on plan, the return is not sensitive to those things, it is dependent on them. Use that word in the memo.

### Step 5 -- Solve for the walk-away price

Hold everything else at base and solve for the entry multiple at which the base case returns exactly the hurdle. Keep the exit convention you committed to: if the base case exits flat to entry, a lower entry price lowers the exit assumption too, and the walk-away lands further below the ask than people expect. A walk-away computed with the exit multiple pinned at the ask is not a walk-away -- it is a multiple-expansion assumption wearing a disguise. State the answer as a multiple and an enterprise value, before the bid is due, and record it.

## Inputs

- The base-case model: entry, capital structure, operating plan, exit
- Fund hurdle rate and the hold period the hurdle is measured over
- Cumulative cash generation over the hold, by year
- Exit multiple evidence: comparable trading and transaction ranges
- The asking price or guided range from the process

## Output format

1. Variables tested, and the collinear ones removed
2. Elasticity results: IRR points gained and lost per increment
3. The two or three that survive, ranked
4. Return surface across them, in prose, one line per row
5. Which variables the sponsor controls
6. Walk-away price: multiple, enterprise value, and gap to the ask

Total length: 500-800 words. The walk-away price appears in the first paragraph and the last.

## Example

**Sensitivity note (fictional -- Ardleigh Clinical Labs, outsourced diagnostics):**

Entry at 11.0x QoE EBITDA of $25.0M is EV of $275.0M; with $125.0M of debt and $9.0M of fees, equity at risk is $159.0M. The base case reaches $40.0M of EBITDA in year 5, pays down $55.0M, and exits flat at 11.0x: exit equity of $370.0M, 2.33x and 18.4% against a 20% hurdle. Elasticity: a turn of exit multiple is worth +2.5 / -2.7 IRR points, ten per cent of exit EBITDA +2.7 / -3.0, half a turn of entry +0.6 / -0.5, fifteen million of cash generation +0.9 / -1.0, and a hundred basis points of rate about a third of a point. Two variables carry the deal; rate and cash generation are noise beside them.

The surface, exit multiple across 10.0x, 11.0x and 12.0x: at $36.0M of exit EBITDA, 12.8%, 15.4% and 17.9%; at $40.0M, 15.7%, 18.4% and 20.9%; at $44.0M, 18.4%, 21.1% and 23.6%. Three cells of nine clear the hurdle, and each of the three requires either a turn of expansion or a ten per cent beat on the plan -- neither of which the sponsor controls. Solving for 20.0% with the exit held flat to entry gives 9.85x, or $246.3M of enterprise value: $28.8M below the ask, returning 2.49x on $130.3M of equity. Pinning the exit at 11.0x while flexing entry would report 10.6x instead -- $265.0M, $18.7M higher -- and that difference is four-tenths of a turn of expansion nobody has agreed to. The walk-away is 9.85x.
