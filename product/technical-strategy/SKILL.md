---
name: technical-strategy
description: Write, communicate, and maintain a technical strategy that connects engineering direction to business outcomes. Covers the diagnosis → guiding policies → coherent actions framework, strategy vs. roadmap vs. vision distinctions, writing a strategy doc, communicating to non-engineers, review cadence, and common failure modes.
triggers:
  - "write a tech strategy"
  - "technical strategy"
  - "tech direction"
  - "engineering strategy"
  - "what should we focus on technically"
  - "technology vision"
  - "where should engineering invest"
  - "build our tech roadmap"
audience:
  - manager
---

# Technical Strategy

A technical strategy answers the question: **given where we are and where the business is going, what must engineering do — and not do — to get there?**

It is not a roadmap (which is a delivery plan). It is not a vision (which is an aspirational destination). A strategy is the *reasoning* that connects the two — explaining why certain bets make sense given the current constraints and business context.

> For quarterly goal-setting that flows from strategy, use the `okr-engineering-alignment` skill.  
> For communicating roadmap priorities to stakeholders, use the `roadmap-prioritization` skill.

---

## Strategy vs. Roadmap vs. Vision

| Artifact | Question it answers | Time horizon | Updated |
|---|---|---|---|
| **Vision** | Where do we want to be? | 3–5 years | Rarely |
| **Strategy** | Why these bets, given our situation? | 1–2 years | Annually + major pivots |
| **Roadmap** | What will we build, in what order? | 6–12 months | Quarterly |
| **OKRs** | What outcomes will we drive this quarter? | Quarter | Quarterly |

Without a strategy, roadmaps become wishlists. Every team fights for priority using local logic. The strategy provides the shared filter.

---

## The Strategy Framework: Diagnosis → Guiding Policies → Coherent Actions

Based on Richard Rumelt's *Good Strategy/Bad Strategy* and applied to engineering by Will Larson and Anna Shipman:

### 1. Diagnosis
A clear-eyed statement of the situation — what's true about where the business and engineering are today. This is the hardest part to write honestly.

Include:
- **Business context**: What stage is the company? What are the critical business bets for the next 2 years?
- **Engineering health**: What are the biggest structural constraints? (e.g., monolith slowing delivery, no observability, toil consuming 40% of eng time)
- **Competitive/market context**: What technical capabilities does the market require in 18 months that we don't have?
- **Team context**: Headcount trajectory, skill gaps, current team topology

> A weak strategy skips the diagnosis. If your strategy could apply to any company, it has no diagnosis.

### 2. Guiding Policies
The 3–5 principles that will govern every significant technical decision for the next year. Not values ("we care about quality") — actual constraints and choices.

Examples of good guiding policies:
- "We will not add new services until we can deploy them in < 10 minutes with zero manual steps."
- "Reliability for the payments flow takes priority over feature velocity for all teams."
- "We invest in platform capabilities that unblock ≥ 3 product teams simultaneously before capabilities that unblock 1."

Bad guiding policies:
- "We will build for scale." (No constraint, no choice, no trade-off)
- "We value developer experience." (A value, not a policy)

### 3. Coherent Actions
The specific initiatives that express the guiding policies. Actions are coherent when they reinforce each other — not a random collection of good ideas.

For each initiative, document:
- What it is and why it fits the guiding policy
- What it unlocks downstream
- What it explicitly deprioritizes

---

## Writing the Strategy Document

### Structure

```markdown
# [Company/Team] Technical Strategy — [Year]

## Situation
[2–3 paragraphs describing the business context, where engineering is today,
and the critical challenge this strategy addresses. Be specific. Use data.]

## Diagnosis
The core tension or constraint we must resolve:
"[Engineering capability X] is the binding constraint on [business outcome Y]."

## Guiding Policies
1. [Policy 1]: [One-sentence rationale]
2. [Policy 2]: [One-sentence rationale]
3. [Policy 3]: [One-sentence rationale]
(3–5 policies maximum — more dilutes focus)

## Key Initiatives
For each initiative:
### Initiative: [Name]
- **What**: [Specific, concrete description]
- **Why now**: [Why this — why not later or never?]
- **Guiding policy it expresses**: [Links back to section above]
- **Unlocks**: [What becomes possible because of this?]
- **Cost**: [Rough order of magnitude — team-quarters or headcount]

## What We Won't Do
[Explicitly list things that are plausible but deprioritized, and why.
This is as important as the initiatives list — it demonstrates real trade-offs.]

## Success Metrics
| Metric | Baseline (today) | Target (12 months) |
|---|---|---|
| [Deploy frequency] | [X/week] | [Y/week] |
| [MTTR] | [X hours] | [Y minutes] |
| [Custom metric] | ... | ... |

## Review Cadence
Next formal review: [Date]
Trigger for out-of-cycle review: [Major pivot, acquisition, leadership change, etc.]
```

---

## Communicating Tech Strategy to Non-Engineers

Non-engineers don't need the technical details — they need to understand:
1. What constraint this addresses (framed as a business risk, not a technical problem)
2. What it enables (framed as business capability, not technical capability)
3. What it costs (time, money, opportunity cost)
4. How you'll know it worked (business metric, not engineering metric)

### Strategy Communication One-Pager Template

```markdown
## Engineering Direction — [Year] (Executive Summary)

**The challenge we're solving:**
[1–2 sentences. Business framing. E.g., "As we move into enterprise markets,
our current deployment process requires 2 days of manual coordination,
which blocks us from shipping security patches on the customer SLA we've committed to."]

**Our approach:**
[2–3 sentences. What you're doing and the logic behind it.
E.g., "We are investing the first half of the year in automated deployment
infrastructure so that all product teams can ship independently.
This is a prerequisite for the multi-region expansion on the business roadmap."]

**What this enables:**
- [Business capability 1, e.g., "Ship hotfixes in < 1 hour for enterprise customers"]
- [Business capability 2]
- [Business capability 3]

**What we're trading off:**
[Be explicit. E.g., "New feature development on [product area] will be slower
in Q1–Q2 while platform work is in progress."]

**Investment:**
[X engineers for Y quarters. Framed as an investment, not a cost.]

**How we'll know it worked:**
[1–2 business-legible metrics with targets and dates.]
```

---

## Aligning Tech Strategy to Business Goals

Work through these questions before writing:

1. **What are the company's top 2–3 bets for the next 12–18 months?**
   - Talk to your CEO, CPO, CFO. Read the board deck if you have access.
   - Every guiding policy should connect to at least one of these bets.

2. **What would make those bets fail?**
   - Technical debt that makes iteration too slow?
   - Reliability that erodes customer trust?
   - Missing capabilities that block the product?

3. **What technical capabilities does the business need that we don't have yet?**
   - Map these to the timeline of business bets.
   - A capability needed in 9 months needs work to start now.

4. **What does the engineering team need to be healthy enough to execute?**
   - Toil reduction, hiring, tooling, skills gaps.
   - Without this, strategy is aspirational fiction.

---

## Common Pitfalls

| Pitfall | What it looks like | Fix |
|---|---|---|
| **Too abstract** | Strategy could apply to any company | Add specific diagnosis grounded in your actual constraints |
| **Roadmap in disguise** | List of projects with no unifying logic | Identify the 3 principles that choose between projects |
| **No trade-offs** | Strategy tries to do everything | Explicitly write "What We Won't Do" |
| **Not updated** | Strategy written once, then ignored | Quarterly check-in; full refresh annually or at major inflection |
| **Executive-only** | Engineers don't know the strategy exists | Share with full team; connect every significant decision back to it |
| **Output-focused metrics** | "Ship 3 platform services" as a success metric | Use outcome metrics: deploy frequency, MTTR, team NPS |
| **No diagnosis** | Jumps straight to solutions | Force yourself to write the situation section first |

---

## Strategy Review Checklist

Run this before publishing and at each review cycle:

**Clarity**
- [ ] Can an engineer who didn't write this explain why we're doing Initiative X?
- [ ] Does the diagnosis name a specific constraint, not a vague challenge?
- [ ] Are the guiding policies actual choices that eliminate some options?

**Coherence**
- [ ] Do the initiatives reinforce each other or pull in different directions?
- [ ] Does "What We Won't Do" contain real things you're actively choosing not to do?
- [ ] Could you reject a plausible project using the guiding policies?

**Connection to business**
- [ ] Is every initiative traceable to a business bet or risk?
- [ ] Are the success metrics legible to a non-engineer?
- [ ] Has a senior non-engineering stakeholder read and agreed with the framing?

**Maintenance**
- [ ] Is the next review date set?
- [ ] Is there a named owner for each initiative?
- [ ] Is the strategy accessible to the full engineering team?

---

## Strategy Review Cadence

| Review type | Frequency | Agenda |
|---|---|---|
| **Quick pulse** | Monthly (15 min) | Are initiatives on track? Any signals to adjust? |
| **Quarterly review** | Quarterly (2 hours) | Progress against metrics; update initiatives; revisit guiding policies if context has shifted |
| **Annual refresh** | Annually (1–2 day offsite or async) | Full rewrite from diagnosis; reconnect to updated business strategy |
| **Out-of-cycle trigger** | As needed | Major pivot, acquisition, leadership change, market shock |

---

## Output Format

When applying this skill, the agent should:
- Ask for the business context and current engineering situation before drafting anything
- Identify whether the request is for a full strategy doc, an executive summary, or a review of an existing strategy
- Produce the requested artifact using the templates above
- Flag any section where the diagnosis or guiding policies are weak
- Call out trade-offs that aren't being made explicitly
- Suggest 2–3 outcome-based success metrics grounded in DORA or business metrics

---

## References
- Anna Shipman: [Creating, defining and refining an effective tech strategy](https://leaddev.com/tech-strategy) — LeadDev
- Randy Shoup: [Building a Technology Strategy](https://leaddev.com/tech-strategy) — LeadDev
- Will Larson: *An Elegant Puzzle* — Chapter on engineering strategy
- Richard Rumelt: *Good Strategy / Bad Strategy* — Source of the diagnosis/policy/action framework
- Will Larson: [Writing an Engineering Strategy](https://lethain.com/writing-an-engineering-strategy/) — lethain.com
- LeadDev: [How to align your engineering work with business strategy](https://leaddev.com/tech-strategy)
