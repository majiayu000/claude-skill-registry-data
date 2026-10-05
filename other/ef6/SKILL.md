---
name: ef6
description: >
  Makes an Entity Framework 6 application dual-provider for the dualdb tool -
  DbConfiguration and provider registration, connection injection, two migration
  lineages with distinct ContextKeys, and the .edmx problem. Use whenever you see
  EntityFramework 6, DbConfiguration, DbMigrationsConfiguration, Database.SqlQuery,
  ExecuteSqlCommand, an .edmx file, or an <entityFramework> config section.
---

# EF6

EF6 is harder than EF Core in one specific way: **provider registration failures
surface at run time, not at build.** The application compiles and then throws
"No Entity Framework provider found" on the first query.

## When to use

Any `DbContext` from `System.Data.Entity`, `DbConfiguration`,
`DbMigrationsConfiguration`, `Database.SqlQuery`, `ExecuteSqlCommand`, `.edmx`,
`<entityFramework>` or `<DbProviderFactories>` config sections.

## Decision procedure

1. Add `EntityFramework6.Npgsql`. Register **both** providers - via
   `DbConfiguration` (preferred) or via `<entityFramework>` plus
   `<DbProviderFactories>` (`PG-ORM-008`).
2. Give the context a constructor taking a `DbConnection` supplied by the factory,
   rather than a connection-string name. A string name re-couples the context to
   one provider.
3. Two migration lineages: `Migrations/SqlServer/` and `Migrations/PostgreSql/`,
   with **distinct `DbMigrationsConfiguration` types and distinct `ContextKey`s**
   (`PG-ORM-004`). `__MigrationHistory` records the ContextKey, so sharing one
   makes each provider think the other's migrations are already applied.
4. Audit `HasColumnType("datetime2"|"varchar"|"money"|"uniqueidentifier")` and
   `HasMaxLength` on text-ish columns (`PG-ORM-002`).
5. Review `HasDatabaseGeneratedOption` and `IsRowVersion()` (`PG-TYPE-035`).
6. Treat `Database.SqlQuery` and `ExecuteSqlCommand` as raw SQL (`PG-ORM-007`).
7. If there is an `.edmx`: `manual-review` (`PG-ORM-009`). There is no partial fix.

## Rule table

<!-- dualdb:rules:begin categories=ef6 -->
<!-- generated from knowledge/rules/*.yaml by `dualdb rules sync` - do not edit -->

| id | SQL Server | PostgreSQL | tier | note |
|---|---|---|---|---|
| `PG-ORM-008` | `public AppContext() : base("name=AppDb") { }` | `public AppContext(DbConnection connection) : base(connection, contextOwnsConnection: tr...` | review | `EF6 needs a DbConfiguration and provider registration per provider` |
| `PG-ORM-009` | `Model.edmx with Provider="System.Data.SqlClient"` | `Model.SqlServer.edmx and Model.PostgreSql.edmx` | manual | `An .edmx model is provider-specific` |

<!-- dualdb:rules:end -->

## Worked examples

### 1. `add-pg-alternate` - connection injection

```csharp
// original, unchanged
public AppContext() : base("name=AppDb") { }

// added
public AppContext(DbConnection connection) : base(connection, contextOwnsConnection: true) { }
```

The parameterless constructor stays for the SQL Server path and for the migrations
tooling, which needs it. The new constructor is what the factory uses. Callers are
updated at the composition root only.

### 2. `add-pg-file` - a second migration lineage

```csharp
// Migrations/PostgreSql/Configuration.cs
internal sealed class PostgreSqlConfiguration : DbMigrationsConfiguration<AppContext>
{
    public PostgreSqlConfiguration()
    {
        MigrationsDirectory = @"Migrations\PostgreSql";
        ContextKey = "App.Data.AppContext.PostgreSql";   // distinct - see below
        SetSqlGenerator("Npgsql", new NpgsqlMigrationSqlGenerator());
    }
}
```

The existing SQL Server configuration is untouched. The distinct `ContextKey` is
the part that is easy to miss and expensive to get wrong: `__MigrationHistory`
keys on it, so sharing one means each provider sees the other's rows and skips its
own migrations.

### 3. `manual-review` - an `.edmx` model

The SSDL section of an `.edmx` describes the store schema in provider terms, so one
`.edmx` cannot serve two providers (`PG-ORM-009`). Three options, all projects
rather than edits:

- **Two `.edmx` files.** Smallest immediate change, no code rewrite - and two
  designer-generated models to keep in step by hand, which is the drift risk the
  tool avoids everywhere else.
- **Convert to Code First.** Removes the problem properly and makes the mapping
  reviewable; a substantial one-off change to a working system, and Database First
  conventions do not always survive it.
- **Move that path to Dapper or ADO.NET.** Best where the `.edmx` covers a small,
  query-shaped area; unrealistic where it models the domain, and it loses change
  tracking.

The tool does not choose. It emits the entry with all three and the file list.

## Traps

- **Registration failures are runtime, not build.** The corpus test for EF6 must
  actually resolve a context per provider, not just compile.
- **A shared `ContextKey`** silently skips migrations. Nothing errors; the schema
  is just missing.
- **`Database.SqlQuery<T>` is raw SQL** and reads by column name, so it inherits
  the casing break (`PG-API-001`).
- **`.edmx` is not the only Database First artifact** - `.dbml` (LINQ to SQL) has
  the same problem and no PostgreSQL provider at all.
- **`IsRowVersion()`** in EF6 fluent config is the same `PG-TYPE-035` decision as
  in EF Core, with fewer provider hooks to express it.

## Escalate when

- An `.edmx` or `.dbml` is present (always).
- `DbConfiguration` is set by attribute or by `<entityFramework
  codeConfigurationType>` and the app has more than one context.
- Migrations were generated with `-IgnoreChanges` or hand-edited - the two
  lineages cannot be derived from the model alone.

## Do not

- Do not replace the parameterless constructor. Migrations tooling needs it.
- Do not remove the existing SqlClient provider entry when adding Npgsql - both
  are registered, side by side.
- Do not attempt one migration set for both providers.
- Do not upgrade EF6 to EF Core as part of this port. That is modernization.
