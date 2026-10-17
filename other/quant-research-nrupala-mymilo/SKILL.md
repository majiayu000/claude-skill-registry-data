---
name: quant-research
description: Research markets with statistical honesty — distributions, biases, data hygiene, and falsifiable hypotheses.
version: 1
triggers: quant, quantitative research, market research, statistical honesty, trading signals
category: Money & markets
blurb: Research markets with statistical honesty — clean data, bias control and falsifiable hypotheses.
archetype: knowledge
example: Design a quant study that doesn't fool itself.
---

# Quantitative Research

Markets are noisy, adversarial data generators. The job is not to find patterns — it is to avoid being fooled by them. Every result is a candidate for "noise until proven load-bearing".

## When to use
- Any data-driven market claim, screen, or strategy idea.
- Building datasets or features for research.
- Reviewing someone's "this indicator works" result.

## Method
1. **Hypothesis pre-registration**: write the hypothesis, the prediction, and the falsification test BEFORE looking at results.
2. **Data hygiene**: adjusted prices (splits/dividends) done correctly; delisted names retained (survivorship!); point-in-time fundamentals (no restatement peeking); timezone & timestamp discipline; document provenance + snapshot version.
3. **Distribution reality**: fat tails, volatility clustering, non-normality — don't assume Gaussian; correlations rise in crises (diversification fails exactly when needed).
4. **Stationarity skepticism**: regimes end; relationships decay; test stability across periods; prefer theories with a mechanism over curve fits without one.
5. **Multiple testing**: screens test thousands of things — the best of 10,000 random signals looks great; control for it (deflated significance awareness, holdout discipline).
6. **Costs from day one**: spreads, fees, slippage, borrow, taxes — a paper edge that dies after costs is not an edge.
7. **Reproducibility**: seeded runs, pinned data snapshots, versioned notebooks/scripts; results rerunnable by someone else (`data-ml-pipelines`).

## Quality gates
- [ ] Hypothesis + falsification written before analysis.
- [ ] Data provenance + adjustments documented; no survivorship gap.
- [ ] Multiple-testing controlled; stability checked across periods.
- [ ] Costs included; results reproducible from the snapshot.

## Red lines
- No result from one lucky sample; no "works since 2021" claims without regime context; no p-hacked screens presented as strategy.

## Related
`backtesting-validation` · `data-ml-pipelines` · `equity-fundamentals` (numbers over stories).
