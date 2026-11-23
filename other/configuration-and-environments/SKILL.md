---
name: configuration-and-environments
description: How settings are layered with appsettings files and environment variables, what the local and docker environments are, and how to add a new setting. Use when adding configuration, a connection string or environment-specific behaviour.
metadata:
  scope: shared
---

# Configuration and environments

## The rule

Settings come from `appsettings.json`, then `appsettings.<environment>.json`, then environment variables (`Section__Key`). The base file holds safe defaults for anywhere; the environment files hold what's only true for that environment.

The Lambda template has no appsettings files or environments. Its startup builds configuration from environment variables alone, so the same keys are set as `ConnectionStrings__MovieReviews` and `Database__SeedSampleData`, and the defaults live in `Startup`.

| Environment | Set by | Used for |
| --- | --- | --- |
| `local` | `launchSettings.json` (`DOTNET_ENVIRONMENT=local`) | `dotnet run` on a developer machine: console logs, sample data on |
| `docker` | `docker-compose.yml` and the Dockerfile | `docker compose up`: telemetry over OTLP through the collector to the Aspire dashboard, database in `/app/data`, sample data on |
| anything else | the host | Real deployments: base settings only, sample data off, HSTS on |

Settings that exist today:

| Key | Meaning |
| --- | --- |
| `ConnectionStrings:MovieReviews` | SQLite connection string. `Data Source=Name;Mode=Memory;Cache=Shared` keeps everything in memory. |
| `Database:SeedSampleData` | Seed sample data into an empty database (`sample-data`). |
| `Authentication:Authority`, `Authentication:Audience` | Only in a solution created with `--include-auth`: turn on token authentication (`optional-token-auth`). MCP also has `Authentication:Scopes`, published in its protected resource metadata. |
| `Serilog:*` | Logging (`serilog`). |

## Steps

1. Put the safe default in `appsettings.json`. If the default is "off" or empty, still write the key so people can find it.
2. Override it only in the environment files that need a different value.
3. Read a single value with `configuration.GetValue<T>("Section:Key")`; read a group into a settings class with a `SectionName` constant and a `FromConfiguration(IConfiguration)` method, like `AuthenticationSettings` in a solution with authentication.
4. Document the key in `docs/RUN.md` if someone running the app might change it.
5. Tests override settings in memory (`integration-tests`), never by editing the JSON.

## Don't

- Put secrets, passwords or tokens in any `appsettings*.json` file. Use environment variables or user secrets.
- Check `IsEnvironment("local")` for behaviour that should be a setting. Add a setting instead.
- Read `Environment.GetEnvironmentVariable` directly. Go through `IConfiguration`.

## Check

``` bash
dotnet test
```
