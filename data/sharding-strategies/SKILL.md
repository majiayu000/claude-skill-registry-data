---
name: sharding-strategies
description: Horizontal scaling patterns for multi-tenant databases. Covers shard key selection, consistent hashing, and shard management.
allowed-tools: Read, Glob, Grep, Task, mcp__perplexity__search, mcp__perplexity__reason, mcp__microsoft-learn__microsoft_docs_search, mcp__microsoft-learn__microsoft_docs_fetch
---

# Sharding Strategies Skill

## When to Use This Skill

Use this skill when:

- **Sharding Strategies tasks** - Working on horizontal scaling patterns for multi-tenant databases. covers shard key selection, consistent hashing, and shard management
- **Planning or design** - Need guidance on Sharding Strategies approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Patterns for horizontally scaling multi-tenant databases through sharding.

Sharding distributes tenant data across multiple database instances to achieve horizontal scale. This skill covers shard key selection, routing strategies, and operational considerations for sharded multi-tenant systems.

## Sharding Architectures

```text
+------------------------------------------------------------------+
|                    Sharding Approaches                            |
+------------------------------------------------------------------+
|                                                                   |
|  Tenant-per-Shard          Tenant-per-Database       Hash-Based  |
|  +--------+                +--------+              +----------+  |
|  |Shard 1 |                | DB 1   |              | Shard 1  |  |
|  |T1,T2,T3|                | Tenant |              | Hash 0-25|  |
|  +--------+                +--------+              +----------+  |
|  |Shard 2 |                | DB 2   |              | Shard 2  |  |
|  |T4,T5,T6|                | Tenant |              | Hash 26-50| |
|  +--------+                +--------+              +----------+  |
|                                                                   |
|  Good for pooled          Good for silo            Good for even |
|  tenants                  tenants                  distribution  |
+------------------------------------------------------------------+
```

## Shard Key Selection

### Key Selection Criteria

```text
Shard Key Considerations:
+------------------------------------------------------------------+
| Criterion          | Good Key                | Bad Key           |
+--------------------+-------------------------+-------------------+
| Cardinality        | TenantId (many values)  | Status (few vals) |
| Distribution       | UUID (even)             | Created date (hot)|
| Query patterns     | Always in WHERE         | Optional filter   |
| Stability          | Immutable               | Can change        |
| Cross-shard joins  | Rarely needed           | Frequently needed |
+--------------------+-------------------------+-------------------+
```

### Recommended: Tenant ID as Shard Key

```csharp
public sealed class ShardKeyResolver
{
    public string GetShardKey(Guid tenantId)
    {
        // TenantId is the natural shard key for multi-tenant systems
        return tenantId.ToString();
    }

    public int GetShardIndex(Guid tenantId, int shardCount)
    {
        // Consistent hashing using tenant ID
        var hash = GetStableHash(tenantId);
        return Math.Abs(hash) % shardCount;
    }

    private static int GetStableHash(Guid guid)
    {
        // Use first 4 bytes of GUID for stable hash
        var bytes = guid.ToByteArray();
        return BitConverter.ToInt32(bytes, 0);
    }
}
```

## Routing Strategies

### Lookup-Based Routing

```csharp
public sealed class ShardRouter(
    IDistributedCache cache,
    IShardMapRepository shardMap)
{
    public async Task<string> GetConnectionStringAsync(
        Guid tenantId,
        CancellationToken ct = default)
    {
        var cacheKey = $"shard:{tenantId}";
        var cached = await cache.GetStringAsync(cacheKey, ct);

        if (cached != null)
            return cached;

        var mapping = await shardMap.GetMappingAsync(tenantId, ct);
        if (mapping == null)
            throw new TenantNotFoundException(tenantId);

        await cache.SetStringAsync(cacheKey, mapping.ConnectionString,
            new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1)
            }, ct);

        return mapping.ConnectionString;
    }
}
```

### Consistent Hashing

```csharp
public sealed class ConsistentHashRing<T>
{
    private readonly SortedDictionary<int, T> _ring = new();
    private readonly int _virtualNodes;

    public ConsistentHashRing(int virtualNodes = 100)
    {
        _virtualNodes = virtualNodes;
    }

    public void AddNode(T node)
    {
        for (var i = 0; i < _virtualNodes; i++)
        {
            var hash = GetHash($"{node}:{i}");
            _ring[hash] = node;
        }
    }

    public void RemoveNode(T node)
    {
        for (var i = 0; i < _virtualNodes; i++)
        {
            var hash = GetHash($"{node}:{i}");
            _ring.Remove(hash);
        }
    }

    public T GetNode(string key)
    {
        if (_ring.Count == 0)
            throw new InvalidOperationException("Ring is empty");

        var hash = GetHash(key);

        // Find first node with hash >= key hash
        foreach (var kvp in _ring)
        {
            if (kvp.Key >= hash)
                return kvp.Value;
        }

        // Wrap around to first node
        return _ring.First().Value;
    }

    private static int GetHash(string key)
    {
        using var md5 = MD5.Create();
        var hash = md5.ComputeHash(Encoding.UTF8.GetBytes(key));
        return BitConverter.ToInt32(hash, 0);
    }
}
```

## Shard Management

### Shard Map

```csharp
public sealed record ShardMapping
{
    public required Guid TenantId { get; init; }
    public required int ShardId { get; init; }
    public required string ConnectionString { get; init; }
    public required DateTimeOffset AssignedAt { get; init; }
    public ShardStatus Status { get; init; } = ShardStatus.Active;
}

public enum ShardStatus
{
    Active,
    ReadOnly,
    Migrating,
    Offline
}

public sealed class ShardMapService(IDbContext db)
{
    public async Task<ShardMapping> AssignTenantAsync(
        Guid tenantId,
        CancellationToken ct)
    {
        // Find shard with lowest tenant count
        var targetShard = await db.Shards
            .Where(s => s.Status == ShardStatus.Active)
            .OrderBy(s => s.TenantCount)
            .FirstOrDefaultAsync(ct)
            ?? throw new NoAvailableShardsException();

        var mapping = new ShardMapping
        {
            TenantId = tenantId,
            ShardId = targetShard.Id,
            ConnectionString = targetShard.ConnectionString,
            AssignedAt = DateTimeOffset.UtcNow
        };

        db.ShardMappings.Add(mapping);
        targetShard.TenantCount++;

        await db.SaveChangesAsync(ct);

        return mapping;
    }
}
```

### Shard Rebalancing

```csharp
public sealed class ShardRebalancer(
    IShardMapService shardMap,
    IDataMigrator migrator,
    ILogger<ShardRebalancer> logger)
{
    public async Task RebalanceAsync(CancellationToken ct)
    {
        var shards = await shardMap.GetAllShardsAsync(ct);
        var avgTenants = shards.Average(s => s.TenantCount);
        var threshold = avgTenants * 0.2; // 20% variance allowed

        var overloaded = shards.Where(s => s.TenantCount > avgTenants + threshold);
        var underloaded = shards.Where(s => s.TenantCount < avgTenants - threshold);

        foreach (var source in overloaded)
        {
            var target = underloaded.FirstOrDefault();
            if (target == null) break;

            var tenantsToMove = (int)((source.TenantCount - avgTenants) / 2);

            logger.LogInformation(
                "Moving {Count} tenants from shard {Source} to {Target}",
                tenantsToMove, source.Id, target.Id);

            await MoveTenantsAsync(source, target, tenantsToMove, ct);
        }
    }
}
```

## Cross-Shard Queries

### Fan-Out Pattern

```csharp
public sealed class CrossShardQueryService(
    IShardRouter router,
    IDbContextFactory<AppDbContext> dbFactory)
{
    public async Task<List<TResult>> QueryAllShardsAsync<TResult>(
        Func<AppDbContext, Task<List<TResult>>> query,
        CancellationToken ct)
    {
        var shards = await router.GetAllShardsAsync(ct);
        var tasks = shards.Select(async shard =>
        {
            await using var context = await dbFactory.CreateDbContextAsync(ct);
            context.Database.SetConnectionString(shard.ConnectionString);
            return await query(context);
        });

        var results = await Task.WhenAll(tasks);
        return results.SelectMany(r => r).ToList();
    }
}

// Usage
var allUsers = await _crossShard.QueryAllShardsAsync(
    db => db.Users.Where(u => u.IsAdmin).ToListAsync(),
    ct);
```

### Aggregation Pattern

```csharp
public async Task<GlobalStats> GetGlobalStatsAsync(CancellationToken ct)
{
    var shardStats = await _crossShard.QueryAllShardsAsync(
        async db => new ShardStats
        {
            TenantCount = await db.Tenants.CountAsync(),
            UserCount = await db.Users.CountAsync(),
            TotalStorage = await db.Storage.SumAsync(s => s.SizeBytes)
        },
        ct);

    return new GlobalStats
    {
        TotalTenants = shardStats.Sum(s => s.TenantCount),
        TotalUsers = shardStats.Sum(s => s.UserCount),
        TotalStorage = shardStats.Sum(s => s.TotalStorage)
    };
}
```

## Shard Splitting

```text
Shard Split Process:
+------------------------------------------------------------------+
| Step | Action                           | Downtime | Risk        |
+------+----------------------------------+----------+-------------+
| 1    | Create new shard                 | None     | Low         |
| 2    | Set source shard to read-only    | Partial  | Low         |
| 3    | Copy data to new shard           | None     | Medium      |
| 4    | Update shard map (atomic)        | Brief    | Medium      |
| 5    | Validate data consistency        | None     | Low         |
| 6    | Enable writes on both shards     | None     | Low         |
| 7    | Delete data from source          | None     | Low         |
+------+----------------------------------+----------+-------------+
```

## Best Practices

```text
Sharding Best Practices:
+------------------------------------------------------------------+
| Practice                    | Benefit                            |
+-----------------------------+------------------------------------+
| TenantId as shard key       | Natural partitioning               |
| Consistent hashing          | Minimal reshuffling on scale       |
| Shard map caching           | Reduce routing latency             |
| Monitor shard size          | Proactive rebalancing              |
| Avoid cross-shard joins     | Performance, complexity            |
| Plan for splits early       | Easier at smaller sizes            |
+-----------------------------+------------------------------------+
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| ------------ | ------- | -------- |
| Too few shards | Hard to scale later | Start with more |
| Cross-shard transactions | Complexity, failures | Denormalize data |
| Manual shard assignment | Error-prone | Automate routing |
| No rebalancing | Hotspots | Automated rebalancing |
| Timestamp shard key | All writes to one shard | Use tenant ID |

## Related Skills

- `database-isolation` - Single-shard isolation options
- `tenant-provisioning` - Shard assignment on provisioning
- `noisy-neighbor-prevention` - Per-shard resource limits

## MCP Research

For current patterns:

```text
perplexity: "database sharding strategies 2024" "consistent hashing multi-tenant"
microsoft-learn: "Azure SQL elastic pools sharding" "Cosmos DB partitioning"
```
