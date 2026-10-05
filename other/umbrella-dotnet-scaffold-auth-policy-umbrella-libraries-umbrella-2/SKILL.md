---
name: umbrella-dotnet-scaffold-auth-policy
description: 'Scaffold a new ASP.NET Core authorization policy — adds a name constant to the shared policy names class and registers the policy in the shared AuthorizationOptions extension method. Used by both controllers ([Authorize]) and Blazor pages/nav (<AuthorizeView>).'
---

# Scaffold Auth Policy

## Purpose

Add a new named authorization policy to the shared project so it can be applied to API controllers (`[Authorize(PolicyName)]`), Blazor page code-behinds (`[Authorize(PolicyName)]`), and nav items (`<AuthorizeView Policy="@PolicyName">`).

Policies are defined in the shared project (not the server or client) so that both the server and Blazor client can reference the same constants without introducing circular dependencies.

**When to add a new policy vs. using an existing one:** Use an existing policy if the feature fits within an existing access boundary (e.g. same admin section = same `SiteSettingsMenu` policy). Add a new policy when the feature has genuinely distinct access requirements — a different user role, a new section of the app, or a combination of roles not already captured.

## Discovery (read these before writing anything)

1. Read the shared policy names class (e.g. `Web\<AppName>.Web.Shared\Security\Policies\SharedPolicyNames.cs`) in full — understand the grouping conventions (role policies, menu policies, feature policies) and the naming style.
2. Read the shared `AuthorizationOptionsExtensions.cs` (e.g. `Web\<AppName>.Web.Shared\Security\Extensions\AuthorizationOptionsExtensions.cs`) in full — understand the existing registration patterns and which role/assertion helpers are available.
3. Confirm the `AppRoleType` enum (or equivalent) to know the available roles.

---

## Step 1 -- Add the policy name constant

**File:** `Web\<AppName>.Web.Shared\Security\Policies\<AppName>PolicyNames.cs`

Add a `public const string` in the appropriate group, in alphabetical order within that group:

```csharp
// Role-based (top-level access gate)
public const string <Name>Role = nameof(<Name>Role);

// Menu / section (controls whether a nav section is visible)
public const string <Name>Menu = nameof(<Name>Menu);

// Feature (specific action or data domain)
public const string <Name>Management = nameof(<Name>Management);
```

Use `nameof(ConstantName)` for the value — this avoids string duplication and keeps constant name and value in sync.

---

## Step 2 -- Register the policy

**File:** `Web\<AppName>.Web.Shared\Security\Extensions\AuthorizationOptionsExtensions.cs`

Add one `options.AddPolicy(...)` call inside the `Add<AppName>Policies` extension method, in the same grouping order as the constants:

### Simple role requirement (single role)
```csharp
options.AddPolicy(<AppName>PolicyNames.<Name>, x => x.RequireRole(nameof(AppRoleType.<Role>)));
```

### Multi-role requirement (any of these roles may access)
```csharp
options.AddPolicy(<AppName>PolicyNames.<Name>, x => x.RequireRole(
    nameof(AppRoleType.<Role1>),
    nameof(AppRoleType.<Role2>)));
```

### Primary role assertion (when role hierarchy or claim-based primary role is used)
```csharp
options.AddPolicy(<AppName>PolicyNames.<Name>, x =>
    x.RequireAssertion(ctx => ctx.User.GetPrimaryRole<AppRoleType>() == AppRoleType.<Role>));
```

### Combined: multiple primary role values
```csharp
options.AddPolicy(<AppName>PolicyNames.<Name>, x =>
    x.RequireAssertion(ctx =>
    {
        var role = ctx.User.GetPrimaryRole<AppRoleType>();
        return role is AppRoleType.<Role1> or AppRoleType.<Role2>;
    }));
```

**Rules:**
- Always use the constant from Step 1 as the policy name — never a raw string.
- `RequireRole` accepts role names as strings — use `nameof(AppRoleType.X)` to keep them refactor-safe.
- `GetPrimaryRole<T>()` is an Umbrella/project extension on `ClaimsPrincipal` — check the shared project for its availability before using it.
- The `AddPolicy` call must be in the shared extension method, not in `Program.cs` directly, so both server and client register the same policies.

---

## Analyzer compatibility

Before finishing, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build the affected projects with their installed analyzers enabled. Treat diagnostics introduced by the generated or changed code as defects in this workflow.

## Verification

1. The constant is in the correct group in `<AppName>PolicyNames.cs` and uses `nameof(...)` for its value.
2. The `AddPolicy` call is in the shared extension method (not `Program.cs` or a server-only file).
3. The policy correctly restricts to the intended role(s) — verify by checking an analogous existing policy as a reference.
4. The constant compiles — no typo in `nameof(...)` that would cause a compile error.
