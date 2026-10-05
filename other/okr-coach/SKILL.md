---
name: okr-coach
description: 'Write and refine OKRs with feedback on ambition, measurability, and alignment to company goals. Use when: write okrs, okr review, objectives and key results, quarterly goals, review my okrs, help with okrs.'
disable-model-invocation: true
---

# OKR Coach

Write and refine OKRs with feedback on ambition, measurability, and alignment to company goals.

**What are OKRs?** Objectives and Key Results (OKRs) are a goal-setting framework where:
- **Objectives** are qualitative, inspirational goals (quarterly)
- **Key Results** are quantitative, measurable outcomes (3-5 per objective)
- **Good OKRs** are stretch goals with ~70% confidence of hitting them

## Output
Save to `strategy/outputs/okrs-[YYYY-MM-DD].md`

## When to Use This Skill
- Quarterly OKR drafting before calibration
- Reviewing team OKRs as a manager
- Training teams on what good OKRs look like
- Converting vague goals into measurable OKRs

## What You'll Need

**One of these:**
- Draft OKRs you want me to review and improve, OR
- Goals/priorities you want me to convert into OKRs

(Either works — I'll meet you where you are)

**Helpful:**
- Company/team OKRs for alignment check
- Current metrics (for realistic baselines)
- Context on strategic priorities

## Process

### Step 1: I'll Check Your Context Files
I'll read your context files to find:
- Company strategic priorities (from `company.md`)
- Current metrics and baselines (from `product.md`)
- Top-level goals if you have them (from `goals.md`)

Then I'll confirm what I found so you can see how I'm grounding the review. For example:
> "I found your company priorities: 'Win the Agency Vertical' and 'Expand AI Capabilities.' Current metrics show DAU/MAU at 45%, NPS at 42. I'll check if your OKRs align to these priorities and use these metrics as baselines."

### Step 2: Understand the Input
If given draft OKRs → review and improve them
If given goals but no OKRs → help draft from scratch

**If critical context is missing, ask:**
> "To write good OKRs, I need a few things:
> 1. What company or team goals should these align to?
> 2. Do you have current metrics I can use as baselines? (e.g., current NPS, retention rate)
>
> You can also add these to your `context/` files so I have them for future sessions."

### Step 3: I'll Score Each OKR
I'll automatically assess each OKR on:
- **Ambition:** Is it a stretch? (50-70% confidence = good)
- **Measurability:** Can you track it objectively with a number?
- **Alignment:** Does it ladder to company goals?
- **Clarity:** Would a stranger understand it?

You'll get a score breakdown in the output.

### Step 4: I'll Flag Common OKR Mistakes
- **Outputs vs. outcomes:** "Ship X" → "X adoption reaches Y%"
- **Activities vs. results:** "Do research" → "Insights inform 3 decisions"
- **Too many KRs:** Keep to 3-5 per objective max
- **Binary vs. measurable:** "Launch" → "N users using feature"
- **Missing baselines:** "Improve" → "Improve from X to Y"
- **Subjective qualifiers:** "Good", "positive", "world-class" → specific numbers

### Step 5: I'll Rewrite Problem OKRs
For each issue I find, I'll provide a specific rewrite with:
- Clear baseline (current state) — pull from product.md if available
- Specific target (end state)
- Rationale for the number

## Output Template

```markdown
# OKR Review

## Context
*What I found in your files:*
- **Company priorities:** [From company.md]
- **Current metrics:** [From product.md — baselines for KRs]
- **Goals alignment:** [From goals.md if exists]

## Summary
- **Objectives Reviewed:** [N]
- **Key Results Reviewed:** [N]
- **Overall Quality:** [X/10]

[One paragraph summary of main issues and strengths]

---

## Objective 1: [Name]

**Original:** [Text]
**Quality Score:** [X/10]
**Alignment:** [Which company priority this supports]

I'll score each criterion on a 1-5 scale (5 = excellent) and highlight issues:

| Criterion | Score | Issue |
|-----------|-------|-------|
| Ambition | [X/5] | [Feedback] |
| Measurable | [X/5] | [Feedback] |
| Aligned | [X/5] | [Feedback — cite company.md] |
| Clear | [X/5] | [Feedback] |

**Suggested Rewrite:**
> [Improved objective]

### Key Results

**KR1 Original:** [Text]
**Issues:**
- [Issue 1]
- [Issue 2]

**Suggested Rewrite:**
> Baseline: [Current value from product.md or ask]
> Target: [Specific number]
> "[Improved KR with baseline → target]"

**Rationale:** [Why this target makes sense]

---

## Common Patterns Found
1. [Pattern and explanation]
2. [Pattern and explanation]

## Alignment Check

| Objective | Company Priority | Alignment |
|-----------|------------------|-----------|
| [Objective 1] | [Priority from company.md] | ✅ Strong / ⚠️ Weak / ❌ Missing |

## Recommendations
1. [Specific action]
2. [Specific action]

## Metrics to Track
*Baselines from your context files to use in KRs:*
| Metric | Current Value | Source |
|--------|---------------|--------|
| [Metric] | [Value] | [product.md] |

## Suggested Updates to Context Files
- [ ] Add OKRs to `goals.md` for reference
- [ ] Update baseline metrics in `product.md` as they change
```

## Framework Reference

**OKR framework** from John Doerr's *Measure What Matters*:

**Objectives should be:**
- Qualitative and inspirational
- Time-bound (usually quarterly)
- Ambitious but achievable

**Key Results should be:**
- Quantitative and measurable
- Specific (baseline → target)
- 3-5 per objective maximum
- Stretch goals (0.7 = success)

**Scoring OKRs:**
- 0.0-0.3: Failed to make progress
- 0.4-0.6: Made progress but fell short
- 0.7-1.0: Delivered (0.7 is target for stretch goals)

## Tips for Best Results

1. **Keep context files updated** — I'll pull baselines from product.md and priorities from company.md
2. **Bring current metrics** — Realistic baselines make better targets
3. **Share company OKRs** — Enables alignment checking
4. **Iterate quickly** — After I give feedback, tell me "make it more ambitious" or "add measurability to KR2" and I'll refine on the spot
