---
name: ibkr-gateway-python
description: Use when working in mm-ibkr-gateway to access market data, account summary, positions, PnL, or orders directly in Python via ibkr_core. Covers connecting with IBKRClient, using market/account/order helpers, and safety rules for preview, place, cancel, and status.
---

# IBKR Gateway Python

## Overview

Use ibkr_core modules in Python scripts or notebooks to fetch market data, read account data, and manage orders with safety rails.

## Workflow

1. Confirm safety mode and connectivity.
   - Ensure IBKR Gateway or TWS is running on the configured host/port.
   - Keep `TRADING_MODE=paper` and `ORDERS_ENABLED=false` unless explicitly asked to enable live trading.
   - For offline testing, set `IBKR_MODE=simulation` and use `get_ibkr_client` from `ibkr_core.simulation`.

2. Create and connect a client.
   - Use `IBKRClient(mode="paper")` or `get_ibkr_client()` (respects `IBKR_MODE`).
   - Call `client.connect()` and `client.disconnect()`.

3. Use market data, account, and order helpers.
   - Market data: `get_quote`, `get_quotes`, `get_historical_bars`, `get_streaming_quote`, `get_quote_with_mode`
   - Account: `get_account_summary`, `get_positions`, `get_pnl`, `get_account_status`, `list_managed_accounts`
   - Orders: `preview_order`, `place_order`, `get_order_status`, `cancel_order`, `get_open_orders`, `cancel_order_set`
   - Pass `account_id` when targeting a specific account; omit to use the first managed account.

4. Prefer preview-first order flow.
   - Call `preview_order` before `place_order`.
   - If `ORDERS_ENABLED=false`, `place_order` returns `SIMULATED`.

## References

- `references/python-usage.md` for import lists and code examples.
- `ibkr_core/models.py` and `docs/SCHEMAS.md` for field names and order types.
- `notebooks/02_market_data.ipynb`, `notebooks/03_account_status.ipynb`, and `notebooks/04_orders.ipynb` for end-to-end workflows.
