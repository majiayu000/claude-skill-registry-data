---
name: prioritize-features
description: Rank a backlog with RICE, ICE, weighted scoring, or Kano (a script does the math) and write a defensible priority memo with sourced estimates, a sensitivity check, and trade-offs. Use when deciding what to build next or justifying a roadmap order.
---

# Prioritize Features

Produce a ranking the team can argue with productively: every input has a source, the math is reproducible, and every override of the score is written down.

## Reasoning Framework

Prioritization frameworks don't decide for you. They make assumptions explicit so people can argue about the assumptions instead of the conclusion. The model's job is estimation with evidence and rationale; `scripts/prioritize.py` does the arithmetic, the ranking, and a sensitivity check, so nobody argues about math. A ranking is only as strong as its weakest estimate, so the memo names the estimate that would change the decision.

## Output Contract

| Artifact | Format | Handed to |
|----------|--------|-----------|
| `backlog.csv` | Items with inputs and a source for each estimate | Working file |
| Ranked table | Markdown from `scripts/prioritize.py` | Appendix |
| Priority memo | Markdown (template below) | Team, leadership |

## When to Use

- Choosing what to build next quarter or sprint
- Justifying a roadmap order, or saying no to requests, with a defensible method
- Comparing growth experiments quickly (ICE)
- Separating table stakes from delighters with survey data (Kano)

## When NOT to Use

- One big bet versus the status quo: use `decision-brief`
- Themes not known yet: run `analyze-user-feedback` first
- A single uncertain assumption: use `validate-hypothesis`

## Inputs

1. **Items**: features, themes, or opportunities, each written as "what + for whom".
2. **The goal**: one metric or outcome this round serves (for example activation), plus the time horizon.
3. **Evidence**: usage data, feedback counts (from `analyze-user-feedback`), customer asks, and effort estimates from engineering.
4. **Constraints**: commitments, deadlines, dependencies.
5. **Framework**: the user's choice, or recommend one from the table below.

## Choosing a Framework

| Framework | Use when | Inputs |
|---|---|---|
| **RICE** | Many items, one goal, reach data and engineering estimates available | Reach per quarter, Impact (3/2/1/0.5/0.25), Confidence (100/80/50%), Effort (person-months) |
| **ICE** | Fast triage of experiments or growth ideas with little data | Impact, Confidence, Ease (1–10) |
| **Weighted** | Several agreed strategic criteria matter (fit, revenue, risk reduction) | A 1–5 score per criterion, higher is better; weights agreed with stakeholders |
| **Kano** | Deciding what's expected versus what delights | Survey answer pairs (functional / dysfunctional) per feature |

## Steps

1. **Anchor on one goal and horizon.** Items serving different goals don't belong in one RICE run.
2. **Clean the list.** Merge duplicates, split items too big to estimate, and cap a pass at about 30 items.
3. **Estimate with sources.** Next to each input, note where it came from (analytics, n feedback items, sales asks, engineering estimate). Get effort from engineering; if that's impossible, mark it as a rough estimate with low confidence. Never invent reach or effort.
4. **Write the CSV and run the script:**
   ```bash
   python3 scripts/prioritize.py rice backlog.csv --sensitivity -o ranked.md
   python3 scripts/prioritize.py ice ideas.csv
   python3 scripts/prioritize.py weighted options.csv --weights value=3,fit=2,risk_reduction=1
   python3 scripts/prioritize.py kano responses.csv
   ```
   Fix any rows the script rejects and read its warnings (off-scale impact, moonshot confidence).
5. **Reality check.** Look for dependencies, commitments, strategic bets, and risk reduction (security, tech debt) the score doesn't capture. Change the order only with a written reason. Never tune inputs to reach a predetermined answer.
6. **Sensitivity.** Report whether the top items hold when any single estimate is ±20% off (the `--sensitivity` column). Name the estimate that would flip the decision and how to firm it up, often with `validate-hypothesis`.
7. **Kano, if you have survey data.** Must-bes first (table stakes), then performance features by value, then attractive features as differentiators. Without survey data, a Kano category is a hypothesis; label it that way.
8. **Write the memo.**

## Memo Template

```markdown
# Priorities: [Goal], [Horizon]

**Recommendation:** Build [A], [B], [C] next. [One sentence why.]
**Method:** RICE on [n] items; estimates sourced below; sensitivity checked.

## Ranked list
(script table)

## Why this order
- [A]: [evidence]
## Overrides of the score
- [Item] moved from #5 to #2 because [dependency/commitment/strategy].
## What we're not doing (and why)
- ..
## What would change our mind
- The ranking depends most on [estimate]; we'll firm it up by [method] by [date].
```

## Examples

- "Here are 18 feature requests; we care about activation this quarter." Source reach from analytics, get effort from engineering, run RICE with sensitivity, and write the memo naming the fragile #2 item.
- "Score these 10 growth experiments quickly." ICE, then flag the two with confidence ≤ 3 for a cheap test first.

## Guardrails

- No fabricated numbers. Unknowns are asked for, or marked as rough estimates with low confidence.
- Don't reverse-engineer inputs to justify a conclusion. Overrides are explicit and explained.
- A score is an input to the decision, not the decision.
- One goal per scoring run.
- Show the scale definitions in the memo so readers can challenge the estimates.

## Related Skills

- `analyze-user-feedback`: evidence for reach and pain
- `validate-hypothesis`: raise confidence on the estimate that matters most
- `decision-brief`: present the recommendation for a decision
- `create-prd`: spec the winners
- `library/lenny-podcast/lenny-prioritizing-roadmap/SKILL.md` and `library/lenny-podcast/lenny-evaluating-trade-offs/SKILL.md`: deeper playbooks
