---
name: tenant-context-propagation
description: Tenant context resolution and propagation patterns for multi-tenant applications. Covers middleware, headers, claims, and distributed tracing.
allowed-tools: Read, Glob, Grep, Task, mcp__perplexity__search, mcp__perplexity__reason, mcp__microsoft-learn__microsoft_docs_search, mcp__microsoft-learn__microsoft_docs_fetch
---

# Tenant Context Propagation Skill

## When to Use This Skill

Use this skill when:

- **Tenant Context Propagation tasks** - Working on tenant context resolution and propagation patterns for multi-tenant applications. covers middleware, headers, claims, and distributed tracing
- **Planning or design** - Need guidance on Tenant Context Propagation approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Patterns for resolving and propagating tenant context throughout multi-tenant applications.

Tenant context must be available everywhere in the application - from web requests to background jobs to microservice calls. This skill covers strategies for establishing, propagating, and accessing tenant context reliably.

## Context Resolution Strategies

```text
Tenant Resolution Methods:
+------------------------------------------------------------------+
| Method          | Source              | Use Case                 |
+-----------------+---------------------+--------------------------+
| Subdomain       | acme.app.com        | SaaS with vanity URLs    |
| Custom Domain   | app.acme.com        | White-label enterprise   |
| Header          | X-Tenant-Id         | API/microservices        |
| JWT Claim       | tenant_id claim     | Authenticated requests   |
| Path Segment    | /tenants/{id}/...   | REST API design          |
| Query Parameter | ?tenant_id=...      | Admin/support tools      |
| Database Lookup | user → tenant       | User-first resolution    |
+-----------------+---------------------+--------------------------+
```

## Context Architecture

```text
+------------------------------------------------------------------+
|                    Tenant Context Flow                            |
+------------------------------------------------------------------+
|                                                                   |
|  +---------+    +------------+    +-------------+                 |
|  | Request |-->| Middleware |-->| Context      |                 |
|  | (HTTP)  |   | Resolver   |   | Provider     |                 |
|  +---------+   +------------+   +-------------+                  |
|                      |                  |                         |
|                      v                  v                         |
|              +-------------+    +---------------+                 |
|              | Validation  |    | AsyncLocal<T> |                 |
|              | (exists?)   |    | (Thread-safe) |                 |
|              +-------------+    +---------------+                 |
|                                        |                          |
|                    +-------------------+-------------------+      |
|                    v                   v                   v      |
|              +---------+        +---------+        +----------+   |
|              | Services|        | EF Core |        | Background|  |
|              |         |        | Filters |        | Jobs      |  |
|              +---------+        +---------+        +----------+   |
|                                                                   |
+------------------------------------------------------------------+
```

## Tenant Context Provider

### Interface Definition

```csharp
public interface ITenantContext
{
    Guid TenantId { get; }
    string TenantName { get; }
    string TenantSlug { get; }
    TenantSettings Settings { get; }
    bool IsResolved { get; }
}

public interface ITenantContextAccessor
{
    ITenantContext? Current { get; set; }
}
```

### AsyncLocal Implementation

```csharp
public sealed class TenantContextAccessor : ITenantContextAccessor
{
    private static readonly AsyncLocal<TenantContextHolder> _current = new();

    public ITenantContext? Current
    {
        get => _current.Value?.Context;
        set
        {
            var holder = _current.Value;
            if (holder != null)
            {
                holder.Context = null;
            }

            if (value != null)
            {
                _current.Value = new TenantContextHolder { Context = value };
            }
        }
    }

    private sealed class TenantContextHolder
    {
        public ITenantContext? Context { get; set; }
    }
}
```

## Resolution Middleware

### Subdomain Resolution

```csharp
public sealed class SubdomainTenantMiddleware(
    RequestDelegate next,
    ITenantContextAccessor contextAccessor,
    ITenantRepository tenants,
    ILogger<SubdomainTenantMiddleware> logger)
{
    private static readonly string[] ExcludedSubdomains = ["www", "api", "admin"];

    public async Task InvokeAsync(HttpContext context)
    {
        var host = context.Request.Host.Host;
        var subdomain = ExtractSubdomain(host);

        if (!string.IsNullOrEmpty(subdomain) && !ExcludedSubdomains.Contains(subdomain))
        {
            var tenant = await tenants.GetBySubdomainAsync(subdomain);
            if (tenant != null)
            {
                contextAccessor.Current = new TenantContext(tenant);
                logger.LogDebug("Resolved tenant {TenantId} from subdomain {Subdomain}",
                    tenant.Id, subdomain);
            }
            else
            {
                logger.LogWarning("Unknown subdomain: {Subdomain}", subdomain);
                context.Response.StatusCode = 404;
                return;
            }
        }

        await next(context);
    }

    private static string? ExtractSubdomain(string host)
    {
        var parts = host.Split('.');
        return parts.Length >= 3 ? parts[0] : null;
    }
}
```

### Header Resolution (APIs)

```csharp
public sealed class HeaderTenantMiddleware(
    RequestDelegate next,
    ITenantContextAccessor contextAccessor,
    ITenantRepository tenants)
{
    private const string TenantHeader = "X-Tenant-Id";

    public async Task InvokeAsync(HttpContext context)
    {
        if (context.Request.Headers.TryGetValue(TenantHeader, out var tenantIdValue))
        {
            if (Guid.TryParse(tenantIdValue, out var tenantId))
            {
                var tenant = await tenants.GetByIdAsync(tenantId);
                if (tenant != null)
                {
                    contextAccessor.Current = new TenantContext(tenant);
                }
            }
        }

        await next(context);
    }
}
```

### JWT Claim Resolution

```csharp
public sealed class ClaimsTenantMiddleware(
    RequestDelegate next,
    ITenantContextAccessor contextAccessor,
    ITenantRepository tenants)
{
    public async Task InvokeAsync(HttpContext context)
    {
        if (context.User.Identity?.IsAuthenticated == true)
        {
            var tenantClaim = context.User.FindFirst("tenant_id");
            if (tenantClaim != null && Guid.TryParse(tenantClaim.Value, out var tenantId))
            {
                var tenant = await tenants.GetByIdAsync(tenantId);
                if (tenant != null)
                {
                    contextAccessor.Current = new TenantContext(tenant);
                }
            }
        }

        await next(context);
    }
}
```

## Propagation to Services

### EF Core Query Filters

```csharp
public sealed class AppDbContext(
    DbContextOptions<AppDbContext> options,
    ITenantContextAccessor tenantContext) : DbContext(options)
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Apply tenant filter to all tenant-scoped entities
        foreach (var entityType in modelBuilder.Model.GetEntityTypes())
        {
            if (typeof(ITenantScoped).IsAssignableFrom(entityType.ClrType))
            {
                modelBuilder.Entity(entityType.ClrType)
                    .AddQueryFilter<ITenantScoped>(e =>
                        e.TenantId == tenantContext.Current!.TenantId);
            }
        }
    }

    public override Task<int> SaveChangesAsync(CancellationToken ct = default)
    {
        // Auto-set TenantId on new entities
        foreach (var entry in ChangeTracker.Entries<ITenantScoped>())
        {
            if (entry.State == EntityState.Added)
            {
                entry.Entity.TenantId = tenantContext.Current!.TenantId;
            }
        }

        return base.SaveChangesAsync(ct);
    }
}
```

### Background Job Propagation

```csharp
public sealed class TenantJobFilter(ITenantContextAccessor contextAccessor) : IJobFilter
{
    public void OnCreating(CreatingContext context)
    {
        // Capture tenant context when job is created
        if (contextAccessor.Current != null)
        {
            context.SetJobParameter("TenantId", contextAccessor.Current.TenantId);
        }
    }

    public void OnPerforming(PerformingContext context)
    {
        // Restore tenant context when job executes
        var tenantId = context.GetJobParameter<Guid?>("TenantId");
        if (tenantId.HasValue)
        {
            // Resolve and set tenant context
            var tenant = context.ServiceProvider
                .GetRequiredService<ITenantRepository>()
                .GetByIdAsync(tenantId.Value)
                .GetAwaiter().GetResult();

            if (tenant != null)
            {
                contextAccessor.Current = new TenantContext(tenant);
            }
        }
    }
}
```

### HTTP Client Propagation

```csharp
public sealed class TenantHeaderHandler(
    ITenantContextAccessor tenantContext) : DelegatingHandler
{
    protected override Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request,
        CancellationToken ct)
    {
        if (tenantContext.Current != null)
        {
            request.Headers.Add("X-Tenant-Id", tenantContext.Current.TenantId.ToString());
        }

        return base.SendAsync(request, ct);
    }
}

// Registration
services.AddHttpClient("downstream")
    .AddHttpMessageHandler<TenantHeaderHandler>();
```

## Distributed Tracing Integration

```csharp
public static class TenantTracing
{
    public static Activity? StartTenantActivity(
        ITenantContext context,
        string operationName)
    {
        var activity = Activity.Current?.Source.StartActivity(operationName);

        if (activity != null && context.IsResolved)
        {
            activity.SetTag("tenant.id", context.TenantId.ToString());
            activity.SetTag("tenant.name", context.TenantName);
        }

        return activity;
    }
}
```

## Best Practices

```text
Context Propagation Best Practices:
+------------------------------------------------------------------+
| Practice                    | Benefit                            |
+-----------------------------+------------------------------------+
| AsyncLocal for thread-safe  | Works across async/await           |
| Early resolution (middleware)| Available everywhere downstream   |
| Cached tenant data          | Avoid repeated DB lookups          |
| Validation in middleware    | Fail fast on invalid tenant        |
| Include in traces/logs      | Debugging multi-tenant issues      |
| Propagate to outbound calls | Consistent context in microservices|
+-----------------------------+------------------------------------+
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| ------------ | ------- | -------- |
| Static tenant | Not thread-safe | AsyncLocal |
| Late resolution | Missing context in services | Middleware |
| No validation | Invalid tenant access | Middleware validation |
| Missing propagation | Lost context in background jobs | Job filters |
| No logging | Hard to debug tenant issues | Include tenant in logs |

## Related Skills

- `tenancy-models` - Overall architecture context
- `database-isolation` - Database-level multi-tenancy
- `audit-logging` - Tenant-aware audit trails

## MCP Research

For current patterns:

```text
perplexity: "multi-tenant context propagation .NET 2024" "AsyncLocal tenant context"
microsoft-learn: "multi-tenant middleware ASP.NET Core" "EF Core query filters"
```
