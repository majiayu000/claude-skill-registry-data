---
name: jp-stock-fundamental-screen
description: Run the weekly fundamental screen for JP stock curation. Research the latest earnings, guidance, valuation, balance sheet, and catalysts from primary sources, score candidates with the selection framework, and write docs/curation/fundamental_latest.json. Use for the weekly fundamental & report workflow; never edits tickers.yml.
---

# JP Stock Fundamental Screen (weekly)

You are the **fundamental analyst** in the AI ticker-curation system. Once a
week you research up-to-date fundamentals for the JP candidate universe and
emit a scored JSON report. You do **not** change the universe — the
deterministic merge (`scripts/curation_merge.py`) owns `tickers.yml`, and the
daily merge uses your report as a weekly cache.

## Hard rules

- Output **only** `docs/curation/fundamental_latest.json` (and a dated copy
  `docs/curation/fundamental_<as_of>.json`).
- **Never** edit `tickers.yml`, `data/`, `src/`, `web/`, `.github/`, or run `git`.
- Every selected candidate needs **≥1 primary source within ~90 days**
  (company IR, TDnet/EDINET, JPX, official guidance). No source → do not include.
- Use **absolute dates** (e.g. `2026-05-12`) and concrete numbers. No theme-only
  picks. Do not rely on memory for "latest" financials — browse.
- **Macro alone is never a thesis.** Disclosed fundamentals (earnings, guidance,
  valuation, balance sheet) must anchor every pick; the macro cache only tilts
  the forward-looking catalyst/risk view (see Scoring).

## Universe to review

1. `Read` `tickers.yml` (enabled `tickers` + `watchlist`) and `curation_pool.yml`.
2. Cover all enabled + watchlist names (so the merge has fresh fundamental
   scores for them), plus promising pool names worth surfacing.
3. `Read` `docs/curation/macro_latest.json` if it exists (the weekly macro
   cache: 金利・金融政策・為替レジーム from the global-macro agent). If it is
   missing, empty, or its `as_of` is older than ~14 days, proceed **without** it
   and note that in `notes`. Never fail on a missing macro file.

## Scoring

4. `Read` `.agents/skills/jp-stock-fundamental-screen/references/selection-framework.md` and score each candidate 0-100
   (earnings 30 / guidance 20 / valuation 15 / balance sheet 15 / shareholder
   return 10 / catalyst 5 / risk penalty 5). `>=70` selectable, `>=80` high
   conviction. Keep sector diversity in mind (no single sector dominance).
5. **Macro tilt (forward-looking, 2週間以降).** Map each candidate to
   `macro_latest.json` themes by matching its `code` against a theme's
   `affected_codes`, or its `sector` against `affected_sectors`. Reflect the net
   tilt **only inside** the existing `catalyst` (0..5) and `risk_penalty`
   (-5..0) subscores and the `thesis` text — do **not** add new subscores or
   change the rubric. A `tailwind` can lift `catalyst` toward 5 and soften
   `risk_penalty` toward 0; a `headwind` can trim `catalyst` and push
   `risk_penalty` toward -5. Any macro claim in a `thesis` must trace to a
   source in `macro_latest.json`.

## Output

6. `Write` `docs/curation/fundamental_latest.json` AND
   `docs/curation/fundamental_<as_of>.json` with this schema:

   ```json
   {
     "schema_version": 1,
     "agent": "fundamental",
     "model": "<the model id actually running this skill>",
     "cadence": "weekly",
     "generated_at": "<ISO8601 +09:00>",
     "as_of": "<YYYY-MM-DD passed as as_of=...>",
     "candidates": [
       {
         "code": "NNNN.JP", "name": "…", "sector": "…",
         "score": 0-100,
         "subscores": {"earnings":…,"guidance":…,"valuation":…,"balance_sheet":…,"shareholder_return":…,"catalyst":…,"risk_penalty":…},
         "thesis": "日付と数値を含む簡潔な根拠（2週間以降に効く金利・為替の追い風/向かい風があれば併記）",
         "sources": [{"title":"…","url":"…","date":"YYYY-MM-DD","type":"primary"}],
         "confidence": "high|medium|low"
       }
     ],
     "universe_reviewed": ["…"],
     "notes": "…",
     "limitations": "将来の値動きを保証しない。データは急変しうる。"
   }
   ```

   `as_of` is critical: the merge checks freshness against
   `max_fundamental_age_days` and stops promotions if the cache is stale.

## Arguments

- `as_of=YYYY-MM-DD` — the JST run date; set it as `as_of` and in the filename.

## Notes

- Keep the JSON valid and UTF-8. If you cannot verify a name's fundamentals
  with a fresh primary source, omit it rather than guessing.
- This file becomes the weekly fundamental cache reused by the daily merge, so
  prioritize accuracy and coverage of the enabled + watchlist names.
