---
name: calibration
description: Inspect the learning feedback loop — review per-market confidence calibration, sample counts, and recent missed predictions. Use when picks feel mis-calibrated, a market is over/under-confident, or before trusting a new analyze run.
---

# Calibration Review

Audit `data/lessons.json` and the backtest history to judge whether the model is well-calibrated.

## Steps

1. Read `data/lessons.json`. Report each market's `market_adjustment`, its settled
   **sample count**, and the Hungarian `note`. An offset only matters with ≥ 5 samples.
2. Run the historical view for outcome rates per market:
   ```bash
   python tippmix.py backtest
   python tippmix.py improve
   ```
3. Diagnose calibration:
   - **Expected vs actual win rate** per market — gaps drive the offset.
   - Markets pinned at ±20 (the cap) are systematically mis-priced; flag for a
     formula/weight change in `recommendations.py`, not just an offset.
   - Low-sample markets (< 5) with extreme recent results — note as noise, not signal.
4. Recommend concrete actions: adjust a weight in `config.py:DEFAULT_CONFIG["weights"]`,
   tweak a probability formula, or leave the auto-offset to keep learning.

## Notes

- Offsets are bounded ±20 and applied in `generate_recommendations()`.
- The calibration display resets per day (display-only) — historical truth is in
  `data/archive/comparisons.jsonl`, not the live panel.
- Prefer fixing the underlying probability model over stacking large manual offsets;
  offsets are a patch, calibration of the formula is the cure.
