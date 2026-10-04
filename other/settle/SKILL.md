---
name: settle
description: Compare predictions against settled results, update the learning feedback loop, and report ROI/P&L. Use when the user wants to settle bets, grade a run, see how picks performed, or refresh calibration after results come in.
---

# Settle & Grade

Evaluate predictions against actual results and refresh the calibration loop.

## Steps

1. Settle the latest run (or a specific saved run):
   ```bash
   python tippmix.py compare
   python tippmix.py compare --run data/predictions/20260609_074456.json
   ```
2. This writes `data/comparisons/compare_<timestamp>.json`, appends
   `data/archive/comparisons.jsonl`, and updates `data/lessons.json`
   (`market_adjustments`, `missed_predictions`, `notes`).
3. Read the comparison output and report:
   - Per-item results (🟢 NYERT / 🔴 VESZÍTETT / 🟡 FOLYAMATBAN).
   - Summary: hit rate, **ROI**, and HUF balance.
   - Which markets moved their calibration offset and why (from `lessons.json` notes).
4. Combo legs settle individually — a pushed/void leg pays the winning legs, it does
   not zero the combo. Verify this held if a combo looks mis-graded.

## Notes

- Markets with < 5 settled predictions keep adjustment = 0 (not enough signal).
- Adjustment formula: `clamp(round((actual_win_rate - expected_win_rate) * 50), -20, 20)`.
- If many picks are still 🟡 FOLYAMATBAN, results haven't landed yet (tennis/esports
  settlement can lag) — re-run later rather than forcing conclusions.
- For a full historical view across all runs, use `/backtest`.
