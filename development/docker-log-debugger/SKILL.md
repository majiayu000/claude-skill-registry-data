---
name: docker-log-debugger
description: Find and debug errors using Docker Compose logs. Use proactively when tests fail or services misbehave. PRIMARY - docker compose logs --since 15m | grep -iE -B 10 -A 10 "error|fail|exception"
---

# Docker Log Debugger

Find and debug errors by examining Docker container logs.

## Primary Command (Use This First!)
```bash
docker compose logs --since 15m | grep -iE -B 10 -A 10 "error|fail|exception"
```

Shows all errors from last 15 minutes with 10 lines of context before/after each match.

## When to Use

Use proactively when:
- Tests fail
- API endpoints return errors
- Worker jobs don't process
- Database/Redis connection issues
- Any service misbehaves

## Project Services

1. **api** - FastAPI (webhooks, HTTP endpoints)
2. **worker** - RQ worker (async jobs, enrichment, interventions)
3. **datastore** - PostgreSQL with pgvector
4. **redis** - Job queue

## Common Commands

```bash
# View all services (last 5 min)
docker compose logs --since 5m

# View specific service
docker compose logs api --since 5m
docker compose logs worker --since 5m

# Follow logs in real-time
docker compose logs -f api worker

# View last N lines
docker compose logs --tail 100 worker

# Search for specific patterns
docker compose logs worker --since 5m | grep -i "KeyError"
docker compose logs api --since 5m | grep -i "connection"
docker compose logs worker --since 5m | grep -i "langfuse"

# Service health
docker compose ps
docker compose restart worker
```

## Time Filters

Use with `--since`: `5m`, `10m`, `1h`, `30s`, `2h30m`

## Quick Debugging

### Test Failed
```bash
docker compose logs --since 15m | grep -iE -B 10 -A 10 "error|fail|exception"
docker compose ps  # Check if services are running
```

### Worker Job Issues
```bash
docker compose logs worker --since 5m | grep -i "exception\|error"
docker compose logs worker --since 5m | grep -i "job\|enrich"
```

### API Errors
```bash
docker compose logs api --since 5m | grep -E "(400|401|404|500|503)"
docker compose logs api --since 5m | grep -A 10 "Traceback"
```

### Database/Redis Issues
```bash
docker compose logs datastore --since 5m
docker compose logs api worker --since 5m | grep -i "connection\|postgres\|redis"
```

### Langfuse Errors
```bash
docker compose logs worker --since 5m | grep -i "langfuse\|prompt.*not found"
```

## Common Error Patterns

| Error | Check |
|-------|-------|
| `KeyError: 'field'` | Fetch Langfuse prompt to see actual schema |
| `Connection refused` | `docker compose ps` - check service status |
| `ModuleNotFoundError` | May need `docker compose build api worker` |
| `Job not found` | Check Redis running, worker processing jobs |
| `OpenAI API error` | Verify OPENAI_API_KEY, check rate limits |
| `alembic` errors | Run migrations: `docker compose exec api alembic upgrade head` |

## Quick Reference

```bash
# 🔥 Find all errors with context
docker compose logs --since 15m | grep -iE -B 10 -A 10 "error|fail|exception"

# Service status
docker compose ps

# Restart services
docker compose restart

# Full reset
docker compose down && docker compose up -d

# Watch live
docker compose logs -f api worker

# Save for analysis
docker compose logs --since 15m > debug.log
```
