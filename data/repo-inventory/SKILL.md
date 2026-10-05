---
name: repo-inventory
description: >
  How dualdb discovers database touchpoints in a .NET repository, and what counts
  as evidence. Use when deciding whether something is a touchpoint, when a finding
  looks wrong or missing, when adding a detector, or when judging discovery recall.
  Missing a touchpoint is the worst bug this tool can have.
---

# Repository inventory

If discovery is incomplete, everything downstream is theatre. A missed touchpoint
is absent from the plan, from the conversion, from the report and from the
reviewer's attention - and nothing indicates it was ever there.

## When to use

Deciding whether a construct is a database touchpoint; adding or tuning a
detector; investigating a missing or spurious finding; authoring or reviewing a
corpus ground-truth file.

## Decision procedure

1. **Recall beats precision, always.** A false positive costs one row in a table
   the rules engine then decides is `no-change`. A false negative costs
   correctness silently. When unsure, emit the finding.
2. **Report evidence, not conclusions.** The analyzer records what is there; the
   rules engine decides what it means. That separation keeps the rule pack the
   single source of truth and means a rule change never needs the sidecar
   rebuilt.
3. **Never omit what you could not read.** An unparseable file, a project that
   failed to load, a semantic model that was unavailable - all go into
   `inventory.errors`. Silence would read as "clean".
4. **Every file in the queue gets a classification**, and `unaffected` always
   carries a reason. "We did not look" is not a reason a report may contain.
5. **Resolve what you can, flag what you cannot.** A partially reconstructed
   statement gets `{?}` placeholders and its fragments recorded, so its confidence
   drops rather than its status looking complete.

## Sources scanned

| Source | Extracted |
|---|---|
| `.sln`, `.csproj`, `.vbproj` | TFMs, SDK-style, project kind, package references |
| `packages.config`, `PackageReference` | data-access libraries and versions |
| `Web.config`, `App.config` | `connectionStrings`, `providerName`, `entityFramework`, `DbProviderFactories` |
| `appsettings*.json` | connection strings, provider settings |
| C#/VB via Roslyn | see below |
| `.edmx`, `.dbml`, `.hbm.xml` | provider-coupled mappings, `HasColumnType`, SQL Server-only types |
| `Migrations/**` | provider-specific SQL |
| `**/*.sql` | DDL, procedures, functions, views, seed scripts |
| `.resx` | SQL held as a resource |
| test projects | tests asserting on SQL text, provider types or DB behaviour |

## What the Roslyn sidecar finds

- **Provider type usage** - `SqlConnection`, `SqlCommand`, `SqlDataAdapter`,
  `SqlParameter`, `SqlDbType`, `SqlBulkCopy`, `SqlException`, `SqlTransaction`,
  `SqlDataReader`.
- **Inline SQL** - literals, interpolation, concatenation and `StringBuilder`
  chains reaching a `CommandText` / Dapper / `SqlQuery` / `FromSqlRaw` sink, via a
  backward dataflow walk. Plus a catch-all pass for SQL that reaches a *bespoke*
  helper, which is where the sink list always falls short.
- **Stored procedure calls** - `CommandType.StoredProcedure` or `EXEC`-shaped
  text, with the parameter list including `Output` and `ReturnValue` directions.
- **ORM surfaces** - EF6 `DbContext`/`DbConfiguration`/`Database.SqlQuery`; EF Core
  `UseSqlServer`, `FromSqlRaw`, `HasColumnType`, value converters; Dapper
  `Query*`/`Execute*`; NHibernate dialect configuration; LINQ query chains.
- **Connection acquisition** - every construction or resolution site. This is the
  set retargeted to the factory.
- **SQL Server-only APIs** - `SqlBulkCopy`, `SqlDependency`,
  `SqlNotificationRequest`, `TransactionScope` escalation, `SqlException.Number`
  switches.
- **Type-coupled reads** - `reader.GetBoolean(i)` vs `(int)reader["Flag"]`,
  `Convert.ToBoolean`, `GetGuid`, `GetDateTime`. Where `bit` and `DateTime.Kind`
  bugs hide.

## What the additive strategy additionally requires

Because conversion is whole-unit, each finding also carries:

- **Unit boundaries** - the containing member with its exact span, signature,
  return type, parameters, accessibility, modifiers, generic constraints and
  containing type. The extract-and-dispatch transform needs all of it to produce a
  compiling alternate.
- **Unit purity** - `pure-data-access` or `mixed`. A mixed unit's business logic
  must never be duplicated (guardrail R2), so the classifier errs toward `mixed`.
- **File purity** - data-access members over total members, plus whether the type
  is `partial`. Drives `add-pg-alternate` vs `add-pg-file`.
- **Unit dependencies** - private helpers, fields and constants, so the alternate
  reuses rather than duplicates them.
- **Call sites** - to confirm the dispatcher preserves the public contract and no
  caller changes.
- **`bodySha256`** - the pre-conversion baseline the immutability check compares
  against.

## Worked examples

### 1. Found by a sink - a command constructor

```csharp
using var command = new SqlCommand(
    "SELECT TOP (@take) Id, CustomerName FROM dbo.[Order] WHERE CustomerId = @customerId",
    connection);
```

The first argument of a `SqlCommand` constructor is a SQL sink, so the statement is
reconstructed directly. Kind `InlineSql`, fully resolved, no unresolved fragments -
the easy case, and the one a sink list handles.

### 2. Found only by the catch-all - SQL reaching a bespoke helper

```csharp
string sql = "SELECT TOP 50 Id, CustomerName FROM dbo.[Order] WHERE 1 = 1";
if (!string.IsNullOrEmpty(search))
    sql += " AND CustomerName LIKE '%" + search + "%'";
DataTable table = SqlHelper.Fill(sql);
```

`SqlHelper.Fill` is not in any signature list, so no sink matches. The catch-all
pass resolves the local instead, accumulating the conditional append and recording
`search` as an unresolved fragment. Kind `InlineSql`, template
`SELECT TOP 50 ... LIKE '%{?}%'`, plus a security finding for the concatenation.

Missing this one would lose both the statement and the injection.

### 3. `manual-review` - a touchpoint that cannot be resolved

```csharp
public static DataTable Fill(string sql, params SqlParameter[] parameters)
```

A real touchpoint: it constructs a connection and a command. But the statement is a
parameter, so nothing can be evaluated against the rule pack, and the signature
itself is provider-coupled. The finding is emitted with `{?}` as its template and
`sql` in `unresolvedFragments`, and it resolves to `manual-review` rather than to a
generated alternate.

The important part is that the finding **exists**. Emitting nothing would leave a
connection site, a command construction and every caller invisible.

## Traps

- **Sinks are not enough.** `SqlHelper.Fill(sql)` is a bespoke helper; the SQL
  reaching it is invisible to a sink list. Hence the literal catch-all pass.
- **A `.sql` file is many units.** Split at `GO` - each batch is its own
  conversion unit with its own line range.
- **A connection string in a test** is still a connection string, and a test that
  opens one must be deferred rather than silently skipped.
- **Two identical statements are one decision.** Dedupe by normalized SQL
  fingerprint, apply everywhere, report once with an occurrence count.
- **An empty findings list is a claim.** If the analyzer did not run, say so - do
  not present a clean, reassuring summary.

## Escalate when

- The analyzer could not load a project at all and the fallback produced
  suspiciously few findings.
- A repo uses a data-access library the signature lists do not cover - the
  catch-all will find the SQL but not the API coupling.
- SQL appears in markup (`<asp:SqlDataSource>`) or in a database-stored
  configuration table. Neither is scanned today.

## Do not

- Do not sample. Every queued file is classified.
- Do not suppress a finding because it looks like a false positive - let the rules
  engine decide `no-change`.
- Do not evaluate rules in the analyzer.
- Do not record a connection-string value anywhere, in any artifact or log.
