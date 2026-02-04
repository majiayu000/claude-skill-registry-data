---
name: backtest-persistence
description: "Save backtest results to SQLite database for comparison. Trigger when: (1) tracking backtest history, (2) comparing model performance, (3) querying best backtests."
author: Claude Code
date: 2024-12-29
---

# Backtest Result Persistence

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-29 |
| **Goal** | Persist backtest results to SQLite for historical comparison |
| **Environment** | backtest/engine.py, db_manager.py, run_backtest.py |
| **Status** | Success |

## Context

Backtest results were only returned in-memory and never persisted. This made it impossible to:
- Compare performance across model versions
- Track which configs produced best results
- Query historical backtest performance
- Find the best performing model for a symbol

## Verified Workflow

### 1. Add Table to Schema (trading_db.sql)

```sql
CREATE TABLE IF NOT EXISTS backtest_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    model_path TEXT,
    run_timestamp INTEGER NOT NULL,
    start_date INTEGER NOT NULL,
    end_date INTEGER NOT NULL,
    initial_capital REAL NOT NULL,
    final_equity REAL NOT NULL,
    total_return REAL NOT NULL,
    sharpe_ratio REAL,
    max_drawdown REAL,
    win_rate REAL,
    profit_factor REAL,
    total_trades INTEGER,
    avg_trade_pnl REAL,
    config_json TEXT,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_backtest_symbol ON backtest_results(symbol, timeframe);
CREATE INDEX IF NOT EXISTS idx_backtest_timestamp ON backtest_results(run_timestamp DESC);
```

### 2. Add Database Methods (db_manager.py)

```python
def save_backtest_result(
    self,
    symbol: str,
    timeframe: str,
    initial_capital: float,
    final_equity: float,
    total_return: float,
    max_drawdown: float,
    total_trades: int,
    win_rate: Optional[float] = None,
    sharpe_ratio: Optional[float] = None,
    profit_factor: Optional[float] = None,
    avg_trade_pnl: Optional[float] = None,
    model_path: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    config: Optional[dict] = None,
    notes: Optional[str] = None
) -> int:
    """Save backtest results to database. Returns backtest ID."""
    now = int(datetime.now(timezone.utc).timestamp())
    start_ts = int(start_date.timestamp()) if start_date else now
    end_ts = int(end_date.timestamp()) if end_date else now
    config_json = json.dumps(config) if config else None

    with self._get_connection() as conn:
        cur = conn.execute("""
            INSERT INTO backtest_results (
                symbol, timeframe, model_path, run_timestamp,
                start_date, end_date, initial_capital, final_equity,
                total_return, sharpe_ratio, max_drawdown, win_rate,
                profit_factor, total_trades, avg_trade_pnl, config_json, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (...))
        return cur.lastrowid
```

### 3. Add save_to_db() to BacktestResult (engine.py)

```python
def save_to_db(
    self,
    db: Optional[Any] = None,
    model_path: Optional[str] = None,
    timeframe: str = "1Hour",
    notes: Optional[str] = None,
) -> int:
    """Save backtest results to SQLite database."""
    from ..data.db_manager import TradingDatabase

    if db is None:
        db = TradingDatabase()

    # Extract dates from equity curve
    start_date = self.equity_curve.index[0].to_pydatetime()
    end_date = self.equity_curve.index[-1].to_pydatetime()

    backtest_id = db.save_backtest_result(
        symbol=self.symbol,
        timeframe=timeframe,
        initial_capital=self.config.initial_capital,
        final_equity=self.equity_curve.iloc[-1],
        total_return=self.metrics.total_return_pct,
        max_drawdown=self.metrics.max_drawdown_pct,
        total_trades=self.metrics.total_trades,
        win_rate=self.metrics.win_rate,
        sharpe_ratio=self.metrics.sharpe_ratio,
        profit_factor=self.metrics.profit_factor,
        avg_trade_pnl=self.metrics.avg_trade_pnl,
        model_path=model_path,
        start_date=start_date,
        end_date=end_date,
        config=self.config.to_dict(),
        notes=notes,
    )
    return backtest_id
```

### 4. Add CLI Flag (run_backtest.py)

```python
parser.add_argument(
    '--save-to-db',
    action='store_true',
    help='Save backtest results to SQLite database'
)

# In run functions:
if save_to_db:
    backtest_id = result.save_to_db(
        model_path=model_path,
        timeframe=timeframe,
    )
    logger.info(f"Saved backtest to database with id={backtest_id}")
```

### 5. Query Methods (db_manager.py)

```python
def get_backtest_results(
    self,
    symbol: Optional[str] = None,
    timeframe: Optional[str] = None,
    limit: int = 100
) -> List[Dict]:
    """Get recent backtest results with optional filters."""
    ...

def get_best_backtest(
    self, symbol: str, timeframe: str, metric: str = 'total_return'
) -> Optional[Dict]:
    """Get the best performing backtest for a symbol/timeframe."""
    valid_metrics = ['total_return', 'sharpe_ratio', 'profit_factor', 'win_rate']
    ...
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Storing dates as strings | Query performance issues | Use Unix timestamps (INTEGER) |
| Storing full equity curve | Database bloat | Only store summary metrics |
| Lazy import at module level | Circular import errors | Use lazy import inside method |
| datetime.to_pydatetime() on Timestamp | Some indices aren't Timestamps | Check with hasattr() first |

## Final Parameters

```yaml
# Table schema
symbol: TEXT NOT NULL          # Trading symbol
timeframe: TEXT NOT NULL       # 1Hour, 4Hour, etc.
model_path: TEXT               # Path to model file
run_timestamp: INTEGER         # When backtest was run
start_date: INTEGER            # Unix timestamp
end_date: INTEGER              # Unix timestamp
initial_capital: REAL          # Starting capital
final_equity: REAL             # Ending equity
total_return: REAL             # Return percentage
sharpe_ratio: REAL             # Risk-adjusted return
max_drawdown: REAL             # Maximum drawdown %
win_rate: REAL                 # Win rate %
profit_factor: REAL            # Gross profit / gross loss
total_trades: INTEGER          # Number of trades
avg_trade_pnl: REAL            # Average P&L per trade
config_json: TEXT              # Serialized config
notes: TEXT                    # Optional notes
```

## Key Insights

- **Lazy imports**: Use `from ..data.db_manager import TradingDatabase` inside the method to avoid circular imports
- **Unix timestamps**: Store dates as INTEGER for efficient queries
- **Optional fields**: Use REAL without NOT NULL for metrics that might be missing
- **Index on symbol+timeframe**: Most queries filter by these columns
- **config_json**: Serialize the config dict for full reproducibility

## Usage Examples

```bash
# Save backtest to database
python scripts/run_backtest.py --model models/rl_symbols/GOOGL_1Hour.pt --save-to-db

# Run all backtests and save
python scripts/run_backtest.py --all --save-to-db
```

```python
# Programmatic save
result = engine.run(model, data, symbol)
result.save_to_db(model_path='models/rl_symbols/GOOGL_1Hour.pt')

# Query best backtest
db = TradingDatabase()
best = db.get_best_backtest('GOOGL', '1Hour', metric='sharpe_ratio')
```

## References
- `alpaca_trading/backtest/engine.py`: BacktestResult.save_to_db()
- `alpaca_trading/data/db_manager.py`: save_backtest_result(), get_backtest_results()
- `scripts/run_backtest.py`: --save-to-db CLI flag
