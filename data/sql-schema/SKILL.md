---
name: sql-schema
description: Database Architect skill. Use this when you need to modify the database schema, add tables, or seed data. This project uses RAW SQL SCRIPTS orchestrated by .NET Aspire, NOT Entity Framework Migrations.
---

# SQL Schema Management Skill

## Overview

MoreSpeakers.com uses a "Script-Load" pattern via .NET Aspire (`MoreSpeakers.AppHost`) to initialize the SQL Server container. We **DO NOT** use `dotnet ef migrations`.

## Source of Truth

The database schema is defined in `scripts/database/`.

## Workflow

### 1. Identify the Change
Determine if you need a new table, a modified column, or new seed data.

### 2. Locate the Loading Logic
Check `src/MoreSpeakers.AppHost/AppHost.cs`. Look for the `sqlText` concatenation logic:

```csharp
var sqlText = string.Concat(
    File.ReadAllText(Path.Combine(path, @"../../scripts/database/create-database.sql")),
    " ",
    File.ReadAllText(Path.Combine(path, @"../../scripts/database/create-tables.sql")),
    // ... other files
);
```

### 3. Apply the Change

**Option A: Modify Existing Files (Preferred for clean slate)**
-   If adding a core table, add T-SQL to `scripts/database/create-tables.sql`.
-   If adding a view, use `scripts/database/create-views.sql`.

**Option B: Create New Script (For specific updates)**
1.  Create a new file, e.g., `scripts/database/update-schema-features.sql`.
2.  **CRITICAL**: You MUST update `AppHost.cs` to include this new file in the `string.Concat` list, or it will be ignored.

### 4. Writing SQL

-   **Idempotency**: Always write idempotent SQL. The script may run on container startup.
    ```sql
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'MyTable')
    BEGIN
        CREATE TABLE MyTable (...)
    END
    ```
-   **Foreign Keys**: Ensure referenced tables are created *before* the table defining the key (check file order in `AppHost.cs`).

### 5. Verification
-   Run `dotnet run --project src/MoreSpeakers.AppHost`.
-   The container will spin up and execute the concatenated SQL script.

## PROHIBITED ACTIONS

-   ❌ `dotnet ef migrations add`
-   ❌ `dotnet ef database update`
-   ❌ Modifying the DbContext `OnModelCreating` without adding corresponding SQL scripts.
