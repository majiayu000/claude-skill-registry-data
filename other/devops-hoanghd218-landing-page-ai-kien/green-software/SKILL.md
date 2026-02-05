---
name: green-software
description: Sustainability assessment and energy efficiency for software systems
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Green Software Skill

## When to Use This Skill

Use this skill when:

- **Green Software tasks** - Working on sustainability assessment and energy efficiency for software systems
- **Planning or design** - Need guidance on Green Software approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Apply Green Software Foundation principles to assess and improve software sustainability.

## MANDATORY: Documentation-First Approach

Before sustainability assessment:

1. **Invoke `docs-management` skill** for sustainability patterns
2. **Verify Green Software Foundation standards** via MCP servers (perplexity)
3. **Base guidance on Green Software Foundation principles and SCI specification**

## Green Software Principles

```text
Green Software Foundation Core Principles:

┌─────────────────────────────────────────────────────────────────────────────┐
│                         GREEN SOFTWARE                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   1. CARBON EFFICIENCY                                                       │
│      Emit the least amount of carbon possible                                │
│                                                                              │
│   2. ENERGY EFFICIENCY                                                       │
│      Use the least amount of energy possible                                 │
│                                                                              │
│   3. CARBON AWARENESS                                                        │
│      Do more when electricity is cleaner, less when dirtier                 │
│                                                                              │
│   4. HARDWARE EFFICIENCY                                                     │
│      Use the least amount of embodied carbon possible                        │
│                                                                              │
│   5. MEASUREMENT                                                             │
│      Quantify carbon emissions to track improvement                          │
│                                                                              │
│   6. CLIMATE COMMITMENTS                                                     │
│      Set science-based targets and net-zero goals                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Software Carbon Intensity (SCI)

The SCI specification provides a methodology to calculate the carbon emissions of software.

```text
SCI Formula:

    SCI = ((E × I) + M) per R

Where:
    E = Energy consumed by the software
    I = Location-based carbon intensity of electricity (gCO2eq/kWh)
    M = Embodied carbon of hardware used
    R = Functional unit (e.g., per user, per transaction, per API call)

Example:
    E = 0.5 kWh (for 1000 API calls)
    I = 400 gCO2eq/kWh (average grid)
    M = 10 gCO2eq (amortized hardware)
    R = 1000 API calls

    SCI = ((0.5 × 400) + 10) / 1000
        = (200 + 10) / 1000
        = 0.21 gCO2eq per API call
```

## Sustainability Assessment Template

````markdown
# Green Software Assessment: [System Name]

## Executive Summary

**System:** [System name and description]
**Assessment Date:** [Date]
**Current SCI:** [X gCO2eq per R]
**Target SCI:** [Y gCO2eq per R]
**Reduction Goal:** [Z%]

## Energy Profile

### Compute Resources

| Resource | Instance Type | Region | Carbon Intensity | Monthly kWh |
|----------|--------------|--------|------------------|-------------|
| API Servers | c5.xlarge | us-east-1 | 379 gCO2/kWh | 500 |
| Databases | db.r5.2xlarge | us-east-1 | 379 gCO2/kWh | 800 |
| Workers | c5.2xlarge | us-west-2 | 89 gCO2/kWh | 300 |
| **Total** | | | | **1600** |

### Carbon Intensity by Region

| Region | Grid Carbon (gCO2/kWh) | Renewable % | Recommendation |
|--------|------------------------|-------------|----------------|
| us-east-1 | 379 | 35% | Consider relocation |
| us-west-2 | 89 | 85% | ✅ Green region |
| eu-west-1 | 295 | 55% | Acceptable |
| eu-north-1 | 28 | 95% | 🌿 Best option |

## SCI Calculation

### Current State

```text
E (Energy): 1,600 kWh/month
I (Intensity): 379 gCO2/kWh (weighted average)
M (Embodied): 50 kgCO2/month (amortized)
R (Functional Unit): 10,000,000 API calls/month

SCI = ((1,600 × 379) + 50,000) / 10,000,000
    = (606,400 + 50,000) / 10,000,000
    = 0.0656 gCO2eq per API call
```

### Target State

```text
Optimization Plan:
- Migrate to eu-north-1 (I: 28 gCO2/kWh)
- Reduce compute by 20% via optimization
- Extend hardware lifecycle

New SCI = ((1,280 × 28) + 40,000) / 10,000,000
        = (35,840 + 40,000) / 10,000,000
        = 0.0076 gCO2eq per API call

Reduction: 88%
```

## Carbon Hotspots

### By Component

| Component | Energy % | Carbon % | Optimization Priority |
|-----------|----------|----------|-----------------------|
| Database | 50% | 55% | 🔴 High |
| API Compute | 30% | 32% | 🟡 Medium |
| Background Jobs | 15% | 10% | 🟢 Low |
| CDN/Static | 5% | 3% | 🟢 Low |

### By Operation

| Operation | Calls/Month | Energy/Call | Carbon/Call | Priority |
|-----------|-------------|-------------|-------------|----------|
| Search | 5M | 0.05 Wh | 0.019 gCO2 | 🔴 High |
| Login | 2M | 0.02 Wh | 0.008 gCO2 | 🟢 Low |
| Order | 1M | 0.1 Wh | 0.038 gCO2 | 🟡 Medium |
| Report | 0.1M | 2 Wh | 0.76 gCO2 | 🔴 High |

## Recommendations

### Quick Wins (< 1 month)

1. **Enable auto-scaling down** during off-peak hours
   - Impact: -15% energy
   - Effort: Low

2. **Implement request caching** for read-heavy APIs
   - Impact: -20% database energy
   - Effort: Low

3. **Optimize container images** to reduce startup energy
   - Impact: -5% energy
   - Effort: Low

### Medium-Term (1-3 months)

1. **Migrate to green region** (eu-north-1 or us-west-2)
   - Impact: -75% carbon intensity
   - Effort: Medium
   - Trade-off: Latency for distant users

2. **Implement carbon-aware scheduling** for batch jobs
   - Impact: -30% carbon for jobs
   - Effort: Medium

3. **Right-size instances** based on actual utilization
   - Impact: -20% compute energy
   - Effort: Medium

### Long-Term (3-12 months)

1. **Adopt ARM-based compute** (Graviton)
   - Impact: -40% energy for compute
   - Effort: High (code testing)

2. **Implement demand shaping** for carbon intensity
   - Impact: -25% carbon
   - Effort: High

3. **Carbon-neutral targets** via renewable energy credits
   - Impact: Net-zero operational carbon
   - Effort: Commercial agreement

````text

````

## Carbon-Aware Patterns

### Demand Shifting

```csharp
// Shift non-urgent workloads to low-carbon periods
public sealed class CarbonAwareScheduler
{
    private readonly ICarbonIntensityProvider _carbonProvider;
    private readonly IJobQueue _jobQueue;
    private readonly CarbonAwareOptions _options;

    public CarbonAwareScheduler(
        ICarbonIntensityProvider carbonProvider,
        IJobQueue jobQueue,
        IOptions<CarbonAwareOptions> options)
    {
        _carbonProvider = carbonProvider;
        _jobQueue = jobQueue;
        _options = options.Value;
    }

    public async Task<ScheduleDecision> ShouldRunNowAsync(
        Job job,
        CancellationToken ct = default)
    {
        // Urgent jobs run immediately regardless of carbon
        if (job.Priority == JobPriority.Urgent)
        {
            return ScheduleDecision.RunNow("Urgent priority");
        }

        var forecast = await _carbonProvider.GetForecastAsync(
            _options.Region,
            TimeSpan.FromHours(24),
            ct);

        var currentIntensity = forecast.Current;
        var threshold = _options.CarbonThresholdGramsPerKwh;

        // Low carbon period - run now
        if (currentIntensity <= threshold)
        {
            return ScheduleDecision.RunNow(
                $"Carbon intensity {currentIntensity} gCO2/kWh below threshold");
        }

        // Find next low-carbon window
        var nextLowCarbon = forecast.Periods
            .FirstOrDefault(p => p.Intensity <= threshold);

        if (nextLowCarbon is not null &&
            job.Deadline > nextLowCarbon.StartTime)
        {
            return ScheduleDecision.Defer(
                nextLowCarbon.StartTime,
                $"Deferring to low-carbon period at {nextLowCarbon.StartTime}");
        }

        // No low-carbon window before deadline - run now
        return ScheduleDecision.RunNow(
            "No low-carbon window available before deadline");
    }
}

public sealed record CarbonAwareOptions
{
    public required string Region { get; init; }
    public required double CarbonThresholdGramsPerKwh { get; init; }
}

public sealed record ScheduleDecision
{
    public required bool ShouldRun { get; init; }
    public DateTimeOffset? DeferUntil { get; init; }
    public required string Reason { get; init; }

    public static ScheduleDecision RunNow(string reason) =>
        new() { ShouldRun = true, Reason = reason };

    public static ScheduleDecision Defer(DateTimeOffset until, string reason) =>
        new() { ShouldRun = false, DeferUntil = until, Reason = reason };
}
```

### Demand Shaping

```csharp
// Shape demand to reduce carbon during high-intensity periods
public sealed class DemandShapingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ICarbonIntensityProvider _carbonProvider;

    public async Task InvokeAsync(HttpContext context)
    {
        var intensity = await _carbonProvider.GetCurrentIntensityAsync();

        // During high carbon periods, apply light processing
        if (intensity > 500)  // gCO2/kWh threshold
        {
            // Reduce image quality
            context.Request.Headers["Accept-Encoding"] = "minimal";

            // Disable optional features
            context.Items["CarbonAware.LowPowerMode"] = true;

            // Suggest client-side caching
            context.Response.Headers["Cache-Control"] = "public, max-age=3600";
        }

        await _next(context);
    }
}
```

## Energy Efficiency Patterns

### Efficient Coding Patterns

```csharp
// Energy-efficient patterns

// 1. Lazy evaluation - compute only when needed
public sealed class LazyUserProfile
{
    private readonly Lazy<Task<ProfileDetails>> _details;

    public LazyUserProfile(Guid userId, IProfileService service)
    {
        // Only fetched if accessed
        _details = new Lazy<Task<ProfileDetails>>(
            () => service.GetDetailsAsync(userId));
    }

    public ValueTask<ProfileDetails> GetDetailsAsync()
    {
        // Lazy fetch - no energy if never called
        return new ValueTask<ProfileDetails>(_details.Value);
    }
}

// 2. Batch operations - reduce network/compute overhead
public sealed class BatchProcessor<T>
{
    private readonly Channel<T> _channel;
    private readonly int _batchSize;
    private readonly TimeSpan _batchWindow;

    public async Task ProcessInBatchesAsync(
        IAsyncEnumerable<T> items,
        Func<IReadOnlyList<T>, Task> processor,
        CancellationToken ct)
    {
        var batch = new List<T>(_batchSize);

        await foreach (var item in items.WithCancellation(ct))
        {
            batch.Add(item);

            if (batch.Count >= _batchSize)
            {
                await processor(batch);
                batch.Clear();
            }
        }

        if (batch.Count > 0)
        {
            await processor(batch);
        }
    }
}

// 3. Early termination - stop when goal achieved
public sealed class EarlyTerminationSearch<T>
{
    public async Task<T?> FindFirstMatchAsync(
        IAsyncEnumerable<T> source,
        Func<T, bool> predicate,
        CancellationToken ct)
    {
        await foreach (var item in source.WithCancellation(ct))
        {
            if (predicate(item))
            {
                return item;  // Stop immediately - save energy
            }
        }

        return default;
    }
}
```

## Measurement & Monitoring

### SCI Dashboard Metrics

```csharp
public static class GreenMetrics
{
    private static readonly Meter Meter = new("GreenSoftware");

    public static readonly Counter<double> EnergyConsumed =
        Meter.CreateCounter<double>(
            name: "energy.consumed.kwh",
            unit: "kWh",
            description: "Energy consumed in kilowatt-hours");

    public static readonly Gauge<double> CarbonIntensity =
        Meter.CreateGauge<double>(
            name: "carbon.intensity.gco2perkwh",
            unit: "gCO2eq/kWh",
            description: "Current grid carbon intensity");

    public static readonly Counter<double> CarbonEmitted =
        Meter.CreateCounter<double>(
            name: "carbon.emitted.gco2eq",
            unit: "gCO2eq",
            description: "Carbon emissions in grams CO2 equivalent");

    public static readonly Histogram<double> SciPerRequest =
        Meter.CreateHistogram<double>(
            name: "sci.per.request",
            unit: "gCO2eq",
            description: "Software Carbon Intensity per request");
}
```

## Sustainability Checklist

```markdown
## Green Software Checklist

### Architecture
- [ ] Deployed in low-carbon regions where possible
- [ ] Compute right-sized for actual demand
- [ ] Auto-scaling configured for efficient resource use
- [ ] CDN used for static content delivery
- [ ] Caching implemented at appropriate layers

### Code Efficiency
- [ ] Algorithms optimized for energy efficiency
- [ ] Lazy loading for non-critical resources
- [ ] Batch processing for bulk operations
- [ ] Connection pooling for external resources
- [ ] Efficient serialization formats (protobuf vs JSON)

### Carbon Awareness
- [ ] Non-urgent jobs scheduled for low-carbon periods
- [ ] Demand shaping during high-carbon periods
- [ ] Region-aware workload distribution
- [ ] Carbon intensity monitoring in place

### Measurement
- [ ] SCI calculated and tracked
- [ ] Energy consumption monitored
- [ ] Carbon emissions reported
- [ ] Targets set for improvement

### Hardware Efficiency
- [ ] Efficient instance types (ARM/Graviton where possible)
- [ ] Hardware lifecycle extended where feasible
- [ ] Embodied carbon considered in procurement
```

## Workflow

When conducting sustainability assessment:

1. **Inventory**: Catalog all compute resources and their locations
2. **Measure**: Calculate current energy consumption and carbon
3. **Calculate**: Determine SCI using the formula
4. **Identify**: Find carbon hotspots and optimization opportunities
5. **Prioritize**: Rank improvements by impact and effort
6. **Implement**: Apply energy efficiency patterns
7. **Monitor**: Track SCI over time
8. **Report**: Communicate progress toward targets

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
