---
name: usage-metering
description: Usage tracking, metering infrastructure, aggregation patterns, and consumption-based billing support for SaaS applications
allowed-tools: Read, Glob, Grep, Task, mcp__perplexity__search, mcp__microsoft-learn__microsoft_docs_search, mcp__context7__query-docs
---

# Usage Metering Skill

Guidance for implementing usage tracking and metering infrastructure in SaaS applications.

## MANDATORY: Documentation-First Approach

Before implementing usage metering:

1. **Invoke `docs-management` skill** for billing and metering patterns
2. **Verify patterns via MCP servers** (perplexity for current best practices, microsoft-learn for Azure patterns)
3. **Base all guidance on official documentation and current industry standards**

## When to Use

- Implementing consumption-based pricing
- Tracking API calls, storage, compute, or feature usage
- Building usage dashboards and alerts
- Integrating with billing systems for usage-based charges

## Core Concepts

### Usage Event Types

```text
Usage Categories:
┌─────────────────────────────────────────────────────────────┐
│ Category        │ Examples                   │ Billing Unit │
├─────────────────┼────────────────────────────┼──────────────┤
│ API Calls       │ Requests, queries, ops     │ Per 1K calls │
│ Compute         │ CPU seconds, GPU hours     │ Per hour     │
│ Storage         │ GB stored, objects         │ Per GB/month │
│ Data Transfer   │ Egress, ingress bytes      │ Per GB       │
│ Seats/Users     │ Active users, MAU          │ Per user     │
│ Features        │ Reports generated, exports │ Per action   │
│ Resources       │ Projects, environments     │ Per resource │
└─────────────────┴────────────────────────────┴──────────────┘
```

### Metering Patterns

```text
Pattern Selection:
┌──────────────────────────────────────────────────────────────┐
│ Pattern          │ Use When                  │ Trade-offs   │
├──────────────────┼───────────────────────────┼──────────────┤
│ Real-time        │ Need instant visibility   │ Higher cost  │
│ Near-real-time   │ 5-15 min latency OK       │ Balanced     │
│ Batch            │ Daily/hourly aggregation  │ Lower cost   │
│ Sampling         │ High volume, estimates OK │ Approximate  │
│ Hybrid           │ Mix of above              │ Complex      │
└──────────────────┴───────────────────────────┴──────────────┘
```

## Implementation Patterns

### Usage Event Model

```csharp
// Core usage event structure
public sealed record UsageEvent
{
    public required Guid EventId { get; init; } = Guid.NewGuid();
    public required Guid TenantId { get; init; }
    public required string MetricName { get; init; }  // e.g., "api.requests"
    public required decimal Quantity { get; init; }
    public required string Unit { get; init; }        // e.g., "count", "bytes"
    public required DateTimeOffset Timestamp { get; init; }
    public required string Source { get; init; }      // e.g., "api-gateway"
    public string? UserId { get; init; }
    public string? ResourceId { get; init; }
    public Dictionary<string, string> Dimensions { get; init; } = [];
    public string? IdempotencyKey { get; init; }
}

// Aggregated usage for billing periods
public sealed record UsageAggregate
{
    public required Guid TenantId { get; init; }
    public required string MetricName { get; init; }
    public required DateOnly PeriodStart { get; init; }
    public required DateOnly PeriodEnd { get; init; }
    public required decimal TotalQuantity { get; init; }
    public required string Unit { get; init; }
    public required int EventCount { get; init; }
    public DateTimeOffset LastUpdated { get; init; }
}
```

### Metering Service Interface

```csharp
public interface IUsageMeteringService
{
    // Record single usage event
    Task RecordUsageAsync(
        Guid tenantId,
        string metricName,
        decimal quantity,
        string unit,
        Dictionary<string, string>? dimensions = null,
        string? idempotencyKey = null,
        CancellationToken ct = default);

    // Record batch of events
    Task RecordBatchAsync(
        IReadOnlyList<UsageEvent> events,
        CancellationToken ct = default);

    // Get current period usage
    Task<UsageAggregate> GetCurrentUsageAsync(
        Guid tenantId,
        string metricName,
        CancellationToken ct = default);

    // Get historical usage
    Task<IReadOnlyList<UsageAggregate>> GetUsageHistoryAsync(
        Guid tenantId,
        string metricName,
        DateOnly startDate,
        DateOnly endDate,
        CancellationToken ct = default);
}
```

### High-Volume Ingestion Pattern

```csharp
// Buffered writer for high-throughput scenarios
public sealed class BufferedUsageWriter : IAsyncDisposable
{
    private readonly Channel<UsageEvent> _channel;
    private readonly IUsageEventStore _store;
    private readonly Task _processorTask;

    public BufferedUsageWriter(
        IUsageEventStore store,
        int batchSize = 100,
        TimeSpan? flushInterval = null)
    {
        _store = store;
        _channel = Channel.CreateBounded<UsageEvent>(
            new BoundedChannelOptions(10_000)
            {
                FullMode = BoundedChannelFullMode.Wait
            });

        flushInterval ??= TimeSpan.FromSeconds(5);
        _processorTask = ProcessEventsAsync(batchSize, flushInterval.Value);
    }

    public ValueTask RecordAsync(UsageEvent evt, CancellationToken ct = default)
        => _channel.Writer.WriteAsync(evt, ct);

    private async Task ProcessEventsAsync(int batchSize, TimeSpan flushInterval)
    {
        var batch = new List<UsageEvent>(batchSize);
        var timer = new PeriodicTimer(flushInterval);

        while (await _channel.Reader.WaitToReadAsync())
        {
            // Drain available events up to batch size
            while (batch.Count < batchSize &&
                   _channel.Reader.TryRead(out var evt))
            {
                batch.Add(evt);
            }

            if (batch.Count >= batchSize || await ShouldFlushAsync(timer))
            {
                await _store.WriteBatchAsync(batch);
                batch.Clear();
            }
        }

        // Flush remaining on shutdown
        if (batch.Count > 0)
            await _store.WriteBatchAsync(batch);
    }
}
```

## Architecture Options

### Event Streaming Architecture

```text
High-Volume Metering:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ API Gateway │────▶│ Event Hub/  │────▶│ Stream      │
│ (emit)      │     │ Kafka       │     │ Processor   │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌──────────────────────────┼──────────────────┐
                    │                          │                  │
                    ▼                          ▼                  ▼
             ┌─────────────┐           ┌─────────────┐    ┌─────────────┐
             │ Time-Series │           │ Aggregates  │    │ Alerts      │
             │ Store       │           │ (Redis/SQL) │    │ Engine      │
             └─────────────┘           └─────────────┘    └─────────────┘
```

### Simple Database Pattern

```text
Low-Volume Metering:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Application │────▶│ Usage Table │────▶│ Background  │
│ (record)    │     │ (append)    │     │ Aggregator  │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │ Aggregates  │
                                        │ Table       │
                                        └─────────────┘
```

## Quota Enforcement

### Quota Check Pattern

```csharp
public sealed class QuotaEnforcementService(
    IUsageMeteringService metering,
    IEntitlementService entitlements,
    ILogger<QuotaEnforcementService> logger)
{
    public async Task<QuotaCheckResult> CheckQuotaAsync(
        Guid tenantId,
        string metricName,
        decimal requestedQuantity,
        CancellationToken ct = default)
    {
        // Get current usage
        var currentUsage = await metering.GetCurrentUsageAsync(
            tenantId, metricName, ct);

        // Get entitlement limit
        var limit = await entitlements.GetLimitAsync(
            tenantId, metricName, ct);

        if (limit is null)
        {
            return QuotaCheckResult.Unlimited();
        }

        var projectedUsage = currentUsage.TotalQuantity + requestedQuantity;

        if (projectedUsage > limit.HardLimit)
        {
            logger.LogWarning(
                "Quota exceeded for tenant {TenantId}, metric {Metric}",
                tenantId, metricName);

            return QuotaCheckResult.Denied(
                current: currentUsage.TotalQuantity,
                limit: limit.HardLimit,
                requested: requestedQuantity);
        }

        if (projectedUsage > limit.SoftLimit)
        {
            return QuotaCheckResult.Warning(
                current: currentUsage.TotalQuantity,
                softLimit: limit.SoftLimit,
                hardLimit: limit.HardLimit);
        }

        return QuotaCheckResult.Allowed(
            remaining: limit.HardLimit - projectedUsage);
    }
}
```

### Rate Limiting vs Quota

```text
Comparison:
┌─────────────────────────────────────────────────────────────┐
│ Aspect          │ Rate Limiting       │ Quota/Metering     │
├─────────────────┼─────────────────────┼────────────────────┤
│ Time Window     │ Seconds/minutes     │ Hours/days/months  │
│ Purpose         │ Protect system      │ Enforce billing    │
│ Enforcement     │ Hard block          │ Soft/hard limits   │
│ Response        │ 429 + retry-after   │ 402/403 + upgrade  │
│ Tracking        │ In-memory/Redis     │ Durable storage    │
│ Precision       │ Approximate OK      │ Exact required     │
└─────────────────┴─────────────────────┴────────────────────┘

Use BOTH:
- Rate limiting: System protection (per-second/minute)
- Quota: Business limits (per-month billing cycles)
```

## References

Load for detailed implementation:

- `references/event-ingestion.md` - High-throughput event capture patterns
- `references/aggregation-strategies.md` - Time-series aggregation and rollups

For billing integration patterns, see the `billing-integration` skill.

## Related Skills

- `billing-integration` - Payment processing and invoicing
- `entitlements-management` - Feature gating and limits
- `subscription-models` - Pricing tier definitions

---

**Last Updated:** 2025-12-29
