---
name: hypothesis-driven
description: State a falsifiable hypothesis, then build a Markdown table comparing what you'd Expect to see if it's true vs. the Actual data (or what data is needed). Use for designing analysis plans, pinpointing where reality diverges from expectation, or step 3 of a strategic analysis.
---

# Hypothesis-Driven Problem Solving

## Concept

Don't boil the ocean. Start with a hypothesis — a specific, falsifiable claim about why the problem exists — then identify exactly what data would confirm or refute it. This is how consultants avoid running 40 analyses when 2 would do.

The visual trick: a comparison table that shows **what you'd expect to see if the hypothesis is true** next to **what the data actually shows** (or what data is required if not yet collected). The point of divergence is where the answer lives.

## Required output format

1. A one-sentence falsifiable hypothesis prefixed `**Hypothesis:**`.
2. A Markdown table with columns: Variable | Expected (if hypothesis true) | Actual / Required Data.

```markdown
**Hypothesis:** [One-sentence falsifiable claim.]

| Variable | Expected (if hypothesis true) | Actual / Required Data |
|---|---|---|
| Variable 1 | Expected pattern | What we observe / need |
```

## Defaults & flex points

| Default | When to flex |
|---|---|
| 4–7 variables | If only 3 truly diagnostic variables exist, use 3. Don't pad. |
| At least one control row | Don't flex this — confirmation bias is the most common failure mode. |
| One hypothesis per table | If multiple hypotheses, output multiple tables. |
| Variables are measurable | Don't flex this — unmeasurable variables aren't testable. |

**The control row test:** at least one row should describe something that should NOT match if the hypothesis is true. If everything in your table is set up to confirm, you're not testing — you're rationalizing.

## Example — pricing

**Problem:** A B2B software company raised list prices 18% in January. Six months in, new-logo bookings are down 22%.

**Hypothesis:** The price increase is the dominant driver of the bookings decline (rather than competitive shifts or pipeline quality issues), and the impact is concentrated in deal sizes under $50K where price sensitivity is highest.

| Variable | Expected (if hypothesis true) | Actual / Required Data |
|---|---|---|
| Win rate by deal size band, Q1 vs. Q3 | Should drop sharpest under $50K, modest under $250K, near-flat above $250K | Need to pull from CRM — segment win rates by ACV band before/after Jan 1 |
| Stage where deals stall | Late-stage stalls (procurement / pricing review) should rise; early-stage should be flat | Q3 stage drop-off: late-stage stalls 38% (Q1: 12%) ✅ matches |
| Discount approval rate | Sales should be requesting more discount approvals to close deals | Discount-request volume up 2.4× ✅ matches |
| Competitive losses citing price | Win/loss survey should show "too expensive" rising as a top-3 reason | Q1: 14% → Q3: 41% ✅ matches |
| Win rate above $250K (control) | Should be near-flat — large deals less price-sensitive | Q1: 28% → Q3: 26% — near-flat ✅ supports hypothesis |
| Pipeline quality score (control) | Should be unchanged — would invalidate hypothesis if it shifted | MQL → SQL conversion stable; no quality shift ✅ supports hypothesis |
| Recent competitor pricing moves | Should show no major change | Two competitors held prices; one raised 10% (similar trajectory) ✅ supports hypothesis |

The two control rows (>$250K win rate, pipeline quality) are designed to invalidate the hypothesis. They didn't — that's strong evidence. Without them, the table would just be confirmation bias.

## Common mistakes

- **Vague hypothesis.** "We have a sales problem" — there's nothing to test.
- **No control rows.** Every variable set up to confirm. The hypothesis becomes unfalsifiable.
- **Cramming multiple hypotheses into one table.** Output two tables instead.
- **Burying the conclusion.** If actuals all match, say so explicitly. Don't make the reader infer.

## When to use this skill alone vs. as part of the full analysis

- **Standalone:** when you already have a candidate hypothesis and need a clean test plan.
- **As part of full analysis:** `strategy-consultant` — hypothesis testing is step 3 of 5. Run `mece-framework` and `issue-trees` first to surface the hypotheses worth testing.

---

## Acknowledgment & License

Adapted from **Analyst Academy** on YouTube — [5 Consulting Frameworks to Solve Any Problem](https://www.youtube.com/watch?v=uCmTk06aM70). MIT-licensed; see [LICENSE](../../LICENSE).
