---
name: native-chart-app
description: Use when launching native chart or live tape.
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [quant, chart, tape, robinhood]
    related_skills: [native-quant-chart-development, launch-quant-tools]
---

# Native Chart App

Trigger: "launch the chart", "native chart", "live tape", "open the chart",
"what's on the chart".

This is the standalone window at `http://127.0.0.1:8791/` — not TradingView,
not Hermes preview, not dashboard `:8787`. Jason sees pixels. You read
`GET /api/state`. Same numbers.

## Must-do sequence (do not skip)

Repo: `E:/BlackHole_Investments/BlackHole` (moved off C: 2026-09-14)
Clean python: `env -u PYTHONPATH -u VIRTUAL_ENV .venv/Scripts/python.exe`

1. **Is 8791 already up?** Use Python, never git-bash `curl` (curl can return
   `000` while the port is listening — do not kill on that).

```bash
cd /e/BlackHole_Investments/BlackHole
env -u PYTHONPATH -u VIRTUAL_ENV .venv/Scripts/python.exe -c "import socket; s=socket.socket(); s.settimeout(1); print('up' if s.connect_ex(('127.0.0.1',8791))==0 else 'down'); s.close()"
```

2. **If down**, start uvicorn as a tracked **background** process (do not
   block the chat):

```bash
cd /e/BlackHole_Investments/BlackHole
env -u PYTHONPATH -u VIRTUAL_ENV .venv/Scripts/python.exe -m uvicorn chart_app.server:app --host 127.0.0.1 --port 8791
```

   (`background=true`. This is a daemon — no `notify_on_complete`.)

3. **Health:** poll `GET http://127.0.0.1:8791/api/state` with Python
   `urllib` until `ok` is true (or 15s). If empty `bars`,
   `POST /api/refresh {"lookback":"20d"}` (default interval is `15m`; 20d seeds EMA200).
   Daily EOD uses last complete weekday.

4. **Open a visible Edge window** (not Hermes preview, not `:8787`).
   `cmd start` from this agent session does **not** raise a window — do not
   use it. Launch Edge with `--new-window`, then `focus_app` Edge if the
   chart is still behind Hermes.

```bash
"/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" --new-window "http://127.0.0.1:8791/" || "/c/Program Files/Microsoft/Edge/Application/msedge.exe" --new-window "http://127.0.0.1:8791/"
```

   Confirm a window titled `chart-app` exists (`list_windows`). If it is
   behind Hermes, `focus_app` Edge with `raise_window=true`.

5. Tell Jason: URL, ticker, interval, bar count, live stamp, WH bar count.
   Close with "No orders placed — read-only."

If already up, skip start. Just health-check, open the URL if he asked to
see it, report state.

## After it's up

| Action | How |
|---|---|
| Read tape | `GET /api/state` |
| Switch | `POST /api/symbol` `{"ticker":"SPY","interval":"15m"}` |
| Fill bars | `POST /api/refresh` `{"lookback":"5d"}` |
| Chart a perp | `POST /api/symbol` `{"ticker":"BTC-PERP","interval":"1h"}` (OKX, not ThetaData) |
| Push RH | after `mcp__robinhood__get_equity_positions`, `POST /api/rh` `{"position":{"qty":n,"avg_price":p},"fills":[]}` |
| Live param test | `POST /api/backtest` `{"config":{"entry_long":25}}` -> metrics + actions |
| Full backtest | `python -m chart_app.backtest_runner --stage all` |

Reading `/api/state`: `live.algo_score` is the conviction (-100..+100),
`live.action`/`live.position` the state machine, `algo.components` the
per-component breakdown, `whale.status` one of `ready|loading|unavailable|off`,
`elmo.has_volume` whether LQ could be measured at all.

## Hard rules

- Never `POST` a chart URL to place an order. There is no `/api/order`.
  Live RH only via `mcp__robinhood__place_equity_order` when Jason says so
  **in chat**. Then refresh `/api/rh`.
- Never per-bar PH. Whale is `flow.scanner_trades` **once per session date**,
  on a background thread, with a provider-side premium floor. Never
  `min_premium=0`: SPY's full tape is 1.39M prints/day and takes 402s for ONE
  day, which is why whales never appeared. Never make it synchronous inside
  `/api/state`.
- Never fan out ThetaData calls. Concurrent callers time each other out.
- Legs W3/SQ/TR/WH/LQ stay visible. **LQ is live now** (ELMo Hui-Heubel).
  Buy/sell come from `chart_app/signal_engine.py`, not the old position gate
  (`markers_legacy` still publishes that).
- Never bind or open `:8787` for this.
- Never kill a healthy 8791 because curl returned `000`. If a restart hits
  `WinError 10048` the old uvicorn is still bound; check its command line
  before killing it.
- After editing `static/js/*`, the page must be **hard**-reloaded.
- Say `BTC-PERP`, never `BTC`: ThetaData answers for `BTC` with the Grayscale
  Bitcoin Mini Trust ETF, a real instrument at a real price that is not bitcoin.
- **Handoff: `chart_app/HANDOFF.md`** (measured numbers + open items), then
  `chart_app/README.md`.

## Fallback

If uvicorn won't start, `cmd.exe //c E:\BlackHole_Investments\BlackHole\chart_app.bat`
then re-check the socket.
