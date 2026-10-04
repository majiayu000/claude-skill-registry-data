---
name: investor-targeting
description: Prioritizes which investors to approach first by tiering candidates, assigning an angle to each, and sequencing outreach. Use when you need to prioritize who to approach first.
---

# Investor Targeting Agent

## When to use
Use this agent when you have a pool of possible investors and must decide who to approach first. The trigger is the point after a broad universe exists but before outreach begins, when you need a disciplined priority order rather than contacting everyone at once.

## What it does
It produces a tiered investor target list with angles: candidates sorted into priority tiers, the specific angle to use with each, and the sequence in which to approach them.

## Method
This agent runs a structured investor targeting and tiering process.

1. Confirm the raise parameters. Restate the amount, instrument, valuation or pricing, and timeline so targeting is judged against a fixed goal.
   - A moving target on size or valuation makes any prioritization unstable, so lock these first.

2. Assemble the candidate pool. Pull together the investors under consideration from prior sourcing or relationships, with their type, check size, and mandate.
   - Deduplicate and remove any investor with a hard conflict before scoring, so effort is not wasted.

3. Define scoring criteria. Set the axes that determine priority: fit with the thesis, check size match, probability of engaging, speed to decision, value beyond capital, and relationship warmth.
   - Weight the axes to the situation; in a time-boxed raise, speed to decision and warmth matter more than marginal fit.

4. Score each candidate. Rate every investor on the criteria and compute a priority signal.
   - Keep the scoring explicit so the tiering is defensible when a decision-maker questions the order.
   - Down-weight investors who habitually take meetings but rarely lead; meeting activity is not the same as decision probability.

5. Assign tiers. Sort into Tier 1 (high fit and high probability, approach first), Tier 2 (good fit, approach as the process builds), and Tier 3 (opportunistic or backup).
   - Cap Tier 1 to a manageable number so management time goes to the names most likely to anchor.
   - Revisit the tiers as feedback arrives; a Tier 2 name that leans in fast can be promoted, and a cold Tier 1 name demoted.

6. Assign an angle per investor. For each name, note the specific hook: a stated thesis, a comparable prior deal, a sector conviction, a portfolio adjacency, or a warm relationship.
   - What good looks like: the angle references something specific to that investor, not a generic pitch.
   - Prefer a warm introduction over a cold approach where one exists; a referred first contact converts to a meeting far more often.

7. Sequence the outreach. Order the approach to build momentum: lead-capable and highest-conviction names first to anchor the round, then broaden.
   - Note dependencies, such as holding participants until a lead is soft-circled so the book has a spine.
   - Avoid saturating the market at once; a controlled sequence preserves the ability to create competitive tension between interested parties.

8. Summarize. Present the tiered list, angles, and sequence with the rationale for the ordering.

## Inputs
- The raise parameters (amount, instrument, valuation, timeline)
- The candidate investor pool with type and check size
- Each investor's mandate and stated thesis where known
- Relationship history or warmth with any candidates
- Constraints: conflicts, exclusivity, or timing sensitivities
- Whether a lead is still needed or already secured
- Management bandwidth for meetings during the window

## Output format
Claude returns:
- A brief statement of the scoring criteria and their weighting.
- A tiered target list grouping candidates into Tier 1, Tier 2, and Tier 3, described as lists rather than a grid, each entry naming investor type, its priority rating, and its angle.
- A closing section with the recommended outreach sequence, any dependencies, and the reasoning behind the order.

## Example
Meridian Foods is raising 60 million dollars and has a pool of 18 candidate investors, scored with extra weight on speed and warmth given a tight window. Tier 1 holds two names to approach first: a consumer-focused growth fund with a high rating whose angle is a stated premiumization thesis and a comparable branded-food deal, and a second growth fund with a high rating whose angle is an existing relationship from a prior process. Tier 2 holds two sector-adjacent funds and a family office at medium ratings to open as momentum builds, and Tier 3 holds three generalist funds with weaker thesis fit as backup. The recommended sequence opens with the two Tier 1 leads to soft-circle an anchor, then opens Tier 2 participants to fill allocation, and holds Tier 3 in reserve only if the book is soft.
