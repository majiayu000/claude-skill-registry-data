---
name: analyze
description: Run the daily Tippmix betting analysis and surface the recommendations + combinations. Use when the user wants to generate today's picks, analyze a date's matches, or produce a fresh PredictionRun.
---

# Daily Analysis

Generate a fresh `PredictionRun` and present the picks the way a trader would read them.

## Steps

1. Confirm scope. Default to today; if the user named a date use `--date YYYY-MM-DD`.
2. Run analysis:
   ```bash
   python tippmix.py analyze            # today
   python tippmix.py analyze --date 2026-06-14
   ```
3. The run writes `data/latest_run.json`, `data/predictions/<timestamp>.json`,
   `data/reports/report_<timestamp>.json`, and appends `data/archive/runs.jsonl`.
4. Read `data/latest_run.json` to summarize for the user. Report **per match**:
   match header, confidence %, recommended bets (selection + confidence + odds + EV
   when present), and the combination buckets with their tiered HUF stakes.
5. Lead with **expected value**, not win probability. Flag any pick where confidence
   is high but EV is negative (odds too short) — that is not a bet.

## Notes

- Recommendations below `high_risk_confidence_threshold` (50) are already discarded by the engine.
- `analyze` reads `data/lessons.json` and applies learned per-market calibration offsets — if calibration looks off, run `/calibration` first.
- Do NOT dump raw stats dicts to the user; the full data lives in the JSON files.
- If the API is unreachable, run `python tippmix.py check` to confirm before debugging deeper.
