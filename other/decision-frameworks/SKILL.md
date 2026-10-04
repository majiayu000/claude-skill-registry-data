---
name: decision-frameworks
version: 1.0.0
category: Leadership & Mindset
domain: decision-making
author: Matt Warren
license: MIT
status: production
updated: 2026-02-07
activation_triggers:
  - "help me decide"
  - "decision framework"
  - "should I"
  - "pros and cons"
  - "trade-offs"
  - "compare options"
  - "weighted decision"
  - "pre-mortem"
  - "thinking through"
tools: []
---

# Decision Frameworks

Structured decision-making for founders using reversibility analysis, weighted scoring, pre-mortems, and second-order thinking.

## Purpose

Founders make hundreds of decisions a week. Most should be fast. Some need structure. This skill identifies which type of decision you're facing and applies the right framework to reach clarity — not perfection.

## Workflow

### Step 1: Classify the Decision

Ask the user to describe the decision, then classify it:

**Type 1 (Irreversible / High-stakes):**
- Hard or impossible to undo
- Large financial, team, or strategic impact
- Examples: Hiring a co-founder, taking funding, pivoting the business, signing a lease
- **Treatment:** Slow down. Use full framework. Get more data.

**Type 2 (Reversible / Low-stakes):**
- Easy to undo or change course
- Limited blast radius
- Examples: Choosing a tool, testing a marketing channel, pricing experiment
- **Treatment:** Decide fast. Run the experiment. Don't overthink.

Tell the user which type they're dealing with.

### Step 2: Select Framework

**For Type 1 decisions — use Weighted Scoring + Pre-mortem:**

**Weighted Scoring Matrix:**
1. List the options (2-5)
2. Define criteria that matter (3-7 criteria)
3. Weight each criterion (must sum to 100%)
4. Score each option per criterion (1-10)
5. Calculate weighted totals

| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| [Criterion 1] | 30% | 7 (2.1) | 5 (1.5) | 8 (2.4) |
| [Criterion 2] | 25% | 6 (1.5) | 8 (2.0) | 4 (1.0) |
| ... | | | | |
| **Total** | 100% | **X.X** | **X.X** | **X.X** |

**Pre-mortem:**
After the scoring, run a pre-mortem on the top option:
- "It's 12 months from now and this decision was a disaster. What went wrong?"
- List 3-5 failure scenarios
- For each: How likely? How preventable? What's the mitigation?

**For Type 2 decisions — use 10/10/10 + Regret Minimization:**

**10/10/10 Rule:**
- How will I feel about this in 10 minutes?
- How will I feel in 10 months?
- How will I feel in 10 years?

**Regret Minimization:**
- "When I'm 80, will I regret NOT doing this more than doing it?"
- Bias toward action for reversible decisions

### Step 3: Surface Second-Order Effects

For any decision, ask:
- "And then what?" (repeat 3 times)
- What does this make easier in the future?
- What does this make harder?
- What door does this open? What door does it close?

### Step 4: Deliver the Recommendation

Structure:
1. **The decision:** Restate clearly
2. **My recommendation:** [Option X] because [reason]
3. **Confidence level:** High / Medium / Low (and why)
4. **Biggest risk:** [What could go wrong]
5. **Mitigation:** [How to reduce that risk]
6. **Reversibility check:** How hard is this to undo if it's wrong?

## Output Format

```markdown
## Decision: [Brief description]

### Classification
**Type:** [1 or 2] — [Irreversible/Reversible]
**Stakes:** [High/Medium/Low]

### Analysis
[Framework output — scoring matrix, pre-mortem, or 10/10/10]

### Second-Order Effects
- If yes: [consequence chain]
- If no: [consequence chain]

### Recommendation
**Go with:** [Option]
**Because:** [Core reason]
**Confidence:** [High/Medium/Low]
**Biggest risk:** [Risk]
**Mitigation:** [How to handle it]
**Reversibility:** [Easy/Hard to undo — timeframe]
```

## Constraints

- Never make the decision for the user — present the analysis and recommendation, but it's their call
- Don't overanalyze Type 2 decisions — the cost of delay often exceeds the cost of a wrong choice
- Always include confidence level — don't present uncertain conclusions with false certainty
- Surface emotional factors ("What does your gut say?") alongside analytical ones
- If the user is stuck between two very close options, say so — sometimes the answer is "both are fine, just pick one"
