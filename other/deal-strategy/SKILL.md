---
name: deal-strategy
description: "Fires when a user asks about deal strategy, how to approach a stalled deal, or needs a business case. Produces: Five-Lens Prism analysis (stakeholder psychology, political capital, competitive dynamics, hidden leverage, temporal dynamics), Three Paths recommendation (velocity/diagnostic/protective), 5-Component POV model. Output contract: three distinct strategic options with evidence grading, never a single recommendation."
user-invocable: false
---

# Deal Strategy — Strategic Frameworks Skill

## Purpose

Contains the three major strategic frameworks used by deal analysis commands: the Five-Lens Prism (used by deal strategy), the Three Paths Framework (used by deal strategy), and the 5-Component POV Model (used by the business case capability). Also includes the evidence grading reference for strategic analysis.

## When Referenced

- **Deal strategy analysis** (think-about-deal intent) — Five-Lens Prism analysis and Three Paths recommendation. Fires when a deal needs strategic direction or is stuck.
- **Building executive business cases** (build-case intent) — 5-Component POV Model for constructing evidence-graded points of view
- **Competitive displacement situations** (handle-competition intent) — Competitive Dynamics lens from Five-Lens Prism for assessing competitive positioning and win probability

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
- Run account research for deeper account intelligence
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
- Run competitive analysis if competitive threat is the issue
- Consider disqualification if Hell No signals are strong

### 5-Component POV Model

Used by the business case capability to build a Point of View document. A POV is NOT a pitch — it's a perspective on the prospect's business that demonstrates deep understanding.

**Before the 5 components fire, the system must complete a context reasoning pass.** The components tell you WHAT to write. The context reasoning tells you HOW TO THINK so you don't write the wrong thing.

#### Context Reasoning (MANDATORY — runs before any component)

This is not a questionnaire. This is internal reasoning the system performs using whatever context the AE provided — their words, the client's email, research data, call notes, deal history. The system reasons through each item and flags gaps only when they'd materially change the output.

**1. Relationship reality**
- What is the relationship between the AE and this person? (friend, warm contact, cold prospect, enterprise stakeholder)
- Is this a personal engagement or a company engagement? (determines "I" vs "we," tone, formality)
- What tone does the relationship demand? Match the client's communication style, not a default template.

**2. Client situation — IS vs BECOMING**
- Research tells you what the firm IS. The AE's context tells you what it's BECOMING.
- A $283M AUM firm with 6 staff might look established in SEC filings but be a fledgling team with an aspirational org chart. A 500-person company might be mid-reorg with half the team leaving.
- **Always ask yourself:** Is the research showing current reality or historical reality? Is the client's own description of their situation aspirational or operational?
- When research and AE context conflict, the AE's context wins. Flag the conflict but write to the reality, not the data.

**3. Language mapping**
- Before writing a single word, identify the language this client uses. Not your language. Not consulting language. THEIR language.
- Industry terms: "advisors" not "reps," "families" not "accounts," "custodian" not "platform"
- Formality level: match the client's email/communication style
- Jargon to avoid: if the buyer isn't technical, no "AI agent," "LLM," "RAG," "skills" (in the jargon sense), or any internal framework terminology
- **Test:** Would this person use this word in a conversation with a colleague? If not, don't use it.

**4. Framing — value, not fear**
- Every pain point, risk, or gap should be framed as an opportunity for value, not a threat.
- "Your team can trust what the system produces — and defend it in an exam" not "you're at risk of compliance violations."
- "Your new partner walks in and the system explains how the firm operates" not "you have a knowledge transfer problem."
- Compliance, risk, and operational gaps are real — but position the solution as positive capability, not disaster avoidance.

**5. Assumption check**
- What am I assuming about this firm's maturity? (Is the org chart real or aspirational?)
- What am I assuming about their urgency? (Are they ready to move or exploring?)
- What am I assuming about who's involved in the decision? (Solo buyer, partner, board?)
- What am I assuming about budget? (Has a number been discussed, or am I guessing?)
- If any assumption would change the POV's framing, tone, or specificity — flag it and write to the safer interpretation.

**6. ROI calibration**
- Default to modest, defensible numbers. Break-even framing over aggressive ROI claims.
- "7 hours/week recovered" is better than "$210K annual return" — the first is tangible, the second invites scrutiny.
- Do deep research to ground the numbers. Present them gently. Keep the receipts but don't show them unless asked.
- If the AE says anything about being nervous about numbers or wanting to de-risk claims, dial back further.

**7. Specificity pass**
- Every section must contain something specific to THIS client that couldn't be copy-pasted into another POV.
- The Executive Anchor references their specific situation, not a generic industry trend.
- The Blind Spot uses their data, their org structure, their competitive position.
- Quarterly milestones (if included) describe things the buyer can PICTURE — concrete scenarios using the client's own role language, not abstract jargon like "skills deployed across all divisions."
- **Test:** If you replaced the company name with a competitor's name and the POV still worked, it's not specific enough.

#### Component 1: Executive Anchor
*Open with THEIR situation, not yours. The first thing they read should make them feel understood.*

**Rules:**
- Address a business outcome, not a technology problem
- Reference their specific situation — their words, their chart, their email, their stated goals
- If they sent you something (an email, a chart, a doc), reference it directly: "You sent me a vision for seven divisions"
- Make them feel understood before you make any claims
- Do NOT open with who you are or what you do. Open with THEM.
- Evidence grade: Should reference Verified data about the company

#### Component 2: Blind Spot
*Something they probably know but haven't fully quantified or addressed.*

**Rules:**
- Not an insult — a genuine insight they'll recognize as true
- Should be specific enough that they think "how did they know that?"
- Often tied to industry trends, competitive shifts, or operational inefficiencies
- Frame as opportunity, not threat (Context Reasoning #4)
- Must use the client's language (Context Reasoning #3)
- Evidence grade: Can be Estimated based on industry patterns, but flag it

#### Component 3: Math of Pain
*Quantify the cost of inaction — modestly.*

**Rules:**
- Use their numbers when possible (from calls, public data)
- If using estimates, clearly tag them and show the math
- Three types of cost: direct financial, opportunity cost, risk cost
- Default to break-even framing: "recover X hours/week" over "save $Xk/year" (Context Reasoning #6)
- Do deep research to ground numbers (industry economics, benchmarks, comparable firms). Use the research to make claims defensible but present them gently.
- Must tag every number with evidence grade (Verified/Estimated/Hypothesis)
- This is where the 50% Rule matters most — if >50% is hypothesis-grade, flag the entire POV
- Position as "we'll build the model together" not "here's what you'll save"

#### Component 4: Mechanism
*How you solve it — but positioned as an approach, not a product demo.*

**Rules:**
- Lead with the approach/methodology, not the product
- Connect back to the Blind Spot — show how the mechanism addresses it
- Use Financial, Technical, or Strategic angle (Commandment 9) — not features
- Reference proof points from similar companies — but only where the prospect matches the vertical or challenge
- Describe outcomes in terms the buyer can picture (Context Reasoning #7)
- Evidence grade: Proof points should be Verified, projected outcomes Estimated

#### Component 5: Call to Action
*One specific, low-friction next step — ideally their own idea reflected back.*

**Rules:**
- Must be proportional to the stage of the relationship
- If the client already suggested a next step (workshop, call, meeting), use THAT — reflect their idea back, don't invent a new one
- Early stage: "15-minute call to explore if this resonates"
- Mid stage: "Working session to map out the impact for your specific situation"
- Late stage: "Executive briefing with your team to align on the business case"
- Never ask for more commitment than the evidence supports
- Pricing (if included): present with flexibility language. "Starting point, not a finished plan." If a range was discussed, anchor at the discussed number with room to adjust.

#### Quality Gate (runs after all 5 components are drafted)

Before presenting the POV, check:

1. **Language test:** Are there any words or phrases the buyer wouldn't use themselves? Replace every one.
2. **Specificity test:** Could this POV work for a different company if you swapped the name? If yes, it's not specific enough.
3. **Tone test:** Does this match the relationship? A POV for a friend should not read like a consulting proposal. A POV for a Fortune 100 should not read like a casual email.
4. **Assumption test:** Did Context Reasoning surface any conflicts between research and AE context? If so, did the POV write to the AE's reality, not the research's data?
5. **ROI test:** Are the numbers modest enough to be defensible? Would the AE feel comfortable if the client asked "where did this number come from?"
6. **Sendability test:** Would the AE actually put their name on this and send it? If it sounds like an AI wrote it, rewrite.

### Evidence Grading for Strategic Analysis

All strategic analysis must be evidence-graded:

| Source | Grade |
|--------|-------|
| Deal data from workspace (stage, MEDDPICC, value) | Verified |
| Customer quotes from call notes | Verified |
| Competitive positioning from battlecard + call history | Estimated |
| Industry trends and benchmarks | Estimated |
| Strategic projections (win probability, path outcomes) | Hypothesis |
| Future-state assumptions | Hypothesis |

**The 50% Rule:** If more than 50% of the strategic analysis is hypothesis-grade, flag it: "This strategy is heavy on assumptions. Consider running account research on [Company] to gather more verified intel before acting."

## Personalization Notes

- Strategic frameworks (Five-Lens Prism, Three Paths) are universal — framework structure is not personalized
- Proof points and case studies come from company-intel skill (Tier 3 — regenerated during deep personalization)
- Competitive analysis references battlecards skill (Tier 3 — regenerated during deep personalization)
- POV angle selection (Financial/Technical/Strategic) uses {{PRODUCT_DESCRIPTION}} context

### First-Use Calibration Storage (deal strategy)

On the first run of deal strategy, the user is asked whether they prefer aggressive or conservative deal strategy. The Three Paths framework is universal, but the **recommendation bias** is personalized:

- **Strategy posture:** [Populated on first deal strategy run — aggressive / balanced / conservative]
- **Posture notes:** [Any additional context, e.g., "I push hard when I see champion engagement" or "I prefer to slow down and gather more intel"]

This does not change the Three Paths framework itself — all three paths are always presented. It influences which path the RECOMMENDATION line suggests when signals are mixed.
