---
name: tenancy-models
description: Use when choosing multi-tenant architecture patterns. Covers Pool (shared), Silo (isolated), and Bridge (hybrid) models with decision frameworks for isolation, cost, and scale trade-offs.
allowed-tools: Read, Glob, Grep, Task
---

# Multi-Tenancy Models

Architecture patterns for deploying multi-tenant SaaS applications, from fully shared to fully isolated.

## When to Use This Skill

- Designing a new SaaS application
- Choosing between shared and dedicated infrastructure
- Evaluating isolation vs cost trade-offs
- Planning tenant tiering strategy
- Migrating from single-tenant to multi-tenant

## Core Concept

```text
Multi-tenancy spectrum:

Fully Shared (Pool)              Hybrid (Bridge)              Fully Isolated (Silo)
     ◄──────────────────────────────────────────────────────────────►
   Low Cost                                                      High Cost
   Low Isolation                                                 High Isolation
   High Density                                                  Low Density
   Noisy Neighbor Risk                                           No Interference
```

## The Three Models

### Pool Model (Shared Everything)

```text
┌─────────────────────────────────────────────────────┐
│                   Application Layer                  │
│    All tenants share compute, storage, database      │
├─────────────────────────────────────────────────────┤
│                     Database                         │
│  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐  │
│  │ T1  │ T2  │ T3  │ T4  │ T5  │ T6  │ T7  │ ... │  │
│  └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘  │
│           (Row-Level Security separates data)        │
└─────────────────────────────────────────────────────┘

Characteristics:
- Single database, shared schema
- Row-level security for isolation
- All tenants share compute resources
- Lowest cost per tenant
- Highest tenant density (millions possible)
```

**Best For:**

- B2C SaaS with many small tenants
- Startup MVP (minimize infrastructure)
- Cost-sensitive markets
- Low compliance requirements

**Challenges:**

- Noisy neighbor problems
- Single point of failure
- Complex schema migrations
- Limited customization per tenant

### Silo Model (Fully Isolated)

```text
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│    Tenant A      │  │    Tenant B      │  │    Tenant C      │
│  ┌────────────┐  │  │  ┌────────────┐  │  │  ┌────────────┐  │
│  │    App     │  │  │  │    App     │  │  │  │    App     │  │
│  ├────────────┤  │  │  ├────────────┤  │  │  ├────────────┤  │
│  │  Database  │  │  │  │  Database  │  │  │  │  Database  │  │
│  └────────────┘  │  │  └────────────┘  │  │  └────────────┘  │
└──────────────────┘  └──────────────────┘  └──────────────────┘

Characteristics:
- Dedicated resources per tenant
- Complete data isolation
- Independent scaling
- Independent maintenance windows
- Highest cost per tenant
```

**Best For:**

- Enterprise B2B with strict compliance
- Regulated industries (healthcare, finance)
- Tenants requiring custom SLAs
- Data sovereignty requirements
- High-value customers justifying cost

**Challenges:**

- High infrastructure cost
- Operational complexity at scale
- Tenant onboarding latency
- Resource underutilization

### Bridge Model (Hybrid)

```text
┌─────────────────────────────────────────────────────────────────┐
│                        Shared Services                          │
│     (Authentication, Billing, Monitoring, Configuration)        │
└─────────────────────────────────────────────────────────────────┘
                    │                       │
        ┌───────────┴───────────┐   ┌───────┴───────┐
        │   Pooled Tier         │   │  Premium Tier │
        │  ┌────┬────┬────┐     │   │  ┌─────────┐  │
        │  │ T1 │ T2 │ T3 │     │   │  │ Tenant  │  │
        │  └────┴────┴────┘     │   │  │  (Silo) │  │
        │  (Shared Database)    │   │  └─────────┘  │
        └───────────────────────┘   └───────────────┘

Characteristics:
- Shared control plane
- Mix of pool and silo at data plane
- Tenant tiering (Standard = Pool, Premium = Silo)
- Gradual migration path from pool to silo
```

**Best For:**

- Growth-stage SaaS with diverse customer base
- Companies offering standard and enterprise tiers
- Migration from pool to silo
- Balancing cost with enterprise requirements

## Decision Framework

### Quick Decision Tree

```text
                    Start
                      │
          ┌───────────┴───────────┐
          │  Strict compliance    │
          │  requirements?        │
          └───────────┬───────────┘
                Yes ──┤──── No
                  │         │
             ┌────▼────┐    │
             │  SILO   │    │
             └─────────┘    │
                      ┌─────▼─────┐
                      │ >10,000   │
                      │ tenants?  │
                      └─────┬─────┘
                    Yes ────┤──── No
                      │           │
                 ┌────▼────┐ ┌────▼────┐
                 │  POOL   │ │ BRIDGE  │
                 └─────────┘ └─────────┘
```

### Weighted Decision Matrix

| Factor | Weight | Pool Score | Silo Score | Bridge Score |
| ------ | ------ | ---------- | ---------- | ------------ |
| Cost Efficiency | 25% | 5 | 1 | 3 |
| Tenant Isolation | 20% | 2 | 5 | 4 |
| Scalability | 20% | 5 | 3 | 4 |
| Operational Simplicity | 15% | 4 | 2 | 3 |
| Customization | 10% | 2 | 5 | 4 |
| Compliance Fit | 10% | 2 | 5 | 4 |

### Model Comparison

| Aspect | Pool | Silo | Bridge |
| ------ | ---- | ---- | ------ |
| **Scale** | 1-1,000,000+ | 1-1,000s | 1-100,000s |
| **Cost per Tenant** | Lowest | Highest | Variable |
| **Isolation** | Low (logical) | Complete | Tiered |
| **Noisy Neighbor Risk** | High | None | Varies by tier |
| **Onboarding Speed** | Instant | Minutes-Hours | Varies by tier |
| **Schema Customization** | None | Full | Limited/Full |
| **Compliance** | Shared controls | Dedicated | Hybrid |
| **Operational Complexity** | Low | High at scale | Medium |

## Implementation Patterns

### Pool Model Implementation

```text
Key Components:
1. Tenant Resolver Middleware
   - Extract tenant from subdomain, header, or JWT claim
   - Set tenant context for request

2. Row-Level Security
   - Database-level isolation (SQL Server RLS, PostgreSQL RLS)
   - All queries filtered by tenant_id

3. Shared Connection Pool
   - Single connection string
   - Tenant context passed per-request

4. Global Query Filters (EF Core)
   - Automatic tenant filtering on all entities
```

See `database-isolation` skill for implementation details.

### Silo Model Implementation

```text
Key Components:
1. Tenant Routing
   - DNS-based (tenant.app.com)
   - API Gateway routing by tenant identifier

2. Dedicated Infrastructure
   - Database per tenant
   - Optionally dedicated compute

3. Tenant Catalog
   - Central registry of tenant configurations
   - Connection strings, feature flags, customizations

4. Infrastructure as Code
   - Automated provisioning (Terraform, Bicep)
   - Template-based tenant environments
```

See `tenant-provisioning` skill for implementation details.

### Bridge Model Implementation

```text
Key Components:
1. Tiered Tenant Classification
   - Standard tier → Pool
   - Premium tier → Silo

2. Unified Control Plane
   - Single admin portal
   - Central configuration management
   - Aggregated monitoring

3. Data Plane Routing
   - Route to pool or silo based on tier
   - Seamless upgrade path (pool → silo)

4. Migration Support
   - Data export from pool
   - Import to dedicated resources
   - Zero-downtime migration
```

## Cloud Provider Considerations

### Azure

| Model | Services |
| ----- | -------- |
| Pool | Azure SQL with RLS, Elastic Pools |
| Silo | SQL Database per tenant, Cosmos DB account per tenant |
| Bridge | Mix of above, Azure Front Door for routing |

### AWS

| Model | Services |
| ----- | -------- |
| Pool | RDS PostgreSQL with RLS, DynamoDB with partition key |
| Silo | RDS per tenant, isolated VPCs |
| Bridge | Mix of above, API Gateway for routing |

### Cosmos DB Specific

| Isolation Level | Pattern | Cost | Isolation |
| --------------- | ------- | ---- | --------- |
| Partition key per tenant | Shared container | Lowest | Logical |
| Container per tenant | Shared database | Medium | Container RBAC |
| Database per tenant | Shared account | Higher | Database RBAC |
| Account per tenant | Dedicated account | Highest | Complete |

## Evolution Path

### Startup to Enterprise

```text
Phase 1: MVP (Pool)
└── Single database, RLS
└── Minimize costs
└── Validate product-market fit

Phase 2: Growth (Bridge)
└── Introduce premium tier (Silo)
└── Keep standard tier (Pool)
└── First enterprise customers

Phase 3: Scale (Optimized Bridge)
└── Cell-based architecture
└── Regional deployment
└── Per-tenant SLA options
```

### Migration Triggers

Move from **Pool → Bridge** when:

- First enterprise customer requires isolation
- Compliance requirements emerge
- Noisy neighbor problems occur

Move from **Bridge → More Silo** when:

- Premium revenue justifies infrastructure
- Enterprise segment grows
- Per-tenant customization demand increases

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
| ------------ | ------- | -------- |
| Over-isolation early | High cost, slow development | Start with pool, migrate later |
| No tenant context | Data leakage risk | Always validate tenant context |
| Shared secrets | Cross-tenant access | Tenant-scoped encryption keys |
| Global caching | Cache pollution | Tenant-prefixed cache keys |
| Synchronous provisioning | Slow onboarding | Async provisioning with status |

## Best Practices

```text
1. Tenant Context is Sacred
   - Validate on every request
   - Never assume tenant from client input
   - Log tenant ID with every operation

2. Defense in Depth
   - Application-level filtering
   - Database-level RLS
   - Network-level isolation (for silo)

3. Observability per Tenant
   - Metrics tagged by tenant
   - Per-tenant dashboards
   - Alerting thresholds per tier

4. Cost Attribution
   - Track resource usage per tenant
   - Enable chargebacks for enterprise
   - Monitor for cost anomalies

5. Test Isolation
   - Automated cross-tenant access tests
   - Penetration testing for isolation
   - Chaos testing for noisy neighbor
```

## Related Skills

- `database-isolation` - Implementation patterns for data isolation
- `tenant-context-propagation` - Context resolution in microservices
- `noisy-neighbor-prevention` - Resource isolation techniques
- `tenant-provisioning` - Automated tenant onboarding

## References

- Load `references/pool-model.md` for detailed Pool implementation
- Load `references/silo-model.md` for detailed Silo implementation
- Load `references/bridge-model.md` for detailed Bridge implementation
- AWS Well-Architected SaaS Lens: <https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/>
- Azure Multi-tenant patterns: <https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/>

---

**Last Updated:** 2025-12-26
