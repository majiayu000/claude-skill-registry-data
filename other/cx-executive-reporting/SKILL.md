---
name: cx-executive-reporting
description: Use to distil a CX dashboard into the three numbers a board or exec actually needs — volume/demand health, quality/outcome, and cost/efficiency — with commentary that drives decisions instead of forty tiles nobody acts on. Trigger for "board pack", "exec summary for support", "what should leadership see", "too many metrics on the dashboard", "three KPIs for the board", quarterly business review CX section, or when a leadership deck is mostly charts with no story.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Executive CX reporting

The usual board pack is a screenshot of the dashboard with forty metrics arranged in
a grid. Everyone nods. Nobody decides anything, because the pack answers every
question except the one executives actually have: **is the operation healthy, and
where do we intervene?**

Dashboards grow by accretion — every team adds a tile, every vendor ships a default
widget, every initiative gets a vanity metric to prove it worked. The result is not
insight. It is coverage: enough numbers that someone can always find one that moved
in the right direction.

This skill picks three numbers that drive decisions, writes commentary that survives
challenge, and leaves the rest in the appendix or off the page entirely.

## The three slots

Every executive CX view needs exactly three headline numbers, one from each lane.
More than three and nothing gets remembered; fewer and a lane goes unmonitored.

| Lane | What it answers | Pick a metric that… |
| --- | --- | --- |
| **Volume / demand health** | Is demand rising, shifting, or becoming harder to serve? | Moves when the business or product changes, not when reporting changes |
| **Quality / outcome** | Are customers getting what they came for? | Reflects customer or audit outcome, not agent activity |
| **Cost / efficiency** | Is the operation sustainable at this demand level? | Uses a denominator everyone agrees on, and includes handle time *or* cost — not both as headlines |

**One number per lane.** If two metrics in the same lane would tell different
stories, that is a definition problem — fix it before the pack, do not show both
and let the board pick.

### Choosing the three

For each candidate metric, run the **decision test**:

1. **Would a board member change a budget, headcount, or policy on this number
   alone?** If not, it is a supporting metric, not a headline.
2. **Does it have a named owner who can explain a move in one sentence?** If not,
   it is not ready for the pack.
3. **Is the definition stable for at least two comparison periods?** If not, show
   the trend with a break label or pick a proxy until the series is fixed.
4. **Can you state the denominator in the headline?** "68% (n=41)" or "£4.20 per
   resolved contact (n=12,400)" — a rate without a denominator is not a headline
   number.

Reject vanity metrics outright: tickets closed per agent, chat concurrency peaks,
bot containment without a quality check, CSAT without response-rate context presented
as if it were pure satisfaction.

## What the pack contains

Structure beats decoration. A workable executive CX section has four parts, in this
order:

1. **Verdict** — one sentence: healthy, watch, or intervene, with the reason tied
   to a lane.
2. **Three numbers** — the headline metrics with period, comparison, denominator,
   and whether the movement is inside noise (check before writing commentary).
3. **Commentary** — what moved, why, so what, do what (see narrative structure
   below). Two paragraphs maximum for the main story; one short paragraph per lane
   only if they diverge.
4. **Appendix pointer** — where the full dashboard, segment breakdowns, and data
   notes live. The pack is not the dashboard.

**Charts are optional and secondary.** If a chart does not change the verdict, cut
it. Executives read sentences; they skim charts for confirmation, not discovery.

## Commentary that survives the room

Write for someone who will ask "why?" and "compared to what?" in the same breath.

- **Lead with whether the movement is real.** A two-point QA move on forty
  evaluations is noise. Saying so is a feature; explaining noise teaches people to
  act on it.
- **Name the comparison.** "Up from last month" is not enough — same ISO week,
  same market scope, same definition version.
- **Separate mix from performance.** Volume shifting to a harder channel can move
  quality and cost in opposite directions without anyone's service changing.
- **State what you ruled out.** Instrument change, sampling shift, integration
  gap — if you checked and it was not the cause, say so briefly.
- **End with a decision or a deliberate non-decision.** "No action — inside noise"
  is a valid outcome. "Monitor for one more period" is valid. "We don't know yet"
  with a named next step is valid. Silence is not.

Do not rank individuals in an executive pack unless the ranking is adjusted for mix
and the sample is large enough to defend.

## Relationship to the dashboard

The dashboard exists for operators. The pack exists for decision-makers. They
should not be the same document.

| Dashboard | Executive pack |
| --- | --- |
| Many metrics, drill-down | Three headlines |
| Updated continuously | Frozen at generation or restated with label |
| Exploratory | Decision-oriented |
| Owned by analytics / ops | Owned by the CX leader presenting it |

When someone asks "can we just export the dashboard?", the answer is: **you can,
but you will bring forty numbers and zero decisions.** Offer the three-number pack
instead, and link the dashboard for follow-up.

## Traps

- **Showing every metric that moved.** Most movement is noise or mix. Curate.
- **Activity metrics as outcomes.** Contacts handled, emails sent, and AHT alone
  do not tell the board whether customers are better off.
- **Hiding bad news in a sub-chart.** If quality fell, it is lane two, not a
  footnote on page twelve.
- **Changing definitions without a break.** A series that jumps because someone
  redefined "resolved" is not a trend — label the break or do not show history.
- **Benchmarking without scope match.** External comparisons belong in a separate
  section with explicit caveats, not woven into headlines as if they were equivalent.

## Present results to the user

1. **The three headline metrics** — one per lane, with formula reference, owner,
   period, comparison, denominator, and noise verdict.
2. **The one-sentence verdict** — healthy, watch, or intervene.
3. **Executive commentary** — what moved, why, so what, do what; two paragraphs
   unless lanes diverge materially.
4. **What was cut and why** — metrics considered but rejected for the pack, with
   the decision-test reason.
5. **Appendix contents list** — what supporting detail exists and where, without
   reproducing the full dashboard.
6. **Definition and data notes** — late data, suppressed cells, definition
   version changes, and which historical periods are not comparable.
