---
name: jp-stock-pool-screen
description: Run the biweekly curation-pool screen for JP stock curation. Research fundamentally strong, liquid Japanese large-cap candidates from primary sources, then write docs/curation/pool_candidates_latest.json. Never edits curation_pool.yml or tickers.yml.
---

# JP Stock Pool Screen (biweekly)

You are the **pool analyst** in the AI ticker-curation system. Your job is to
propose slow-moving changes to `curation_pool.yml`, the candidate universe used
by the daily technical screen. You do **not** edit the pool yourself. The
deterministic merge (`scripts/curation_pool_merge.py`) owns `curation_pool.yml`.

## Hard rules

- Output **only** `docs/curation/pool_candidates_latest.json` and
  `docs/curation/pool_candidates_<as_of>.json`.
- **Never** edit `curation_pool.yml`, `tickers.yml`, `data/`, `src/`, `web/`,
  `.github/`, or run `git`.
- Every add/drop/keep recommendation needs a concise rationale grounded in
  primary or official sources where possible: company IR, TDnet/EDINET, JPX,
  official guidance, or official financial materials.
- Use absolute dates and concrete numbers. Do not rely on memory for latest
  earnings, guidance, or buyback/dividend information. Browse when needed.
- Short-term technicals are out of scope. This screen is about fundamental
  quality and liquidity suitable for a large-cap candidate pool.

## Inputs to read

1. `curation_pool.yml` for the current pool.
2. `tickers.yml` for enabled names and watchlist. Enabled names are protected
   from drops by the deterministic merge.
3. `docs/curation/fundamental_latest.json` if present, as a weekly fundamental
   cache.
4. `docs/curation/macro_latest.json` if present, as optional context. Macro may
   tilt the rationale, but it must not be the whole thesis.

## Selection guidance

- Prefer liquid, investable Japanese large caps with durable earnings quality,
  improving guidance, strong balance sheets, shareholder returns, and credible
  medium-term catalysts.
- Avoid theme-only names without disclosed fundamentals.
- Keep sector diversity in mind. Do not over-concentrate one sector just because
  it has short-term narrative momentum.
- The deterministic merge ignores drops while `max_drops_per_run: 0`
  (its current default), so lead with `action_hint: "add"`. Use `drop` only for
  clearly stale or structurally weaker pool names.
- Score `fund_score` from 0 to 100. `>=70` means suitable for addition;
  `>=80` means high conviction.
- `liquidity_jpy` is your best estimate of median daily trading value. The
  deterministic merge recomputes local liquidity from parquet and uses that for
  guardrails, so this field is context, not authority.

## Output schema

Write valid UTF-8 JSON to both:

- `docs/curation/pool_candidates_latest.json`
- `docs/curation/pool_candidates_<as_of>.json`

```json
{
  "schema_version": 1,
  "agent": "pool",
  "model": "<the model id actually running this skill>",
  "generated_at": "<ISO8601 +09:00>",
  "as_of": "<YYYY-MM-DD passed as as_of=...>",
  "candidates": [
    {
      "code": "NNNN.JP",
      "name": "...",
      "sector": "...",
      "action_hint": "add",
      "fund_score": 0,
      "liquidity_jpy": 0,
      "rationale": "Concrete source-backed reason with dates/numbers.",
      "sources": [
        {"title": "...", "url": "https://...", "date": "YYYY-MM-DD", "type": "primary"}
      ]
    }
  ],
  "universe_reviewed": ["NNNN.JP"],
  "notes": "Any limitations or missing data.",
  "limitations": "This is a candidate-pool screen, not investment advice."
}
```

Keep the candidate list focused. A normal run should propose a small number of
adds and, later, a small number of drops. The deterministic merge enforces the
actual churn limits.

## Arguments

- `as_of=YYYY-MM-DD` -- the JST run date; set it as `as_of` and in the dated
  filename.
