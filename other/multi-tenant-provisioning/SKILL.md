---
name: multi-tenant-provisioning
description: >
  Use when provisioning multi-tenant infrastructure, setting up tenant isolation,
  managing tenant lifecycles, or handling tenant-specific resource allocation.
  This skill provides standardized patterns for multi-tenant SaaS operations.
---

# Multi-Tenant Provisioning - Shared Skill

## Overview
This skill provides standardized patterns and procedures for multi-tenant SaaS provisioning, ensuring consistent tenant isolation and resource management across all companies.

## When to Use
- When setting up new tenant infrastructure
- When configuring tenant isolation patterns
- When managing tenant resource allocation
- When planning tenant scaling
- When implementing tenant security

## Core Procedures

### Tenant Isolation Patterns

#### Schema-Based Isolation (PostgreSQL)
```sql
-- Tenant namespace using schemas
CREATE SCHEMA tenant_{tenant_id};
ALTER DATABASE SET search_path = tenant_{tenant_id};

-- Row-level security
CREATE POLICY tenant_isolation ON data_table
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

#### Database-Per-Tenant
```
Each tenant gets:
├── companya-db (PostgreSQL instance)
├── companya-cache (Redis)
├── companya-storage (S3 bucket)
```

### Tenant Provisioning Workflow
1. **Tenant Creation** - Create tenant record in master database
2. **Schema/DB Creation** - Create isolated database resources
3. **Resource Allocation** - Allocate compute/storage based on plan
4. **Initial Data** - Seed initial tenant data
5. **Configuration** - Set tenant-specific settings
6. **Health Check** - Verify tenant environment

### Resource Allocation by Plan
```yaml
plans:
  starter:
    compute: 0.5 CPU, 512MB RAM
    storage: 5GB
    database: shared with RLS
    support: email
  
  professional:
    compute: 1 CPU, 1GB RAM
    storage: 25GB
    database: dedicated schema
    support: priority email
  
  enterprise:
    compute: 2 CPU, 4GB RAM
    storage: 100GB
    database: dedicated database
    support: dedicated support
    sla: 99.9%
```

## Security Patterns

### Zero Trust Tenant Isolation
```yaml
security:
  network_isolation:
    - private networking between tenant resources
    - no cross-tenant network access
    - encrypted inter-service communication
  
  data_isolation:
    - encryption at rest per tenant
    - encryption in transit
    - key management per tenant
  
  access_control:
    - tenant-scoped authentication
    - least privilege principles
    - audit logging per tenant
```

### Compliance Requirements
- GDPR: Data residency per region
- SOC 2: Access controls and audit
- HIPAA: Healthcare data isolation (optional)
- PCI DSS: Payment data segregation (optional)

## Scaling Patterns

### Horizontal Scaling
```yaml
scaling:
  auto_scale:
    enabled: true
    min_instances: 1
    max_instances: 10
    target_cpu: 70%
    scale_up_cooldown: 300s
    scale_down_cooldown: 600s
  
  load_balancing:
    - round robin for even distribution
    - sticky sessions for authenticated users
    - health check-based routing
```

### Multi-Region Deployment
```
Global Architecture:
├── US East (primary)
│   └── tenant US-based customers
├── EU West (GDPR compliance)
│   └── tenant EU-based customers
└── AP South (optional)
    └── tenant APAC customers
```

## Monitoring & Observability

### Tenant Metrics
```yaml
metrics:
  per_tenant:
    - request_count
    - error_rate
    - latency_p95
    - resource_usage
    - active_users
  
  alerting:
    - error_rate > 1%
    - latency_p95 > 500ms
    - resource_usage > 80%
```

### Audit Logging
```yaml
audit:
  log_per_tenant: true
  retention: 90 days
  events:
    - authentication
    - data_access
    - configuration_changes
    - resource_operations
```

## Error Handling

### Tenant Resource Exhaustion
- **Response:** Alert tenant, implement throttling
- **Escalation:** Auto-upgrade recommendation
- **Prevention:** Proactive capacity monitoring

### Cross-Tenant Data Leakage
- **Response:** IMMEDIATE incident response
- **Isolation:** Isolate affected tenant
- **Notification:** Alert security team
- **Remediation:** Full audit and fix
