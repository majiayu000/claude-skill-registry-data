---
name: celery-monitor
description: Monitor, debug, and troubleshoot Celery tasks and workers in ettametta. Use when investigating task failures, queue bottlenecks, worker health, or beat schedule issues. Covers task tracing, async bridge patterns, retry debugging, and worker architecture.
---
# Celery Monitoring & Debugging

Skill for diagnosing Celery task issues in ettametta — failures, queue congestion, missing traces, async/sync bridge bugs, and worker health.

## Quick Diagnostics

### Check worker health
```bash
# List active workers
celery -A src.api.utils.celery inspect active

# Check registered tasks
celery -A src.api.utils.celery inspect registered

# Check queue lengths (requires redis-cli)
redis-cli -p 7204 -a "$REDIS_PASSWORD" llen celery
redis-cli -p 7204 -a "$REDIS_PASSWORD" llen default
```

### Check beat schedule
```bash
# Dump the current beat schedule
celery -A src.api.utils.celery beat --dump_schedule
```

### Check task status via API
```bash
# Poll task result (uses AsyncResult)
curl http://localhost:8000/api/v1/discovery/analyze/{task_id}
```

## Architecture Reference

### Task Registry (20+ tasks across 8 modules)

| Module | Tasks | Retry Pattern |
|--------|-------|---------------|
| `video_engine/tasks.py` | 4 (download_and_process, generate, generate_story, narrative_fusion) | `autoretry_for=(Exception,)` + exponential backoff + jitter |
| `discovery/tasks.py` | 5 (sentinel_watcher, scan_trends, analyze_pattern, deep_scan, process_high_potential) | Manual error handling, no autoretry |
| `discovery/scanner_service.py` | 1 (scan_trending_content) | CircuitBreaker per platform |
| `nexus_engine/tasks.py` | 1 (create_cinema_video) | No retry |
| `optimization/scheduler_tasks.py` | 6 (check_and_post_scheduled, retry_failed_posts, retry_missed_schedules, cleanup_pending_videos, cleanup_old_scheduled, viral_loop_compilation) | Mixed: some autoretry, some DB-level retry |
| `security/tasks.py` | 1 (system_audit) | No retry, synchronous |
| `storage/tasks.py` | 1 (manage_lifecycle) | No retry |
| `openclaw/tasks.py` | 1 (ettametta_polling) | No retry, synchronous |

### Key Files

| File | Purpose |
|------|---------|
| `src/api/utils/celery.py` | App init, broker/backend config, beat schedule, OTEL instrumentation |
| `src/api/utils/tracing.py` | Request ID context var (`request_id_var`) and TracingFilter |
| `src/shared/observability.py` | OTEL TracerProvider setup, JSON structured logging |
| `src/services/video_engine/tasks.py` | `run_async()` bridge helper, video task definitions |
| `src/api/utils/resilience.py` | CircuitBreaker implementation |

### Beat Schedule (9 periodic tasks)

| Schedule | Task | Interval |
|----------|------|----------|
| `sentinel-trend-watcher-4h` | `discovery.sentinel_watcher` | 4h |
| `scan-trending-content-2h` | `scan_trending_content` | 2h |
| `check-scheduled-posts-5m` | `optimization.check_and_post_scheduled` | 5m |
| `retry-missed-schedules-5m` | `optimization.retry_missed_schedules` | 5m |
| `system-security-audit-daily` | `security.system_audit` | 24h |
| `storage-lifecycle-manager-daily` | `storage.manage_lifecycle` | 24h |
| `ettametta-job-polling-10m` | `openclaw.ettametta_polling` | 10m |
| `viral-loop-compilation-12h` | `optimization.viral_loop_compilation` | 12h |
| `autonomous-nexus-trigger-1h` | `discovery.process_high_potential` | 1h |

## Common Issues & Fixes

### Task has no request_id in logs

Only video_engine tasks call `set_request_id()`. Discovery, security, storage, and openclaw tasks produce logs without request correlation. Fix by adding at task entry:

```python
from src.api.utils.tracing import set_request_id

@celery_app.task(bind=True)
def my_task(self, ...):
    set_request_id(self.request.id)
    # ... rest of task
```

### Async code blocking the worker

Three inconsistent async bridge patterns exist. Use the video_engine pattern (safest):

```python
import asyncio

def run_async(coro):
    """Run async coroutine from sync Celery task. Creates fresh loop per call."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)
```

Do NOT use bare `asyncio.run()` — it creates and destroys the loop, which breaks libraries that cache loop references.

### Non-retryable errors still retrying

Video tasks use a fragile pattern that manipulates `self.request.retries` directly. Instead, raise a custom exception and exclude it from `autoretry_for`:

```python
class NonRetryableError(Exception):
    pass

@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def my_task(self, ...):
    try:
        ...
    except SomeError as e:
        if is_non_retryable(e):
            raise NonRetryableError(str(e)) from e  # Won't be retried
        raise  # Will be retried by autoretry_for
```

### Worker crashes lose tasks silently

No `acks_late` or `task_reject_on_worker_lost` is configured. Add to celery.py:

```python
celery_app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_track_started=True,
)
```

### Long-running tasks hang indefinitely

No `time_limit` or `soft_time_limit` is set on any task. Add per-task:

```python
@celery_app.task(
    bind=True,
    soft_time_limit=600,   # SIGTERM after 10 min
    time_limit=660,        # SIGKILL after 11 min
)
```

## Docker Services

```bash
# Restart workers
docker compose restart celery_worker celery_beat

# View worker logs
docker compose logs -f celery_worker

# Scale workers (limited by shared default queue)
docker compose up -d --scale celery_worker=3
```

## Debugging Checklist

1. Is the task registered? `celery -A src.api.utils.celery inspect registered`
2. Is the worker consuming? `celery -A src.api.utils.celery inspect active`
3. Is Redis reachable? `redis-cli -p 7204 ping`
4. Is the task in the queue? `redis-cli -p 7204 llen celery`
5. Check worker logs: `docker compose logs --tail=100 celery_worker`
6. Check OTEL traces if configured (OTLP endpoint in `observability.py`)

## References

- [Retry Patterns Deep Dive](references/retry-patterns.md)
- [Async Bridge Patterns](references/async-bridge.md)
