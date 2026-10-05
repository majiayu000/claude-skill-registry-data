---
name: db-performance
description: Debug and troubleshoot database performance in ettametta. Use when investigating slow queries, connection pool issues, migration conflicts, N+1 patterns, or schema drift.
---
# Database Performance Debugging

## Quick Diagnostics

```bash
# Connection count
docker compose exec db psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# Active queries
docker compose exec db psql -U postgres -c "SELECT pid, now()-query_start AS duration, query FROM pg_stat_activity WHERE state='active' ORDER BY duration DESC;"

# Table sizes
docker compose exec db psql -U postgres -c "SELECT relname, n_live_tup, pg_size_pretty(pg_total_relation_size(relid)) FROM pg_stat_user_tables ORDER BY n_live_tup DESC;"

# Migration state
alembic heads
alembic current
alembic check
```

## Connection Configuration

**Async engine (FastAPI):** `pool_pre_ping=True`, defaults pool_size=5, max_overflow=10

**Sync engine (Celery):** Default QueuePool, pool_size=5, max_overflow=10

**Celery task-scoped:** pool_size=2, max_overflow=0 (tight isolation)

**NullPool for Celery workers:** Fresh engine per call, disposed after use. Expensive but avoids event-loop conflicts.

**Default DATABASE_URL:** `sqlite:///./data/db/ettametta.db`. Production uses PostgreSQL.

## Session Management

- **Pattern A (routes):** `get_db()` dependency with rollback on exception
- **Pattern B (services):** `async_session_factory()` inline
- **Pattern C (Celery):** `get_async_session()` with NullPool

All use `expire_on_commit=False`, `autocommit=False`, `autoflush=False`.

## Models

35 ORM models. **Zero `relationship()` declarations** — all cross-table access via explicit joins.

Key models: UserDB (7 unique indexes), ContentCandidateDB (external_id unique, niche, region), VideoJobDB, PublishedContentDB, ScheduledPostDB, SocialAccount.

### Missing indexes (potential)
- video_jobs.user_id
- audit_logs.user_id
- scheduled_posts.user_id
- nexus_jobs.user_id

No composite indexes declared.

## Migrations

20 migration files. Current HEAD: `d410fb0d40a9`. 2 merge migrations exist.

**CI/CD bypasses Alembic:** Deployment uses `create_all()` not `alembic upgrade head`.

## Query Patterns

### N+1 risks
- Nexus stats: 4 separate COUNT(*) queries (lines 482-506 in routes/nexus.py). Fix: single GROUP BY.
- Settings: 2 separate queries for system + user settings. Fix: join.

### In-memory pagination
Discovery routes use `paginate_list()` — loads all then slices. Use SQL `.offset().limit()`.

## DateTime Monkeypatch
`database.py` lines 12-24: strips timezone info from DateTime. Workaround for SQLite/PG compat.

## Common Issues

### Connection pool exhaustion
```bash
docker compose exec db psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"
```

### Stale connections
Async engine has `pool_pre_ping=True`. Sync engine does not.

### NullPool performance
`get_async_session()` creates/disposes full engine per call. Expensive for high-frequency ops.

### Missing composite indexes
Queries on multiple columns do sequential scans. Add `Index()` declarations.

### expire_on_commit=False
Correct for async but means stale data if objects reused after commit without refresh.
