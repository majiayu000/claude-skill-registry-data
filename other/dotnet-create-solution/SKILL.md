---
name: dotnet-create-solution
description: 'Scaffold a .NET solution with src/test layout, Central Package Management, Directory.Build.props and .editorconfig for libraries or apps. Use when starting a .NET solution.'
disable-model-invocation: true
metadata:
  opencode/autoinvoke: 'false'
---

Scaffold a new .NET solution with the standard project structure. Paths to `scripts/` and `templates/` are relative to this skill's directory.

## Stack

- `dotnet` SDK, `.slnx` solution format, NuGet via Central Package Management (`Directory.Packages.props`)
- `pwsh` for the scaffold script

## Steps

1. **Ask first:** solution name; **Library** (NuGet package, multi-target `net10.0;net9.0;net8.0`) or **Application** (single `net10.0`); project template (classlib / webapi / worker / console / grpc); additional NuGet packages
2. **Run the scaffold script:**

   ```powershell
   pwsh scripts/New-Solution.ps1 -SolutionName <Name> -ProjectType <template> -OutputType <library|app> [-UpdatePackages]
   ```

   It creates the directory structure and `.slnx`, generates source and test projects, strips redundant properties from the `.csproj` files, copies all templates (including the matching CI workflow), optionally updates `Directory.Packages.props` to the latest versions, and runs `dotnet build`.
3. Add any additional packages to `Directory.Packages.props` and reference them without `Version` in the `.csproj`
4. Run `dotnet build` to verify

Parameters: `-SolutionName` (required), `-ProjectType` (classlib/console/webapi/worker/grpc), `-OutputType` (library/app), `-UpdatePackages` (switch), `-OutputDirectory`

## Templates

| File                               | Purpose                                                                                                                                                                                  |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Directory.Build.props`            | Shared MSBuild: `LangVersion=Latest`, `GenerateDocumentationFile`, `NoWarn`; multi-target for libraries, single `<TargetFramework>` for apps                                             |
| `Directory.Packages.props`         | CPM stub with the NUnit, NUnit.Analyzers, NSubstitute, Shouldly and coverlet test packages plus `Microsoft.SourceLink.GitHub`                                                            |
| `src/Directory.Build.props`        | Imports root props, sets `OutputPath`                                                                                                                                                    |
| `test/Directory.Build.props`       | Imports root, `IsPackable=false`, test `PackageReference`s without versions, global `Using NUnit.Framework`                                                                              |
| `.editorconfig`                    | From `project-setup` (`templates/dotnet.editorconfig`; its warning when not installed): C# style: file-scoped namespaces, primary constructors, `_camelCase` fields, analyzer severities |
| `.github/workflows/ci-library.yml` | NuGet library CI via the `GravionLabs/ci` reusable workflow (build, test, pack, publish)                                                                                                 |
| `.github/workflows/ci-app.yml`     | Application CI: `dotnet build` + `dotnet test` with test results reporter                                                                                                                |

## Constraints

- `.slnx` format only; avoid legacy `.sln`
- All package versions live in `Directory.Packages.props`, never in individual `.csproj` files
- Generated `.csproj` files must not repeat properties already in `Directory.Build.props`
- Libraries multi-target; applications use a single target framework
- The solution must build cleanly before the task is complete
- Workflows reference `GravionLabs/ci` at the major tag `@v<major>` (today `@v1`), never `@main` or a commit SHA; third-party actions stay SHA-pinned where the repository requires it

Report: summary, files created, verify command (`dotnet build`).
