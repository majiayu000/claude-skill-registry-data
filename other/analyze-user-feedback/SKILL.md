---
name: analyze-user-feedback
description: Turn raw feedback (surveys, tickets, reviews, Slack, notes) into ranked themes with counts, sentiment, quotes, and recommended actions; a script does the counting. Use when you have a pile of feedback to make sense of. For one interview transcript, use analyze-user-interview.
---

# Analyze User Feedback

Synthesize feedback from any mix of sources into a short, evidence-backed report: what people are telling us, how often, how strongly, and what we should do about it.

## Reasoning Framework

Feedback analysis goes wrong in two ways: counting by feel (the loudest anecdote wins) and theming without evidence. This skill splits the work. A script does the deterministic parts (merging files, de-duplicating, sampling, counting); the model does the judgment (codebook, coding, interpretation). Every number comes from the script and every claim points to item IDs, so anyone can audit the result.

## Output Contract

| Artifact | Format | Handed to |
|----------|--------|-----------|
| `feedback.csv` | Normalized items with stable IDs (`F0001`…) | Working file |
| `codes.csv` + codebook | `id,theme,sentiment[,severity]` plus theme definitions | Working file, reused next cycle |
| `themes.md` | Theme counts, shares, sentiment (script output) | Appendix |
| Feedback analysis | Markdown report (template below) | PM, team, leadership |

## When to Use

- Survey open-ends, NPS/CSAT comments, support tickets, app-store reviews, sales notes, community threads
- Combining several feedback sources into one view
- Repeating an analysis each cycle and comparing to last time

## When NOT to Use

- One interview transcript: use `analyze-user-interview`
- Designing a survey: use `devex-survey` (developer experience) or `create-user-interview`
- Deciding what to build from known themes: use `prioritize-features`

## Inputs

Ask for anything missing, in one message:

1. **Files**: CSV, TSV, JSONL, TXT or MD. Excel: export to CSV first.
2. **The question**: the decision this informs (e.g. "why don't trial users convert?").
3. **Scope**: date range, segments, or products to include.
4. **Prior codebook** (optional): last cycle's themes, for comparison.

## Steps

1. **Frame.** Restate the question and scope in one sentence and confirm it.
2. **Prep (script).** Merge and number everything; read the script's summary, not the raw files:
   ```bash
   python3 scripts/feedback_tally.py prep <files...> -o <workdir>/feedback.csv
   ```
   If it suggests sampling (over ~600 items or ~60k tokens), rerun with `--sample 400 --seed 7`, code the sample, and report results as estimates. If it picked the wrong text column, pass `--text-col`.
3. **Draft the codebook.** Read a spread of ~60–100 items across sources. Define 6–12 themes, each with a one-line definition, an include/exclude rule, and an example ID. Name themes as user problems or needs ("Can't find old tickets"), not solutions ("Add search filters"). Reuse the prior codebook when there is one.
4. **Code every item.** Read `feedback.csv` in batches of about 100 rows and write `codes.csv` rows: `id,theme,sentiment[,severity]`. An item can carry several themes (`;`-separated). Add a new theme only when 3+ items need it; otherwise use `Other`. Note codebook changes as you go.
5. **Tally (script).**
   ```bash
   python3 scripts/feedback_tally.py tally <workdir>/feedback.csv <workdir>/codes.csv -o <workdir>/themes.md
   ```
   Add `--moe --population <N>` when you coded a sample. Fix any uncoded items or unknown IDs it reports, then rerun.
6. **Interpret.** For the top themes: the underlying need (what they ask for is often not what they need), who says it (sources, segments), severity, 2–3 verbatim quotes with IDs, and what's missing (silent segments, churned users, channels not covered).
7. **Recommend.** 3–5 actions, each tied to theme evidence and a next step (a fix, an experiment via `validate-hypothesis`, or a backlog item for `prioritize-features`).
8. **Write the report** to `<workdir>/feedback-analysis.md` using the template. Keep raw data local.

## Report Template

```markdown
# Feedback Analysis: [Scope], [Date range]

**Question:** [the decision this informs]
**Sources:** [source: n items, ...] · **Coded:** [n] ([sample of N] if sampled)

## Summary
[3 sentences: the biggest themes, what changed since last time, the recommended action.]

## Themes
| Theme | Share | Sentiment | Who | Representative quote |
|---|---|---|---|---|
| [Theme] | [x% ± moe] | [mostly negative] | [segments/sources] | "[verbatim]" (F0123) |

## What's behind the top themes
### [Theme]
[Underlying need, severity, evidence, open questions.]

## Recommendations
1. [Action]: [evidence] → [next step, owner]

## Gaps and caveats
[Missing channels or segments, sampling, coding judgment calls.]

## Appendix
Codebook, themes.md table.
```

## Longitudinal Tracking

Reuse the codebook (add themes, don't silently rename them), rerun `tally` per cycle, and compare shares. Treat a change smaller than the margin of error as noise.

## Examples

- "Here are last quarter's NPS comments and support tickets. What are people frustrated about?" Prep both files, code, tally, and report the top themes with quotes.
- "5,000 app reviews. Anything about onboarding?" Prep with `--sample 400`, code the sample, report onboarding share with a margin of error.

## Guardrails

- Never count by hand. Every count and percentage comes from the script.
- Quote verbatim, with the item ID. Don't paraphrase inside quotation marks.
- Frequency is not importance: a rare data-loss bug can outrank a common nit. Say so when it applies.
- Strip personal data (names, emails, account IDs) from the report; describe people by role or segment.
- Don't upload feedback files to external services, and don't commit them to this public repo.
- A sample gives estimates: report the sample size and margin of error.

## Related Skills

- `analyze-user-interview`: one interview in depth
- `prioritize-features`: rank what to build from these themes
- `validate-hypothesis`: test the riskiest belief a theme suggests
- `library/lenny-podcast/lenny-analyzing-user-feedback/SKILL.md`: principles from product leaders
