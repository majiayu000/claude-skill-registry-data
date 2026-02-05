---
name: data-residency
description: Data residency and geo-fencing patterns for SaaS compliance. Covers regional deployment, data sovereignty, and cross-border data transfer.
allowed-tools: Read, Glob, Grep, Task, mcp__perplexity__search, mcp__perplexity__reason, mcp__microsoft-learn__microsoft_docs_search, mcp__microsoft-learn__microsoft_docs_fetch
---

# Data Residency Skill

## When to Use This Skill

Use this skill when:

- **Data Residency tasks** - Working on data residency and geo-fencing patterns for saas compliance. covers regional deployment, data sovereignty, and cross-border data transfer
- **Planning or design** - Need guidance on Data Residency approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Patterns for implementing data residency requirements in multi-tenant SaaS applications.

Data residency ensures that tenant data is stored and processed within specific geographic boundaries. This is critical for compliance with regulations like GDPR (EU), LGPD (Brazil), PIPL (China), and various industry requirements.

## Residency Requirements by Region

```text
+------------------------------------------------------------------+
|                  Data Residency Requirements                      |
+------------------------------------------------------------------+
| Region/Law    | Requirement               | Impact                |
+---------------+---------------------------+-----------------------+
| EU (GDPR)     | EU data stays in EU       | EU infrastructure     |
| Germany       | Stricter than GDPR        | German data centers   |
| Brazil (LGPD) | Brazil data in Brazil     | Brazil region         |
| China (PIPL)  | China data in China       | China-specific setup  |
| Russia        | Russia data in Russia     | Local hosting only    |
| Australia     | Government data local     | AU region for gov     |
| Canada        | Some sectors require local| CA region option      |
| Singapore     | PDPA requirements         | SG region preferred   |
+---------------+---------------------------+-----------------------+
```

## Architecture Patterns

### Multi-Region Deployment

```text
+------------------------------------------------------------------+
|                 Multi-Region Architecture                         |
+------------------------------------------------------------------+
|                                                                   |
|  +-------------+         +-------------+         +-------------+  |
|  | US Region   |         | EU Region   |         | APAC Region |  |
|  | us-east-1   |         | eu-west-1   |         | ap-south-1  |  |
|  +-------------+         +-------------+         +-------------+  |
|  | App Servers |         | App Servers |         | App Servers |  |
|  | Database    |         | Database    |         | Database    |  |
|  | Storage     |         | Storage     |         | Storage     |  |
|  | Backups     |         | Backups     |         | Backups     |  |
|  +-------------+         +-------------+         +-------------+  |
|         |                       |                       |         |
|         +--------+    +---------+    +--------+---------+         |
|                  |    |              |                            |
|            +-----v----v--------------v-----+                      |
|            |    Global Control Plane       |                      |
|            |    (routing, auth, billing)   |                      |
|            +-------------------------------+                      |
|                                                                   |
+------------------------------------------------------------------+
```

### Tenant Region Assignment

```csharp
public sealed class TenantRegionService(
    IDbContext db,
    IRegionRouter router)
{
    private static readonly Dictionary<string, string> CountryToRegion = new()
    {
        // EU countries
        ["DE"] = "eu-central-1",
        ["FR"] = "eu-west-3",
        ["GB"] = "eu-west-2",
        ["NL"] = "eu-west-1",
        // US
        ["US"] = "us-east-1",
        // APAC
        ["AU"] = "ap-southeast-2",
        ["JP"] = "ap-northeast-1",
        ["SG"] = "ap-southeast-1",
        // LATAM
        ["BR"] = "sa-east-1"
    };

    public async Task<string> AssignRegionAsync(
        Guid tenantId,
        string countryCode,
        CancellationToken ct)
    {
        var region = CountryToRegion.GetValueOrDefault(countryCode, "us-east-1");

        var tenant = await db.Tenants.FindAsync([tenantId], ct);
        if (tenant == null)
            throw new TenantNotFoundException(tenantId);

        tenant.DataRegion = region;
        tenant.DataRegionAssignedAt = DateTimeOffset.UtcNow;

        await db.SaveChangesAsync(ct);

        return region;
    }

    public async Task<bool> CanMigrateToRegionAsync(
        Guid tenantId,
        string targetRegion,
        CancellationToken ct)
    {
        // Check if migration is allowed based on tenant's country/compliance needs
        var tenant = await db.Tenants
            .Include(t => t.ComplianceRequirements)
            .FirstOrDefaultAsync(t => t.Id == tenantId, ct);

        if (tenant == null)
            return false;

        // Check if target region meets compliance requirements
        return tenant.ComplianceRequirements.All(req =>
            IsRegionCompliant(targetRegion, req));
    }
}
```

## Request Routing

### Geo-Aware Router

```csharp
public sealed class GeoRouter(
    ITenantRepository tenants,
    IDistributedCache cache)
{
    public async Task<RegionEndpoint> GetEndpointAsync(
        Guid tenantId,
        CancellationToken ct)
    {
        var cacheKey = $"region:{tenantId}";
        var cached = await cache.GetStringAsync(cacheKey, ct);

        if (cached != null)
        {
            return RegionEndpoint.Parse(cached);
        }

        var tenant = await tenants.GetAsync(tenantId, ct);
        if (tenant == null)
            throw new TenantNotFoundException(tenantId);

        var endpoint = new RegionEndpoint
        {
            Region = tenant.DataRegion,
            ApiUrl = GetApiUrl(tenant.DataRegion),
            DatabaseHost = GetDatabaseHost(tenant.DataRegion)
        };

        await cache.SetStringAsync(cacheKey, endpoint.ToString(),
            new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1)
            }, ct);

        return endpoint;
    }

    private static string GetApiUrl(string region) => region switch
    {
        "eu-west-1" => "https://eu.api.example.com",
        "ap-southeast-1" => "https://ap.api.example.com",
        _ => "https://us.api.example.com"
    };
}
```

### Regional Middleware

```csharp
public sealed class RegionalRoutingMiddleware(
    RequestDelegate next,
    IGeoRouter router,
    ITenantContextAccessor tenantContext)
{
    public async Task InvokeAsync(HttpContext context)
    {
        if (tenantContext.Current == null)
        {
            await next(context);
            return;
        }

        var expectedRegion = await router.GetEndpointAsync(
            tenantContext.Current.TenantId,
            context.RequestAborted);

        var currentRegion = Environment.GetEnvironmentVariable("AWS_REGION");

        if (expectedRegion.Region != currentRegion)
        {
            // Redirect to correct regional endpoint
            context.Response.StatusCode = 307;
            context.Response.Headers.Location = expectedRegion.ApiUrl + context.Request.Path;
            return;
        }

        await next(context);
    }
}
```

## Database Residency

### Regional Database Routing

```csharp
public sealed class RegionalDbContextFactory(
    ITenantContextAccessor tenantContext,
    IRegionalConnectionStrings connections) : IDbContextFactory<AppDbContext>
{
    public async Task<AppDbContext> CreateDbContextAsync(CancellationToken ct)
    {
        var tenant = tenantContext.Current
            ?? throw new InvalidOperationException("No tenant context");

        var connectionString = await connections.GetAsync(tenant.DataRegion, ct);

        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseSqlServer(connectionString)
            .Options;

        return new AppDbContext(options, tenantContext);
    }
}
```

### Cross-Region Restrictions

```csharp
public sealed class DataResidencyValidator(ITenantContext tenant)
{
    public void ValidateDataAccess(string targetRegion)
    {
        if (tenant.DataRegion != targetRegion)
        {
            throw new DataResidencyViolationException(
                $"Tenant data is in {tenant.DataRegion}, cannot access from {targetRegion}");
        }
    }

    public bool CanReplicateTo(string targetRegion)
    {
        // Check if cross-region replication is allowed
        return (tenant.DataRegion, targetRegion) switch
        {
            // EU to EU is allowed
            ("eu-west-1", "eu-central-1") => true,
            ("eu-central-1", "eu-west-1") => true,
            // US to US is allowed
            ("us-east-1", "us-west-2") => true,
            // Cross-continental not allowed by default
            _ => false
        };
    }
}
```

## Storage Residency

### Regional Storage Configuration

```csharp
public sealed class RegionalStorageService(
    ITenantContext tenant,
    IRegionalStorageFactory storageFactory)
{
    public async Task<BlobReference> UploadAsync(
        Stream content,
        string fileName,
        CancellationToken ct)
    {
        var storage = storageFactory.GetStorage(tenant.DataRegion);

        var blobName = $"{tenant.TenantId}/{Guid.NewGuid()}/{fileName}";
        await storage.UploadAsync(blobName, content, ct);

        return new BlobReference
        {
            BlobName = blobName,
            Region = tenant.DataRegion,
            Url = storage.GetUrl(blobName)
        };
    }
}

public sealed class RegionalStorageFactory(IConfiguration config) : IRegionalStorageFactory
{
    public IBlobStorage GetStorage(string region)
    {
        var connectionString = config[$"Storage:{region}:ConnectionString"];
        return new AzureBlobStorage(connectionString);
    }
}
```

## Compliance Metadata

```csharp
public sealed record DataResidencyCompliance
{
    public required Guid TenantId { get; init; }
    public required string DataRegion { get; init; }
    public required DateTimeOffset AssignedAt { get; init; }
    public required List<string> ComplianceFrameworks { get; init; }
    public bool CanMigrateRegion { get; init; } = false;
    public string? MigrationRestrictionReason { get; init; }
    public DateTimeOffset? LastAuditedAt { get; init; }
}

public sealed class DataResidencyAuditService(IDbContext db, IAuditLog audit)
{
    public async Task AuditResidencyComplianceAsync(
        Guid tenantId,
        CancellationToken ct)
    {
        var tenant = await db.Tenants
            .Include(t => t.DataLocations)
            .FirstOrDefaultAsync(t => t.Id == tenantId, ct);

        if (tenant == null) return;

        var violations = new List<string>();

        // Check all data locations match declared region
        foreach (var location in tenant.DataLocations)
        {
            if (!IsWithinRegion(location.StorageRegion, tenant.DataRegion))
            {
                violations.Add($"Data in {location.StorageRegion}, expected {tenant.DataRegion}");
            }
        }

        await audit.LogAsync(new DataResidencyAuditEntry
        {
            TenantId = tenantId,
            AuditedAt = DateTimeOffset.UtcNow,
            DeclaredRegion = tenant.DataRegion,
            Violations = violations,
            IsCompliant = violations.Count == 0
        }, ct);
    }
}
```

## Best Practices

```text
Data Residency Best Practices:
+------------------------------------------------------------------+
| Practice                    | Benefit                            |
+-----------------------------+------------------------------------+
| Early region assignment     | Data never leaves target region   |
| Region in tenant context    | Consistent routing everywhere     |
| Audit trail                 | Compliance evidence               |
| Prevent accidental transfer | Block cross-region API calls      |
| Regional backups            | DR within compliance              |
| Clear customer communication| Set expectations correctly         |
+-----------------------------+------------------------------------+
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| ------------ | ------- | -------- |
| Global database | Compliance violation | Regional databases |
| CDN without geo-fencing | Data leaves region | Regional CDN config |
| Logs to central region | Audit data leaks | Regional logging |
| Backup to different region | Compliance violation | Same-region backups |
| Admin access from anywhere | Access controls | Regional admin |

## Related Skills

- `tenant-provisioning` - Region assignment during provisioning
- `saas-compliance-frameworks` - GDPR, LGPD requirements
- `sharding-strategies` - Regional sharding

## MCP Research

For current patterns:

```text
perplexity: "data residency multi-tenant SaaS 2024" "GDPR data localization"
microsoft-learn: "Azure data residency" "Azure sovereign clouds"
```
