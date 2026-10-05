---
name: umbrella-dotnet-scaffold-file-handler
description: 'Scaffold a file handler (interface, implementation, DirectoryNames constant, DI registration) in the Core.Logic project, following the Umbrella UmbrellaFileHandler pattern. Authorization is separate — see umbrella-dotnet-scaffold-file-authorization-handler.'
---

# Scaffold File Handler

## Purpose

Add a new file handler to the `Core.<AppName>.Core.Logic` project. File handlers plug into the Umbrella file storage infrastructure and are responsible for **storage operations only**: saving, retrieving, deleting files, generating web-relative or versioned URLs, caching file lookups, and optional post-save processing (e.g. image resizing).

Authorization is decoupled and lives in a separate `UmbrellaFileAuthorizationHandler` — see the `umbrella-dotnet-scaffold-file-authorization-handler` skill. A file handler can exist without a matching authorization handler if access control is handled elsewhere, but be aware that the default storage provider behaviour is to deny access for directories with no registered auth handler.

A file handler can represent any logical grouping of files — files attached to a database record, files in a SharePoint-style folder, user uploads, generated reports, or anything else. The group ID (`int`) is whatever identifier separates one group of files from another for this particular handler.

## How the provider uses the handler

The provider uses the handler's `DirectoryName` to construct the file path (`/<directoryName>/<groupId>/<fileName>`). The `DirectoryName` property on the handler **must exactly match** the constant registered in `DirectoryNames`, as authorization lookup (in the separate auth handler) uses the same value.

## Discovery (read these before writing anything)

1. Read existing file handler implementations in `Core\<AppName>.Core.Logic\FileSystem\` to understand the pattern.
2. Read the interfaces in `Core\<AppName>.Core.Logic\FileSystem\Abstractions\`.
3. Read `Core\<AppName>.Core.Common\FileSystem\Constants\DirectoryNames.cs` to see existing constants and the `All` collection.
4. Read `Core\<AppName>.Core.Logic\IServiceCollectionExtensions.cs` to see where handlers are registered.
5. Read the consuming project's `TargetFramework` or `TargetFrameworks` and its direct package references. Do not infer its target frameworks from Umbrella's multi-targeted source projects.
6. Confirm the installed `UmbrellaFileHandler<TGroupId>` constructor for every consumer target. Current Umbrella packages use Microsoft `HybridCache` on .NET 9 or later and `IDistributedCache` below .NET 9; never use the removed Umbrella `IHybridCache` abstraction.

---

## Step 1 -- Add the DirectoryNames constant

**File:** `Core\<AppName>.Core.Common\FileSystem\Constants\DirectoryNames.cs`

Add a new `public const string` entry using lowercase, hyphenated naming (kebab-case):

```csharp
public const string <Name> = "<name-in-kebab-case>";
```

Also add the new constant to the `All` collection:

```csharp
public static readonly IReadOnlyCollection<string> All = [
    // existing entries ...
    <Name>
];
```

---

## Step 2 -- Create the interface

**File location:** `Core\<AppName>.Core.Logic\FileSystem\Abstractions\I<Name>FileHandler.cs`

```csharp
using Umbrella.FileSystem.Abstractions;

namespace <AppName>.Core.Logic.FileSystem.Abstractions;

public interface I<Name>FileHandler : IUmbrellaFileHandler<int>;
```

**Rules:**
- Empty marker interface — all behaviour comes from the base interface and implementation
- Always extends `IUmbrellaFileHandler<int>`
- Needs the explicit `using Umbrella.FileSystem.Abstractions;` — not in global usings for this project

---

## Step 3 -- Create the implementation

**File location:** `Core\<AppName>.Core.Logic\FileSystem\<Name>FileHandler.cs`

The primary examples below are for projects whose targets are all .NET 9 or later. Use the target-framework decision rules after the examples for legacy or genuinely cross-boundary multi-targeted consumers.

**Minimal pattern (no post-save processing):**

```csharp
using <AppName>.Core.Common.FileSystem.Constants;
using <AppName>.Core.Logic.FileSystem.Abstractions;
using Microsoft.Extensions.Caching.Hybrid;
using Umbrella.FileSystem.Abstractions;
using Umbrella.Utilities.Caching.Abstractions;

namespace <AppName>.Core.Logic.FileSystem;

internal sealed class <Name>FileHandler : UmbrellaFileHandler<int>, I<Name>FileHandler
{
    public <Name>FileHandler(
        ILogger<<Name>FileHandler> logger,
        HybridCache cache,
        ICacheKeyUtility cacheKeyUtility,
        IUmbrellaFileStorageProvider fileProvider,
        IUmbrellaFileStorageProviderOptions options)
        : base(logger, cache, cacheKeyUtility, fileProvider, options)
    {
    }

    public override string DirectoryName => DirectoryNames.<Name>;
}
```

**With post-save image resizing:**

```csharp
using <AppName>.Core.Common.FileSystem.Constants;
using <AppName>.Core.Logic.FileSystem.Abstractions;
using Microsoft.Extensions.Caching.Hybrid;
using Umbrella.DynamicImage.Abstractions;
using Umbrella.FileSystem.Abstractions;
using Umbrella.Utilities.Caching.Abstractions;

namespace <AppName>.Core.Logic.FileSystem;

internal sealed class <Name>FileHandler : UmbrellaFileHandler<int>, I<Name>FileHandler
{
    private readonly IDynamicImageResizer _dynamicImageResizer;
    private readonly IDynamicImageUtility _dynamicImageUtility;

    public <Name>FileHandler(
        ILogger<<Name>FileHandler> logger,
        HybridCache cache,
        ICacheKeyUtility cacheKeyUtility,
        IUmbrellaFileStorageProvider fileProvider,
        IUmbrellaFileStorageProviderOptions options,
        IDynamicImageResizer dynamicImageResizer,
        IDynamicImageUtility dynamicImageUtility)
        : base(logger, cache, cacheKeyUtility, fileProvider, options)
    {
        _dynamicImageResizer = dynamicImageResizer;
        _dynamicImageUtility = dynamicImageUtility;
    }

    public override string DirectoryName => DirectoryNames.<Name>;

    protected override async Task AfterSavingAsync(IUmbrellaFileInfo fileInfo, int groupId, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        byte[] imageBytes = await fileInfo.ReadAsByteArrayAsync(cancellationToken: cancellationToken);
        var format = _dynamicImageUtility.ParseImageFormat(Path.GetExtension(fileInfo.Name));
        var (resizedBytes, _, _) = _dynamicImageResizer.ResizeImage(imageBytes, 1600, 1600, DynamicResizeMode.UseWidth, format, DynamicImageFilterQuality.High, 100);
        await fileInfo.WriteFromByteArrayAsync(resizedBytes, cancellationToken: cancellationToken);
    }
}
```

**Rules:**
- Always `internal sealed class` inheriting `UmbrellaFileHandler<int>` and the marker interface
- Base 5 constructor params in this exact order: `ILogger<T>`, the cache type selected below, `ICacheKeyUtility`, `IUmbrellaFileStorageProvider`, `IUmbrellaFileStorageProviderOptions` — all passed to `: base(...)`
- Choose the cache dependency from the consuming project's targets:

| Consumer targets | Constructor type | Using |
| --- | --- | --- |
| All targets are .NET 9 or later | `HybridCache` | `using Microsoft.Extensions.Caching.Hybrid;` |
| All targets are below .NET 9 | `IDistributedCache` | `using Microsoft.Extensions.Caching.Distributed;` |
| Targets exist on both sides of .NET 9 | A conditional `PlatformCache` alias | Alias `HybridCache` for `NET9_0_OR_GREATER`; otherwise alias `IDistributedCache` |

- Do not emit preprocessor directives for a single-target project, or for a multi-target project whose targets all select the same cache API. Umbrella's own multi-targeting is not a reason to copy its conditional alias into consumer code.
- If the consumer directly names `HybridCache`, add a direct `Microsoft.Extensions.Caching.Hybrid` package reference for each applicable target and keep its major version coupled to that target framework (for example, 9.x for `net9.0` and 10.x for `net10.0`).
- On .NET 9 or later, `AddUmbrellaUtilities()` provides the baseline `HybridCache` registration. Do not add a second `AddHybridCache()` call merely to activate the handler. Use Microsoft's `AddHybridCache(options => ...)` only when the application intentionally configures cache options.
- Below .NET 9, verify that the application registers an `IDistributedCache` implementation.
- Extra dependencies go AFTER the 5 base params and are stored as `private readonly` fields
- `DirectoryName` must return `DirectoryNames.<Name>` — the same constant added in Step 1
- Do NOT add `AuthorizeAsync` here — authorization belongs in a separate `UmbrellaFileAuthorizationHandler` (see `umbrella-dotnet-scaffold-file-authorization-handler`)
- Override `AfterSavingAsync` only when post-save processing is needed; always call `cancellationToken.ThrowIfCancellationRequested()` first
- `using Umbrella.DynamicImage.Abstractions;` is only needed when overriding `AfterSavingAsync` for image work — confirm the package is referenced in the `.csproj`
- Dynamic Image consumers obtain their URL/token pair from the inherited `GetVersionedWebFilePathAsync`; do not add a second token algorithm to the concrete handler.
- If several concrete handlers share behavior, put it in an `internal abstract` base whose name ends in `FileHandlerBase`; keep each DI-resolved implementation named `*FileHandler` and `internal sealed`.

### Custom operations and logging

When a handler needs a custom public operation, keep argument guards and cancellation checks before its outer `try`. The preferred logging pattern is the repository exception filter with explicit method state:

```csharp
catch (Exception exc) when (Logger.WriteError(exc, new { groupId, fileName, ownerId }))
{
    throw new <AppName>CoreLogicException("There has been a problem processing the file.", exc);
}
```

Use this form instead of calling `Logger.LogError` or `Logger.LogCritical` directly. UA008 currently accepts structured calls to those methods, so an analyzer-clean build alone does not prove that the preferred exception-filter pattern was used.

### Authorization metadata and temporary files

File handlers are singletons and must remain stateless between calls. When protected-file reads depend on per-request ownership or tenancy metadata:

- Pass the metadata to a narrowly scoped custom handler method as explicit parameters.
- Resize or otherwise prepare the temporary file and write its authorization metadata **before** calling `CreateByGroupIdAndTempFileNameAsync`. This lets the normal move carry a fully secured file into the protected directory.
- Do not defer required authorization metadata until a post-move read or `AfterSavingAsync` operation if that read would need the same metadata to authorize it.
- Never use `AsyncLocal`, `ThreadStatic`, mutable singleton fields, ambient context classes, or authorization-bypass flags to transport metadata through the file lifecycle.
- Never add a special bypass to the matching file authorization handler for file-handler internals. If the framework lifecycle appears to require one, inspect the base handler lifecycle and storage-provider APIs before proceeding.
- Verify through the real HTTP file endpoint that metadata survives the temporary-to-protected move and that matching and mismatching identities receive the expected responses.

---

## Step 4 -- Register in DI

**File:** `Core\<AppName>.Core.Logic\IServiceCollectionExtensions.cs`

Add one line in the `// File Handlers` section, in alphabetical order:

```csharp
_ = services.AddSingleton<I<Name>FileHandler, <Name>FileHandler>();
```

File handlers are always `AddSingleton` — they are stateless and safe to share across requests.

---

## Analyzer compatibility

Before finishing, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build the affected projects with their installed analyzers enabled. Treat diagnostics introduced by the generated or changed code as defects in this workflow.

## Verification

1. `DirectoryNames.<Name>` constant exists and is added to the `All` collection.
2. The interface is an empty marker extending `IUmbrellaFileHandler<int>` with the `using Umbrella.FileSystem.Abstractions;` directive.
3. The implementation is `internal sealed`, the constructor passes exactly the 5 base params to `: base(...)`, and `DirectoryName` returns the correct constant. Reusable abstract bases are `internal abstract` and end in `FileHandlerBase`.
4. There is no `AuthorizeAsync` on the file handler — authorization is in a separate handler.
5. `AddSingleton<I<Name>FileHandler, <Name>FileHandler>()` is present in `IServiceCollectionExtensions.cs`.
6. If authorization is needed, the `umbrella-dotnet-scaffold-file-authorization-handler` skill has been used to create a matching `<Name>FileAuthorizationHandler` with the same `DirectoryName`.
7. If the handler backs Dynamic Image, callers use `GetVersionedWebFilePathAsync` and propagate its URL and token together.
8. The cache constructor type matches every consuming target: direct `HybridCache` for all-.NET-9-or-later projects, direct `IDistributedCache` for all-legacy projects, or a conditional alias only for a genuine cross-boundary multi-target project. There is no `IHybridCache` usage or legacy-cache warning suppression.
9. Custom public methods use the `Logger.WriteError` exception-filter pattern with relevant state.
10. Ownership or tenancy metadata is attached without ambient state or an authorization bypass, and its behavior is covered through the HTTP file endpoint.
