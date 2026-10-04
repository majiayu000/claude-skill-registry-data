---
name: deal-strategy
description: Strategic frameworks including the Five-Lens Prism, Three Paths, and 5-Component POV Model for deal analysis
tier: 1 (universal)
auto-fire: /strategy, /pov, /battle
user-invocable: false
---

# Deal Strategy — Strategic Frameworks Skill

## Purpose

Contains the three major strategic frameworks used by deal analysis commands: the Five-Lens Prism (used by /strategy), the Three Paths Framework (used by /strategy), and the 5-Component POV Model (used by /pov). Also includes the evidence grading reference for strategic analysis.

## When Referenced

- **/strategy** — Five-Lens Prism analysis and Three Paths recommendation
- **/pov** — 5-Component POV Model
- **/battle** — Competitive Dynamics lens from Five-Lens Prism

## Core Framework

### Five-Lens Prism

Analyze any deal through 5 distinct strategic lenses. Each lens reveals different aspects of the deal's health and opportunities.

#### Lens 1: Stakeholder Psychology
*Who supports us, who blocks us, who's undecided?*

**Analysis prompts:**
- Map every known stakeholder by role (Champion, Economic Buyer, Technical Buyer, Influencer, Blocker, User)
- Assess each stakeholder's sentiment (Champion, Supportive, Neutral, Skeptical, Blocker)
- Identify motivations: What does each stakeholder personally gain or lose from this decision?
- Map political dynamics: Who influences whom? Who's rising, who's falling?
- Identify the "silent stakeholder" — someone we haven't met who could influence the outcome

**Strength assessment:**
- **Strong:** Multiple supporters including the economic buyer. Blockers identified and neutralized.
- **Mixed:** Some supporters, but key stakeholders are neutral or unknown. Blockers present but not dominant.
- **Weak:** Few supporters. Key decision makers are skeptical or unknown. Blockers have significant influence.

#### Lens 2: Political Capital
*What are the internal dynamics at the prospect organization?*

**Analysis prompts:**
- Who has political capital to spend on this decision?
- Is our champion rising or falling politically?
- Any recent reorgs, leadership changes, or power shifts?
- Is there internal alignment or competing priorities?
- Who would be embarrassed if this project fails?

**Strength assessment:**
- **Strong:** Our champion has strong political capital. Organization is stable. Project has executive sponsorship.
- **Mixed:** Champion has moderate influence. Some organizational uncertainty. Competing priorities exist.
- **Weak:** Champion lacks political capital. Reorg underway. No clear executive sponsorship.

#### Lens 3: Competitive Dynamics
*Where do we stand vs. alternatives (including do-nothing)?*

**Analysis prompts:**
- Who's the primary competitor? What's their positioning?
- Does the competitor have existing relationships with key stakeholders?
- What's the incumbent advantage (if displacing)?
- What's our unique wedge — the thing only we can do?
- What would happen if they choose "do nothing"?

**Strength assessment:**
- **Strong:** Clear differentiation. No incumbent advantage. Our relationships are stronger.
- **Mixed:** Some differentiation. Competitor has partial relationships. Evaluation is genuinely competitive.
- **Weak:** Competitor has strong incumbent advantage. They're the safe choice. Our differentiation is unclear.

#### Lens 4: Hidden Leverage
*What untapped advantages haven't we used?*

**Analysis prompts:**
- Are there proof points, case studies, or references we haven't surfaced?
- Do we have adjacent relationships (other departments, sister companies, board connections)?
- Are there timing advantages we haven't exploited (contract renewals, budget cycles, events)?
- Can we change the evaluation criteria in our favor?
- Is there competitive intelligence we haven't applied?

**Strength assessment:**
- **Strong:** Multiple untapped advantages identified. Clear path to leverage them.
- **Mixed:** Some potential advantages, but uncertain impact.
- **Weak:** Few untapped advantages. We've played most of our cards.

#### Lens 5: Temporal Dynamics
*What time-based pressures and windows exist?*

**Analysis prompts:**
- When does their current contract expire?
- What's their budget cycle? When does money expire?
- Are there seasonal factors (Q4 urgency, fiscal year end, planning cycles)?
- Is there a triggering event creating urgency (regulation, competitor launch, leadership mandate)?
- What happens if they DON'T decide by [date]?

**Strength assessment:**
- **Strong:** Multiple urgency factors. Clear window of opportunity. Time pressure favors action.
- **Mixed:** Some time pressure, but no hard deadline. Customer could delay without consequence.
- **Weak:** No urgency. Customer has no timeline pressure. "Next quarter" energy.

### Three Paths Framework

After Five-Lens analysis, synthesize into three distinct paths forward. The AE always chooses — the system never prescribes.

#### Path 1: Velocity (Strike)
*When to recommend: Strong signals across 3+ lenses, champion engaged, window closing.*

**Characteristics:**
- Accelerate the deal. Push for concrete next steps.
- Propose a timeline. Create mutual action plan.
- Risk: Moving too fast before the deal is truly ready.

**Actions to recommend:**
- Schedule next meeting within [X] days
- Propose specific timeline to decision
- Send executive summary or business case
- Request champion to schedule EB meeting
- Set up technical validation or POC

#### Path 2: Diagnostic (Go Deep)
*When to recommend: Mixed signals, MEDDPICC gaps, need more intelligence before acting.*

**Characteristics:**
- Slow down to speed up. Don't accelerate into a wall.
- Run discovery. Fill MEDDPICC gaps.
- Invest in relationships before asking for commitments.
- Risk: Losing momentum or appearing indecisive.

**Actions to recommend:**
- Schedule discovery call focused on specific gaps
- Request meetings with additional stakeholders
- Run /research for deeper account intelligence
- Ask champion for honest deal assessment
- Map the complete decision process before proposing

#### Path 3: Protective (Pause)
*When to recommend: Red flags, stalled champion, competitive threat, political uncertainty.*

**Characteristics:**
- Protect the relationship. Don't burn bridges.
- Re-engage differently — new angle, new stakeholder, new timing.
- Consider whether this deal is winnable at all.
- Risk: Deal goes cold or competitor advances.

**Actions to recommend:**
- Shift to value-add mode (share insights without asking for anything)
- Identify new stakeholder entry points
- Wait for a triggering event to re-engage
- Run /battle if competitive threat is the issue
- Consider disqualification if Hell No signals are strong

### 5-Component POV Model

Used by /pov to build a Point of View document. A POV is NOT a pitch — it's a perspective on the prospect's business that demonstrates deep understanding.

#### Component 1: Executive Anchor
*A 2-sentence opening that speaks to what the executive cares about.*

**Rules:**
- Address a business outcome, not a technology problem
- Reference their specific situation (industry, size, competitive position)
- Make them feel understood before you make any claims
- Evidence grade: Should reference Verified data about the company

#### Component 2: Blind Spot
*Something they probably know but haven't fully quantified or addressed.*

**Rules:**
- Not an insult — a genuine insight they'll recognize as true
- Should be specific enough that they think "how did they know that?"
- Often tied to industry trends, competitive shifts, or operational inefficiencies
- Evidence grade: Can be Estimated based on industry patterns, but flag it

#### Component 3: Math of Pain
*Quantify the cost of inaction.*

**Rules:**
- Use their numbers when possible (from calls, public data)
- If using estimates, clearly tag them and show the math
- Three types of cost: direct financial, opportunity cost, risk cost
- Must tag every number with evidence grade (Verified/Estimated/Hypothesis)
- This is where the 50% Rule matters most — if >50% is hypothesis-grade, flag the entire POV

#### Component 4: Mechanism
*How you solve it — but positioned as an approach, not a product demo.*

**Rules:**
- Lead with the approach/methodology, not the product
- Connect back to the Blind Spot — show how the mechanism addresses it
- Use Financial, Technical, or Strategic angle (Commandment 9) — not features
- Reference proof points from similar companies
- Evidence grade: Proof points should be Verified, projected outcomes Estimated

#### Component 5: Call to Action
*One specific, low-friction next step.*

**Rules:**
- Must be proportional to the stage of the relationship
- Early stage: "15-minute call to explore if this resonates"
- Mid stage: "Working session to map out the impact for your specific situation"
- Late stage: "Executive briefing with your team to align on the business case"
- Never ask for more commitment than the evidence supports

### Evidence Grading for Strategic Analysis

All strategic analysis must be evidence-graded:

| Source | Grade |
|--------|-------|
| Deal data from Notion (stage, MEDDPICC, value) | Verified |
| Customer quotes from call notes | Verified |
| Competitive positioning from battlecard + call history | Estimated |
| Industry trends and benchmarks | Estimated |
| Strategic projections (win probability, path outcomes) | Hypothesis |
| Future-state assumptions | Hypothesis |

**The 50% Rule:** If more than 50% of the strategic analysis is hypothesis-grade, flag it: "This strategy is heavy on assumptions. Consider running `/research [Company]` to gather more verified intel before acting."

## Personalization Notes

- Strategic frameworks (Five-Lens Prism, Three Paths) are universal — framework structure is not personalized
- Proof points and case studies come from company-intel skill (Tier 3 — regenerated during /setup)
- Competitive analysis references battlecards skill (Tier 3 — regenerated during /setup)
- POV angle selection (Financial/Technical/Strategic) uses {{PRODUCT_DESCRIPTION}} context

### First-Use Calibration Storage (/strategy)

On the first run of `/strategy`, the user is asked whether they prefer aggressive or conservative deal strategy. The Three Paths framework is universal, but the **recommendation bias** is personalized:

- **Strategy posture:** [Populated on first /strategy run — aggressive / balanced / conservative]
- **Posture notes:** [Any additional context, e.g., "I push hard when I see champion engagement" or "I prefer to slow down and gather more intel"]

This does not change the Three Paths framework itself — all three paths are always presented. It influences which path the RECOMMENDATION line suggests when signals are mixed.
