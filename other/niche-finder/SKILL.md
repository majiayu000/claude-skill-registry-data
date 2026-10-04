---
name: niche-finder
description: Turn recurring work complaints into a defensible, specific niche statement grounded in problems the user has personally experienced. Use whenever someone wants to find or choose a niche, identify a service or consulting offer, turn workplace frustrations into a business idea, find a first-client angle, or says they do not know what niche to pursue. Prefer lived evidence over trends and never invent a market the user did not describe.
---

# Niche Finder

Find the niche already hiding inside work the user complains about. Treat lived friction as stronger evidence than market trends: it carries the buyer's language, edge cases, frequency, and cost.

## Input

Ask the user for a raw list of recurring work complaints: processes they dread, tools they curse, reports nobody trusts, or tasks they would automate in their sleep.

If they provide only a broad category such as “education technology” or “marketing,” ask for the last specific bad occurrence before continuing. Do not manufacture examples for them.

## Method

For each complaint:

1. Extract the concrete failure in the user's own words. Name the silent wrong join, day-long export, duplicate record, missed handoff, or other observable failure—not a broad category.
2. Score it from 1–5 on:
   - **Frequency** — how often it recurs.
   - **Pain** — its cost in time, money, risk, or dread.
   - **Who else** — how many comparable people or companies plausibly face it.
   - **Can charge** — whether a business would pay to make it stop.
3. Rank by total score. Prefer the recurring, payable, specific pain over the loudest or most fashionable complaint.
4. For the winner, identify three edge cases the user already knows that an outsider would need months to learn. These details are the user's practical advantage.

When the input lacks enough evidence to score an axis, ask the minimum question needed rather than guessing.

## Output

Return only:

**Niche statement**

> We help [specific people] turn [specific painful input] into [trusted output] in [time], without [what they dread today].

**Your unfair advantage**

- [edge case 1]
- [edge case 2]
- [edge case 3]

**Peer sentence**

> [One sentence the user can say to a peer with this pain that makes the peer feel understood.]

## Guardrails

- Use only problems the user personally described. Never suggest a trendy category or unrelated market.
- Keep the user's concrete language; remove abstract phrases such as “optimize workflows” or “leverage AI.”
- Prefer boring, specific pain over exciting, broad positioning.
- If the strongest complaint scores low on **Can charge**, say plainly that it may be a hobby rather than a niche and ask for another complaint.
- Do not produce branding, product features, market-size claims, or an implementation plan. The deliverable is one defensible niche statement and the lived proof behind it.
