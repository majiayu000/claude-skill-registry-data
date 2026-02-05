---
name: alphaear-stock
description: Search A-Share stock tickers and retrieve stock price history. Use when user asks about stock codes, recent price changes, or specific company stock info.
---

# AlphaEar Stock Skill

## Overview

This skill provides access to A-Share market data, including fuzzy search for stock tickers and retrieval of historical price data (OHLCV).

## Capabilities

### 1. Stock Search & Data Retrieval

Use `scripts/stock_tools.py` to interact with the stock database (and network fallback).

**Key Methods:**

-   `search_ticker(query)`: Fuzzy search for stock code or name.
    -   **Returns**: List of `{'code': '...', 'name': '...'}`.
-   `get_stock_price(ticker, start_date, end_date)`: Get daily OHLCV dataframe.
    -   **Arguments**: `ticker` (e.g. "600519"), dates in "YYYY-MM-DD".

**Example Usage (Python):**

```python
from scripts.database_manager import DatabaseManager
from scripts.stock_tools import StockTools
import pandas as pd
from datetime import datetime, timedelta

db = DatabaseManager()
stock_tools = StockTools(db)

# 1. Search Ticker
results = stock_tools.search_ticker("茅台")
print(results)
# Output: [{'code': '600519', 'name': '贵州茅台'}]

# 2. Get Price
end = datetime.now()
start = end - timedelta(days=30)
df = stock_tools.get_stock_price(
    "600519", 
    start_date=start.strftime('%Y-%m-%d'),
    end_date=end.strftime('%Y-%m-%d')
)
print(df.tail())
```

## Dependencies

-   `pandas`
-   `requests`
-   `sqlite3` (built-in)

Ensure `DatabaseManager` is initialized correctly to access the shared SQLite database.
