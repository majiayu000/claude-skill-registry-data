---
name: company-report-structure
description: "Use when assembling a company report, business review, management briefing, KPI update or analysis memo from computed metrics: chooses the depth (monitoring, exception, exploration), orders content by decision relevance, structures each finding as claim vs comparison base, drivers, caveats, evidence, and keeps recommendations, unknowns and method separate. Use before writing the first section of any recurring or one-off report."
license: CC-BY-4.0
---

# Company report structure

A report exists to move a reader from *what happened* to *what to do*, with
the least reading and the least false confidence. Its length and number of
charts are costs, not achievements.

## Step 1: pick the depth

| Type | When | Shape |
|---|---|---|
| **Monitoring** | Routine cadence, nothing outside normal range | 3–6 lines: status of each tracked metric vs its base; "no action needed" is a valid conclusion |
| **Exception** | A metric left its normal range, a source failed, a threshold was crossed | lede + nut graf, one figure, drivers, caveats, decision needed |
| **Exploration** | Someone asked a question ("why did conversion fall?") | question, answer first, evidence, alternatives considered, what would settle it |

Most issues of a recurring report are monitoring. Do not inflate them.

## Step 2: the top block (always)

Four labelled lines, before anything else:

- **What changed:** the one or two facts that matter, with numbers and base.
- **Why it matters:** the consequence for money, capacity, customers or risk.
- **What is uncertain:** the main caveat, missing data, or competing explanation.
- **What warrants action:** the decision or check requested, with an owner,
  or "nothing this period".

## Step 3: each finding

1. **Claim** with number, period and comparison base
   (`headline-and-deck`).
2. **Drivers**: a decomposition that adds up (volume × price, rate × mix,
   segment contributions). State the residual if it does not fully explain.
3. **Caveats**: the pitfalls from `when-numbers-lie-audit` that could not be
   ruled out.
4. **Evidence**: one figure or table that shows the claim
   (`chart-choice-by-relationship`), with its source line.

Order findings by decision relevance, not by data source or department.

## Step 4: the back

- **Recommendations** in their own section, each with owner and the evidence
  it rests on. Never phrased as findings.
- **Unknowns**: what the data cannot answer yet and what would answer it.
- **Method and sources** (`source-and-provenance`).
- **Appendix**: full tables, definitions, figures not essential to a finding.

## Rules

- **One finding per figure; one figure per finding at most** in the body.
- **No chart without a claim**, no claim without evidence.
- **Comparisons are explicit**: vs last period, vs same period last year, vs
  plan; say which and why.
- **Decompositions must add up.** Example: revenue went from 188 orders ×
  €650 = €122,200 (Aug) to 212 × €690 = €146,280 (Sep), +€24,080. Volume
  effect at August price: 24 × €650 = €15,600. Price effect at September
  volume: €40 × 212 = €8,480. Total €24,080.
- **Unknowns are content.** "We cannot yet separate the campaign from
  seasonality" is a finding.
- **Write the top block last, read it first.** Check it against the body.
- **Stop when the information ends.** No filler sections to match a
  template.

## Template

`references/skeleton.md` has the skeleton with a worked monitoring and
exception example.

## Checklist

- [ ] Depth chosen; monitoring issues kept short.
- [ ] Top block has all four lines and matches the body.
- [ ] Each finding: claim + base, drivers that add up, caveats, one piece of evidence.
- [ ] Findings ordered by decision relevance.
- [ ] Recommendations separate, with owners.
- [ ] Unknowns and method sections present.
- [ ] Every figure supports a stated claim; none decorative.

Adapted in part from Anthropic's `analyze` and `validate-data` skills
(Apache-2.0) and ieeVisualizer's `docs/REPORTING_DECISION_LOOP.md` (MIT);
changed: restructured around decision depth and the four-line top block,
examples replaced. Sources and licences: `SOURCES.md`.
