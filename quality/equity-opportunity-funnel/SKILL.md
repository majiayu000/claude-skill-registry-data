---
name: equity-opportunity-funnel
description: Search a broad investable stock universe and progressively narrow it into recommendation-grade equity ideas. Use when the user asks which stock to buy, the best or highest-upside stock, stock alternatives, a BIST or global stock scan, many shares to compare, or wants a prior stock recommendation rechecked before acting. Automatically deepen a simple “hisse öner” request through universe construction, multi-factor screening, medium diligence, full fundamental/valuation/technical/catalyst analysis, probabilistic forecasting, independent red-team review, failed-candidate replacement, and recommendation consistency tracking. Do not use for a purely descriptive company summary or when the user names a non-equity instrument.
---

# Equity Opportunity Funnel

Own the end-to-end selection process. A screen result is never a recommendation. Keep intermediate work compact for the user, but complete it internally unless the user explicitly requests a rough screen only.

Read:

- [references/funnel-protocol.md](references/funnel-protocol.md) for the staged search and recycling loop.
- [references/recommendation-gate.md](references/recommendation-gate.md) before issuing `AL`, `SPEKÜLATİF AL`, or `ARTIR`.
- [references/horizon-factors.md](references/horizon-factors.md) to adapt evidence to the holding period.
- [references/revision-protocol.md](references/revision-protocol.md) when a prior candidate or recommendation exists.
- [references/funnel-packet-schema.md](references/funnel-packet-schema.md) before validating a final selection.

## Intake

Resolve market/access, horizon, budget, risk posture, allowed instruments, liquidity need, and exclusions from the active conversation. Ask one bundled clarification only when an unresolved choice materially changes the universe. Do not silently reuse an old horizon, budget, holding, or risk statement.

## Required funnel

1. **Construct the universe.** Use the broadest reliably accessible investable universe matching the mandate. Preserve and verify the exact membership ledger, artifact hash, source timestamp, covered tickers and exclusions; derive counts from the ledgers rather than self-reporting them. Never imply “the market was scanned” after checking a handful of familiar tickers or web articles.
2. **Run a broad multi-lane screen.** Evaluate quality, growth/revisions, value, catalysts, momentum/technical structure, liquidity, balance-sheet risk, and high-upside asymmetry in separate lanes. Use `scripts/rank_universe.py` when structured rows exist. Preserve missingness and rejected names.
3. **Create a research shortlist.** Advance roughly 8–12 names when the universe permits. Verify identity, current price, latest filing, liquidity, sector metrics, material news, catalyst timing, valuation context, and obvious disqualifiers. Label every name `ADAY`; do not use action language.
4. **Deepen the finalists.** Advance roughly 3–5 names. Use `$public-equity-research` for company facts, primary filings, earnings quality, valuation, what is priced in, thesis and catalysts. It may use the installed `$public-equity-investing` plugin for narrower workflows when available, but must remain complete without it. Use `$turkey-markets-analysis` for BIST/KAP/TMS 29/Türkiye context, `$technical-quant-analysis` for timing, and `$probabilistic-market-forecast` for realistic outcome ranges.
5. **Apply evidence and red-team review.** Run `$finance-evidence-guard` on decisive facts and `$investment-red-team` on each proposed finalist. Compare against cash/benchmark and the best runner-up.
6. **Recycle failed candidates.** Move every failed finalist to the candidate graveyard with the exact reason. Promote the next shortlisted name and perform the same full diligence. If the whole finalist set fails, rebuild the broad screen with a different defensible lane or broaden the universe once. Stop with `NO EDGE` only after documenting the second pass.
7. **Validate and issue the final selection.** Build the structured packet described in the schema and run `scripts/validate_funnel.py`. Recommend only the 1–3 names that clear the recommendation gate and receive process exit code 0 / `PASS`. If validation is unavailable, fails, or returns `CONDITIONAL`, do not claim a final recommendation; fix the packet or label the best researched name `SPEKÜLATİF ADAY` / `BEST WITHIN COVERED SET` with the exact coverage limitation. If none clears but the user still wants a trade, provide the least-bad conditional setup as `SPEKÜLATİF ADAY`, not a disguised conviction call.
8. **Handoff the winner.** Use `$portfolio-risk-and-sizing` before exact allocation, `$pre-trade-investment-gate` when action is imminent, and `$investment-thesis-tracker` when the recommendation will be monitored. A passed research funnel does not submit an order.

## Consistency rules

- Never upgrade a coarse screen, popularity list, recent rally, analyst target, or single indicator directly to `AL`.
- Never hide eliminated candidates; show a compact funnel count and the main rejection reasons.
- Never lower the diligence standard for the replacement candidate after the first choice fails.
- Do not force the final winner to be the highest initial score. Deep evidence overrides screen rank.
- A later detailed analysis may change a final recommendation only through new evidence, price/time movement, thesis invalidation, or an explicitly admitted earlier analytical defect. Show the delta.
- A prose claim such as “BIST 500 tarandı” is not coverage evidence. The packet must reconcile membership source, counts, exclusions and every screened eligible ticker.
- Validation is fail-closed: only exit code 0 and `PASS` authorize `AL`, `SPEKÜLATİF AL`, or `ARTIR` from an open-ended equity search.

## Final answer

Lead with the final action and horizon, then provide:

- Universe and funnel counts: scanned → shortlisted → deep-dived → passed.
- Best recommendation, runner-up, and why the winner survived deeper work.
- Current price/time, entry condition, bear/base/bull ranges, target probabilities, invalidation, size inputs, catalysts, and exit/review rule.
- Main eliminated names and rejection reasons.
- Evidence confidence and the exact facts that could change the recommendation.

For a simple prompt, keep this concise; depth is in the process, not in forcing the user to read every intermediate table.
