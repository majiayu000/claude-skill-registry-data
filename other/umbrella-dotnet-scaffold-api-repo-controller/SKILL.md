---
name: umbrella-dotnet-scaffold-api-repo-controller
description: 'Scaffold an ASP.NET Core API controller that inherits GenericRepositoryApiController, communicating directly with a repository. Supports selective endpoint disabling via NoOp types and object placeholders.'
---

# Scaffold API Repository Controller

## Purpose

Add an ASP.NET Core API controller to `Web\<AppName>.Web.Server\Controllers\Api\` that communicates directly with a repository via `GenericRepositoryApiController`. All CRUD hooks (`AfterCreateEntityAsync`, etc.) live on the controller itself.

This pattern does not have a separate service abstraction and does not support Blazor SSR pre-rendering. For features that need pre-rendering support, use `umbrella-dotnet-scaffold-api-data-service-controller` instead.

## Discovery (read these before writing anything)

1. Read 2–3 existing controllers in `Web\<AppName>.Web.Server\Controllers\Api\` to confirm the project-specific base class name (e.g. `IndyRecordsGenericRepositoryApiController`) and its generic type parameter count (typically 11).
2. Note any NoOp/`object` usage in existing controllers — these indicate which endpoint-disabling patterns are already established in the project.
3. Read `Web\<AppName>.Web.Shared\Security\Policies\<AppName>PolicyNames.cs` and comparable feature controllers. Select the narrowest existing policy that represents the feature's real access boundary; if more than one policy is plausible and the choice changes who can call the API, stop and ask rather than guessing.

---

## Step 1 -- Create the controller

**File:** `Web\<AppName>.Web.Server\Controllers\Api\Manage<Name>Controller.cs`

### Full CRUD controller

```csharp
using Microsoft.AspNetCore.Authorization;
using <AppName>.Core.Data.Repositories.Abstractions;
using <AppName>.Core.Domain.Entities;
using <AppName>.Web.Server.Infrastructure.Mvc;
using <AppName>.Web.Shared.Models.Api.Manage<Name>;
using <AppName>.Web.Shared.Security.Policies;
using Umbrella.DataAccess.Abstractions;
using Umbrella.Utilities.Data.Pagination;
using Umbrella.Utilities.Mapping.Abstractions;

namespace <AppName>.Web.Server.Controllers.Api;

[Authorize(<AppName>PolicyNames.<Policy>)]
public class Manage<Name>Controller : <AppName>GenericRepositoryApiController<
    SlimManage<Name>Model,
    PaginatedResultModel<SlimManage<Name>Model>,
    Manage<Name>Model,
    CreateManage<Name>Model,
    CreateManage<Name>ResultModel,
    UpdateManage<Name>Model,
    UpdateManage<Name>ResultModel,
    I<Name>Repository,
    <Name>,
    RepoOptions,
    int>
{
    public Manage<Name>Controller(
        ILogger<Manage<Name>Controller> logger,
        IWebHostEnvironment hostingEnvironment,
        IUmbrellaMapper mapper,
        Lazy<I<Name>Repository> repository,
        IUmbrellaRepositoryCoreDataService coreDataService)
        : base(logger, hostingEnvironment, mapper, repository, coreDataService)
    {
    }

    protected override bool AuthorizationSlimReadChecksEnabled => false;
    protected override bool AuthorizationCreateChecksEnabled => false;
    protected override bool AuthorizationReadChecksEnabled => false;
    protected override bool AuthorizationUpdateChecksEnabled => false;
    protected override bool AuthorizationDeleteChecksEnabled => false;
}
```

**Rules:**
- No DI registration step — controllers are auto-discovered by ASP.NET Core.
- Extra dependencies (e.g. `I<Name>FileHandler`) go after the 5 base constructor params and are stored as `private readonly` fields.
- `AfterCreateEntityAsync`, `AfterUpdateEntityAsync`, and `AfterDeleteEntityAsync` are added only when the feature's persistence semantics require them. File replacement/deletion hooks are destructive behavior: confirm the feature's optional/required filename rules and authorization boundary before adding them. Always start with `cancellationToken.ThrowIfCancellationRequested()` and `Guard.IsNotNull(...)` on each parameter.
- The base controller enables resource authorization checks by default. The full-CRUD template explicitly suppresses all five checks because it assumes the declarative controller policy is sufficient. Omit only the specific suppression overrides backed by registered resource authorization handlers; never describe the base defaults as `false`.
- Generic type params in order (11 total): `TSlimModel`, `TPaginatedResultModel`, `TModel`, `TCreateModel`, `TCreateResultModel`, `TUpdateModel`, `TUpdateResultModel`, `TRepository`, `TEntity`, `TRepositoryOptions`, `TEntityKey`.

### Lifecycle hook example (file handling)

```csharp
protected override async Task AfterCreateEntityAsync(<Name> entity, CreateManage<Name>Model model, CreateManage<Name>ResultModel result, CancellationToken cancellationToken)
{
    cancellationToken.ThrowIfCancellationRequested();
    Guard.IsNotNull(entity);
    Guard.IsNotNull(model);
    Guard.IsNotNull(result);

    _ = await _fileHandler.CreateByGroupIdAndTempFileNameAsync(entity.Id, model.ImageProviderFileName, null, cancellationToken);
    UmbrellaVersionedUrl image = await _fileHandler
        .GetVersionedWebFilePathAsync(entity.Id, model.ImageProviderFileName, cancellationToken)
        ?? throw new InvalidOperationException("The saved image could not be resolved.");

    result.ImageUrl = image.Url;
    result.ImageVersionToken = image.VersionToken;
}
```

When Dynamic Image fingerprinting is enabled, the result model declares the matching nullable `ImageVersionToken`; always populate URL/token pairs together.

---

## Selective endpoint disabling (NoOp / object patterns)

When not all CRUD operations are needed, use NoOp types and `object` to disable specific endpoints. `TSlimModel`/`TPaginatedResultModel` are always paired, as are `TUpdateModel`/`TUpdateResultModel`.

| Goal | Replace | With |
|---|---|---|
| Disable SearchSlim (list) | T1 `TSlimModel`, T2 `TPaginatedResultModel` | `object`, `PaginatedResultModel<object>` |
| Disable Get detail | T3 `TModel` | `object` |
| Disable Create (POST) | T4 `TCreateModel`, T5 `TCreateResultModel` | `object`, `NoopCreateResultModel<int>` |
| Disable Update (PUT) | T6 `TUpdateModel`, T7 `TUpdateResultModel` | `NoopUpdateModel<int>`, `NoopUpdateResultModel` |

All `Noop*` types are defined in Umbrella — no extra imports are needed.

When using `object` to disable an endpoint, also add the corresponding `XxxEndpointEnabled` override. Check the existing codebase for the exact property name used — common examples:

```csharp
protected override bool SlimReadEndpointEnabled => false;
protected override bool ReadEndpointEnabled => false;
protected override bool CreateEndpointEnabled => false;
protected override bool UpdateEndpointEnabled => false;
```

### Example: Create-only (analytics / session recording)

```csharp
[Authorize(<AppName>PolicyNames.<Policy>)]
public class <Name>Controller : <AppName>GenericRepositoryApiController<
    object,
    PaginatedResultModel<object>,
    object,
    Create<Name>Model,
    Create<Name>ResultModel,
    NoopUpdateModel<int>,
    NoopUpdateResultModel,
    I<Name>Repository,
    <Name>,
    RepoOptions,
    int>
{
    public <Name>Controller(
        ILogger<<Name>Controller> logger,
        IWebHostEnvironment hostingEnvironment,
        IUmbrellaMapper mapper,
        Lazy<I<Name>Repository> repository,
        IUmbrellaRepositoryCoreDataService coreDataService)
        : base(logger, hostingEnvironment, mapper, repository, coreDataService)
    {
    }

    protected override bool SlimReadEndpointEnabled => false;
    protected override bool ReadEndpointEnabled => false;
    protected override bool UpdateEndpointEnabled => false;
}
```

### Example: Read list + detail + create, no update

```csharp
[Authorize(<AppName>PolicyNames.<Policy>)]
public class <Name>Controller : <AppName>GenericRepositoryApiController<
    SlimManage<Name>Model,
    PaginatedResultModel<SlimManage<Name>Model>,
    Manage<Name>Model,
    CreateManage<Name>Model,
    CreateManage<Name>ResultModel,
    NoopUpdateModel<int>,
    NoopUpdateResultModel,
    I<Name>Repository,
    <Name>,
    RepoOptions,
    int>
{
    // ...
    protected override bool UpdateEndpointEnabled => false;
}
```

---

## Customising CRUD behaviour — use lifecycle hooks, not endpoint overrides

To run logic before or after a standard CRUD operation, override a lifecycle hook (`BeforeCreateEntityAsync`, `AfterCreateEntityAsync`, `BeforeUpdateEntityAsync`, `AfterUpdateEntityAsync`, `BeforeDeleteEntityAsync`, `AfterDeleteEntityAsync`) — never override `PostAsync`, `GetAsync`, `PutAsync`, `DeleteAsync`, `PatchAsync`, or `SearchSlimAsync` directly.

Overriding a CRUD method without calling `base.XxxAsync()` silently skips all base-class cross-cutting concerns: authorization checks, error handling, concurrency stamp validation, and any future hooks added to the base class.

**If you must override a CRUD method** (e.g. to enrich the incoming model before delegation), always call `await base.XxxAsync(...)` within the override body — UA019 enforces this.

**To disable an endpoint entirely:** use the NoOp/object pattern with `XxxEndpointEnabled => false` (documented above) — not a `[NonAction]` throw override, which leaves the route registered while lying about availability.

---

## Custom action methods

When the feature requires endpoints beyond standard CRUD, add them to the controller. Follow these conventions.

**Attribute:** Use `[UmbrellaProducesResponseType(StatusCodes.StatusXxx)]` (NOT the standard `[ProducesResponseType]`). Umbrella's attribute automatically maps status codes to `UmbrellaProblemDetails` or `UmbrellaValidationProblemDetails` with the correct `application/problem+json` content type.

**Status codes to declare per verb** (401, 403, 500 are already covered at class level):

| HTTP verb | Declare on the custom method |
|---|---|
| `[HttpGet]` | 200, 400, 404 (if not found is possible) |
| `[HttpPost]` | 201, 400, 409 (if conflict is possible), 422 |
| `[HttpPut]` | 200, 400, 404, 409 (conflict/concurrency), 422 |
| `[HttpPatch]` | 200, 400, 404, 409 (conflict/concurrency), 422 |
| `[HttpDelete]` | 204, 400, 404, 409 (conflict/concurrency) |

Note: 405 (Method Not Allowed) is returned by the base class for disabled endpoints — do not declare it on custom methods.

**Error helper methods** inherited from `UmbrellaApiController`:

```csharp
BadRequest(reason, code?)          // 400 — UmbrellaValidationProblemDetails
NotFound(reason, code?)            // 404 — UmbrellaProblemDetails
Conflict(reason, code?)            // 409 — UmbrellaProblemDetails
ConcurrencyConflict(reason)        // 409 — code: HttpProblemCodes.ConcurrencyStampMismatch
InternalServerError(reason, code?) // 500 — UmbrellaProblemDetails
OperationResult(IOperationResult)  // converts OperationResultStatus enum to the correct HTTP response
```

**Example: custom GET endpoint**

```csharp
[HttpGet("GetByExternalId")]
[UmbrellaProducesResponseType(StatusCodes.Status200OK)]
[UmbrellaProducesResponseType(StatusCodes.Status400BadRequest)]
[UmbrellaProducesResponseType(StatusCodes.Status404NotFound)]
public async Task<IActionResult> GetByExternalIdAsync([FromQuery] string externalId, CancellationToken cancellationToken = default)
{
    cancellationToken.ThrowIfCancellationRequested();

    var result = await _repository.Value.FindByExternalIdAsync(externalId, cancellationToken);

    return result is null ? NotFound("Not found.") : Ok(result);
}
```

**Note on `UmbrellaDataAccessApiController`:** For non-CRUD or singleton-entity controllers where you need full control over which endpoints are exposed (e.g. a settings controller that only exposes GET and PUT for a hardcoded record), inherit from `UmbrellaDataAccessApiController` directly rather than this generic controller. See `SystemSettingsController` for an example.

---

## Analyzer compatibility

Before finishing, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build the affected projects with their installed analyzers enabled. Treat diagnostics introduced by the generated or changed code as defects in this workflow.

## Verification

1. The controller inherits the project-specific `<AppName>GenericRepositoryApiController` base (not the Umbrella base directly).
2. All 11 generic type params are in the correct order.
3. The 5 base constructor params are passed to `: base(...)` in the correct order.
4. `object`/NoOp combinations are used consistently (T1+T2 paired, T6+T7 paired).
5. Every `object` position has a corresponding `XxxEndpointEnabled => false` override.
6. Lifecycle hook overrides (`AfterCreateEntityAsync`, etc.) start with `ThrowIfCancellationRequested` and `Guard.IsNotNull` on all non-cancellation params.
7. No standard CRUD method (`PostAsync`, `GetAsync`, `PutAsync`, `DeleteAsync`, `PatchAsync`, `SearchSlimAsync`) is overridden without a `base.XxxAsync(...)` call in its body.

---

## Next steps

After the controller builds and its routes are wired, generate integration tests for it with `umbrella-dotnet-generate-api-repo-controller-tests` (run `umbrella-dotnet-audit-api-controller-response-contract` first to derive the per-endpoint status contract).
