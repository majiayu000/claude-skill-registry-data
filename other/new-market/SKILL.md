---
name: new-market
description: Add a new betting market to the analysis engine end-to-end (recommendation generation, odds extraction, settlement, i18n, docs). Use when the user wants to support a new bet type / market (e.g. corners, cards, exact-score, a new handicap line).
---

# Add a Betting Market

Wire a new market through the full pipeline so it is generated, priced, settled, calibrated, and translated.

## Checklist (do all that apply)

1. **Generate it** — add a row to `raw_recommendations` in
   `recommendations.py:generate_recommendations`:
   `(market_type, selection, probability, category, odds)`. Derive `probability`
   from existing stats/Elo signals; don't invent a constant.
2. **Price it** — add an odds-extraction pattern in `recommendations.py:_market_odds()`
   (and `_extract_market_odds`) so bookmaker odds and EV get populated. The matching
   is fuzzy regex — verify against real API market names from `python tippmix.py events`.
3. **Settle it** — add result-evaluation logic in `evaluation.py:evaluate_run()` so the
   market can be graded win/loss/push. Handle voids (push pays, doesn't zero combos).
4. **Score impact (optional)** — if it should influence match confidence, weight it in
   `recommendations.py:score_match_confidence()` and add the weight key to
   `config.py:DEFAULT_CONFIG["weights"]` (+ `tippmix.config.json` if user-configurable).
5. **Translate it** — add `market_label`/`selection`/`result_label` strings to
   `tippmix_system/i18n.py`. Code stays English; only output strings are Hungarian.
6. **Calibrate it** — new markets start with adjustment 0 until ≥ 5 settle; that's expected.
7. **Test it** — add a fixture-based test under `tests/` (mirror `test_combo_settlement.py`
   / `test_calibration.py`). Cover generation, odds extraction, and settlement.
8. **Document it** — update the market tables in `ARCHITECTURE.md` and `CLAUDE.md`.

## Verify

```bash
python -m py_compile tippmix_system/recommendations.py tippmix_system/evaluation.py
python -m pytest tests/ -q
python tippmix.py analyze    # confirm the market appears with sane odds/EV
```
