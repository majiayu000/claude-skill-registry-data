---
name: sentiment-scanner
description: Use when launching, debugging, or scripting sentiment-scanner (StockTwits/Reddit/YouTube contested-narrative detection + 7 options scanners + correlation engine) — covers its shared root .venv launch, real headless flags, and what actually happens when the bgutil PO-token server is unreachable.
---

## Overview

`sentiment-scanner/main.py` scans trending tickers on StockTwits, scores contested-narrative sentiment, runs 7 options scanners (GEX, Unusual OI, IV Rank, Skew, Max Pain, Vol Dispersion, Earnings-Vol Premium) via ThetaData, cross-references CME SDR swap data, and optionally pulls YouTube caption sentiment. Results feed a `CorrelationEngine` for composite signals. It loops on a timer by default (`config.SCAN_INTERVAL_MINUTES`) — this is a long-running scanner, not a single-shot tool, unless you pass `--no-loop`.

For venv/port/PATH conventions shared across all four suites, see `.claude/skills/quant-suite-launch-conventions.md` — don't repeat those checks here.

## Launch

Interactive: `sentiment-scanner\sentiment.bat` (from that directory) — uses the shared root `.venv`, dependency install, and PO-token server auto-start described in the shared reference.

Headless flags (verified against `main.py`'s actual `argparse` setup — source-read, since `--help` couldn't run in this sandbox due to a missing `httpx` dependency unrelated to the flags themselves):

`--no-loop` (single pass then exit), `--export-context <path>` (writes a `suite_context.json`-compatible sentiment block — schema_version 2, includes `ranked_tickers`/`pack_json_path`/`group_id`), `--benchmark <ticker>` (default SPY, for vol dispersion), `--skip-gex`, `--skip-youtube`, `--skip-sector-prompt`, `--skip-report-prompt`, `--launch-vol-suite` (subprocess-launches Vol_Suite on the alert highlight pack, if one exists).

Confirmed: there is no `--context`/`--context-out` pair. sentiment-scanner is producer-only for `suite_context.json` — it never consumes one. `--export-context` writes on every loop cycle (not just at exit), so a long-running scheduled instance keeps the export file current.

## Debug / Common Mistakes

**Max pain / OI snapshot 404:** pin `scan_max_pain(ticker, expiry=focus.expiration_date)` from the run context — never invent an expiry. A ThetaData `bulk_snapshot` 404 (e.g. SMCI/20261112 OI) is expected; `orchestrator.run_market_signals_stage` falls back (~331–349). Do not treat that 404 string as a scanner crash.

**Max pain (and likely other scanners) can go silent when the run context carries no expiry.** Reported live more than once: max pain output shows up fine when the ticker/expiry context is present but produces nothing when the scanner is invoked with an empty/context-free scope. The expiry/context `scan_max_pain` needs (see the bullet above) is normally supplied by the surrounding run; a bare `--no-loop` invocation needs it supplied explicitly (or a sane default resolved) or the scanner silently comes back empty instead of raising — check what expiry/context is actually available before assuming a wiring bug elsewhere. (The old `--unified` subprocess chain that used to supply it was removed 2026-09-04; in the widget/module path supply `ticker`/`expiration_date` in the run scope.)

YouTube captions being silently thin or absent is not a bug — verified in `scanner/youtube.py`: `_check_pot_server_once()` does a cheap one-time `/ping` health check and just logs a warning if the bgutil server is unreachable; it does not raise or abort. The actual per-request PO-token failure is caught separately and also treated as non-fatal, falling back to no caption data for that fetch. So a missing PO-token server degrades gracefully all the way through — no launch error, no exception, just thinner sentiment data. If sentiment output looks unexpectedly sparse, check for the one-time "bgutil PO-token server not reachable" warning near the top of the log rather than assuming a code bug.

Interactive prompts (`_prompt_yes_no` for Sector Rotation launch and PDF report generation) auto-skip when stdin isn't a TTY, so scheduled/cron runs never hang — but `--skip-sector-prompt`/`--skip-report-prompt` still make headless behavior explicit and are cheap to always pass in scripts.

Recurring bug classes (added 2026-08-17, from a fix-hotspot audit — the YouTube integration was ~40% of one worktree's fix commits):
- **yt-dlp's `js_runtimes` config must be a dict `{"node": {"path": _NODE_PATH}}`, not a list.** `scanner/youtube.py`'s `_ytdl_search`/`_fetch_transcript` both build `ydl_config["js_runtimes"]`; an earlier version used a list form (`["node"]`, then `[f"node:{_NODE_PATH}"]`) that yt-dlp didn't accept — the dict form is current and correct (fixed `f6ee104`, `b43682a`).
- **Always pass the full resolved Node.js path**, not a bare `"node"` relying on PATH resolution — `_NODE_PATH = shutil.which("node")`'s result, set once at module import, feeds directly into the `js_runtimes` dict above.
- **`main.py` imports `scanner.youtube.scan_ticker` under a private alias (`_youtube_scan`), not a bare re-export named `run_youtube_scanner`** — `main.py` also defines its own `run_youtube_scanner(ticker, engine)` function, and re-exporting the module's `scan_ticker` under that same name shadowed it. If touching the YouTube call site in `main.py`, use `_youtube_scan(ticker)`, not a name that collides with the local function (fixed `726d926`).
- **`scanner/gex_scanner.py` must not assume the legacy `dealer_positioning.py` result shape.** After the 2026-08-20 `expiry_book_production` migration, code reading a dealer-exposure result must use `ProductionDealerExposure`'s real fields (compute a forward price directly, anchor off `result.spot`) — an earlier version read `result.forward`, a field that dataclass doesn't have, which is a guaranteed `AttributeError` on every successful (non-error) scan, not just an edge case (fixed `1020eac`).
- **Never call `.close()` on the shared, session-cached `ThetaDataController`.** `get_td()`'s own docstring says callers must not close it — `gex_scanner.py` closed it after the first ticker's scan, which silently broke every subsequent ticker in the same run with "Cannot send a request, as the client has been closed" (fixed `3b6b9b3`).
- **`run_directional_scan` must copy `max_pain_strike` and `build_oi_snapshot` real OI into the directional-scan JSON.** `--universe` is the producer of `outputs/directional_scan` — omitting those fields is a regression, not a thin-data case.

`requirements.txt` has no dev/test split (unlike Vol_Suite) — one file, no `requirements-dev.txt`. `tests/` exists (pytest-based, `test_main.py`, `test_correlation_engine.py`, etc.) with no `pytest.ini`/`pyproject.toml`, so run with plain `pytest tests/` from `sentiment-scanner/` using the shared root `.venv` interpreter (`..\.venv\Scripts\python.exe`), which carries this project's deps (yt-dlp, curl_cffi, bgutil-ytdlp-pot-provider) since 2026-09-14.

## Quick Reference

| Item | Value |
|---|---|
| Entry point | `sentiment-scanner/main.py` |
| Interactive launch | `sentiment-scanner\sentiment.bat` |
| venv | shared root `.venv` (sentiment.bat pip-installs root requirements each launch) |
| Producer/consumer | producer only — `--export-context <path>`, no `--context` |
| Single-pass mode | `--no-loop` |
| PO-token server | `http://127.0.0.1:4416/ping` — degrades gracefully, no launch failure |
| Tests | `pytest tests/` from `sentiment-scanner/`, root venv, no config file |
