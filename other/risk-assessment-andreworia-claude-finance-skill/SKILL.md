---
name: risk-assessment
description: Builds a deal risk register with likelihood, impact, owners, and mitigations for transactions that carry risks needing clear ownership and response.
---

# Risk Assessment Agent

## When to use
Use this agent when a deal carries risks that need owners and responses: at kickoff to establish a baseline register, before a key committee, or when new diligence findings change the risk picture. It is the right tool whenever risks are being tracked informally and need to be made explicit and owned. Run it again whenever a milestone or finding materially shifts the picture.

## What it does
Produces a deal risk register that captures each material risk with its category, likelihood, impact, an assigned owner, a mitigation, and a residual risk rating after mitigation.

## Method
1. Frame the transaction: capture the deal, the parties, the timeline, and the value at stake.
   - Severity only means something in context, so record what a bad outcome would cost in money, time, or reputation.
   - Note the hurdle or return the base case assumes, since some risks threaten it directly.

2. Identify risks by category so nothing is missed.
   - Commercial: demand, customer concentration, pricing, competitive response.
   - Financial: leverage, working capital, covenants, financing certainty.
   - Legal and regulatory: consents, antitrust, litigation, change of control.
   - Execution: integration, key-person retention, timeline slippage.
   - Market: rates, cycle, and financing conditions.

3. Score likelihood on a simple scale of low, medium, high.
   - Anchor the score to evidence where possible rather than gut feel.

4. Score impact on the same scale against value, timeline, or reputation.
   - Separate a high-impact rare event from a low-impact frequent one; both need visibility.

5. Combine likelihood and impact into an inherent risk rating.
   - This lets the register be sorted so the committee sees the worst first.

6. Assign a single named owner to each risk.
   - Diffuse ownership is a red flag; every risk gets one accountable person with the authority to act.

7. Define a mitigation or response for each material risk.
   - Choose to reduce, transfer (for example reps and warranties insurance or an escrow), accept, or add a condition to close.
   - Make the mitigation concrete and dated, not aspirational.

8. Re-score residual risk after the mitigation.
   - Show what remains once the plan is in place; residual, not inherent, is what the committee is accepting.

9. Flag the top risks and set a review cadence tied to deal milestones.
   - Call out any risk that stays high after mitigation as a decision point.

## Inputs
- Deal description, parties, timeline, and value at stake
- Diligence findings and any known issues to date
- The base-case return or hurdle the deal must clear
- Names of workstream leads available to own risks
- Any deal-specific constraints such as financing terms or regulatory context
- Prior risk registers from comparable deals if available

## Output format
Claude returns a ranked risk register, most severe first, described in prose:
- A summary block naming the top three risks and any that remain high after mitigation.
- One entry per risk, each stating the risk, its category, likelihood, impact, inherent rating, assigned owner, mitigation or response, and residual rating.
- A review-cadence note tying the next refresh to specific deal milestones.
No markdown table is used; each register row is written as a short prose entry.

## Example
For Meridian Foods' acquisition of a regional bakery: Commercial, customer concentration, the top two grocers are forty percent of revenue; likelihood medium, impact high, inherent high; owner the commercial diligence lead; mitigation is a renegotiated multi-year supply agreement as a condition to close; residual medium. Legal, antitrust clearance in one overlapping region; likelihood medium, impact high, inherent high; owner outside counsel; mitigation is early regulator engagement and a divestiture backstop; residual medium. Execution, retention of the head baker and plant manager; likelihood medium, impact medium, inherent medium; owner the integration lead; mitigation is retention packages signed at close; residual low. The summary flags customer concentration and antitrust as the two risks the investment committee is really being asked to accept, and sets the next review for the confirmatory-diligence milestone.
