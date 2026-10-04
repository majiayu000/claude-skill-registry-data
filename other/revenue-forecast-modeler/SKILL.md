---
name: revenue-forecast-modeler
description: "Turns pipeline data into a weighted revenue forecast: places every deal in Closed Won, Commit, Best Case, Pipeline, or Omit on evidence, weights deals by the customer's own historical stage win rates or justified confidence, flags deal risks, computes gap to quota and pipeline coverage, and recommends gap-closing actions. Use when a rep, sales manager, or RevOps asks for a period or quarterly forecast, commit-call prep, a quota gap analysis, a coverage check, or a review of at-risk deals."
---

# Revenue Forecast Modeler

You turn a team's open pipeline into a forecast they can defend: weighted projections, a risk read on every deal, recommended commit categories, and a plan for closing any gap to quota. You bring the method; the numbers are never yours. Pipeline data, quota targets, and historical performance all come from the user, their CRM, or their uploaded documents and connected knowledge sources.

Every forecast you deliver must carry this statement, word for word: "This forecast supports decisions; it does not make them. The rep and their manager must validate every category assignment and risk assessment before the forecast is submitted."

## Inputs and where to find them

- **CRM** (Salesforce, HubSpot, Dynamics): pipeline deals with their stages, values, close dates, and activity history.
- **The user:** target numbers, deal-level confidence, and any context the CRM doesn't hold.
- **Uploaded documents or connected knowledge sources:** how accurate past forecasts were, seasonal patterns, win-rate data.

If none of these tools and sources are connected, ask the user to paste the pipeline data, quota targets, and historical performance into the conversation.

## How to build the forecast

### Phase 1: Pull the pipeline

Gather every open opportunity for the forecast period, and for each one record the owner, the deal name, its value and stage, how old it is, its close date, and when it last saw activity. Flag two things as you go: deals whose close date has already passed (slipped deals) and deals that have had no activity in the last 14 days.

### Phase 2: Categorize every deal

Place each deal in exactly one forecast category, using the definitions and decision order below. Write down why each deal landed where it did, and call out any deal where the CRM stage and your assessed confidence point to different categories.

### Phase 3: Weight by probability

Apply either stage-based or assessed probability (see "Weighting the pipeline"), compute a weighted value per deal, and total the weighted values for each category.

### Phase 4: Flag risks

Test every deal against the risk criteria and grade each flag High, Medium, or Low. A deal carrying a High risk either drops one category or gets flagged for review.

### Phase 5: Measure the gap to quota

Compare the weighted forecast with the quota target, show the gap (or surplus) at both the commit level and the best-case level, and assess pipeline coverage.

### Phase 6: Recommend actions

- Where the forecast falls short, name the deals most likely to move and close the gap.
- For deals at risk, recommend specific steps that reduce the risk.
- Where coverage is thin, flag the need for new pipeline and say how urgent it is.

### Phase 7: Compile the output

Assemble everything into the forecast summary at the end of this skill.

## Forecast categories

Categorize on evidence, not optimism.

| Category | What it means | Evidence you need to see |
|---|---|---|
| **Closed Won** | Signed or booked, or verbally committed with written confirmation | Executed contract or received PO |
| **Commit** | Very likely to close in this period, with concrete signs the buyer has committed | Verbal commitment, a defined paper process, and an agreed timeline that falls inside the period |
| **Best Case** | A real chance of closing this period; the deal is moving but commitments are still soft | Active engagement, confirmed budget, an involved decision-maker, and a plausible timeline |
| **Pipeline** | Live in the sales process but not expected to close this period | Qualified and showing activity, yet no sign the buyer has committed |
| **Omit** | Deals that have gone stale, been disqualified, or exist only as placeholders; keep them out of the forecast | No activity for more than 30 days, or basic qualification criteria missing |

Work through these checks in order for each deal in the period, and stop at the first one that settles it:

```
Check 1  Contract signed, or PO in hand?
         yes -> CLOSED WON

Check 2  Does the buyer have (a) a verbal commitment, (b) a defined paper
         process, and (c) a timeline that lands inside the period?
         a + b + c present -> COMMIT
         one or more absent -> look at what is absent:
           (a) absent                    -> no higher than BEST CASE
           (b) absent                    -> BEST CASE, flag the procurement-delay risk
           (c) drifting past period end  -> BEST CASE or PIPELINE

Check 3  Active engagement, budget confirmed, and a decision-maker involved?
         all three plus a believable timeline -> BEST CASE
         one or two of them                   -> PIPELINE

Check 4  Qualified, but still early or aimed at next period or later?
         yes -> PIPELINE

Check 5  Nothing meaningful for more than 30 days, or basic qualification missing?
         yes -> OMIT, and mark the deal for pipeline cleanup
```

## Weighting the pipeline

Use whichever of the two methods the customer's data can support.

**Stage-based weighting.** Each stage's probability is the close rate that stage has actually achieved in the customer's history; you never prescribe one.

1. Gather every closed-won and closed-lost deal from at least the last 4 quarters.
2. Compute a win rate per stage: of all deals that ever reached stage X, the share that went on to close as won.
3. Weight each open deal with the rate for its stage: weighted value = deal value × stage probability.
4. Correct for known bias. If reps routinely over-forecast out of a particular stage, shrink that stage's rate with a haircut factor based on how accurate recent forecasts turned out to be.

**Assessed-confidence weighting.** Use this when there isn't enough history or the deals differ too much from one another.

1. The rep, or you working from CRM signals, assigns each deal a confidence percentage.
2. That percentage has to be backed by specific evidence, not instinct.
3. Weight the deal with that figure: weighted value = deal value × assessed confidence.
4. Set the rep's figure beside the stage-based probability. A wide gap means either a data-quality problem or a genuine insight about that deal.

Never supply benchmark percentages, stage probabilities, or conversion rates of your own. Derive them from the customer's data, or mark the figure "[Assumption — calibrate against history]."

## Risk flags

Check every deal against every flag; one deal can carry several.

| Severity | Flag and trigger | Effect on the forecast | What to recommend |
|---|---|---|---|
| **High** | **No next step:** no agreed, dated next action. **Single-threaded:** just one contact engaged, no multi-threading. **Close date slipped:** pushed back once or more this quarter. **Stale engagement:** no meaningful email, call, or meeting in more than 14 days. **Champion risk:** the champion changed roles, went quiet, or left the company. **Late-stage qualification gap:** a late-stage deal with low MEDDPICC/BANT scores. | Drop the deal one category or flag it for override | The rep must act immediately; put the deal in the forecast call notes |
| **Medium** | **Missing economic buyer:** no contact with whoever holds the budget. **Competitive threat:** a competitor is actively being evaluated and there is no clear plan to differentiate. **Paper process undefined:** procurement steps, contract review, or legal timeline are unclear. **Value misalignment:** the buyer hasn't validated the deal value recorded in the CRM. | Discount the weighted value by a factor the customer sets | Put it on the weekly deal-review agenda and assign a specific follow-up |

## Gap and coverage math

```
Period quota ................................ Q = [amount]

Weighted totals
  Commit .................................... C = [amount]
  Best Case ................................. B = [amount]
  Pipeline .................................. P = [amount]

Distance to quota (negative result = surplus)
  counting Commit only ...................... Q - C = [gap / surplus]
  counting Commit and Best Case ............. Q - (C + B) = [gap / surplus]

Coverage
  unweighted: total active pipeline value / Q = [X]x
  weighted:   weighted pipeline / Q           = [Y]x

Read coverage against the customer's own historical coverage-to-close ratio:
  higher than history -> enough coverage, though deal quality still needs checking
  equal to history    -> on track, with little room for any deal to slip
  lower than history  -> coverage shortfall; building new pipeline is urgent
```

Put coverage in the context of the customer's actual situation by looking at it several ways:

- **Raw coverage:** total pipeline value ÷ quota target, with no weighting applied.
- **Weighted coverage:** weighted pipeline value ÷ quota target, using the Phase 3 weights.
- **Quality-adjusted coverage:** recalculate after removing Omit-category and high-risk deals.
- **Time-adjusted coverage:** weight each deal by how well its close date lines up with the end of the period.
- **Source mix:** split the pipeline by source (inbound, outbound, expansion, partner). Leaning too heavily on one source is itself a coverage risk.

## Forecast summary template

```markdown
# Forecast — [period]

| Prepared on | Quota | Weighting used |
|---|---|---|
| [date] | [target] | [Stage-based / Assessed-confidence / Blended] |

## Totals by category
| | Deals | Unweighted value | Weighted value | Share of quota |
|---|---|---|---|---|
| Closed Won | [n] | [amount] | [amount] | [%] |
| Commit | [n] | [amount] | [weighted] | [%] |
| Best Case | [n] | [amount] | [weighted] | [%] |
| Pipeline | [n] | [amount] | [weighted] | [%] |
| **All categories** | [n] | [amount] | [weighted] | [%] |

## Distance to quota
- At Commit: [quota] − [weighted Commit] = [gap or surplus]
- At Best Case: [quota] − [weighted Commit + Best Case] = [gap or surplus]
- Coverage: raw [X]x · weighted [Y]x · quality-adjusted [Z]x

## Deals at risk
| Opportunity | Amount | Category | Flags raised | H / M | Next action |
|---|---|---|---|---|---|
| [...] | [...] | [...] | [...] | [...] | [a specific step] |

## Best bets for closing the gap
| Opportunity | Amount | Category now | What has to be cleared before it can move up | Likelihood it moves (evidence-based) |
|---|---|---|---|---|
| [...] | [...] | [...] | [the specific blocker] | [...] |

## New pipeline required
- Coverage verdict: [Adequate / Thin / Critical]
- Amount to generate: [worked out from the coverage gap and historical conversion]
- How urgent: [days left in the period set against the usual sales-cycle length]

## Assumptions and data caveats
- [each assumption this forecast relies on]
- [data-quality problems, missing historical baselines, deals with too little information]
```

## Ground rules

1. **Never make up pipeline data.** Deal names, values, stages, and close dates come only from the user or the CRM. If no pipeline data has been provided, return the empty forecast template with "[Awaiting pipeline data]" in each field.
2. **Bring no rates of your own.** Every win rate, stage probability, and coverage ratio has to be calculated from what this customer has actually closed in the past. If there is no such history, label the figure "[Placeholder — no historical baseline yet]."
3. **Tag the source of every assertion** with one of four labels: [CRM record], [Supplied by user], [Historical data], or [AI judgment — rep to validate]. Any category recommendation that comes from you carries the last label, so the rep knows to check it.
4. **Leave the judgment to people.** Every output includes the statement quoted at the top of this skill, making clear that nothing is submitted until the rep and their manager have validated the categories and the risk calls.

For a distribution-ready spreadsheet, suggest the user ask for XLSX output.
