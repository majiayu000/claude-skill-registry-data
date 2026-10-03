---
name: stock-split-adjustment
description: Debug and implement split-adjusted pricing for Taiwan stock data (0050, 0052, etc.) when FinMind raw prices show artificial gaps
---

# Stock Split Adjustment for TWSE Stocks

## When to use
- User reports anomalous price drops/spikes in stock charts (e.g., -75% single-day drop)
- New stock data shows unusual gaps in price history
- MA/RSI calculations produce unexpected results
- Before deploying any stock analysis feature

## Root cause pattern
Taiwan stocks frequently undergo splits (分割), reverse splits (反分割), and face value changes (面額變更). FinMind `taiwan_stock_daily()` returns **raw unadjusted prices**, which creates artificial price drops on split dates.

## Debugging workflow

### Step 1: Identify the stock split event
```bash
docker exec <container> uv run python3 -c "
from FinMind.data import DataLoader
loader = DataLoader()
df = loader.taiwan_stock_split_price(start_date='2020-01-01', end_date='2026-12-31')
print(df[df['stock_id'].astype(str).str.contains('<TICKER>', na=False)])
"
```

Key fields returned (actual columns in API response):
- `stock_id`: 股票代碼 (may be string or int)
- `date`: split effective date (YYYY-MM-DD)
- `before_price`: price before split
- `after_price`: price after split
- ⚠️ No `type` field in response — determine type by ratio (>1=分割, <1=反分割)

### Step 2: Verify the split ratio
Split ratio = `before_price / after_price`
Example: 0050 had 4:1 split on 2025-06-18 (188.65 / 47.16 ≈ 4:1)

### Step 3: Check FinMind adjusted price API
```bash
docker exec <container> uv run python3 -c "
from FinMind.data import DataLoader
loader = DataLoader()
# This may return KeyError: 'data' - known issue
df = loader.taiwan_stock_daily_adj(stock_id='0050', start_date='2025-06-01', end_date='2025-07-01')
"
```
⚠️ **Known issue**: `taiwan_stock_daily_adj` sometimes returns `KeyError: 'data'`. Work around by computing adjustments manually using `taiwan_stock_split_price`.

### Step 4 (NEW): Check FinMind split price auth bug ⚠️ CRITICAL
**The FinMind SDK has an auth-dependent response format bug**:
- `DataLoader()` (no auth) → `taiwan_stock_split_price()` returns `{"data": [...]}` ✓
- `DataLoader(token=...)` (logged in) → returns `{"columns": [...]}` (no `data` key) ✗

This causes `KeyError: 'data'` when the global `self.fm_loader` is authenticated.

**Fix**: Always create a fresh, unauthenticated `DataLoader()` for split queries:
```python
# WRONG — may fail if fm_loader is logged in:
df = self.fm_loader.taiwan_stock_split_price(...)

# CORRECT — always use a fresh instance:
fm: DataLoader = DataLoader()  # no token = no auth
df = fm.taiwan_stock_split_price(...)
```

⚠️ **Also**: FinMind `taiwan_stock_split_price()` does NOT return a `split_ratio` column. You must calculate it manually:
```python
split_ratio = row['before_price'] / row['after_price'] if row.get('after_price', 0) > 0 else 1.0
```

### Step 4: Verify container env vars
```bash
docker exec <container> env | grep -i finmind
docker exec <container> cat /app/.env
```

## Implementation

### Database schema (add to database.py)
```python
class SplitDB:
    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS split_info (
                stock_id TEXT, event_date TEXT, type TEXT,
                before_price REAL, after_price REAL, ratio REAL,
                PRIMARY KEY (stock_id, event_date)
            )
        ''')
        self.conn.commit()
    
    def fetch_split_info(self, stock_id):
        return self.conn.execute(
            "SELECT * FROM split_info WHERE stock_id=? ORDER BY event_date",
            (stock_id,)
        ).fetchall()
    
    def update_from_finmind(self):
        from FinMind.data import DataLoader
        # CRITICAL: Use fresh DataLoader() without auth to avoid
        # the "columns" vs "data" response format bug
        fm: DataLoader = DataLoader()
        df = fm.taiwan_stock_split_price(start_date='2020-01-01', end_date='2026-12-31')
        for _, row in df.iterrows():
            # split_ratio is NOT in FinMind response — calculate it
            ratio = row['before_price'] / row['after_price'] if row.get('after_price', 0) > 0 else 1.0
            self.conn.execute('''
                INSERT OR REPLACE INTO split_info
                (stock_id, event_date, type, before_price, after_price, ratio)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (row['stock_id'], row['date'], row['type'],
                  row['before_price'], row['after_price'], ratio))
        self.conn.commit()
```

### API layer: apply split adjustment
```python
def get_adjusted_prices(stock_id, adjusted=True):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(f"SELECT * FROM '{stock_id}' ORDER BY Date", conn)
    conn.close()
    
    if not adjusted or df.empty:
        return df
    
    splits = SplitDB().fetch_split_info(stock_id)
    for split_date, _, _, _, _, ratio in splits:
        mask = df['Date'] < pd.to_datetime(split_date)
        if mask.any():
            df.loc[mask, ['Open', 'High', 'Low', 'Close']] *= ratio
            df.loc[mask, 'Volume'] = (df.loc[mask, 'Volume'] / ratio).astype(int)
    
    return df
```

### API endpoint
```python
@router.get("/market/{ticker}/data")
async def get_stock_data(ticker: str, adjusted: bool = Query(True)):
    db = TwStockDB()
    df = db.get_daily_data(ticker)
    if adjusted:
        df = apply_split_adjustment(ticker, df)
    return df.to_dict(orient="records")
```

## Common split events (check periodically)
- 0050: 4:1 split on 2025-06-18
- 0052: 7:1 split on 2025-11-26
- 00663L: 7:1 split on 2025-06-11
- 00673R: reverse split on 2025-10-22
- 00676R: reverse split on 2025-02-19
- 00706L: reverse split on 2025-10-22

## Verification
1. Price chart shows continuous line on split date
2. MA calculations are smooth across split dates
3. 52-week high/low includes both pre and post-split prices

## Pitfalls
- **FinMind API timeout**: Use `timeout=30` on get_data calls
- **Token not set**: Check `FINMIND_TOKEN` env var in container
- **Division by zero**: Handle `after_price == 0` in split calculations
- **Volume adjustment**: Volume must be divided by ratio, not multiplied
- **Multiple splits**: Apply adjustments in chronological order