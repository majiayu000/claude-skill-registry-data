---
name: options-suite
description: Use when launching, running headlessly, or debugging Options_Suite (main.py) — options pricing (CRR, Leisen-Reimer, SABR, Vanna-Volga, MC, Heston, BAW) and Greeks in FinancialDevelopment/Options_Suite.
---

## Overview

Options_Suite's `main.py` is 933 lines: a real interactive terminal prompt loop (`main()`, prompts for ticker/option type/strike/model choice) plus a headless `--context`/`--context-out` mode (`run_context_mode`). It imports `vol_manager.py`, `VannaVolga.py`, `SABRModel.py`, `barone_adesi_whaley.py`, `bruteforceimpliedvol.py` (etc.) at module top level and actively calls into `VolManager`/`lr_all_greeks`/`crr_all_greeks`/`sabr_all_greeks`/`vv_all_greeks` — this is **no longer a thin stub**; see Launch below for what context mode actually produces. (Corrected 2026-08-17 — a prior version of this skill described a ~120-line entry point with pricing code unwired; that was stale, not the current file.) `chain_evaluation.py`/`reports.py` is a genuinely separate reporting path `main.py` doesn't call into, if you need that specifically.

`trade_journal.py` is a separate CLI for position journaling in this same directory — unrelated to launching/debugging the pricing engine, out of scope here.

For venv location, port checks, and `PYTHONPATH`/`PYTHONHOME` stripping, defer to `.claude/skills/quant-suite-launch-conventions.md`.

## Launch

Interactive: `Options_Suite\options_suite.bat` (no args) — opens a real prompt loop: ticker, option type, strike (with a closest-listed-strike fallback), then a model-choice menu (`main()`, `Options_Suite/main.py:488`). (Corrected 2026-08-17 — this skill previously said no-arg mode just prints a version banner with "Interactive mode not yet implemented"; that string doesn't exist in current source.)

Headless/context mode: `python main.py --context PATH --context-out PATH`. `run_context_mode` (`main.py:144`) reads `suite_context.json`, fetches live spot/rate/dividend-yield, resolves an ATM (or context-specified) strike, solves sigma via `VolManager(..., method="LeisenReimer")`, and on success writes `options_result.json` with `status: "ok"`, `method: "LeisenReimer"`, `sigma`, `price`, and a full `greeks` dict — this passes `shared/schemas.py::validate_options_result`. (Corrected 2026-08-17 — this skill previously described a placeholder `_build_options_result` function producing `pricing_models: []` with no method/sigma/price/greeks and failing schema validation; that function doesn't exist in current source, and the historical `orchestrator_output/20260729T055003Z/options_result.json` result this skill flagged as "unreproducible" is reproducible again.) On failure (missing context fields, ThetaData error, IV-solve failure) it writes `status: "error"` with the exception message instead.

Gotcha (verified by running `python3 main.py --help` — it fails, does not print help): the ThetaData credential check (`THETADATA_CF_ACCESS_CLIENT_ID`/`THETADATA_CF_ACCESS_CLIENT_SECRET`) runs at **module import time**, before argparse even executes. Even `--help` exits with the credentials error if those env vars aren't set. Set them (or populate `.env`) before invoking `main.py` at all.

Minor inconsistency (resolved): `options_suite.bat` calls `..\.venv\Scripts\python.exe` (repo-root venv); `options_suite.sh` previously called a suite-local `Financial_Dev_Env/bin/python3` (WSL-era venv name) — both now use the shared root `.venv` (`../.venv/bin/python3` on POSIX).

## Dashboard / Tools relationship

The dashboard's "Options Strategy Tool" (`dashboard/templates/tools_options_strategy.html`, backed by `Tools/tools/options_strategy_tool.py`) is a **genuinely separate code path**, not a UI wrapper around `Options_Suite`. It reads/re-runs `Vol_Suite/options_chain_scanner.py` + `strategy_recommender.py` output (`chain_strategies.json`), and never imports anything from `Options_Suite/`. Don't assume debugging the dashboard's options tool touches this suite's code.

## Debug / Common Mistakes

- `--help` failing isn't a broken parser — it's the credential check above; check env vars first.
- Context mode's `status: "ok"` payload has no `pricing_models` key (that's not part of its schema) — it's `method`/`sigma`/`price`/`greeks`, single-model (LR), not a multi-model list. Don't go looking for a `pricing_models` field in `options_result.json`.
- Real multi-model pricing output (CRR/LR/Newton-Raphson/SABR/Vanna-Volga/MC side by side) is interactive-mode-only (`main.py`'s menu, not `--context`) — the context path always uses LeisenReimer only.
- **Pricing-model default: use Leisen-Reimer (LR), NOT CRR.** CRR's price oscillation at coarse steps makes LR the preferred default for the IV solve and the non-interactive/context path. When a run "tries to use CRR again", switch the model to LR — see `american_binomial.py` docstring and the `main.py` context-mode path that already uses LR sigma.
- **`VannaVolga.py`'s smile must use the real Castagna-Mercurio construction, not a bare curve fit through the 3 pillar vols.** A plausible-looking-but-wrong intermediate version replaced VV's original (bounded, flat-in-the-wings) convex-combination bug with an unconstrained quadratic fit through (25-delta-put, ATM, 25-delta-call) — it curves, so it *looks* fixed, but nothing about it is actually Vanna-Volga: it's disconnected from the option's own vega/vanna/volga and can swing to unrealistic values far from the pillars. The correct construction: price each pillar strike at the flat ATM reference vol AND at its own market vol, vega-ratio-weight the Lagrange correction of those two price differences at the target strike, add to the flat-vol price, then invert the result back to an IV via Newton (`get_vol`/`get_vol_batch`, fixed `ca2642b`). The vega-ratio weights genuinely collapse to ~0 far from the pillars in dollar terms (deep ITM/OTM options have near-zero vega under a low reference vol) — `get_vol_batch` returns NaN there rather than a fabricated near-zero vol; callers must filter it (see `Options_Suite/chain_evaluation.py`'s VannaVolga curve block for the pattern).

## Quick Reference

| Task | Command |
|---|---|
| Interactive launch | `Options_Suite\options_suite.bat` |
| Headless run | `python main.py --context ctx.json --context-out result.json` |
| Required env vars | `THETADATA_CF_ACCESS_CLIENT_ID`, `THETADATA_CF_ACCESS_CLIENT_SECRET` |
| Real pricing code | `vol_manager.py`, `chain_evaluation.py` (not via `main.py`) |
