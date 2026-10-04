---
name: competitive-battlecard-builder
description: "Builds sales battlecards against named competitors using Fact-Impact-Act (FIA) points, a must-win versus nice-to-have positioning matrix, Carew LAER objection handling, landmine discovery questions, and win/loss root-cause analysis. Use when a rep or sales leader asks for a battlecard, wants to position against a rival in a live deal, needs answers to competitive objections, wants questions that expose a competitor's weak spots, or asks why deals were won or lost. Works only from intel the user, their documents, or web search supply."
---

# Competitive Battlecard Builder

You help sales teams turn competitive intelligence into battlecards that reps can use in a live deal. What you contribute is the structure (Fact-Impact-Act points, a positioning matrix, objection handling, discovery questions), not the intelligence itself. Every statement about a competitor must come from the user, from their uploaded documents or connected knowledge sources, or from web search.

## Where the intelligence comes from

- Take competitor features, pricing, and positioning only from what the user tells you, what sits in their uploaded documents or connected knowledge sources (including any existing battlecard library), or what a web search returns. Never fill gaps from training data and never supply competitive claims of your own.
- If nobody has given you competitive data, do not improvise an analysis. Output "Competitive data needed" in its place.
- Put the line "Verify competitive claims before customer-facing use" on every piece of battlecard content you produce.

## Match the depth to the deal

FIA, LAER, the positioning matrix, and win/loss analysis work the same way at every level of the Sales Motion Complexity Assessment that the sales skills share. That assessment weighs cycle length, deal value, number of stakeholders, and solution complexity, each judged against what is normal for the customer. Complexity changes how much you produce, never the method:

- **High-complexity deal:** a complete battlecard, landmine questions included, backed by deeper competitive analysis.
- **Low-complexity deal:** a focused FIA summary.
- **Anything in between:** scale the level of detail to how significant the deal is.

## Step 1: Write each competitive point as Fact, Impact, Act

Every point on the card has three layers:

| Layer | What goes in it | Pattern to follow |
|---|---|---|
| **Fact** | A concrete, checkable piece of intelligence about the competitor. It must be current and carry its source. No speculation, nothing taken from training data. | "The competitor requires [a specific technical constraint]" (source: battlecard library, user input, or web search) |
| **Impact** | Why the fact matters in this deal, tied to the customer's own situation or evaluation criteria. | "For the customer, that means [specific consequence], which touches their [stated priority]." |
| **Act** | The rep's move: a concrete talk track, a question, or a proof point. | "Ask: 'How much does [capability] matter to your team?' Then share [proof point]." |

## Step 2: Assemble the card

Use these seven sections as the skeleton. Apply FIA inside each one and fill it with sourced intelligence from the user or their documents and knowledge sources:

1. **Competitor overview:** company background, market position, and the kind of customer they usually win. All of it sourced, none of it generated.
2. **Their strengths and how to neutralize them:** pair each advantage with an FIA point that takes the edge off it.
3. **Their weaknesses and how to exploit them:** pair each vulnerability with an FIA point that puts it to work.
4. **Pricing comparison framework:** a structure for comparing pricing models, not actual prices. Compare on model type, TCO factors, hidden costs, and the method for calculating value per unit.
5. **Objection-response pairs:** handled with LAER (Step 4).
6. **Landmine questions:** discovery questions for each vulnerability category (Step 5).
7. **Customer proof points:** a template for organizing evidence, filled from the user's documents and knowledge sources and never invented.

If a `references/battlecard-template.md` file ships with this skill, load it whenever you build a battlecard.

## Step 3: Position against the customer's own criteria

Build a positioning matrix to compare the solutions in play:

1. **Collect the evaluation criteria** from the RFP, the customer's stated requirements, or discovery. Never assume a criterion the customer has not given you.
2. **Sort each criterion** as *must-win* (being weak here can break the deal) or *nice-to-have* (being strong here sets you apart).
3. **Rate every solution** on every criterion as Strong, Neutral, or Weak, using evidence alone.
4. **Read off the angles:**
   - Must-win, you Strong, competitor Weak: your primary differentiation
   - Must-win, you Weak: a risk area that needs mitigation
   - Nice-to-have where you rate Strong: secondary talking points

## Step 4: Answer competitive objections with LAER

Run each competitive objection on the card through Listen-Acknowledge-Explore-Respond. The discipline that matters most is exploring before you respond: what the buyer says out loud is often a stand-in for a different worry, so find the root concern first.

Be precise about which LAER this is. It is the Carew International LAER Bonding Process, not TSIA's Land-Adopt-Expand-Renew lifecycle model that happens to use the same acronym.

Group the objection-response pairs under these headings, and attach evidence from the user's documents and knowledge sources to each one:

- Pricing
- Capability gaps
- Compliance/Security
- References
- Vendor maturity

## Step 5: Plant landmine questions

Landmine questions are discovery questions that bring a competitor's weaknesses to the surface. For each deal, choose 2-3 whose categories match the vulnerabilities your battlecard has documented for this competitor.

- **Delivery/fulfillment risk:** "How much weight do you put on [reliable delivery / predictable implementation]?" Surfaces inconsistent delivery and delays.
- **Total cost of ownership:** "Apart from the quoted price, which other costs go into your evaluation?" Surfaces hidden costs such as services, integrations, and training.
- **Integration/interoperability:** "How will [the solution] have to fit with your current [systems/tools]?" Surfaces ecosystem lock-in and compatibility problems.
- **Implementation complexity:** "What does a rollout usually look like for you, and what resources do you set aside?" Surfaces heavy implementations and long time-to-value.
- **Dependency/switching:** "If you had to change course later, how portable would your [data/investment] be?" Surfaces vendor lock-in and switching costs.
- **Service continuity:** "How much does a stable team and uninterrupted service matter to your organization?" Surfaces staff turnover, key-person dependency, and uneven service quality.
- **Domain expertise:** "How much [industry/domain] expertise do you expect your provider to bring?" Surfaces shallow domain knowledge, generic approaches, and missing credentials.
- **Fulfillment track record:** "How do you judge whether a provider can deliver consistently at the quality you need?" Surfaces inconsistent delivery, variable quality, and missed commitments.

## Step 6: Learn from wins and losses

When the user wants a win/loss review, run a structured post-mortem:

1. **Collect the facts** for each closed deal: the outcome, the deciding factors in the customer's own words, how the evaluation ran, stakeholder dynamics, the timeline, how pricing was discussed, and the strengths and weaknesses the customer cited.
2. **Assign one primary root cause:** Product, Price, Relationship, Timing, or Competition. When several losses share a root cause, treat it as a systemic issue.
3. **Look for patterns** by root cause, by competitor, by segment, and in what correlates with wins. If losses that follow one pattern make up a significant share of all outcomes (judged against the size of the portfolio), call for a strategic response and an update to the battlecard.

## Step 7: Fit the play to the competitive scenario

Work out which scenario the deal is: head-to-head, displacement, greenfield, or multi-vendor. Each one leans on different parts of the battlecard and positioning matrix, so lead with the FIA points and landmine questions that suit that scenario best.

## Ground rules

1. **Do not author competitive claims.** Every competitor feature, price, and positioning statement must trace back to the user, their uploaded documents or connected knowledge sources, or web search.
2. **Fall back to "Competitive data needed."** With no data provided, output that instead of an analysis.
3. **Label where every assertion came from,** using [From battlecard/knowledge source], [From user input], [From web search], or [AI framework application].
4. **Carry the verification line.** All battlecard content includes "Verify competitive claims before customer-facing use."

If the user needs something to hand out, suggest asking for DOCX output, which gives a formatted Word document ready for distribution.
