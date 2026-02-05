---
name: ibkr-gateway-api
description: Use when working in mm-ibkr-gateway to access market data, account summary, positions, PnL, or orders via the REST API (FastAPI). Covers starting the API server, required env and safety settings, authentication with X-API-Key, and market/account/order endpoints for quote, historical bars, preview, place, status, cancel, and open orders.
---

# IBKR Gateway API

## Overview

Use the REST API in this repo to fetch market data, read account data, and manage orders safely with preview-first flow.

## Workflow

1. Confirm safety mode and connectivity.
   - Ensure IBKR Gateway or TWS is running on the configured host/port.
   - Keep `TRADING_MODE=paper` and `ORDERS_ENABLED=false` unless explicitly asked to enable live trading.
   - If exposing the API, set `API_KEY` and require `X-API-Key` on requests.

2. Start the API server.
   - `python -m api.server` or `ibkr-gateway start-api`
   - Verify with `GET /health`.

3. Use market data, account, and order endpoints.
   - Read `api/API.md` for full endpoint docs and error codes.
   - Read `docs/SCHEMAS.md` for request/response schemas (OrderSpec, Position, AccountSummary).
   - Read `docs/SAFETY_CHECKLIST.md` before enabling live trading.

4. Prefer preview-first order flow.
   - Call `POST /orders/preview` before `POST /orders`.
   - If `ORDERS_ENABLED=false`, `POST /orders` returns `SIMULATED`.

## Minimal Examples

Account summary:

```bash
curl http://localhost:8000/account/summary
```

Quote snapshot:

```bash
curl -X POST http://localhost:8000/market-data/quote \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "securityType": "STK"}'
```

Preview a limit order:

```bash
curl -X POST http://localhost:8000/orders/preview \
  -H "Content-Type: application/json" \
  -d '{
    "instrument": {"symbol": "AAPL", "securityType": "STK"},
    "side": "BUY",
    "quantity": 10,
    "orderType": "LMT",
    "limitPrice": 150.00
  }'
```

## References

- `references/api-endpoints.md` for market/account/order endpoint lists and request patterns.
