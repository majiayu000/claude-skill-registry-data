---
name: native-chart-app
description: Use when launching native chart or live tape.
version: 1.2.0
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

Repo: `C:/Users/bottl/FinancialDevelopment`
Clean python: `env -u PYTHONPATH -u VIRTUAL_ENV .venv/Scripts/python.exe`

1. **Is 8791 already up?** Use Python, never git-bash `curl` (curl can return
   `000` while the port is listening — do not kill on that).

```bash
cd /c/Users/bottl/FinancialDevelopment
env -u PYTHONPATH -u VIRTUAL_ENV .venv/Scripts/python.exe -c "import socket; s=socket.socket(); s.settimeout(1); print('up' if s.connect_ex(('127.0.0.1',8791))==0 else 'down'); s.close()"
```

2. **If down**, start uvicorn as a tracked **background** process (do not
   block the chat):

```bash
cd /c/Users/bottl/FinancialDevelopment
env -u PYTHONPATH -u VIRTUAL_ENV .venv/Scripts/python.exe -m uvicorn chart_app.server:app --host 127.0.0.1 --port 8791
```

   (`background=true`. This is a daemon — no `notify_on_complete`.)

3. **Health:** poll `GET http://127.0.0.1:8791/api/state` with Python
   `urllib` until `ok` is true (or 15s). If empty `bars`,
   `POST /api/refresh {"lookback":"5d"}` (default interval is `15m`).
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
| Push RH | after `mcp__robinhood__get_equity_positions`, `POST /api/rh` `{"position":{"qty":n,"avg_price":p},"fills":[]}` |

## Hard rules

- Never `POST` a chart URL to place an order. There is no `/api/order`.
  Live RH only via `mcp__robinhood__place_equity_order` when Jason says so
  **in chat**. Then refresh `/api/rh`.
- Never per-bar PH. Whale is `flow.scanner_trades` **once per session date**
  (cap 5 days), stamped in `chart_app/flow_stamp.py`. Range-query
  `scanner_trades_in_time_range` times out on multi-hour windows — do not
  use it for the tape. LQ still off.
- Legs (W3/SQ/TR/WH/LQ) stay visible; buy/sell stay position-gated.
- Never bind or open `:8787` for this.
- Never kill a healthy 8791 because curl returned `000`.
- Handoff: `chart_app/README.md`.

## Fallback

If uvicorn won't start, `cmd.exe //c C:\Users\bottl\FinancialDevelopment\chart_app.bat`
then re-check the socket.
