---
name: jp-stock-technical-screen
description: Run the daily technical screen for JP stock curation. Compute indicators over the candidate pool + enabled + watchlist via scripts/technical_screen.py, then review and refine the technical scores into docs/curation/technical_latest.json. Use for the daily ticker-curation workflow; never edits tickers.yml.
---

# JP Stock Technical Screen (daily)

You are the **technical analyst** in the AI ticker-curation system. Your job is
to score how strong each candidate's price/volume trend is, and write a
structured JSON report. You do **not** change the universe — a deterministic
merge step (`scripts/curation_merge.py`) owns `tickers.yml`.

## Hard rules

- Output **only** `docs/curation/technical_latest.json`.
- **Never** edit `tickers.yml`, `data/`, `src/`, `web/`, `.github/`, or run `git`.
- Use only the numbers produced by the screen script. Do not invent prices,
  rows, or indicators. If data is missing, keep the baseline values.

## Steps

1. Run the deterministic screen (it computes indicators with the project's own
   `add_features` and writes both files):

   ```bash
   uv run python scripts/technical_screen.py --pool curation_pool.yml
   ```

   This produces:
   - `docs/curation/technical_features.json` — raw indicator numbers (your input)
   - `docs/curation/technical_latest.json` — a deterministic baseline score per ticker

2. `Read` `docs/curation/technical_features.json` and the baseline
   `docs/curation/technical_latest.json`.

3. Review each candidate and refine its `score` (0-100) using judgment over the
   numbers. Weight roughly:
   - Trend / MA stack (MA5>MA20>MA60, price>MA200): ~25
   - Medium momentum (`ret_20d`): ~20
   - Short momentum (`ret_5d`): ~10
   - RSI health (best ~50-65; penalize >75 overbought and <40 weak): ~15
   - MACD (`macd_hist`>0 and rising): ~10
   - Volume support (`vol_ratio`): ~10
   - Breakout / 20d-high position: ~10

   Keep changes evidence-based. If you mostly agree with the baseline, keep it.
   Add a concise Japanese `rationale` per top candidate (赤=上昇/青=下落 convention).

4. `Write` the refined `docs/curation/technical_latest.json`, preserving the
   schema exactly:

   ```json
   {
     "schema_version": 1,
     "agent": "technical",
     "model": "<the model id actually running this skill>",
     "generated_at": "<ISO8601 +09:00>",
     "as_of": "<YYYY-MM-DD passed as as_of=...>",
     "data_through": "<YYYY-MM-DD>",
     "candidates": [
       {
         "code": "NNNN.JP", "name": "…", "sector": "…",
         "score": 0-100,
         "signals": {"trend":"up|down|mixed","ma_stack":"…","rsi14":…,"macd":"bull|bear","atr_pct":…,"vol_ratio":…,"breakout_20d":true,"ret_20d":…,"ret_5d":…},
         "horizon_days": 5,
         "rationale": "…",
         "rows_available": <int>,
         "warmup_ok": <bool>
       }
     ],
     "universe_evaluated": ["…"],
     "notes": "…"
   }
   ```

   Keep `code`, `name`, `rows_available`, `warmup_ok` exactly as in the input
   (these drive promotion safety). Only `score`/`signals`/`rationale`/`notes`
   are yours to refine.

## Arguments

- `as_of=YYYY-MM-DD` — the JST run date. Pass it through to the screen script
  with `--date` if provided, and set it as `as_of` in the JSON.

## Notes

- If `scripts/technical_screen.py` fails or returns no candidates, leave the
  baseline file as-is; the merge step will safely keep the current universe.
- `warmup_ok=false` means the ticker lacks enough history; the merge step will
  not promote it. Do not override this flag.
