---
name: observability-strategy
description: Design observability strategy using the three pillars (logs, metrics, traces)
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Observability Strategy Skill

## When to Use This Skill

Use this skill when:

- **Observability Strategy tasks** - Working on design observability strategy using the three pillars (logs, metrics, traces)
- **Planning or design** - Need guidance on Observability Strategy approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Design comprehensive observability strategies using the three pillars.

## MANDATORY: Documentation-First Approach

Before designing observability:

1. **Invoke `docs-management` skill** for observability patterns
2. **Verify OpenTelemetry patterns** via MCP servers (context7, perplexity)
3. **Base guidance on current observability best practices**

## Three Pillars of Observability

```text
OBSERVABILITY PILLARS:

┌─────────────────────────────────────────────────────────────────┐
│                      OBSERVABILITY                               │
│                                                                  │
│  "Understanding system state from external outputs"              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │    LOGS      │  │   METRICS    │  │   TRACES     │           │
│  │              │  │              │  │              │           │
│  │ What happened│  │ Aggregated   │  │ Request      │           │
│  │ Event records│  │ measurements │  │ journey      │           │
│  │ Debug detail │  │ Trends/alerts│  │ Causality    │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│         │                 │                 │                    │
│         └────────────────┬┴─────────────────┘                    │
│                          │                                       │
│                    CORRELATION                                   │
│              (trace_id, span_id, request_id)                     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Pillar Comparison

```text
PILLAR CHARACTERISTICS:

                │ LOGS          │ METRICS       │ TRACES
────────────────┼───────────────┼───────────────┼───────────────
Data Type       │ Events        │ Numbers       │ Spans
Cardinality     │ High          │ Low           │ Medium
Storage Cost    │ High          │ Low           │ Medium
Query Speed     │ Slower        │ Fast          │ Medium
Best For        │ Debugging     │ Alerting      │ Latency
When to Use     │ Something     │ Tracking      │ Understanding
                │ unexpected    │ trends        │ flow
────────────────┴───────────────┴───────────────┴───────────────

WHEN TO USE EACH:

LOGS: "What exactly happened?"
- Error details and stack traces
- Audit trail and compliance
- Business event recording
- Debug information

METRICS: "How is the system performing?"
- Request rate, error rate, latency (RED)
- Resource utilization (CPU, memory)
- Business KPIs (orders/minute)
- Alerting and dashboards

TRACES: "Where did time go?"
- Cross-service request flow
- Latency breakdown by component
- Dependency mapping
- Root cause analysis
```

## OpenTelemetry Strategy

```text
OPENTELEMETRY ARCHITECTURE:

Application Code
       │
       ▼
┌─────────────────────────────────────────┐
│           OpenTelemetry SDK              │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐    │
│  │ Traces  │ │ Metrics │ │  Logs   │    │
│  │ API     │ │ API     │ │ Bridge  │    │
│  └────┬────┘ └────┬────┘ └────┬────┘    │
│       │          │          │           │
│  ┌────┴──────────┴──────────┴────┐      │
│  │       Exporters/Processors     │      │
│  └───────────────┬───────────────┘      │
└──────────────────┼──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│           Collector (Optional)           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │Receivers │→│Processors│→│Exporters │ │
│  └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │ Jaeger  │ │Prometheus│ │  Loki   │
   │ (traces)│ │(metrics) │ │ (logs)  │
   └─────────┘ └─────────┘ └─────────┘
```

## .NET OpenTelemetry Setup

```csharp
// OpenTelemetry configuration for .NET
// Program.cs

using OpenTelemetry.Logs;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

var builder = WebApplication.CreateBuilder(args);

// Define resource (service identity)
var resourceBuilder = ResourceBuilder.CreateDefault()
    .AddService(
        serviceName: "OrdersApi",
        serviceVersion: "1.0.0",
        serviceInstanceId: Environment.MachineName)
    .AddAttributes(new Dictionary<string, object>
    {
        ["deployment.environment"] = builder.Environment.EnvironmentName,
        ["team.name"] = "orders-team"
    });

// Configure Tracing
builder.Services.AddOpenTelemetry()
    .WithTracing(tracing =>
    {
        tracing
            .SetResourceBuilder(resourceBuilder)
            // Auto-instrumentation
            .AddAspNetCoreInstrumentation(options =>
            {
                options.RecordException = true;
                options.Filter = ctx => !ctx.Request.Path.StartsWithSegments("/health");
            })
            .AddHttpClientInstrumentation()
            .AddEntityFrameworkCoreInstrumentation()
            // Custom instrumentation
            .AddSource("OrdersApi.Domain")
            // Exporters
            .AddOtlpExporter(options =>
            {
                options.Endpoint = new Uri("http://collector:4317");
            });
    })
    .WithMetrics(metrics =>
    {
        metrics
            .SetResourceBuilder(resourceBuilder)
            // Auto-instrumentation
            .AddAspNetCoreInstrumentation()
            .AddHttpClientInstrumentation()
            .AddRuntimeInstrumentation()
            .AddProcessInstrumentation()
            // Custom metrics
            .AddMeter("OrdersApi.Business")
            // Exporters
            .AddOtlpExporter(options =>
            {
                options.Endpoint = new Uri("http://collector:4317");
            });
    });

// Configure Logging
builder.Logging.AddOpenTelemetry(logging =>
{
    logging
        .SetResourceBuilder(resourceBuilder)
        .AddOtlpExporter(options =>
        {
            options.Endpoint = new Uri("http://collector:4317");
        });
});
```

## Structured Logging Pattern

```csharp
// Structured logging with Serilog
// Infrastructure/Logging/LoggingConfiguration.cs

public static class LoggingConfiguration
{
    public static IHostBuilder ConfigureStructuredLogging(
        this IHostBuilder hostBuilder)
    {
        return hostBuilder.UseSerilog((context, services, configuration) =>
        {
            configuration
                .ReadFrom.Configuration(context.Configuration)
                .ReadFrom.Services(services)
                .Enrich.FromLogContext()
                .Enrich.WithMachineName()
                .Enrich.WithEnvironmentName()
                .Enrich.WithProperty("Application", "OrdersApi")
                // Correlation
                .Enrich.WithCorrelationId()
                .Enrich.WithSpanId()
                .Enrich.WithTraceId()
                // Output
                .WriteTo.Console(new JsonFormatter())
                .WriteTo.OpenTelemetry(options =>
                {
                    options.Endpoint = "http://collector:4317";
                    options.Protocol = OtlpProtocol.Grpc;
                });
        });
    }
}

// Structured log usage
public class OrderService
{
    private readonly ILogger<OrderService> _logger;

    public async Task<Order> CreateOrderAsync(CreateOrderCommand command)
    {
        using var _ = _logger.BeginScope(new Dictionary<string, object>
        {
            ["CustomerId"] = command.CustomerId,
            ["OrderTotal"] = command.Total
        });

        _logger.LogInformation(
            "Creating order for customer {CustomerId} with {ItemCount} items",
            command.CustomerId,
            command.Items.Count);

        try
        {
            var order = await ProcessOrder(command);

            _logger.LogInformation(
                "Order {OrderId} created successfully. Total: {Total:C}",
                order.Id,
                order.Total);

            return order;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Failed to create order for customer {CustomerId}",
                command.CustomerId);
            throw;
        }
    }
}
```

## Custom Metrics

```csharp
// Custom business metrics
// Infrastructure/Telemetry/BusinessMetrics.cs

using System.Diagnostics.Metrics;

public class BusinessMetrics
{
    private readonly Counter<long> _ordersCreated;
    private readonly Counter<long> _ordersFailed;
    private readonly Histogram<double> _orderValue;
    private readonly ObservableGauge<int> _pendingOrders;

    private int _pendingOrderCount;

    public BusinessMetrics(IMeterFactory meterFactory)
    {
        var meter = meterFactory.Create("OrdersApi.Business");

        _ordersCreated = meter.CreateCounter<long>(
            name: "orders.created",
            unit: "{order}",
            description: "Number of orders created");

        _ordersFailed = meter.CreateCounter<long>(
            name: "orders.failed",
            unit: "{order}",
            description: "Number of failed order attempts");

        _orderValue = meter.CreateHistogram<double>(
            name: "orders.value",
            unit: "USD",
            description: "Order value distribution");

        _pendingOrders = meter.CreateObservableGauge(
            name: "orders.pending",
            observeValue: () => _pendingOrderCount,
            unit: "{order}",
            description: "Current pending orders");
    }

    public void RecordOrderCreated(string customerId, decimal value)
    {
        _ordersCreated.Add(1,
            new KeyValuePair<string, object?>("customer.type",
                GetCustomerType(customerId)));

        _orderValue.Record((double)value,
            new KeyValuePair<string, object?>("currency", "USD"));
    }

    public void RecordOrderFailed(string reason)
    {
        _ordersFailed.Add(1,
            new KeyValuePair<string, object?>("failure.reason", reason));
    }

    public void SetPendingOrders(int count) => _pendingOrderCount = count;
}
```

## Tool Selection Guide

```text
OBSERVABILITY TOOL SELECTION:

TRACING BACKENDS:
┌─────────────────┬──────────────────────────────────────────────┐
│ Tool            │ Best For                                     │
├─────────────────┼──────────────────────────────────────────────┤
│ Jaeger          │ Open source, self-hosted, Kubernetes        │
│ Zipkin          │ Simple setup, legacy compatibility          │
│ Tempo           │ Grafana stack, cost-effective storage       │
│ Azure Monitor   │ Azure-native, APM features                  │
│ AWS X-Ray       │ AWS-native, Lambda integration              │
│ Datadog APM     │ Full-featured commercial, easy setup        │
└─────────────────┴──────────────────────────────────────────────┘

METRICS BACKENDS:
┌─────────────────┬──────────────────────────────────────────────┐
│ Tool            │ Best For                                     │
├─────────────────┼──────────────────────────────────────────────┤
│ Prometheus      │ Open source standard, Kubernetes            │
│ Mimir           │ Grafana stack, multi-tenant                 │
│ Azure Monitor   │ Azure-native, auto-scale                    │
│ CloudWatch      │ AWS-native, integrated                      │
│ Datadog         │ Commercial, unified platform                │
└─────────────────┴──────────────────────────────────────────────┘

LOG BACKENDS:
┌─────────────────┬──────────────────────────────────────────────┐
│ Tool            │ Best For                                     │
├─────────────────┼──────────────────────────────────────────────┤
│ Loki            │ Grafana stack, label-based, cost-effective  │
│ Elasticsearch   │ Full-text search, complex queries           │
│ Azure Log Ana.  │ Azure-native, KQL queries                   │
│ CloudWatch Logs │ AWS-native, integrated                      │
│ Splunk          │ Enterprise, compliance, security            │
└─────────────────┴──────────────────────────────────────────────┘

VISUALIZATION:
┌─────────────────┬──────────────────────────────────────────────┐
│ Tool            │ Best For                                     │
├─────────────────┼──────────────────────────────────────────────┤
│ Grafana         │ Open source, multi-source, flexible         │
│ Azure Dashboards│ Azure-native, workbooks                     │
│ Datadog         │ Commercial, APM integration                 │
│ Kibana          │ Elasticsearch visualization                 │
└─────────────────┴──────────────────────────────────────────────┘
```

## Strategy Template

```markdown
# Observability Strategy: {Service Name}

## Service Overview

| Aspect | Value |
|--------|-------|
| Service Name | [Name] |
| Criticality | [Critical/High/Medium/Low] |
| Team | [Team name] |
| Dependencies | [List] |

## Pillar Strategy

### Logging Strategy

**Log Levels:**
| Level | Usage |
|-------|-------|
| Error | Unhandled exceptions, failures |
| Warning | Recoverable issues, degradation |
| Information | Business events, request flow |
| Debug | Troubleshooting (disabled in prod) |

**Structured Fields:**
- `trace_id` - Correlation with traces
- `user_id` - User context
- `request_id` - Request correlation
- `operation` - Business operation name

**Retention:** [Duration]

### Metrics Strategy

**RED Metrics (Request-driven):**
- Rate: `http_requests_total`
- Errors: `http_requests_failed_total`
- Duration: `http_request_duration_seconds`

**USE Metrics (Resource-driven):**
- Utilization: `cpu_usage_percent`, `memory_usage_bytes`
- Saturation: `threadpool_queue_length`
- Errors: `gc_collection_count`

**Business Metrics:**
- [Custom metric 1]
- [Custom metric 2]

### Tracing Strategy

**Instrumented Components:**
- [ ] HTTP endpoints
- [ ] HTTP clients
- [ ] Database queries
- [ ] Message consumers
- [ ] Cache operations

**Sampling Strategy:**
- Production: [1%, 10%, 100%]
- Non-production: 100%

## Tool Stack

| Component | Tool | Rationale |
|-----------|------|-----------|
| Traces | [Tool] | [Why] |
| Metrics | [Tool] | [Why] |
| Logs | [Tool] | [Why] |
| Dashboards | [Tool] | [Why] |

## Implementation Phases

### Phase 1: Foundation
- [ ] Add OpenTelemetry SDK
- [ ] Configure auto-instrumentation
- [ ] Set up exporters

### Phase 2: Custom Telemetry
- [ ] Add custom metrics
- [ ] Implement structured logging
- [ ] Add manual spans for business operations

### Phase 3: Visualization
- [ ] Create service dashboard
- [ ] Set up SLO dashboards
- [ ] Configure alerts

## Success Criteria

- [ ] All requests have trace context
- [ ] RED metrics visible in dashboard
- [ ] Logs correlated with traces
- [ ] Alerts configured for SLO breaches
```

## Workflow

When designing observability strategy:

1. **Assess Service**: Understand criticality, dependencies, SLOs
2. **Define Signals**: What logs, metrics, traces are needed?
3. **Select Tools**: Choose backends that fit infrastructure
4. **Plan Instrumentation**: Identify instrumentation points
5. **Design Correlation**: Ensure signals can be correlated
6. **Create Dashboards**: Plan visualization and alerting

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
