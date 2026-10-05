---
name: umbrella-dotnet-scaffold-resource-auth-handler
description: 'Scaffold a resource-based ASP.NET Core IAuthorizationHandler for an entity, handling row-level access control (ownership, role, operation-specific checks). Used when AuthorizationXxxChecksEnabled is not suppressed on a controller or controller service.'
---

# Scaffold Resource Authorization Handler

## Purpose

Add a resource-based `IAuthorizationHandler` that enforces row-level access control for a specific entity type. The Umbrella base controller and controller service internally call `IAuthorizationService.AuthorizeAsync(user, entity, policyName)` for each CRUD operation when the corresponding `AuthorizationXxxChecksEnabled` property is not suppressed. This handler is what ASP.NET Core invokes in response to those calls.

**When is this needed?** By default, the controller skills set all `AuthorizationXxxChecksEnabled` overrides to `false`, which bypasses the built-in resource-level checks. If you remove those overrides (or set any to `true`) for a specific operation, a matching `IAuthorizationHandler<OperationAuthorizationRequirement, TEntity>` must be registered — otherwise access will be denied for all users.

**Relationship to `[Authorize(PolicyName)]`:** The controller-level `[Authorize]` attribute is a coarse-grained gate (is the user authenticated and in the right role?). The resource auth handler is the fine-grained gate (can this specific user access this specific entity row?). Both must pass.

## Discovery (read these before writing anything)

1. Read 2–3 existing resource auth handlers in `Web\<AppName>.Web.Server\Security\Handlers\` to understand the role-check patterns, how ownership is verified (e.g. `resource.AppUserId == context.User.GetId<int>()`), and how operation-specific logic is structured.
2. Confirm which `CoreItemOperations` are used (`Create`, `Read`, `Update`, `Delete`) — these are the requirement values the base controller passes.
3. Read the entity type to understand what ownership or relationship fields are available (e.g. `AppUserId`, `LearningProviderId`).
4. Read `Web\<AppName>.Web.Server\IServiceCollectionExtensions.cs` — find the `// Authorization Handlers` section to see the existing registration style.
5. Confirm the target controller or controller service already exists and identify the exact `AuthorizationXxxChecksEnabled` override to remove. If it does not exist, stop and use `umbrella-dotnet-scaffold-api-repo-controller` or `umbrella-dotnet-scaffold-api-data-service-controller` first; do not create an ad-hoc controller inside this security-only workflow.

---

## Step 1 -- Create the handler

**File:** `Web\<AppName>.Web.Server\Security\Handlers\<Name>AuthorizationHandler.cs`

```csharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authorization.Infrastructure;
using <AppName>.Core.Domain.Entities;
using Umbrella.AspNetCore.WebUtilities.Security.Policies;

namespace <AppName>.Web.Server.Security.Handlers;

internal sealed class <Name>AuthorizationHandler : AuthorizationHandler<OperationAuthorizationRequirement, <Name>>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        OperationAuthorizationRequirement requirement,
        <Name> resource)
    {
        if (context.User.GetId<int>() == resource.AppUserId)
            context.Succeed(requirement);

        return Task.CompletedTask;
    }
}
```

### Operation-specific logic

When different operations need different checks, switch on `requirement`:

```csharp
protected override Task HandleRequirementAsync(
    AuthorizationHandlerContext context,
    OperationAuthorizationRequirement requirement,
    <Name> resource)
{
    bool succeed = requirement switch
    {
        var operation when operation == CoreItemOperations.Read =>
            context.User.GetId<int>() == resource.AppUserId,

        var operation when operation == CoreItemOperations.Create ||
                           operation == CoreItemOperations.Update ||
                           operation == CoreItemOperations.Delete =>
            context.User.IsInRole(nameof(AppRoleType.Administrator)),

        _ => false
    };

    if (succeed)
        context.Succeed(requirement);

    return Task.CompletedTask;
}
```

### Role-aware ownership (multi-role pattern)

When higher roles bypass ownership checks:

```csharp
protected override Task HandleRequirementAsync(
    AuthorizationHandlerContext context,
    OperationAuthorizationRequirement requirement,
    <Name> resource)
{
    bool succeed = false;

    if (context.User.IsInRole(nameof(AppRoleType.System)) ||
        context.User.IsInRole(nameof(AppRoleType.SuperAdministrator)) ||
        context.User.IsInRole(nameof(AppRoleType.Administrator)))
    {
        succeed = true;
    }
    else if (context.User.IsInRole(nameof(AppRoleType.Student)))
    {
        succeed = requirement == CoreItemOperations.Read &&
                  resource.AppUserId == context.User.GetId<int>();
    }

    if (succeed)
        context.Succeed(requirement);

    return Task.CompletedTask;
}
```

**Rules:**
- `internal sealed class` — registered and resolved via `IAuthorizationHandler`; never needs to be referenced directly.
- Inherit directly from `AuthorizationHandler<OperationAuthorizationRequirement, TEntity>` — there is no Umbrella-specific base class for resource handlers.
- Call `context.Succeed(requirement)` when authorized. **Never call `context.Fail()`** — per ASP.NET Core convention, non-success is the default and explicit failure blocks all other handlers.
- The handler is only invoked when the base controller/service calls `AuthorizeAsync` for the matching entity type — it does not need to guard against being called for the wrong type.
- Use `CoreItemOperations.Create`, `CoreItemOperations.Read`, `CoreItemOperations.Update`, `CoreItemOperations.Delete` for comparisons (not string literals).

---

## Step 2 -- Enable the auth check on the controller or controller service

In the controller (Pattern 1) or controller service (Pattern 2), remove the suppression override(s) for the operations this handler should enforce. The base class defaults to `true` (enabled) — only operations explicitly suppressed with `=> false` bypass the handler.

**Pattern 1 controller — enable Read check:**
```csharp
// Remove this line (or omit it):
protected override bool AuthorizationReadChecksEnabled => false;

// Keep suppressed for operations the handler does not cover:
protected override bool AuthorizationSlimReadChecksEnabled => false;
protected override bool AuthorizationCreateChecksEnabled => false;
protected override bool AuthorizationUpdateChecksEnabled => false;
protected override bool AuthorizationDeleteChecksEnabled => false;
```

**Pattern 2 controller service — same approach:**
Remove the suppression override for the targeted operation on `<Name>ControllerService`.

---

## Step 3 -- Register in DI

**File:** `Web\<AppName>.Web.Server\IServiceCollectionExtensions.cs` — `// Authorization Handlers` section, alphabetical order:

```csharp
_ = services.AddScoped<IAuthorizationHandler, <Name>AuthorizationHandler>();
```

---

## Analyzer compatibility

Before finishing, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build the affected projects with their installed analyzers enabled. Treat diagnostics introduced by the generated or changed code as defects in this workflow.

## Verification

1. The handler is `internal sealed class` inheriting `AuthorizationHandler<OperationAuthorizationRequirement, <EntityType>>`.
2. `HandleRequirementAsync` calls `context.Succeed(requirement)` on the success path and **never** calls `context.Fail()`.
3. The corresponding `AuthorizationXxxChecksEnabled` override is absent (or `true`) on the controller/controller service for any operation this handler covers.
4. `services.AddScoped<IAuthorizationHandler, <Name>AuthorizationHandler>()` is present in `IServiceCollectionExtensions.cs`.
5. If the handler only covers some operations (e.g. Read only), the remaining operations on the controller are still suppressed with `=> false`.
6. A test identity can be constructed that the handler denies (e.g. a non-owner user id or missing role). A handler that succeeds for every authenticated user makes the imperative 403 path untestable in integration tests — if that is intentional, note it so test generation skips the 403 tests.
