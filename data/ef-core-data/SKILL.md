---
name: ef-core-data
description: >-
  EF Core in an Umbraco package: one model for SQL Server and SQLite, prefixed migrations,
  internal repositories, query shape for large tables, and testing against a real database.
  Use when designing or reviewing a package's entities, migrations or repositories.

---

# EF Core data for Umbraco packages

EF Core is the recommended approach for a new Umbraco package's persistence. NPoco in older
code is legacy, not a coequal choice. When adding to an existing NPoco codebase, match its
convention rather than adding a second persistence technology for one feature. For anything
new, use EF Core and the conventions below.

## *🎯 Why: Design for Change*

A package's tables usually share a database with Umbraco core and every other installed
package. These conventions keep a schema change local to your package and keep persistence
changes from breaking the rest of the codebase.

## One entity model, two providers

Sites run Umbraco on SQL Server or SQLite. A package tested against only one will break
installs on the other. Write provider-agnostic entities and LINQ, and handle what differs:

- String comparison case-sensitivity (SQLite is case-sensitive by default for `=`;
  SQL Server usually isn't, depending on collation). Don't rely on either — compare
  explicitly (`.ToLower()` on both sides, or a configured case-insensitive collation) if it
  matters.
- `DateTime` vs `DateTimeOffset` handling differs between providers. Pick one and use it
  across the whole entity model.
- Some provider-specific string/date functions don't translate on the other provider — the
  usual cause when a LINQ query throws on only one. Test against both, not just the local one.

```csharp
// Provider-agnostic — translates cleanly on both providers
var recent = await _dbSet
    .Where(x => x.CreatedUtc >= cutoff)
    .OrderByDescending(x => x.CreatedUtc)
    .ToListAsync(cancellationToken);
```

## Migrations: generated per provider, prefixed to avoid collisions

Every migration name **must** be prefixed with a short, unique product/package name.
Otherwise two packages can collide in the migration history table or in object names:

```bash
# SQL Server
dotnet ef migrations add MyPackage_InitialCreate \
  -p src/MyPackage.Persistence.SqlServer -c MyPackageDbContext --output-dir Migrations

# SQLite
dotnet ef migrations add MyPackage_InitialCreate \
  -p src/MyPackage.Persistence.Sqlite -c MyPackageDbContext --output-dir Migrations
```

Both providers share one entity model but get **separate, independently generated**
migrations. A schema change is not done until both are regenerated and committed. A reviewer
treats "SQL Server migration added, SQLite migration missing" as an automatic finding, not a
follow-up.

Pick your package's prefix once and use it for every migration, forever — changing it later
breaks collision-avoidance for anything migrated under the old name.

### Porting a migration to another version line

When a package keeps one branch per CMS major and a schema change goes to more than one line,
**copy the migration files as they are**. Never run `dotnet ef migrations add` again on the
other line. Copy each provider's `<timestamp>_<Name>.cs`, its `.Designer.cs`, and the model
snapshot change, and keep the same `[Migration("...")]` ID.

EF records applied migrations by ID. If two lines use different IDs for the same change, a
site upgrading from the older line doesn't find the newer line's ID in its history, runs the
migration again, and fails on schema that already exists (SQL Server error 2705, "Column
names in each table must be unique"; SQLite reports a duplicate column). Every later
migration for the package then stops at startup.

- Before merging a port, list the migration file names for each provider on both lines and
  diff them. They must be identical.
- If different IDs have already shipped, don't rename the shipped files. Map the older line's
  ID to the newer line's in the migration history table before migrating, so the newer line
  sees the change as already applied.

## Repository pattern: internal to the owning service

`umbraco-package-conventions` states this rule generally; this is the EF Core half. The
`DbContext` and every repository built on it are `internal` to the persistence assembly by
default (that skill covers the one exception: a specific, nameable reason for a `public`
repository):

```
Controller / other service ──▶ EntityService ──▶ EntityRepository (internal) ──▶ DbContext (internal)
```

Repository methods use short forms with the entity implicit — `GetByIdAsync`,
`GetByAliasAsync`, `GetAllAsync`, `AddAsync`, `UpdateAsync`, `DeleteAsync` — the class name
already names the entity. A `DbContext` reference (or repository interface) leaking into
`Web`/`Api` project code is a design smell: schema changes can no longer stay local to the
persistence layer.

## Query shape: read only what you need

A package's tables grow on the sites that install it, not on the demo site. Write repository
queries for the big table:

- **`AsNoTracking()` for reads.** Change tracking costs memory and time per row, and a
  read-only query never uses it.
- **Project to what the caller needs.** `.Select(x => new ItemSummary(x.Id, x.Name))` reads
  two columns; returning the entity reads all of them, including large text columns.
- **One query, not one per row.** A query inside a `foreach`, or a navigation property read
  per item, is one round trip per row. Load related data in the same query (`.Include()`,
  or a projection that reaches into it), or batch the keys into one `Where(x =>
  keys.Contains(x.Id))`.
- **Page in the database.** `OrderBy` then `Skip`/`Take` on the `IQueryable`, before
  `ToListAsync`. Paging after materializing loads the whole table first.
- **Index what you filter and sort on.** A column used in a list screen's `Where` or
  `OrderBy` gets an index in the entity configuration, in both providers' migrations.

```csharp
var page = await _dbSet
    .AsNoTracking()
    .Where(x => x.OwnerKey == ownerKey)
    .OrderByDescending(x => x.CreatedUtc)
    .Skip(skip)
    .Take(take)
    .Select(x => new ItemSummary(x.Id, x.Name, x.CreatedUtc))
    .ToListAsync(cancellationToken);
```

For caching and Umbraco-side performance, see `umbraco-performance`.

## Testing repositories against a real database, not a fake

EF Core's `InMemory` provider does **not** generate real SQL. It will pass queries a real
database rejects (an invalid `GroupBy`, an untranslatable `Where`, a broken migration),
hiding exactly the bugs repository tests exist to catch.

Use a real in-memory SQLite database, which exercises SQL translation and applied
migrations:

```csharp
public sealed class EFCoreTestFixture : IDisposable
{
    private readonly SqliteConnection _connection;
    public MyPackageDbContext Context { get; }

    public EFCoreTestFixture()
    {
        // Keep the connection open for the fixture's lifetime — SQLite's in-memory
        // database only exists while at least one connection holds it open.
        _connection = new SqliteConnection("DataSource=:memory:");
        _connection.Open();

        var options = new DbContextOptionsBuilder<MyPackageDbContext>()
            .UseSqlite(_connection)
            .Options;

        Context = new MyPackageDbContext(options);
        Context.Database.Migrate(); // exercises the real migrations, not just a fresh schema
    }

    public void Dispose()
    {
        Context.Dispose();
        _connection.Dispose();
    }
}
```

Use `Context.Database.Migrate()`, not `EnsureCreated()` — the latter skips migrations, so a
broken or missing migration passes tests and still breaks real installs. Build this fixture
once per package and share it (a `[OneTimeSetUp]` in NUnit, `IClassFixture<T>` in xUnit)
across every repository test.

## SQLite tests don't prove SQL Server

The fixture above only runs SQLite. A SQL Server migration that was read but never applied
is not tested: column types, defaults, index names and generated SQL all differ between
providers. When a change adds or edits a migration and the project supports SQL Server,
apply it to a real SQL Server before calling the work done:

- A throwaway container, e.g. `mcr.microsoft.com/mssql/server:2022-latest` in Docker, with the
  demo site's connection string pointed at it. Keep the password out of committed settings
  (user secrets or an environment variable).
- Or the project's own SQL Server dev database, if it has one.

Start the site so Umbraco runs the migrations, check the tables are there, and do one real
read and write through the feature. If no SQL Server is available, say so in the build log and
the PR ("SQL Server migration read, not run"). Never imply it was tested.

## Schema conventions worth defaulting to

- **Surrogate keys** (`Guid` or `int` primary keys), not natural keys — an alias or slug can
  need to change; a surrogate key never does.
- **Explicit `NOT NULL` foreign keys** unless the relationship is genuinely optional. An
  optional FK is a deliberate, documented decision, not a forgotten `.IsRequired()`.
- **Soft-delete vs. hard-delete is a per-entity decision**, not a blanket default. Decide it
  in the `feature-design` phase and record the *why* (audit requirements, referential integrity
  from other entities, GDPR erasure obligations), not whichever is less code.
- **Keep entity classes free of Umbraco CMS framework dependencies** where possible, so they
  stay testable without a running Umbraco instance.
