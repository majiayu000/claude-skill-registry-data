---
name: ef-core
description: >
  Makes an EF Core model dual-provider for the dualdb tool - conditional
  UseSqlServer/UseNpgsql, per-provider mapping where types diverge, two migration
  sets, and the LINQ translations that change results. Use whenever you see
  DbContext, OnModelCreating, HasColumnType, HasDefaultValueSql, IsRowVersion,
  FromSqlRaw, a migration, or an EF Core LINQ query.
---

# EF Core

## When to use

Any `DbContext`, `IEntityTypeConfiguration<T>`, `OnModelCreating`, migration,
`UseSqlServer`, `FromSqlRaw`/`ExecuteSqlRaw`, value converter, or LINQ query that
reaches the database.

## Decision procedure

1. **One `DbContext`.** Never one per provider - the model is duplicated and the
   copies drift (`PG-ORM-001`).
2. Fork the provider at the single registration site: conditional
   `UseSqlServer` / `UseNpgsql`, driven by the provider switch.
3. Audit every `HasColumnType` (`PG-ORM-002`). Prefer a provider-neutral facet
   (`HasPrecision`, `HasMaxLength`) over a type name; fork on
   `Database.IsSqlServer()` / `IsNpgsql()` where a name is unavoidable; move
   heavily divergent entities into per-provider
   `IEntityTypeConfiguration<T>` implementations.
4. Audit every `HasDefaultValueSql` and `HasComputedColumnSql` (`PG-ORM-003`) -
   the strings inside are raw SQL and go through the Appendix A rules.
5. Resolve the concurrency token (`PG-TYPE-035`, `PG-TYPE-042`). `IsRowVersion`
   has no PostgreSQL equivalent. Pick one strategy for the whole model.
6. Two migration sets, separate assemblies or folders (`PG-ORM-004`). Every model
   change gets a migration in **every** set.
7. Audit LINQ: `StartsWith`/`Contains`/`EndsWith` (`PG-ORM-005`), `Skip`/`Take`
   without `OrderBy` (`PG-ORM-006`), `DateTime` arithmetic, `GroupBy`
   projections.
8. Treat every `FromSqlRaw`/`ExecuteSqlRaw` string as inline SQL (`PG-ORM-007`).
9. Configure PostgreSQL retry separately, including `40001` (`PG-ERR-002`).
10. Check value converters for `Guid`, `DateTime`, `bool` and enums - they may
    need per-provider variants.

## Rule table

<!-- dualdb:rules:begin categories=ef-core -->
<!-- generated from knowledge/rules/*.yaml by `dualdb rules sync` - do not edit -->

| id | SQL Server | PostgreSQL | tier | note |
|---|---|---|---|---|
| `PG-ORM-001` | `options.UseSqlServer(cs);` | `if (provider == DatabaseProvider.PostgreSql) options.UseNpgsql(csPg); else options.UseS...` | auto | `One DbContext, provider chosen at registration` |
| `PG-ORM-002` | `e.Property(x => x.Name).HasColumnType("nvarchar(200)");` | `e.Property(x => x.Name).HasColumnType( Database.IsNpgsql() ? "varchar(200)" : "nvarchar...` | review | `HasColumnType names a provider-specific type` |
| `PG-ORM-003` | `e.Property(x => x.ExternalRef).HasDefaultValueSql("NEWID()");` | `e.Property(x => x.ExternalRef).HasDefaultValueSql(Database.IsNpgsql() ? "gen_random_uui...` | review | `HasDefaultValueSql and HasComputedColumnSql contain raw SQL` |
| `PG-ORM-004` | `services.AddDbContext<AppContext>(o => o.UseSqlServer(cs));` | `o.UseNpgsql(cs, b => b.MigrationsAssembly("App.Migrations.PostgreSql")); // and Migrati...` | review | `A migration set per provider` |
| `PG-ORM-005` | `.Where(i => i.Name.StartsWith(prefix))` | `.Where(i => EF.Functions.ILike(i.Name, prefix + "%"))` | behaviour-risk | `LINQ StartsWith, Contains and EndsWith are collation-sensitive` |
| `PG-ORM-006` | `.Where(x => x.IsActive).Skip(20).Take(10).ToListAsync()` | `.Where(x => x.IsActive).OrderBy(x => x.Id).Skip(20).Take(10).ToListAsync()` | behaviour-risk | `Skip / Take without an OrderBy` |
| `PG-ORM-007` | `.FromSqlRaw("SELECT * FROM dbo.CatalogItem WHERE IsActive = 1")` | `.FromSqlRaw("SELECT * FROM dbo.\\"CatalogItem\\" WHERE \\"IsActive\\"")` | review | `FromSqlRaw and ExecuteSqlRaw are raw SQL` |

<!-- dualdb:rules:end -->

## Worked examples

### 1. `portable-rewrite` - a type name that did not need to be one

```csharp
e.Property(x => x.Price).HasColumnType("money");
```

becomes

```csharp
e.Property(x => x.Price).HasPrecision(19, 4);
```

Valid on both providers, produces `money` on SQL Server and `numeric(19,4)` on
PostgreSQL, and removes the fork rather than adding one. This is a genuine
`portable-rewrite`: the model configuration is shared code, the change is
provider-neutral, and there is no behaviour risk.

Note the contrast with `HasColumnType("nvarchar(200)")`, which has no neutral
facet with the same meaning and must be forked.

### 2. `add-pg-alternate` - the registration site

```csharp
services.AddDbContext<CatalogContext>((sp, options) =>
{
    var provider = sp.GetRequiredService<IDatabaseProviderAccessor>().Current;
    if (provider == DatabaseProvider.PostgreSql)
        options.UseNpgsql(config.GetConnectionString("AppDb_PostgreSql"),
                          npg => npg.EnableRetryOnFailure(3)
                                    .MigrationsAssembly("App.Migrations.PostgreSql"));
    else
        options.UseSqlServer(config.GetConnectionString("AppDb_SqlServer"),
                             sql => sql.EnableRetryOnFailure(3)
                                       .MigrationsAssembly("App.Migrations.SqlServer"));
});
```

This is the *only* provider conditional outside a dispatcher. Note that
`EnableRetryOnFailure` is per-provider: the SQL Server execution strategy does
nothing on Npgsql (`PG-ERR-002`).

### 3. `manual-review` - `IsRowVersion`

```csharp
e.Property(x => x.RowVersion).IsRowVersion();
```

`rowversion` has no PostgreSQL equivalent (`PG-TYPE-035`), and the three options
have genuinely different consequences:

- **`xmin`** - `e.UseXminAsConcurrencyToken()` on the Npgsql provider only. No
  schema change, automatically maintained; but the model now has a per-provider
  concurrency token, and `xmin` is a 32-bit transaction id that wraps.
- **An explicit `Version` column** - identical on both engines, so the fork
  disappears; costs a schema change and discipline in every update path.
- **`ModifiedUtc`** - cheapest, and genuinely weaker: two updates within the
  clock's resolution are indistinguishable.

No option is auto-picked. The entry goes to `MANUAL_REVIEW.md` with all three,
and whichever is chosen must be applied model-wide (`PG-TYPE-042`).

## Traps

- **`HasColumnType("datetime2")` fails at model build**, which is loud and fine.
  `DateTime.Kind` (`PG-DATE-008`) fails at *run time*, per value, and is not.
- **`.StartsWith(prefix)` translates to `LIKE`** and inherits the case-sensitivity
  change (`PG-ORM-005`). `EF.Functions.ILike` fixes it and is Npgsql-only, so the
  expression itself then needs a fork.
- **`Skip`/`Take` without `OrderBy`** (`PG-ORM-006`) is the LINQ form of
  `PG-ORD-005`: pages overlap or skip rows.
- **Migration drift** is the real risk in `PG-ORM-004`, not the initial split. A
  set that falls behind is a schema that diverges silently.
- **Generated index names exceed 63 bytes** routinely (`PG-IDENT-003`), and
  PostgreSQL truncates without warning.
- **`FromSqlRaw` looks provider-neutral** because the surrounding code is. It is
  not (`PG-ORM-007`).

## Escalate when

- A value converter's behaviour differs per provider and the model cannot express
  both.
- An entity needs a genuinely different key strategy per provider.
- A `GroupBy` projection translates on one provider and evaluates client-side on
  the other - that is a performance and semantics change, not a mapping.
- The concurrency-token choice cannot be made without the schema owner.

## Do not

- Do not create a second `DbContext`.
- Do not maintain one migration set and hand-edit its SQL.
- Do not enable a compatibility switch and move on - `PG-DATE-011` exists to stop
  exactly that.
- Do not "improve" a LINQ query while porting it.
- Do not introduce PostgreSQL arrays or native `enum` into the shared model.
