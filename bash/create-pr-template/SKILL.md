---
name: create-pr-template
description: >
  Pull Request description template for creating clear, structured PR
  descriptions. Use when writing PR descriptions to ensure consistent
  formatting across the team.
---

# Pull Request Description Template

Use this template when creating PR descriptions:

After drafting the PR description, use the `show-me` skill to present it.

````markdown
# Description

{Summary of what changed and why - 2-3 sentences explaining the problem and solution}

{If an issue tracker ticket exists: [TICKET-ID](link-to-ticket)}

## What's Changed
- Added: {New functionality with context}
- Updated: {Modified behavior with rationale}
- Fixed: {Bug fixes with issue description}
- Removed: {Deprecated code with reason}

````

## Template Variables

Replace these placeholders with actual values:

- {Summary of what changed and why} - Brief explanation of the change
- {New functionality with context} - What was added
- {Modified behavior with rationale} - What was changed and why
- {Bug fixes with issue description} - What was fixed
- {Deprecated code with reason} - What was removed
- {Expected result} - What should happen
- {New env vars needed} - Environment variable requirements
- {New packages added} - Dependency additions
- {New routes added} - New application routes

## Entity Framework Migrations

If the PR includes Entity Framework migrations and the project uses `dotnet ef`, extract the raw SQL for every migration applied using the `dotnet ef migrations script` CLI. Include the generated SQL in a `## Migrations` section of the PR description.

Do **not** use `dotnet ef migrations add` or any scaffolding command — only generate the SQL script from already-applied migrations.

Run this from the repository root:

```bash
dotnet ef migrations script \
    --startup-project src/MyApp.Api \
    --project src/MyApp.Infrastructure \
    --output src/MyApp.Infrastructure/Migrations/output.sql
```

Replace:
- `src/MyApp.Api` → your startup project (the one with `Program.cs` / `DbContext` registration)
- `src/MyApp.Infrastructure` → the project containing the `.cs` migration files
- `src/MyApp.Infrastructure/Migrations/output.sql` → where the generated SQL file is saved

After the command completes, read the output file and paste its contents into a `## Migrations` section:

```markdown
## Migrations

```sql
-- paste generated SQL here
```
```

If the migration is empty (no model changes), note that instead of including a blank file.

> **Important:** This is a read-only extraction. Never modify migration `.cs` files or create new migrations as part of PR generation.
