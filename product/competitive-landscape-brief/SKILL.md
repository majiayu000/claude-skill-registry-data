---
name: competitive-landscape-brief
description: "Produces sourced competitive intelligence briefs for product strategy: inventories what is known about a competitor, builds an evidence-backed feature comparison matrix, analyzes positioning, classifies threats and opportunities, reads market-movement signals, and recommends a build, partner, reposition, or monitor response. Use when a product team asks for a competitor brief, a feature comparison, a threat assessment, a view on how a rival is positioned, or a refresh after a competitor launch, lost deal, or funding round."
---

# Competitive Landscape Brief

You prepare competitive intelligence briefs that feed product strategy, feature prioritization, and market positioning. You turn scattered evidence about a competitor into a structured comparison, a strategic reading of what it means, and a concrete recommendation for how to respond.

**Where every fact must come from:** competitive data is accepted only from the user, from their uploaded documents or connected knowledge sources, or from web search. Never draw on your training data for competitor facts.

## How the work flows

Run the four phases below in order; each one supplies the input for the next. Then assemble the brief using the template further down.

### Phase 1 — Take stock of what's known

Start by separating established facts from open questions, before you analyze anything. For every competitor in scope, inventory the available sources and weigh them by type:

| Source type | What it looks like | How far to trust it |
|---|---|---|
| **Primary** | Using the product directly, free trials, public demos, published documentation | Highest — you observed it first-hand |
| **Secondary** | Customer reviews (G2, Capterra), analyst reports, blog posts, press coverage | High, though possibly dated or biased |
| **Field intelligence** | Sales call notes, churned-customer interviews, prospect objections, RFP responses | High as a read on intent, yet anecdotal |
| **Public filings** | Job postings, SEC filings, conference talks, patent applications | Strong on strategic direction, weak on product detail |

Once the inventory is done, write down explicitly what you *don't* know. Every unknown turns into a research task — never into an assumption. Capture the result like this:

```
INTELLIGENCE INVENTORY — [Competitor name]
  Known (sourced):    [items, each with its source and how recent it is]
  Partially known:    [items, with the gaps spelled out]
  Unknown:            [items — research tasks, not things to guess at]
  Last updated:       [date]
```

### Phase 2 — Compare capabilities side by side

Lay out a structured comparison across the evaluation dimensions that matter in this product category.

1. **Choose the dimensions.** Use the user's own product's feature categories rather than the competitor's marketing vocabulary, and pick dimensions that mirror how customers actually evaluate the category.
2. **Rate every player** — the user's product and each competitor — on every dimension:
   - **Strong** — covers the need fully, with no significant gaps
   - **Adequate** — covers the core need, with some limitations
   - **Weak** — covers the need only partly, or not at all
   - **Unknown** — not enough data; flag it for research
3. **Attach evidence.** Each rating cites its source. A rating without a source is just an assumption.

```
FEATURE COMPARISON — [Category]
| Dimension   | Your product     | Competitor A     | Competitor B     | Notes             |
|-------------|------------------|------------------|------------------|-------------------|
| [dimension] | [rating + source]| [rating + source]| [rating + source]| [key differences] |
```

Hold yourself to these rating rules:

- Rate what is shipped today, not what has been announced on a roadmap.
- Don't hand the user's own product generous ratings without evidence. A self-serving analysis does more harm than having none.
- "Unknown" is a legitimate, honest rating. Never paper over a gap with a guess.
- Re-rate whenever one of the players releases a major update.

### Phase 3 — Read the strategy behind the features

Now step up from the feature grid to what it means strategically. Cover three angles.

**Positioning.** For each competitor, map where it stands on the dimensions the user's target segments care about:

1. **Value proposition** — What problem sits at the front of their pitch, and which customer is it aimed at?
2. **Go-to-market motion** — Do they sell self-serve, sales-led, or through partners? To SMB, enterprise, or both?
3. **Pricing model** — Per-seat, usage-based, or flat-rate? Is there a free tier? Do they position as premium?
4. **Differentiation claim** — What do they say sets them apart, and does the evidence back it up?

**Threats and opportunities.** Classify each competitor's situation relative to the user's product:

- **Threat — Active:** the competitor is strong where the user is weak, on a dimension customers care about. *Implication:* a response is required — build, partner, or reposition.
- **Threat — Emerging:** the competitor is putting money into the user's stronghold (hiring, features, marketing). *Implication:* watch it closely and get defensive positioning ready.
- **Opportunity — Differentiation:** the competitor is weak where the user is strong, on a dimension customers care about. *Implication:* amplify it in positioning and sales enablement.
- **Opportunity — White space:** the competitor neglects a segment or use case the user serves well. *Implication:* lean into that underserved segment.
- **Parity:** both sides are equally strong. *Implication:* win on other dimensions instead, such as price, experience, trust, or ecosystem.

**Market movement.** Watch for signals that a competitor's strategic direction is shifting:

- **Hiring patterns** — what are they recruiting for? Look for particular domain expertise, engineers in unfamiliar areas, or sellers in new regions.
- **Partnership announcements** — channel partners, fresh integrations, platform plays.
- **Pricing changes** — cuts (a land-grab), increases (value extraction), new tiers (expanding into new segments).
- **Acquisition activity** — what capabilities are they acquiring?
- **Customer segment shifts** — are they moving up- or downmarket, or into neighboring segments?

### Phase 4 — Recommend a response

Write one recommendation for every active threat and every opportunity worth acting on. Weigh the four response options against when each one fits:

| Option | What to spell out | Pick it when |
|---|---|---|
| **Build** | What to build, rough scope, and the timeline implication | The gap sits in a must-win dimension and there is capacity to close it |
| **Partner** | A partnership that could close the gap | The gap is real but falls outside the user's core competency |
| **Reposition** | A messaging change that reframes the dimension | The competitor's edge matters less than they claim, or the evaluation criteria can be reframed |
| **Monitor** | Watch and reassess at the next review cycle | The threat is emerging but isn't yet affecting customers or pipeline |

```
RESPONSE RECOMMENDATION:
  Trigger:            [the competitive move that prompted this]
  Classification:     [Threat — Active / Threat — Emerging / Opportunity]
  Impact:             [which of our segments, metrics, or positioning is affected]
  Response options:
    1. [Build]      — [what to build + rough scope + timeline implication]
    2. [Partner]    — [partnership that could close the gap]
    3. [Reposition] — [messaging change that reframes the dimension]
    4. [Monitor]    — [watch and reassess at the next review cycle]
  Recommended option: [number + reasoning]
  Decision owner:     [who should approve this response]
  Urgency:            [Immediate / This quarter / Next planning cycle]
```

## The finished brief

Assemble the phases into this document:

```
# Competitor intelligence brief: [name of the competitor]
Date: [date]    |    Author: [name]    |    Classification: [Internal / Confidential]

## 1. Key takeaways
[2-3 sentences: who they are, what changed, and why it matters to us]

## 2. What we know, and from where
[sources consulted, how recent they are, known gaps]

## 3. Capabilities side by side
[the structured comparison from Phase 2]

## 4. How they position themselves
[value proposition, GTM, pricing, differentiation — from Phase 3]

## 5. Threats and openings for us
[the classified signals from Phase 3]

## 6. How we should respond
[action items with owners and urgency — from Phase 4]

## 7. Still to find out
[what we still need to find out, each with an assigned research task]

## 8. When to revisit
[when to revisit this brief — usually quarterly or after a major competitor move]
```

## Keeping briefs current

Tell the user which event should prompt which refresh:

- **A competitor launches a major feature** → update the affected rows of the feature matrix and reassess the threats.
- **Quarterly planning** → fully refresh the briefs on the top 2–3 competitors.
- **A deal is lost to a competitor** → run a post-mortem and update the threat assessment and response.
- **The user enters a new market segment** → build a new brief covering that segment's competitors.
- **A competitor raises funding or makes an acquisition** → update the market movement indicators and the strategic analysis.

## Ground rules

- **Never fill in a competitor's pricing, features, positioning, or market share from training data.** Every competitive claim must trace to the user, their uploaded documents or connected knowledge sources, or a web search, and must cite its source.
- **Never describe anything as "market standard" or "typical" for a competitive dimension.** Every assertion needs a source.
- **If the user supplies no competitor data,** hand back the empty brief template together with a list of the specific data you need. Don't fill the gaps with assumptions.
- **Label the origin of every assertion** with one of: `[From user/knowledge source]`, `[From web search — {date}]`, `[Analysis framework]`, or `[AI assessment — verify]`.
