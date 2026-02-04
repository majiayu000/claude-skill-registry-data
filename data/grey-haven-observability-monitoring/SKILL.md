---
name: grey-haven-observability-monitoring
description: Implement observability and monitoring using Cloudflare Workers Analytics, wrangler tail for logs, and health checks. Use when setting up monitoring, implementing logging, configuring alerts, or debugging production issues.
# v2.0.43: Skills to auto-load for observability work
skills:
  - grey-haven-code-style
  - grey-haven-deployment-cloudflare
# v2.0.74: Tools for observability implementation
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Grey Haven Observability and Monitoring

Implement comprehensive monitoring for Grey Haven applications using **Cloudflare Workers** built-in observability tools.

## Observability Stack

### Grey Haven Monitoring Architecture

- **Logging**: Cloudflare Workers logs + wrangler tail
- **Metrics**: Cloudflare Workers Analytics dashboard
- **Custom Events**: Cloudflare Analytics Engine
- **Health Checks**: Cloudflare Health Checks for endpoint availability
- **Error Tracking**: Console errors visible in Cloudflare dashboard

## Cloudflare Workers Logging

### Console Logging in Workers

```typescript
// app/utils/logger.ts
export interface LogEvent {
  level: "debug" | "info" | "warn" | "error";
  message: string;
  context?: Record<string, unknown>;
  userId?: string;
  tenantId?: string;
  requestId?: string;
  duration?: number;
}

export function log(event: LogEvent) {
  const logData = {
    timestamp: new Date().toISOString(),
    level: event.level,
    message: event.message,
    environment: process.env.ENVIRONMENT,
    user_id: event.userId,
    tenant_id: event.tenantId,
    request_id: event.requestId,
    duration_ms: event.duration,
    ...event.context,
  };

  // Structured console logging (visible in Cloudflare dashboard)
  console[event.level](JSON.stringify(logData));
}

// Convenience methods
export const logger = {
  debug: (message: string, context?: Record<string, unknown>) =>
    log({ level: "debug", message, context }),
  info: (message: string, context?: Record<string, unknown>) =>
    log({ level: "info", message, context }),
  warn: (message: string, context?: Record<string, unknown>) =>
    log({ level: "warn", message, context }),
  error: (message: string, context?: Record<string, unknown>) =>
    log({ level: "error", message, context }),
};
```

### Logging Middleware

```typescript
// app/middleware/logging.ts
import { logger } from "~/utils/logger";
import { v4 as uuidv4 } from "uuid";

export async function loggingMiddleware(
  request: Request,
  next: () => Promise<Response>
) {
  const requestId = uuidv4();
  const startTime = Date.now();

  try {
    const response = await next();
    const duration = Date.now() - startTime;

    logger.info("Request completed", {
      request_id: requestId,
      method: request.method,
      url: request.url,
      status: response.status,
      duration_ms: duration,
    });

    return response;
  } catch (error) {
    const duration = Date.now() - startTime;

    logger.error("Request failed", {
      request_id: requestId,
      method: request.method,
      url: request.url,
      error: error.message,
      stack: error.stack,
      duration_ms: duration,
    });

    throw error;
  }
}
```

## Cloudflare Workers Analytics

### Workers Analytics Dashboard

Access metrics at: `https://dash.cloudflare.com → Workers → Analytics`

**Key Metrics**:
- Request rate (requests/second)
- CPU time (milliseconds)
- Error rate (%)
- Success rate (%)
- Response time (P50, P95, P99)
- Invocations per day
- GB-seconds (compute usage)

### Wrangler Tail (Real-time Logs)

```bash
# Stream production logs
npx wrangler tail --config wrangler.production.toml

# Filter by status code
npx wrangler tail --status error --config wrangler.production.toml

# Filter by method
npx wrangler tail --method POST --config wrangler.production.toml

# Filter by IP address
npx wrangler tail --ip 1.2.3.4 --config wrangler.production.toml

# Output to file
npx wrangler tail --config wrangler.production.toml > logs.txt
```

### Accessing Logs in Cloudflare Dashboard

1. Go to `https://dash.cloudflare.com`
2. Navigate to Workers & Pages
3. Select your Worker
4. Click "Logs" tab
5. View real-time logs with filtering

**Log Features**:
- Real-time streaming
- Filter by status code
- Filter by request method
- Search log content
- Export logs (JSON)

## Analytics Engine (Custom Events)

### Setup Analytics Engine

**wrangler.toml**:
```toml
[[analytics_engine_datasets]]
binding = "ANALYTICS"
```

### Track Custom Events

```typescript
// app/utils/analytics.ts
export async function trackEvent(
  env: Env,
  eventName: string,
  data: {
    user_id?: string;
    tenant_id?: string;
    duration_ms?: number;
    [key: string]: string | number | undefined;
  }
) {
  try {
    await env.ANALYTICS.writeDataPoint({
      blobs: [eventName],
      doubles: [data.duration_ms || 0],
      indexes: [data.user_id || "", data.tenant_id || ""],
    });
  } catch (error) {
    console.error("Failed to track event:", error);
  }
}

// Usage in server function
export const loginUser = createServerFn({ method: "POST" }).handler(
  async ({ data, context }) => {
    const startTime = Date.now();
    const user = await authenticateUser(data);
    const duration = Date.now() - startTime;

    // Track login event
    await trackEvent(context.env, "user_login", {
      user_id: user.id,
      tenant_id: user.tenantId,
      duration_ms: duration,
    });

    return user;
  }
);
```

### Query Analytics Data

Use Cloudflare GraphQL API:

```graphql
query GetLoginStats {
  viewer {
    accounts(filter: { accountTag: $accountId }) {
      workersAnalyticsEngineDataset(dataset: "my_analytics") {
        query(
          filter: {
            blob1: "user_login"
            datetime_gt: "2025-01-01T00:00:00Z"
          }
        ) {
          count
          dimensions {
            blob1  # event name
            index1 # user_id
            index2 # tenant_id
          }
        }
      }
    }
  }
}
```

## Health Checks

### Health Check Endpoint

```typescript
// app/routes/api/health.ts
import { createServerFn } from "@tanstack/start";
import { db } from "~/lib/server/db";

export const GET = createServerFn({ method: "GET" }).handler(async ({ context }) => {
  const startTime = Date.now();
  const checks: Record<string, string> = {};

  // Check database
  let dbHealthy = false;
  try {
    await db.execute("SELECT 1");
    dbHealthy = true;
    checks.database = "ok";
  } catch (error) {
    console.error("Database health check failed:", error);
    checks.database = "failed";
  }

  // Check Redis (if using Upstash)
  let redisHealthy = false;
  if (context.env.REDIS) {
    try {
      await context.env.REDIS.ping();
      redisHealthy = true;
      checks.redis = "ok";
    } catch (error) {
      console.error("Redis health check failed:", error);
      checks.redis = "failed";
    }
  }

  const duration = Date.now() - startTime;
  const healthy = dbHealthy && (!context.env.REDIS || redisHealthy);

  return new Response(
    JSON.stringify({
      status: healthy ? "healthy" : "unhealthy",
      checks,
      duration_ms: duration,
      timestamp: new Date().toISOString(),
      environment: process.env.ENVIRONMENT,
    }),
    {
      status: healthy ? 200 : 503,
      headers: { "Content-Type": "application/json" },
    }
  );
});
```

### Cloudflare Health Checks

Configure in Cloudflare dashboard:

1. Go to Traffic → Health Checks
2. Create health check for `/api/health`
3. Configure:
   - Interval: 60 seconds
   - Timeout: 5 seconds
   - Retries: 2
   - Expected status: 200
4. Set up notifications (email/webhook)

## Error Tracking

### Structured Error Logging

```typescript
// app/utils/error-handler.ts
import { logger } from "~/utils/logger";

export function handleError(error: Error, context?: Record<string, unknown>) {
  // Log error with full context
  logger.error(error.message, {
    error_name: error.name,
    stack: error.stack,
    ...context,
  });

  // Also log to Analytics Engine for tracking
  if (context?.env) {
    trackEvent(context.env as Env, "error_occurred", {
      error_name: error.name,
      error_message: error.message,
    });
  }
}

// Usage in server function
export const updateUser = createServerFn({ method: "POST" }).handler(
  async ({ data, context }) => {
    try {
      return await userService.update(data);
    } catch (error) {
      handleError(error, {
        user_id: context.user?.id,
        tenant_id: context.tenant?.id,
        env: context.env,
      });
      throw error;
    }
  }
);
```

### Viewing Errors in Cloudflare

1. **Workers Dashboard**: View errors in real-time
2. **Wrangler Tail**: `npx wrangler tail --status error`
3. **Analytics**: Check error rate metrics
4. **Health Checks**: Monitor endpoint failures

## Supporting Documentation

All supporting files are under 500 lines per Anthropic best practices:

- **[examples/](examples/)** - Complete monitoring examples
  - [cloudflare-logging.md](examples/cloudflare-logging.md) - Structured console logging
  - [wrangler-tail.md](examples/wrangler-tail.md) - Real-time log streaming
  - [analytics-engine.md](examples/analytics-engine.md) - Custom event tracking
  - [health-checks.md](examples/health-checks.md) - Health check implementations
  - [error-tracking.md](examples/error-tracking.md) - Error handling patterns
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[reference/](reference/)** - Monitoring references
  - [cloudflare-metrics.md](reference/cloudflare-metrics.md) - Available metrics
  - [wrangler-commands.md](reference/wrangler-commands.md) - Wrangler CLI reference
  - [alert-configuration.md](reference/alert-configuration.md) - Setting up alerts
  - [INDEX.md](reference/INDEX.md) - Reference navigation

- **[templates/](templates/)** - Copy-paste ready templates
  - [logger.ts](templates/logger.ts) - Cloudflare logger template
  - [health-check.ts](templates/health-check.ts) - Health check endpoint

- **[checklists/](checklists/)** - Monitoring checklists
  - [observability-setup-checklist.md](checklists/observability-setup-checklist.md) - Setup checklist

## When to Apply This Skill

Use this skill when:
- Setting up monitoring for new Cloudflare Workers projects
- Implementing structured logging with console
- Debugging production issues with wrangler tail
- Setting up health checks
- Implementing custom metrics tracking with Analytics Engine
- Configuring Cloudflare alerts

## Template Reference

These patterns are from Grey Haven's production monitoring:
- **Cloudflare Workers Analytics**: Request and performance metrics
- **Wrangler tail**: Real-time log streaming
- **Console logging**: Structured JSON logs
- **Analytics Engine**: Custom event tracking

## Critical Reminders

1. **Structured logging**: Use JSON.stringify for console logs
2. **Request IDs**: Track requests with UUIDs for debugging
3. **Error context**: Include tenant_id, user_id in all error logs
4. **Health checks**: Monitor database and external service connections
5. **Wrangler tail**: Use filters to narrow down logs (--status, --method)
6. **Performance**: Track duration_ms for all operations
7. **Environment**: Log environment in all messages for filtering
8. **Analytics Engine**: Use for custom metrics and event tracking
9. **Dashboard access**: Logs available in Cloudflare Workers dashboard
10. **Real-time debugging**: Use wrangler tail for live production debugging
