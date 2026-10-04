---
name: tool-launcher
description: Use when running, driving, or debugging registered modules (the widget-run / module-execution layer) or the dashboard's Tools/ framework — how a module's ModuleResult surfaces as status/error, and how Vol_Suite, Options_Suite, VaR_Tools_Simulations and sentiment-scanner modules are run in-process.
---

## Overview

Since Phase 7 (2026-09-04) there is **no cross-suite subprocess launcher**. The CLI
`--unified`/`--suite` and `run_suite`/`run_unified` were removed (removed 2026-09-04),
along with the dashboard `trigger_run`/`POST /run/{suite}` route
and `orchestrator.bat`/`orchestrator.sh`. Registered modules run **in-process**:

- **Interactive / dashboard**: browse `GET /api/widgets/catalog`, run any module
  with `POST /api/widgets/{slug}/run` (body = scope/context dict). The route
  resolves one `ModuleSpec`, calls `spec.run(context)`, writes the result to the
  scoped widget cache and any `context_patch` to the Context Store
  (`shared/context_store.py`).
- **Scripted / agent**: `shared.module_execution.run_selected_modules(slugs, context)`
  — resolves, expands `requires` transitively, topo-sorts, runs each module's
  `run(context)`, and merges each returned `context_patch` into the running
  context. `orchestrator.py` re-exports this function and the two helpers
  (`_expand_module_requires`, `_topo_sort_modules`), and still hosts the module-CLI
  shell (`orchestrator.py --modules slug,slug --ticker T` / `--interactive`).

`Tools/` (dashboard-side, `Tools/registry.py`'s `ToolSpec` pattern) is a separate,
lighter integration surface for one-off tools that read a `suite_context.json` —
see the shared conventions file, not repeated here.

For venv/port/PYTHONPATH preflight, defer to `.claude/skills/quant-suite-launch-conventions.md`.

## Run

**After a code fix, do not start the dashboard / run modules unless the user
explicitly asked to run.** Default to a handoff package.

Widget (dashboard): start `dashboard.bat`, open `http://127.0.0.1:8787`, use the
Quant Console — or call the route directly:

```bash
curl -s -X POST http://127.0.0.1:8787/api/widgets/chain_scanner/run \
  -H "Content-Type: application/json" -d '{"ticker":"NVDA","target_years":0.25}'
```

In-process (scripted/agent), no web UI:

```bash
.venv\Scripts\python.exe -c "import shared.module_execution as me; r=me.run_selected_modules(['dealer_exposure'], {'ticker':'SPY'}); print(r['status'], r['order'])"
```

Unknown slug → `run_selected_modules` raises `ValueError`; the widget route maps
that to a 404. Module-level failures surface as `status: error`/`failed` on the
`ModuleResult` (with a `metrics.error`), never a silent fallback.

## Debug — module failures given each suite's known limits

Module `run()` implementations live under each suite's `module_registry.py` and
share the quirks documented in that suite's skill. The rules that still bite when
a run looks wrong:

- **VaR's `corr_sim` is the only fully-wired context-mode module.** Other VaR
  slugs can return `status: error` in a scoped run because their
  `run_context_mode` path isn't implemented. Confirm which module actually ran
  before debugging a "VaR failed" as a data problem.
- **Options pricing defaults to Leisen-Reimer, not CRR.** A module result that
  reports CRR for the default path is a regression Jason has reported more than
  once — investigate, don't ship it.
- **Vol_Suite's heavy sub-steps are env-var gated in context/module mode.**
  `VS_RUN_CHAIN_SCANNER`, `VS_RUN_GROUP_SCREENER`, `VS_RUN_VOL_SURFACE_2D`,
  `VS_RUN_SENTIMENT_BACKTEST` default OFF outside the interactive flow
  (`VS_RUN_VRP_TERM_STRUCTURE` defaults ON). If a module run skips a section you
  expected, check these before suspecting a bug.
- **Context Store threading (do not re-debug as a scanner crash).** A producing
  module (dealer exposure, vol-stats) writes its `context_patch` to the Context
  Store keyed by scope. A downstream consumer (VaR's `_resolve_vol_and_quality` /
  `_resolve_drift_and_quality`) reading it back shows `0.0`/`0.25`/identity-matrix
  fallbacks when the entry is missing — i.e. the producer didn't run, or ran under
  a different scope key. Confirm the scope matches (`GET /api/context?scope=...`)
  before assuming a wiring bug. (This replaced the removed `_thread_vol_stats_into_context`
  that mutated a shared suite_context object in place.)

## Dashboard quant-summary gotchas (`shared/summary.py`)

Added 2026-08-17 — this was the repo's single highest fix-ratio area (dashboard
commits are 60-75% `fix` type across every worktree sampled) and the recurring bug
class wasn't written down anywhere. Both fixes below live in `shared/summary.py`,
not `dashboard/app.py` itself:
- **`_extract_sentiment` must understand BOTH bundle shapes.** `sentiment_result.json`
  has two producers — the real sentiment-scanner's `--export-context`
  (`sentiment.ranked_tickers`) and, on a full run,
  `orchestrator.py::run_market_signals_stage`'s scanners/simulations/direction
  bundle. Recognizing only the sentiment-scanner shape makes the quant summary's
  market-signals module fall through to `degraded` and hides a full run's real
  numbers behind a fake failure (fixed `8f284b9`).
- **Bundle-level `errors` must be surfaced even when per-item scanner/sim dicts are
  empty.** `run_market_signals_stage` can put scanner import failures, GARCH fit
  failures, or direction-suite crashes into a bundle-level `errors` list while
  leaving `scanners`/`simulations` empty — a per-key `.get("error") is None` check
  over an empty dict is vacuously true, so the summary silently reported "0/0
  scanners, 0/0 sims" with zero warnings and dropped the actual reason. Append
  un-represented `errors` entries to `warnings` on the non-error path (fixed
  `61667bb`).
- General rule from both fixes: a bundle/import/fit failure anywhere in this
  pipeline should surface as an explicit warning in the dashboard summary, never
  silently degrade to a status that hides what actually happened.

(A stale shared `.venv` missing a required package is covered under "Which venv,
and is it complete" in `quant-suite-launch-conventions.md` — `dashboard.bat`/
`tools.bat` pre-check `import fastapi, uvicorn, jinja2, slowapi` so that fails fast
with one clear message, not a mid-startup traceback.)

## Output / Audit Trail

A widget/module run returns a `ModuleResult` (status/artifacts/metrics) and caches
it under the run's scope key (table `widget_cache`). Any `context_patch` is written
to the Context Store's `context_entries`, with a hashed/snapshot audit row in
`context_store_audit` (the Phase 1 successor to the old `orchestrator_runs`
per-run audit). Read back without re-running via `GET /api/widgets/{slug}/state`
and `GET /api/context`.

## Quick Reference

| Task | Command / route |
|---|---|
| Browse registered modules | `GET /api/widgets/catalog` (or `from shared.module_registry import all_modules`) |
| Run one module (dashboard) | `POST /api/widgets/{slug}/run` with `{"ticker": ...}` scope/context |
| Run modules in-process | `.venv\Scripts\python.exe -c "import shared.module_execution as me; me.run_selected_modules([...], {...})"` |
| Module-CLI shell | `orchestrator.py --modules slug,slug --ticker T` (`--modules-category`, `--all-modules`, `--list-modules`, `--interactive`) |
| Last cached result | `GET /api/widgets/{slug}/state?scope=...` |
| Context-Store provenance | `GET /api/context?scope=...` |
| Result files | suite modules still write `vol_result.json` / `options_result.json` / `var_result.json` where they produce them |
