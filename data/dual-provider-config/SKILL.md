---
name: dual-provider-config
description: >
  Wires provider selection into an application's existing configuration for the
  dualdb tool - the switch key, two named connection strings, keyword mapping, and
  fail-fast startup validation. Use whenever you touch Web.config, App.config,
  appsettings.json, a connection string, DbProviderFactories, or the place where
  the provider is chosen.
---

# Dual-provider configuration

Seam 1 of three. Everything else in the port assumes the provider has already been
resolved, once, into a typed value.

## When to use

Any `connectionStrings` section, `appsettings*.json`, `DbProviderFactories`
registration, `<entityFramework>` section, or startup/composition-root code.

## Decision procedure

1. **One switch key** (`PG-CFG-001`). `switch_key` defaults to `Data:Provider` and
   is an input, not a fixed name. Values: `SqlServer`, `PostgreSql`. Read once at
   startup into a typed `DatabaseProvider`.
2. **Fail fast** on a missing or invalid value, naming the key and the allowed
   values. No default engine. No auto-detection.
3. **Two named connection strings, side by side** (`PG-CFG-002`). Add the
   PostgreSQL one; never modify or translate the SQL Server one.
4. Map the keywords (`PG-CFG-003`) - they are almost all different, and two differ
   structurally.
5. Set `Search Path` **in the connection string** (`PG-CFG-006`), never as a
   session `SET`.
6. Assert at startup that the selected provider's connection string exists and is
   non-empty (`PG-CFG-008`).
7. Report, do not solve: `Integrated Security` (`PG-CFG-004`),
   `MultipleActiveResultSets` (`PG-API-003`), `ApplicationIntent`
   (`PG-CFG-007`). These are infrastructure prerequisites.
8. **No credentials in source** (guardrail R5). Generated connection strings use
   placeholders; the tool records only redacted shapes.

## Rule table

<!-- dualdb:rules:begin categories=configuration -->
<!-- generated from knowledge/rules/*.yaml by `dualdb rules sync` - do not edit -->

| id | SQL Server | PostgreSQL | tier | note |
|---|---|---|---|---|
| `PG-CFG-001` | `no provider switch` | `"Data:Provider": "SqlServer"` | auto | `Provider is selected by one config key, resolved once at startup` |
| `PG-CFG-002` | `<add name="AppDb" connectionString="Server=...;" providerName="Microsoft.Data.SqlClient...` | `<add name="AppDb_SqlServer" connectionString="Server=__HOST__;Database=__DB__;..." prov...` | auto | `Two named connection strings, side by side` |
| `PG-CFG-003` | `Server=sqlprod01,1433;Initial Catalog=AppDb;User Id=app;Password=__PWD__` | `Host=pgprod01;Port=5432;Database=AppDb;Username=app;Password=__PWD__` | auto | `Connection-string keyword mapping` |
| `PG-CFG-004` | `Server=sqlprod01;Database=AppDb;Integrated Security=SSPI` | `Host=pgprod01;Database=AppDb;Username=app;Password=__PWD__` | manual | `Integrated Security has no Npgsql equivalent` |
| `PG-CFG-005` | `Encrypt=True;TrustServerCertificate=True` | `SSL Mode=Require;Trust Server Certificate=true` | auto | `TLS settings are named differently` |
| `PG-CFG-006` | `default schema is dbo` | `Host=pgprod01;Database=AppDb;Search Path=dbo` | auto | `search_path must be set in the connection string` |
| `PG-CFG-007` | `Server=aglistener;ApplicationIntent=ReadOnly;Database=AppDb` | `Host=pg-replica;Database=AppDb` | review | `ApplicationIntent=ReadOnly has no Npgsql equivalent` |
| `PG-CFG-008` | `var cs = config.GetConnectionString("AppDb");` | `var cs = config.GetConnectionString(name) ?? throw new InvalidOperationException( $"Dat...` | auto | `Assert the selected provider's connection string exists at startup` |
| `PG-CFG-009` | `ConfigurationManager.ConnectionStrings["AppDb"].ConnectionString` | `_connections.For(_provider.Current) // AppDb_SqlServer \| AppDb_PostgreSql` | review | `A named connection string read in code is provider-specific` |

<!-- dualdb:rules:end -->

## Keyword mapping

| Concern | SqlClient | Npgsql |
|---|---|---|
| Host | `Server=` / `Data Source=` | `Host=` |
| Port | `Server=host,1433` | `Port=5432` (separate key) |
| Database | `Database=` / `Initial Catalog=` | `Database=` |
| User | `User Id=` | `Username=` |
| Windows auth | `Integrated Security=SSPI` | none - SCRAM or Kerberos/GSSAPI |
| TLS | `Encrypt=True;TrustServerCertificate=` | `SSL Mode=Require;Trust Server Certificate=` |
| Pool | `Max Pool Size=`, `Min Pool Size=` | `Maximum Pool Size=`, `Minimum Pool Size=` |
| Timeout | `Connect Timeout=` | `Timeout=`, `Command Timeout=` (two settings) |
| MARS | `MultipleActiveResultSets=True` | none |
| Read routing | `ApplicationIntent=ReadOnly` | none - use a reader host |
| Default namespace | `dbo` | `Search Path=` |

## Worked examples

### 1. `add-pg-alternate` - `appsettings.json`

```json
{
  "Data": { "Provider": "SqlServer" },
  "ConnectionStrings": {
    "AppDb_SqlServer": "Server=__HOST__;Database=__DB__;User Id=__USER__;Password=__PWD__;Encrypt=True;TrustServerCertificate=True",
    "AppDb_PostgreSql": "Host=__HOST__;Port=5432;Database=__DB__;Username=__USER__;Password=__PWD__;SSL Mode=Require;Trust Server Certificate=true;Search Path=dbo"
  }
}
```

Placeholders, never values. `Search Path=dbo` matches the default `pg_schema`.
Switching engines is now editing one string.

### 2. `add-pg-alternate` - `Web.config`

```xml
<appSettings>
  <add key="Data:Provider" value="SqlServer" />
</appSettings>
<connectionStrings>
  <add name="AppDb_SqlServer" connectionString="Server=__HOST__;..." providerName="Microsoft.Data.SqlClient" />
  <add name="AppDb_PostgreSql" connectionString="Host=__HOST__;..." providerName="Npgsql" />
</connectionStrings>
<system.data>
  <DbProviderFactories>
    <add name="Npgsql" invariant="Npgsql" description="Npgsql"
         type="Npgsql.NpgsqlFactory, Npgsql" />
  </DbProviderFactories>
</system.data>
```

A colon is legal in an `appSettings` key, so one `switch_key` value serves both
config styles with no translation. The existing SqlClient factory entry stays.

### 3. `manual-review` - `Integrated Security`

```
Server=sqlprod01;Database=AppDb;Integrated Security=SSPI
```

There is nothing to write in the PostgreSQL string that means this
(`PG-CFG-004`). Three options, each an infrastructure project rather than a config
line:

- **SCRAM password auth** - simple, portable, works everywhere; introduces a
  secret where there was none, which is a real regression for a shop that chose
  Windows auth deliberately.
- **Kerberos / GSSAPI** - preserves the no-stored-credential property; needs a
  service principal, a keytab and correct DNS.
- **Managed identity** - best where the platform offers it, removes the secret
  entirely, ties the deployment to one platform.

Reported at Phase 0 specifically so it can be started early - it is the
prerequisite most often discovered late.

## Traps

- **`SET search_path` after opening is lost.** Pooled connections reset session
  state, so it must be in the connection string (`PG-CFG-006`). The resulting
  `relation does not exist` errors appear only under load, when the pool starts
  recycling - which is the worst possible time to find out.
- **`Server=host,1433` does not port.** Npgsql needs a separate `Port` key
  (`PG-CFG-003`); a comma in `Host` is silently wrong.
- **`Connect Timeout` is one setting, Npgsql has two.** `Timeout` is connect,
  `Command Timeout` is per command.
- **`Encrypt=true` became the default in Microsoft.Data.SqlClient 4.0**, so the
  *SQL Server* side may need attention during the prerequisite step even though
  nothing about PostgreSQL changed.
- **Sniffing the connection string** (`cs.Contains("Host=")`) is forbidden by
  guardrail R7 and rejected by the scope guard.

## Escalate when

- `Integrated Security` or `ApplicationIntent` is in use.
- The connection string is assembled at run time from parts, so the two named
  strings cannot simply sit side by side.
- Multiple applications share one connection string through a central config
  store - the switch has to be scoped, and that is an ops decision.

## Do not

- Do not translate one connection string into the other at run time.
- Do not put a real credential in a generated file, a report, or a log.
- Do not remove or edit the existing SQL Server connection string.
- Do not default the provider when the key is missing. Fail, and say which key.
