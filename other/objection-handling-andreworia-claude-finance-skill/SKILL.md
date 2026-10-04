---
name: objection-handling
description: Builds an objection playbook that catalogs buyer pushback on price, risk, and terms and gives each a structured response with proof, for use when a counterparty is resisting the deal.
---

# Objection Handling Agent

## When to use
Use this agent when buyers or investors are pushing back on price, risk, terms, or timing and the deal team needs ready responses that hold up under pressure. It is most useful heading into a negotiation round, responding to a lowball indication, or preparing a banker to defend a valuation in a live conversation.

## What it does
It produces an objection playbook: a catalog of the objections most likely to arise, and for each one a structured response pattern with the supporting proof the team can point to.

## Method
This agent builds an objection handling playbook.

1. Catalog the objections. List every objection you expect, grouped into four buckets.
   - Price: "the multiple is too high," "comps trade lower," "your growth is already priced in."
   - Risk, terms, and timing: concentration and margin durability; escrow and earnout size; "we need more diligence" or "let us revisit next quarter."

2. Diagnose the real interest behind each. Separate a genuine concern from a negotiating tactic.
   - A tactic is answered with resolve and a reanchor; a genuine concern is answered with evidence.
   - Test which it is: if the objection survives new evidence, it is probably a tactic to move price.

3. Apply the response pattern to each objection. Use four moves in strict order.
   - Acknowledge so the counterparty feels heard, reframe into the right context, present evidence, then reanchor to your position or value.
   - Skipping the acknowledge step reads as defensive and hardens the other side.

4. Assemble the evidence for each response. Attach the specific proof behind the reframe.
   - Use a comparable transaction multiple, a cohort analysis, a quality-of-earnings finding, a signed contract, or a reference call.

5. Prepare the reanchor. Script how to bring the conversation back to your number.
   - For price, reanchor on growth, strategic value, or synergy rather than conceding the multiple.
   - End the reanchor with your number restated, not with a question that invites a counter.

6. Set fallback positions. For each objection where you may have to move, define the trade in advance.
   - Name the concession you would give and the exact thing you require in return, so nothing is conceded for free.

7. Rank and sequence. Identify deal-breakers versus noise and plan the order of engagement.
   - Grant one or two easy, honest concessions early to build goodwill, then hold the line on the issues that carry real value.

## Inputs
- The valuation or terms being defended and the rationale behind them
- The objections already raised, or the counterparty type if none yet
- Supporting evidence available: comps, diligence findings, contracts, references
- Which terms are firm and which have genuine room to move
- The deal timeline and any leverage points such as competing bidders
- The seller's walk-away threshold on price and key terms
- Which team member will voice which response in the room
- Prior rounds of pushback and how the counterparty reacted to each answer

## Output format
Claude returns an objection playbook with these sections:
- Four objection buckets: price, risk, terms, and timing, each listing the objections expected.
- Response cards: under each objection, the four-move response (acknowledge, reframe, evidence, reanchor) written as usable talking points, the proof to cite, and the fallback position if the team must give ground.
- A diagnosis note: for each objection, whether it reads as a genuine concern or a tactic.
- A sequencing note: which objections are true deal-breakers and the order to address them, described in prose rather than a table grid.

## Example
For Meridian Foods, a specialty snack maker in a sale process, a strategic buyer objects: "Nine times EBITDA is rich; the last two deals in this space cleared at seven." The playbook responds. Acknowledge: "Fair point, those are the right reference deals." Reframe: "Both targets were flat-growth private label; Meridian grows branded volume at 14 percent with 200 basis points more margin." Evidence: the three-year revenue CAGR, the gross margin premium, and shelf gains at two national grocers. Reanchor: "On forward EBITDA the effective multiple is closer to seven and a half, and the brand gives you pricing power the comps never had." The fallback, if the buyer holds firm, is to offer a modest earnout tied to next-year volume in exchange for holding the headline multiple, giving nothing on price without a matching protection. The diagnosis note marks this as a tactic rather than a genuine concern, since the buyer reopened price only after diligence confirmed the margin premium, so the plan sequences it as a hold-the-line issue to be answered last.
