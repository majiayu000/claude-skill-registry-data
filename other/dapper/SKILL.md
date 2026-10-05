---
name: dapper
description: >
  Converts Dapper data access to a dual-provider shape for the dualdb tool. Use
  whenever you see Query, QueryAsync, Execute, QueryFirst, QuerySingle,
  QueryMultiple, DynamicParameters, a Dapper TypeHandler, or SQL passed to an
  IDbConnection extension method. Dapper adds no provider coupling of its own,
  which means it offers no protection either.
---

# Dapper

## When to use

Any `IDbConnection` extension call: `Query*`, `Execute*`, `QueryMultiple`, plus
`DynamicParameters`, `SqlMapper.AddTypeHandler`, and `CommandDefinition`.

## Decision procedure

1. Every Dapper call site is **raw SQL** (`PG-ORM-010`). Run the string through
   the full Appendix A and B rule set - being inside a Dapper call changes
   nothing.
2. Route the connection through the factory (`PG-API-007`).
3. `DynamicParameters` is portable with `@name` (`PG-PARAM-003`) - no placeholder
   migration is needed. Verify the edge cases: a parameter used twice, a name that
   prefixes another (`@id` with `@id2`), and `@` or `:` inside literals, casts,
   JSON operators or comments.
4. `QueryMultiple` is a MARS dependency (`PG-API-003`) - it needs splitting or
   buffering.
5. Under `identifier_style=snake`, set
   `DefaultTypeMap.MatchNamesWithUnderscores = true`.
6. Check custom `TypeHandler`s: one written against `SqlDbType` or a SQL Server
   value shape needs a per-provider variant.
7. Generated `IN` lists -> `= ANY(@ids)` (`PG-PARAM-001`). Dapper's own list
   expansion (`WHERE Id IN @ids`) works on both engines but expands to one
   parameter per element, so it still meets the SQL Server ceiling.

## Rule table

<!-- dualdb:rules:begin categories=dapper,parameters,ado-net -->
<!-- generated from knowledge/rules/*.yaml by `dualdb rules sync` - do not edit -->

| id | SQL Server | PostgreSQL | tier | note |
|---|---|---|---|---|
| `PG-API-001` | `SELECT CatalogItemId, Name FROM dbo.CatalogItem` | `SELECT "CatalogItemId", "Name" FROM dbo."CatalogItem"` | review | `PostgreSQL lowercases column labels unless the SELECT quotes them` |
| `PG-API-002` | `int id = (int)command.ExecuteScalar();` | `int id = Convert.ToInt32(command.ExecuteScalar());` | auto | `ExecuteScalar returns a different boxed type per engine` |
| `PG-API-003` | `while (reader.Read()) { using var inner = new SqlCommand(sql2, connection); ... }` | `var rows = ReadAll(reader); foreach (var row in rows) { /* second command */ }` | review | `MultipleActiveResultSets has no Npgsql equivalent` |
| `PG-API-004` | `using var bulk = new SqlBulkCopy(connection); bulk.DestinationTableName = "dbo.Staging"...` | `await using var writer = connection.BeginBinaryImport( "COPY dbo.\"Staging\" (\"Id\",\"...` | review | `SqlBulkCopy -> COPY binary import` |
| `PG-API-005` | `var name = (string)table.Rows[0]["ProductName"];` | `SELECT "ProductName" FROM ... // the C# is unchanged once the SQL quotes the column` | review | `DataSet, DataTable and DataRow column access break on casing too` |
| `PG-API-006` | `command.Parameters.Add("@id", SqlDbType.Int).Value = id;` | `command.Parameters.AddWithValue("id", NpgsqlDbType.Integer, id);` | auto | `Concrete Sql* types must not appear in a generated alternate` |
| `PG-API-007` | `using var connection = new SqlConnection(ConfigurationManager.ConnectionStrings["AppDb"...` | `using var connection = _dbFactory.CreateConnection();` | auto | `Route connection creation through the factory` |
| `PG-ORM-010` | `conn.Query<Order>("SELECT TOP 10 Id, Name FROM dbo.[Order]")` | `conn.Query<Order>("SELECT \\"Id\\", \\"Name\\" FROM dbo.\\"Order\\" LIMIT 10")` | review | `Dapper is dialect-neutral and therefore unprotected` |
| `PG-ORM-012` | `DbProviderFactories.GetFactory("System.Data.SqlClient")` | `DbProviderFactories.GetFactory(providerInvariantName)` | auto | `Register the Npgsql factory where DbProviderFactories is already used` |
| `PG-PARAM-001` | `WHERE CustomerId IN (@p0, @p1, @p2)` | `WHERE "CustomerId" = ANY(@ids)` | review | `Parameter-count ceilings and generated IN lists` |
| `PG-PARAM-002` | `command.Parameters.Add(new SqlParameter("@ids", SqlDbType.Structured) { Value = table });` | `command.Parameters.AddWithValue("ids", idArray); // WHERE "Id" = ANY(@ids)` | manual | `Table-valued parameters have no PostgreSQL equivalent` |
| `PG-PARAM-003` | `command.CommandText = "SELECT * FROM dbo.[Order] WHERE Id = @id";` | `command.CommandText = 'SELECT * FROM dbo."Order" WHERE "Id" = @id';` | auto | `@name placeholders are portable; verify the edge cases` |
| `PG-PARAM-004` | `p.Add("@price", SqlDbType.Money).Value = price;` | `p.Add(new NpgsqlParameter("price", NpgsqlDbType.Numeric) { Value = price });` | review | `Provider-specific parameter types belong behind the dialect` |

<!-- dualdb:rules:end -->

## Worked examples

### 1. `add-pg-alternate` - a paged search

```csharp
var sql = @"SELECT TOP (@take) CatalogItemId, Name, Price
              FROM dbo.CatalogItem WITH (NOLOCK)
             WHERE Name LIKE @search AND IsActive = 1
             ORDER BY Name";
var rows = await connection.QueryAsync<CatalogItem>(sql, new { take, search });
```

Rules: `PG-PAG-001`, `PG-HINT-001`, `PG-COLL-001`, `PG-TYPE-005`, `PG-IDENT-001`.

```csharp
var sql = """
    SELECT "CatalogItemId", "Name", "Price"
      FROM dbo."CatalogItem"
     WHERE "Name" ILIKE @search AND "IsActive"
     ORDER BY "Name"
     LIMIT @take
    """;
var rows = await connection.QueryAsync<CatalogItem>(sql, new { take, search });
```

The anonymous parameter object is unchanged - that is the portable part. Note
`ILIKE` is a deliberate decision recorded as `PG-COLL-004`, not a mechanical
substitution: whether case-insensitivity was intended depends on the column.

Dapper's case-insensitive column matching means the quoted-identifier change is
about the *SQL* being valid, not about the mapping - which is why Dapper escapes
the reader-casing break that hits hand-written mappers.

### 2. `add-pg-alternate` - splitting a `QueryMultiple`

```csharp
using var multi = await connection.QueryMultipleAsync(sqlItem + sqlTagCount, new { id });
var item = await multi.ReadFirstOrDefaultAsync<CatalogItem>();
var tags = await multi.ReadFirstAsync<int>();
```

Npgsql has no MARS (`PG-API-003`). Two calls instead of one:

```csharp
var item = await connection.QueryFirstOrDefaultAsync<CatalogItem>(sqlItem, new { id });
var tags = await connection.ExecuteScalarAsync<int>(sqlTagCount, new { id });
```

Two round trips rather than one. Measure before assuming it matters; wrap both in
a transaction if they must see the same snapshot.

### 3. `manual-review` - a custom `TypeHandler`

```csharp
public class HierarchyIdHandler : SqlMapper.TypeHandler<HierarchyPath>
{
    public override void SetValue(IDbDataParameter p, HierarchyPath value)
    {
        ((SqlParameter)p).SqlDbType = SqlDbType.Udt;
        ((SqlParameter)p).UdtTypeName = "hierarchyid";
        p.Value = value.ToSqlHierarchyId();
    }
}
```

Two independent blockers: the handler downcasts to `SqlParameter`, and
`hierarchyid` has no PostgreSQL equivalent at all (`PG-TYPE-038`). The type
question has to be answered - `ltree`, a materialised path, or a recursive CTE -
before the handler can be written, and each answer changes the stored
representation.

`manual-review`, with the `PG-TYPE-038` options carried through and the handler
listed as blocked on that decision.

## Traps

- **Dapper's portability is about Dapper, not about your SQL.** The library adds
  no coupling; the queries are exactly as portable as they were written.
- **`WHERE Id IN @ids`** is Dapper list expansion, not SQL. It works on both
  engines and still produces one parameter per element - so it hits the 2100
  ceiling on SQL Server (`PG-PARAM-001`).
- **`ExecuteScalar<int>()` is safe; `(int)ExecuteScalar()` is not.** The generic
  overload converts; the cast unboxes (`PG-API-002`).
- **A reused parameter** (`WHERE Id = @id OR ParentId = @id`) is the classic
  client-side rewriting bug. Verify it explicitly (`PG-PARAM-003`).
- **`MatchNamesWithUnderscores` is global**, so it cannot be enabled per provider
  in a process serving both.

## Escalate when

- A `TypeHandler` binds a provider-specific type.
- The SQL is assembled from fragments the analyzer could not resolve
  (`PG-DYN-004`).
- `QueryMultiple` results are consumed lazily by a caller outside the unit -
  buffering changes that caller's memory profile.

## Do not

- Do not replace Dapper with an ORM, or add a repository layer, while porting.
- Do not switch placeholder style. `@name` works on both engines
  (`PG-PARAM-003`).
- Do not assume Dapper's case-insensitive mapping covers `DataTable` code in the
  same file - it does not (`PG-API-005`).
