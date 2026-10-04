---
name: battlecards
description: "Fires when a competitor is mentioned, a competitive situation arises, or the user asks how to beat/displace/win against a specific vendor. Produces: per-competitor displacement playbook with strengths, weaknesses, talk tracks, proof points, trap questions, and landmine responses. Triggers on: handle-competition, think-about-deal (competitive lens), battle analysis."
user-invocable: false
---

# Battlecards — Competitive Displacement Playbooks Skill

> **Tier 3 — This entire file is regenerated during deep personalization Phase 3 (Competitive Landscape) with per-competitor displacement playbooks.**

## Purpose

Contains detailed competitive battlecards for each of the AE's top competitors. Each battlecard includes: competitor overview, strengths, weaknesses, displacement strategy, talk tracks, proof points, trap questions, and landmine responses. This is the ammunition for competitive selling situations.

## When Referenced

- **Competitive displacement situations** (handle-competition intent) — loads the relevant battlecard and applies it to a specific deal with talk tracks and proof points
- **Deal strategy analysis** (think-about-deal intent) — Competitive Dynamics lens of the Five-Lens Prism references competitor positioning and win probability
- **Meeting preparation with known competitor** (prepare-meeting intent) — includes competitive context, trap questions, and landmine responses when a deal has a known competitor
- **Competitive displacement presentations** (create-deck intent) — Competitive Displacement template uses battlecard content for slides

## Core Framework

### Battlecard Structure

Each competitor gets a full battlecard with 8 sections. During deep personalization Phase 3, SalesSidekick researches each competitor via web search and builds these playbooks.

---

### Competitor 1: {{TOP_COMPETITOR_1}}

#### Overview
- **Company:** {{TOP_COMPETITOR_1}}
- **Website:** [Populated during deep personalization]
- **Founded:** [Populated during deep personalization]
- **Size:** [Populated during deep personalization]
- **Market position:** [Leader/Challenger/Niche — populated during deep personalization]
- **Primary pitch:** [What they lead with — populated during deep personalization]

#### Strengths (Where They Win)
*Populated during deep personalization via web research — what they're genuinely good at.*

1. [Strength 1 — specific and honest. Don't dismiss real advantages.]
2. [Strength 2]
3. [Strength 3]

**When they're strongest:** [Specific scenarios where they have a genuine advantage]

#### Weaknesses (Where They Lose)
*Populated during deep personalization via web research — genuine gaps, not FUD.*

1. [Weakness 1 — specific and verifiable]
2. [Weakness 2]
3. [Weakness 3]

**When they struggle:** [Specific scenarios where they consistently fall short]

#### Displacement Strategy
*How to win when they're the incumbent or primary competitor.*

- **Wedge play:** [The specific angle that opens the conversation — Financial, Technical, or Strategic]
- **Reframe the evaluation:** [How to shift decision criteria in our favor]
- **Key differentiator to lead with:** [The one thing they can't match]
- **Proof point:** [Specific customer who switched from them to us — if available]

#### Talk Tracks
*Specific things to say in competitive conversations.*

1. **When prospect mentions their strength:**
   > "[Acknowledging response that reframes to our advantage]"

2. **When prospect is comparing features:**
   > "[Response that shifts from features to outcomes — Commandment 9]"

3. **When prospect says they're "good enough":**
   > "[Response that quantifies the gap between 'good enough' and optimal]"

#### Proof Points
- [Verified] [Specific case study or metric that favors us]
- [Verified] [Published comparison or analyst report]
- [Estimated] [Calculated advantage based on available data]

#### Trap Questions (Ask These)
*Questions that expose their weaknesses without being aggressive.*

1. "[Question about an area where they're known to be weak]"
2. "[Question about scalability, integration, or support — our advantage areas]"
3. "[Question that makes the prospect realize they need what we offer]"

#### Landmine Responses
*When they've set traps — how to respond.*

| They Say | You Respond |
|----------|-------------|
| "[Common competitor claim #1]" | "[Evidence-based counter]" |
| "[Common competitor claim #2]" | "[Evidence-based counter]" |
| "[Common competitor claim #3]" | "[Evidence-based counter]" |

---

### Competitor 2: {{TOP_COMPETITOR_2}}

*Same 8-section structure. Populated during deep personalization Phase 3.*

#### Overview
[Populated during deep personalization]

#### Strengths
[Populated during deep personalization]

#### Weaknesses
[Populated during deep personalization]

#### Displacement Strategy
[Populated during deep personalization]

#### Talk Tracks
[Populated during deep personalization]

#### Proof Points
[Populated during deep personalization]

#### Trap Questions
[Populated during deep personalization]

#### Landmine Responses
[Populated during deep personalization]

---

### Competitor 3: {{TOP_COMPETITOR_3}}

*Same 8-section structure. Populated during deep personalization Phase 3.*

#### Overview
[Populated during deep personalization]

#### Strengths
[Populated during deep personalization]

#### Weaknesses
[Populated during deep personalization]

#### Displacement Strategy
[Populated during deep personalization]

#### Talk Tracks
[Populated during deep personalization]

#### Proof Points
[Populated during deep personalization]

#### Trap Questions
[Populated during deep personalization]

#### Landmine Responses
[Populated during deep personalization]

---

### General Competitive Rules

1. **Never fabricate competitive intelligence.** If we don't know something about a competitor, say so. Commandment 8 (Laws of Karma).
2. **Never bash competitors directly.** Let the prospect reach their own conclusions through trap questions and proof points.
3. **Lead with our value, not their flaws.** Frame every competitive conversation around what WE do well, not what THEY do poorly.
4. **Evidence-grade competitive claims:**
   - Competitor features from public sources (website, docs) → Verified
   - Competitive positioning based on call mentions or analyst reports → Estimated
   - Win probability and displacement predictions → Hypothesis
5. **Update battlecards** when new competitive intelligence emerges from calls (call processing captures this in Output 6).

### Win Probability Framework

When assessing competitive win probability:

| Signal | Impact on Win Probability |
|--------|--------------------------|
| Champion actively advocating for us | +0.2 |
| Champion aligned with competitor | -0.2 |
| Economic buyer met and positive | +0.15 |
| Incumbent advantage (they're already in) | -0.15 |
| We've redefined the evaluation criteria | +0.15 |
| They're ahead in the evaluation timeline | -0.1 |
| Customer has switched from them before | +0.1 |
| Decision criteria favor our strengths | +0.1 |

**Starting base:** 0.5 (coin flip). Adjust up/down based on signals.

## Personalization Notes

- **This entire file is Tier 3** — fully regenerated during deep personalization Phase 3 (Competitive Landscape)
- Deep personalization researches each competitor via web search and builds detailed battlecards
- Competitor names come from {{TOP_COMPETITOR_1}}, {{TOP_COMPETITOR_2}}, {{TOP_COMPETITOR_3}} (Tier 2 variables)
- Battlecards are updated when call processing captures new competitive intelligence
- Talk tracks and landmine responses are crafted based on public competitive positioning
- Win probability framework is universal — no personalization needed
