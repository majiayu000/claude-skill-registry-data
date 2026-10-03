---
name: pyramid-principle
description: Structure a recommendation top-down — Barbara Minto's Pyramid Principle. Outputs a single-sentence top-line answer, three to five supporting arguments, and one layer of evidence under each. Use to convert analysis into executive communication, or to structure a board-meeting talk track.
---

# Pyramid Principle

## Concept

Barbara Minto, working at McKinsey in the 1960s, codified how consultants structure communication: the **answer first, supporting arguments second, evidence third**. Top-down. Audiences don't want a journey of discovery; they want the conclusion, then the reasons.

The Pyramid Principle works like this:

- **Top:** the single-sentence answer to the question on the audience's mind.
- **Middle:** 3–5 supporting arguments. Each argument is itself a complete thought (not a topic).
- **Bottom:** evidence — data, examples, observations — supporting each argument.

Used at the end of a strategy analysis (after MECE, Issue Tree, Hypothesis, Pareto, So What), the Pyramid translates the analytical work into a deliverable that a CEO can read in 90 seconds and quote in a board meeting.

## Required output format

A pyramid structure rendered in Markdown: top-line answer in bold, supporting arguments as numbered list items each with their own evidence sub-bullets.

```markdown
**Answer:** [One-sentence direct answer to the question. Specific. Actionable. No hedging.]

1. **[Supporting argument 1]**
   - [Evidence point]
   - [Evidence point]
   - [Evidence point]

2. **[Supporting argument 2]**
   - [Evidence point]
   - [Evidence point]

3. **[Supporting argument 3]**
   - [Evidence point]
   - [Evidence point]
```

## Defaults & flex points

| Default | When to flex |
|---|---|
| 3–5 supporting arguments | If only 2 arguments genuinely make the case, use 2. If you have 7, you're confusing arguments with evidence — re-group. |
| 2–4 evidence points per argument | Use as many as you need — but if you have 8, you're conflating evidence with subsidiary arguments. Re-structure. |
| Top-line is one sentence | Don't flex. Two sentences is two answers; pick one. |
| Top-line is specific and actionable | Don't flex. "We should improve customer experience" is not a Pyramid top-line; "Reverse the price increase on the $50–$250K segment within 30 days" is. |

**Minto's two MECE rules for the Pyramid:**

1. The supporting arguments must be MECE under the top-line answer.
2. Each evidence set must be MECE under its argument.

If two arguments overlap, merge them. If an argument doesn't actually support the top-line, cut it.

## Example — sales reorg recommendation

A continuation of the upstream analysis for a SaaS sales-cycle problem (sales cycle stretched 60 → 110 days, leadership considering reorg).

**Answer:** Do not reorganize the sales team — fix internal handoff bottlenecks (security review, legal redlines) within 90 days; revisit reorg only if the bottleneck thesis is invalidated.

1. **The cycle stretch is dominantly an internal-process problem, not a sales-execution problem.**
   - Time spent in late-stage internal review (security + legal) accounts for ~60% of the 50-day increase
   - Win rates from late-stage to closed-won are roughly stable (64% vs. historical 67%) — deals that get out the door still close
   - AE quota attainment is uniformly down across tenure bands, not concentrated among new hires (which would point to ramp problems)

2. **The two specific bottlenecks are well-defined and fixable in 90 days.**
   - Security review averaging 22 days, vs. historical 8 days — single staffing issue post-Q2 InfoSec reorg
   - Legal redline turnaround averaging 18 days, vs. historical 6 days — one in-house counsel handling all vendor agreements
   - Both have known interventions: temporary security reviewer + standardized MSA template

3. **A sales reorg now would burn time and trust without addressing the cause.**
   - Reorgs typically take 6–9 months to settle and depress productivity 15–25% during that window
   - The cycle stretch is observable across reps, segments, and deal sizes — a structural change to the sales team won't move it
   - If the bottleneck thesis is wrong, we'll know in 30 days from the data pull and can revisit then

## Common mistakes

- **Top-line that's a topic, not an answer.** "Sales cycle issues" is a topic. "Don't reorg, fix internal handoffs within 90 days" is an answer.
- **Hedging in the top-line.** "We might want to consider..." or "It could be that..." defeats the Pyramid. Commit.
- **Arguments that are actually topics.** "Customer success" is a topic. "Customer success activity has dropped post-reorg, contributing 30% of the cycle increase" is an argument.
- **Evidence that isn't evidence.** "Our team thinks..." is not evidence. Numbers, specific observations, named instances are.
- **Too many top-line answers.** A second sentence in the top-line is a second answer — pick one and put the other in a follow-up.

## When to use this skill alone vs. as part of the full analysis

- **Standalone:** when the user already has the analysis done and needs to convert it into an executive-ready memo, presentation, or talk track.
- **As part of full analysis:** in the 7-framework master (`strategy-consultant-7`), Pyramid Principle runs after the "So What?" test — taking the action-oriented insight and structuring it for executive communication.

---

## Acknowledgment & License

The Pyramid Principle is **Barbara Minto's** framework, codified in her 1985 book *The Pyramid Principle: Logic in Writing and Thinking*, developed during her time at McKinsey. The visual contract here is adapted in the spirit of the **Analyst Academy** original — see [5 Consulting Frameworks to Solve Any Problem](https://www.youtube.com/watch?v=uCmTk06aM70). MIT-licensed; see [LICENSE](../../LICENSE).
