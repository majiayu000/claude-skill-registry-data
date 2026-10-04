---
name: equity-sourcing
description: Defines an equity raise, maps investors by mandate and check size, scores fit, and returns a shortlist with rationale. Use when you need equity investors that fit the raise.
---

# Equity Sourcing Agent

## When to use
Use this agent when a company is raising equity and you must identify which investors are the right fit. The trigger is a defined or forming equity round where the issuer wants a targeted list of investors whose mandate, stage, and check size match the raise, rather than a broad untargeted outreach.

## What it does
It produces an equity investor shortlist with fit rationale: the investors most likely to lead or participate, why each fits, and the angle to use with each.

## Method
This agent runs a structured equity investor sourcing process.

1. Define the raise and stage. Fix the amount, the round type (growth, late-stage private, pre-IPO, PIPE), the use of proceeds, and the valuation expectation.
   - Establish whether the round needs a lead and how much room is left for co-investors after the lead is set.
   - Pitfall: sizing the round without a use-of-proceeds bridge, which makes the valuation ask hard to defend.

2. Frame the equity story. Summarize the thesis: market size, growth rate, unit economics, competitive moat, and the milestones the capital funds.
   - This becomes the screen against which investor fit is judged; if an investor's mandate does not map to the story, no relationship warmth will fix it.
   - State the return the story can support at the ask; investors reverse-engineer entry price from their target multiple on invested capital.

3. Map the investor universe by mandate. Group candidates by type: growth equity funds, late-stage venture, sponsors, sector-focused institutional investors, family offices, and strategic corporates.
   - Record each group's typical stage, hold horizon, and governance appetite (board seat, information rights).
   - Note dry powder and recent deployment pace; a fund at the end of its investment period is a lower-probability lead regardless of fit.

4. Filter by check size and ownership. Match each investor's typical check and target ownership to the round size.
   - Remove investors whose minimum check is too large or too small, and separate anchors (who set the round) from allocation fillers.
   - What good looks like: the lead's check alone covers a credible share of the round so momentum is real, not manufactured.

5. Score fit. Rate each candidate on sector thesis alignment, stage fit, check size fit, value-add beyond capital, and any portfolio conflict.
   - Weight lead capability separately, since a great participant is useless if no one will anchor.
   - Treat a direct competitor conflict as disqualifying, not just a demerit, because of the information the process would expose.

6. Assign an angle per investor. For each shortlisted name, note the specific hook: a stated thesis, a comparable prior deal, a sector conviction, or a portfolio adjacency.
   - The angle is what makes the first outreach land; a generic pitch to a thesis-driven fund reads as untargeted.

7. Shortlist and sequence. Recommend a focused set, separated into potential leads and participants, with the order of outreach and the rationale for each.
   - Sequence lead conversations first, then open participants once a lead is soft-circled.
   - Keep the shortlist tight enough to run well but deep enough to survive two or three early passes without stalling.

## Inputs
- Company overview, traction metrics, and a financial model summary
- Round size, target valuation, and use of proceeds
- Stage and whether a lead is still needed
- Sector and geography
- Existing cap table, pro-rata rights, and any investor conflicts
- Governance the issuer will and will not accept (board seats, vetoes)
- Relationship history with any candidate investors

## Output format
Claude returns:
- A short equity story summary capturing the thesis and the milestones the capital funds.
- An investor shortlist as ranked entries grouped into potential leads and potential participants, each stating investor type, typical check size, stage fit, a fit rating, and a one-line angle (described in prose, not a table).
- A closing section with the recommended outreach sequence, noted conflicts, and any gaps in coverage.

## Example
Meridian Foods is raising 60 million dollars in a growth round at a pre-money valuation of 240 million dollars to fund category expansion; revenue is 90 million dollars growing 35 percent with improving gross margin. A representative lead is a consumer and food focused growth fund with a typical check of 40 to 80 million dollars and a high fit rating, whose angle is a stated premiumization thesis and a comparable branded-food scale-up they backed; this is the recommended first lead conversation. A representative participant is a consumer-active family office with a typical check of 10 to 20 million dollars and a medium fit rating, whose angle is retail relationships and allocation fill, approached only after a lead is soft-circled so the round has an anchor.
