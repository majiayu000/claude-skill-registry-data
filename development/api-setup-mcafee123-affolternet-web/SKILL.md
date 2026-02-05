---
name: api-setup
description: Configure affolterNET.Web.Api service registration and middleware pipeline. Use when setting up AddApiServices, ConfigureApiApp, or configuring the API middleware order.
---

# API Setup

Configure the affolterNET.Web.Api service registration and middleware pipeline.

For complete reference, see [Library Guide](../../LIBRARY_GUIDE.md).

## Quick Start

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Step 1: Register services
var options = builder.Services.AddApiServices(
    builder.Environment.IsDevelopment(),
    builder.Configuration,
    opts => {
        opts.EnableSecurityHeaders = true;
        opts.ConfigureApi = api => {
            api.AuthMode = AuthenticationMode.Authorize;
        };
    });

var app = builder.Build();

// Step 2: Configure middleware
app.ConfigureApiApp(options);

app.Run();
```

## Configuration Options

### ApiAppOptions

| Property | Type | Description |
|----------|------|-------------|
| `EnableSecurityHeaders` | bool | Enable security headers middleware |
| `ConfigureApi` | Action<ApiOptions> | Configure API-specific options |
| `ConfigureAfterRoutingCustomMiddleware` | Action<IApplicationBuilder> | Add custom middleware after routing |
| `ConfigureBeforeEndpointsCustomMiddleware` | Action<IApplicationBuilder> | Add custom middleware before endpoints |

### ApiOptions

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `AuthMode` | AuthenticationMode | `None` | Authentication mode (None/Authenticate/Authorize) |

## Middleware Pipeline

The `ConfigureApiApp` configures middleware in this order:

1. Security Headers Middleware
2. Swagger/OpenAPI
3. Routing
4. Custom Middleware (after routing hook)
5. CORS
6. Authentication & Authorization + RPT Middleware
7. Custom Middleware (before endpoints hook)
8. Endpoint Mapping (with Health Checks)

## Common Patterns

### Development vs Production

```csharp
var options = builder.Services.AddApiServices(
    builder.Environment.IsDevelopment(),  // isDev flag
    builder.Configuration,
    opts => {
        // Development-specific config happens automatically
        // based on isDev flag
    });
```

### Adding Custom Middleware

```csharp
var options = builder.Services.AddApiServices(isDev, config, opts => {
    opts.ConfigureAfterRoutingCustomMiddleware = app => {
        app.UseMiddleware<RequestLoggingMiddleware>();
    };
    opts.ConfigureBeforeEndpointsCustomMiddleware = app => {
        app.UseMiddleware<TenantMiddleware>();
    };
});
```
