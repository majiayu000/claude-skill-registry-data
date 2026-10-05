---
name: fastapi-debug
description: Debug and troubleshoot ettametta's FastAPI application. Use when investigating middleware issues, authentication failures, route errors, dependency injection problems, CORS, rate limiting, or OpenAPI issues.
---
# FastAPI Debugging

## Quick Diagnostics

```bash
curl http://localhost:8000/health
curl http://localhost:8000/openapi.json | jq '.paths | keys' | head -30
curl http://localhost:8000/metrics | head -20
```

## Middleware Stack (outermost first)

| Order | Middleware | Purpose |
|---|---|---|
| 1 | GZipMiddleware | Compress responses >= 1KB |
| 2 | SecurityHeadersMiddleware | HSTS, X-Frame-Options, nosniff (prod only) |
| 3 | TracingMiddleware | X-Request-ID generation/propagation |
| 4 | RequestLoggingMiddleware | Log method, path, status, response time |
| 5 | CORSMiddleware | CORS with configurable origins |

## Route Structure

All routes under `/api/v1/` via `v1_router = APIRouter(prefix="/v1")`.

| Module | Prefix |
|---|---|
| routes/auth.py | /auth |
| routes/discovery.py | /discovery |
| routes/video_transform.py | /video |
| routes/video_generate.py | /video |
| routes/video_jobs.py | /video/jobs |
| routes/publish/ | /publish (sub-routers: oauth, publisher, scheduler, analytics, accounts, opencli) |
| routes/analytics.py | /analytics |
| routes/monetization.py | /monetization |
| routes/billing.py | /billing |
| routes/settings.py | /settings |
| routes/nexus.py | /nexus |
| routes/security.py | /security |
| routes/llm.py | /llm |
| routes/ws.py | /ws |
| routes/health.py | /health |
| routes/admin.py | /admin |

Special: `/health` (direct), `/static` (file serving), `/metrics` (Prometheus).

## Key Files

| File | Purpose |
|---|---|
| src/api/main.py | App init, middleware, startup events |
| src/api/utils/auth.py | get_current_user, admin_required, JWT decode |
| src/api/utils/security.py | Password hashing (bcrypt), JWT creation |
| src/api/utils/limiter.py | slowapi rate limiter with tiered keys |
| src/api/utils/database.py | get_db() dependency |
| src/api/utils/api_responses.py | success_response, error_response, PaginatedResponse |
| src/api/utils/errors.py | ErrorCode enum, ErrorResponse, factory functions |
| src/api/exception_handlers.py | Global exception handler registration |
| src/api/config/settings.py | Pydantic Settings singleton |

## Authentication

OAuth2 password bearer. Flow:
1. Extract JWT from `Authorization: Bearer <token>`
2. Check Redis blacklist (`token_blacklist` set)
3. Decode with python-jose (HS256, SECRET_KEY)
4. Extract `sub` (email), query UserDB

Route-level: `Depends(get_current_user)` or `Depends(admin_required)`.

## Error Handling

Custom hierarchy: APIError -> ValidationError(422), NotFoundError(404), AuthenticationError(401), AuthorizationError(403), RateLimitError(429), ExternalServiceError(502), ConflictError(409).

Standard format:
```json
{"error": {"code": "ERROR_CODE", "message": "...", "timestamp": "...", "details": {}}}
```

Catch-all persists to SelfHealingAuditDB.

## Rate Limiting

| Tier | Limit |
|---|---|
| FREE | 100/hr |
| PRO/PREMIUM/BASIC | 500/hr |
| SOVEREIGN/STUDIO | 5000/hr |

## Startup Events

1. Init Redis cache (FastAPICache)
2. Seed default monitored niches
3. Start hot-reload listener
4. sync_all_vitals() recovery
5. ConsistencySentinel loop
6. Agent Zero state recovery

## Common Issues

### CORS errors
Check: `docker compose exec api env | grep CORS_ORIGINS`

### 401 on valid token
Expired (24h default)? Blacklisted? SECRET_KEY mismatch?

### Rate limit 429
Check tier. Wait or adjust LIMIT_* env vars.

### Request ID missing
TracingMiddleware generates UUID4. If missing, middleware not registered.

### Health check fails
`/health` does `SELECT 1`. DB down = 500.
