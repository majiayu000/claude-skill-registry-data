---
name: umbrella-dotnet-scaffold-client-data
description: 'Scaffold a client-side HTTP data service implementing an existing IManage<Name>Service interface, following the Umbrella GenericHttpDataService pattern. Registers the service in the client project and updates the server DI from AddScoped to ReplaceScoped.'
---

# Scaffold Client Data Service

## Purpose

Add a client-side HTTP data service to `Web\<AppName>.Web.Client.Data\Services\` that implements an existing `IManage<Name>Service` interface using `GenericHttpDataService`. This is the transport layer that Blazor client components use to call the API — the same interface that `Manage<Name>ControllerService` implements on the server side.

**Prerequisite:** `umbrella-dotnet-scaffold-api-data-service-controller` must have run first. The service interface (`IManage<Name>Service`) and server controller service (`Manage<Name>ControllerService`) must already exist.

This skill also updates the server DI registration from `AddScoped` to `ReplaceScoped`, so the server continues to use the direct-repository implementation while the client uses this HTTP implementation.

## Discovery (read these before writing anything)

1. Read 2–3 existing client data services in `Web\<AppName>.Web.Client.Data\Services\` to confirm naming conventions, usings, and the exact `ApiUrl` format used (e.g. `"api/ManageIndustry"`).
2. Read `Web\<AppName>.Web.Client.Data\IServiceCollectionExtensions.cs` to see where to add the `AddScoped` registration and how existing services are registered.
3. Read `Web\<AppName>.Web.Server\IServiceCollectionExtensions.cs` — find the `// Controller Services` section to confirm the current registration for `IManage<Name>Service` and whether it is already `ReplaceScoped`.

---

## Step 1 -- Create the client data service

**File:** `Web\<AppName>.Web.Client.Data\Services\Manage<Name>Service.cs`

```csharp
using <AppName>.Web.Client.Data.Services.Abstractions;
using <AppName>.Web.Shared.Models.Api.Manage<Name>;
using Umbrella.Utilities.Data.Pagination;
using Umbrella.Utilities.DataAnnotations.Abstractions;
using Umbrella.Utilities.Http.Abstractions;

namespace <AppName>.Web.Client.Data.Services;

internal sealed class Manage<Name>Service : GenericHttpDataService<
    Manage<Name>Model,
    int,
    SlimManage<Name>Model,
    PaginatedResultModel<SlimManage<Name>Model>,
    CreateManage<Name>Model,
    CreateManage<Name>ResultModel,
    UpdateManage<Name>Model,
    UpdateManage<Name>ResultModel>, IManage<Name>Service
{
    public Manage<Name>Service(
        ILogger<Manage<Name>Service> logger,
        IGenericHttpService httpService,
        IGenericHttpServiceUtility httpServiceUtility,
        IUmbrellaValidator validator)
        : base(logger, httpService, httpServiceUtility, validator)
    {
    }

    protected override string ApiUrl => "api/Manage<Name>";
}
```

**Rules:**
- `internal sealed class` — the service is resolved via the interface; it never needs to be referenced directly outside this assembly.
- `GenericHttpDataService` generic params in order (8 total): `TModel`, `TIdentifier`, `TSlimModel`, `TPaginatedResultModel`, `TCreateModel`, `TCreateResultModel`, `TUpdateModel`, `TUpdateResultModel`. Note `TModel` comes first (same order as `IGenericDataService`).
- `ApiUrl` must match the controller's route: `[Route("api/[controller]")]` resolves to `"api/Manage<Name>"` — verify against the existing controller.
- No additional overrides are needed unless an endpoint uses a non-standard URL segment. Check existing client services to confirm.

---

## Step 2 -- Register in client DI

**File:** `Web\<AppName>.Web.Client.Data\IServiceCollectionExtensions.cs`

Add one line in alphabetical order among the other `AddScoped` service registrations. Preserve unrelated registration order and formatting; do not turn this focused scaffold into a wholesale reordering of an existing section.

```csharp
_ = services.AddScoped<IManage<Name>Service, Manage<Name>Service>();
```

---

## Step 3 -- Update server DI registration

**File:** `Web\<AppName>.Web.Server\IServiceCollectionExtensions.cs`

Find the existing `AddScoped<IManage<Name>Service, Manage<Name>ControllerService>()` line added by `umbrella-dotnet-scaffold-api-data-service-controller` and change it to `ReplaceScoped`:

```csharp
// Before:
_ = services.AddScoped<IManage<Name>Service, Manage<Name>ControllerService>();

// After:
_ = services.ReplaceScoped<IManage<Name>Service, Manage<Name>ControllerService>();
```

This ensures that at server runtime the client's `AddScoped` registration (loaded when the server bootstraps the client services for SSR pre-rendering) is replaced by the direct-repository implementation.

If the server registration is already `ReplaceScoped`, skip this step.

---

## Analyzer compatibility

Before finishing, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build the affected projects with their installed analyzers enabled. Treat diagnostics introduced by the generated or changed code as defects in this workflow.

## Verification

1. The client service is `internal sealed class` inheriting `GenericHttpDataService` with 8 type params in the correct order (same as `IGenericDataService`).
2. `ApiUrl` matches the controller route — confirm against the existing controller file.
3. `AddScoped<IManage<Name>Service, Manage<Name>Service>()` is present in `Web.Client.Data.IServiceCollectionExtensions.cs`.
4. The server registration for `IManage<Name>Service` is now `ReplaceScoped` (not `AddScoped`).
5. The implementation imports the namespaces that own `IUmbrellaValidator`, `IGenericHttpService`, and `IGenericHttpServiceUtility`; do not rely on project-specific global usings unless discovery confirms them.
