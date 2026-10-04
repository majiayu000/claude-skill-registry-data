---
name: analyze-stock-decision
description: Combine point-in-time equity data, deterministic factor/risk calculations, sourced business evidence, and explicit AI causal reasoning to produce conditional entry, hold, reduce, exit, stop, and time-exit judgments for 20-, 60-, or 120-session horizons. Use when Codex is asked to assess a stock or equity universe, compare candidates, propose price-conditioned buy or sell timing, balance quantitative signals against a reasoned business outlook, size hypothetical risk, backtest a factor workflow, or explain why an AI judgment differs from the mechanical model. For Korean equities, consider using collect-factchart-data during discovery to map disclosures, news, hard-to-find company details, and candidate peers before verifying material claims with primary sources. Require fresh point-in-time evidence and never present the result as individualized investment advice or a guaranteed forecast.
---

# Analyze Stock Decision

Produce a mechanical baseline, a sourced AI reasoning outlook, and a final conditional judgment. Use calculation as one evidence axis and risk-control tool, not as the sole decision-maker. Treat every conclusion as falsifiable research, never as a guaranteed forecast or automatic order.

## Core workflow

1. Fix `as_of`, exchange/timezone, 20/60/120-session horizon, benchmark, sector peers, investable universe, and `position_state` (`flat` or `held`).
2. Read [references/data-contract.md](references/data-contract.md) and [references/research-discipline.md](references/research-discipline.md) before collecting or transforming data.
3. If the target is listed in Korea or the request concerns Korean equities, consider invoking `$collect-factchart-data` before broad research. Require its documented `factchart-handoff/1.0` object; consume `instrument`, `retrieval`, `quality`, `discovery`, and `downstream` rather than guessing from an ad hoc payload. Use its validated output as a discovery map to surface recent disclosure identifiers and types, repeated or contradictory news themes, hard-to-find company or financial fields, unusual data gaps, and broad-sector comparison candidates. Convert those findings into a prioritized follow-up queue for DART filings, KRX records, issuer IR, earnings releases or presentations, call materials, regulatory sources, and original articles. Read that skill and its required references before access, respect its authorization and quality gates, and retain its retrieval and freshness ledger in the research record. Treat every unverified FactChart item as an `aggregator / screening` lead rather than a confirmed fact. Let such leads guide search priority and provisional hypotheses, while reserving decision weight for evidence appropriate to its materiality. Treat its comparison group as a peer longlist only; qualify actual peers by business model, revenue drivers, customers, geography, accounting basis, and horizon relevance. Import into the engine only fields explicitly listed in `downstream.engine_eligible_fields`; do not use FactChart prices as the engine's adjusted OHLCV ledger or provider-defined metrics as model inputs until their periods, formulas, units, and primary-source values are verified. If the source is unavailable, unsupported, stale, outside the authorized scope, or unlikely to add value, proceed without it; do not let the optional discovery step block the analysis.
4. Collect only information available by `as_of`. Prefer filings, exchange/regulator data, company IR, and licensed point-in-time market/estimate data. Browse for fresh data whenever the request concerns the current market. Verify material and decision-critical FactChart leads against dated primary sources when reasonably available. Keep noncritical or not-yet-verified leads in a separate discovery ledger with their source, date, definition limits, and confidence; they may shape follow-up questions and a provisional outlook but must not be restated as confirmed facts. Preserve FactChart provenance when it materially shaped what was searched.
5. Structure business and catalyst claims using [references/business-evidence.md](references/business-evidence.md). Preserve supporting and contradicting evidence. Grade the research environment A/B/C and label material statements as fact, calculation, estimate, assumption, judgment, or unknown; never confuse abundant coverage with investment certainty.
6. Reconcile critical financial inputs with at least two genuinely independent source or calculation clusters when available. Use `scripts/financial_rigor.py` for market-cap identity, ratios, pairwise source differences, scenario valuation, and a structured critical-figure ledger. Resolve accounting definition, period, currency, unit scale, and share basis before averaging or scoring; a breached tolerance that could indicate a unit or point-in-time error blocks execution.
7. Validate timestamps, adjusted-price consistency, universe membership, staleness, liquidity, and coverage. Supply at least five contemporaneous securities for relative ranking; a single-stock payload is not a valid ranking universe. Classify thin peer coverage as `PARTIAL_DATA` and block only the mechanical/execution decision. Return `INSUFFICIENT_DATA` or `STALE_DATA` for true integrity failures, but still produce an explicitly limited research outlook whenever sourced business evidence remains usable.
8. Run the deterministic engine:

   ```text
   python scripts/stock_decision_engine.py analyze INPUT.json --output RESULT.json
   ```

9. Label the engine action and score as the `mechanical baseline`, not the final recommendation. Read [references/methodology.md](references/methodology.md) when explaining, reviewing, or changing calculations.
10. Read [references/reasoning-policy.md](references/reasoning-policy.md). Build an independent causal outlook from business trajectory, expectations, catalyst path, durability, market context, downside asymmetry, and a serious counter-thesis.
11. For a held position, post-earnings update, material news event, or comparison with an earlier report, read [references/thesis-monitoring.md](references/thesis-monitoring.md). Compare the dated baseline assumption by assumption and classify changes as fact, valuation, wording, or data quality before changing the thesis.
12. Apply [references/decision-policy.md](references/decision-policy.md). Let the AI final judgment agree with, weaken, strengthen, or oppose the mechanical baseline when the sourced reasoning is more decision-relevant for the selected horizon. Preserve any divergence explicitly.
13. Draft the user-facing conclusion with the AI research outlook first, independent of whether execution is blocked. Record `research_status`, `execution_status`, reasoning tilt, conclusion, and limitations separately from the mechanical action. When point-in-time fundamentals support it, infer a sourced bear/base/bull fair-value range with explicit method, horizon, assumptions, confidence, contradictions, and invalidations; keep it separate from engine execution targets. When evidence cannot support a defensible range, record fair value as unavailable rather than inventing one. For a visual report or durable artifact, read [references/insights-contract.md](references/insights-contract.md), save the synchronized synthesis and fair-value analysis as `INSIGHTS.json`, then follow [references/visualization.md](references/visualization.md).
14. For simulations, calibration, or model promotion, read [references/validation.md](references/validation.md) and run the relevant engine command.
15. Cite source URLs beside time-sensitive claims and name the observation date. Distinguish facts, calculations, estimates, assumptions, judgments, and unknowns.

## Proportional verification policy

Apply verification effort according to materiality and use:

- Use discovery leads, including single-source or aggregator observations, to expand the search space, find overlooked events, and form tentative hypotheses. Label them clearly; do not require primary-source confirmation merely to retain them as leads.
- Use credible but imperfect secondary evidence as supporting context when primary material is unavailable or disproportionate to obtain. Reduce confidence, expose the gap, and seek contradiction rather than discarding the evidence automatically.
- Seek primary evidence and an independent check for claims that materially change the causal thesis, fair-value range, or final judgment. When that check is unavailable, prefer a conditional conclusion, wider scenario range, or `UNKNOWN` label over an automatic research veto.
- Require strict reconciliation for execution-critical and integrity-critical inputs: instrument identity, point-in-time availability, price adjustment, currency, unit scale, share basis, and the values needed to define executable risk. Reserve hard blocks for failures that can make the instrument, timestamp, calculation, or risk level materially wrong.
- Treat incomplete corroboration as uncertainty, not as negative evidence. Lower confidence, reduce hypothetical risk, tighten monitoring conditions, or keep the result research-only before defaulting to `NO_DECISION`.
- Match effort to the selected horizon and expected decision impact. Do not spend equal verification effort on every background detail, and do not let a low-impact unresolved field dominate stronger, more direct evidence.

## Non-negotiable rules

- Use `available_at <= as_of`; do not substitute period end, latest restatement, or retrieval time.
- Keep research-environment grade separate from investment certainty. Sparse evidence lowers what can be claimed; abundant coverage does not prove a durable business or an information edge.
- Reconcile decision-critical financial figures by definition, period, currency, scale, and share basis. Two articles repeating one filing are one source cluster, not independent confirmation.
- For Korean equities, use FactChart to expand discovery and prioritize primary-source research, never to replace DART, KRX, issuer IR, verified market data, or independent peer qualification. Keep unverified provider fields, news sentiment, disclosure reactions, and broad-sector candidates out of the engine; they may inform explicitly provisional hypotheses but not confirmed facts or execution-critical conclusions.
- Treat a structured numeric audit as an arithmetic and consistency check only. It does not prove source truth, independence, or point-in-time availability.
- Use a contemporaneous universe including delisted securities for historical tests.
- Align stock and benchmark returns by exact exchange session date; never align unequal histories only by array position.
- Generate signals on adjusted prices but express executable levels on internally consistent raw prices.
- Do not turn missing values into neutral zeros. Reweight available factors, disclose coverage, and block the mechanical/execution decision below the configured threshold. Do not suppress the separate AI research outlook or fair-value analysis when their own evidence is sufficient.
- Do not call a 0–100 score a probability. Emit probability only from frozen, expanding-window out-of-sample calibration with reported Brier score and sample size.
- Use a calibrated probability in expected-value math only when its target exactly matches the traded barrier event. A probability of positive horizon return is not a probability of reaching +2R before -1R.
- Do not mechanically copy the engine action into the final conclusion. Produce an independent reasoning outlook before choosing the final judgment.
- Do not use a fixed arithmetic weight between model and reasoning. Weigh horizon relevance, causal directness, source quality, freshness, independence, durability, expectation gap, and downside asymmetry.
- Permit a bullish or bearish reasoning tilt, including a conclusion opposite to the model, only when the causal chain, supporting evidence, counterevidence, assumptions, and model blind spot are explicit.
- Never override data-integrity gates: future/unavailable information, corrupted or internally inconsistent prices, unverifiable point-in-time availability, or missing inputs needed to define executable risk. Treat missing peer ranks and sub-threshold relative-factor coverage as model limitations, not as proof that every research layer is invalid.
- Treat policy and execution constraints as reviewable rather than absolute when appropriate. AI may conditionally override regime, stop-width, liquidity-threshold, or model-EV vetoes only by naming the reason, sizing/execution compensation, remaining risk, and cancellation condition. Do not move a defensible stop closer merely to justify the override.
- Never hide disagreement by editing the engine score or levels. Show the mechanical baseline, reasoning outlook, final judgment, and divergence reason separately.
- Never present an AI-inferred fair value as a calibrated probability, guaranteed target, or executable order level. Store its method, scenario assumptions, evidence references, confidence, and caveats; keep it visibly separate from entry, stop, no-chase, and +1.5R/+2.5R execution targets.
- Do not claim an exact future buy or sell date. Give the earliest valid session plus a conditional price zone/trigger, cancellation conditions, and a latest review or time-exit session.
- Do not use universal ROE, margin, P/E, or leverage thresholds as proof across sectors. Treat simple cutoffs as screening prompts and use sector-aware, full-cycle evidence.
- For a held-position update, do not treat price movement or rewritten prose as thesis drift. Name the new fact, valuation input, or data-quality correction that changed the conclusion.
- Treat ATR, stops, and volatility scaling as risk controls, not alpha signals. Never widen a long-position stop after entry.
- Treat market regime as an exposure overlay. Do not double-count it as a company alpha factor.
- Flag a defensible stop wider than the default risk limit as a reviewable constraint. Honor it by default; override only with smaller risk, explicit controls, and residual-risk disclosure. Never pull the stop closer merely to increase position size.
- When building a dashboard, use only the matching point-in-time input and engine result. Never hand-edit levels, conceal integrity gates or reviewable constraints, or make an integrity-blocked assessment look actionable.
- Keep an optional dashboard synchronized with the response through `INSIGHTS.json`; do not drop material support, contradictions, thresholds, or limitations.
- Mention gap/slippage, tax, currency, liquidity, corporate-action, and event risks relevant to the instrument.
- Never place an order or imply guaranteed execution.

## Data collection minimum

Gather these layers in proportion to decision relevance and reasonable availability, with provenance for every collected layer. Treat a missing noncritical layer as a coverage or confidence limitation; block only when a required engine/execution input is missing or an integrity failure makes the result materially unreliable:

- Daily adjusted OHLCV: target, broad benchmark, and peers; target at least 253 valid sessions. Add a sector benchmark as supplementary context when reliable point-in-time history exists.
- Point-in-time fundamentals: current and prior comparable periods, filing/availability timestamps, market cap, enterprise value, shares, and cash-flow items.
- Critical-figure audit: market-cap identity, at least two independent clusters for decision-critical statement figures when available, explicit metric definitions, field-specific tolerances, and unresolved differences.
- Point-in-time expectations: actual/consensus EPS surprise, 60-day consensus revision, and up/down revision breadth.
- Business evidence: guidance, unit economics or operating KPI, capital allocation, product/regulatory events, competitive changes, management commitment delivery, footnote or accounting-definition changes, and explicit thesis invalidations.
- Korean-equity discovery when useful: a FactChart retrieval/freshness record, recent disclosure and news-theme map, hard-to-find field and inconsistency list, broad-sector peer longlist, and a primary-source verification queue.
- Risk/execution: average dollar/share volume, spread or conservative cost assumption, corporate actions, event calendar, currency, and exchange calendar.
- Market overlay: benchmark trend and volatility plus universe breadth; add credit/liquidity stress only when vintage-safe data exist.

Analyst estimates are optional. If unavailable, reduce earnings-factor coverage and confidence; never fabricate them. Read [references/source-catalog.md](references/source-catalog.md) for source choices and research provenance.

## Engine use

Preflight critical figures and assumption-dependent valuation when the necessary raw inputs exist:

```text
python scripts/financial_rigor.py verify-market-cap --price "510" --shares "9.11e9" --reported "4.65e12" --currency HKD --tolerance-pct "1"
python scripts/financial_rigor.py audit-ledger --ledger critical-figures.json --output audit-result.json
python scripts/financial_rigor.py scenario-valuation --price "100" --eps "5" --years 3 --discount-rate "0.10" --scenarios scenarios.json --output valuation.json
```

Review exit code `2` means arithmetic or source agreement requires reconciliation. Do not continue to an actionable result merely because one aggregator looks plausible.

Generate and analyze synthetic data to verify the local runtime:

```text
python scripts/stock_decision_engine.py demo --output demo-input.json
python scripts/stock_decision_engine.py analyze demo-input.json --output demo-result.json
```

Backtest a point-in-time feature panel:

```text
python scripts/stock_decision_engine.py backtest panel.csv --horizon 60 --cost-bps 20 --output metrics.json
```

Fit leakage-safe one-dimensional score calibration only after a sufficient time-ordered panel exists:

```text
python scripts/stock_decision_engine.py calibrate panel.csv --horizon 60 --min-train-dates 24 --universe-id US-LARGE-MID-v1 --output calibration.json
```

Treat default weights and thresholds as preregistration-friendly starting priors, not discovered truths. Change them only inside a declared training/validation window and record every attempted specification.

## Optional visual report

When a visual artifact is requested or materially useful, validate the result, draft `INSIGHTS.json`, then generate and capture the decision-room report:

```text
python scripts/render_trade_dashboard.py INPUT.json RESULT.json --print-result-sha256
python scripts/render_trade_dashboard.py INPUT.json RESULT.json --ticker TICKER --insights INSIGHTS.json --locale en --output TICKER-dashboard.html
node scripts/capture_dashboard.cjs TICKER-dashboard.html TICKER-dashboard.png
```

Copy the printed fingerprint and the exact engine binding fields into the schema 1.3 insight artifact, including separate research/execution statuses and the sourced fair-value analysis or an explicit unavailable reason. Regenerate the insight artifact after any engine rerun; do not reuse same-date narrative against a changed result.

Use `--locale ko` for a Korean response. Follow [references/visualization.md](references/visualization.md) for runtime fallback, integrity checks, visual preflight, comparison limits, and final artifact placement. The HTML is the complete interactive and auditable report; the PNG is its inline preview. Do not use Mermaid as the primary financial chart.

## Final response contract

Lead with `as_of`, research status, research-environment grade, AI outlook, execution status, mechanical status, horizon, evidence confidence, critical-number audit status, and whether a calibrated probability exists. Never let `NO_DECISION` hide an otherwise supportable research conclusion. Then give:

1. AI-inferred fair value near the top when defensible: bear/base/bull prices, observed price, horizon, method, confidence, scenario rationale, source references, assumptions, and caveats. Otherwise state why fair value is unavailable.
2. One-paragraph causal thesis, the five-sentence mirror thesis when decision-useful, and the decisive assumptions or unknowns.
3. Mechanical baseline: engine action, score, factor coverage, market regime, hard data gates, and reviewable trade constraints.
4. Reasoning outlook: why the business/evidence path is stronger, weaker, or different from the model within the selected horizon.
5. Three strongest supporting observations and three strongest contradictions or unknowns.
6. Explicit divergence explanation when final judgment differs from the engine; otherwise state why they agree for different reasons.
7. Entry window and trigger, cancellation conditions, stop, sizing constraint, exit logic, and time stop. Keep levels from the engine; disclose any conditionally overridden trade constraint and its compensating controls.
8. Source ledger, independent-source reconciliation summary, monitoring thresholds, limitations, and the conditional-research disclaimer. For an update, state whether each material change was factual, valuation-only, wording-only, or a data-quality correction.
9. If a visual artifact was generated, finish with the inspected PNG and a clickable absolute link to the self-contained HTML report. Put no analysis after the HTML link.

When no calibrated model exists, say “relative decision score” rather than “chance of rising.” When evidence conflicts, show the conflict instead of averaging it away in prose.
