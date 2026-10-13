---
name: aspnet-minimal-api
description: ASP.NET Core Minimal API best practices for .NET 8. Use when building or reviewing Minimal API endpoints, route groups, IResult returns, Problem Details error handling, OpenAPI/Swagger setup, CancellationToken wiring, and endpoint extension method patterns. Covers SpaceOS.Kernel API layer conventions (kebab-case routes, plural nouns, Result<T> mapping, 201 Created with Location header).
---

This skill provides authoritative patterns for ASP.NET Core Minimal API in .NET 8 LTS. Apply these rules when writing or reviewing any file in the `SpaceOS.Kernel.Api` project.

## Core Principles

- **No controllers.** Minimal API only. `ControllerBase`, `[ApiController]`, `[Route]` attributes are forbidden.
- **`IResult` everywhere.** Every endpoint returns `IResult` — never a raw object or `void`.
- **Delegate to MediatR.** Endpoint lambdas contain zero business logic. One line: `mediator.Send(...)`.
- **`CancellationToken` end-to-end.** Every endpoint accepts `CancellationToken ct` and passes it to `mediator.Send()`.

---

## Route Conventions

```
/api/{resource}                          GET list, POST create
/api/{resource}/{id:guid}                GET by id, PUT update
/api/{parent}/{parentId:guid}/{child}    GET child list, POST create child
```

Rules:
- **kebab-case** — `flow-epics`, `work-stations`, `space-layers`
- **plural nouns** — `/api/tenants` not `/api/tenant`
- **`{id:guid}` constraint** — always typed, never raw `{id}`
- No verbs in URLs — `/api/flow-epics/{id}/delegate` is acceptable for FSM transitions

---

## Endpoint Extension Method Pattern

Every aggregate gets its own static class. `Program.cs` only calls `Map*Endpoints()`.

```csharp
// SpaceOS.Kernel.Api/Endpoints/TenantEndpoints.cs

/// <summary>Registers all Tenant endpoints.</summary>
public static class TenantEndpoints
{
    public static IEndpointRouteBuilder MapTenantEndpoints(
        this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/tenants")
            .WithTags("Tenants")
            .WithOpenApi();

        group.MapGet("/", GetAllAsync);
        group.MapGet("/{id:guid}", GetByIdAsync);
        group.MapPost("/", CreateAsync);
        group.MapPut("/{id:guid}", UpdateAsync);

        return app;
    }

    // Handlers as private static methods — keeps lambdas readable
    private static async Task<IResult> GetAllAsync(
        IMediator mediator, CancellationToken ct)
    {
        var result = await mediator
            .Send(new GetAllTenantsQuery(), ct)
            .ConfigureAwait(false);
        return result.ToApiResult();
    }

    private static async Task<IResult> GetByIdAsync(
        Guid id, IMediator mediator, CancellationToken ct)
    {
        var result = await mediator
            .Send(new GetTenantByIdQuery(id), ct)
            .ConfigureAwait(false);
        return result.ToApiResult();
    }

    private static async Task<IResult> CreateAsync(
        CreateTenantRequest request, IMediator mediator, CancellationToken ct)
    {
        var result = await mediator
            .Send(new CreateTenantCommand(request.Name), ct)
            .ConfigureAwait(false);
        return result.ToCreatedResult("GetTenantById", r => new { id = r.Id });
    }

    private static async Task<IResult> UpdateAsync(
        Guid id, UpdateTenantNameRequest request,
        IMediator mediator, CancellationToken ct)
    {
        var result = await mediator
            .Send(new UpdateTenantNameCommand(id, request.Name), ct)
            .ConfigureAwait(false);
        return result.ToApiResult();
    }
}
```

**Program.cs stays clean:**
```csharp
app.MapTenantEndpoints();
app.MapFacilityEndpoints();
app.MapWorkStationEndpoints();
app.MapSpaceLayerEndpoints();
app.MapFlowEpicEndpoints();
```

---

## Result<T> → IResult Mapping

Single shared extension — create once in `Api/Extensions/ResultExtensions.cs`:

```csharp
// SpaceOS.Kernel.Api/Extensions/ResultExtensions.cs

/// <summary>Maps Ardalis.Result to ASP.NET Core IResult (RFC 7807).</summary>
public static class ResultExtensions
{
    /// <summary>Maps a Result to 200 OK, 404, 422, or 500 Problem Details.</summary>
    public static IResult ToApiResult<T>(this Result<T> result) =>
        result.Status switch
        {
            ResultStatus.Ok       => Results.Ok(result.Value),
            ResultStatus.NotFound => Results.Problem(
                title: "Resource Not Found",
                detail: result.Errors.FirstOrDefault(),
                statusCode: 404,
                type: "https://httpstatuses.io/404"),
            ResultStatus.Invalid  => Results.ValidationProblem(
                result.ValidationErrors.ToDictionary(
                    e => e.Identifier,
                    e => new[] { e.ErrorMessage })),
            ResultStatus.Error    => Results.Problem(
                title: "An error occurred",
                detail: result.Errors.FirstOrDefault(),
                statusCode: 500,
                type: "https://httpstatuses.io/500"),
            _ => Results.Problem(statusCode: 500)
        };

    /// <summary>Maps a Result to 201 Created with Location header, or error response.</summary>
    public static IResult ToCreatedResult<T>(
        this Result<T> result,
        string routeName,
        Func<T, object> routeValues) =>
        result.Status switch
        {
            ResultStatus.Ok      => Results.CreatedAtRoute(
                routeName,
                routeValues(result.Value),
                result.Value),
            ResultStatus.Invalid => Results.ValidationProblem(
                result.ValidationErrors.ToDictionary(
                    e => e.Identifier,
                    e => new[] { e.ErrorMessage })),
            _ => Results.Problem(statusCode: 500)
        };

    /// <summary>Maps a non-generic Result to 204 No Content or error response.</summary>
    public static IResult ToApiResult(this Result result) =>
        result.Status switch
        {
            ResultStatus.Ok       => Results.NoContent(),
            ResultStatus.NotFound => Results.Problem(statusCode: 404,
                type: "https://httpstatuses.io/404"),
            ResultStatus.Invalid  => Results.ValidationProblem(
                result.ValidationErrors.ToDictionary(
                    e => e.Identifier,
                    e => new[] { e.ErrorMessage })),
            _ => Results.Problem(statusCode: 500)
        };
}
```

---

## HTTP Status Code Semantics

| Operation | Success | Validation fail | Not found | Server error |
|-----------|---------|-----------------|-----------|--------------|
| GET | `200 OK` | — | `404` Problem Details | `500` Problem Details |
| POST (create) | `201 Created` + `Location` | `422` ValidationProblem | — | `500` Problem Details |
| PUT (update) | `200 OK` | `422` ValidationProblem | `404` Problem Details | `500` Problem Details |
| FSM transition (PUT) | `200 OK` | `422` ValidationProblem | `404` Problem Details | `500` Problem Details |

**Never use `400 Bad Request` for validation.** FluentValidation failures → `422 Unprocessable Entity`.  
**`400 Bad Request` is reserved** for `DomainException` (business rule violations).

---

## Problem Details (RFC 7807)

Every non-2xx response must include:

```json
{
  "type": "https://httpstatuses.io/404",
  "title": "Resource Not Found",
  "status": 404,
  "detail": "Tenant with id '...' was not found.",
  "instance": "/api/tenants/00000000-0000-0000-0000-000000000000"
}
```

**Global exception middleware** catches unhandled exceptions:

```csharp
// SpaceOS.Kernel.Api/Middleware/ExceptionHandlingMiddleware.cs

/// <summary>Global handler — maps exceptions to RFC 7807 Problem Details.</summary>
internal sealed class ExceptionHandlingMiddleware(
    RequestDelegate next,
    ILogger<ExceptionHandlingMiddleware> logger)
{
    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await next(context).ConfigureAwait(false);
        }
        catch (DomainException ex)
        {
            logger.LogWarning(ex, "Domain rule violation on {Path}", context.Request.Path);
            context.Response.StatusCode = 400;
            context.Response.ContentType = "application/problem+json";
            await context.Response.WriteAsJsonAsync(new ProblemDetails
            {
                Type     = "https://httpstatuses.io/400",
                Title    = "Domain Rule Violation",
                Status   = 400,
                Detail   = ex.Message,
                Instance = context.Request.Path
            }).ConfigureAwait(false);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Unhandled exception on {Path}", context.Request.Path);
            context.Response.StatusCode = 500;
            context.Response.ContentType = "application/problem+json";
            await context.Response.WriteAsJsonAsync(new ProblemDetails
            {
                Type     = "https://httpstatuses.io/500",
                Title    = "Internal Server Error",
                Status   = 500,
                Detail   = "An unexpected error occurred.",
                Instance = context.Request.Path
            }).ConfigureAwait(false);
        }
    }
}
```

Register **before routing** in `Program.cs`:
```csharp
app.UseMiddleware<ExceptionHandlingMiddleware>();
app.UseRouting(); // after middleware
```

---

## OpenAPI / Swagger (.NET 8 — Swashbuckle v6)

.NET 8 uses Swashbuckle, not the built-in `AddOpenApi()` (that is .NET 9+).

```xml
<!-- SpaceOS.Kernel.Api.csproj -->
<PackageReference Include="Swashbuckle.AspNetCore" Version="6.*" />
```

```csharp
// Program.cs
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title       = "SpaceOS Kernel API",
        Version     = "v1",
        Description = "ConTech & PropTech Operating System"
    });
});

// ...

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "SpaceOS v1"));
}
```

Endpoint metadata for Swagger:
```csharp
group.MapGet("/{id:guid}", GetByIdAsync)
    .WithName("GetTenantById")           // used in CreatedAtRoute
    .WithSummary("Get tenant by ID")
    .Produces<TenantDto>(200)
    .ProducesProblem(404)
    .WithOpenApi();
```

---

## Request Records

Thin, no validation — FluentValidation in Application layer handles it:

```csharp
// SpaceOS.Kernel.Api/Endpoints/Requests/TenantRequests.cs

/// <summary>Request body for creating a Tenant.</summary>
public sealed record CreateTenantRequest(string Name);

/// <summary>Request body for renaming a Tenant.</summary>
public sealed record UpdateTenantNameRequest(string Name);
```

One file per aggregate: `TenantRequests.cs`, `FacilityRequests.cs`, etc.

---

## Program.cs Full Template (.NET 8)

```csharp
// SpaceOS.Kernel.Api/Program.cs

var builder = WebApplication.CreateBuilder(args);

// Infrastructure + Application DI
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);

// API services
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "SpaceOS Kernel API", Version = "v1"
    }));

var app = builder.Build();

// Middleware — order matters
app.UseMiddleware<ExceptionHandlingMiddleware>();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "SpaceOS v1"));
}

// Health check — unauthenticated
app.MapGet("/healthz", () => Results.Ok(new { status = "healthy" }))
    .WithTags("Health")
    .ExcludeFromDescription();

// Aggregate endpoints
app.MapTenantEndpoints();
app.MapFacilityEndpoints();
app.MapWorkStationEndpoints();
app.MapSpaceLayerEndpoints();
app.MapFlowEpicEndpoints();

app.Run();

// Required for WebApplicationFactory in integration tests
public partial class Program { }
```

---

## Integration Test Setup

```csharp
// SpaceOS.Kernel.IntegrationTests/Infrastructure/SpaceOsApiFactory.cs

/// <summary>Test factory with SQLite in-memory replacing PostgreSQL.</summary>
public sealed class SpaceOsApiFactory : WebApplicationFactory<Program>, IAsyncLifetime
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureTestServices(services =>
        {
            var descriptor = services.SingleOrDefault(
                d => d.ServiceType == typeof(DbContextOptions<AppDbContext>));
            if (descriptor is not null)
                services.Remove(descriptor);

            services.AddDbContext<AppDbContext>(o =>
                o.UseSqlite("DataSource=:memory:"));
        });
    }

    public async Task InitializeAsync()
    {
        using var scope = Services.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        await db.Database.EnsureCreatedAsync().ConfigureAwait(false);
    }

    public new Task DisposeAsync() => Task.CompletedTask;
}
```

`public partial class Program { }` in `Program.cs` is **required** — without it `WebApplicationFactory<Program>` cannot reference the entry point.

---

## Anti-Patterns — Never Generate These

```csharp
// ❌ Controller
[ApiController]
public class TenantsController : ControllerBase { }

// ❌ Raw object return (no IResult)
app.MapGet("/api/tenants/{id}", async (Guid id) => await repo.GetByIdAsync(id));

// ❌ Business logic in endpoint
app.MapPost("/api/tenants", async (CreateTenantRequest req) => {
    if (req.Name.Length > 100) return Results.BadRequest("Too long"); // belongs in VO
});

// ❌ Missing CancellationToken
app.MapGet("/api/tenants", async (IMediator mediator) =>
    await mediator.Send(new GetAllTenantsQuery())); // no ct

// ❌ 400 for validation failure
Results.BadRequest("Name is required"); // use Results.ValidationProblem → 422

// ❌ AddOpenApi() — this is .NET 9 only
builder.Services.AddOpenApi(); // use Swashbuckle on .NET 8
```
