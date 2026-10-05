---
name: cx-recurring-report-spec
description: Use to turn an ad-hoc CX reporting request into a versioned spec that can be re-run each period and actually compared across periods. Trigger for weekly or monthly QA and support reports, "same report but for last week", "generate the weekly digest", "supervisor report for each team", a report request pasted as a long prompt for the second or third time, or when two runs of the same report disagree.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Recurring report specs

The most common CX reporting task is not building a report. It is rebuilding last
period's report with a new date range — and the way that usually happens is that
someone re-types a long prompt, tweaking the window and the team name.

That works once. What it does not do is produce a **series**. Every re-type is a
chance for a definition to shift, and when the number moves nobody can tell whether
the business moved or the definition did. By the third period the comparison is
worthless and no one knows it.

This skill converts a one-off request into a spec: parameters that are meant to
vary, definitions that are frozen, and a version number that changes when a
definition does.

## Recognise the trigger

You are in this skill's territory when any of these is true:

- The user has asked for a similarly-shaped report before.
- The request contains a date range and a team, department, or market name — the
  two things most likely to be the only real variables.
- The request is a long pasted prompt with a heading structure ("Overall
  performance / Team-wide trends / Individual agents").
- The user says "same as last time but…".
- Two runs of nominally the same report produced different numbers.

Say so. Offer to write the spec once instead of answering the prompt a fourth
time. This is a better use of the turn than producing the report faster.

## The one rule

**Only parameters may vary between runs. Everything else changing means a new
spec version.**

| Parameters — vary freely | Definitions — frozen |
| --- | --- |
| Period start and end | Which metric, and its exact formula |
| Team / market / queue / channel scope | The denominator |
| Comparison period | Which date field defines membership |
| Output destination and format | Status and validity filters |
| | Excluded accounts (bots, system, test) |
| | Taxonomy version, if categories are reported |
| | Small-cell suppression threshold |
| | Rounding and units |

If someone asks to "just also exclude the AI tickets this time", that is a version
bump, not a parameter. Produce it, label it v2, and say plainly that the series
before and after are not comparable. Silently honouring it is how a trend becomes
fiction.

## Writing the spec

Capture it as a file the user keeps, not as prose in a chat. Something like:

```yaml
name: weekly-qa-supervisor-report
version: 2                    # bump when any definition below changes
owner: cx-ops

parameters:
  period: {start: 2026-07-20, end: 2026-07-26}
  compare_to: previous_period
  scope: {teams: [inbound, outbound], channels: all}

definitions:
  period_boundary: iso_week            # or: custom, thu_to_wed — declare it
  date_field: conversation_closed_at   # NOT imported_at, NOT evaluated_at
  population: closed conversations eligible for QA
  metric: mean evaluation score
  denominator: completed, active evaluations   # excludes superseded
  exclude_accounts: [bot, system, integration]
  taxonomy_version: contact-drivers-v3
  suppress_below_n: 30
  restatement: freeze_at_generation     # or: restate_and_label

output:
  sections: [headline_movement, drivers, by_team, exceptions, data_notes]
  artifact: sheet
```

Then every run is: fill the parameters, apply the definitions unchanged, emit the
same sections in the same order.

## The four definitions that break series

These account for nearly every "the same report gave two different answers".

**1. The date field.** "July" is at least three different populations depending on
whether you filter on when the conversation happened, when it was imported, or when
it was evaluated. Backfills and late syncs make these diverge by a lot. Pick one,
name it in the spec, and never switch.

**2. The status filter.** Re-evaluated work leaves superseded records behind.
Including them inflates counts, and it inflates some aggregates more than others,
so totals stop reconciling between two sections of your own report. Apply one
status filter everywhere in the spec.

**3. Period boundaries.** ISO weeks are not the only convention in use — plenty of
teams run a reporting week that starts mid-week, and month boundaries and week
boundaries disagree about which period a Tuesday belongs to. Declare the
convention. Never mix ISO weeks in one section with calendar weeks in another.

**4. Restatement policy.** Data arrives late. Evaluations get completed after the
report ran. So last week's number changes when you re-run it, and someone will
notice. Decide up front:

- **Freeze at generation** — the number in the report is the number forever.
  Comparable across periods, diverges from the live dashboard.
- **Restate and label** — always recompute, and mark restated figures. Matches the
  dashboard, but a chart of frozen reports and a chart of restated ones tell
  different stories.

Either is defensible. Not choosing is not. If the report exists to be compared
period over period, freeze; if it exists to drive this week's action, restate.

## Report content that survives review

- **Put the denominator next to every rate.** "68% (n=41)" not "68%". A rate with a
  hidden denominator is the most common way a report misleads without containing a
  false statement.
- **Lead with whether the movement is real.** Before explaining a change, check
  whether it exceeds sampling noise. A two-point move on 40 evaluations is noise,
  and a report that explains noise teaches the reader to act on it. Decomposing the
  movement is a separate skill; the spec just needs to require the check.
- **Never rank people on unadjusted numbers.** Agents work different mixes of
  channel, queue and difficulty, so an unadjusted ranking substantially ranks their
  inbox. Either adjust for mix or report the metric without the ranking.
- **Suppress small cells at the spec's threshold**, and show that a cell was
  suppressed rather than omitting the row. A missing row reads as zero.
- **Separate "changed" from "notable".** Most sections of a recurring report have
  nothing to say most periods. Saying so is a feature; manufacturing a narrative to
  fill a heading is how these reports lose their audience.
- **Include a data-notes section** every period: what was late, what was
  suppressed, what was excluded, and any definition change. This is the section that
  makes the report trustworthy, and it is the first one people cut.

## Per-segment runs

A request for "the same report for each team" is one spec run N times, not N
reports. Two consequences worth stating to the user:

- **Multiplicity.** Run a 5% test across twelve teams and you should expect a
  "significant" movement somewhere every period by chance. If the report flags
  exceptions, either widen the threshold for the per-team version or say plainly
  that per-team flags are for looking at, not for acting on.
- **The totals will not be the sum of the parts** if any conversation touches two
  teams. Decide whether the org-level figure is computed independently or rolled up,
  put it in the spec, and expect someone to add up the teams and ask.

## Present results to the user

1. **The spec**, as a file they can keep, with its version.
2. **The report for this period**, in the spec's section order.
3. **Movement vs the comparison period**, with the noise check before the
   explanation.
4. **Data notes** — late data, suppressed cells, exclusions, definition changes.
5. **What changed about the spec**, if anything, and which historical periods are
   therefore not comparable.
6. **The command or prompt to re-run it next period**, so the next run is a
   parameter change rather than a rewrite.
