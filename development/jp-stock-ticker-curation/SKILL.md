---
name: jp-stock-ticker-curation
description: Research and curate fundamentally strong Japanese stock candidates from up-to-date internet sources, then submit a source-backed proposal and apply eligible changes through the repository's deterministic curation workflow without directly editing `tickers.yml`. Use when a user asks to add, replace, shortlist, or refresh JP tickers based on earnings momentum, guidance revisions, valuation rerating room, balance sheet quality, shareholder returns, or other fundamental upside drivers.
---

# JP Stock Ticker Curation

Use this skill to research a fundamentally driven JP stock basket and, when
requested, pass it through the repository's deterministic curation guardrails.
Prioritize primary sources, date-stamped facts, and explicit tradeoffs over
generic stock picks or chart-only stories.

Never edit `tickers.yml` or `curation_pool.yml` directly. Only deterministic
repository scripts may write them. Do not bypass pool membership, warmup,
technical, freshness, churn, cooldown, or sector guards to force a requested
name into the enabled universe.

## Workflow

1. Confirm local schema and constraints.
- Read `AGENTS.md`, `specification_document/08_invariants.md`, `tickers.yml`,
  `curation_pool.yml`, `README.md`, and `src/config.py`.
- Read the `fundamental_latest.json` contract in
  `specification_document/ai_ticker_curation/04_data_contracts.md` before
  creating a proposal.
- Treat repository paths as repo-relative when documenting changes.

2. Gather latest market evidence from the web.
- Use internet browsing for every run; do not rely on memory for "latest" financial information.
- Prefer primary sources: company IR, TDnet/EDINET disclosures, JPX pages, financial statements, and official guidance documents.
- Use secondary sources only to complement coverage gaps.
- Record concrete dates and numbers for each key claim, and note whether the claim is based on reported actuals, company guidance, or an inference.

3. Build a fundamental longlist.
- Start from liquid JP equities where the latest disclosure suggests upside from fundamentals, not just price momentum.
- Favor earnings acceleration, upward guidance revisions, margin expansion, ROE/ROIC improvement, balance-sheet strength, buybacks or dividend growth, and rerating catalysts tied to business performance.
- Exclude names with weak liquidity or stale disclosure.
- Exclude names whose recent strength is mostly one-off, technically driven, or contradicted by balance-sheet stress or deteriorating core earnings.
- Keep a temporary longlist, then narrow with the scoring framework.

4. Score with the framework.
- Read `.agents/skills/jp-stock-ticker-curation/references/selection-framework.md`,
  which points at the canonical rubric shared with the weekly fundamental agent.
  Score against that canonical rubric — do not invent your own weights.
- Read `docs/curation/macro_latest.json`. If it exists and its `as_of` is within
  ~14 days, apply the macro tilt inside `catalyst` / `risk_penalty` only, tracing
  every macro claim to a source in that file. If it is missing, empty, or older
  than ~14 days, score without the tilt and note that in the report.
- Score each candidate on earnings quality, guidance, valuation, cash generation, shareholder return, and fundamental catalysts.
- Drop low-conviction names and keep a balanced sector mix.

5. Select the proposed tickers.
- Choose the final set size from user intent. If unspecified, use 5-8 names.
- Keep portfolio concentration reasonable; avoid one-sector dominance.
- Use ticker codes in `NNNN.JP` format.

6. Apply only through the deterministic curation path when requested.
- For a shortlist-only request, do not mutate repository state.
- For an apply request, write a date-stamped proposal such as
  `docs/curation/interactive_fundamental_<YYYY-MM-DD>.json` using the
  `fundamental_latest.json` contract. Do not overwrite the automated
  `fundamental_latest.json`.
- Refresh the deterministic technical baseline:
  `uv run python scripts/technical_screen.py --pool curation_pool.yml --date <YYYY-MM-DD>`.
- Confirm every proposed candidate is already in `curation_pool.yml`, appears in
  `docs/curation/technical_latest.json`, and has sufficient warmup. If not, stop
  at a source-backed proposal and report the unmet prerequisite.
- Run `scripts/curation_merge.py` with the current technical JSON and the
  interactive fundamental proposal using `--dry-run` first. Inspect
  `docs/curation/decision_latest.json`.
- If the user requested application and the dry run proposes guarded changes,
  rerun the same command with `--apply`. If the guardrails reject or defer a
  candidate, do not edit YAML to override the result.

7. Validate and report.
- Re-open the decision log and, if changed, `tickers.yml`.
- Run a lightweight parser check via the project config loader:
  `uv run python -c "from src.config import load_tickers; print(len(load_tickers()))"`
- Mention that the next `main.py` / watchdog run will treat the updated enabled ticker universe as the source of truth.
- Report proposed picks, actually applied changes, guardrail rejections or
  prerequisites, concise rationale, and source links.
- State limitations (no guarantee of returns; data can change quickly).

## Source Quality Rules

- Treat recency as mandatory for financial claims.
- Use absolute dates (for example `2026-02-04`) when summarizing earnings updates.
- Prioritize direct evidence over narrative commentary.
- Prefer facts tied to fundamentals: revenue, operating profit, EPS, guidance, margins, ROE, net cash/debt, buybacks, dividends, backlog/order trends, and capital allocation.
- Avoid unverifiable claims and avoid copying long excerpts.
- Avoid recommending a ticker on "theme" alone unless the thesis is anchored by current disclosed fundamentals.

## Output Contract

When finishing, provide:
- The proposal and decision-log paths, plus `tickers.yml` only if the
  deterministic merge changed it.
- Final ticker list in code + name format.
- 1-2 line rationale per sector/theme bucket.
- A link list of sources used.
- Any verification steps that could not be run locally.

## References

- `.agents/skills/jp-stock-ticker-curation/references/selection-framework.md` —
  points at the canonical rubric (`jp-stock-fundamental-screen/references/selection-framework.md`)
  for scoring weights, thresholds, and diversification rules, and records the one
  interactive-path difference (macro-cache availability).
