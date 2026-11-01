---
name: journal-analytics
description: Journal Analytics Engineer — Institutional capability and runbook for journal-analytics.
---

# SKILL: Journal Analytics Engineer
## Domain: imJournal — Trading Performance Analytics, TimescaleDB, Metrics

**Activation triggers:** trading journal, trade analytics, performance metrics,
win rate, profit factor, Sharpe ratio, drawdown calculation, equity curve,
calendar heatmap, trade annotation, journal entry.

---

## Domain Model

```
journal.trades          ← synced from broker (MT5, Binance, cTrader)
journal.journal_entries ← user annotations on trades (text, tags, screenshots)
journal.daily_stats     ← TimescaleDB continuous aggregate (materialized daily)
journal.equity_snapshots← TimescaleDB hypertable (time-series equity curve)
```

---

## Core Analytics Queries (TimescaleDB)

```python
# app/services/journal/analytics.py

async def get_performance_summary(
    db: AsyncSession,
    account_id: str,
    from_dt: datetime,
    to_dt: datetime,
) -> PerformanceSummary:
    """Compute win rate, profit factor, Sharpe ratio, max drawdown."""

    result = await db.execute(
        text("""
        WITH trade_metrics AS (
            SELECT
                ticket,
                profit,
                CASE WHEN profit > 0 THEN 1 ELSE 0 END AS is_win,
                CASE WHEN profit > 0 THEN profit ELSE 0 END AS gross_profit,
                CASE WHEN profit < 0 THEN ABS(profit) ELSE 0 END AS gross_loss
            FROM journal.trades
            WHERE account_id = :account_id
              AND closed_at BETWEEN :from_dt AND :to_dt
              AND status = 'closed'
        )
        SELECT
            COUNT(*)                            AS total_trades,
            SUM(is_win)                         AS wins,
            ROUND(AVG(is_win::FLOAT)::NUMERIC, 4) AS win_rate,
            SUM(profit)                         AS total_pnl,
            CASE WHEN SUM(gross_loss) > 0
                 THEN ROUND((SUM(gross_profit) / SUM(gross_loss))::NUMERIC, 2)
                 ELSE NULL
            END                                 AS profit_factor,
            ROUND(AVG(CASE WHEN profit > 0 THEN profit ELSE NULL END)::NUMERIC, 2) AS avg_win,
            ROUND(AVG(CASE WHEN profit < 0 THEN profit ELSE NULL END)::NUMERIC, 2) AS avg_loss
        FROM trade_metrics
        """),
        {"account_id": account_id, "from_dt": from_dt, "to_dt": to_dt},
    )
    row = result.mappings().first()
    return PerformanceSummary(**row) if row else PerformanceSummary()
```

---

## Max Drawdown Calculation

```python
async def get_max_drawdown(
    db: AsyncSession,
    account_id: str,
    from_dt: datetime,
    to_dt: datetime,
) -> float:
    """Window-function based max drawdown over equity curve."""
    result = await db.execute(
        text("""
        WITH equity AS (
            SELECT
                snapshotted_at,
                equity,
                MAX(equity) OVER (ORDER BY snapshotted_at ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS peak_equity
            FROM journal.equity_snapshots
            WHERE account_id = :account_id
              AND snapshotted_at BETWEEN :from_dt AND :to_dt
            ORDER BY snapshotted_at
        )
        SELECT MIN((equity - peak_equity) / NULLIF(peak_equity, 0)) AS max_drawdown
        FROM equity
        """),
        {"account_id": account_id, "from_dt": from_dt, "to_dt": to_dt},
    )
    row = result.first()
    return float(row[0] or 0.0)
```

---

## Sharpe Ratio Calculation

```python
import numpy as np

async def get_sharpe_ratio(
    db: AsyncSession,
    account_id: str,
    from_dt: datetime,
    to_dt: datetime,
    risk_free_rate: float = 0.05,   # annual, default 5%
) -> float:
    """Annualized Sharpe ratio from daily returns."""
    result = await db.execute(
        text("""
        SELECT
            date_trunc('day', closed_at) AS day,
            SUM(profit) AS daily_pnl,
            MAX(equity) AS equity   -- from equity_snapshots join or approximation
        FROM journal.trades
        WHERE account_id = :account_id
          AND closed_at BETWEEN :from_dt AND :to_dt
          AND status = 'closed'
        GROUP BY 1
        ORDER BY 1
        """),
        {"account_id": account_id, "from_dt": from_dt, "to_dt": to_dt},
    )
    rows = result.fetchall()
    if len(rows) < 5:
        return 0.0

    # Daily return = daily PnL / starting equity (approximation)
    pnls = np.array([float(r.daily_pnl) for r in rows])
    daily_rf = risk_free_rate / 252
    excess = pnls - daily_rf
    if excess.std() == 0:
        return 0.0
    return float((excess.mean() / excess.std()) * np.sqrt(252))
```

---

## Calendar Heatmap Data

```python
async def get_calendar_heatmap(
    db: AsyncSession,
    account_id: str,
    year: int,
) -> list[dict]:
    """Daily PnL for calendar heatmap visualization."""
    result = await db.execute(
        text("""
        SELECT
            DATE(closed_at AT TIME ZONE 'UTC') AS trade_date,
            SUM(profit) AS daily_pnl,
            COUNT(*) AS trade_count
        FROM journal.trades
        WHERE account_id = :account_id
          AND EXTRACT(YEAR FROM closed_at) = :year
          AND status = 'closed'
        GROUP BY 1
        ORDER BY 1
        """),
        {"account_id": account_id, "year": year},
    )
    return [
        {"date": str(r.trade_date), "pnl": float(r.daily_pnl), "trades": r.trade_count}
        for r in result.fetchall()
    ]
```

---

## TimescaleDB Continuous Aggregate (daily_stats)

```sql
-- Migration: create continuous aggregate for daily stats
CREATE MATERIALIZED VIEW journal.daily_stats
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', closed_at) AS day,
    account_id,
    COUNT(*) FILTER (WHERE status = 'closed') AS total_trades,
    SUM(profit) AS daily_pnl,
    SUM(profit) FILTER (WHERE profit > 0) AS gross_profit,
    SUM(ABS(profit)) FILTER (WHERE profit < 0) AS gross_loss,
    AVG(profit) FILTER (WHERE profit > 0) AS avg_win,
    AVG(profit) FILTER (WHERE profit < 0) AS avg_loss
FROM journal.trades
GROUP BY day, account_id
WITH NO DATA;

-- Refresh policy: auto-refresh every hour
SELECT add_continuous_aggregate_policy(
    'journal.daily_stats',
    start_offset => INTERVAL '7 days',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour'
);
```

---

## Pydantic Response Schemas

```python
# app/schemas/journal.py
from pydantic import BaseModel
from decimal import Decimal

class PerformanceSummary(BaseModel):
    total_trades: int = 0
    wins: int = 0
    win_rate: Decimal = Decimal("0")
    total_pnl: Decimal = Decimal("0")
    profit_factor: Decimal | None = None
    avg_win: Decimal | None = None
    avg_loss: Decimal | None = None
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0

class CalendarDay(BaseModel):
    date: str          # ISO date "2024-03-15"
    pnl: Decimal
    trades: int

class JournalEntry(BaseModel):
    id: str
    trade_ticket: int
    account_id: str
    notes: str
    tags: list[str] = []
    screenshots: list[str] = []    # R2 object keys
    emotional_state: str | None = None  # "confident", "fearful", "neutral"
    created_at: datetime
```

---

## Anti-Patterns

```
✗ Computing drawdown in Python loop (10k+ trades — use SQL window functions)
✗ Missing NULL guards on profit_factor (division by zero on all-winning accounts)
✗ No TimescaleDB continuous aggregates (daily stats would be O(n) every request)
✗ Returning raw profit without currency context
✗ Mixing open and closed trades in performance stats (always filter status='closed')
✗ Sharpe ratio without annualization factor (√252 for daily data)
✗ Ignoring swap and commission in PnL calculations
✗ No pagination on trade history endpoint (10k trades crashes mobile)
```
