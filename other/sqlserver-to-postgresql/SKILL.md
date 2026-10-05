---
name: sqlserver-to-postgresql
description: >
  Converts SQL Server / T-SQL to PostgreSQL for the dualdb tool, and decides when
  conversion is unsafe. Use this skill whenever you encounter T-SQL, inline SQL in
  .NET code, a .sql file, a SQL Server data type or function, or any question about
  SQL Server vs PostgreSQL differences - even if the task looks like a simple
  find-and-replace. Always use it before writing any PostgreSQL SQL.
---

# SQL Server -> PostgreSQL conversion

The hub skill. Everything else in `skills/` is a specialisation of the decision
procedure below.

## When to use

- Any T-SQL statement, anywhere: a string literal in C#, a `.sql` file, an
  `.edmx`, a migration, a `HasDefaultValueSql`, a Dapper call.
- Any SQL Server data type or function name.
- Any question of the form "does X behave the same on PostgreSQL?" - the answer is
  usually "not exactly", and the rule pack says how.
- **Before** writing a single line of PostgreSQL SQL. Not after.

## Decision procedure

1. **Identify the enclosing data-access unit** - normally the whole method, or a
   whole `.sql` batch. You convert the unit, never individual lines. Converting
   the SQL string and leaving `SqlParameter`, `SqlDbType` and `reader.GetBoolean`
   in place produces code that compiles and then fails at run time.
2. **Normalize the statement.** If it contains unresolved dynamic fragments
   (`PG-DYN-004`) -> `manual-review`. Do not guess at what the fragment contains.
3. **Match rules** from `knowledge/rules/*.yaml`. Collect the tiers.
4. If any hit is `tier: manual` -> `manual-review`, with the rule's two to three
   options carried into the report.
5. If a hit has `requiresSchema: true` and you do not have that schema ->
   `manual-review`. **Do not infer schema.** This is the most important
   behavioural rule in the tool.
6. If the file is a pure SQL handler, or a `.sql` file -> `add-pg-file`: write a
   complete parallel PostgreSQL implementation and leave the original untouched.
7. Otherwise -> `add-pg-alternate`: write a complete PostgreSQL counterpart of the
   whole unit, including connection acquisition, parameter binding, execution,
   reader access and error handling. Record every `behaviour-risk` hit. **The
   original unit is not edited.**
8. `portable-rewrite` only if *every* condition holds: the statement is fully
   resolved, every rule hit is `tier: auto`, there are zero `behaviour-risk` hits,
   and no provider-specific .NET API is involved. When in doubt, go to step 7 -
   an extra method costs nothing and a silent regression in a shared path costs
   a great deal.

## Rule table

<!-- dualdb:rules:begin categories=identifiers,pagination,literals,nulls,strings,expressions,conversion,formatting,dml,joins,session,scripts,system,aggregation -->
<!-- generated from knowledge/rules/*.yaml by `dualdb rules sync` - do not edit -->

| id | SQL Server | PostgreSQL | tier | note |
|---|---|---|---|---|
| `PG-FUNC-001` | `SELECT FirstName + ' ' + LastName FROM dbo.Person` | `SELECT FirstName \|\| ' ' \|\| LastName FROM dbo.Person` | review | `String concatenation: + -> \|\| or CONCAT` |
| `PG-FUNC-002` | `SELECT LEN(Code) FROM dbo.Product` | `SELECT LENGTH(Code) FROM dbo."Product"` | review | `LEN(s) -> LENGTH(s)` |
| `PG-FUNC-003` | `SELECT DATALENGTH(Notes) FROM dbo.Order` | `SELECT OCTET_LENGTH("Notes") FROM dbo."Order"` | auto | `DATALENGTH(s) -> OCTET_LENGTH(s)` |
| `PG-FUNC-004` | `SELECT CHARINDEX('@', Email) FROM dbo.Person` | `SELECT POSITION('@' IN "Email") FROM dbo."Person"` | review | `CHARINDEX(needle, haystack) -> POSITION / STRPOS` |
| `PG-FUNC-005` | `SELECT IIF(IsActive = 1, 'yes', 'no') FROM dbo.[Order]` | `SELECT CASE WHEN IsActive = 1 THEN 'yes' ELSE 'no' END FROM dbo.[Order]` | auto | `IIF(c, a, b) -> CASE WHEN` |
| `PG-FUNC-006` | `SELECT FORMAT(Total, 'N2') FROM dbo.[Order]` | `SELECT to_char("Total", 'FM999,999,990.00') FROM dbo."Order"` | review | `FORMAT(v, fmt) / STR(n) -> to_char` |
| `PG-FUNC-009` | `DELETE FROM dbo.[Order] OUTPUT DELETED.Id WHERE IsActive = 0` | `DELETE FROM dbo."Order" WHERE "IsActive" = FALSE RETURNING "Id"` | review | `OUTPUT INSERTED/DELETED -> RETURNING` |
| `PG-FUNC-010` | `MERGE dbo.Stock AS t USING (SELECT @sku AS Sku, @qty AS Qty) AS s ON t.Sku = s.Sku WHEN...` | `INSERT INTO dbo."Stock" ("Sku", "Qty") VALUES (@sku, @qty) ON CONFLICT ("Sku") DO UPDAT...` | review | `MERGE -> INSERT ... ON CONFLICT DO UPDATE` |
| `PG-FUNC-011` | `UPDATE dbo.[Order] SET IsActive = 0 WHERE Id = @id; SELECT @@ROWCOUNT;` | `UPDATE dbo."Order" SET "IsActive" = FALSE WHERE "Id" = @id` | auto | `@@ROWCOUNT -> ExecuteNonQuery's return value` |
| `PG-FUNC-012` | `UPDATE o SET o.IsActive = 0 FROM dbo.[Order] AS o JOIN dbo.Customer AS c ON c.Id = o.Cu...` | `UPDATE dbo."Order" AS o SET "IsActive" = FALSE FROM dbo."Customer" AS c WHERE c."Id" = ...` | auto | `UPDATE ... FROM join syntax` |
| `PG-FUNC-013` | `DELETE o FROM dbo.[Order] o JOIN dbo.Customer c ON c.Id = o.CustomerId WHERE c.IsClosed...` | `DELETE FROM dbo."Order" o USING dbo."Customer" c WHERE c."Id" = o."CustomerId" AND c."I...` | auto | `DELETE ... FROM join syntax -> DELETE ... USING` |
| `PG-FUNC-014` | `SELECT o.Id, x.Total FROM dbo.[Order] o CROSS APPLY (SELECT SUM(Amount) AS Total FROM d...` | `SELECT o."Id", x.total FROM dbo."Order" o CROSS JOIN LATERAL (SELECT SUM("Amount") AS t...` | auto | `CROSS APPLY / OUTER APPLY -> LATERAL` |
| `PG-FUNC-015` | `SET NOCOUNT ON;` | `no direct equivalent` | auto | `SET NOCOUNT / ANSI_NULLS / QUOTED_IDENTIFIER` |
| `PG-FUNC-016` | `CREATE TABLE dbo.[Order] (Id int); GO CREATE INDEX IX ON dbo.[Order] (Id);` | `two separate commands, no GO` | auto | `GO is not SQL` |
| `PG-FUNC-017` | `SELECT STUFF((SELECT ',' + Name FROM dbo.Tag WHERE OrderId = o.Id FOR XML PATH('')), 1,...` | `SELECT (SELECT STRING_AGG("Name", ',' ORDER BY "Name") FROM dbo."Tag" WHERE "OrderId" =...` | review | `STUFF(... FOR XML PATH('')) -> STRING_AGG` |
| `PG-FUNC-018` | `SELECT Id FROM dbo.[Order] WHERE CustomerId IN (SELECT value FROM STRING_SPLIT(@ids, ','))` | `SELECT "Id" FROM dbo."Order" WHERE "CustomerId" = ANY(@ids)` | auto | `STRING_SPLIT -> string_to_array + unnest` |
| `PG-FUNC-019` | `SELECT * FROM (SELECT Year, Region, Total FROM dbo.Sales) s PIVOT (SUM(Total) FOR Regio...` | `SELECT "Year", SUM(CASE WHEN "Region" = 'North' THEN "Total" END) AS "North", SUM(CASE ...` | review | `PIVOT / UNPIVOT -> conditional aggregation` |
| `PG-FUNC-020` | `SELECT Name + SPACE(4) + Code FROM dbo.Product` | `SELECT "Name" \|\| repeat(' ', 4) \|\| "Code" FROM dbo."Product"` | auto | `SPACE(n) -> repeat(' ', n)` |
| `PG-FUNC-021` | `SELECT @@VERSION` | `SELECT version()` | auto | `@@VERSION -> version()` |
| `PG-FUNC-022` | `TRUNCATE TABLE dbo.Staging` | `TRUNCATE TABLE dbo."Staging"` | auto | `TRUNCATE TABLE is portable` |
| `PG-FUNC-026` | `INSERT INTO REMOTEDW.Warehouse.dbo.OrderFact SELECT Id, Total FROM dbo.[Order]` | `no direct equivalent` | manual | `Linked servers and OPENQUERY have no PostgreSQL equivalent` |
| `PG-IDENT-001` | `SELECT [Id], [CustomerName] FROM dbo.[Order]` | `SELECT "Id", "CustomerName" FROM dbo."Order"` | auto | `[bracket] quoting -> "double quote" quoting` |
| `PG-IDENT-002` | `SELECT Id FROM dbo.[Order]` | `SELECT "Id" FROM dbo."Order"` | auto | `dbo schema qualification` |
| `PG-IDENT-003` | `CREATE INDEX IX_CatalogItem_Name_Including_Price_And_CreatedUtc_For_Search ON dbo.Catal...` | `CREATE INDEX "IX_CatalogItem_Name_Search" ON dbo."CatalogItem" ("Name")` | review | `PostgreSQL truncates identifiers at 63 bytes` |
| `PG-IDENT-004` | `CREATE TABLE dbo.[CatalogItem] ([CatalogItemId] int)` | `CREATE TABLE dbo."CatalogItem" ("CatalogItemId" int)` | behaviour-risk | `PostgreSQL folds unquoted identifiers to lower case` |
| `PG-NULL-001` | `SELECT ISNULL(Discount, 0) FROM dbo.Orders` | `SELECT COALESCE(Discount, 0) FROM dbo.Orders` | auto | `ISNULL(a, b) -> COALESCE(a, b)` |
| `PG-NULL-002` | `SELECT COUNT(*) FROM dbo.[Order] WHERE Notes = ''` | `SELECT COUNT(*) FROM dbo."Order" WHERE "Notes" = ''` | auto | `Empty string and NULL are distinct on both engines` |
| `PG-NULL-003` | `SELECT FirstName + ' ' + LastName FROM dbo.Person WHERE MiddleName IS NULL` | `SELECT "FirstName" \|\| ' ' \|\| "LastName" FROM dbo."Person"` | behaviour-risk | `CONCAT skips NULLs; + and \|\| propagate them` |
| `PG-PAG-001` | `SELECT TOP 10 Id FROM dbo.Orders ORDER BY Id` | `SELECT Id FROM dbo.Orders ORDER BY Id LIMIT 10` | auto | `SELECT TOP n -> LIMIT n` |
| `PG-PAG-002` | `SELECT TOP 10 PERCENT Id FROM dbo.Orders ORDER BY Total DESC` | `SELECT Id FROM (SELECT Id, ntile(10) OVER (ORDER BY Total DESC) AS bucket FROM dbo.Orde...` | review | `TOP n PERCENT / WITH TIES` |
| `PG-PAG-003` | `SELECT Id FROM dbo.Orders ORDER BY Id OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY` | `SELECT Id FROM dbo.Orders ORDER BY Id OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY` | auto | `OFFSET/FETCH is portable` |
| `PG-PAG-004` | `DELETE TOP (1000) FROM dbo.AuditLog WHERE CreatedUtc < @cutoff` | `DELETE FROM dbo."AuditLog" WHERE "Id" IN (SELECT "Id" FROM dbo."AuditLog" WHERE "Create...` | review | `DELETE TOP (n) / UPDATE TOP (n)` |
| `PG-TYPE-001` | `SELECT * FROM dbo.[Order] WHERE CustomerName = N'Müller'` | `SELECT * FROM dbo."Order" WHERE "CustomerName" = 'Müller'` | auto | `N'literal' national character prefix` |
| `PG-TYPE-002` | `SELECT CONVERT(varchar(10), Id) FROM dbo.[Order]` | `SELECT CAST(Id AS varchar(10)) FROM dbo.[Order]` | auto | `CONVERT(type, value) -> CAST(value AS type)` |
| `PG-TYPE-003` | `SELECT TRY_CONVERT(int, Code) FROM dbo.Import` | `SELECT CASE WHEN "Code" ~ '^-?[0-9]+$' THEN "Code"::int END FROM dbo."Import"` | manual | `TRY_CONVERT / TRY_CAST have no equivalent` |
| `PG-TYPE-004` | `WHERE ISNUMERIC(Code) = 1` | `WHERE "Code" ~ '^-?[0-9]+$'` | manual | `ISNUMERIC has no equivalent` |

<!-- dualdb:rules:end -->

Full detail per area is in `references/`:

| Reference | Covers |
|---|---|
| [datatypes.md](references/datatypes.md) | Appendix C, GUID ordering, `rowversion` |
| [functions.md](references/functions.md) | string, math and system functions |
| [datetime.md](references/datetime.md) | `DateTime.Kind`, precision, ranges, Npgsql switches |
| [nulls-and-collation.md](references/nulls-and-collation.md) | `ISNULL`, case sensitivity, sort order |
| [pagination.md](references/pagination.md) | `TOP`, `LIMIT`, `OFFSET/FETCH`, ordering |
| [identity-and-sequences.md](references/identity-and-sequences.md) | identity, `RETURNING`, sequence re-sync |
| [temp-tables-and-tvs.md](references/temp-tables-and-tvs.md) | `#temp`, table variables, TVPs |
| [transactions-and-hints.md](references/transactions-and-hints.md) | isolation, `NOLOCK`, `40001` retry |
| [dynamic-sql.md](references/dynamic-sql.md) | `sp_executesql`, unresolved fragments |
| [errors-and-sqlstates.md](references/errors-and-sqlstates.md) | error numbers to SQLSTATEs |
| [json-and-xml.md](references/json-and-xml.md) | `FOR JSON`, `OPENJSON`, XML methods |
| [identifiers-and-casing.md](references/identifiers-and-casing.md) | quoting, folding, reserved words, 63 bytes |
| [engine-limits.md](references/engine-limits.md) | parameter counts, identifier length, precision |

## Worked examples

### 1. `add-pg-alternate` - a paged query with a hint

```sql
SELECT TOP (@take) Id, CustomerName, IsActive, CreatedUtc
  FROM dbo.[Order] WITH (NOLOCK)
 WHERE CustomerId = @customerId
 ORDER BY CreatedUtc DESC
```

Rules: `PG-PAG-001` (auto), `PG-HINT-001` (manual), `PG-IDENT-001` (auto),
`PG-TYPE-005` (review, via `IsActive`), `PG-API-001` (review, the reader reads by
column name).

`PG-HINT-001` is `tier: manual`, so by step 4 this is `manual-review` — *unless*
the `NOLOCK` is classified as habitual, which it is here: the query reads for
display and nothing depends on seeing uncommitted rows. With that classification
recorded, the decision is `add-pg-alternate`:

```sql
SELECT "Id", "CustomerName", "IsActive", "CreatedUtc"
  FROM dbo."Order"
 WHERE "CustomerId" = @customerId
 ORDER BY "CreatedUtc" DESC
 LIMIT @take
```

Behaviour risks recorded: `PG-TXN-004` (the hint's removal), `PG-ORD-001` if
`CreatedUtc` is nullable. The C# alternate binds a `bool` for `IsActive` and reads
it with `GetBoolean`.

### 2. `portable-rewrite` - the narrow case

```sql
SELECT ISNULL(Discount, 0) FROM dbo.Orders
```

One rule hit: `PG-NULL-001`, `tier: auto`, no behaviour risk, statement fully
resolved, no provider-specific .NET API in the unit (it runs through
`DbConnection` already). `COALESCE` is valid on both engines, so one statement can
serve both:

```sql
SELECT COALESCE(Discount, 0) FROM dbo.Orders
```

This is the *only* shape that qualifies. Note what is absent: no bracket
identifiers, no reader-by-name mapping, no `SqlParameter`.

### 3. `manual-review` - a statement that must not be converted

```sql
SELECT COUNT(*) FROM dbo.ImportBatch WITH (NOLOCK) WHERE Status = 0
```

Identical syntax to example 1, and a completely different answer. This query polls
a batch that a long-running import transaction is still writing, and the whole
point of the `NOLOCK` is to see the in-flight rows. On PostgreSQL that is not
possible at any isolation level.

`PG-HINT-001` fires as `noEquivalent`, so the output is a `MANUAL_REVIEW.md` entry
carrying its three options - remove the hint, restructure into one transaction, or
stage the rows - with the trade-offs, and **no generated alternate**. A missing
artifact is recoverable; a wrong one that compiles is not.

## Traps

- **Two identical-looking `NOLOCK`s, two different answers.** Examples 1 and 3
  differ only in what the caller depends on. This is why every occurrence is
  classified rather than deleted on sight.
- **`CONCAT` is not `+`.** `PG-NULL-003`: `CONCAT` skips NULLs, `+` and `||`
  propagate them. The rewrite is valid, plausible, and changes results.
- **`LEN` is not `LENGTH`.** `PG-FUNC-002`: `LEN` ignores trailing spaces.
- **The `.NET` half is half the work.** Reader casing (`PG-API-001`),
  `ExecuteScalar` types (`PG-API-002`), `bit` reads (`PG-TYPE-005`) and exception
  types (`PG-ERR-001`) all break independently of the SQL.
- **`TIMESTAMP` in T-SQL is `rowversion`.** `PG-TYPE-008`. Mapping it to a
  PostgreSQL `timestamp` corrupts data and the migration succeeds.

## Escalate when

Any of these forces `manual-review` regardless of everything else:

- an unresolved dynamic fragment (`PG-DYN-004`)
- any rule with `noEquivalent: true`
- a rule with `requiresSchema: true` and no schema hints supplied
- a `behaviour-risk` hit the classification cannot resolve from the code alone
- the unit is `mixed` (data access plus business logic) and the data access cannot
  be cleanly separated - duplicating business logic is forbidden

## Do not

- Do not convert at line granularity when the unit is a method.
- Do not edit the SQL Server statement. Ever. Add beside it.
- Do not infer schema - nullability, collation, precision, whether a `bit` is read
  as `bool` or `int`. If the decision needs schema you do not have, the answer is
  `manual-review`.
- Do not "improve" the SQL while porting it: no added indexes, no rewritten joins,
  no caching, no changed pagination semantics.
- Do not emit a plausible-looking wrong function or statement. Emit a stub and a
  review entry.
- Do not introduce PostgreSQL arrays or native `enum` into the shared model - they
  have no SQL Server equivalent.
