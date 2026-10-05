---
name: investment-journal-review
description: Review one completed investment/trade or a journal of many decisions while preserving the original plan, separating process quality from profit/loss, testing thesis and forecast accuracy, identifying repeated evidence/sizing/execution errors, and proposing one or two measurable improvements. Use for post-trade reviews, recommendation scorecards, “why did this lose”, “what am I doing wrong”, and Turkish intents such as “işlem günlüğümü analiz et”, “işlem sonrası analiz”, “tahminlerin ne kadar tuttu”, “zararımdan ders çıkar”, “geçmiş al-satları incele”. Do not rewrite the original plan with hindsight or infer a stable edge from a small sample.
---

# Investment Journal Review

Own learning after a decision. Support two modes: a single-decision postmortem and a multi-decision pattern review. Never judge process solely from P&L.

Read [references/journal-protocol.md](references/journal-protocol.md). Use `scripts/journal_metrics.py` for a normalized trade CSV when available. Use `$probabilistic-market-forecast` scoring for matured probability records and `$investment-thesis-tracker` for evidence deltas.

## Workflow

1. **Freeze provenance.** Preserve the original timestamped thesis, evidence cutoff, forecast, entry/exit plan, size, loss limit and any amendments. Never edit the old record; append review fields.
2. **Reconstruct execution.** Record actual entry/exit, fees, spread/slippage, partial fills, holding time, deviations and whether the planned invalidation or review rule was observable.
3. **Separate four outcomes.** Classify good process/good outcome, good process/bad outcome, bad process/good outcome and bad process/bad outcome. Luck does not repair a broken process; a valid process can lose.
4. **Score the forecast.** When a probability or interval matured, compare the frozen forecast with the realized outcome and a declared naive/market benchmark. Preserve unresolved or early-closed cases separately.
5. **Diagnose cause.** Distinguish research/evidence, thesis, timing, sizing, portfolio concentration, product mechanics, execution, discipline and unforeseeable shock. Avoid vague labels such as “emotion” without observable behavior.
6. **Analyze patterns.** Normalize P&L by planned risk (`R`) and segment only when sample size permits. Compare repeated errors, regime, horizon, strategy and instrument; report missing data and selection bias.
7. **Change little.** Recommend at most one or two falsifiable process changes for the next sample, with a measurement and review date. Do not optimize rules to explain the past perfectly.

## Hard rules

- Never use later information to claim it should have been known at the original cutoff.
- Never celebrate a rule-breaking winner as a good decision.
- Never infer skill from a handful of trades, one regime or selected successes.
- Include costs, abandoned ideas and no-trade decisions when available; survivor-only journals overstate quality.
- Do not respond to losses by automatically increasing risk, leverage or trading frequency.

## Output

For one decision: original plan, evidence available then, execution delta, process/outcome quadrant, forecast score, cause, retained lesson and one next experiment.

For a journal: coverage/sample warnings, expectancy in R, win/loss distribution, drawdown, process adherence, forecast calibration when available, recurring strengths/errors, regime dependence and one or two measurable changes.
