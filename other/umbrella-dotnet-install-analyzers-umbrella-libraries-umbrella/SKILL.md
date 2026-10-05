---
name: umbrella-dotnet-install-analyzers
description: 'Install the Umbrella Roslyn analyzer packages (Umbrella.Analyzers, Umbrella.DataAccess.Analyzers, Umbrella.Utilities.Mapping.Mapperly.Analyzers, Umbrella.WebUtilities.DynamicImage.Analyzers) and the Umbrella.Analyzers.Abstractions package supplying the model marker and exception attributes into a consuming .NET repository with the correct per-package scope. Also use when those attributes fail to resolve in a consuming project.'
---

# Install Umbrella Analyzers

## Purpose

Wire up the four Umbrella Roslyn analyzer packages in a consuming repository (e.g. a Kernel/API/Blazor solution that already references other `Umbrella.*` packages) so that `UA*`, `UDA*`, `UMA*`, and `UWDI*` diagnostics documented in `.ai-shared\bundles\umbrella\analyzer-compatibility.md` are actually enforced at build time. Installing the packages does not change any C#/Razor source — it only adds `PackageReference` entries. Diagnostics surfaced by a fresh install are a separate follow-up, not part of this skill (see Verification).

Each package has a different correct scope. Do not install them all the same way.

Four of the five are analyzers and are installed as `PrivateAssets="All"` development dependencies. The fifth,
`Umbrella.Analyzers.Abstractions`, is **not** an analyzer — it is an ordinary runtime assembly supplying the model
opt-out attributes, and it must **not** be private. See Step 1 for why.

| Package | Scope | Rule |
|---|---|---|
| `Umbrella.Analyzers` | Global | Every project in the solution — general coding-standard/model-immutability rules (`UA*`) apply everywhere. |
| `Umbrella.Analyzers.Abstractions` | Global, **not** private | Supplies `[UmbrellaInputModel]`, `[UmbrellaAllowUnsealedModel]`, `[UmbrellaAllowNonRequiredProperty]` and `[UmbrellaAllowMutableProperty]` (namespace `Umbrella.Analyzers`). Needed by every project that applies them, and must reach publish output. |
| `Umbrella.Utilities.Mapping.Mapperly.Analyzers` | Global | Every project. It is inert outside Mapperly `[Mapper]` usage, so global installation is safe and avoids per-project drift as new mapping consumers are added. |
| `Umbrella.DataAccess.Analyzers` | Per-project | Only projects that **implement** repositories (`UDA*` checks naming/encapsulation on concrete repository classes). |
| `Umbrella.WebUtilities.DynamicImage.Analyzers` | Per-project | Only projects with an actual Dynamic Image surface: Razor/Blazor markup using `<UmbrellaDynamicImage>`/`<UmbrellaFileImagePreviewUpload>`, or a mapping project that assigns `*Url`/`*VersionToken` model pairs together. |

## Discovery (read/run these before editing anything)

1. **Resolve the shared Umbrella package version.** Grep the target repo for an existing `Umbrella.*` `PackageReference` version (e.g. `Umbrella.AspNetCore.WebUtilities`, `Umbrella.DataAccess.Abstractions`) in `.csproj` files. Use that exact version string for all five packages — never hardcode a version from this skill or from another repo. If multiple versions are present, use the version that matches the majority of `Umbrella.*` references and flag any outliers to the user.
2. **Confirm the shared-injection pattern.** Open `Directory.Packages.props` at the repo root. In this org it is **not** real NuGet Central Package Management (`ManagePackageVersionsCentrally` is not set) — it is a shared file whose unconditioned `<ItemGroup>` of `<PackageReference>` items is imported into every project, the same way `Microsoft.CodeAnalysis.Analyzers`/`Microsoft.VisualStudio.Threading.Analyzers` already are. If the repo instead uses genuine CPM (`ManagePackageVersionsCentrally=true` and `<PackageVersion>` items), adapt: add `<PackageVersion>` centrally and an unversioned `<PackageReference>` in each qualifying project.
3. **Check what is already installed.** Grep all `.csproj`/`.props` files for each of the five package IDs. Skip any that are already present at the correct version and scope; report a version mismatch rather than silently overwriting it. Treat an existing `Umbrella.Analyzers.Abstractions` reference carrying `PrivateAssets` as a defect to fix, not as already-installed.
4. **Enumerate repository-implementation projects** (for `Umbrella.DataAccess.Analyzers`). A project qualifies when it:
   - has a `Repositories\` folder containing concrete repository classes (not just an `Abstractions`/domain project that merely references `Umbrella.DataAccess.Abstractions` for entity/domain types), **and**
   - references a concrete Umbrella data-access implementation package, e.g. `Umbrella.DataAccess.EntityFrameworkCore[.SqlServer]`, or is a library implementing `IUmbrellaRepository` directly (e.g. a Dataverse/Cosmos/etc. data-access library).
   Domain/entity-only projects (referencing only `Umbrella.DataAccess.Abstractions`) do not qualify, even though they're part of the data-access layer.
5. **Enumerate Dynamic Image projects** (for `Umbrella.WebUtilities.DynamicImage.Analyzers`). A project qualifies when it:
   - contains `.razor` files or Razor views using `<UmbrellaDynamicImage>` / `<UmbrellaFileImagePreviewUpload>` tag helpers or components, **or**
   - is the Mapperly model-factory/mapping project that assigns `*Url` and `*VersionToken` properties together (it participates in the paired-assignment check even without its own markup).
   A project that merely references `Umbrella.AspNetCore.WebUtilities.DynamicImage`/`Umbrella.DynamicImage.*` for server-side registration (service registration, middleware, catalog config) but has **no** Razor/Blazor surface and does **not** perform the paired model assignment does **not** automatically qualify — flag it to the user instead of guessing. This situation is common in API-only projects that expose Dynamic Image endpoints without owning any Razor/Blazor markup themselves.

If step 4 or 5 turns up an ambiguous project (e.g. no `.razor` files anywhere in the repo, or a repository-shaped project that doesn't cleanly match the pattern), stop and ask the user to confirm scope before editing rather than guessing.

## Step 1 — Install the global analyzers and the attributes package

In `Directory.Packages.props`, add these to the existing unconditioned `<ItemGroup>` (next to `Microsoft.CodeAnalysis.Analyzers` etc.), using the version resolved in Discovery step 1:

```xml
<PackageReference Include="Umbrella.Analyzers" Version="{{resolvedVersion}}" PrivateAssets="All" />
<PackageReference Include="Umbrella.Utilities.Mapping.Mapperly.Analyzers" Version="{{resolvedVersion}}" PrivateAssets="All" />
<PackageReference Include="Umbrella.Analyzers.Abstractions" Version="{{resolvedVersion}}" />
```

**Never put `PrivateAssets` on `Umbrella.Analyzers.Abstractions`, and never rely on the analyzer package to supply the
attributes.** Applying `[UmbrellaInputModel]`, `[UmbrellaAllowUnsealedModel]`, `[UmbrellaAllowNonRequiredProperty]` or `[UmbrellaAllowMutableProperty]`
writes a permanent assembly reference into the consuming assembly, so the attribute assembly has to reach publish
output. `Umbrella.Analyzers` is a `developmentDependency` and is stripped from publish output, so if the attributes
resolve from it the solution builds and every test passes, then the deployed app dies at startup with
`FileNotFoundException: Could not load file or assembly 'Umbrella.Analyzers'` the moment anything reflects over a
decorated type — ASP.NET Core building model metadata during `MapControllers`, for instance. This failure is invisible
to `dotnet build` and `dotnet test`; only a `dotnet publish` output check or an actual deployment reveals it.

If the repo produces NuGet packages of its own, note that a global non-private reference becomes a public dependency of
those packages. That is usually acceptable (the assembly is tiny and dependency-free), but if you need to avoid it, add
`<PackageReference Update="Umbrella.Analyzers.Abstractions" PrivateAssets="All" />` to the packable projects only —
never to a project that applies the attributes or to a deployed application.

## Step 2 — Install `Umbrella.DataAccess.Analyzers` per repository-implementation project

For each project identified in Discovery step 4, add directly to that project's `.csproj`:

```xml
<PackageReference Include="Umbrella.DataAccess.Analyzers" Version="{{resolvedVersion}}" PrivateAssets="All" />
```

Do not add this to `Directory.Packages.props` and do not add it to domain/entity-only projects.

## Step 3 — Install `Umbrella.WebUtilities.DynamicImage.Analyzers` per Dynamic Image project

For each project identified in Discovery step 5, add directly to that project's `.csproj`:

```xml
<PackageReference Include="Umbrella.WebUtilities.DynamicImage.Analyzers" Version="{{resolvedVersion}}" PrivateAssets="All" />
```

This is independent of the `UmbrellaDynamicImageEnableUrlFingerprinting` MSBuild property — that property (when the repo uses URL fingerprinting) is typically set once, repo-wide, in `Directory.Build.props`, and is unrelated to which projects carry the analyzer package itself. Do not conflate the two: setting the property is out of scope for this skill unless the user explicitly asks for it.

## Analyzer compatibility

Before finishing, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` so you know what each rule actually checks, then build the whole solution.

## Verification

1. Every `Umbrella.Analyzers` / `Umbrella.Utilities.Mapping.Mapperly.Analyzers` reference lives in the shared injection file (or the CPM equivalent), not duplicated into individual projects.
2. Every `Umbrella.DataAccess.Analyzers` reference is in a project with a `Repositories\` folder and a concrete data-access implementation package — list the exact projects you added it to.
3. Every `Umbrella.WebUtilities.DynamicImage.Analyzers` reference is in a project with genuine Razor/Blazor Dynamic Image usage or paired `*Url`/`*VersionToken` assignment — list the exact projects you added it to, and separately list any project you considered but excluded, with the reason.
4. `dotnet build` the solution. New diagnostics from these analyzers are expected on a first install into an existing codebase — report them grouped by rule ID and file, but do not silently fix or suppress them as part of this skill; that is separate follow-up work the user should triage.
5. No project ended up with a duplicate `PackageReference` for the same analyzer (e.g. once in `Directory.Packages.props` and again locally).
6. `Umbrella.Analyzers.Abstractions` carries no `PrivateAssets` anywhere it is needed. If the repo has a deployable app project, run `dotnet publish` on it and confirm `Umbrella.Analyzers.Abstractions.dll` is present in the publish output and `Umbrella.Analyzers.dll` is absent. A green build is not evidence — this specific defect only manifests at publish/runtime.
