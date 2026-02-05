---
name: resilience-patterns
description: Circuit breaker, retry, and DLQ patterns for .NET using Polly and Brighter. Use when implementing fault tolerance, handling transient failures, configuring retry strategies, or setting up dead letter queues. Includes Polly HttpClient patterns and Brighter message handler resilience.
allowed-tools: Read, Write, Glob, Grep, Bash, Skill
---

# Resilience Patterns Skill

## Overview

This skill provides guidance on implementing resilience patterns in .NET applications. It covers both synchronous resilience (HTTP clients, service calls) using Polly and asynchronous resilience (message handlers) using Brighter.

**Key Principle:** Design for failure. Systems should gracefully handle transient faults, prevent cascade failures, and provide meaningful fallback behavior.

## When to Use This Skill

**Keywords:** resilience, circuit breaker, retry, polly, brighter, fault tolerance, transient failure, DLQ, dead letter queue, timeout, bulkhead, fallback, http client resilience

**Use this skill when:**

- Implementing HTTP client resilience
- Configuring retry policies for transient failures
- Setting up circuit breakers to prevent cascade failures
- Designing message handler error handling
- Implementing dead letter queue patterns
- Adding timeout policies to service calls
- Configuring bulkhead isolation

## Resilience Strategy Overview

### Synchronous Resilience (Polly)

For HTTP calls and synchronous service communication:

| Pattern | Purpose | When to Use |
| --- | --- | --- |
| **Retry** | Retry failed operations | Transient failures (network, 503, timeouts) |
| **Circuit Breaker** | Stop calling failing services | Repeated failures indicate service is down |
| **Timeout** | Bound operation time | Prevent indefinite waits |
| **Bulkhead** | Isolate failures | Prevent one caller from exhausting resources |
| **Fallback** | Provide alternative | Graceful degradation |

### Asynchronous Resilience (Brighter)

For message-based and async operations:

| Pattern | Purpose | When to Use |
| --- | --- | --- |
| **Retry** | Redeliver failed messages | Transient processing failures |
| **Dead Letter Queue** | Park unprocessable messages | Poison messages, business rule failures |
| **Circuit Breaker** | Stop processing temporarily | Downstream service unavailable |
| **Timeout** | Bound handler execution | Prevent handler blocking |

## Quick Start: Polly v8 with HttpClient

### Basic Setup

```csharp
// Program.cs or Startup.cs
builder.Services.AddHttpClient<IOrderService, OrderService>()
    .AddStandardResilienceHandler();
```

The `AddStandardResilienceHandler()` adds a preconfigured pipeline with:

- Rate limiter
- Total request timeout
- Retry (exponential backoff)
- Circuit breaker
- Attempt timeout

### Custom Configuration

```csharp
builder.Services.AddHttpClient<IOrderService, OrderService>()
    .AddResilienceHandler("custom-pipeline", builder =>
    {
        // Retry with exponential backoff
        builder.AddRetry(new HttpRetryStrategyOptions
        {
            MaxRetryAttempts = 3,
            Delay = TimeSpan.FromSeconds(1),
            BackoffType = DelayBackoffType.Exponential,
            UseJitter = true,
            ShouldHandle = new PredicateBuilder<HttpResponseMessage>()
                .Handle<HttpRequestException>()
                .HandleResult(r => r.StatusCode == HttpStatusCode.ServiceUnavailable)
        });

        // Circuit breaker
        builder.AddCircuitBreaker(new HttpCircuitBreakerStrategyOptions
        {
            FailureRatio = 0.5,
            MinimumThroughput = 10,
            SamplingDuration = TimeSpan.FromSeconds(30),
            BreakDuration = TimeSpan.FromSeconds(30)
        });

        // Timeout per attempt
        builder.AddTimeout(TimeSpan.FromSeconds(10));
    });
```

**Detailed Polly patterns:** See `references/polly-patterns.md`

## Quick Start: Brighter Message Handler

### Basic Retry Policy

```csharp
public class OrderCreatedHandler : RequestHandler<OrderCreated>
{
    [UsePolicy("retry-policy", step: 1)]
    public override OrderCreated Handle(OrderCreated command)
    {
        // Process order
        return base.Handle(command);
    }
}
```

### Policy Registry Setup

```csharp
var policyRegistry = new PolicyRegistry
{
    {
        "retry-policy",
        Policy
            .Handle<Exception>()
            .WaitAndRetry(
                retryCount: 3,
                sleepDurationProvider: attempt =>
                    TimeSpan.FromSeconds(Math.Pow(2, attempt)))
    }
};

services.AddBrighter()
    .UseExternalBus(/* config */)
    .UsePolicyRegistry(policyRegistry);
```

**Detailed Brighter patterns:** See `references/brighter-resilience.md`

## Pattern Decision Tree

### When to Use Retry

**Use retry when:**

- Failure is likely transient (network blip, temporary 503)
- Operation is idempotent
- Delay between retries is acceptable

**Don't use retry when:**

- Failure is business logic (validation error, 400 Bad Request)
- Operation is not idempotent (unless with idempotency key)
- Immediate response required

### When to Use Circuit Breaker

**Use circuit breaker when:**

- Calling external services that might be down
- Need to fail fast instead of waiting
- Want to prevent cascade failures
- Service recovery needs time

**Configuration guidance:** See `references/circuit-breaker-config.md`

### When to Use DLQ

**Use DLQ when:**

- Message cannot be processed after max retries
- Business rule prevents processing
- Manual intervention needed
- Audit trail required for failures

**DLQ patterns:** See `references/dlq-patterns.md`

## Retry Strategy Patterns

### Immediate Retry

For very transient failures:

```csharp
.AddRetry(new RetryStrategyOptions
{
    MaxRetryAttempts = 2,
    Delay = TimeSpan.Zero  // Immediate retry
});
```

### Exponential Backoff

For transient failures that need time:

```csharp
.AddRetry(new RetryStrategyOptions
{
    MaxRetryAttempts = 4,
    Delay = TimeSpan.FromSeconds(1),
    BackoffType = DelayBackoffType.Exponential,
    UseJitter = true  // Prevents thundering herd
});
```

**Delays:** 1s → 2s → 4s → 8s (with jitter)

### Linear Backoff

For rate-limited services:

```csharp
.AddRetry(new RetryStrategyOptions
{
    MaxRetryAttempts = 3,
    Delay = TimeSpan.FromSeconds(2),
    BackoffType = DelayBackoffType.Linear
});
```

**Delays:** 2s → 4s → 6s

**Full retry strategies:** See `references/retry-strategies.md`

## Circuit Breaker Configuration

### Conservative (Sensitive Service)

```csharp
.AddCircuitBreaker(new CircuitBreakerStrategyOptions
{
    FailureRatio = 0.25,        // Open after 25% failures
    MinimumThroughput = 5,       // Need at least 5 calls to evaluate
    SamplingDuration = TimeSpan.FromSeconds(10),
    BreakDuration = TimeSpan.FromSeconds(60)  // Stay open 60s
});
```

### Aggressive (High Availability)

```csharp
.AddCircuitBreaker(new CircuitBreakerStrategyOptions
{
    FailureRatio = 0.5,          // Open after 50% failures
    MinimumThroughput = 20,      // Need 20 calls before evaluation
    SamplingDuration = TimeSpan.FromSeconds(30),
    BreakDuration = TimeSpan.FromSeconds(15)  // Quick recovery attempt
});
```

**Detailed configuration:** See `references/circuit-breaker-config.md`

## Dead Letter Queue Pattern

### When Message Processing Fails

```text
1. Message received
2. Handler attempts processing
3. Failure occurs
4. Retry policy applied (1...N attempts)
5. All retries exhausted
6. Message moved to DLQ
7. Alert/monitoring triggered
8. Manual investigation
```

### Brighter DLQ Setup

```csharp
services.AddBrighter()
    .UseExternalBus(config =>
    {
        config.Publication.RequeueDelayInMs = 500;
        config.Publication.RequeueCount = 3;
        // After 3 requeues, message goes to DLQ
    });
```

**Full DLQ patterns:** See `references/dlq-patterns.md`

## Combined Patterns

### HTTP Client with Full Resilience

```csharp
builder.Services.AddHttpClient<IPaymentGateway, PaymentGateway>()
    .AddResilienceHandler("payment-gateway", builder =>
    {
        // Order matters: outer to inner

        // 1. Total timeout (outer boundary)
        builder.AddTimeout(TimeSpan.FromSeconds(30));

        // 2. Retry (with circuit breaker inside)
        builder.AddRetry(new HttpRetryStrategyOptions
        {
            MaxRetryAttempts = 3,
            Delay = TimeSpan.FromMilliseconds(500),
            BackoffType = DelayBackoffType.Exponential,
            UseJitter = true
        });

        // 3. Circuit breaker
        builder.AddCircuitBreaker(new HttpCircuitBreakerStrategyOptions
        {
            FailureRatio = 0.5,
            MinimumThroughput = 10,
            BreakDuration = TimeSpan.FromSeconds(30)
        });

        // 4. Per-attempt timeout (inner)
        builder.AddTimeout(TimeSpan.FromSeconds(5));
    });
```

### Message Handler with Fallback

```csharp
public class ProcessPaymentHandler : RequestHandler<ProcessPayment>
{
    [UsePolicy("circuit-breaker", step: 1)]
    [UsePolicy("retry", step: 2)]
    [UsePolicy("fallback", step: 3)]
    public override ProcessPayment Handle(ProcessPayment command)
    {
        _paymentService.Process(command);
        return base.Handle(command);
    }
}
```

## Observability

### Polly Telemetry

```csharp
services.AddResiliencePipeline("my-pipeline", builder =>
{
    builder.AddRetry(/* options */)
        .ConfigureTelemetry(LoggerFactory.Create(b => b.AddConsole()));
});
```

### Key Metrics to Monitor

| Metric | Purpose | Alert Threshold |
| --- | --- | --- |
| Retry count | Track transient failures | > 3 per minute |
| Circuit state | Track service health | State = Open |
| DLQ depth | Track processing failures | > 0 |
| Timeout rate | Track slow services | > 5% |

## Anti-Patterns

### Over-Retrying

**Problem:** Retrying too many times, too quickly.

```csharp
// BAD: 10 immediate retries
.AddRetry(new RetryStrategyOptions { MaxRetryAttempts = 10 });
```

**Fix:** Use exponential backoff, limit retries:

```csharp
// GOOD: 3 retries with backoff
.AddRetry(new RetryStrategyOptions
{
    MaxRetryAttempts = 3,
    Delay = TimeSpan.FromSeconds(1),
    BackoffType = DelayBackoffType.Exponential
});
```

### Retrying Non-Transient Failures

**Problem:** Retrying business logic failures.

```csharp
// BAD: Retrying 400 Bad Request
ShouldHandle = new PredicateBuilder<HttpResponseMessage>()
    .HandleResult(r => !r.IsSuccessStatusCode)
```

**Fix:** Only retry transient failures:

```csharp
// GOOD: Only retry transient HTTP codes
ShouldHandle = new PredicateBuilder<HttpResponseMessage>()
    .Handle<HttpRequestException>()
    .HandleResult(r => r.StatusCode is
        HttpStatusCode.ServiceUnavailable or
        HttpStatusCode.GatewayTimeout or
        HttpStatusCode.RequestTimeout)
```

### Missing Circuit Breaker

**Problem:** Retrying endlessly when service is down.

**Fix:** Always pair retry with circuit breaker for external calls.

### DLQ as Black Hole

**Problem:** Messages go to DLQ and are never processed.

**Fix:**

- Monitor DLQ depth
- Set up alerts
- Implement replay mechanism
- Document investigation procedures

## References

- `references/polly-patterns.md` - Comprehensive Polly v8 patterns
- `references/circuit-breaker-config.md` - Circuit breaker configuration guide
- `references/retry-strategies.md` - Retry strategy patterns
- `references/brighter-resilience.md` - Brighter message handler resilience
- `references/dlq-patterns.md` - Dead letter queue patterns

## Related Skills

- `fitness-functions` - Test resilience with performance fitness functions
- `modular-architecture` - Isolate resilience concerns by module
- `adr-management` - Document resilience decisions

---

**Last Updated:** 2025-12-22

## Version History

- **v1.0.0** (2025-12-26): Initial release

---
