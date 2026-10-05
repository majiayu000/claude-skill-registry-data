---
name: nhibernate
description: >
  Makes an NHibernate application dual-provider for the dualdb tool - dialect and
  driver selection, .hbm.xml sql-type and generator review, and CreateSQLQuery as
  raw SQL. Use whenever you see NHibernate, ISession, ISessionFactory,
  MsSql20xxDialect, SqlClientDriver, an .hbm.xml mapping, or Fluent NHibernate
  configuration.
---

# NHibernate

The dialect swap is the easy part. The work is in the mappings.

## When to use

Any `ISession`, `ISessionFactory`, `Configuration`, `.hbm.xml`, Fluent NHibernate
`ClassMap`, `CreateSQLQuery`, or `hibernate.cfg.xml`.

## Decision procedure

1. Select dialect and driver from configuration, keyed by the same provider switch
   as everything else (`PG-ORM-011`):

   | | SQL Server | PostgreSQL |
   |---|---|---|
   | dialect | `MsSql2012Dialect` | `PostgreSQL83Dialect` or later |
   | driver | `SqlClientDriver` | `NpgsqlDriver` |

2. Audit every `sql-type` attribute in `.hbm.xml` - they name SQL Server types and
   go through the Appendix C rules.
3. Review the id generator strategy. `identity` and `native` resolve differently:
   PostgreSQL prefers sequence-backed generators, and `native` will pick one, which
   changes the generated DDL and the insert round-trip behaviour.
4. Treat every `CreateSQLQuery` as raw SQL (`PG-ORM-007` applies by analogy).
5. Review HQL that uses provider-specific functions - `registerFunction` entries
   and anything the dialect maps.
6. Check `<column>` names against the reserved-word list (`PG-IDENT-010`) and the
   63-byte limit (`PG-IDENT-003`).

## Rule table

<!-- dualdb:rules:begin categories=nhibernate -->
<!-- generated from knowledge/rules/*.yaml by `dualdb rules sync` - do not edit -->

| id | SQL Server | PostgreSQL | tier | note |
|---|---|---|---|---|
| `PG-ORM-011` | `<property name="dialect">NHibernate.Dialect.MsSql2012Dialect</property>` | `<property name="dialect">NHibernate.Dialect.PostgreSQL83Dialect</property>` | review | `NHibernate dialect and driver come from configuration` |

<!-- dualdb:rules:end -->

## Worked examples

### 1. `add-pg-alternate` - dialect and driver selection

```csharp
// original, unchanged
private static Configuration BuildSqlServer() => new Configuration()
    .DataBaseIntegration(db => {
        db.Dialect<MsSql2012Dialect>();
        db.Driver<SqlClientDriver>();
        db.ConnectionString = SqlServerConnectionString;
    });

// added
private static Configuration BuildPostgreSql() => new Configuration()
    .DataBaseIntegration(db => {
        db.Dialect<PostgreSQL83Dialect>();
        db.Driver<NpgsqlDriver>();
        db.ConnectionString = PostgreSqlConnectionString;
    });
```

The session factory is built once at startup from whichever the provider switch
selects. This is a registration site, not a query path, so it is the one place the
conditional belongs.

### 2. `add-pg-file` - a parallel mapping for a divergent entity

```xml
<!-- Order.hbm.xml, unchanged -->
<property name="Price" column="Price" type="Currency" sql-type="money" />
<id name="Id"><generator class="identity" /></id>
```

```xml
<!-- Order.PostgreSql.hbm.xml, added -->
<property name="Price" column="Price" type="Currency" sql-type="numeric(19,4)" />
<id name="Id">
  <generator class="sequence"><param name="sequence">order_id_seq</param></generator>
</id>
```

Two mapping files, selected with the dialect. Note the generator change is not
cosmetic: `sequence` fetches the value *before* the insert, so the entity has its
id earlier, which can change behaviour in code that batches or that inspects the
id during a flush.

### 3. `manual-review` - a `sql-type` with no clean target

```xml
<property name="RowVersion" column="RowVersion" type="BinaryBlob"
          sql-type="rowversion" generated="always" />
<version name="RowVersion" column="RowVersion" type="BinaryBlob" />
```

`rowversion` has no PostgreSQL equivalent (`PG-TYPE-035`), and NHibernate's
`<version>` element is load-bearing: it drives optimistic concurrency on every
update. The options - `xmin`, an explicit integer version, or a timestamp - each
change the mapping *and* the update SQL NHibernate generates.

`manual-review` with the three options. Whichever is chosen must be applied to
every versioned entity (`PG-TYPE-042`), because a per-entity mix means the
concurrency contract differs across the model.

## Traps

- **`native` is not stable across dialects.** It resolves to `identity` on SQL
  Server and typically to `sequence` on PostgreSQL, so the same mapping produces
  different DDL and different insert timing.
- **`CreateSQLQuery` results are read by column alias**, so they inherit the
  casing break (`PG-API-001`).
- **HQL is not fully portable.** Functions registered by the dialect differ, and
  an HQL expression that translated on `MsSql2012Dialect` may not on
  `PostgreSQL83Dialect`.
- **Schema export** (`SchemaExport`/`SchemaUpdate`) generates provider-specific
  DDL, so it is a second migration path that also needs two lineages.
- **`<column name="Order">`** is a reserved word on PostgreSQL and must be quoted
  with backticks in the mapping (NHibernate's escape) or renamed.

## Escalate when

- A `<version>` mapping exists (always - see example 3).
- A custom `IUserType` binds a provider-specific type or `SqlDbType`.
- `SchemaExport` is used to create the production schema - the two dialects
  generate materially different DDL and the divergence needs review, not
  regeneration.
- A dialect subclass overrides function registration.

## Do not

- Do not upgrade NHibernate, or migrate it to EF, as part of this port.
- Do not change the mapped column names to suit PostgreSQL conventions. Quote
  them instead; renaming needs `allow_schema_changes`.
- Do not rely on `SchemaUpdate` to reconcile the two schemas.
