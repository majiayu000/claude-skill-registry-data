---
name: rsr-brief
version: 1.0.0
description: Turn research into a decision-ready brief tailored to a specific stakeholder and decision.
author: matrixx0070
tags: [research, brief, decision-support, stakeholder, recommendation]
capabilities: []
---

# Research Brief

## When to use
Reach for this when research is done and someone has to *act* on it — pick a vendor, set a strategy, approve a budget, brief an exec. It packages findings into a short, top-down document built around the decision the reader faces, not around what you found.

**Not for:** doing the research (use rsr-deep-dive); merging raw sources (use rsr-synthesis); mapping a field (use rsr-literature-map). A brief is the last mile — it assumes the analysis exists and formats it for a decision.

## Method
1. **Name the decision and the reader.** What choice is being made, by whom, by when, and what do they already know? *Decision:* if there's no actual decision, this is a summary, not a brief — say so and adjust.
2. **Lead with the answer.** Write the recommendation or bottom line first, in one or two sentences. The reader may read nothing else.
3. **Give the "so what."** 3-5 findings that directly drive the recommendation — each stated as an implication, not a raw fact.
4. **Show the options.** *Decision:* if it's a choice, lay out the realistic alternatives with the key trade-off of each; if it's informational, skip to risks.
5. **State confidence and risk.** How sure are you, what could change the answer, what's the biggest unknown.
6. **Close with next steps.** Concrete actions, owners if known. Push detailed evidence and citations to an appendix so the front stays scannable.

## Example
Decision: "Should we adopt Tool A or B for support automation? — VP Support, by Friday." Bottom line: "Adopt A: it fits our stack and costs 30% less at our volume; B wins only above 10k tickets/mo, which we won't hit this year." Findings: integration effort, cost curve, migration risk. Options table: A vs B vs status quo. Confidence: Medium — pricing confirmed, integration effort estimated. Next: 2-week pilot of A, owner named. Evidence and vendor quotes in appendix.

## Pitfalls
- Burying the recommendation under background — the busy reader quits before reaching it.
- Listing facts instead of implications ("costs $X" vs "at our volume, A saves $Y/yr").
- Projecting false certainty; a decision-maker needs the confidence level to weigh the call.
- Writing it generically instead of to the actual reader's knowledge and the actual deadline.

## Output format
```
BRIEF: <topic> — for <stakeholder>, decision by <date>

Bottom line: <1-2 sentences: the recommendation>

Why (so-what findings):
- <implication> 
- ...

Options: <A vs B vs status quo — one trade-off line each>   [omit if informational]

Confidence: <High|Med|Low> — biggest unknown: <..>
Next steps: <action — owner — by when>

Appendix: <evidence, sources, methodology>
```
