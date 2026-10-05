---
name: umbrella-dotnet-audit-server-bootstrap
description: 'Read-only audit of an ASP.NET Core server app''s Program.cs and startup extensions against Umbrella bootstrap conventions: claims principal propagation, MVC/API behavior, authorization, service wiring, Dynamic Image catalogs and mappings, and middleware ordering. Reports deviations with their runtime consequences and recommended fixes.'
---

# Audit Server Bootstrap

## Purpose

Inspect an ASP.NET Core server application's `Program.cs` (or `Startup`) and the extension methods it calls, and report where the bootstrap deviates from Umbrella conventions. Each deviation is reported with its **observable runtime consequence** — several produce subtle wrong-status-code behaviour rather than crashes. This skill is read-only: report and recommend; do not modify files.

Run this before generating controller integration tests (the response-code contract depends on several of these facts), when onboarding an existing app to Umbrella conventions, or after copying a `Program.cs` from another project.

## Checks

Work through the checklist. For each item record: present / absent / present-but-deviating, the evidence (file:line), and the consequence.

### 1. Claims principal propagation

Look for `UseUmbrellaPropagateClaimsPrincipal()` (or an equivalent middleware assigning `Thread.CurrentPrincipal = context.User`).

- **Must be registered after `UseAuthentication()`** so `HttpContext.User` is populated when it runs.
- **Consequence if missing**: `UmbrellaRepositoryCoreDataService` and any other code reading `ClaimsPrincipal.Current` throws — imperative resource authorization checks surface as `500` instead of `403`/success. This is a production defect, not just a test-environment issue.

### 2. Umbrella MVC/API behavior options

Look for `ConfigureUmbrellaMvcBuilderOptions(...)` on the MVC builder, or its parts: `ConfigureUmbrellaApiBehaviorOptions(...)`, `ConfigureUmbrellaMvcOptions()` (Umbrella model binders), `ConfigureUmbrellaJsonOptions(...)`, `ConfigureUmbrellaOpenApiConventions()`.

- Record which of the **three validation states** the app is in: behavior options with default (`422`), explicit `validationFailureStatusCode` argument, or not registered (plain ASP.NET `400`s with `ValidationProblemDetails` bodies and no malformed-JSON-root distinction). This is the same determination `umbrella-dotnet-audit-api-controller-response-contract` performs — cross-reference results if both run.
- Hand-rolled equivalents (e.g. `AddMvcOptions(o => o.InsertUmbrellaModelBinders())` + manual `AddJsonOptions`) are functional deviations: note which Umbrella parts they replicate and which they miss (most commonly the API behavior options).
- **Consequence if the behavior options are missing**: the app's validation contract differs from every conforming app, and generated tests/clients expecting `422` + `UmbrellaValidationProblemDetails` fail.
- Note: Pattern 1 generic controllers additionally require the Umbrella model binders (`SortExpression`/`FilterExpression` query binding) — flag if `SearchSlim` endpoints exist without them.

### 3. Authorization registration

- `AddCorePolicies()` (framework CRUD policies used by the imperative checks) plus the app's shared policies extension (e.g. `AddSharedPolicies()` / `AddSecurityPolicies()`), with policy name constants in a shared policy-names class.
- Resource `IAuthorizationHandler` registrations for every entity whose controllers/controller services leave `AuthorizationXxxChecksEnabled` at the default `true`.
- **Consequence of a missing policy**: `IAuthorizationService.AuthorizeAsync` throws for unknown policy names → `500`. **Consequence of a missing handler**: policies with no handler never succeed → blanket `403`s.

### 4. Umbrella service wiring

Confirm the presence and pairing of the core registrations the app's feature set requires:

- `AddUmbrellaAspNetCoreWebUtilities(...)` (also provides `IRazorViewToStringRenderer` for email senders);
- `AddUmbrellaUtilities(...)` using its current signature. Flag a removed `hybridCacheOptionsBuilder` named argument as a compile-time migration defect. On .NET 9 or later, this call supplies the baseline Microsoft `HybridCache` registration; do not recommend a second `AddHybridCache()` call merely to activate caching. If the application intentionally customizes cache options, preserve that behavior through Microsoft's `AddHybridCache(options => ...)`. Below .NET 9, verify a concrete `IDistributedCache` registration. Base this advice on the consuming project's actual target frameworks, not Umbrella's multi-targeted source projects;
- `AddUmbrellaDataAccess...` + the EF Core provider registration (`...EntityFrameworkCore(SqlServer)` etc.) where repositories exist;
- the Mapperly mapping registration (`AddUmbrellaUtilitiesMappingMapperly...`) where mappers exist;
- file storage provider registration (e.g. Azure Blob) where file handlers exist, plus `UseUmbrellaFileAccessTokenQueryString()` when secured file access uses access tokens;
- options bound with validate-on-start for required configuration sections.

Flag registrations whose dependencies are only partially wired (e.g. file handlers registered but no storage provider).

### 5. Dynamic Image integration

When Dynamic Image is present, read `.agents\skills\umbrella-dotnet-configure-dynamic-image\references\dynamic-image-contract.md` and verify:

- the analyzer is installed directly in every participating source project and the generator is Server-only;
- cross-project fingerprint activation, named external Razor roots, generated catalog registration, and validation agree;
- every file-provider mapping has an intentional `Public`, `Private`, or `NoStore` policy and long max-age is paired with fingerprinting;
- `UseUmbrellaDynamicImage` runs before terminal endpoint/fallback handling.

Report missing catalog ownership or unsafe cacheability as runtime/security defects, not style observations.

### 6. Middleware pipeline order

Verify the relative order: routing → authentication → authorization → `UseUmbrellaPropagateClaimsPrincipal` → endpoints. Note any Umbrella middleware in use (`UseUmbrellaApiException`, `UseUmbrellaFileAccessTokenQueryString`, multi-tenant session context) and whether its position is sensible relative to auth and endpoints.

### 7. Environment-sensitive behaviour

Record how the app branches on `IsDevelopment()` during startup (developer exception page, production-only services, seeding). The base controllers' exception filters only produce contractual `500` responses outside `Development` — note what a non-`Development` test host must provide to boot (cross-reference `umbrella-dotnet-audit-aspnetcore-integration-test-readiness`).

## Output

Return a bootstrap conformance report:

| # | Check | Status | Evidence | Consequence | Recommended fix |
| --- | --- | --- | --- | --- | --- |

Order findings by severity: production-defect class first (missing claims propagation, missing policies/handlers), contract deviations second (validation status state, model binders), advisory items last (middleware ordering nits, options binding style). For each fix, name the exact call to add and where. Do not modify files in this skill.
