---
name: langfuse-observability
description: |
  Set up comprehensive observability for Langfuse with metrics, dashboards, and alerts.
  Use when implementing monitoring for LLM operations, setting up dashboards,
  or configuring alerting for Langfuse integration health.
  Trigger with phrases like "langfuse monitoring", "langfuse metrics",
  "langfuse observability", "monitor langfuse", "langfuse alerts", "langfuse dashboard".
allowed-tools: Read, Write, Edit
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Langfuse Observability

## Overview
Set up comprehensive observability for Langfuse integrations including metrics, dashboards, and alerts.

## Prerequisites
- Prometheus or compatible metrics backend
- Grafana or similar dashboarding tool
- AlertManager or PagerDuty configured
- Langfuse SDK integrated

## Key Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `langfuse_traces_total` | Counter | Total traces created |
| `langfuse_generations_total` | Counter | Total LLM generations |
| `langfuse_generation_duration_seconds` | Histogram | LLM call latency |
| `langfuse_tokens_total` | Counter | Total tokens used |
| `langfuse_cost_usd_total` | Counter | Total LLM cost |
| `langfuse_errors_total` | Counter | Error count by type |
| `langfuse_flush_duration_seconds` | Histogram | SDK flush latency |

## Instructions

### Step 1: Implement Prometheus Metrics

```typescript
// lib/langfuse/metrics.ts
import { Registry, Counter, Histogram, Gauge } from "prom-client";

const registry = new Registry();

// Trace metrics
export const traceCounter = new Counter({
  name: "langfuse_traces_total",
  help: "Total Langfuse traces created",
  labelNames: ["name", "status", "environment"],
  registers: [registry],
});

// Generation metrics
export const generationCounter = new Counter({
  name: "langfuse_generations_total",
  help: "Total LLM generations",
  labelNames: ["model", "status"],
  registers: [registry],
});

export const generationDuration = new Histogram({
  name: "langfuse_generation_duration_seconds",
  help: "LLM generation duration",
  labelNames: ["model"],
  buckets: [0.1, 0.5, 1, 2, 5, 10, 30, 60],
  registers: [registry],
});

// Token metrics
export const tokenCounter = new Counter({
  name: "langfuse_tokens_total",
  help: "Total tokens used",
  labelNames: ["model", "type"], // type: prompt, completion
  registers: [registry],
});

// Cost metrics
export const costCounter = new Counter({
  name: "langfuse_cost_usd_total",
  help: "Total LLM cost in USD",
  labelNames: ["model"],
  registers: [registry],
});

// Error metrics
export const errorCounter = new Counter({
  name: "langfuse_errors_total",
  help: "Langfuse errors by type",
  labelNames: ["error_type", "operation"],
  registers: [registry],
});

// SDK health metrics
export const flushDuration = new Histogram({
  name: "langfuse_flush_duration_seconds",
  help: "Langfuse SDK flush duration",
  buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5],
  registers: [registry],
});

export const pendingEventsGauge = new Gauge({
  name: "langfuse_pending_events",
  help: "Number of events pending flush",
  registers: [registry],
});

export { registry };
```

### Step 2: Create Instrumented Langfuse Wrapper

```typescript
// lib/langfuse/instrumented.ts
import { Langfuse } from "langfuse";
import {
  traceCounter,
  generationCounter,
  generationDuration,
  tokenCounter,
  costCounter,
  errorCounter,
  flushDuration,
} from "./metrics";

const MODEL_PRICING: Record<string, { input: number; output: number }> = {
  "gpt-4-turbo": { input: 10.0, output: 30.0 },
  "gpt-4o": { input: 5.0, output: 15.0 },
  "gpt-4o-mini": { input: 0.15, output: 0.6 },
  "claude-3-sonnet": { input: 3.0, output: 15.0 },
};

class InstrumentedLangfuse {
  private langfuse: Langfuse;
  private environment: string;

  constructor(config: ConstructorParameters<typeof Langfuse>[0]) {
    this.langfuse = new Langfuse(config);
    this.environment = process.env.NODE_ENV || "development";
  }

  trace(params: Parameters<typeof this.langfuse.trace>[0]) {
    const trace = this.langfuse.trace(params);

    traceCounter.inc({
      name: params.name || "unknown",
      status: "created",
      environment: this.environment,
    });

    // Wrap update to track completion
    const originalUpdate = trace.update.bind(trace);
    trace.update = (updateParams) => {
      if (updateParams.level === "ERROR") {
        traceCounter.inc({
          name: params.name || "unknown",
          status: "error",
          environment: this.environment,
        });
      } else if (updateParams.output) {
        traceCounter.inc({
          name: params.name || "unknown",
          status: "completed",
          environment: this.environment,
        });
      }
      return originalUpdate(updateParams);
    };

    // Wrap generation to track LLM calls
    const originalGeneration = trace.generation.bind(trace);
    trace.generation = (genParams) => {
      const startTime = Date.now();
      const generation = originalGeneration(genParams);
      const model = genParams.model || "unknown";

      generationCounter.inc({ model, status: "started" });

      // Wrap end to track completion
      const originalEnd = generation.end.bind(generation);
      generation.end = (endParams) => {
        const duration = (Date.now() - startTime) / 1000;
        generationDuration.observe({ model }, duration);
        generationCounter.inc({ model, status: "completed" });

        // Track tokens
        if (endParams?.usage) {
          const { promptTokens = 0, completionTokens = 0 } = endParams.usage;

          tokenCounter.inc({ model, type: "prompt" }, promptTokens);
          tokenCounter.inc({ model, type: "completion" }, completionTokens);

          // Track cost
          const pricing = MODEL_PRICING[model];
          if (pricing) {
            const cost =
              (promptTokens / 1_000_000) * pricing.input +
              (completionTokens / 1_000_000) * pricing.output;
            costCounter.inc({ model }, cost);
          }
        }

        return originalEnd(endParams);
      };

      return generation;
    };

    return trace;
  }

  async flushAsync() {
    const timer = flushDuration.startTimer();
    try {
      await this.langfuse.flushAsync();
    } catch (error) {
      errorCounter.inc({ error_type: "flush_error", operation: "flush" });
      throw error;
    } finally {
      timer();
    }
  }

  async shutdownAsync() {
    return this.langfuse.shutdownAsync();
  }
}

export const langfuse = new InstrumentedLangfuse({
  publicKey: process.env.LANGFUSE_PUBLIC_KEY!,
  secretKey: process.env.LANGFUSE_SECRET_KEY!,
});
```

### Step 3: Expose Metrics Endpoint

```typescript
// api/metrics/route.ts (Next.js) or app.get('/metrics') (Express)
import { registry } from "@/lib/langfuse/metrics";

export async function GET() {
  const metrics = await registry.metrics();

  return new Response(metrics, {
    headers: {
      "Content-Type": registry.contentType,
    },
  });
}
```

### Step 4: Configure Prometheus Scraping

```yaml
# prometheus.yml
scrape_configs:
  - job_name: "llm-app"
    static_configs:
      - targets: ["app:3000"]
    metrics_path: "/api/metrics"
    scrape_interval: 15s

  - job_name: "langfuse-cloud"
    static_configs:
      - targets: ["cloud.langfuse.com"]
    scheme: https
    metrics_path: "/api/public/metrics"
    bearer_token: "${LANGFUSE_PUBLIC_KEY}"
```

### Step 5: Create Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Langfuse LLM Observability",
    "panels": [
      {
        "title": "LLM Requests per Second",
        "type": "timeseries",
        "targets": [{
          "expr": "rate(langfuse_generations_total[5m])",
          "legendFormat": "{{model}}"
        }]
      },
      {
        "title": "LLM Latency (P50/P95/P99)",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.5, rate(langfuse_generation_duration_seconds_bucket[5m]))",
            "legendFormat": "P50"
          },
          {
            "expr": "histogram_quantile(0.95, rate(langfuse_generation_duration_seconds_bucket[5m]))",
            "legendFormat": "P95"
          },
          {
            "expr": "histogram_quantile(0.99, rate(langfuse_generation_duration_seconds_bucket[5m]))",
            "legendFormat": "P99"
          }
        ]
      },
      {
        "title": "Token Usage by Model",
        "type": "timeseries",
        "targets": [{
          "expr": "rate(langfuse_tokens_total[1h])",
          "legendFormat": "{{model}} - {{type}}"
        }]
      },
      {
        "title": "LLM Cost (USD/hour)",
        "type": "stat",
        "targets": [{
          "expr": "sum(rate(langfuse_cost_usd_total[1h])) * 3600"
        }]
      },
      {
        "title": "Error Rate",
        "type": "timeseries",
        "targets": [{
          "expr": "rate(langfuse_errors_total[5m])",
          "legendFormat": "{{error_type}}"
        }]
      }
    ]
  }
}
```

### Step 6: Configure Alerts

```yaml
# alerts/langfuse.yaml
groups:
  - name: langfuse_alerts
    rules:
      - alert: LangfuseHighErrorRate
        expr: |
          rate(langfuse_errors_total[5m]) /
          rate(langfuse_generations_total[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Langfuse error rate > 5%"
          description: "LLM error rate is {{ $value | humanizePercentage }}"

      - alert: LangfuseHighLatency
        expr: |
          histogram_quantile(0.95,
            rate(langfuse_generation_duration_seconds_bucket[5m])
          ) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "LLM P95 latency > 10s"

      - alert: LangfuseHighCost
        expr: |
          sum(rate(langfuse_cost_usd_total[1h])) * 24 > 100
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Projected daily LLM cost > $100"

      - alert: LangfuseFlushBacklog
        expr: langfuse_pending_events > 1000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Langfuse event backlog > 1000"

      - alert: LangfuseDown
        expr: up{job="llm-app"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "LLM application is down"
```

## Output
- Prometheus metrics for all Langfuse operations
- Instrumented Langfuse wrapper
- Metrics endpoint for scraping
- Grafana dashboard configuration
- AlertManager rules

## Metrics Reference

| Dashboard Panel | Prometheus Query | Purpose |
|-----------------|------------------|---------|
| Request Rate | `rate(langfuse_generations_total[5m])` | LLM throughput |
| Latency | `histogram_quantile(0.95, ...)` | Performance |
| Token Usage | `rate(langfuse_tokens_total[1h])` | Usage tracking |
| Cost | `sum(rate(langfuse_cost_usd_total[1h]))` | Budget |
| Error Rate | `rate(langfuse_errors_total[5m])` | Reliability |

## Error Handling
| Issue | Cause | Solution |
|-------|-------|----------|
| Missing metrics | No instrumentation | Use wrapped client |
| High cardinality | Too many labels | Limit label values |
| Alert storms | Wrong thresholds | Tune alert rules |
| Metric gaps | Scrape failures | Check Prometheus targets |

## Resources
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
- [Grafana Dashboards](https://grafana.com/docs/grafana/latest/dashboards/)
- [AlertManager](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [Langfuse Analytics](https://langfuse.com/docs/analytics)

## Next Steps
For incident response, see `langfuse-incident-runbook`.
