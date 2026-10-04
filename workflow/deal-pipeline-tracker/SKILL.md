---
name: deal-pipeline-tracker
description: Runs origination as a managed funnel with stage criteria, cohort conversion, and capacity limits when you need a pipeline that forecasts rather than a list that flatters.
---

# Deal Pipeline Tracker Agent

## When to use
Use this when origination is run off a list of names and nobody can say what will close. Typical triggers: a partner asking whether the year's target is reachable, a review where every opportunity is somehow still active, or a team fully occupied and closing nothing. Reach for it when the question is not which deals are live but how many will land and whether the team can carry them.

## What it does
It produces a managed pipeline: stage definitions with objective entry criteria, cohort conversion between stages, the top-of-funnel volume implied by the closing target, work-in-progress limits set against real capacity, staleness rules, and a weighted forecast reconciled to what closed.

## Method
1. Define the stages MECE. One opportunity, one stage, no overlaps.
   - Mapped, contacted, qualified, engaged under NDA, indication submitted, exclusivity, signed, closed — with passed, lost, and watchlist as terminal states.

2. Make each entry criterion an observable event. Not a feeling.
   - "Owner agreed a second meeting and sent revenue" is a criterion; "warm" is not. If two people would stage the same deal differently, the definition is not written yet.

3. Give every opportunity an owner and a dated next step.
   - A live opportunity with no date on its next action is not live, and that one field catches most of what a pipeline review would otherwise miss.

4. Measure conversion by cohort, not snapshot.
   - Follow the deals that entered a stage in one period through to their outcome; a snapshot ratio flatters whenever the top of the funnel is growing.

5. Back-solve the top of the funnel from the closing target.
   - Multiply the stage conversions into a cumulative rate, divide the target by it, and test the answer against the contacts the team can actually make in a week.

6. Set work-in-progress limits against real capacity. Use Little's Law.
   - Work in progress equals throughput times cycle time: deals entering a stage each year times the months they sit there gives the concurrent load to set against the number of teams.
   - When it says the constraint is capacity, more origination makes the numbers worse, not better.

7. Kill or park the stale ones. Carrying them is not free.
   - Flag anything past 1.5x the median time in its stage or lacking a dated next step, then move it to the watchlist with a re-approach date rather than leave it in the count.

8. Report a weighted forecast and reconcile it. Adjust the rates, not the story.
   - Weight each opportunity by its stage's cumulative probability of closing, then compare last period's forecast against what closed and re-cut the conversions.

## Inputs
- The closing target for the period and the fee or capital per closing
- The opportunity list with stage, owner, and last action date
- Historic outcomes for at least two years of cohorts
- Median time in stage, by stage
- The number of deal teams and what one live process consumes
- Screening criteria, so a mis-fit is passed rather than staged

## Output format
- Stage definitions, each with its entry criterion stated as an observable event
- Stage-to-stage conversion by cohort, naming the period measured
- The implied top of funnel: qualified opportunities and contacts needed per period
- A capacity section applying Little's Law, stating concurrent load against teams
- A staleness list naming what to kill, park, or restart, with dates
- A weighted forecast in expected closings, reconciled to the prior period
- Present the pipeline and its metrics in prose, never as markdown tables

## Example
For Ardsley Partners (fictional, illustrative), a mid-market desk targeting three closings a year: trailing cohorts convert qualified to engaged at 40 percent, engaged to indication at 50, indication to exclusivity at 25, exclusivity to signed at 70, and signed to closed at 90 — a cumulative 3.15 percent. Three closings therefore need 95 qualified opportunities a year and, at 30 percent qualification, 317 contacts, or six a week. Little's Law then binds: 4.8 deals must enter exclusivity a year, each holding a team for four months, a concurrent load of 1.6 against two teams. The active list of 41 — 24 qualified, nine engaged, five at indication, two in exclusivity, one signed — weights to 4.41 expected closings; stripping the 12 with no dated next step, eight qualified and four engaged, leaves 29 and 3.85. The forecast fell by 0.57 and the outcome by nothing: against a target of three, the binding constraint was never origination.
