---
name: rate-limit-options
description: Use when acquiring options history via ThetaData (option_bulk_hist_oi_by_day / greeks routes) and hitting transient 502s or rate limits — distinguish rate-limit noise from genuinely missing data, and apply backoff/concurrency discipline.
---

# Rate-limit options acquisition (ThetaData)

Guidance for ThetaData options-history acquisition. Invoked via `/rate-limit-options`.

## Core rule (AMENDED 2026-09-19 — read the amendment first)

**AMENDMENT: a timeout at ~5.0s is NOT a rate limit. It was our own httpx
default.** `PHClient` built its `httpx.Client` with no timeout, inheriting
httpx's 5.0s default, and `ClientConfig` exposed no way to change it. Measured
on SPY one-minute history, every span from 10 to 25 days failed at exactly
5.0s and then served in **0.3-0.5s** once the timeout was raised. Those were
filed as rate limits for a long time. They were not. Fixed in
`shared/thetadata.py::_apply_http_timeout` (`THETADATA_HTTP_TIMEOUT_S`,
default 120) — see the `phclient-v2` skill for the full table.

**Diagnose with the clock before you diagnose with folklore:** a failure at
almost exactly 5.0s is the old client default. An instant `PHAPIError` is a
real `LARGE_REQUEST` refusal. A 502 after real work under load is a real rate
limit.

**Still true for genuine 502s:** a 502 / empty response on an options bulk
route usually means the proxy is rate-limited, not that the ticker/expiry has
no data. Do NOT record a hard gap or impute a zero from a 502.

## Acquisition discipline (from `Vol_Suite/seed_data_maker.py`)
- `option_bulk_hist_oi_by_day` is the **proxy-fragile leg** — treat every response as possibly
  rate-limited.
- **Retry up to 3× with backoff** on transient 502/5xx.
- **Run ONE TICKER AT A TIME** — never concurrent whole-chain fan-outs on this route.
- Prefer the DENSE EOD route (`option_bulk_hist_eod`, IV solved from bid/ask via
  `implied_vol.implied_vol`) + `hist_stock_eod` for spot over the sparser per-contract
  `option_bulk_hist_greeks` route, which is what starves history in the first place.

## Handling
- Transient 502 → backoff and retry (3× max) before classifying anything.
- After retries exhausted and the response is still empty/5xx, only then record a genuine
  gap/INELIGIBLE — never an imputed zero.
- Persist response status + retry count so the provenance census is honest.
- Respect `THETADATA_HIST_CONCURRENCY`; keep sequential for OI-by-day.

## Falsifier / provenance note
A rate-limited acquisition must be labeled as such (retried, backoff), never silently treated as
"data absent" — otherwise it poisons later causal/provenance claims.
