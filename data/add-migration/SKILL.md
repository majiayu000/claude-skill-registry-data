---
name: add-migration
description: "Generate a new EF Core migration for Skoleoverblikket. USE THIS SKILL when the user says 'add migration', 'create migration', 'generate migration', 'ef migration', or after model/entity changes that need a schema update. Never modify existing migration files."
---

# Add Migration Skill

Generates a new EF Core migration and verifies the result.

## Project paths

- **API project**: `api/Skoleoverblikket.Api/Skoleoverblikket.Api.csproj`
- **Migrations folder**: `api/Skoleoverblikket.Api/Data/Migrations/`
- **DbContext**: `AppDbContext` in `api/Skoleoverblikket.Api/Data/`

## Steps

### 1. Confirm migration name

If the user did not provide a name, ask for one. Migration names must be PascalCase and describe the schema change — e.g. `Add_Course_Category`, `Remove_Staff_Slug`, `Add_SchemaDateRange`.

### 2. Run the migration script

Always use the repo script — it adds the migration AND regenerates `migration_script.sql` atomically:

```powershell
.\scripts\add-migration.ps1 -MigrationName <MigrationName>
```

Never call `dotnet ef` directly for this task. The script handles both steps and exits non-zero on failure.

### 3. Verify output

After the script succeeds, check that:

- Two new files exist: `<timestamp>_<Name>.cs` and `<timestamp>_<Name>.Designer.cs`
- `AppDbContextModelSnapshot.cs` was updated
- `migration_script.sql` contains the new migration ID at the bottom
- The migration `Up()` method contains the expected SQL operations — read it and confirm with the user if the changes look unexpected

### 4. Build to confirm no compile errors

```powershell
dotnet build api/Skoleoverblikket.Api/Skoleoverblikket.Api.csproj --configuration Release
```

## Rules

- **Never modify an existing migration file** — if a migration needs changing, add a new one
- **Never run `dotnet ef database update` in CI or production** — migrations are applied via `migration_script.sql` in the CI pipeline
- If the migration is empty (no `Up()` body), the model change was not registered — check that the entity has a corresponding `IEntityTypeConfiguration<T>` and is picked up by `ApplyConfigurationsFromAssembly`
- If `dotnet ef` is not installed, run: `dotnet tool install --global dotnet-ef`
