---
name: using-azure-functions
description: Build .NET 8/9 Azure Functions (isolated worker) — HTTP, Service Bus, Timer, and Durable Functions triggers.
when_to_use: Reach for this when writing serverless function code on Azure (host.json, [Function] attributes, isolated worker). For general .NET app/service code use developing-with-dotnet; for provisioning the Azure infra around it use using-terraform-azure; for the deploy pipeline use managing-azure-devops. Serverless app-code skill.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
paths:
  - "host.json"
  - "**/*Function*.cs"
  - "function.json"
  - "local.settings.json"
---

# Azure Functions Development Skill

**Version**: 1.0.0 | **Target**: <500 lines | **Purpose**: Fast reference for Azure Functions isolated worker model

---

## When to Use

**Auto-Detection Triggers**:
- `host.json` present in project
- `*.csproj` with `Microsoft.Azure.Functions.Worker` package reference
- User mentions "Azure Functions", "serverless", or "function app"

**Progressive Disclosure**:
- **This file (SKILL.md)**: Quick reference for immediate use
- **[REFERENCE.md](REFERENCE.md)**: Migration guides, advanced Durable Functions, managed identity, deployment

---

## CRITICAL: Isolated Worker Model Only

**The in-process model reaches end-of-life November 2026.** ALL new code MUST use the **isolated worker model**.

| Aspect | In-Process (DEPRECATED) | Isolated Worker (USE THIS) |
|--------|------------------------|---------------------------|
| Host builder | `ConfigureFunctionsWorkerDefaults()` | `ConfigureFunctionsWebApplication()` |
| HTTP model | `HttpRequest` / `IActionResult` | ASP.NET Core integration |
| Middleware | Function filters only | Full ASP.NET Core middleware pipeline |
| NuGet root | `Microsoft.Azure.WebJobs.*` | `Microsoft.Azure.Functions.Worker.*` |

**CRITICAL**: Use `ConfigureFunctionsWebApplication()` NOT `ConfigureFunctionsWorkerDefaults()`.
The `WebApplication` variant enables ASP.NET Core integration for HTTP triggers.

### Required NuGet Packages

```xml
<PackageReference Include="Microsoft.Azure.Functions.Worker" Version="2.*" />
<PackageReference Include="Microsoft.Azure.Functions.Worker.Sdk" Version="2.*" />
<PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.Http.AspNetCore" Version="2.*" />
<PackageReference Include="Microsoft.ApplicationInsights.WorkerService" Version="2.*" />
```

---

## Program.cs Setup

```csharp
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var host = new HostBuilder()
    .ConfigureFunctionsWebApplication(builder =>
    {
        builder.UseMiddleware<ExceptionHandlingMiddleware>();
    })
    .ConfigureServices(services =>
    {
        services.AddApplicationInsightsTelemetryWorkerService();
        services.ConfigureFunctionsApplicationInsights();
        services.AddSingleton<IMyService, MyService>();
        services.AddHttpClient<IExternalApi, ExternalApiClient>();
    })
    .Build();

host.Run();
```

### Custom Middleware

```csharp
public class ExceptionHandlingMiddleware : IFunctionsWorkerMiddleware
{
    private readonly ILogger<ExceptionHandlingMiddleware> _logger;
    public ExceptionHandlingMiddleware(ILogger<ExceptionHandlingMiddleware> logger) => _logger = logger;

    public async Task Invoke(FunctionContext context, FunctionExecutionDelegate next)
    {
        try { await next(context); }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unhandled exception in {Function}", context.FunctionDefinition.Name);
            throw;
        }
    }
}
```

---

## HTTP Triggers

With `ConfigureFunctionsWebApplication`, HTTP triggers use standard ASP.NET Core types.

```csharp
public class ProductFunctions
{
    private readonly ILogger<ProductFunctions> _logger;
    private readonly IProductService _productService;

    public ProductFunctions(ILogger<ProductFunctions> logger, IProductService productService)
    {
        _logger = logger;
        _productService = productService;
    }

    [Function("GetProduct")]
    public async Task<IActionResult> GetProduct(
        [HttpTrigger(AuthorizationLevel.Function, "get", Route = "products/{id}")] HttpRequest req,
        string id)
    {
        var product = await _productService.GetByIdAsync(id);
        return product is null ? new NotFoundResult() : new OkObjectResult(product);
    }

    [Function("CreateProduct")]
    public async Task<IActionResult> CreateProduct(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "products")] HttpRequest req,
        [FromBody] CreateProductRequest body)
    {
        if (string.IsNullOrWhiteSpace(body.Name))
            return new BadRequestObjectResult(new { error = "Name is required" });

        var product = await _productService.CreateAsync(body);
        return new CreatedResult($"/products/{product.Id}", product);
    }
}
```

### Multiple Outputs (HTTP + Queue)

```csharp
public class MultiOutputResult
{
    [HttpResult]
    public IActionResult HttpResponse { get; set; } = default!;

    [ServiceBusOutput("orders", Connection = "ServiceBusConnection")]
    public string? QueueMessage { get; set; }
}
```

---

## Service Bus Triggers

**CRITICAL**: Use `ServiceBusReceivedMessage` (Extension v5.x), NOT the old `Message` class.

**CRITICAL**: `[FixedDelayRetry]` and `[ExponentialBackoffRetry]` are **REMOVED** for Service Bus triggers.
Use host.json `clientRetryOptions` instead (see [Retry and Error Handling](#retry-and-error-handling)).

```csharp
public class OrderProcessor
{
    private readonly ILogger<OrderProcessor> _logger;
    private readonly IOrderService _orderService;

    public OrderProcessor(ILogger<OrderProcessor> logger, IOrderService orderService)
    {
        _logger = logger;
        _orderService = orderService;
    }

    [Function("ProcessOrder")]
    public async Task ProcessOrder(
        [ServiceBusTrigger("orders", Connection = "ServiceBusConnection")]
        ServiceBusReceivedMessage message,
        ServiceBusMessageActions messageActions)
    {
        try
        {
            var order = message.Body.ToObjectFromJson<OrderMessage>();
            await _orderService.ProcessAsync(order);
            await messageActions.CompleteMessageAsync(message);
        }
        catch (Exception ex) when (ex is not OperationCanceledException)
        {
            _logger.LogError(ex, "Failed to process {MessageId}", message.MessageId);
            if (message.DeliveryCount >= 3)
                await messageActions.DeadLetterMessageAsync(message,
                    deadLetterReason: "MaxRetriesExceeded",
                    deadLetterErrorDescription: ex.Message);
            else
                await messageActions.AbandonMessageAsync(message);
        }
    }
}
```

### Topic Subscription Trigger

```csharp
[Function("ProcessNotification")]
public async Task ProcessNotification(
    [ServiceBusTrigger("notifications", "email-subscription", Connection = "ServiceBusConnection")]
    ServiceBusReceivedMessage message,
    ServiceBusMessageActions messageActions)
{
    var notification = message.Body.ToObjectFromJson<NotificationMessage>();
    await _notificationService.SendEmailAsync(notification);
    await messageActions.CompleteMessageAsync(message);
}
```

### Message Settlement

| Action | When | Method |
|--------|------|--------|
| Complete | Processed successfully | `messageActions.CompleteMessageAsync(message)` |
| Abandon | Transient failure | `messageActions.AbandonMessageAsync(message)` |
| Dead-letter | Permanent failure | `messageActions.DeadLetterMessageAsync(message, reason, desc)` |
| Defer | Process later | `messageActions.DeferMessageAsync(message)` |

---

## Timer Triggers

NCrontab 6-field format: `{second} {minute} {hour} {day} {month} {day-of-week}`.

```csharp
[Function("CleanupExpiredSessions")]
public async Task CleanupExpiredSessions(
    [TimerTrigger("0 */5 * * * *")] TimerInfo timerInfo)
{
    _logger.LogInformation("Cleanup triggered at {Time}", DateTime.UtcNow);
    if (timerInfo.IsPastDue)
        _logger.LogWarning("Timer is past due");
    await _cleanupService.RemoveExpiredSessionsAsync();
}
```

### CRON Quick Reference (6-Field)

| Schedule | Expression |
|----------|-----------|
| Every minute | `0 * * * * *` |
| Every 5 minutes | `0 */5 * * * *` |
| Every hour | `0 0 * * * *` |
| Daily at 2 AM UTC | `0 0 2 * * *` |
| Weekdays at 9 AM | `0 0 9 * * 1-5` |
| Monthly 1st midnight | `0 0 0 1 * *` |

---

## Durable Functions

### CRITICAL: Orchestrator Determinism Rules

Orchestrator code is replayed on each await. It MUST be deterministic:

| PROHIBITED | Use Instead |
|-----------|-------------|
| `DateTime.UtcNow` | `context.CurrentUtcDateTime` |
| `Guid.NewGuid()` | `context.NewGuid()` |
| `Thread.Sleep()` / `Task.Delay()` | `context.CreateTimer(fireAt)` |
| HTTP calls, DB queries, file I/O | Activity functions |
| `Random` / non-deterministic APIs | Activities or `context.NewGuid()` seed |

### Orchestrator + Activity Pattern

```csharp
// HTTP starter
[Function("StartOrderWorkflow")]
public async Task<IActionResult> Start(
    [HttpTrigger(AuthorizationLevel.Function, "post", Route = "orders/workflow")] HttpRequest req,
    [FromBody] OrderRequest orderRequest,
    [DurableClient] DurableTaskClient client)
{
    var instanceId = await client.ScheduleNewOrchestrationInstanceAsync(
        nameof(OrderWorkflowOrchestrator), orderRequest);
    return new AcceptedResult($"/orders/workflow/{instanceId}", new { instanceId });
}

// Orchestrator - MUST be deterministic
[Function(nameof(OrderWorkflowOrchestrator))]
public static async Task<OrderResult> OrderWorkflowOrchestrator(
    [OrchestrationTrigger] TaskOrchestrationContext context)
{
    var order = context.GetInput<OrderRequest>()!;

    var isValid = await context.CallActivityAsync<bool>(nameof(ValidateOrderActivity), order);
    if (!isValid) return new OrderResult { Status = "rejected" };

    await context.CallActivityAsync(nameof(ReserveInventoryActivity), order);
    var payment = await context.CallActivityAsync<PaymentResult>(nameof(ProcessPaymentActivity), order);

    return new OrderResult { Status = "completed", CompletedAt = context.CurrentUtcDateTime };
}

// Activity functions - can perform I/O
[Function(nameof(ValidateOrderActivity))]
public async Task<bool> ValidateOrderActivity([ActivityTrigger] OrderRequest order)
    => await _validator.ValidateAsync(order);
```

### Fan-Out / Fan-In

```csharp
[Function(nameof(BatchProcessOrchestrator))]
public static async Task<BatchResult> BatchProcessOrchestrator(
    [OrchestrationTrigger] TaskOrchestrationContext context)
{
    var items = context.GetInput<List<WorkItem>>()!;
    var tasks = items.Select(item =>
        context.CallActivityAsync<ItemResult>(nameof(ProcessItemActivity), item));
    var results = await Task.WhenAll(tasks);
    return new BatchResult { Succeeded = results.Count(r => r.Success) };
}
```

> **More patterns**: See [REFERENCE.md](REFERENCE.md) for eternal orchestrations, human interaction, sub-orchestrations, and entity functions.

---

## Retry and Error Handling

### host.json for Service Bus (Recommended)

```json
{
  "version": "2.0",
  "extensions": {
    "serviceBus": {
      "clientRetryOptions": {
        "mode": "Exponential",
        "maxRetries": 3,
        "delay": "00:00:05",
        "maxDelay": "00:01:00"
      },
      "autoCompleteMessages": false
    }
  }
}
```

### Retry Attributes (HTTP and Timer Only)

```csharp
[Function("RetryableHttpFunction")]
[FixedDelayRetry(3, "00:00:10")]
public async Task<IActionResult> RetryableHttpFunction(
    [HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequest req) { /* ... */ }

[Function("RetryableTimerFunction")]
[ExponentialBackoffRetry(5, "00:00:05", "00:05:00")]
public async Task RetryableTimerFunction(
    [TimerTrigger("0 */5 * * * *")] TimerInfo timerInfo) { /* ... */ }
```

### Dead-Letter Processing

```csharp
[Function("ProcessDeadLetters")]
public async Task ProcessDeadLetters(
    [ServiceBusTrigger("orders/$deadletterqueue", Connection = "ServiceBusConnection")]
    ServiceBusReceivedMessage message,
    ServiceBusMessageActions messageActions)
{
    _logger.LogWarning("Dead-letter: {MessageId}, Reason: {Reason}",
        message.MessageId, message.DeadLetterReason);
    await _alertService.NotifyDeadLetterAsync(message);
    await messageActions.CompleteMessageAsync(message);
}
```

---

## host.json Configuration Reference

| Setting | Default | Description |
|---------|---------|-------------|
| `extensions.http.routePrefix` | `"api"` | HTTP route prefix |
| `extensions.http.maxConcurrentRequests` | `-1` | Max concurrent HTTP requests |
| `extensions.serviceBus.autoCompleteMessages` | `true` | Set `false` for explicit settlement |
| `extensions.serviceBus.maxConcurrentCalls` | `16` | Concurrent message processing |
| `extensions.serviceBus.prefetchCount` | `0` | Messages to prefetch |
| `extensions.durableTask.hubName` | `"DurableFunctionsHub"` | Durable Functions task hub name |
| `functionTimeout` | `"00:05:00"` | Max execution time (Consumption plan) |

---

## Quick Reference Card

### CLI

```bash
func init MyApp --dotnet-isolated    # Create project
func new --name MyFunc --template "HTTP trigger"  # Add function
func start                           # Run locally
func azure functionapp publish <name>  # Deploy
```

### Trigger Attributes

```csharp
[HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = "items/{id}")]
[ServiceBusTrigger("queue-name", Connection = "ServiceBusConnection")]
[ServiceBusTrigger("topic", "subscription", Connection = "ServiceBusConnection")]
[TimerTrigger("0 */5 * * * *")]
[OrchestrationTrigger]
[ActivityTrigger]
[DurableClient]
```

### Output Bindings

```csharp
[ServiceBusOutput("queue-name", Connection = "ServiceBusConnection")]
[BlobOutput("container/{name}", Connection = "StorageConnection")]
[TableOutput("TableName", Connection = "StorageConnection")]
```

### Common Mistakes

| Mistake | Correction |
|---------|-----------|
| `ConfigureFunctionsWorkerDefaults()` | `ConfigureFunctionsWebApplication()` |
| `[FixedDelayRetry]` on Service Bus | host.json `clientRetryOptions` |
| Old `Message` class | `ServiceBusReceivedMessage` |
| `DateTime.UtcNow` in orchestrators | `context.CurrentUtcDateTime` |
| `Guid.NewGuid()` in orchestrators | `context.NewGuid()` |
| I/O in orchestrators | Activity functions |
| `autoCompleteMessages: true` + manual settlement | Set `false` in host.json |
| 5-field CRON | 6-field NCrontab (include seconds) |

---

**Progressive Disclosure**: Start here for quick reference. Load [REFERENCE.md](REFERENCE.md)
for migration guides, advanced Durable Functions, managed identity, and deployment patterns.

**Skill Version**: 1.0.0
