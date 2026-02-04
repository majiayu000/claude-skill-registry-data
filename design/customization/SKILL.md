---
name: customization
description: Configure middleware extension hooks for affolterNET.Web.Bff. Use when adding custom middleware, extending the pipeline, or integrating third-party components.
---

# Customization Hooks

Extend the BFF middleware pipeline with custom components.

For complete reference, see [Library Guide](../../LIBRARY_GUIDE.md).

## Extension Points

The BFF provides two middleware hooks:

| Hook | Position | Use Case |
|------|----------|----------|
| `ConfigureAfterRoutingCustomMiddleware` | After routing | Tenant resolution, request context |
| `ConfigureBeforeEndpointsCustomMiddleware` | Before endpoints | Audit logging, final validation |

## Quick Start

```csharp
var options = builder.Services.AddBffServices(isDev, config, opts => {
    opts.ConfigureAfterRoutingCustomMiddleware = app => {
        app.UseMiddleware<TenantMiddleware>();
        app.UseMiddleware<RequestContextMiddleware>();
    };

    opts.ConfigureBeforeEndpointsCustomMiddleware = app => {
        app.UseMiddleware<AuditMiddleware>();
    };
});
```

## Middleware Pipeline Position

```
1. Exception Handling
2. Security Headers
3. HTTPS Redirection
4. Static Files
5. Swagger
6. Routing
7. ══► ConfigureAfterRoutingCustomMiddleware ◄══
8. CORS
9. Antiforgery
10. Authentication & Authorization
11. Token Refresh
12. RPT Middleware
13. NoUnauthorizedRedirect
14. Antiforgery Token
15. ══► ConfigureBeforeEndpointsCustomMiddleware ◄══
16. API 404 Handling
17. Endpoint Mapping
```

## Example: Tenant Middleware

```csharp
public class TenantMiddleware
{
    private readonly RequestDelegate _next;

    public TenantMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        // Extract tenant from route or header
        var tenantId = context.Request.RouteValues["tenant"]?.ToString()
            ?? context.Request.Headers["X-Tenant-Id"].FirstOrDefault();

        if (!string.IsNullOrEmpty(tenantId))
        {
            context.Items["TenantId"] = tenantId;
        }

        await _next(context);
    }
}
```

## Example: Audit Middleware

```csharp
public class AuditMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<AuditMiddleware> _logger;

    public AuditMiddleware(RequestDelegate next, ILogger<AuditMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var userId = context.User?.FindFirst(ClaimTypes.NameIdentifier)?.Value;
        var path = context.Request.Path;
        var method = context.Request.Method;

        _logger.LogInformation("User {UserId} accessing {Method} {Path}",
            userId, method, path);

        await _next(context);
    }
}
```

## Example: Request Timing

```csharp
public class TimingMiddleware
{
    private readonly RequestDelegate _next;

    public TimingMiddleware(RequestDelegate next) => _next = next;

    public async Task InvokeAsync(HttpContext context)
    {
        var sw = Stopwatch.StartNew();

        context.Response.OnStarting(() => {
            sw.Stop();
            context.Response.Headers["X-Response-Time"] = $"{sw.ElapsedMilliseconds}ms";
            return Task.CompletedTask;
        });

        await _next(context);
    }
}
```

## Accessing Services

```csharp
public async Task InvokeAsync(HttpContext context, IMyService myService)
{
    // Services can be injected via InvokeAsync
    var result = await myService.DoSomethingAsync();
    await _next(context);
}
```

## Troubleshooting

### Middleware not executing
- Verify hook is configured correctly
- Check middleware order dependencies
- Add logging to confirm registration

### User claims not available
- After-routing hook runs before authentication
- Use before-endpoints hook for authenticated context
