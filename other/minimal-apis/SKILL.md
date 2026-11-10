---
name: minimal-apis
description: Builds, reviews and fixes ASP.NET Core minimal APIs on .NET 10 (current LTS, checked on 10.0.14). Covers built-in request validation (AddValidation, DataAnnotations on records and parameters, nested paths, PascalCase error keys, IValidatableObject order, and the per-assembly source generator that silently skips endpoints in class libraries), TypedResults and Results<T1,T2> unions, problem details and exception handling that never leak internals, deny-by-default authorization with a fallback policy, the .NET 10 cookie change that returns 401/403 only for endpoints it sees as APIs, antiforgery for forms, and WebApplicationFactory tests with xunit v3 on Microsoft.Testing.Platform. Use when code calls MapGet/MapPost/MapGroup, when adding validation, error handling or auth to a .NET 8-10 web API, when an API answers 302 instead of 401, when DataAnnotations seem ignored, or when dotnet test fails on the .NET 10 SDK.
license: MIT
---

# ASP.NET Core minimal APIs on .NET 10

.NET 10 is the current LTS (10.0.14, SDK 10.0.403, November 2026); .NET 11 is at RC and not GA.
Most minimal API examples on the web, and in model training data, are .NET 6 to 8. Several .NET 8
habits still compile on .NET 10 and quietly do something else. Everything marked *measured* below
was run on 10.0.14 in `mcr.microsoft.com/dotnet/sdk:10.0.403`.

## 1. Know what you are on

```sh
dotnet --version                       # SDK; global.json may pin it
grep -h "<TargetFramework" -r --include=*.csproj --include=*.props .
```

| You see | It means |
| --- | --- |
| `net10.0` | Built-in validation, cookie 401/403 for API endpoints, `TypedResults.ServerSentEvents`, OpenAPI 3.1 by default. |
| `net9.0` | No built-in validation. `ExceptionHandlerOptions.StatusCodeSelector` and built-in OpenAPI exist. |
| `net8.0` | No built-in validation. `IExceptionHandler`, antiforgery for form binding, `[AllowedValues]`/`[Length]`. |
| `Microsoft.NET.Sdk.Web` | Web project. A plain `Microsoft.NET.Sdk` library needs `<FrameworkReference Include="Microsoft.AspNetCore.App" />` to map endpoints. |

Don't add NuGet packages for things the framework now does (FluentValidation or MiniValidation just
for request validation, a problem-details library). Follow the repo if it already uses one.

## 2. Request validation (.NET 10)

```csharp
builder.Services.AddValidation();      // without this, DataAnnotations on minimal API parameters do nothing

public record CreateEventRequest(
    [Required, MaxLength(120)] string? Title,
    [Required] Venue? Venue,
    [Required, Length(1, 10)] List<TicketTier>? Tiers,
    SaleWindow? Sales);

public record TicketTier([Required] string? Name, [Range(0, 1_000_000)] int PriceCents);

public record SaleWindow([Required] DateTimeOffset? Opens, [Required] DateTimeOffset? Closes) : IValidatableObject
{
    public IEnumerable<ValidationResult> Validate(ValidationContext context)
    {
        if (Closes <= Opens) yield return new("Sales must close after they open.", [nameof(Closes)]);
    }
}

app.MapPost("/api/events", (CreateEventRequest request, EventStore store) => { /* only valid requests get here */ });
app.MapGet("/api/events", ([Range(1, 50)] int limit = 10) => /* ... */);
```

What it does (measured):

- Validates query, header and body parameters before the handler runs, recursing into
  nested objects and collection items. Attributes on **positional record parameters** work.
- A failure is a 400 `application/problem+json` `HttpValidationProblemDetails`, all errors at once:
  `{"title":"One or more validation errors occurred.","status":400,"errors":{"Venue.Capacity":[...],"Tiers[1].PriceCents":[...]}}`.
- **Keys are C# member paths in PascalCase** (`Tiers[1].PriceCents`), or the parameter name for a
  top-level parameter (`limit`). They ignore the JSON naming policy and `[JsonPropertyName]`, so a
  camelCase body produces PascalCase keys. If clients need JSON names, say so in the contract, match
  case-insensitively, or rewrite the keys in `AddProblemDetails(o => o.CustomizeProblemDetails = ...)`,
  which also runs for validation responses.
- Order inside an object: property attributes, then type-level attributes, then
  `IValidatableObject.Validate`. Any property error **skips** `Validate`, so a cross-field error
  only appears once the fields themselves are valid.
- `.DisableValidation()` turns it off for one endpoint. Unknown JSON properties are not rejected;
  set `JsonSerializerOptions.UnmappedMemberHandling = Disallow` if you need that.

### The trap: the generator only sees its own assembly

`AddValidation()` is backed by a source generator that emits metadata for the endpoints and types in
**the assembly that calls it**. Endpoints mapped from a class library (a feature module with its own
`MapVenuesModule()`) are **not validated** when only the host calls `AddValidation()`, with no
error, warning or log (measured). Fix it in the library:

```csharp
// Ticketing.Venues (class library with <FrameworkReference Include="Microsoft.AspNetCore.App" />)
public static IServiceCollection AddVenuesModule(this IServiceCollection services)
{
    services.AddValidation();          // generator runs for this assembly's endpoints and types
    services.AddSingleton<VenueDirectory>();
    return services;
}
```

- Keep the host's own `AddValidation()` too: the registrations compose, and removing the host call
  stops validation of the host's endpoints (measured).
- `[ValidatableType]` on the library type does not help while the library never calls
  `AddValidation()` (measured); it is also experimental in .NET 10 (`ASP0029`).
- Attributes directly on simple handler parameters (`[Range] int seats`) are still checked in
  that case; complex types are what silently go unvalidated. Always prove it with a test that posts
  an invalid body to the module's endpoint.
- A library without the ASP.NET Core framework reference needs the `Microsoft.Extensions.Validation`
  package for the generator (docs).

### DataAnnotations gotchas

- `[Required] int Quantity` never fails: a missing JSON number binds to 0. Use `[Range(1, ...)]`, or
  `int?` with `[Required]`.
- .NET 10 known issue: attributes on a *nullable value-type handler parameter*
  (`[Range(1, 50)] int? limit`) are not checked when the value is null (dotnet/aspnetcore#67033).
- `Validator.TryValidateObject` is not a substitute. It reads property attributes only, so it
  ignores attributes on positional record parameters, and it never recurses into nested objects or
  lists (measured: every rule on a record request silently passed).
- `[EmailAddress]` only checks for one `@` that is neither first nor last. `[Phone]` is loose too.
  `[RegularExpression]` must match the whole value.
- `[AllowedValues("a", "b")]`, `[DeniedValues]` and `[Length(min, max)]` (strings and collections)
  exist since .NET 8; `[MaxLength]`/`[MinLength]` also count collection items.

On .NET 8 or 9 there is no built-in validation: validate in the handler or an endpoint filter and
return `TypedResults.ValidationProblem(errors)`, walking nested objects yourself. Details and the
error-key rewrite: [references/validation.md](references/validation.md).

## 3. Results: return types are API surface

- Prefer `TypedResults` over `Results`. `TypedResults.Ok(x)` is `Ok<T>`; `Results.Ok(x)` is an opaque
  `IResult`. Typed results feed OpenAPI and, on .NET 10, mark the endpoint as an API for cookie auth
  (section 5).
- Branching handlers declare a union: `Results<Ok<Ticket>, NotFound, Conflict<ProblemDetails>> (...) =>`.
  A lambda whose branches return different typed results needs that explicit return type.
- `TypedResults.ValidationProblem(dict)` and `TypedResults.Problem(...)` write problem details.
- Don't return bare strings from JSON APIs: they are `text/plain` and are not treated as API
  endpoints.

## 4. Errors: problem details, never internals

```csharp
builder.Services.AddProblemDetails();           // IProblemDetailsService: RFC 9457 bodies with traceId
builder.Services.AddExceptionHandler<DomainExceptionHandler>();  // optional: map known exceptions
var app = builder.Build();
app.UseExceptionHandler();                      // 500 problem details, no exception text
app.UseStatusCodePages();                       // bodies for empty 4xx/5xx responses (401, 403, 404)
```

- `UseExceptionHandler()` without `AddProblemDetails()` (or a handler path) throws at startup
  (measured).
- With `UseExceptionHandler()`, an unexpected exception gives a generic 500 in every environment.
  Without it, the Development environment's developer exception page returns the exception message
  and stack trace as problem details (measured). Never run production as Development.
- Map expected failures explicitly: an `IExceptionHandler` that returns `true` after writing a
  problem (`IProblemDetailsService.TryWriteAsync`), or `StatusCodeSelector` (.NET 9+) for status
  only. Only put `ex.Message` in `detail` for exceptions you wrote for clients.
- .NET 10 no longer logs exceptions that an `IExceptionHandler` handled; use
  `ExceptionHandlerOptions.SuppressDiagnosticsCallback` if you want those logs.

More in [references/errors-and-results.md](references/errors-and-results.md).

## 5. Authorization and cookies

**Deny by default.** An endpoint without authorization metadata is anonymous unless a fallback
policy exists:

```csharp
builder.Services.AddAuthorizationBuilder()
    .AddPolicy("finance", p => p.RequireRole("finance"))
    .SetFallbackPolicy(new AuthorizationPolicyBuilder().RequireAuthenticatedUser().Build());

app.MapGet("/healthz", () => TypedResults.Ok()).AllowAnonymous();
payouts.MapPost("/{id}/approve", ApprovePayout).RequireAuthorization("finance");
```

`FallbackPolicy` applies to endpoints with no `[Authorize]`/`RequireAuthorization`/`AllowAnonymous`;
`DefaultPolicy` is what a bare `RequireAuthorization()` means. Group-level `RequireAuthorization()`
protects only that group, not endpoints mapped elsewhere later.

**Cookie authentication on .NET 10** answers 401/403 instead of redirecting only for endpoints
carrying `IDisableCookieRedirectMetadata`. Measured on 10.0.14 with a signed-out request:

| Handler returns | Response |
| --- | --- |
| `TypedResults.Ok/Created/NoContent/NotFound`, `Results<...>`, a POCO, or reads a JSON body | 401 |
| `Results.Ok(...)`, `Results.NoContent()` and other `IResult` | **302 to the login page** |
| `string`, `TypedResults.Text(...)`, `TypedResults.Content(...)` | **302 to the login page** |

So "it's .NET 10, APIs get 401 now" is wrong for half a typical codebase. Make it explicit for the
whole API surface, and keep redirects for HTML pages:

```csharp
var api = app.MapGroup("/api").DisableCookieRedirect();          // .NET 10: 401/403 for everything under it
// or, independent of how endpoints are mapped:
options.Events.OnRedirectToLogin = ctx => RejectOrRedirect(ctx, StatusCodes.Status401Unauthorized);
options.Events.OnRedirectToAccessDenied = ctx => RejectOrRedirect(ctx, StatusCodes.Status403Forbidden);

static Task RejectOrRedirect(RedirectContext<CookieAuthenticationOptions> ctx, int status)
{
    if (ctx.Request.Path.StartsWithSegments("/api")) ctx.Response.StatusCode = status;
    else ctx.Response.Redirect(ctx.RedirectUri);
    return Task.CompletedTask;
}
```

- The 401/403 body is empty unless `UseStatusCodePages()` (with `AddProblemDetails()`) runs before
  authentication, or you write a problem yourself.
- `.AllowCookieRedirect()` or `[AllowCookieRedirect]` opts an endpoint back into redirects.
- Requests with `X-Requested-With: XMLHttpRequest` always got 401/403; `fetch()` doesn't send it.

**Forms.** An endpoint that binds `[FromForm]`, `IFormFile` or `IFormCollection` requires
`AddAntiforgery()` *and* `app.UseAntiforgery()` (after authentication and authorization); without
the middleware it fails with a 500 `InvalidOperationException` (measured). Don't `DisableAntiforgery()`
on cookie-authenticated forms. Details: [references/auth.md](references/auth.md).

## 6. Test it through HTTP

```csharp
public sealed class ApiFactory : WebApplicationFactory<Program>
{
    protected override void ConfigureWebHost(IWebHostBuilder b) => b.UseEnvironment("Production");
}
var client = factory.CreateClient(new() { AllowAutoRedirect = false });   // see 302s as 302s
```

- On .NET 10 the top-level `Program` class is public; `public partial class Program;` is only
  needed for older target frameworks.
- xunit.v3 4.x runs on Microsoft.Testing.Platform v2, which the .NET 10 SDK's `dotnet test` only
  drives in MTP mode: add `"test": { "runner": "Microsoft.Testing.Platform" }` to `global.json`, or
  `dotnet test` fails with "Testing with VSTest target is no longer supported" (measured). Then run
  `dotnet test --project tests/Foo.Tests`.
- Assert status, `Content-Type` (`application/problem+json`) and the `errors` keys, and test the
  module endpoints too, not only the host's. See [references/testing.md](references/testing.md).

## Review checklist

- [ ] `AddValidation()` is called in **every assembly** that maps endpoints or declares request
      types; a test posts an invalid body to each module.
- [ ] Rules are attributes on the bound records/parameters, nested types included; no `[Required]`
      on non-nullable value types; cross-field rules in `IValidatableObject`.
- [ ] Error keys match what clients expect (PascalCase member paths by default).
- [ ] `AddProblemDetails` + `UseExceptionHandler` + `UseStatusCodePages`; no exception text for
      unexpected errors; expected errors mapped to 4xx problems.
- [ ] A fallback policy requires an authenticated user; public endpoints say `AllowAnonymous`.
- [ ] Cookie-authenticated APIs return 401/403 for every endpoint (`DisableCookieRedirect` on the
      API group or path-based events), and pages still redirect.
- [ ] Handlers return `TypedResults` (unions when branching), not bare strings or `Results.*`.
- [ ] Form endpoints have antiforgery middleware.
- [ ] No new packages for features the framework has.

## More

- [references/validation.md](references/validation.md): rules, keys, multi-assembly setup, .NET 8/9 fallback.
- [references/errors-and-results.md](references/errors-and-results.md): problem details, exception handlers, typed results.
- [references/auth.md](references/auth.md): fallback policies, cookie redirects, JWT, antiforgery.
- [references/testing.md](references/testing.md): WebApplicationFactory, xunit v3 on MTP, offline restore.
- [references/sources.md](references/sources.md): documentation and experiments behind every claim.
