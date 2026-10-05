---
name: competitive-battlecard
description: 'On-demand sales battlecards for live competitive deals - positioning matrix, top objections with responses, trap questions, proof points, and a "do not say" list. Use when: competitor surfaced in deal, sales battlecard, competitive enablement, deal-specific battlecard, objection handling, competitive trap questions, why we win against, why we lose to, displacement playbook.'
---

# Competitive Battlecard

Generate a deal-specific competitive battlecard in minutes when a competitor surfaces in an active opportunity. Sales reps get a focused, defensible playbook - not a 30-page positioning deck - that maps directly to the deal context (industry, company size, current stack) so they can respond confidently in the next call.

This skill assumes you already have a working understanding of the competitor (or have run **win-loss-analysis** / **competitive-positioning**). It is the *delivery layer* - turning prior intelligence into something a rep can act on between meetings. **No external sources are queried; the skill produces the battlecard from the inputs you provide.**

## Core Principle

**A battlecard is a constraint, not just a cheat sheet.** Its job is to keep reps on the messages that win and off the messages that lose - especially the ones that *feel* compelling in the moment but historically tank deals. Half the value is the "do not say" list.

---

## What You'll Get

| Section | Description |
|---------|-------------|
| **Positioning Matrix** | Side-by-side comparison on the 4-6 dimensions the buyer actually weighs |
| **Top 3 Objections + Responses** | The objections this competitor's reps are trained to plant, with battle-tested responses |
| **Trap Questions** | 3-5 questions the rep can ask the buyer that are easy for *us* to answer and hard for *them* - surfaces our strengths without naming the competitor |
| **Proof Points** | Customer outcomes, case study one-liners, and metrics, mapped to the deal's industry/size when possible |
| **"Do Not Say" List** | The 3-5 talking points that feel right but lose deals - with the reason each one backfires |
| **Discovery Re-Open** | Suggested questions to re-open discovery if the rep has been pulled into a feature comparison too early |
| **Next-Step Recommendation** | The specific next action that historically advances deals against this competitor (POC structure, exec alignment, security-led demo, etc.) |

---

## Output

Save to `outputs/battlecard-[competitor]-[deal-id]-[YYYY-MM-DD].md`

Battlecards are *deal-specific by design.* The same competitor in a different industry / company size / stack context produces a different card.

---

## Process

### Step 1: Intake
I'll ask:
> "Which competitor has surfaced? What's the deal context - industry, company size, current stack, deal stage, the buying committee roles you've met, and what the competitor has reportedly told the buyer? What internal intel do you have on this competitor (positioning, prior win-loss data, recent product launches)?"

### Step 2: Positioning Matrix
Map the 4-6 dimensions this buyer actually cares about (drawn from the deal context - not a generic feature grid). Score each side as **Win / Tie / Lose / Mixed**, with a one-line rationale per cell. Reps don't read three-paragraph cells.

### Step 3: Predict the Competitor's 3 Objections
For this competitor in this deal context, what will their rep most likely plant in the buyer's mind? Phrase each as the buyer is likely to repeat it back ("I heard your platform doesn't handle X"), then write the response.

Each response follows the **3-line structure**:
1. **Acknowledge** the partial truth (don't deny what's verifiably true)
2. **Reframe** to a dimension we win on
3. **Proof** - a specific customer outcome or capability the buyer can verify

### Step 4: Generate Trap Questions
Trap questions are buyer-facing and *competitor-neutral*. They surface a real pain that we solve well and the competitor handles poorly - without naming the competitor (which always backfires). Each trap question includes:
- The question itself
- Why it surfaces our advantage
- The likely buyer answer that opens the door

### Step 5: Pull Proof Points
Match customer stories / metrics / quotes to this deal's industry and company size. Prefer:
- Same industry, same size band → highest weight
- Same industry OR same size band → medium weight
- Logo-recognition only → lowest weight, used sparingly

For each proof point, include the specific metric (not "improved efficiency" - *"reduced ramp time from 14 to 4 days"*).

### Step 6: Build the "Do Not Say" List
The hardest and most valuable section. Identify 3-5 talking points that:
- Reps reach for instinctively against this competitor
- Have historically correlated with losses (from win-loss data) OR
- Pattern-match to known buyer triggers (e.g., trash-talking the competitor, over-claiming, attacking on price)

Each item explains *why* it backfires so reps internalize the reason, not just the rule.

### Step 7: Re-Open Discovery (if needed)
If the deal has slid into a feature comparison too early, suggest 3 discovery questions that pull the conversation back to business outcomes. This often resets the playing field more than any battlecard answer.

### Step 8: Next Step
One specific recommendation tied to deal stage:
- **Discovery / qualification** → which exec to bring in, what document to send
- **Demo / POC** → the specific demo flow that beats this competitor, success criteria for the POC
- **Pricing / negotiation** → which lever to pull (term length, scope, success-based pricing) and which to *not* pull

---

## Demo Battlecard Snippet (illustrative)

**Competitor:** "Acme Platform" · **Deal:** Mid-market FinServ, 800 FTEs, currently on legacy stack · **Stage:** Demo scheduled

**Positioning Matrix (excerpt):**

| Dimension | Us | Acme | Notes |
|-----------|----|----|-------|
| Time to first value | Win (avg 11 days) | Lose (avg 6+ weeks) | Acme requires PS engagement; ours is self-serve |
| Compliance posture | Win (SOC2 II, ISO 27001) | Tie (SOC2 II) | Don't over-claim; Acme matches on the basics |
| Native integrations | Tie | Tie | Both have the top 10 the buyer mentioned |
| Pricing transparency | Win (public tiers) | Lose (custom-quote only) | Strong wedge with finance buyer |

**Top Objection #1 - "Acme has more enterprise logos."**
1. Acknowledge: "Acme has been in market longer in the enterprise tier - that's true."
2. Reframe: "What we hear from buyers who switched is that mid-market and upper-mid was where Acme's deployment model started slowing them down - multi-month PS engagements vs. self-serve in days."
3. Proof: "[Customer X], 1,200 FTEs in your industry, ran POC in 9 days and was in production in 5 weeks."

**Trap Question:** *"How much PS budget did you set aside for implementation, and what's the trigger that releases it?"*
→ Surfaces Acme's implementation cost without naming Acme. If buyer hasn't budgeted PS, that's a problem they didn't know they had.

**Do Not Say:**
- ❌ *"Acme is bloated / legacy / overpriced."* → Buyer may have peers using Acme; trash-talking lowers trust in *us*, not Acme.
- ❌ *"We have feature X and they don't."* → Acme will ship it next quarter; battle on outcomes, not feature lists.
- ❌ *"Our pricing is 30% cheaper."* → Triggers a price negotiation we don't need; lead with time-to-value and let pricing surface in procurement.

**Next Step:** Schedule technical-deep-dive with the buyer's data team in week 1. Acme historically loses on data-engineering self-serve; structure the demo around their stated data quality use case.

---

## Tips
1. **Refresh quarterly minimum.** Competitor positioning shifts; a 6-month-old battlecard often advises responses the competitor has since fixed.
2. **The "do not say" list is where most of the value lives.** Reps already know what to say; they need help with what to *stop* saying.
3. **Trap questions never name the competitor.** Naming them validates the comparison and concedes ground.
4. **One battlecard per (competitor × industry × size).** Generic battlecards lose to specific ones every time.
5. **Pair with win-loss-analysis.** The "do not say" list should be data-driven from actual loss reasons, not folklore.

---

## Pairs With

- **win-loss-analysis** - supplies the empirical loss reasons that populate "Do Not Say"
- **competitive-positioning** - supplies the strategic positioning that frames the matrix
- **competitive-exec-brief** - battlecard for executive-level conversations rather than rep-level deals
