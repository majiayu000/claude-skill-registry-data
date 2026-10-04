---
name: financial-planning
description: Build a grounded, verified long-horizon financial plan for a person - accumulation, financial-independence timing, drawdown, and the decision rules to run it by. Use this whenever someone asks when they can retire or go work-optional, wants a FIRE or retirement plan built or reviewed, brings a spreadsheet or planner document to audit, asks about safe withdrawal rates, savings schedules, drawdown strategy, or whether their money supports a life change (quitting, sabbatical, going independent, relocating). Trigger even for partial asks like "check my retirement math" or "how much do I need to leave my job" - the pieces need the whole model. Pairs with the life-paths skill (this skill prices a chosen life; that one chooses it), but runs fully standalone.
---

# Financial Planning

Produce a financial plan a careful skeptic would sign: every fact verified, every assumption named with its sensitivity, risk expressed as the spending floor the person would actually live on, and the whole thing operable through written decision rules rather than a one-time forecast.

## Why this skill exists

Self-built retirement models, including sophisticated ones with Monte Carlo engines and dynamic withdrawal rules, fail in recurring ways: spending targets that quietly contradict the person's actual spending, a single return assumption at the optimistic edge with no sensitivity shown, "100% success" claims that are true by construction because the model cuts spending instead of depleting, healthcare bridges and their tax interactions left unmodeled, horizons that stop at average life expectancy, and tax facts that were stale the year after they were typed. Professional plans fail differently: generic assumptions, no connection to the life actually being planned. This skill exists to produce the plan neither of those produces, and every stage below traces to one of those failures.

A third source of failure now has measurements: the unaided language model. Choukhmane, de Silva, Lin, and Akuzawa simulate lifetimes spent following LLM financial advice and find it anchors on heuristics (98.3% of withdrawal recommendations at or under the 4% rule, 31% of saving rates at multiples of 10%), advises where new savings go but almost never that existing holdings be rebalanced (recommended portfolios drift with market returns nearly one-for-one), cuts recommended spending in step with income after a job loss even when the buffer exists to absorb it, and over-saves so consistently that fitting the advice to a life cycle model needs a discount factor above one ("AI Financial Advice: Supply, Demand, and Life Cycle Implications", working paper, 2026, https://doi.org/10.2139/ssrn.6446286). Their structured-prompt benchmark, which hands the model full financial state and explicit assumptions, reduces the heuristic reliance but not the drift; that benchmark is intake and the registers in miniature, and it is why the stages below carry the target-allocation, withdrawal-derivation, and income-interruption items as requirements rather than reminders. The paper's findings are distilled, with exact magnitudes and figure anchors, in `references/llm-advice.md`; read it when the red team or the deliverable needs the measured numbers rather than this summary.

## Core principles

- **Verified beats recalled.** Any fact that changes or varies by jurisdiction (contribution limits, tax brackets, benefit ages and formulas, healthcare rules) gets checked by web search at plan time and logged with source and date. A plan resting on remembered numbers is wrong on arrival or wrong within a year; the verified-facts register (see `references/verification.md`) is what separates this plan from the one it replaces.
- **Actuals beat estimates.** Spending comes from statements and exports wherever they exist. The gap between what people say they spend and what they spend is the single most common silent error, and it propagates into every headline number.
- **Sensitivity is a first-class result.** Never present one future. The deliverable's headline is a range with the assumptions that move it, and the return assumption always appears at the user's value and at least two more conservative values.
- **The floor is the risk metric.** For any plan with adaptive spending, report the 10th-percentile lifetime spending and the worst pre-benefit stretch, judged against the person's actual lifestyle. Survival percentages are reported but never headlined.
- **A plan is a document plus decision rules.** The forecast will be wrong; the plan should say, in observable if-then form, what to do when it is. Deliverable structure in `references/deliverable.md`.
- **The model serves a life.** Income phases, exits, sabbaticals, part-time years, and lumpy expenses come from the life being planned. When a `life-paths` workspace exists, consume its chosen path and finances files as input; when standalone, elicit the life shape in intake. If the person has not actually chosen what life they are financing and the conversation keeps sliding into "but what should I do," that is the life-paths skill's job; suggest it once and continue with the shape they give you.

## Code policy

The bundled `scripts/simcore.py` is scaffolding: tested primitives (return generators, a ledger engine, spending policies, summarizers), not a finished model. Plan-specific logic - the person's phases, their tax buckets, their jurisdiction's interactions - is written on the fly per run, composed from the scaffolding. This is deliberate: a fixed model flexible enough for every household would be a config language nobody can audit; small bespoke code on tested primitives is both flexible and checkable.

The rule that makes on-the-fly code safe: any bespoke module gets its own tests before its outputs are trusted, at minimum a zero-volatility analytic case (returns fixed, arithmetic checkable by hand) and a conservation check (wealth change equals returns plus flows). Run the scaffolding's own suite once per run (`python3 -m unittest discover tests`) so a modified environment fails loudly. Numbers from untested code do not enter the deliverable.

## Workspace

Default `./financial-plan-workspace/` (or the life-paths workspace's `finances/` directory when running as part of that flow):

```
financial-plan-workspace/
  intake.md            - situation, life shape, jurisdiction, data provenance
  facts.md             - verified-facts register (fact, value, source, date)
  assumptions.md       - assumptions register (value, basis, sensitivity)
  data/                - spending actuals, historical return series (with source)
  model/               - bespoke run code and its tests
  results/             - simulation outputs
  FINANCIAL_PLAN.md    - the deliverable
  notes.md             - open questions, where you left off
```

These files are the stages' exit artifacts, and the deliverable is assembled from them section by section, never from memory of the run - that is what makes a skipped stage visible instead of silently absorbed. A document section with no file behind it has two honest continuations, run the stage or name the gap in the deliverable's limitations section, and no third. When the ask is small and the full flow would be disproportionate, shrink each file's depth (fewer scenarios, coarser tax treatment, estimate-grade inputs so labeled) rather than dropping files: a small plan and a large one differ in resolution, not in which disciplines quietly lapsed.

## Stages

Read each reference when its stage begins, even if it was skimmed up front. The reason is mechanical: a requirement shapes an artifact only if it is in context when the artifact is written, and by the later stages an up-front skim is dozens of tool calls in the past. What that distance loses is exactly the specific, checkable requirements - the memorable principles survive on their own; the specifics do not.

1. **Intake** - situation, actuals, accounts, the life shape being priced, jurisdiction. Interactive. Read `references/intake.md`.
2. **Fact verification** - search-verify everything jurisdiction- or year-dependent; build the register. Read `references/verification.md`.
3. **Modeling** - compose the model from scaffolding plus tested bespoke code; obtain historical return data with provenance. Read `references/modeling.md`.
4. **Stress and sensitivity** - the sensitivity matrix, historical sequences, named stress scenarios, floor analysis. Read `references/stress-and-sensitivity.md`.
5. **Draft and red team** - assemble the draft `FINANCIAL_PLAN.md` from the workspace files, then a fresh-context auditor agent tries to break it; findings get fixed, sensitized, or documented. Read `references/deliverable.md` for the draft, then `references/red-team.md`.
6. **Delivery** - apply the triaged findings, finalize `FINANCIAL_PLAN.md`, walk the person through the headline range and the decision rules. Presentation guidance is in `references/deliverable.md`.

Stage 1 is a conversation (small question batches, end turns). Stages 2-5 run autonomously once inputs are confirmed; announce the handoff. If the person brought an existing model, stages 2-5 double as its audit: reproduce its headline first so you know you understand it, then improve on it, and report the differences explicitly - people trust a critique of their model far more when you have first shown you can reproduce it.

## Boundaries

This is educational modeling, not licensed financial advice; say so once, where the stakes justify it, and include the professional-handoff questions in the deliverable rather than repeating disclaimers. Do not recommend specific securities or products. If intake surfaces acute financial distress (imminent insolvency, debt crisis), the long-horizon plan is the wrong tool; deal with the near term plainly and offer to return to planning later.
