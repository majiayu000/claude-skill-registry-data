---
name: performance-engineering
description: Performance Engineering — Institutional capability and runbook for performance-engineering.
---

# SKILL: Performance Engineering
## Domain: Query Optimization, Caching, Response Budgets, Profiling

**Activation triggers:** slow query, N+1 problem, cache strategy, pagination,
response time budget, database index, Redis cache, query explain, profiling,
lazy loading, connection pool.

---

## Performance Budgets

```
API Response Time Targets (P99):
  - Auth endpoints:           < 200ms
  - Broker account info:      < 500ms  (includes MT5 call)
  - Trade history (paginated):< 300ms
  - Performance analytics:    < 800ms  (complex aggregations)
  - WebSocket message latency:< 100ms

Frontend Core Web Vitals:
  - LCP (Largest Contentful Paint): < 2.5s
  - INP (Interaction to Next Paint): < 200ms
  - CLS (Cumulative Layout Shift):   < 0.1

Database Query Targets:
  - Simple lookups:   < 10ms
  - Analytics queries:< 500ms
  - Bulk inserts:     < 1s for 1000 rows
```

---

## N+1 Query Prevention

```python
# WRONG — N+1: 1 query for accounts + N queries for each position list
accounts = await db.execute(select(BrokerAccount).where(...))
for account in accounts:
    positions = await db.execute(select(Position).where(Position.account_id == account.id))

# CORRECT — single query with explicit join
result = await db.execute(
    select(BrokerAccount, Position)
    .outerjoin(Position, Position.account_id == BrokerAccount.id)
    .where(BrokerAccount.user_id == user_id)
    .options(selectinload(BrokerAccount.positions))   # SQLAlchemy batches subquery
)

# ALSO CORRECT — selectinload for relationships
result = await db.execute(
    select(CopySubscription)
    .options(
        selectinload(CopySubscription.provider),
        selectinload(CopySubscription.execution_logs).limit(10),
    )
    .where(CopySubscription.subscriber_id == user_id)
)
```

---

## Redis Caching Strategy

```python
# app/core/cache.py
import json
from functools import wraps
from typing import Any, Callable
import aioredis
from app.core.config import settings

class Cache:
    def __init__(self):
        self.redis: aioredis.Redis | None = None

    async def connect(self):
        self.redis = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)

    async def get(self, key: str) -> Any | None:
        if not self.redis:
            return None
        raw = await self.redis.get(key)
        return json.loads(raw) if raw else None

    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        if self.redis:
            await self.redis.setex(key, ttl, json.dumps(value, default=str))

    async def delete(self, key: str) -> None:
        if self.redis:
            await self.redis.delete(key)

    async def invalidate_prefix(self, prefix: str) -> None:
        """Delete all keys matching prefix:* — use sparingly."""
        if self.redis:
            keys = await self.redis.keys(f"{prefix}:*")
            if keys:
                await self.redis.delete(*keys)

cache = Cache()

# Cache TTL reference:
CACHE_TTL = {
    "performance_summary": 300,   # 5min — analytics are expensive
    "provider_list":       60,    # 1min — provider stats change often
    "symbol_info":         3600,  # 1hr  — symbol metadata rarely changes
    "account_info":        30,    # 30s  — balance updates frequently
}
```

---

## Query Optimization with EXPLAIN ANALYZE

```python
# Development helper — wrap slow queries with EXPLAIN ANALYZE
async def explain_query(db: AsyncSession, query) -> None:
    """Log query execution plan for optimization."""
    import re
    explain = text(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query.compile(compile_kwargs={'literal_binds': True})}")
    result = await db.execute(explain)
    plan = result.fetchone()[0][0]
    logger.debug("Query plan", extra={
        "execution_time_ms": plan["Execution Time"],
        "planning_time_ms": plan["Planning Time"],
        "plan": plan["Plan"],
    })

# Key metrics to look for in EXPLAIN output:
# - "Seq Scan" on large tables → needs index
# - "Nested Loop" with high rows → N+1 pattern
# - "Hash Join" on filtered small set → usually fine
# - Actual vs Estimated rows diverging by 10x+ → stale statistics (ANALYZE)
```

---

## Database Index Strategy

```sql
-- Always add indexes for:
-- 1. Foreign keys (SQLAlchemy doesn't auto-create these in PostgreSQL)
-- 2. Columns used in WHERE clauses on large tables
-- 3. Columns used in ORDER BY on paginated queries
-- 4. Partial indexes for filtered queries

-- Trade history — most common query pattern
CREATE INDEX CONCURRENTLY idx_trades_account_closed
    ON journal.trades (account_id, closed_at DESC)
    WHERE status = 'closed';

-- Provider signal routing
CREATE INDEX CONCURRENTLY idx_provider_signals_provider_created
    ON copy_trading.provider_signals (provider_id, created_at DESC);

-- Active subscriptions
CREATE INDEX CONCURRENTLY idx_subscriptions_active
    ON copy_trading.subscriptions (provider_id)
    WHERE is_active = TRUE;

-- TimescaleDB — always chunk_time_interval matches your query range
SELECT add_dimension('journal.equity_snapshots', 'account_id', number_partitions => 4);
```

---

## Pagination Pattern

```python
# All list endpoints use cursor-based pagination for large datasets
# Offset pagination degrades at high offsets (OFFSET 10000 scans 10000 rows)

from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class PagedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int
    has_more: bool

async def get_trades_paginated(
    db: AsyncSession,
    account_id: str,
    limit: int = 50,
    offset: int = 0,
    from_dt: datetime | None = None,
    to_dt: datetime | None = None,
) -> PagedResponse:
    base_query = (
        select(Trade)
        .where(
            Trade.account_id == account_id,
            Trade.status == "closed",
            Trade.deleted_at.is_(None),
        )
    )
    if from_dt:
        base_query = base_query.where(Trade.closed_at >= from_dt)
    if to_dt:
        base_query = base_query.where(Trade.closed_at <= to_dt)

    # Count (cached separately — avoid recount on every page flip)
    count_result = await db.execute(select(func.count()).select_from(base_query.subquery()))
    total = count_result.scalar_one()

    items_result = await db.execute(
        base_query.order_by(Trade.closed_at.desc()).limit(limit).offset(offset)
    )
    items = items_result.scalars().all()

    return PagedResponse(items=items, total=total, limit=limit, offset=offset, has_more=offset + len(items) < total)
```

---

## Frontend Performance

```typescript
// Code splitting — lazy load heavy modules
const imCharts = lazy(() => import('@/modules/expert/imCharts'));
const imJournal = lazy(() => import('@/modules/expert/imJournal'));
const imCopying = lazy(() => import('@/modules/expert/imCopying'));

// Memoize expensive selectors
const filteredTrades = useMemo(
  () => trades.filter(t => t.symbol === selectedSymbol && t.status === 'closed'),
  [trades, selectedSymbol],
);

// Debounce search inputs
const debouncedSearch = useMemo(
  () => debounce((q: string) => setSearchQuery(q), 300),
  [],
);

// React Query staleTime — avoid unnecessary refetches
const { data } = useQuery({
  queryKey: ['performance', accountId, dateRange],
  queryFn: fetchPerformance,
  staleTime: 5 * 60 * 1000,   // 5 minutes — performance data doesn't change in real-time
  gcTime: 10 * 60 * 1000,     // keep in cache 10 minutes
});
```

---

## Anti-Patterns

```
✗ SELECT * in queries (always list explicit columns)
✗ Offset pagination > 5000 rows (use cursor-based or keyset)
✗ Missing index on foreign key columns (causes seq scans on JOINs)
✗ Caching user-specific data with shared keys (cache key must include user_id)
✗ Infinite cache TTL (stale data in trading context is dangerous)
✗ N+1 queries with lazy loading ORM relationships
✗ Synchronous MT5 calls in request path (P99 > 5s)
✗ Rendering all trades without virtual scroll (DOM crash at 1000+ rows)
✗ Re-fetching analytics on every component mount (use staleTime)
```
