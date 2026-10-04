---
name: value-creation-plan
description: Use when the user needs to turn a diligence finding, investment thesis, strategic priority, acquisition, or transformation ambition into an accountable value creation plan. Triggers include post-acquisition plans, 100-day plans, synergy plans, value creation theses, initiative portfolios, benefit tracking, investor updates, operating plans, and execution roadmaps.
---

# Value Creation Plan

Turn a strategic or investment thesis into a small, owned portfolio of initiatives that delivers measurable value. Use it after commercial due diligence, a strategy review, an acquisition, or a transformation diagnosis.

## Reference Loading

Read `references/value-plan-artifacts.md` when building an initiative portfolio, financial bridge, 100-day plan, benefits tracker, governance cadence, or investor/board progress update.

## First Frame

Start with the decision context, then distinguish three things that are frequently conflated:

1. Value potential: the directional upside if every relevant lever works.
2. Underwritten plan: the portion supported by a named owner, baseline, mechanism, investment, and timing.
3. Realized value: finance-validated results after implementation, not pipeline or activity.

The plan should answer: which 3-5 moves matter most, how they change revenue, margin, cash, or risk, who owns each move, and what evidence would cause the plan to change.

## Workflow

1. Set the value ambition.
   - State the enterprise objective, time horizon, and value metric: revenue, EBITDA, cash, working capital, risk reduction, or capacity.
   - Define the baseline, including period, scope, currency, and source.
   - Identify the executive sponsor and finance partner.

2. Convert the thesis into a value tree.
   - Translate findings into operational levers such as pricing, sales coverage, retention, procurement, cost-to-serve, footprint, working capital, or product mix.
   - Explain the causal mechanism from action to financial outcome.
   - Eliminate initiatives that do not have a credible mechanism or a measurable metric.

3. Prioritize an initiative portfolio.
   - Score each initiative for value, confidence, time-to-impact, execution complexity, investment, and dependency risk.
   - Select a focused portfolio of 3-5 initiatives; keep additional ideas in a separately labelled backlog.
   - Assign a single accountable executive owner and a delivery lead to every selected initiative.

4. Underwrite the benefits.
   - Build a financial bridge from baseline to expected outcome.
   - Show gross benefit, one-off cost, recurring run cost, disbenefits, and net value separately.
   - Label every assumption as validated, directional, or untested, and define the test that would upgrade it.

5. Sequence the 100-day plan.
   - Days 0-30: validate the baseline, confirm owners, remove critical blockers, and launch no-regret actions.
   - Days 31-60: pilot or implement the most important levers; collect leading indicators and revise assumptions.
   - Days 61-100: scale proven interventions, lock operating routines, and approve the next-wave plan.
   - Separate actions required to learn from actions required to capture value.

6. Establish the execution system.
   - Run a weekly initiative review for milestones, decisions, and blockers.
   - Run a monthly value review with finance to validate benefit attribution and forecast changes.
   - Escalate material dependencies, missed milestones, and red-flag assumptions to the sponsor promptly.

7. Produce the decision-ready plan.
   - Lead with the value thesis and the 3-5 priority initiatives.
   - Make the bridge, owners, timing, dependencies, risks, and confidence visible.
   - State the next decision required from the executive team, board, or investment committee.

## Initiative Prioritization

Score each dimension from 1 (weak) to 5 (strong):

| Dimension | What to test |
| --- | --- |
| Net value | Material, measurable value after required costs |
| Confidence | Evidence quality and reliability of assumptions |
| Time-to-impact | Time until value is visible in an agreed metric |
| Controllability | The team can influence the outcome directly |
| Execution readiness | Owner, capability, data, and dependencies are workable |
| Strategic fit | Supports the investment or enterprise thesis |

Do not treat the total score as a mechanical answer. A high-value initiative with low confidence may merit a short validation sprint; a high-confidence initiative with low value should not crowd out a material lever.

## Output Templates

### Value Creation Thesis

```markdown
## Value Creation Thesis
Objective: <outcome, scope, and horizon>
Baseline: <metric, period, source, and finance owner>
Target: <net value and timing>

The plan will create value primarily through:
1. <initiative and causal mechanism>
2. <initiative and causal mechanism>
3. <initiative and causal mechanism>

Critical assumptions: <assumptions that could materially change the plan>
Decision required: <approval, resource, or escalation>
```

### Initiative Card

| Field | Content |
| --- | --- |
| Initiative | <clear action-oriented name> |
| Value mechanism | <how the action changes a financial or risk metric> |
| Net annual run-rate | <annual gross benefit - recurring cost/disbenefit; show probability separately> |
| One-off cash and in-year value | <one-off cost; phased year-one benefit/cash on an explicit timeline> |
| Confidence | <validated / directional / untested> |
| Accountable owner | <executive owner> |
| Delivery lead | <day-to-day lead> |
| Milestone | <specific outcome and date> |
| Dependencies | <decisions, systems, people, or vendors> |
| Leading indicator | <measure that precedes financial value> |
| Red flag | <trigger that causes review or stop> |

### Benefits Tracker

| Initiative | Baseline | Gross benefit | Cost to achieve | Net value | Timing | Confidence | Finance status |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| <initiative> |  |  |  |  |  |  | <unreviewed / forecast / validated / realized> |

### 100-Day Plan

| Phase | Outcomes | Critical actions | Owner | Decision or dependency | Evidence of progress |
| --- | --- | --- | --- | --- | --- |
| Days 0-30 | Baseline and plan validated |  |  |  |  |
| Days 31-60 | Priority levers in market or implementation |  |  |  |  |
| Days 61-100 | Proven levers scaled and operating routines locked |  |  |  |  |

### Executive Value Review

```markdown
## Headline
<value forecast versus plan, and the one decision or risk that matters most>

## Portfolio Status
| Initiative | Status | Net value forecast | Change since last review | Decision / escalation |
| --- | --- | ---: | --- | --- |

## Value Bridge
<baseline -> initiatives -> costs -> revised value forecast>

## Assumptions at Risk
| Assumption | Evidence | Impact if wrong | Owner | Next test |
| --- | --- | --- | --- | --- |
```

## Guardrails

- Do not represent value potential as realized results; retain the confidence and finance-status labels throughout the output.
- Use a defined baseline and avoid double-counting benefits across initiatives, functions, or acquisitions.
- Do not deduct one-off costs from recurring annual run-rate or call a full-year run-rate a first-year result; show implementation timing and cash separately.
- Treat revenue as value only when its incremental margin, cost-to-serve, and likelihood of realization have been considered.
- Do not recommend cost actions that bypass safety, legal, regulatory, customer, labor, or contractual obligations.
- Keep client, target, employee, and transaction information confidential; use anonymized placeholders unless the user has provided authorized data.
- Surface tradeoffs explicitly: a plan that raises near-term EBITDA while damaging retention, quality, resilience, or strategic capability requires a stated decision.
