---
name: company-intel
description: "Fires on meeting prep, outreach, research, deck creation, and business case building. Provides: company overview, product portfolio, market position, differentiators, pricing context, case studies by vertical, key selling metrics, voice & language patterns, pain signal mapping, and prism insights. Output contract: company-specific context that makes outputs relevant to the prospect's actual situation. When a Platform Document exists (from /research), loads enriched voice, pain, and strategic intelligence."
user-invocable: false
---

# Company Intel — Product & Competitive Positioning Skill

> **Tier 3 — This entire file is regenerated during deep personalization Phase 2 (Company Intel) via web research on {{COMPANY}}.**

## Purpose

Contains the AE's company overview, product portfolio, competitive positioning, pricing context, case studies by vertical, and key metrics. This is the company knowledge base that informs all outbound communication, deal strategy, and presentation content.

## When Referenced

- **Meeting preparation** (prepare-meeting intent) — provides product context, proof points, and positioning for pre-meeting intelligence briefs
- **Deal strategy analysis** (think-about-deal intent) — informs competitive dynamics lens and hidden leverage analysis
- **Prospecting outreach** (write-email intent, new relationship) — provides proof points and positioning for cold and warm outreach emails
- **Company research** (research-company intent) — compares prospect's situation against our capabilities and market positioning
- **Presentation creation** (create-deck intent) — populates proof points, case studies, and positioning slides across all deck templates
- **Executive business cases** (build-case intent) — informs Math of Pain and Mechanism components of POV documents

## Core Framework

### Company Overview

**Company:** {{COMPANY}}
**Website:** {{COMPANY_URL}}
**Industry:** [Populated during deep personalization via web research]
**Founded:** [Populated during deep personalization]
**HQ:** [Populated during deep personalization]
**Size:** [Populated during deep personalization — employees, revenue if public]

**Mission/positioning:** [1-2 sentences from company website — populated during deep personalization]

### Product Portfolio

**Primary Product:** {{PRIMARY_PRODUCT}}
**Additional Products:** {{SECONDARY_PRODUCTS}}
**Description:** {{PRODUCT_DESCRIPTION}}

**Product overview** (populated during deep personalization):
- What it does: [Core capabilities]
- Who it's for: [Target personas]
- Key differentiators: [What makes it unique]
- Integration ecosystem: [Key integrations]

### Competitive Positioning

**Top Competitors:**
1. {{TOP_COMPETITOR_1}}
2. {{TOP_COMPETITOR_2}}
3. {{TOP_COMPETITOR_3}}

**Our positioning vs. each competitor** (populated during deep personalization via web research):

*Competitor 1: {{TOP_COMPETITOR_1}}*
- Their strength: [What they're known for]
- Our advantage: [Where we win]
- Key differentiator: [The thing only we do]

*Competitor 2: {{TOP_COMPETITOR_2}}*
- Their strength: [What they're known for]
- Our advantage: [Where we win]
- Key differentiator: [The thing only we do]

*Competitor 3: {{TOP_COMPETITOR_3}}*
- Their strength: [What they're known for]
- Our advantage: [Where we win]
- Key differentiator: [The thing only we do]

### Pricing Context

*Not detailed pricing — just enough context for strategic conversations.*

- **Pricing model:** [Subscription/Usage/License/Hybrid — populated during deep personalization]
- **Typical deal range:** {{AVERAGE_DEAL_SIZE}}
- **Pricing relative to market:** [Premium/Mid-market/Value — populated during deep personalization]
- **Key pricing conversations:** [Common objections and responses — populated during deep personalization]

### Case Studies by Vertical

*Populated during deep personalization via web research on {{COMPANY}}'s published case studies.*

**Format per case study:**

| Field | Content |
|-------|---------|
| **Customer** | [Company name or anonymized description] |
| **Vertical** | [Industry] |
| **Size** | [Enterprise/Mid-Market/SMB] |
| **Challenge** | [What they were facing] |
| **Solution** | [How they used our product] |
| **Results** | [Quantified outcomes — evidence-graded] |
| **Quote** | [Customer quote if available] |

*Default (before deep personalization):* No case studies available. Run deep personalization Phase 2 to populate from {{COMPANY}}'s published materials.

**Usage rules:**
- Only reference case studies when the prospect matches the vertical or challenge
- Always evidence-grade: published case studies = Verified, projected comparisons = Estimated
- Never fabricate case studies — if nothing matches, say "We don't have a direct case study for this situation, but here's a relevant parallel..."

### Key Metrics

*Company-level metrics for use in proposals, POVs, and presentations.*

- **Customers served:** [Number — populated during deep personalization]
- **Key industries:** [Verticals — populated during deep personalization]
- **Notable logos:** [Reference customers — populated during deep personalization]
- **Growth metrics:** [If public — populated during deep personalization]
- **Awards/recognition:** [If relevant — populated during deep personalization]

**Evidence grading for metrics:**
- Published on company website or press releases → Verified
- Calculated from available data → Estimated
- Projected or assumed → Hypothesis

### Voice & Language

*Populated by /research (Stage 2, Lens 2) or during deep personalization. Captures how the PROSPECT's target companies talk — not the AE's company voice (that's in brand-voice skill).*

**Purpose:** When the AE reaches out to or communicates with a prospect, mirroring the prospect's language builds instant credibility. This section stores language patterns extracted during account research.

**Per-company voice data** (stored in each company's Platform Document at `data/research/{company-slug}-platform.md`):

| Field | Content |
|-------|---------|
| **Key phrases** | Recurring language from their website, press, job postings |
| **Executive quotes** | Direct quotes from leadership — what they emphasize |
| **Terminology** | Industry-specific or company-specific jargon they use |
| **Tone** | Formal/casual, technical/business, aspirational/operational |
| **What they emphasize** | Themes they repeat across communications |
| **What they avoid** | Topics or language conspicuously absent |

**Usage rules:**
- Mirror prospect language in outreach, emails, and presentations
- Use their terminology, not generic industry terms
- Match their tone level — if they're formal, be formal; if they're conversational, be conversational
- Evidence grade: direct quotes from materials = Verified; tone assessments = Estimated

**Before research:** No voice data available. Use default professional tone from brand-voice skill.

### Pain Signal Mapping

*Populated by /research (Stage 2, Lens 3). Maps discovered pain points to the AE's product/solution.*

**Purpose:** Raw research finds company information. Pain signal mapping translates that information into selling intelligence by connecting what the prospect is dealing with to what the AE can solve.

**Pain signal structure:**

| Field | Content |
|-------|---------|
| **Signal** | The pain point or challenge identified |
| **Evidence** | Where this was found (job posting, news article, earnings call, etc.) |
| **Type** | Stated (they said it), Implied (inferred from signals), Projected (industry pattern) |
| **Severity** | High / Medium / Low |
| **Personas affected** | Which roles feel this pain most |
| **Product mapping** | How {{PRIMARY_PRODUCT}} or {{SECONDARY_PRODUCTS}} addresses this |
| **Evidence grade** | Verified / Estimated / Hypothesis |

**Usage rules:**
- Stated pain (from their own words) is always stronger than implied or projected
- Never fabricate pain signals — if research finds nothing, say so
- Pain signals feed into: outreach angles, POV documents, meeting prep talking points, deal strategy
- Update pain signals after every call that reveals new information

**Before research:** No pain signals mapped. Generic ICP-level pain patterns from {{ICP_USE_CASE}} used as starting point.

### Prism Insights

*Populated by /research (Stage 3). Five perspectives that surface non-obvious intelligence.*

**Purpose:** Every vendor researching a prospect finds the same public information. The Prism adds a reasoning layer that produces differentiated insights — the kind that make a prospect say "nobody else has mentioned that."

**Five perspectives:**

| Perspective | What it reveals |
|-------------|----------------|
| **Stakeholder View** | What keeps the key contact up at night. What they're measured on. Internal politics. |
| **Contrarian View** | The angle nobody else is taking. The counterintuitive insight. |
| **Operator View** | Monday morning reality for the people doing the work. Gap between exec messaging and operations. |
| **Growth Pressure View** | What breaks first at 2x scale. Scaling bottlenecks not yet visible. |
| **Hidden Connection** | The thread connecting unrelated data points into a story. The "aha" moment. |

**Usage rules:**
- Prism insights are Estimated grade at best (they're analytical, not factual)
- Not every perspective will produce a useful insight for every company — skip empty perspectives
- The Hidden Connection is the highest-value insight but also the hardest to find — don't force it
- Prism insights feed into: outreach (differentiated angles), meeting prep (talking points), deal strategy (hidden leverage lens)

**Before research:** No prism insights available. Generated only when /research runs Stage 3.

### Pitch Angle Templates

Three angles for positioning (Commandment 9: Don't Pitch Features, Pitch Angles):

**Financial Angle:**
> "[Prospect] is spending $[X] on [current approach]. Based on what we've seen with [similar company], switching to {{PRIMARY_PRODUCT}} could [reduce/save/generate] [Y] within [timeframe]."

**Technical Angle:**
> "[Prospect]'s current stack includes [known tools]. {{PRIMARY_PRODUCT}} integrates with [relevant integrations] to [solve technical gap]. Companies like [reference] saw [technical outcome]."

**Strategic Angle:**
> "[Prospect] is facing [market pressure/competitive threat/growth challenge]. Organizations in [their industry] are moving toward [trend]. {{PRIMARY_PRODUCT}} positions them to [strategic advantage]."

## Personalization Notes

- **This entire file is Tier 3** — fully regenerated during deep personalization Phase 2 (Company Intel)
- Deep personalization uses web search to research {{COMPANY}} and populate all sections
- Case studies are sourced from the company's public materials during deep personalization
- Competitive positioning is cross-referenced with battlecards skill
- Pitch angle templates use Tier 2 variables ({{PRIMARY_PRODUCT}}, {{PRODUCT_DESCRIPTION}})
- This file is the most frequently updated Tier 3 skill — refreshed whenever significant company changes occur
