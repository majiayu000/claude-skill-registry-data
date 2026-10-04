---
model_tier: medium
name: multi-tenancy
description: "Use when working with the multi-tenant architecture — customer DB switching, FQDN routing, tenant isolation, or cross-tenant operations."
domain: engineering
framework: laravel
workspaces:
  - engineering
packs:
  - engineering-base
triggers:
  - phrase: "tenant isolation"
  - phrase: "cross-tenant"
  - phrase: "tenant scoping"
---

<!-- Framework scope: Laravel only. Uses Eloquent model conventions,
     Laravel Context, and Artisan traits — concepts not portable across
     frameworks. Other stacks need a stack-native multi-tenancy skill. -->

# multi-tenancy

## When to use

Use this skill when working with tenant-specific data, customer database connections, or any code that touches the dual-database architecture.


Do NOT use when:
- Single-database applications
- Frontend-only changes

## Procedure: Work with multi-tenancy

1. **Gather context** — read `agents/reference/docs/` for multi-tenant architecture, `config/database.php` for connection definitions, and search for the tenant switching service.
2. **Identify connection** — determine whether the code touches central, tenant, or both databases. Set `$connection` explicitly on any new model.
3. **Implement** — write the feature using the correct connection. Use the tenant switching service for cross-tenant operations. Never mix connections in a single query.
4. **Verify isolation** — inspect the code for tenant leaks: global scopes, missing `$connection`, shared caches, or job serialization without tenant context.
5. **Test** — write a test that exercises the tenant boundary: seed tenant-specific data, switch context, verify correct data is returned and other tenants' data is invisible.

## Architecture overview

```
Request → Identify Tenant (JWT / subdomain / API key)
        → Lookup credentials from central database
        → Reconfigure tenant connection at runtime
        → All tenant queries use tenant connection
```

### Dual-database pattern

| Connection type | Purpose | Scope |
|---|---|---|
| Central / shared | Global data — tenants, config, shared resources | Shared across all tenants |
| Tenant / customer | Tenant-specific data — domain entities | One per tenant |

The central connection is typically the **default connection**.
The tenant connection starts **empty** and is configured dynamically per request.

### Additional connections

Projects may have additional connections for admin operations, provisioning, or monitoring. Check `config/database.php`.

## Core tenant switching service

**Scope**: Laravel-specific (see frontmatter). For non-Laravel multi-tenant systems, the concepts below still apply but the implementation differs — consult the framework's connection / session / DI conventions.

Search the codebase for the service responsible for tenant switching. Typical responsibilities:

1. Store tenant context (e.g., in Laravel Context or a singleton)
2. Load tenant configuration
3. Set monitoring context (tenant ID, name, domain)
4. Reconfigure the database connection with tenant credentials
5. Bind tenant-specific services via the container

## Model conventions

### Setting `$connection`

Every model **must** explicitly set its connection:

```php
// Central models
class Tenant extends Model
{
    protected $connection = 'central_database';
}

// Tenant models
class Project extends Model
{
    protected $connection = 'tenant_database';
}
```

Check the project for the actual connection names and namespace conventions.

## Tenant isolation rules

- **Never query the tenant connection before the tenant is set.**
- **Never mix connections in a single query** — use explicit joins or separate queries.
- **Always specify `$connection`** on new models — never rely on the default.
- **Use transactions per connection** — `DB::connection('tenant_database')->transaction(...)`.
- **Artisan commands** that need tenant access must use the appropriate trait (search for it in the project).

## Testing with tenants

- Tests use dedicated tenant seeders (check `agents/reference/docs/` for seeder conventions).
- The testing database may consolidate multiple connections into a single DB for simplicity.
- Use `RefreshDatabase` or manual seeding — never assume a specific tenant state from previous tests.

## Common pitfalls

| Problem | Solution |
|---|---|
| Query on `customer_database` returns empty | Customer not set yet — check middleware order |
| Race condition in parallel tests | Each test process gets its own DB (parallel testing with separate DBs) |
| Wrong tenant data in background jobs | Serialize customer ID, re-resolve in job's `handle()` method |
| Migration on wrong connection | Specify `--database=customer_database` or set `$connection` in migration |


## Output format

1. Tenant-aware code with correct DB connection switching
2. Verification that tenant isolation is maintained

## Auto-trigger keywords

- multi-tenant
- tenant isolation
- customer database
- FQDN routing

## Gotcha

- Always verify which database connection is active before running queries — cross-tenant data leaks are critical bugs.
- The model forgets to switch back to the main connection after tenant operations.
- Queue jobs serialize the connection state — ensure the tenant context is restored when the job runs.
- Don't use `DB::connection()` directly — use the tenant switching helpers.

## Do NOT

- Do NOT hardcode database names — always use connection names.
- Do NOT assume `customer_database` is available in service providers or early boot.
- Do NOT access tenant data in global middleware that runs before customer identification.
- Do NOT store tenant DB credentials in code — they come from the `customer_databases` table.
