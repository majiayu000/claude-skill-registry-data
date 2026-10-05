---
name: umbrella-dotnet-add-ef-migration
description: 'Add an EF Core database migration with auto-detection of the migrations project, startup project, and DbContext. Reports generated and modified files and warns on empty migrations.'
---

# dotnet Add EF Core Migration

## Purpose

This skill adds EF Core migrations consistently without running `dotnet ef migrations add` by hand.

## Assets

- `scripts\Invoke-AddEfMigration.ps1`

## Inputs

- `-MigrationName` (required) — name for the new migration; use semantic versioning to match existing migrations (e.g. `1.0.20`)
- `-RepoRoot` (optional) — defaults to git repository root
- `-MigrationsProject` (optional) — relative path to the `.Migrations.csproj`; auto-detected if omitted
- `-StartupProject` (optional) — relative path to the Web SDK startup `.csproj`; auto-detected if omitted
- `-Context` (optional) — DbContext class name; auto-detected via `dotnet ef dbcontext list` if omitted

## Migration naming convention

Migration names must use semantic versioning to match the existing migration history (e.g. `1.0.20`). Before running the script, inspect the existing files in the `Migrations` folder to find the current highest version and use the next increment.

## Workflow

1. Inspect the `Migrations` folder to determine the current highest version number.
2. Confirm the next migration name with the user if it is not already provided.
3. Run the wrapper script with `-MigrationName`.
4. The shared script auto-detects the migrations project, startup project, and DbContext from current `dotnet ef --json` output, then normalizes whitespace and applies the repository's IDE0005/IDE0058/IDE0161 generated-migration style.
5. Report the new and modified files returned by the script.
6. If the script warns that the migration is empty, stop and ask the user to verify their entity model changes are saved before proceeding.
7. Remind the user to review the migration content and commit once confirmed.

## Command examples

Add a migration (auto-detected projects):

```powershell
powershell -ExecutionPolicy Bypass -File .claude\skills\umbrella-dotnet-add-ef-migration\scripts\Invoke-AddEfMigration.ps1 -MigrationName 1.0.20
```

Add a migration (explicit projects):

```powershell
powershell -ExecutionPolicy Bypass -File .claude\skills\umbrella-dotnet-add-ef-migration\scripts\Invoke-AddEfMigration.ps1 `
    -MigrationName 1.0.20 `
    -MigrationsProject "Core\MyApp.Core.Data.Migrations\MyApp.Core.Data.Migrations.csproj" `
    -StartupProject "Web\MyApp.Web.Server\MyApp.Web.Server.csproj" `
    -Context MyAppDbContext
```

## Output expectations

- `New files:` — the `.cs` and `.Designer.cs` migration files
- `Modified files:` — the `*ModelSnapshot.cs` file
- Warning if the migration body contains no `migrationBuilder` calls

## Analyzer compatibility

Before finishing, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build the affected projects with their installed analyzers enabled. Treat diagnostics introduced by the generated or changed code as defects in this workflow.

## Safety rules

- Never run `dotnet ef migrations add` directly.
- Always verify the migration is non-empty before committing.
- Keep reusable logic in `.ai-shared\` and keep this folder as a thin wrapper.
