---
name: network-tracing
description: Instrument API requests with spans and distributed tracing. Use when tracking request latency, correlating client-backend traces, or debugging API issues.
triggers:
  - "correlate backend traces"
  - "distributed tracing"
  - "network performance"
  - "slow API calls"
  - "trace requests"
  - "track API requests"
priority: 2
---

# Network Tracing

Measure API requests and correlate with backend traces.

## What to Capture (OTel-Compatible Names)

| Attribute | OTel Name | Purpose |
|-----------|-----------|---------|
| Method | `http.request.method` | GET, POST, etc. |
| Status | `http.response.status_code` | Success/failure |
| URL | `url.path` | Endpoint (sanitized) |
| Duration | `http.request.duration` | Request time (ms) |
| Size | `http.response.body.size` | Payload bytes |

Using OTel naming = easier migration when OTel mobile matures.
See `references/otel-mobile.md` for rationale.

## Distributed Tracing

Propagate trace context to backend:

```
Client Request
    │
    ├── traceparent: 00-{trace_id}-{span_id}-01
    ├── X-Request-Id: {uuid}
    └── X-Session-Id: {session}
         │
         ▼
    Backend (correlates logs with trace_id)
```

## Key Thresholds

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| API p50 | <500ms | <1s | >1s |
| API p95 | <2s | <5s | >5s |
| Error rate | <1% | <3% | >3% |

## Integration Options

**Choose based on existing vendor:**

| Vendor | iOS | Android | Approach |
|--------|-----|---------|----------|
| Sentry | Auto URLSession swizzling | OkHttp integration | Automatic |
| Datadog | URLSession delegate | OkHttp interceptor | Semi-auto |
| Embrace | Auto-instrumentation | Auto-instrumentation | Automatic |
| Custom | Manual interceptor | Manual interceptor | Manual |

**Automatic (swizzling):** Less code, may miss custom clients
**Manual (interceptors):** More control, works with any HTTP client

## Platform Integration Points

| Platform | Manual Option | Works With |
|----------|---------------|------------|
| iOS | URLSession delegate | All URLSession-based clients |
| iOS | Alamofire EventMonitor | Alamofire |
| Android | OkHttp Interceptor | OkHttp, Retrofit |
| Android | Ktor HttpClientPlugin | Ktor |
| RN | fetch wrapper | Native fetch |
| RN | axios interceptor | axios |

## Implementation

See `references/mobile-challenges.md` (Client-Backend Correlation) for:
- W3C trace header format
- Platform-specific interceptor code
- Backend log correlation patterns

See `references/performance.md` (Network section) for latency budgets.
