---
name: decide
description: Run a decision through the 12-lens framework
trigger: /decide
---

# Decision Framework

Run any decision through the evaluation framework from `system/04_decision_frameworks.md`. Produces a structured recommendation.

## Usage

`/decide [decision or opportunity to evaluate]`

## Process

1. **Parse the decision** — What's being decided? What are the options?
2. **Run relevant lenses** — Not all 12 apply to every decision. Select the 4-6 most relevant:
   - Leverage — disproportionate output?
   - Alignment — advances an active priority?
   - Reversibility — can it be undone?
   - Time Sensitivity — does waiting cost anything?
   - Revenue Impact — creates/protects/accelerates revenue?
   - Asymmetry — large upside, bounded downside?
   - Dependency — unblocks other work?
   - Cost — money, time, attention?
   - Compounding — gets better over time?
   - Simplicity — simpler path available?
   - Confidence — how certain are the inputs?
   - Opportunity Cost — what are we NOT doing?
3. **Check against principal's decision framework** — `system/14_decision_framework.md`
   - Does it pass the pattern filter?
   - Where does it sit in the priority stack?
   - Does it pass the asymmetry test?
4. **Check authority level** — `system/12_authority_matrix.md`
   - Is this Level 1 (just do it), Level 2 (recommend), or Level 3 (human only)?

## Output Format

```
DECISION: [What we're deciding]
OPTIONS: [A vs B vs C]
RECOMMENDATION: [What to do and why]
KEY LENSES: [3-4 lenses that drove the recommendation]
TRADE-OFF: [What we're giving up]
CONFIDENCE: [High / Medium / Low — and why]
AUTHORITY: [Level 1/2/3 — can the AIgent act or needs approval]
NEXT ACTION: [Specific immediate step]
```

## Rules

- Be direct. Recommend, don't waffle.
- If confidence is low, structure it as an experiment, not a commitment.
- If it's Level 3, present the analysis but explicitly say "this is your call."
- Always name the trade-off. Every yes is a no to something else.
