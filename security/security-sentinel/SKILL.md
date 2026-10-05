---
name: security-sentinel
description: Debug and troubleshoot ettametta's SecuritySentinel — system integrity monitoring, threat detection, audit logging, and vulnerability scanning. Use when health scores drop, audits fail, or threat levels spike.
---
# Security Sentinel Debugging

The SecuritySentinel monitors system integrity, API anomalies, and vulnerability exposure. Runs a daily Celery audit and maintains a rolling event log.

## Quick Diagnostics

```bash
# Health score and threat level
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/security/status

# Manual audit trigger (admin only)
curl -X POST -H "Authorization: Bearer $ADMIN_TOKEN" http://localhost:8000/api/v1/security/scan

# Recent events
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/security/events

# Redis sentinel logs
redis-cli -p 7204 -a "$REDIS_PASSWORD" lrange sentinel:security_logs 0 20

# Audit reports in Redis
redis-cli -p 7204 -a "$REDIS_PASSWORD" keys "sentinel:security_health:*"

# DB audit logs
docker compose exec -T db psql -U ettametta -d ettametta -c "SELECT id, action, resource_type, created_at FROM audit_logs ORDER BY created_at DESC LIMIT 10;"
```

## Architecture

### SecuritySentinel Class (`src/services/security/service.py`)

Singleton: `base_security_service`

Monitors:
- **System integrity** — SECRET_KEY validation, `.env` file permissions, port scanning (SSH/DB/Redis on localhost)
- **Health scoring** — Base 100, penalties: -20 per critical event, -30 for Redis down, -15/10 for missing API keys
- **API request anomalies** — Per-IP tracking in Redis (5-min window), flags at >100 requests
- **Vulnerability scanning** — grep-based detection of DEBUG mode and hardcoded secrets in `/app`
- **Threat categorization** — Last 100 events aggregated into LOW/MEDIUM/HIGH/CRITICAL/NOMINAL

### Celery Task

`security.system_audit` — runs daily (86400s interval). Calls `audit_system_integrity()`, logs score and findings.

### Key Files

| File | Purpose |
|------|---------|
| `src/services/security/service.py` | `SecuritySentinel` class, integrity checks, anomaly detection |
| `src/services/security/tasks.py` | Celery task wrapper for daily audit |
| `src/api/routes/security.py` | REST API — status, scan, events, bias-scan |
| `src/api/utils/models.py` | `AuditLogDB`, `SelfHealingAuditDB` models |
| `src/api/utils/limiter.py` | SlowAPI rate limiter with tiered keys |

### DB Models

| Model | Purpose |
|-------|---------|
| `AuditLogDB` | General audit trail: user_id, action, resource_type, resource_id, details (JSON), ip_address, user_agent |
| `SelfHealingAuditDB` | Fault persistence: path, method, exception_type, message, traceback, resolved, resolution_notes |

### Redis Key Patterns

| Key | TTL | Purpose |
|-----|-----|---------|
| `sentinel:security_logs` | None (trim 1000) | Rolling event list (LPUSH) |
| `sentinel:security_health:audit:{date}` | 7d | Daily audit report |
| `security:requests:{client_ip}` | 5m | Per-IP request rate tracking |
| `sentinel:security_health` | Default | Cached vulnerability scan results |

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/security/errors` | POST | Public | Frontend error ingestion |
| `/security/status` | GET | User | Health score + threat breakdown |
| `/security/scan` | POST | Admin | Manual integrity audit |
| `/security/events` | GET | User | Raw sentinel event log |
| `/security/bias-scan` | POST | User | Neural bias neutrality scan |

## Common Issues

### Health score drops below 80
Check which penalties fired:
```bash
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/security/status | jq '.threat_breakdown'
```

### Daily audit not running
Check Celery beat schedule:
```bash
celery -A src.api.utils.celery inspect scheduled | grep security
```
Also check Redis for today's report:
```bash
redis-cli -p 7204 -a "$REDIS_PASSWORD" get "sentinel:security_health:audit:$(date +%Y-%m-%d)"
```

### SelfHealingAuditDB growing unbounded
Catch-all exception handler persists to this table. Check size:
```bash
docker compose exec -T db psql -U ettametta -d ettametta -c "SELECT count(*) FROM self_healing_audit;"
```
The `storage.manage_lifecycle` task does NOT clean this table. May need manual pruning.

### Per-IP rate tracking false positives
Redis keys `security:requests:{ip}` have 5-min TTL but >100 requests triggers a flag. In containerized setups, all requests may appear from the same gateway IP.

### Vulnerability scan false positives
The grep-based scanner flags any string matching common secret patterns. False positives from comments, docs, or test fixtures are expected. Check `self_healing_audit.resolved` for known issues.

## Rate Limiting Integration

SlowAPI handles tiered rate limits (FREE/PRO/SOVEREIGN). The sentinel adds its own IP-based anomaly detection on top. These are independent systems — a request can pass SlowAPI limits but still trigger sentinel flags.

## Debugging Checklist

1. Health score: `GET /security/status`
2. Recent events: `GET /security/events`
3. Redis logs: `redis-cli lrange sentinel:security_logs 0 20`
4. Daily audit: `redis-cli get sentinel:security_health:audit:{date}`
5. Audit logs in DB: `SELECT count(*) FROM audit_logs`
6. Self-healing backlog: `SELECT count(*) FROM self_healing_audit WHERE resolved = false`
7. Celery task active: `celery inspect active | grep security`
