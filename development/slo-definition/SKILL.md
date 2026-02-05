---
name: slo-definition
description: Define Service Level Objectives (SLOs), Indicators (SLIs), and error budgets
allowed-tools: Read, Glob, Grep, Write, Edit
---

# SLO Definition Skill

## When to Use This Skill

Use this skill when:

- **Slo Definition tasks** - Working on define service level objectives (slos), indicators (slis), and error budgets
- **Planning or design** - Need guidance on Slo Definition approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Define Service Level Objectives (SLOs), Service Level Indicators (SLIs), and error budgets following Google SRE principles.

## MANDATORY: Documentation-First Approach

Before defining SLOs:

1. **Invoke `docs-management` skill** for SRE patterns
2. **Verify Google SRE best practices** via MCP servers (perplexity for latest)
3. **Base all guidance on Google SRE book and industry standards**

## SLO/SLI/SLA Hierarchy

```text
Service Level Hierarchy:

┌─────────────────────────────────────────────────────────────────────────────┐
│                     SLA (Service Level Agreement)                            │
│              External contract with customers/users                          │
│              Example: "99.9% availability per month"                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                     SLO (Service Level Objective)                            │
│              Internal target (typically stricter than SLA)                   │
│              Example: "99.95% availability per month"                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                     SLI (Service Level Indicator)                            │
│              Quantitative measure of service behavior                        │
│              Example: "Successful requests / Total requests"                 │
└─────────────────────────────────────────────────────────────────────────────┘

                    SLI measures → SLO targets → SLA contracts
```

## SLI Categories

### The Four Golden Signals

```text
Google's Four Golden Signals:

┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│    Latency      │    Traffic      │     Errors      │   Saturation    │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ Time to serve   │ Demand on       │ Rate of failed  │ How "full" the  │
│ requests        │ the system      │ requests        │ service is      │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ P50, P95, P99   │ Requests/sec    │ 5xx/total       │ CPU, memory,    │
│ response time   │ QPS, bytes/sec  │ Error rate      │ queue depth     │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

### Common SLI Types

| Category | SLI | Measurement |
|----------|-----|-------------|
| **Availability** | Success rate | Successful requests / Total requests |
| **Latency** | Response time | Requests < threshold / Total requests |
| **Throughput** | Processing rate | Operations / Time window |
| **Correctness** | Data quality | Correct responses / Total responses |
| **Freshness** | Data currency | Data updated within threshold |
| **Coverage** | Completeness | Items processed / Items expected |

## SLO Definition Template

````markdown
# SLO Definition: [Service Name]

## Service Overview

**Service:** [Service name and brief description]
**Owners:** [Team responsible]
**Stakeholders:** [Dependent teams/users]
**Tier:** [Critical / Standard / Development]

## SLIs

### SLI-001: Availability

**Definition:**
The proportion of successful HTTP requests, as measured from the load balancer.

**Formula:**
```promql
count(http_requests{status!~"5.."}) / count(http_requests) * 100
```

**Good Event:** HTTP response with status code < 500
**Valid Event:** Any HTTP request to the service

### SLI-002: Latency

**Definition:**
The proportion of requests that complete within the latency threshold.

**Formula:**
```promql
count(http_requests{duration<="500ms"}) / count(http_requests) * 100
```

**Good Event:** Request completes in < 500ms
**Valid Event:** Any HTTP request to the service

## SLOs

### SLO-001: Availability

**Target:** 99.9% of requests succeed over a 30-day rolling window
**SLI:** SLI-001 (Availability)
**Window:** 30-day rolling

**Rationale:**
This target provides approximately 43 minutes of downtime budget per month,
balancing reliability with development velocity.

### SLO-002: Latency (P95)

**Target:** 99% of requests complete in < 500ms over a 30-day rolling window
**SLI:** SLI-002 (Latency)
**Window:** 30-day rolling

**Rationale:**
P95 latency target ensures good user experience for majority of users
while allowing headroom for complex operations.

## Error Budget

### Availability Error Budget

**Monthly Budget:** (100% - 99.9%) × 30 days = 43.2 minutes
**Current Burn Rate:** [calculated from monitoring]
**Budget Remaining:** [calculated from monitoring]

### Latency Error Budget

**Monthly Budget:** (100% - 99%) × total_requests = 1% slow requests
**Current Burn Rate:** [calculated from monitoring]
**Budget Remaining:** [calculated from monitoring]

## Alerting Policy

### Error Budget Burn Alerts

| Alert Level | Condition | Action |
|-------------|-----------|--------|
| Warning | >2% budget consumed in 1 hour | Investigate |
| Critical | >5% budget consumed in 1 hour | Page on-call |
| Emergency | >50% budget consumed | Freeze deployments |

## Review Schedule

- **Weekly:** Review burn rate and recent incidents
- **Monthly:** Review SLO achievement, adjust if needed
- **Quarterly:** Review SLO relevance and stakeholder satisfaction

````

## SLO Calculation Patterns

### Availability Calculation

```csharp
public sealed class AvailabilitySloCalculator
{
    private readonly IMetricsClient _metrics;

    public AvailabilitySloCalculator(IMetricsClient metrics)
    {
        _metrics = metrics;
    }

    public async Task<SloStatus> CalculateAsync(
        string serviceName,
        TimeSpan window,
        double targetPercentage,
        CancellationToken ct = default)
    {
        var query = $"""
            sum(rate(http_requests_total{{
                service="{serviceName}",
                status!~"5.."
            }}[{window.TotalMinutes}m]))
            /
            sum(rate(http_requests_total{{
                service="{serviceName}"
            }}[{window.TotalMinutes}m]))
            * 100
            """;

        var currentSli = await _metrics.QueryAsync(query, ct);
        var errorBudget = CalculateErrorBudget(targetPercentage, currentSli, window);

        return new SloStatus
        {
            CurrentSli = currentSli,
            Target = targetPercentage,
            Window = window,
            ErrorBudget = errorBudget,
            IsHealthy = currentSli >= targetPercentage
        };
    }

    private static ErrorBudget CalculateErrorBudget(
        double target,
        double current,
        TimeSpan window)
    {
        var budgetTotal = 100.0 - target; // e.g., 0.1% for 99.9% target
        var budgetConsumed = Math.Max(0, target - current);
        var budgetRemaining = Math.Max(0, budgetTotal - budgetConsumed);

        return new ErrorBudget
        {
            TotalBudget = budgetTotal,
            ConsumedBudget = budgetConsumed,
            RemainingBudget = budgetRemaining,
            RemainingPercentage = (budgetRemaining / budgetTotal) * 100,
            BurnRate = budgetConsumed / window.TotalHours // per hour
        };
    }
}

public sealed record SloStatus
{
    public required double CurrentSli { get; init; }
    public required double Target { get; init; }
    public required TimeSpan Window { get; init; }
    public required ErrorBudget ErrorBudget { get; init; }
    public required bool IsHealthy { get; init; }
}

public sealed record ErrorBudget
{
    public required double TotalBudget { get; init; }
    public required double ConsumedBudget { get; init; }
    public required double RemainingBudget { get; init; }
    public required double RemainingPercentage { get; init; }
    public required double BurnRate { get; init; }  // per hour
}
```

### Multi-Window SLO (Burn Rate)

```csharp
public sealed class BurnRateCalculator
{
    /// <summary>
    /// Calculate burn rate using multiple windows for better alerting.
    /// Fast burn: 1-hour window with 14.4x burn rate (2% budget in 1 hour)
    /// Slow burn: 6-hour window with 6x burn rate (10% budget in 6 hours)
    /// </summary>
    public BurnRateStatus Calculate(
        double targetSlo,
        double shortWindowSli,    // 1-hour
        double longWindowSli,     // 6-hour
        TimeSpan budgetWindow)    // 30-day
    {
        var budgetTotalPercent = 100.0 - targetSlo;

        // Fast burn: consuming 2% of monthly budget in 1 hour
        // = (1/720) * 14.4 = 2% per hour (720 hours in 30 days)
        var fastBurnRate = (100.0 - shortWindowSli) /
                          (budgetTotalPercent / (budgetWindow.TotalHours / 1));

        // Slow burn: consuming 10% of monthly budget in 6 hours
        var slowBurnRate = (100.0 - longWindowSli) /
                          (budgetTotalPercent / (budgetWindow.TotalHours / 6));

        return new BurnRateStatus
        {
            FastBurnRate = fastBurnRate,
            SlowBurnRate = slowBurnRate,
            IsFastBurnAlert = fastBurnRate >= 14.4 && slowBurnRate >= 14.4,
            IsSlowBurnAlert = fastBurnRate >= 6.0 && slowBurnRate >= 6.0,
            ProjectedBudgetExhaustion = CalculateExhaustion(fastBurnRate, budgetWindow)
        };
    }

    private static TimeSpan? CalculateExhaustion(double burnRate, TimeSpan window)
    {
        if (burnRate <= 0) return null;
        return TimeSpan.FromHours(window.TotalHours / burnRate);
    }
}

public sealed record BurnRateStatus
{
    public required double FastBurnRate { get; init; }
    public required double SlowBurnRate { get; init; }
    public required bool IsFastBurnAlert { get; init; }
    public required bool IsSlowBurnAlert { get; init; }
    public TimeSpan? ProjectedBudgetExhaustion { get; init; }
}
```

## Availability Targets Reference

| Target | Annual Downtime | Monthly Downtime | Weekly Downtime |
|--------|----------------|------------------|-----------------|
| 99% (two 9s) | 3.65 days | 7.31 hours | 1.68 hours |
| 99.5% | 1.83 days | 3.65 hours | 50.4 minutes |
| 99.9% (three 9s) | 8.77 hours | 43.8 minutes | 10.1 minutes |
| 99.95% | 4.38 hours | 21.9 minutes | 5.04 minutes |
| 99.99% (four 9s) | 52.6 minutes | 4.38 minutes | 1.01 minutes |
| 99.999% (five 9s) | 5.26 minutes | 26.3 seconds | 6.05 seconds |

## Error Budget Policies

```markdown
# Error Budget Policy

## Philosophy

Error budgets represent a balance between reliability and velocity.
Spending error budget on innovation is encouraged; exhausting it
requires course correction.

## Budget States

### Green (>50% remaining)
- Normal development velocity
- New features proceed
- Experiments encouraged

### Yellow (25-50% remaining)
- Increased caution on risky changes
- Enhanced review for deployments
- Focus on reliability improvements

### Red (<25% remaining)
- Feature freeze until budget recovers
- Priority on reliability work only
- Post-mortem for budget consumption

### Exhausted (0% remaining)
- All non-emergency deployments halted
- Emergency reliability sprint
- Stakeholder communication required

## Recovery Actions

When budget is exhausted:
1. Immediate deployment freeze
2. Incident review for contributing factors
3. Prioritize top reliability issues
4. Daily burn rate monitoring
5. Resume deployments when 10% budget recovers
```

## SLO for Different Service Types

### API Service SLO

```yaml
service: order-api
tier: critical

slis:
  availability:
    type: request-based
    good_events: 'status < 500'
    valid_events: 'all requests'

  latency_p95:
    type: threshold
    good_events: 'duration < 200ms'
    valid_events: 'all requests'

  latency_p99:
    type: threshold
    good_events: 'duration < 1s'
    valid_events: 'all requests'

slos:
  - name: availability
    target: 99.9%
    window: 30d

  - name: latency_p95
    target: 99%
    window: 30d

  - name: latency_p99
    target: 95%
    window: 30d
```

### Background Job SLO

```yaml
service: order-processor
tier: standard

slis:
  success_rate:
    type: request-based
    good_events: 'job.status = completed'
    valid_events: 'job.status in (completed, failed)'

  freshness:
    type: threshold
    good_events: 'queue.age < 5m'
    valid_events: 'queue.depth > 0'

slos:
  - name: success_rate
    target: 99.5%
    window: 7d

  - name: freshness
    target: 95%
    window: 1d
```

### Data Pipeline SLO

```yaml
service: analytics-pipeline
tier: standard

slis:
  completeness:
    type: coverage
    good_events: 'records_processed'
    valid_events: 'records_expected'

  freshness:
    type: threshold
    good_events: 'last_update < 1h'
    valid_events: 'pipeline.active = true'

  correctness:
    type: quality
    good_events: 'validation.passed = true'
    valid_events: 'validation.executed = true'

slos:
  - name: completeness
    target: 99.9%
    window: 1d

  - name: freshness
    target: 99%
    window: 1d

  - name: correctness
    target: 99.99%
    window: 7d
```

## Workflow

When defining SLOs:

1. **Identify**: User journeys and critical paths
2. **Select**: Choose appropriate SLI types for each journey
3. **Measure**: Implement instrumentation for SLIs
4. **Target**: Set realistic SLO targets based on user needs
5. **Budget**: Calculate error budgets and policies
6. **Alert**: Configure multi-window burn rate alerts
7. **Review**: Establish regular SLO review cadence

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
