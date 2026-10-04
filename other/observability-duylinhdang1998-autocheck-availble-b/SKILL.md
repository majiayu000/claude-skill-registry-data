---
name: observability
description: Production observability from Google SRE and Netflix. Use when implementing structured logging, setting up metrics collection (Prometheus, Datadog, CloudWatch), configuring distributed tracing (Jaeger, OpenTelemetry), creating dashboards (Grafana), defining alert rules, or building observability pipelines. Triggers on logging, monitoring, tracing, metrics, alerts, dashboards, Prometheus, Grafana, OpenTelemetry, or production observability.
---

# Observability - Logging, Monitoring & Tracing

**Purpose**: Implement comprehensive observability for production systems with logs, metrics, and distributed tracing

**Agent**: Google SRE / Netflix Backend Architect
**Use When**: Setting up monitoring, debugging production issues, or ensuring system reliability

---

## Three Pillars of Observability

### 1. Logging (What happened?)
### 2. Metrics (How much/how fast?)
### 3. Tracing (Where did it happen?)

---

## 1. Structured Logging

```typescript
import pino from 'pino'

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label })
  }
})

// Structured logs (JSON)
logger.info({ userId: 123, action: 'login' }, 'User logged in')
logger.error({ error: err, userId: 123 }, 'Failed to process payment')

// Request logging middleware
app.use((req, res, next) => {
  req.log = logger.child({
    requestId: crypto.randomUUID(),
    method: req.method,
    url: req.url,
    ip: req.ip
  })

  req.log.info('Request started')

  res.on('finish', () => {
    req.log.info({
      statusCode: res.statusCode,
      duration: Date.now() - req.startTime
    }, 'Request completed')
  })

  next()
})
```

**Best Practices**:
- Use JSON format for easy parsing
- Include context (requestId, userId, etc.)
- Log levels: ERROR, WARN, INFO, DEBUG
- Don't log sensitive data (passwords, tokens)
- Use correlation IDs across services

---

## 2. Metrics (Prometheus + Grafana)

```typescript
import { register, Counter, Histogram, Gauge } from 'prom-client'

// HTTP request counter
const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status']
})

// HTTP request duration
const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10]
})

// Active connections
const activeConnections = new Gauge({
  name: 'active_connections',
  help: 'Number of active connections'
})

// Metrics middleware
app.use((req, res, next) => {
  const start = Date.now()

  activeConnections.inc()

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000

    httpRequestsTotal.inc({
      method: req.method,
      route: req.route?.path || req.path,
      status: res.statusCode
    })

    httpRequestDuration.observe({
      method: req.method,
      route: req.route?.path || req.path,
      status: res.statusCode
    }, duration)

    activeConnections.dec()
  })

  next()
})

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType)
  res.end(await register.metrics())
})
```

**Key Metrics to Track**:
- Request rate (requests/second)
- Error rate (errors/second)
- Response time (p50, p95, p99)
- Database query time
- Cache hit rate
- CPU/Memory usage
- Active connections

---

## 3. Distributed Tracing (OpenTelemetry)

```typescript
import { NodeTracerProvider } from '@opentelemetry/sdk-trace-node'
import { registerInstrumentations } from '@opentelemetry/instrumentation'
import { HttpInstrumentation } from '@opentelemetry/instrumentation-http'
import { ExpressInstrumentation } from '@opentelemetry/instrumentation-express'
import { JaegerExporter } from '@opentelemetry/exporter-jaeger'

// Set up tracer
const provider = new NodeTracerProvider()

provider.addSpanProcessor(
  new SimpleSpanProcessor(
    new JaegerExporter({
      endpoint: 'http://localhost:14268/api/traces'
    })
  )
)

provider.register()

// Auto-instrument HTTP and Express
registerInstrumentations({
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation()
  ]
})

// Manual instrumentation
import { trace } from '@opentelemetry/api'

const tracer = trace.getTracer('my-service')

app.post('/api/orders', async (req, res) => {
  const span = tracer.startSpan('create-order')

  try {
    span.setAttribute('userId', req.user.id)
    span.setAttribute('orderTotal', req.body.total)

    // Create order
    const order = await db.order.create({ data: req.body })

    // Child span for payment
    const paymentSpan = tracer.startSpan('process-payment', {
      parent: span
    })

    await processPayment(order.id)
    paymentSpan.end()

    span.setStatus({ code: SpanStatusCode.OK })
    res.json(order)
  } catch (error) {
    span.recordException(error)
    span.setStatus({ code: SpanStatusCode.ERROR })
    res.status(500).json({ error: 'Failed to create order' })
  } finally {
    span.end()
  }
})
```

---

## 4. Application Performance Monitoring (APM)

**Popular Tools**:
- Datadog APM
- New Relic
- Elastic APM
- Sentry (error tracking)

```typescript
import * as Sentry from '@sentry/node'

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1 // Sample 10% of transactions
})

// Sentry middleware
app.use(Sentry.Handlers.requestHandler())
app.use(Sentry.Handlers.tracingHandler())

// Error handler (must be last)
app.use(Sentry.Handlers.errorHandler())

// Manual error tracking
try {
  await dangerousOperation()
} catch (error) {
  Sentry.captureException(error, {
    user: { id: userId, email: userEmail },
    tags: { operation: 'payment' },
    extra: { orderId: order.id }
  })
}
```

---

## 5. Health Checks

```typescript
// Liveness probe (is app running?)
app.get('/health/live', (req, res) => {
  res.json({ status: 'ok' })
})

// Readiness probe (is app ready to serve traffic?)
app.get('/health/ready', async (req, res) => {
  try {
    // Check database
    await db.$queryRaw`SELECT 1`

    // Check Redis
    await redis.ping()

    // Check external APIs
    await fetch('https://api.example.com/health', { timeout: 2000 })

    res.json({ status: 'ok', checks: { db: 'ok', redis: 'ok', api: 'ok' } })
  } catch (error) {
    res.status(503).json({ status: 'error', error: error.message })
  }
})
```

---

## 6. Alerting

```yaml
# Prometheus alert rules
groups:
  - name: api_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"

      - alert: SlowResponse
        expr: histogram_quantile(0.95, http_request_duration_seconds) > 1
        for: 10m
        annotations:
          summary: "95th percentile response time > 1s"
```

---

## Best Practices

1. **Use correlation IDs** across logs, metrics, and traces
2. **Sample traces** in production (not 100%)
3. **Set up alerts** for SLOs (error rate, latency)
4. **Dashboard for each service** (Grafana)
5. **Centralized logging** (Elasticsearch, CloudWatch)
6. **Monitor business metrics** (orders/hour, revenue)

---

**Remember**: You can't fix what you can't see. Implement observability from day one.

**Created**: 2026-02-04
**Maintained By**: Google SRE
