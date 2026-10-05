---
name: umbrella-nuget-safe-upgrade
description: 'Safely analyze and apply NuGet package upgrades in multi-targeted .NET repositories using exclusions, framework-aware version selection, restore checks, and transitive dependency graph validation.'
---

# NuGet Safe Upgrade

## Purpose

This skill safely analyzes and applies NuGet package upgrades while respecting exclusions, framework-coupling rules, and transitive dependency graph constraints.

## Assets

- `scripts\Invoke-NuGetSafeUpgrade.ps1`
- `scripts\NuGetSafeUpgrade.Common.ps1`
- `scripts\Test-NuGetSafeUpgrade.Common.ps1`
- `nuget-upgrade-exclusions.schema.json`

## Inputs

- optional package IDs to limit scope
- optional project paths to limit scope
- repository root or current working directory
- root-level `nuget-upgrade-exclusions.json`

## Workflow

1. Read `nuget-upgrade-exclusions.json`.
2. Run the wrapper script in `{{skill_dir}}\umbrella-nuget-safe-upgrade\scripts\`.
3. Start in Analyze mode unless the user explicitly requested direct application.
4. Filter scope by package IDs or project paths if provided.
5. Let the shared implementation select the highest safe candidate version for each package.
6. Keep only changes that pass restore and transitive graph checks.
7. Return successful, skipped, and blocked packages with override guidance.
8. After each Apply pass, check the blocked list for lockstep family packages and run a second Apply pass if any are present.
9. After the final Apply pass, run `dotnet build <solutionPath>` and verify the solution builds cleanly. Report any build failures before declaring the upgrade complete.

## Legacy TFM version pinning

Packages listed in `frameworkCoupledFamilies` (in `nuget-upgrade-exclusions.json`) are capped at the target framework's major version for net5+ TFMs. For legacy TFMs (`netstandard*`, `net4*`), the cap is the package's *current* major version — preventing inadvertent upgrades that pull in transitive dependencies from a newer runtime generation.

`System.Text.Json` and `System.Net.Http.Json` are included in `frameworkCoupledFamilies` for this reason: on `netstandard2.0`/`net462` they must stay at their current 6.x baseline and must not be upgraded to 10.x.

`Microsoft.Extensions.Caching.Hybrid` is covered by the existing `Microsoft.Extensions.` family prefix. Keep its version framework-coupled: .NET 9 references stay on the 9.x line while .NET 10 references track the 10.x line.

`Microsoft.Maui.` packages follow the same contract and must also appear in `frameworkCoupledFamilies`. More generally, any SDK family whose major version must match the target framework's major (MAUI, ASP.NET Core, EF Core, etc.) belongs in this list. If you encounter an already-conditional reference that was upgraded to a version whose major exceeds the condition TFM's major, that family is missing from `frameworkCoupledFamilies` — add it to `nuget-upgrade-exclusions.json` before re-running.

A cap that applies to only *some* of a project's TFMs does not block the upgrade outright: the capped TFMs keep the current version and the remaining TFMs are upgraded, via the framework split described below. An unconditional reference in a multi-targeted project therefore becomes per-TFM conditional blocks on first upgrade — each tracking its own major thereafter.

## Framework-split upgrades

When a package upgrade is blocked on some TFMs but would be safe on others, the script automatically splits the single unconditional `<PackageReference>` into per-framework conditional `<ItemGroup>` blocks:

- **Blocked TFMs** keep the current version (e.g., `netstandard2.0`/`net8.0`/`net9.0` when the new version pulls v10 transitive deps, bumps the package major, or exceeds the coupled-family cap for that TFM).
- **Allowed TFMs** receive the upgraded version (e.g., `net10.0`).

Split candidates appear in the `successful` list with action `Analyzed (split candidate)` or `Applied (split by framework)` and include `upgradeFrameworks`/`keepFrameworks` fields.

Split only applies to unconditional `PackageReference` items directly in `.csproj` files. `PackageVersion` entries in `Directory.Packages.props` and already-conditional references are not split.

For Central Package Management, each `PackageVersion` condition is evaluated against the consuming project's `TargetFramework` and `MSBuildProjectName`. Only matching project/framework pairs are validated, and the exact centralized item is updated even when multiple conditional entries share a package ID and version.

**TFM ordering:** Condition strings and `<ItemGroup>` blocks are written in ascending semantic order: `netstandard*` (lowest) → `net4*` → `net5+` (ascending by major version). Lower TFMs always appear first in the file, matching conventional `.csproj` reading order.

**Legacy-TFM major-version guard:** For `netstandard*` and `net4*` TFMs any candidate that bumps the package's major version is automatically added to the blocked set — the same as a transitive-graph violation on `net5+` TFMs. This prevents a major upgrade from silently pulling in runtime dependencies that only ship on newer .NET targets. Use `-OverrideBlockedPackageId` to bypass after manual verification.

## Lockstep package families

Some packages must be upgraded together — for example `System.Composition.AttributedModel`, `System.Composition.Runtime`, and `System.Composition.TypedParts` all share the same version number and each member pulls the others transitively.

The script processes packages independently, so when it tests a family member in isolation the siblings have already been reverted (Analyze) or not yet written (Apply). This produces a NU1605 blocked result:

```
Candidate X.Y.Z failed restore: Detected package downgrade: <SiblingPackage> from X.Y.Z to <OldVersion>
```

**How to identify:** a blocked package's NU1605 error references sibling packages that appear in the *successful* list of the same report, upgraded to the same candidate version.

**How to resolve:** in Apply mode no action is needed — siblings are written to disk before each subsequent package is tested, so the family resolves in a single Apply pass. In Analyze mode the blocked entry is expected; proceed directly to Apply.

## Command examples

Analyze:

```powershell
powershell -ExecutionPolicy Bypass -File {{skill_dir}}\umbrella-nuget-safe-upgrade\scripts\Invoke-NuGetSafeUpgrade.ps1 -Mode Analyze
```

Apply:

```powershell
powershell -ExecutionPolicy Bypass -File {{skill_dir}}\umbrella-nuget-safe-upgrade\scripts\Invoke-NuGetSafeUpgrade.ps1 -Mode Apply
```

Override a blocked package after review:

```powershell
powershell -ExecutionPolicy Bypass -File {{skill_dir}}\umbrella-nuget-safe-upgrade\scripts\Invoke-NuGetSafeUpgrade.ps1 -Mode Apply -PackageId Microsoft.Extensions.Logging.Abstractions -OverrideBlockedPackageId Microsoft.Extensions.Logging.Abstractions
```

## Output expectations

- `successful`: packages safely upgraded or safe upgrade candidates in Analyze mode
- `skipped`: packages excluded or with no newer safe version
- `blocked`: packages that failed compatibility or graph checks
- `options`: the requested package/project filters, prerelease setting, and explicit blocked-package overrides; each blocked item also contains safe follow-up commands

## Safety rules

- Never ignore `nuget-upgrade-exclusions.json`.
- Never flatten framework-specific versions into a single package version.
- Never keep a candidate that fails restore.
- Never treat a NuGet source/query failure as evidence that no newer versions exist; stop and surface the failure.
- Never keep a candidate that resolves framework-coupled package families beyond the target framework major unless explicitly overridden.
- Always verify that already-conditional package references are upgraded to a version compatible with their condition's TFM. If a package family is TFM-version-coupled but absent from `frameworkCoupledFamilies`, add it before applying upgrades.
- Never declare an Apply pass complete without running `dotnet build` to confirm the solution compiles cleanly.
- Keep reusable logic in `.ai-shared\` and keep this folder as a thin wrapper.
