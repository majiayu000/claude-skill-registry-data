---
name: dotnet-update-packages
description: Use when user mentions updating NuGet packages, checking for outdated dependencies, upgrading .NET package versions, or asks about package updates in a .NET project.
---

# .NET Package Updates

## When to Use

This skill applies when the user:
- Asks about outdated NuGet packages
- Wants to update dependencies in a .NET project
- Mentions package version upgrades
- Discusses dependency management in .NET

## Workflow

1. **List outdated packages** (including transitive) using:
   ```bash
   dotnet package list --outdated --include-transitive --format json
   ```

2. **Parse output** to identify:
   - Projects with outdated packages
   - Whether each package is **direct** or **transitive**

3. **Analyze project dependencies** by reading `<ProjectReference>` elements in each csproj

4. **Present findings** in a readable format showing project, package name, current → latest version

5. **Confirm with user** before making changes

6. **Update packages per project** with `--project` parameter:
   - Update leaf projects first (no dependencies)
   - Then update dependent projects
   - Independent branches can run in parallel
   ```bash
   dotnet package update <package> --project <path-to-csproj>
   ```

7. **Verify** with `dotnet build`

8. **If build fails**, ask user:
   - Fix automatically (review errors, apply fixes)
   - Fix manually (show errors, let user handle)

## Key Commands

| Command | Purpose |
|---------|---------|
| `dotnet package list --outdated --include-transitive --format json` | List outdated packages (incl. transitive) |
| `dotnet package update <name> --project <path>` | Update specific package in project |
| `dotnet package update --project <path>` | Update all packages in project |

## Transitive vs Direct Packages

- **Direct**: Explicitly in csproj. Update directly.
- **Transitive**: Pulled in by dependencies. Marked `[T]` in output.
  - To update: update the parent package, or add direct reference to pin version

## Notes

- Requires .NET 8+ SDK for `dotnet package update`
- Always use `--project` parameter to update per-project
- Update in dependency order: leaves first, then dependents
- Always confirm with user before updating
- Run build after updates to catch breaking changes
