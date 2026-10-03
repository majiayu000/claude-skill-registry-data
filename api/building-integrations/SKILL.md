---
name: building-integrations
description: Patterns for robust third-party API integrations — webhook verification, idempotency, retry/Polly, circuit breakers, HttpClientFactory.
when_to_use: Reach for this when wiring up an external service (Stripe, Twilio, SendGrid, HubSpot, etc.) and you need reliability patterns — signature verification, idempotency keys, retries, circuit breakers. For Clerk *auth* specifically use using-clerk; for first-party LLM SDKs use the using-*-platform skills. Generic integration-reliability skill (C#/.NET-leaning).
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Building Integrations Skill

Patterns for integrating third-party APIs in .NET applications.
Covers adapter design, webhook verification, resilience, and secret management.

---

## When to Use

Loaded by `backend-developer` when:
- User mentions third-party API, webhook, or external service integration
- Stripe, Twilio, SendGrid, HubSpot, Everflow, or similar vendor names appear
- `IHttpClientFactory`, `Polly`, or `ResiliencePipeline` usage detected
- Webhook endpoints or signature verification logic needed

---

## Integration Architecture

Wrap every vendor SDK behind a domain interface. The adapter translates
vendor types and errors into your domain `Result<T>`.

```csharp
// Domain interface - small, focused, one per capability
public interface IPaymentGateway
{
    Task<Result<PaymentConfirmation>> ChargeAsync(
        PaymentRequest request, CancellationToken ct = default);
    Task<Result<RefundConfirmation>> RefundAsync(
        string transactionId, decimal amount, CancellationToken ct = default);
}
```

```csharp
// Adapter maps vendor errors at the boundary
public sealed class StripePaymentGateway : IPaymentGateway
{
    private readonly IStripeClient _client;
    private readonly ILogger<StripePaymentGateway> _logger;

    public StripePaymentGateway(IStripeClient client,
        ILogger<StripePaymentGateway> logger)
    { _client = client; _logger = logger; }

    public async Task<Result<PaymentConfirmation>> ChargeAsync(
        PaymentRequest request, CancellationToken ct)
    {
        try
        {
            var intent = await new PaymentIntentService(_client)
                .CreateAsync(new PaymentIntentCreateOptions
                {
                    Amount = (long)(request.Amount * 100),
                    Currency = request.Currency,
                    PaymentMethod = request.PaymentMethodId,
                    Confirm = true,
                }, cancellationToken: ct);
            return Result<PaymentConfirmation>.Success(
                new PaymentConfirmation(intent.Id, intent.Status));
        }
        catch (StripeException ex)
        {
            _logger.LogWarning(ex, "Stripe charge failed: {Code}",
                ex.StripeError?.Code);
            return Result<PaymentConfirmation>.Failure(
                MapStripeError(ex));
        }
    }

    private static Error MapStripeError(StripeException ex) =>
        ex.StripeError?.Code switch
        {
            "card_declined" => Error.PaymentDeclined,
            "expired_card"  => Error.PaymentMethodExpired,
            _ => Error.IntegrationFailure(ex.Message),
        };
}
```

**Interface segregation**: prefer focused interfaces (`IEmailSender`,
`IEmailTemplateRenderer`) over one monolithic vendor interface.

---

## Webhook Handling

### HMAC-SHA256 Signature Verification

Always verify signatures before processing. Use raw body bytes because
model binding can alter whitespace or encoding.

```csharp
public static class WebhookSignatureValidator
{
    public static bool VerifyHmacSha256(
        byte[] payload, string signature, string secret)
    {
        using var hmac = new HMACSHA256(Encoding.UTF8.GetBytes(secret));
        var computed = Convert.ToHexString(
            hmac.ComputeHash(payload)).ToLowerInvariant();
        // Constant-time comparison prevents timing attacks
        return CryptographicOperations.FixedTimeEquals(
            Encoding.UTF8.GetBytes(computed),
            Encoding.UTF8.GetBytes(signature));
    }
}
```

### Stripe Webhook Endpoint

```csharp
private static async Task<IResult> HandleStripeWebhook(
    HttpContext context, IOptions<StripeSettings> settings,
    IIdempotencyStore store, ISender sender, CancellationToken ct)
{
    // 1. Read raw body (do NOT use model binding)
    context.Request.EnableBuffering();
    using var reader = new StreamReader(context.Request.Body);
    var rawBody = await reader.ReadToEndAsync(ct);

    // 2. Verify signature via Stripe SDK
    Event stripeEvent;
    try {
        stripeEvent = EventUtility.ConstructEvent(rawBody,
            context.Request.Headers["Stripe-Signature"].ToString(),
            settings.Value.WebhookSecret);
    } catch (StripeException) { return TypedResults.Unauthorized(); }

    // 3. Idempotency: deduplicate by event ID
    if (await store.ExistsAsync(stripeEvent.Id, ct))
        return TypedResults.Ok();

    // 4. Process and mark done
    await sender.Send(new ProcessStripeEventCommand(stripeEvent), ct);
    await store.MarkProcessedAsync(stripeEvent.Id, ct);
    return TypedResults.Ok();
}
```

### Generic HMAC Webhook (non-Stripe)

Key steps for any vendor webhook:
1. Read raw body bytes (`EnableBuffering` + `ReadAllBytesAsync`)
2. Verify HMAC-SHA256 against header (e.g., `X-Signature`)
3. Reject stale events (timestamp older than 5 minutes)
4. Extract idempotency key from header; return 200 if already processed
5. Deserialize, dispatch via MediatR, mark processed

```csharp
public interface IIdempotencyStore
{
    Task<bool> ExistsAsync(string key, CancellationToken ct = default);
    Task MarkProcessedAsync(string key, CancellationToken ct = default);
}
```

---

## HTTP Client Patterns

Never create `HttpClient` directly. Use `IHttpClientFactory` for proper
socket management and DNS rotation.

```csharp
// Typed client
public sealed class HubSpotClient
{
    private readonly HttpClient _http;
    private readonly ILogger<HubSpotClient> _logger;

    public HubSpotClient(HttpClient http, ILogger<HubSpotClient> logger)
    { _http = http; _logger = logger; }

    public async Task<Result<ContactDto>> GetContactAsync(
        string contactId, CancellationToken ct)
    {
        var response = await _http.GetAsync(
            $"/crm/v3/objects/contacts/{contactId}", ct);
        if (!response.IsSuccessStatusCode)
            return Result<ContactDto>.Failure(
                MapHttpError(response.StatusCode));
        var contact = await response.Content
            .ReadFromJsonAsync<ContactDto>(ct);
        return Result<ContactDto>.Success(contact!);
    }
}
```

### DI Registration with Resilience

```csharp
services.AddHttpClient<HubSpotClient>((sp, client) =>
{
    var s = sp.GetRequiredService<IOptions<HubSpotSettings>>().Value;
    client.BaseAddress = new Uri(s.BaseUrl);
    client.DefaultRequestHeaders.Authorization =
        new AuthenticationHeaderValue("Bearer", s.ApiKey);
    client.Timeout = TimeSpan.FromSeconds(30);
})
.ConfigurePrimaryHttpMessageHandler(() => new SocketsHttpHandler
{
    PooledConnectionLifetime = TimeSpan.FromMinutes(2),
})
.AddStandardResilienceHandler(); // Polly v8 defaults
```

### Request/Response Logging

Use a `DelegatingHandler` that logs method, URI, and status code.
Redact sensitive headers (`Authorization`, `X-Api-Key`, `Cookie`).

---

## Rate Limiting and Backoff

### Polly v8 Resilience Pipeline

Use Polly v8 `ResiliencePipeline`, not the legacy v7 `Policy` API.

```csharp
services.AddHttpClient<HubSpotClient>()
    .AddResilienceHandler("hubspot-pipeline", builder =>
    {
        // Retry with exponential backoff + jitter
        builder.AddRetry(new HttpRetryStrategyOptions
        {
            MaxRetryAttempts = 3,
            Delay = TimeSpan.FromSeconds(1),
            BackoffType = DelayBackoffType.ExponentialWithJitter,
            ShouldHandle = new PredicateBuilder<HttpResponseMessage>()
                .HandleResult(r =>
                    r.StatusCode == HttpStatusCode.TooManyRequests
                    || r.StatusCode >= HttpStatusCode.InternalServerError)
                .Handle<HttpRequestException>()
                .Handle<TimeoutRejectedException>(),
            OnRetry = static args =>
            {
                // Respect Retry-After header on 429
                if (args.Outcome.Result?.StatusCode
                    == HttpStatusCode.TooManyRequests
                    && args.Outcome.Result.Headers.RetryAfter
                        ?.Delta is { } retryAfter)
                    args.RetryDelay = retryAfter;
                return ValueTask.CompletedTask;
            },
        });

        // Circuit breaker
        builder.AddCircuitBreaker(new HttpCircuitBreakerStrategyOptions
        {
            FailureRatio = 0.5,
            SamplingDuration = TimeSpan.FromSeconds(30),
            MinimumThroughput = 10,
            BreakDuration = TimeSpan.FromSeconds(15),
        });

        builder.AddTimeout(TimeSpan.FromSeconds(10));
    });
```

### Token Bucket for Outbound Rate Limiting

Use a `SemaphoreSlim`-guarded token bucket when the vendor has a strict
requests-per-second limit and you need client-side throttling beyond
what Polly retry provides.

---

## Circuit Breaker Pattern

| State | Behavior |
|-------|----------|
| **Closed** | Requests pass through; failures counted |
| **Open** | Requests fail immediately; no calls to vendor |
| **Half-Open** | Limited probe requests test recovery |

### Standalone Circuit Breaker (non-HTTP)

```csharp
services.AddResiliencePipeline("stripe-circuit", builder =>
{
    builder.AddCircuitBreaker(new CircuitBreakerStrategyOptions
    {
        FailureRatio = 0.5,
        SamplingDuration = TimeSpan.FromSeconds(30),
        MinimumThroughput = 10,
        BreakDuration = TimeSpan.FromSeconds(15),
        ShouldHandle = new PredicateBuilder()
            .Handle<HttpRequestException>()
            .Handle<TimeoutException>(),
    });
});

// Consume via keyed DI
public sealed class StripeGateway(
    [FromKeyedServices("stripe-circuit")] ResiliencePipeline pipeline)
{
    public async Task<Result<T>> ExecuteAsync<T>(
        Func<CancellationToken, ValueTask<Result<T>>> action,
        CancellationToken ct)
        => await pipeline.ExecuteAsync(action, ct);
}
```

---

## Secret Management

Never read secrets from environment variables directly in application
code. Bind through the configuration system.

```csharp
public sealed class StripeSettings
{
    public const string SectionName = "Stripe";
    [Required] public required string ApiKey { get; init; }
    [Required] public required string WebhookSecret { get; init; }
}

// Program.cs - Azure Key Vault for production
builder.Configuration.AddAzureKeyVault(
    new Uri(builder.Configuration["KeyVault:Uri"]!),
    new DefaultAzureCredential());

services.AddOptionsWithValidateOnStart<StripeSettings>()
    .BindConfiguration(StripeSettings.SectionName)
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

**Rules**: Store in Key Vault (prod) or user-secrets (dev). Bind via
`IOptions<T>` with `[Required]`. Never log settings containing secrets.

---

## Testing Integrations

### Recorded HTTP Fixtures

Store real vendor responses as JSON files and replay in tests.

```csharp
public static HttpResponseMessage SuccessFixture() =>
    new(HttpStatusCode.OK)
    {
        Content = JsonContent.Create(
            JsonDocument.Parse(File.ReadAllText(
                "fixtures/hubspot/get-contact-200.json")).RootElement),
    };
```

### WireMock for Integration Testing

```csharp
public class HubSpotTests : IAsyncLifetime
{
    private WireMockServer _server = null!;
    private HubSpotClient _client = null!;

    public Task InitializeAsync()
    {
        _server = WireMockServer.Start();
        _client = new HubSpotClient(
            new HttpClient { BaseAddress = new Uri(_server.Url!) },
            NullLogger<HubSpotClient>.Instance);
        return Task.CompletedTask;
    }

    [Fact]
    public async Task GetContact_Returns_On_200()
    {
        _server.Given(Request.Create()
                .WithPath("/crm/v3/objects/contacts/123").UsingGet())
            .RespondWith(Response.Create().WithStatusCode(200)
                .WithBodyAsJson(new { id = "123" }));

        var result = await _client.GetContactAsync("123", default);
        result.IsSuccess.Should().BeTrue();
    }

    public Task DisposeAsync() { _server.Stop(); return Task.CompletedTask; }
}
```

### Test Doubles for Integration Interfaces

```csharp
var gateway = Substitute.For<IPaymentGateway>();
gateway.ChargeAsync(Arg.Any<PaymentRequest>(), Arg.Any<CancellationToken>())
    .Returns(Result<PaymentConfirmation>.Success(
        new PaymentConfirmation("pi_123", "succeeded")));
```

---

## Error Mapping

### HTTP Status Code Mapping

| Vendor Status | Domain Error | Category |
|---------------|-------------|----------|
| 400 | `Error.Validation` | Permanent |
| 401 | `Error.AuthenticationFailed` | Permanent |
| 403 | `Error.Forbidden` | Permanent |
| 404 | `Error.NotFound` | Permanent |
| 409 | `Error.Conflict` | Permanent |
| 422 | `Error.UnprocessableEntity` | Permanent |
| 429 | `Error.RateLimited` | Transient |
| 500+ | `Error.IntegrationFailure` | Transient |
| Timeout | `Error.Timeout` | Transient |

```csharp
public static bool IsTransient(HttpStatusCode status) =>
    status is HttpStatusCode.TooManyRequests
        or HttpStatusCode.RequestTimeout or HttpStatusCode.BadGateway
        or HttpStatusCode.ServiceUnavailable
        or HttpStatusCode.GatewayTimeout
        or HttpStatusCode.InternalServerError;
```

### Dead-Letter for Unprocessable Webhooks

Persist failed webhooks after exhausting retries for manual review.

```csharp
public interface IDeadLetterStore
{
    Task PersistAsync(string source, string eventId,
        string payload, string reason, CancellationToken ct = default);
}
```

---

## Quick Reference Card

### Key NuGet Packages

| Package | Purpose |
|---------|---------|
| `Microsoft.Extensions.Http` | `IHttpClientFactory` |
| `Microsoft.Extensions.Http.Resilience` | Polly v8 HTTP integration |
| `Microsoft.Extensions.Resilience` | Non-HTTP resilience pipelines |
| `Polly.Core` | Core resilience abstractions |
| `Stripe.net` | Stripe SDK |
| `Azure.Identity` | Azure Key Vault auth |
| `Azure.Extensions.AspNetCore.Configuration.Secrets` | Key Vault config |
| `WireMock.Net` | HTTP mock server for tests |

### Patterns Summary

| Pattern | When | Key Rule |
|---------|------|----------|
| Adapter | Every vendor | Domain interface + vendor impl |
| Webhook signature | Incoming webhooks | Verify HMAC before processing |
| Idempotency | All webhook handlers | Deduplicate by event ID |
| Typed HttpClient | All outbound HTTP | Never `new HttpClient()` |
| Polly v8 retry | Transient failures | Exponential backoff + jitter |
| Circuit breaker | Unreliable vendors | Fail fast when vendor is down |
| IOptions | All secrets/config | Bind + validate, no raw env vars |
| Dead letter | Webhook processing | Persist unprocessable events |
| Recorded fixtures | Unit tests | Replay real vendor responses |
| WireMock | Integration tests | Full HTTP round-trip verification |
