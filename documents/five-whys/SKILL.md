---
name: five-whys
description: Apply the 5 Whys technique to drill from a surface problem to a root cause. Outputs five sequentially numbered "Why?" lines with brief answers, ending in a root-cause statement. Use after an issue tree to drill the critical branch deeper, or any time the user wants to test whether the apparent cause is the actual cause.
---

# 5 Whys

## Concept

Toyota's Sakichi Toyoda popularized the 5 Whys: take any apparent cause and ask "Why?" five times in succession. Each answer becomes the new statement; you drill until you hit a root cause that isn't itself a symptom of something deeper.

In the consulting toolkit, 5 Whys complements issue trees. Issue trees go *wide* (every plausible cause). 5 Whys goes *deep* on one branch — the one you suspect dominates. It's especially useful after a Pareto step has named the vital 20%, before committing to interventions.

Five is a heuristic, not a magic number. Sometimes you reach root cause at three; sometimes you have to push to seven. The discipline is asking "why" until the answer stops being a symptom and starts being something structural.

## Required output format

A numbered list of five Why → Because pairs, followed by a one-sentence root-cause statement.

```markdown
**Starting problem:** [The apparent issue you're drilling into.]

1. **Why?** [First-level reason]
2. **Why?** [Second-level — drilling into #1's answer]
3. **Why?** [Third-level — drilling into #2's answer]
4. **Why?** [Fourth-level — drilling into #3's answer]
5. **Why?** [Fifth-level — drilling into #4's answer]

**Root cause:** [One-sentence structural cause, addressable as a system change.]
```

## Defaults & flex points

| Default | When to flex |
|---|---|
| 5 levels deep | Sometimes 3 is enough (the structural cause is shallow); sometimes 6–7 is needed (deep institutional cause). Push until the answer is no longer a symptom. |
| One thread | Drill a single chain — don't branch mid-way. If the answer to a "Why?" is multi-causal, pick the dominant cause and drill that one. Run a separate 5 Whys on the other if needed. |
| Each Why builds on the previous | Don't restart the chain or re-ask the same question. Each answer must logically follow from the one above. |

**The root-cause test:** the final answer should be something you can *change as a system* — a process, a policy, an incentive, a data-flow design. If the final answer is "people are bad" or "the world is hard," you haven't reached root cause. Push deeper.

## Example — sales / win rate

**Starting problem:** Mid-market sales win rate dropped from 28% to 17% in two quarters.

1. **Why?** Late-stage deals (post-evaluation) are stalling at procurement and rarely closing.
2. **Why?** Procurement keeps pushing back on our standard MSA terms — primarily on data-residency and indemnity.
3. **Why?** Our standard MSA hasn't been updated since pre-GDPR; the data-residency clause is too vague for current customer expectations, and the indemnity cap is below industry norm.
4. **Why?** The MSA template lives in a Google Doc owned by a Sales Director who left the company; updates have been ad hoc, with no formal review cadence.
5. **Why?** There is no process owner for commercial document management — no cadence, no version control, no responsible counsel, no SLA on updates.

**Root cause:** The company has no process owner for commercial document lifecycle management. The MSA degradation is a symptom; the structural cause is institutional ownership of contract templates.

## Common mistakes

- **Stopping at "people did X."** "Why? Because Bob made a mistake" isn't root cause — it's a symptom. Why did Bob make the mistake? What in the system permitted it?
- **Branching the chain.** "Why? Because of A and B and C" — pick one and drill. Run separate 5 Whys for the others if needed.
- **Restating the same level.** Each Why should drill *down*, not sideways. "Why is X happening? Because X is a problem" is not progress.
- **Reaching for "macro factors" too early.** "Why? Because of the economy" or "Why? Because of regulation" can be true but rarely actionable. Push for the proximate cause first.

## When to use this skill alone vs. as part of the full analysis

- **Standalone:** when the user has a specific issue branch they want to drill, and they know which one. Skip the issue tree if the relevant branch is already obvious.
- **As part of full analysis:** in the 7-framework master (`strategy-consultant-7`), 5 Whys runs after Issue Trees and before Hypothesis-Driven — drilling the most-likely branch surfaces the testable hypothesis.

---

## Acknowledgment & License

The 5 Whys is attributed to Sakichi Toyoda and the Toyota Production System; widely adopted in lean manufacturing and consulting practice. Visual contract adapted in the spirit of the **Analyst Academy** original — see [5 Consulting Frameworks to Solve Any Problem](https://www.youtube.com/watch?v=uCmTk06aM70). MIT-licensed; see [LICENSE](../../LICENSE).
