---
name: umbrella-dotnet-scaffold-custom-api-controller
description: 'Scaffold a custom API controller on UmbrellaDataAccessApiController (custom-shaped CRUD composing the protected data-access helpers), UmbrellaDataServiceApiController (ExecuteOperationAsync over a controller service), or UmbrellaApiController (fully hand-rolled orchestration/Identity actions), following the Umbrella house conventions: status helper envelope, UmbrellaProducesResponseType declarations, concurrency handling, and authorization. Use when the endpoint shape does not fit the generic repository controllers.'
---

# Scaffold Custom API Controller

## Purpose

Add an API controller whose endpoint surface does not fit the two generic CRUD patterns. Covers the three endpoint-less Umbrella base controllers:

- **`UmbrellaDataAccessApiController`** (Variant A) — the entity is repository-backed but the endpoint shape is custom: a singleton resource (`GET` with no `id`), partial CRUD, shaped queries. Actions compose the protected `ReadAllAsync`/`ReadAsync`/`CreateAsync`/`UpdateAsync`/`DeleteAsync` helpers.
- **`UmbrellaApiController`** (Variant B) — no repository or data-service usage: orchestration over services, ASP.NET Identity flows, external integrations. Actions are fully hand-rolled using the status helper methods and/or `OperationResult` mapping.
- **`UmbrellaDataServiceApiController<TDataService>`** (Variant C) — the operations live on a controller service (a subset of `IGenericDataService`, an `UmbrellaRepositoryDataService`-derived service, or a fully custom interface returning `IOperationResult`s) but the endpoint shape is custom. Actions compose the protected `ExecuteOperationAsync` envelope.

## Pattern selection (decide first)

For raw-body temporary-file uploads, use `umbrella-dotnet-scaffold-file-upload-controller`
instead. Its specialized base owns the action and exposes upload hooks; the generic
intermediate-base and hand-written action rules below do not apply to that workflow.

1. Standard CRUD over one entity, standard endpoint shapes → **do not use this skill**: use `umbrella-dotnet-scaffold-api-repo-controller` (Pattern 1) or `umbrella-dotnet-scaffold-api-data-service-controller` (Pattern 2).
2. Repository-backed entity, non-standard endpoint shapes, no service abstraction needed → Variant A below.
3. Operations belong on a controller service (shared interface, SSR pre-rendering, or the logic-in-service convention) with a non-standard endpoint shape, and every delegated operation returns `IOperationResult` or `IOperationResult<T>` → Variant C below. A plain `Task<T>` method is not compatible with `ExecuteOperationAsync`; use Variant B or change the service contract deliberately.
4. Anything else (service orchestration without a data-service abstraction, Identity, external APIs, no entity) → Variant B below.

A single controller must not mix variants; if part of the surface is standard CRUD, prefer a generic controller plus a separate custom controller.

## Discovery (read these before writing anything)

1. Read the app-level intermediate base controllers in `Web\<AppName>.Web.Server\Infrastructure\Mvc\` (e.g. `IndyRecordsApiController : UmbrellaApiController`, `IndyRecordsDataAccessApiController : UmbrellaDataAccessApiController`). They typically carry `[Route("api/[controller]")]` (or a versioned route), the mapper, and shared error message constants. **Always derive from the intermediate base, never from the Umbrella base directly.** If no intermediate base exists for the chosen variant, create one first (Step 1).
2. Read 1–2 existing custom controllers for project-specific idioms.
3. Read `Web\<AppName>.Web.Shared\Security\Policies\<AppName>PolicyNames.cs` for auth policy constants.
4. Identify the repository interface and entity (DataAccess variant) or the services to orchestrate (ApiController variant).

## Step 1 -- Intermediate base (only if missing)

```csharp
using Microsoft.AspNetCore.Mvc;
using Umbrella.AspNetCore.WebUtilities.Mvc;
using Umbrella.DataAccess.Abstractions;
using Umbrella.Utilities.Mapping.Abstractions;

namespace IndyRecords.Web.Server.Infrastructure.Mvc;

[Route("api/[controller]")]
public abstract class IndyRecordsDataAccessApiController : UmbrellaDataAccessApiController
{
	protected const string ConcurrencyErrorMessage = "This item has been updated by another user. Please reload and try again.";

	protected IndyRecordsDataAccessApiController(
		ILogger logger,
		IWebHostEnvironment hostingEnvironment,
		IUmbrellaMapper mapper,
		IUmbrellaRepositoryCoreDataService dataAccessService)
		: base(logger, hostingEnvironment, mapper, dataAccessService)
	{
	}
}
```

The `UmbrellaApiController` intermediate base may impose additional constructor dependencies such as `IUmbrellaMapper` even when a particular action does not map. Preserve and pass every dependency required by the discovered app base; do not bypass it by deriving from Umbrella directly.

## Shared conventions (all variants)

- **Response type declarations**: use `[UmbrellaProducesResponseType(StatusCodes.StatusXxx)]` (never plain `[ProducesResponseType]`) on each action for its method-level codes. Verify whether 401/403/500 are already declared on the intermediate base; if not, put them on the concrete controller class. Do not duplicate them at action level. Per verb:

| Verb | Declare on the action |
|---|---|
| `[HttpGet]` | 200, 404 (when the lookup can miss), 422 (when input binds) |
| `[HttpPost]` | 201 (or 200/204 for commands), 400, 409 (when conflict is possible), 422 |
| `[HttpPut]` / `[HttpPatch]` | 200, 400, 404, 409 (concurrency), 422 |
| `[HttpDelete]` | 204, 404, 409 (when guarded), 422 (non-string keys) |

- **Status helpers** from `UmbrellaApiController`: `BadRequest(reason)`, `NotFound(reason)`, `Unauthorized(reason)`, `Forbidden(reason)`, `Conflict(reason)`, `ConcurrencyConflict(reason)`, `MethodNotAllowed(reason)`, `TooManyRequests(reason)`, `InternalServerError(reason)`, and `OperationResult(...)` / `OperationResult<T>(...)` for `IOperationResult` values returned by services.
- **Do not return statuses via `StatusCode(...)` or MVC's built-in helpers** — the Umbrella helpers produce the `UmbrellaProblemDetails`/`UmbrellaValidationProblemDetails` contract.
- **Route shape**: action-level routes via `[HttpGet("Xxx")]` etc.; the controller route comes from the intermediate base.
- **Authorization**: `[Authorize(<AppName>PolicyNames.<Policy>)]` at class level (or `[AllowAnonymous]` deliberately). Entity-level checks either flow through the data-access helpers (`enableAuthorizationChecks`) or, in hand-rolled actions, call `IAuthorizationService.AuthorizeAsync(User, resource, policy)` and return `Forbidden(...)` on failure.

## Variant A -- `UmbrellaDataAccessApiController`

Each action composes a protected helper with explicit generic arguments. Example — a singleton settings resource:

```csharp
using IndyRecords.Core.Data.Repositories.Abstractions;
using IndyRecords.Core.Domain.Entities;
using IndyRecords.Web.Server.Infrastructure.Mvc;
using IndyRecords.Web.Shared.Models.Api.SystemSettings;
using IndyRecords.Web.Shared.Security.Policies;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Umbrella.DataAccess.Abstractions;
using Umbrella.Utilities.Mapping.Abstractions;

namespace IndyRecords.Web.Server.Controllers.Api;

[Authorize(IndyRecordsPolicyNames.SystemSettingsManagement)]
public class SystemSettingsController : IndyRecordsDataAccessApiController
{
	private readonly Lazy<ISystemSettingsRepository> _repository;

	public SystemSettingsController(
		ILogger<SystemSettingsController> logger,
		IWebHostEnvironment hostingEnvironment,
		IUmbrellaMapper mapper,
		IUmbrellaRepositoryCoreDataService dataAccessService,
		Lazy<ISystemSettingsRepository> repository)
		: base(logger, hostingEnvironment, mapper, dataAccessService)
	{
		_repository = repository;
	}

	[HttpGet]
	[UmbrellaProducesResponseType(StatusCodes.Status200OK)]
	[UmbrellaProducesResponseType(StatusCodes.Status404NotFound)]
	public Task<IActionResult> GetAsync(CancellationToken cancellationToken = default)
		=> ReadAsync<SystemSettings, int, ISystemSettingsRepository, RepoOptions, SystemSettingsModel>(
			1, _repository, cancellationToken, enableAuthorizationChecks: false);

	[HttpPut]
	[UmbrellaProducesResponseType(StatusCodes.Status200OK)]
	[UmbrellaProducesResponseType(StatusCodes.Status400BadRequest)]
	[UmbrellaProducesResponseType(StatusCodes.Status404NotFound)]
	[UmbrellaProducesResponseType(StatusCodes.Status409Conflict)]
	[UmbrellaProducesResponseType(StatusCodes.Status422UnprocessableEntity)]
	public Task<IActionResult> PutAsync(UpdateSystemSettingsModel model, CancellationToken cancellationToken = default)
		=> UpdateAsync<SystemSettings, int, ISystemSettingsRepository, RepoOptions, UpdateSystemSettingsModel, UpdateSystemSettingsResultModel>(
			model, _repository, cancellationToken, enableAuthorizationChecks: false);
}
```

**Rules:**

- Repositories are injected `Lazy<T>`.
- Decide `enableAuthorizationChecks` per action: pass `false` only when a declarative class-level policy fully covers access (as above); leave the default `true` when entity-level (row) authorization applies — a resource authorization handler must then exist (`umbrella-dotnet-scaffold-resource-auth-handler`).
- The helpers own the status codes, error handling, and concurrency behaviour — do not wrap helper calls in additional try/catch.
- Custom loading/mapping goes through the helper callbacks, not around them.
- Declare `[UmbrellaProducesResponseType]` per the helper's contract: `ReadAsync` → 200/404, `UpdateAsync` → 200/400/404/409, `CreateAsync` → 201/400, `DeleteAsync` → 204/404, plus 422 whenever the action binds input. Omit codes the shape rules out (e.g. no 404 when the seed row always exists — but only make that claim if seeding guarantees it).

## Variant B -- `UmbrellaApiController` (hand-rolled)

Every action follows the house envelope:

```csharp
[HttpGet]
[UmbrellaProducesResponseType(StatusCodes.Status200OK)]
[UmbrellaProducesResponseType(StatusCodes.Status404NotFound)]
[UmbrellaProducesResponseType(StatusCodes.Status422UnprocessableEntity)]
public async Task<IActionResult> GetAsync(string urlSegment, CancellationToken cancellationToken = default)
{
	cancellationToken.ThrowIfCancellationRequested();

	try
	{
		ContentPage? contentPage = await _contentPageRepository.Value.FindByUrlSegmentAsync(urlSegment, cancellationToken: cancellationToken);

		if (contentPage is null)
			return NotFound("The content page could not be found.");

		var model = await Mapper.MapAsync<ContentPage, ContentPageModel>(contentPage, cancellationToken);

		return Ok(model);
	}
	catch (Exception exc) when (Logger.WriteError(exc, new { urlSegment }, returnValue: !IsDevelopment))
	{
		return InternalServerError("There has been a problem getting the page content.");
	}
}
```

**Rules:**

- First line `cancellationToken.ThrowIfCancellationRequested();`, then `Guard` non-null reference parameters.
- Body wrapped in `try` / `catch (Exception exc) when (Logger.WriteError(exc, new { <inputs> }, returnValue: !IsDevelopment))` returning `InternalServerError("<action-specific message>")`. The `returnValue: !IsDevelopment` filter is mandatory — it re-throws in Development.
- Return every error through the status helpers; each distinct helper call is a branch the integration tests will target.
- **Concurrency on update paths**: load the tracked entity, compare `model.ConcurrencyStamp != entity.ConcurrencyStamp` → `return ConcurrencyConflict(ConcurrencyErrorMessage);` before saving, and add `catch (UmbrellaConcurrencyException) { return ConcurrencyConflict(ConcurrencyErrorMessage); }` before the general catch.
- **Duplicate guards on create paths**: pre-check and return `Conflict(...)`; when the save result can also report duplicates (e.g. Identity error codes), re-check after the save to close the race window.
- **Validation from save results** (e.g. `IdentityResult`): copy errors into `ModelState` and `return ValidationProblem(ModelState);` — this is a `400` by design, distinct from the model-binding `422`.
- **Related-entity references**: decide the response contract before adding a repository lookup. When an invalid mapped foreign key is intentionally a persistence failure handled by the catch-all `500`, map the scalar key and let the data layer enforce referential integrity; do not inject another repository or preload the navigation solely to check existence. Prevalidate only when the endpoint promises a domain-specific `400` or `404`, and declare that branch explicitly.
- **Logic services returning `IOperationResult`**: `return OperationResult<TModel>(result);` and declare the statuses the service can produce.
- **Sensitive lookups** (password reset, account existence): consider returning the success status regardless of resource existence (anti-enumeration) — document the choice in a comment so test generation asserts the intended behaviour instead of inferring a 404.
- Actions are `public virtual` only when a base-controller hierarchy needs overrides; otherwise non-virtual.

## Variant C -- `UmbrellaDataServiceApiController<TDataService>`

Each action composes the protected `ExecuteOperationAsync` envelope over one operation on the injected service. The envelope owns cancellation, `IOperationResult` → HTTP mapping, exception logging with caller info, and the `500` response — do not add try/catch around it. Example — a singleton settings resource backed by a read+update controller service:

```csharp
using IndyRecords.Web.Server.Infrastructure.Mvc;
using IndyRecords.Web.Server.Services.Abstractions;
using IndyRecords.Web.Shared.Models.Api.SystemSettings;
using IndyRecords.Web.Shared.Security.Policies;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace IndyRecords.Web.Server.Controllers.Api;

[Authorize(IndyRecordsPolicyNames.SystemSettingsManagement)]
public class SystemSettingsController : IndyRecordsDataServiceApiController<IManageSystemSettingsService>
{
	public SystemSettingsController(
		ILogger<SystemSettingsController> logger,
		IWebHostEnvironment hostingEnvironment,
		Lazy<IManageSystemSettingsService> dataService)
		: base(logger, hostingEnvironment, dataService)
	{
	}

	[HttpGet]
	[UmbrellaProducesResponseType(StatusCodes.Status200OK)]
	[UmbrellaProducesResponseType(StatusCodes.Status404NotFound)]
	public Task<IActionResult> GetAsync(CancellationToken cancellationToken = default)
		=> ExecuteOperationAsync<SystemSettingsModel>(
			(service, token) => service.FindAsync(token),
			"An error occurred while attempting to load the settings.",
			cancellationToken);

	[HttpPut]
	[UmbrellaProducesResponseType(StatusCodes.Status200OK)]
	[UmbrellaProducesResponseType(StatusCodes.Status400BadRequest)]
	[UmbrellaProducesResponseType(StatusCodes.Status404NotFound)]
	[UmbrellaProducesResponseType(StatusCodes.Status409Conflict)]
	[UmbrellaProducesResponseType(StatusCodes.Status422UnprocessableEntity)]
	public Task<IActionResult> PutAsync(UpdateSystemSettingsModel model, CancellationToken cancellationToken = default)
		=> ExecuteOperationAsync<UpdateSystemSettingsResultModel>(
			(service, token) => service.UpdateAsync(model, token),
			"An error occurred while attempting to update the settings.",
			cancellationToken,
			new { model });
}
```

The intermediate base for this variant is generic and passes the service type through:

```csharp
[Route("api/[controller]")]
public abstract class IndyRecordsDataServiceApiController<TDataService> : UmbrellaDataServiceApiController<TDataService>
{
	protected IndyRecordsDataServiceApiController(
		ILogger logger,
		IWebHostEnvironment hostingEnvironment,
		Lazy<TDataService> dataService)
		: base(logger, hostingEnvironment, dataService)
	{
	}
}
```

**Rules:**

- `TDataService` is unconstrained at the base-type level, but every method passed to `ExecuteOperationAsync` must return `Task<IOperationResult>` or `Task<IOperationResult<T>>`. The service may implement a subset of `IGenericDataService`, derive from `UmbrellaRepositoryDataService` (in which case its enablement/authorization flags and hooks behave as in Pattern 2), or be a fully custom result-based interface. Plain `Task<T>` methods require Variant B or an intentional service-contract change.
- Pass **expression lambdas returning the service's `Task` directly** — `(service, token) => service.FindAsync(token)` — never `async` lambdas, which can bind to the wrong `ExecuteOperationAsync` overload and lose the typed response body.
- Use the generic overload for operations returning `IOperationResult<T>` (200/201 with body) and the non-generic overload for plain `IOperationResult` (204/200 without body).
- Give each action an endpoint-specific `500` error message and pass the action's significant inputs as the `logState` anonymous object.
- Declare `[UmbrellaProducesResponseType]` per the statuses the composed service operation can return (for `UmbrellaRepositoryDataService`-derived services these match the Pattern 2 endpoint sets), plus 422 whenever the action binds input.
- Status codes come from the service's `IOperationResult`s — put conflict/not-found/validation decisions in the service, not the controller.

## Analyzer compatibility

Before finishing, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build the affected projects with their installed analyzers enabled. Treat diagnostics introduced by the generated or changed code as defects in this workflow.

## Verification

1. The controller derives from the app intermediate base, not the Umbrella base directly.
2. Every action declares its method-level codes with `[UmbrellaProducesResponseType]`; 401/403/500 are class-level only.
3. Variant A: no try/catch around helper calls; `enableAuthorizationChecks` decisions are deliberate and handlers exist where it is `true`.
4. Variant B: every action has the cancellation/guard/try-catch envelope with `returnValue: !IsDevelopment`; every error path uses an Umbrella status helper; update paths handle concurrency; create paths guard duplicates where applicable.
5. Variant C: actions are expression-bodied one-liners over `ExecuteOperationAsync` with expression lambdas (no `async` lambdas), endpoint-specific error messages, and log state for their inputs; no try/catch around the envelope.
6. `[Authorize]`/`[AllowAnonymous]` is explicit and intentional at class level.
7. Build the server project.

## Next steps

Generate integration tests: run `umbrella-dotnet-audit-api-controller-response-contract`, then `umbrella-dotnet-generate-custom-api-controller-tests` (its variants mirror this skill's). The explicit `[UmbrellaProducesResponseType]` declarations and status-helper branches this skill produces are exactly what test generation derives the contract from.
