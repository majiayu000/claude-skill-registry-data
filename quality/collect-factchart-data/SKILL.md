---
name: collect-factchart-data
description: Collect, inspect, validate, normalize, and document FactChart source data for an operator-authorized derivative information service, including Korean-equity prices, disclosures, news, company_info, market/finance snapshots, company-tab metrics, and client-side peer metadata. Use when Codex is asked to test FactChart access, collect a supported stock, inspect the 기업 분석 tab or comparison-stock group, build or review FactChart ingestion, validate schema/freshness/completeness/scaling, or prepare FactChart inputs for downstream research. Do not use this skill to make an investment decision or to treat FactChart as a replacement for DART, KRX, or issuer IR.
---

# Collect FactChart Data

Receive FactChart source information, validate it, and prepare clearly separated raw and derived records for the authorized derivative information service.

## Project boundary

- Record that the project owner states FactChart's operator has authorized source-data receipt for a derivative information service.
- Treat the actual partnership agreement as controlling for endpoints, frequency, storage, transformation, redistribution, attribution, security, and commercial use.
- Do not claim the repository independently verifies or stores the agreement.
- Keep data collection separate from buy/sell classification, portfolio advice, target-price decisions, or order execution.

## Required reference

Read [references/factchart-data-guide.md](references/factchart-data-guide.md) completely before calling or documenting FactChart endpoints. It contains the tested schemas, company-tab behavior, comparison-group logic, authorization context, known defects, request examples, and operating checklist.

Read [references/factchart-output-contract.md](references/factchart-output-contract.md) completely before shaping or handing off collected data. Emit `schema_version: "factchart-handoff/1.0"` and keep raw provider fields, normalized values, quality state, discovery leads, and downstream-use allowlists separate.

## Workflow

1. Fix the retrieval time, `Asia/Seoul` timezone, FactChart company name, KRX ticker/market, and official DART company identifier. Do not join records on company name alone when identity is ambiguous.
2. Confirm the intended operation is within the partnership scope. Do not infer that a browser-visible `anon` key grants additional rights.
3. Select only the necessary source:
   - `stock_data.json` for the 348-stock bundle, market/finance snapshots, and cached discovery.
   - Supabase `prices`, `disclosures`, `news`, or `company_info` for one-stock retrieval.
   - The versioned `app.js` metadata only when reproducing the site's client-side sector or company-tab logic.
4. Pass the current API key through a session secret or environment variable. Never commit, print, log, or embed it in documents or command history.
5. Collect with one concurrent request, the agreement's rate limit, deterministic secondary sorting, bounded retries, and cache reuse. Prefer a single filtered request over copying the site's parallel peer requests.
6. Record HTTP status, endpoint and selected fields, retrieval time, response date range, `Content-Range`, row count, schema, and response hash when reproducibility matters.
7. Paginate until collected rows equal the exact total. Deduplicate prices by instrument/date, disclosures by `rcp_no`, news by stable ID/URL, and company rows by the verified instrument identity.
8. Normalize raw provider fields without overwriting them. Store provider values, normalized values, formulas, units, period labels, and validation flags separately.
9. When raw records need deterministic shaping, run `python scripts/normalize_factchart_data.py normalize INPUT.json --output HANDOFF.json`, then validate with `python scripts/normalize_factchart_data.py validate HANDOFF.json`. Use the input envelope and output structure defined in [references/factchart-output-contract.md](references/factchart-output-contract.md). This tool performs no network access, accepts no credentials, preserves provider fields, deduplicates records, computes only scale-independent ratios, and leaves unsafe fields off the engine allowlist.
10. Apply the quality gates below. Mark an observation `unverified`, `delayed`, `stale`, `truncated`, or `definition_unknown` instead of silently repairing uncertainty.
11. Produce one `factchart-handoff/1.0` object and a primary-source follow-up list. Hand off to a separate analysis skill only after material claims are checked against DART, KRX, company IR, or another documented primary source.

## Company and comparison data

- Retrieve company fundamentals from `company_info`; combine them with price and market snapshots only after recording each component's timestamp.
- Recompute debt ratio, ROE, operating margin, equity ratio, EPS, BPS, PER, PBR, and any derived valuation from preserved inputs.
- Treat `y0/y1/y2`, TTM fields, and bundle `fin` fields as different definitions until their accounting periods and formulas are verified.
- Reconstruct comparison candidates from the versioned `STOCK_META` and `bigSector()` logic only when required.
- Label those names `broad sector candidates`, never verified competitors or related businesses. Report the valid sample count separately for every metric.
- Do not promote the site's simplified PER/PBR/DCF reference values into an investment conclusion.

## Hard quality gates

- Do not use REST disclosure `change` directly. Recompute `r0/r1/r5` from verified prices and the DART publication time using the event-session rules in the reference.
- Do not call a REST result complete unless `Content-Range` total equals the post-deduplication collected count or the discrepancy is explained.
- Do not treat an empty array as proof that a company has no data; distinguish unsupported name, spelling, renamed issuer, temporary omission, and genuine absence.
- Do not use FactChart prices as a full quantitative price ledger: daily volume, adjustment policy, corporate actions, delistings, exchange, currency, and point-in-time universe rules are incomplete.
- Do not mix REST prices, bundled market snapshots, `company_info.updated_at`, TTM fields, and annual fields without explicit timestamps and definitions.
- Do not score provider-defined sentiment, `amt10`, PER/PBR/ROE, `tone`, or `price_reaction` when the formula or period is unknown.
- Stop and report a schema or access change instead of bypassing authentication, authorization, rate limits, or service controls.

## Output contract

Follow [references/factchart-output-contract.md](references/factchart-output-contract.md). Return or store:

1. Authorization context and partnership-scope note.
2. Instrument identity: FactChart name, KRX ticker/market, DART identifier, and any unresolved mismatch.
3. Retrieval ledger: endpoint, fields, timestamps, row counts, `Content-Range`, hashes, and application-script version when used.
4. Raw coverage summary for prices, disclosures, news, company information, market, finance, and comparison metadata.
5. Normalized and derived fields with units, periods, formulas, and provenance.
6. Data-quality findings, including freshness, truncation, nulls, duplicates, definition conflicts, and mixed timestamps.
7. Broad comparison candidates with metric-specific valid sample counts and a warning that they are not confirmed competitors.
8. Primary-source verification queue for DART, KRX, issuer IR, and article originals.
9. A clear statement of what is safe for discovery, safe for the derivative service, or blocked from downstream quantitative analysis.

Do not emit an undocumented ad hoc shape. When a requested source is absent, retain its contract container and record `null`, an empty array, or a quality flag as specified; never make a downstream skill guess whether omission means unsupported, unrequested, failed, or genuinely empty.

Generate a deterministic example when testing the tool or teaching a downstream consumer the contract:

```text
python scripts/normalize_factchart_data.py demo --output factchart-demo-handoff.json
python scripts/normalize_factchart_data.py validate factchart-demo-handoff.json
```
