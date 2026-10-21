---
name: ieevisualizer-report-figures
description: "Use when an agent prepares figures and text for a recurring company report or management briefing with ieeVisualizer, or answers a reader's follow-up question about one: classifies each item as monitoring, exception or exploration, runs evidence → figure → caveat → decision, keeps figures to the few that change a decision, freezes artifacts for reproducibility, and refuses to generate reports or charts nobody needs."
license: CC-BY-4.0
---

# Report figures for recurring briefings

The output is not "a report was sent". It is "a decision-maker saw a
specific change, understood how sure we are, and made a better decision with
little extra effort". Every figure, sentence and section is judged against
that.

## Who owns what

| Owner | Responsibility |
|---|---|
| Host reporting workflow (e.g. a scheduled job runner) | schedule and cadence, permissions, recipient filtering, approval, delivery |
| Domain systems and analytics | authoritative data and every computed metric, interval and forecast |
| ieeVisualizer | visual form, templates, themes, rendering, export, manifests |
| The agent (you) | choose items and forms, bind evidence, inspect figures, write the explanation |

You never compute a business metric inside the figure step, never widen
access beyond the permission-filtered evidence you were given, and never
send anything externally without the host's approval step.

## Step 1: classify every candidate item

| Class | Test | Treatment |
|---|---|---|
| **Monitoring** | metric within its normal range vs the stated base | one line in the top block; no figure unless a trend is the point |
| **Exception** | outside normal range, a threshold crossed, or a source failed | lede + one figure + caveat + decision request |
| **Exploration** | a reader asked a question | answer first, then evidence; reuse existing artifacts |

"Normal range" must be defined (e.g. same weeks last year ± the historical
spread, or a threshold the readers set), not felt. A failed source is
always an exception: say so and show no figure for it (`figure-is-a-claim`).

## Step 2: evidence → figure → caveat → decision

For each exception or exploration item:

1. **Evidence.** The computed values, with provenance and the comparison
   base. Run `when-numbers-lie-audit`.
2. **Figure** only if it shows something a sentence cannot
   (`chart-choice-by-relationship`); build with `ieevisualizer-figures`;
   put the report run id in `spec.metadata` and the provenance. Render with
   the organisation's registered report theme, looked up with
   `themes.list_themes()` rather than a name hardcoded in the skill or the
   report code, and pin it as `name@version` so a re-render matches what was
   sent.
3. **Caveat.** One sentence naming the main thing that could make the figure
   misleading or the competing explanation.
4. **Decision.** What the readers could do, the owner, and when the
   question can be settled. Or "no action".

## Step 3: assemble

Use `company-report-structure`: the four-line top block (what changed, why
it matters, what is uncertain, what warrants action), then exceptions, then
explorations, then method. Prose in `editorial-voice-wsj-like`; numbers in
`numbers-style`; every headline checked by `headline-and-deck`; final pass
with `figure-review-redteam`.

## Metric traps (generic examples, illustrative)

Every recurring metric needs a written definition before it is reported.
Typical traps, using an online shop as the example:

| Metric | Define | Common trap |
|---|---|---|
| Orders | paid orders, by date of payment | counting by order date vs delivery date mixes two series |
| Lead-to-order conversion | orders / leads, same cohort | immature cohorts: recent leads have not had time to convert |
| Revenue, revenue per order | € excl. VAT, recognised on a stated date | average of regional averages; restatements after late refunds |
| Ad spend per order (CPA), ROAS | spend / attributed orders, named attribution window | window changes; platform-reported vs observed conversions |
| On-time delivery | deliveries within the promised window / deliveries | deliveries with no recorded time silently excluded |
| Return rate | returns by order month / orders | returns arrive weeks later: the latest month is incomplete |
| Capacity utilisation | booked hours / available hours | missing shift data read as zero availability or zero use |
| Budget burn | spend / budget | a nullable budget column where null means "no budget set" is undefined, not 0% |

## Follow-up questions

When a reader asks "why did conversion fall?":

1. Reopen the report's artifacts (spec + frozen snapshot) rather than
   starting from a screenshot.
2. Compare with preceding periods and the same period last year.
3. Segment where the data permits (channel, region, cohort, device) and
   decompose rate vs mix.
4. Check the usual suspects: tracking or attribution change, price change,
   traffic quality, response latency, seasonality, immature cohorts.
5. Report supported findings with uncertainty. Name a likely cause only as
   far as the design allows (`statistical-claims`), and say what would
   verify it (a holdout, a week more data, a reconciliation).
6. A refreshed analysis is a new artifact; the sent figures stay as they were.

## No autonomous bureaucracy

- Do not create new recurring reports, sections or charts on your own
  initiative. Propose them; humans decide.
- A quiet period gets a short monitoring note (or nothing, if that is the
  agreed rule), not padding.
- Prefer one decisive figure to five descriptive ones.
- Prefer human approval for external distribution, sensitive data and
  consequential recommendations.
- Usefulness is measured by questions resolved, time to explanation and
  decisions supported, not by reports, pages or charts produced.

## Good / bad

Bad: 14-chart weekly PDF covering every metric, each titled with the metric
name, sent automatically every Monday.
Good: top block with three monitoring lines and one exception ("Meta ads
attribution export failed; ad spend per order unavailable this week"),
one figure for the conversion change with its caveat, and a decision request.

## Checklist

- [ ] Every item classified monitoring / exception / exploration against a defined base.
- [ ] Source failures reported as exceptions with no figure.
- [ ] Each exception: evidence, at most one figure, one caveat, one decision with owner.
- [ ] Figures built with `ieevisualizer-figures`, inspected, run id in metadata.
- [ ] Theme looked up from the registry and pinned by version, not hardcoded by name.
- [ ] Top block written last and checked against the body.
- [ ] Follow-ups reuse frozen artifacts; refreshed analyses are new artifacts.
- [ ] Nothing added for completeness; nothing sent without the host's approval.

Adapted in part from ieeVisualizer's own documentation (`docs/`, MIT);
changed: rewritten as an agent procedure with generic examples.
Sources and licences: `SOURCES.md`.
