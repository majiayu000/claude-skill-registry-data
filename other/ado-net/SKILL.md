---
name: ado-net
description: >
  Converts raw ADO.NET data access - SqlConnection, SqlCommand, SqlParameter,
  SqlDataReader, SqlDataAdapter, DataSet/DataTable, SqlBulkCopy - to a
  dual-provider shape for the dualdb tool. Use whenever a unit constructs a
  connection or command directly, reads a DbDataReader, fills a DataTable, casts
  an ExecuteScalar result, or catches SqlException. The SQL is only half the work;
  this skill covers the other half.
---

# ADO.NET

## When to use

Any unit containing `SqlConnection`, `SqlCommand`, `SqlParameter`, `SqlDbType`,
`SqlDataReader`, `SqlDataAdapter`, `SqlTransaction`, `SqlBulkCopy` or
`SqlException`; any `DataSet`/`DataTable` filled from a query; any
`ExecuteScalar` whose result is cast; any `reader["Column"]` access.

## Decision procedure

1. Convert the **whole unit**. A PostgreSQL alternate that keeps `SqlParameter`
   and `reader.GetBoolean` compiles and fails at run time - worse than no
   alternate.
2. Route connection acquisition through the factory (`PG-API-007`). This is the
   one in-place edit permitted outside a generated alternate, and only at sites
   the inventory marked `ConnectionSite`. If the app already uses
   `DbProviderFactories`, use that rather than adding an interface (`PG-ORM-012`).
3. Quote every column in the PostgreSQL `SELECT`, aliases included
   (`PG-API-001`), or the reader's string indexers break.
4. Convert every `ExecuteScalar` cast to `Convert.ToInt32`/`ToInt64`
   (`PG-API-002`).
5. Replace `catch (SqlException)` with `DbException` plus the dialect classifier
   (`PG-ERR-001`).
6. Check for MARS dependencies - a command issued while a reader is open
   (`PG-API-003`).
7. Check every `try`/`catch` inside a transaction (`PG-TXN-006`).
8. `SqlBulkCopy` -> `IBulkInserter` / `COPY` (`PG-API-004`). Never a row loop.
9. No `Sql*` type may appear in the generated alternate (`PG-API-006`).

## Rule table

<!-- dualdb:rules:begin categories=ado-net,parameters,errors -->
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
| `PG-ERR-001` | `catch (SqlException ex) when (ex.Number == 2627 \|\| ex.Number == 2601)` | `catch (DbException ex) when (dialect.IsUniqueViolation(ex))` | review | `SqlException numbers vs PostgreSQL SQLSTATEs` |
| `PG-ERR-002` | `options.UseSqlServer(cs, sql => sql.EnableRetryOnFailure(3));` | `options.UseNpgsql(cs, npg => npg.EnableRetryOnFailure(3));` | review | `Retry policies keyed on SQL Server error numbers must be extended` |
| `PG-ORM-012` | `DbProviderFactories.GetFactory("System.Data.SqlClient")` | `DbProviderFactories.GetFactory(providerInvariantName)` | auto | `Register the Npgsql factory where DbProviderFactories is already used` |
| `PG-PARAM-001` | `WHERE CustomerId IN (@p0, @p1, @p2)` | `WHERE "CustomerId" = ANY(@ids)` | review | `Parameter-count ceilings and generated IN lists` |
| `PG-PARAM-002` | `command.Parameters.Add(new SqlParameter("@ids", SqlDbType.Structured) { Value = table });` | `command.Parameters.AddWithValue("ids", idArray); // WHERE "Id" = ANY(@ids)` | manual | `Table-valued parameters have no PostgreSQL equivalent` |
| `PG-PARAM-003` | `command.CommandText = "SELECT * FROM dbo.[Order] WHERE Id = @id";` | `command.CommandText = 'SELECT * FROM dbo."Order" WHERE "Id" = @id';` | auto | `@name placeholders are portable; verify the edge cases` |
| `PG-PARAM-004` | `p.Add("@price", SqlDbType.Money).Value = price;` | `p.Add(new NpgsqlParameter("price", NpgsqlDbType.Numeric) { Value = price });` | review | `Provider-specific parameter types belong behind the dialect` |

<!-- dualdb:rules:end -->

## Worked examples

### 1. `add-pg-file` - a pure DAL class

`OrderDataAccess.cs` is entirely data access: every member opens a connection,
builds a command and maps a reader. Above the parallel-file threshold (more than
~3 methods or more than ~40% of members), so it gets a sibling file rather than
per-method alternates:

```
Data/OrderDataAccess.cs              <- unchanged, byte for byte
Data/OrderDataAccess.PostgreSql.cs   <- added
```

`partial class` where the type already is, or can be made, partial with a
one-word edit; otherwise a sibling class selected by the factory.

The PostgreSQL implementation:

```csharp
using var connection = _factory.CreateConnection();          // PG-API-007
using var command = connection.CreateCommand();
command.CommandText = """
    SELECT "Id", "CustomerName", "IsActive", "CreatedUtc"      -- PG-API-001
      FROM dbo."Order"
     WHERE "CustomerId" = @customerId
     ORDER BY "CreatedUtc" DESC
     LIMIT @take
    """;
command.Parameters.AddWithValue("customerId", customerId);     // PG-PARAM-003
command.Parameters.AddWithValue("take", take);
connection.Open();
using var reader = command.ExecuteReader();
while (reader.Read())
{
    results.Add(new Order
    {
        Id = reader.GetInt32(reader.GetOrdinal("Id")),
        IsActive = reader.GetBoolean(reader.GetOrdinal("IsActive")),   // PG-TYPE-005
        CreatedUtc = reader.GetDateTime(reader.GetOrdinal("CreatedUtc")),
    });
}
```

### 2. `add-pg-alternate` - an identity insert in a mixed file

```csharp
public int CreateOrder(string customerName)   // dispatcher, signature unchanged
    => _db.Provider == DatabaseProvider.PostgreSql
        ? CreateOrder_PostgreSql(customerName)
        : CreateOrder_SqlServer(customerName);
```

`CreateOrder_SqlServer` is the original body, moved verbatim. The alternate uses
`RETURNING "Id"` (`PG-FUNC-008`) and `Convert.ToInt32` (`PG-API-002`), because
`SCOPE_IDENTITY()` returns a boxed `decimal` and `RETURNING` a boxed `int`.

### 3. `manual-review` - SQL arrives as a parameter

```csharp
public static DataTable Fill(string sql, params SqlParameter[] parameters)
```

The SQL text is unknowable at analysis time, so no rule can be evaluated against
it and no PostgreSQL alternate can be written for the *statement*. The method
signature is also provider-coupled: `SqlParameter[]` is part of its public
contract, so every caller changes too.

`manual-review`, grouped under "generic SQL helper", with the call sites listed so
the reviewer can see the scale. Do not generate a `Fill_PostgreSql` that simply
passes the same text to Npgsql - it would compile and fail on the first T-SQL
statement handed to it.

## Traps

- **Aliases must be quoted too.** `SUM(x) AS "GrandTotal"`, not `AS GrandTotal`.
  This is the one people forget after quoting every column.
- **`DataTable` and `DataRow` break exactly like a reader** (`PG-API-005`), and
  they do not show up when grepping for `reader`.
- **`AddWithValue` with an `int` for a `bit` column** now throws - PostgreSQL's
  `boolean` is a real boolean (`PG-TYPE-005`).
- **A `catch` inside a transaction that logs and continues** fails on the *next*
  statement, not the one that failed (`PG-TXN-006`).
- **`SqlDbType.Money` is `NpgsqlDbType.Numeric`**, `SqlDbType.Bit` is
  `NpgsqlDbType.Boolean`, `SqlDbType.UniqueIdentifier` is `NpgsqlDbType.Uuid`.
  Letting Npgsql infer from the CLR type is usually better than transcribing
  (`PG-PARAM-004`).

## Escalate when

- The SQL text is a parameter or otherwise unresolvable (`PG-DYN-004`).
- A provider type appears in a **public** signature - converting it changes the
  contract, and callers are outside the unit.
- MARS is genuinely load-bearing and buffering would change memory behaviour
  materially.
- `SqlBulkCopy` column mappings need schema the run does not have.

## Do not

- Do not replace `DataTable`/`DataSet` usage with typed models. That is
  modernization, not porting.
- Do not widen the original unit's types to `Db*`. The original is not shared
  code; widening it edits the SQL Server path.
- Do not parameterize the original's concatenated SQL. Report it as a security
  finding instead - fixing it in place is an edit to a working path.
- Do not substitute a row-by-row insert loop for `SqlBulkCopy`. It is an
  order-of-magnitude regression that then gets blamed on PostgreSQL.
