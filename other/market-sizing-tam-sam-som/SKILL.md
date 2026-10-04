---
name: market-sizing-tam-sam-som
description: "Sizes TAM, SAM, and SOM using independent top-down and bottom-up methods, narrowing each step with explicitly named constraints (geography, segment, go-to-market capacity) rather than an arbitrary percentage. Use when a market-size figure has to hold up under scrutiny in a business case or investor conversation, not just sound impressively large."
---

# Market Sizing (TAM/SAM/SOM)

## Purpose

Quantitatively sizes the market and the genuinely reachable share of it —
not to produce an impressively large headline number, but to give a
defensible, traceable estimate that a business case or investment
conversation can actually stand on.

## Anchored in research

- The standard TAM/SAM/SOM framework (Total Addressable Market / Serviceable
  Addressable Market / Serviceable Obtainable Market), widely used in
  venture and strategic planning to move from "the size of the whole
  market" down to "what we could realistically capture" in three explicit,
  progressively narrower steps.
- stratarts — market-opportunity-analyzer (a public reference
  implementation of a market-sizing workflow)
- Business Opportunity Scout (buYoung) (a public reference implementation of
  opportunity scouting and sizing)

## Method

1. **Define TAM (Total Addressable Market) using two independent
   approaches, not one.**
   - **Top-down**: start from a recognized industry or market-research
     figure for the broadest relevant category, and state the source.
   - **Bottom-up**: start from a realistic unit economic (price per
     customer, or revenue per transaction) and multiply by a defensible
     estimate of the total number of potential buyers.
   Running both and comparing them is the single most effective way to
   catch an inflated or nonsensical TAM before it enters a business case —
   see `../agents/market-sizing-cross-validator.md`, which exists
   specifically to do this cross-check.
2. **Narrow TAM to SAM (Serviceable Addressable Market)** by applying the
   real constraints of the business: geography actually served, product
   segment actually addressed, language/regulatory/channel constraints.
   Every narrowing filter should be named explicitly — "we only serve
   [region/segment] because [reason]" — not folded silently into a lower
   percentage.
3. **Narrow SAM to SOM (Serviceable Obtainable Market)** using realistic
   go-to-market constraints over a defined time horizon: sales capacity,
   competitive response, adoption curve, channel access. SOM should be
   expressed with an explicit time frame ("reachable within 3 years"), not
   as a static number — reachable share changes as the business matures.
4. **Make every multiplier and percentage traceable to its source.** For
   each number used in the chain, note whether it's: user-supplied, an
   industry benchmark (name the source), an assumption
   (`[assumption — verify]`), or pulled from a connected external data
   source (see `../../../meta/external-data-mcp.md`). A TAM/SAM/SOM chain is
   only as credible as its weakest, least-traceable multiplier.
5. **Watch for double counting** when multiple narrowing factors are chained
   together (e.g. "30% of the market × 15% conversion") — check whether the
   two percentages are actually independent of each other, or whether one
   already implicitly contains the other.
6. **Sanity-check the result against an external anchor** if one is
   available: a known industry revenue figure, a comparable company's
   disclosed revenue, or a connected external data source. This is a
   magnitude check, not a precise validation — is the number the right
   order of magnitude, or off by 10x without an explanation?
7. **Route the result through cross-validation before it's used.** Before
   the TAM/SAM/SOM figures go into a business case or in front of a
   decision-maker, run them through
   `../agents/market-sizing-cross-validator.md`, which independently
   re-derives the number using a second method and reports a confidence
   level.

## Available scripts

- **`scripts/market_sizing.py`** -- computes TAM from top-down and/or
  bottom-up inputs (Method step 1), flags a divergence when the two methods
  disagree by more than a configurable ratio (default 3x), then narrows to
  SAM and SOM using explicitly named filters/constraints (steps 2-3) --
  from EACH available TAM basis, so you see a range instead of one
  arbitrarily-picked number. Run it once you have at least one TAM input;
  supplying both top-down and bottom-up is strongly preferred, since the
  cross-check is the point.

  ```bash
  python3 scripts/market_sizing.py --example > input.json   # see the input shape
  python3 scripts/market_sizing.py input.json
  ```

  Stdlib only (json, argparse) -- no install needed. Warns (not errors) if
  a divergence is detected; errors only on missing/invalid required fields.

## What this skill does NOT do

- Doesn't make the final decision for you — it produces a structured draft
  to support a human decision.
- Doesn't confirm figures, market data, or competitor data from memory — it
  uses the inputs you provide, or clearly flags an assumption
  (`[assumption — verify]`).
- Doesn't rely on a single calculation path as sufficient proof — a
  top-down-only or bottom-up-only estimate should be treated as provisional
  until cross-checked by the other method or by
  `../agents/market-sizing-cross-validator.md`.

## Refinement notes

Areas to keep deepening with real practice:

- your own rules of thumb and heuristics for this technique
- concrete templates (into `../../references/`)
- reference cases / your own examples
- what this skill deliberately does *not* do (guardrails, common mistakes) —
  add to the list above

Once this section is filled in and validated in practice, update the
`maturity` field in `skills_index.json` to `draft`, `validated`, or
`canonical` (see `../../../meta/maturity_levels.md`). **Don't add new fields
to the frontmatter** — `name` and `description` are the only ones allowed
(see `../../../meta/frontmatter_schema.md`).

## Continue from here

- Next in this pack: `../competitive-and-five-forces-mapping/SKILL.md` —
  Maps the competitive dynamics and structural forces of the industry.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — this pack's shared guardrails
- `../../../meta/external-data-mcp.md` — an optional external data MCP
  (Market Sizing MCP Server / TAM-MCP-Server) as underlying data for the
  calculation or for cross-checking, if one is connected in the user's
  environment. Not a dependency — the skill works without it.
- `../agents/market-sizing-cross-validator.md` — a delegatable agent that
  cross-checks the calculation this skill produces before the figure is
  used in a business case
