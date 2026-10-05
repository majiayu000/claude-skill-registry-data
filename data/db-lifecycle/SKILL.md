---
name: "db-lifecycle"
description: "Use when a developer needs to check migration status, run migrations, seed data, or start the application. Trigger phrases: migration status, run migrations, apply migrations, seed database, seed data, start app, run app, pending migrations, EF migrations, database setup, db lifecycle."
argument-hint: "Specify which operation: check-status, run-migrations, seed-data, or run-app."
user-invocable: true
---

## Instructions

Read the full database lifecycle guide at `.github/prompts/db-lifecycle.prompt.md` and follow all instructions, commands, and known-error resolutions defined there.

The `.github/prompts/db-lifecycle.prompt.md` file is the single source of truth for database lifecycle operations and is shared with GitHub Copilot. Do not duplicate its content here.

## Operations

The guide covers four operations:

- **A — Check migration status**: List defined migrations and inspect which are applied against the live database.
- **B — Run migrations**: Apply pending migrations automatically (via AppHost startup) or manually via `dotnet ef database update`.
- **C — Seed data**: Trigger automatic seeding on first startup, or force a re-seed by truncating target tables.
- **D — Run the app**: Start the full stack with `dotnet run --project src/eShop.AppHost/eShop.AppHost.csproj`.

## User Input

```text
$ARGUMENTS
```

Use the user input to determine which operation to focus on. If empty, present all four operations and ask which the user needs.
