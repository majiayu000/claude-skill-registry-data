---
name: bff-setup
description: Configure affolterNET.Web.Bff service registration and middleware pipeline. Use when setting up AddBffServices, ConfigureBffApp, or configuring the BFF middleware order.
---

# BFF Setup

Configure the affolterNET.Web.Bff service registration and middleware pipeline.

For complete reference, see [Library Guide](../../LIBRARY_GUIDE.md).

## Quick Start

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Step 1: Register services
var options = builder.Services.AddBffServices(
    builder.Environment.IsDevelopment(),
    builder.Configuration,
    opts => {
        opts.EnableSecurityHeaders = true;
        opts.ConfigureBff = bff => {
            bff.AuthMode = AuthenticationMode.Authorize;
            bff.EnableSessionManagement = true;
        };
    });

var app = builder.Build();

// Step 2: Configure middleware
app.ConfigureBffApp(options);

app.Run();
```

## Configuration Options

### BffAppOptions

| Property | Type | Description |
|----------|------|-------------|
| `EnableSecurityHeaders` | bool | Enable security headers middleware |
| `ConfigureBff` | Action<BffOptions> | Configure BFF-specific options |
| `ConfigureAfterRoutingCustomMiddleware` | Action<IApplicationBuilder> | Add custom middleware after routing |
| `ConfigureBeforeEndpointsCustomMiddleware` | Action<IApplicationBuilder> | Add custom middleware before endpoints |

### BffOptions

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `AuthMode` | AuthenticationMode | `None` | Authentication mode |
| `EnableSessionManagement` | bool | `false` | Enable session management |

## Middleware Pipeline

The `ConfigureBffApp` configures middleware in this order:

1. Exception Handling
2. Security Headers Middleware
3. HTTPS Redirection
4. Static Files
5. Swagger/OpenAPI
6. Routing
7. Custom Middleware (after routing hook)
8. CORS
9. Antiforgery (CSRF protection)
10. Authentication & Authorization
11. Token Refresh Middleware
12. RPT Middleware
13. NoUnauthorizedRedirect Middleware (API routes)
14. Antiforgery Token Middleware
15. Custom Middleware (before endpoints hook)
16. API 404 Handling
17. Endpoint Mapping (Razor Pages, Controllers, YARP, Fallback)

## Common Patterns

### Development vs Production

```csharp
var options = builder.Services.AddBffServices(
    builder.Environment.IsDevelopment(),  // isDev flag
    builder.Configuration,
    opts => {
        // Development-specific config happens automatically
    });
```

### Adding Custom Middleware

```csharp
var options = builder.Services.AddBffServices(isDev, config, opts => {
    opts.ConfigureAfterRoutingCustomMiddleware = app => {
        app.UseMiddleware<TenantMiddleware>();
    };
    opts.ConfigureBeforeEndpointsCustomMiddleware = app => {
        app.UseMiddleware<AuditMiddleware>();
    };
});
```

### With Session Management

```csharp
var options = builder.Services.AddBffServices(isDev, config, opts => {
    opts.ConfigureBff = bff => {
        bff.EnableSessionManagement = true;
    };
});
```
