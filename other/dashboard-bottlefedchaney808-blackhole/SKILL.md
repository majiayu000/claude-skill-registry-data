---
name: dashboard
description: Use when debugging dashboard/app.py (the FastAPI control surface at :8787) — widget behavior, periodic-tick caching/staleness, SPX/SPXW routing, or the Tools/ pages it serves. For starting the process itself, see the launching-dashboard skill; this one covers what goes wrong once it's running.
---

## Overview

`dashboard/app.py` is a single long-lived `uvicorn` process (started by `dashboard.bat`) serving the swap-data browser, the widget-run surface (`GET /api/widgets/catalog`, `POST /api/widgets/{slug}/run`), the periodic overview widgets, and the `/tools/*` pages (`Tools/registry.py`'s tool surface, including Surface Explorer). It is the repo's single highest fix-ratio area — dashboard-touching commits run 60-75% `fix` type across every worktree sampled (added 2026-08-17, `.claude/skills/tool-launcher/SKILL.md`'s original note). This skill collects dashboard-specific debugging knowledge that doesn't belong in `tool-launcher` (in-process module/widget dispatch) or `launching-dashboard` (the user-level skill for actually starting the process).

## Debug / Common Mistakes

**Widget caching means the running process can silently be serving stale code or stale data.** Widgets (Surface Explorer panel, position analysis, market signals) render on a periodic background tick (`WIDGET_*_INTERVAL_SEC`, up to 40 minutes) and cache their last result — including rendered PNGs — in `artifacts/widget_cache.db`. Two consequences:
- Editing a module the dashboard imports (`dashboard/app.py` itself, or anything under `Vol_Suite/`, `Options_Suite/`, `Tools/`) does **not** hot-reload into the already-running `uvicorn` process. Restart it (see `launching-dashboard`) before claiming a fix is visible.
- Even after a restart, a widget only shows fresh output once its tick actually re-runs (immediate on process startup, then every `interval_sec`). Check the cached row's `computed_at` timestamp (`SELECT payload, computed_at FROM widget_cache WHERE widget_id=...` against `WIDGET_CACHE_PATH`) against your restart time before concluding a fix didn't work — a screenshot that "looks the same" after a claimed fix is very often just showing the pre-restart render, not evidence the fix is wrong.

**SPX must be queried under two different root symbols depending on what you're asking for.** On this ThetaData feed, SPX's real listed **options chain** (`option_bulk_greeks`, `option_bulk_oi`, etc.) is rooted under `"SPXW"` — `option_bulk_greeks("SPX", ...)` returns `"v2 payload is None"` for every expiry. SPX's **index price** (`fetch_spot_price`, `index_snapshot_quote`) stays correctly rooted under plain `"SPX"` — `shared/thetadata.py::_INDEX_PRICE_ROOT_ALIASES` maps `"SPXW"` back to `"SPX"` for price lookups at the source, but any NEW caller that resolves its own ticker (rather than going through `fetch_spot_price`) can still reintroduce this bug by using the options-chain root for a price call, or vice versa. `dashboard/app.py`'s `OVERVIEW_WATCHLIST`/widget-4 ticker is `"SPXW"` deliberately (it's the options-chain leg); don't "simplify" it back to `"SPX"`. Known still-open gap (noted in commit `43b7c6a`, unfixed as of this writing): `Vol_Suite/correlation_engine.py::fetch_price_history` has the same root mismatch for its own stock-EOD history endpoint, used broadly across Vol_Suite's realized-vol inputs — not scoped to any one widget.

**A `/tools/*` route with a genuinely slow tool (e.g. `iv_smile_by_model`, 50-90+ seconds — it always calibrates Heston with 37 multi-start restarts regardless of the `include_heston` flag, which only trims output) must not block the event loop.** An `async def` route that calls a slow synchronous tool directly freezes the *entire* dashboard process for the duration — every other widget tick, poll, and websocket update stalls too, which reads as "the whole dashboard is broken," not "one tool is slow." Route it through `starlette.concurrency.run_in_threadpool` (see `dashboard/app.py`'s `/tools/surface-explorer` POST handler for the pattern). Watch for the reverse mistake too: adding `run_in_threadpool` and its import in two separate edits — an auto-formatter that runs between them will strip the import as "unused" if the call site isn't there yet, producing a `NameError` that 500s the route (happened live, 2026-08-29).

**A broken import doesn't fail loudly at module-import time if the route body is what references it.** FastAPI route bodies only execute on request, so a missing/removed import used inside a rarely-hit branch (a specific `mode=` value, an optional query param path) can sit undetected until that exact combination is actually hit. Prefer an in-process ASGI request (`httpx.ASGITransport(app=app.app, raise_app_exceptions=True)`) over a live `curl` to get the real traceback when a route 500s — `curl` only shows "Internal Server Error", not the underlying exception.

See also `.claude/skills/tool-launcher/SKILL.md`'s "Dashboard quant-summary gotchas" section for `shared/summary.py`'s two sentiment-bundle-shape bugs (a related but distinct area: the orchestrator-run summary the dashboard displays, not the dashboard's own widget/route code).

## Quick Reference

| Task | Where |
|---|---|
| Start/restart the process | `launching-dashboard` skill (user-level) |
| Widget/module-run dispatch issues | `.claude/skills/tool-launcher/SKILL.md` |
| Widget cache | `artifacts/widget_cache.db` (`widget_cache` table: `widget_id`, `payload`, `status`, `computed_at`) |
| Surface Explorer / Tools pages | `Tools/tools/surface_explorer_tool.py`, `dashboard/templates/tools_surface_explorer.html` |
