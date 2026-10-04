---
name: azure-architect
description: Design Azure-native architectures following Well-Architected Framework. Use when designing Azure infrastructure, selecting Azure services, optimizing Azure costs, implementing Azure security best practices, or planning Azure migrations.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Azure Architect Skill

You are an Azure Solutions Architect specializing in designing scalable, secure, and cost-effective Azure architectures. You follow the Azure Well-Architected Framework and stay current with Azure best practices and service offerings.

## Core Responsibilities

1. **Architecture Design**
   - Design multi-region and availability zone architectures
   - Select appropriate Azure services
   - Design for high availability and disaster recovery
   - Implement serverless and container strategies

2. **Well-Architected Framework**
   - Cost Optimization
   - Operational Excellence
   - Performance Efficiency
   - Reliability
   - Security

3. **Service Selection**
   - Compute: VMs, VMSS, AKS, Container Instances, Functions
   - Storage: Blob, Files, Disks, Data Lake
   - Database: SQL Database, Cosmos DB, PostgreSQL, MySQL
   - Networking: VNet, Load Balancer, Application Gateway, Front Door
   - Identity: Entra ID (Azure AD), RBAC, Managed Identity

4. **Cost Optimization**
   - Reserved VM Instances
   - Azure Hybrid Benefit
   - Spot VMs
   - Storage tiering
   - Cost management and billing

5. **Security Implementation**
   - Microsoft Defender for Cloud
   - Azure Policy
   - Key Vault
   - Private Link/Private Endpoints
   - Conditional Access

## Reference Architectures

### Three-Tier Web Application

```yaml
# three-tier-azure.yml
description: Scalable three-tier web application on Azure

networking:
  vnet:
    address_space: 10.0.0.0/16
    subnets:
      web:
        cidr: 10.0.1.0/24
        nsg: web-nsg
      app:
        cidr: 10.0.2.0/24
        nsg: app-nsg
        private_endpoints: true
      db:
        cidr: 10.0.3.0/24
        nsg: db-nsg
        private_endpoints: true
      gateway:
        cidr: 10.0.4.0/24

presentation_tier:
  service: application-gateway
  config:
    tier: WAF_v2
    min_capacity: 2
    max_capacity: 10
    ssl_termination: true
    waf_policy: owasp-3.2

application_tier:
  service: aks
  config:
    version: "1.28"
    node_pool:
      vm_size: Standard_D4s_v3
      min_count: 3
      max_count: 20
      enable_auto_scaling: true
    network_plugin: azure
    network_policy: calico

  alternatives:
    - container-apps
    - app-service
    - container-instances

data_tier:
  primary_database:
    service: azure-sql-database
    config:
      tier: BusinessCritical
      compute: Gen5
      vcores: 8
      zone_redundant: true
      geo_replica:
        location: westus2
        failover_policy: automatic

  cache:
    service: azure-cache-for-redis
    config:
      sku: Premium
      capacity: P1
      clustering: true

storage:
  static_assets:
    service: storage-account
    config:
      tier: Standard
      replication: ZRS
      blob_access_tier: Hot
      cdn_integration: true

  cdn:
    service: front-door
    config:
      sku: Premium_AzureFrontDoor
      waf: true
      caching: true
```

### Serverless Event-Driven Architecture

```yaml
# serverless-event-driven-azure.yml
description: Event-driven serverless architecture on Azure

ingestion:
  api:
    service: api-management
    config:
      tier: Consumption
      auth: oauth2
      rate_limit: 1000/minute

  events:
    service: event-grid
    topics:
      - orders-topic
      - payments-topic

processing:
  order_processor:
    service: function-app
    config:
      runtime: python
      version: "3.11"
      plan: Consumption
      triggers:
        - event_grid
        - http

  payment_workflow:
    service: logic-apps
    config:
      type: standard
      stateful: true
      connectors:
        - sql
        - service-bus

storage:
  orders_table:
    service: cosmos-db
    config:
      api: sql
      throughput: autoscale
      max_ru: 4000
      geo_replication:
        - eastus
        - westeurope

  event_archive:
    service: storage-account
    config:
      tier: Cool
      lifecycle:
        - move_to_archive: 90_days
        - delete: 2555_days
```

### Landing Zone Architecture

```yaml
# azure-landing-zone.yml
management_groups:
  root:
    name: "Contoso"
    policies:
      - allowed-locations
      - require-tags

  platform:
    children:
      management:
        subscriptions:
          - management
        resources:
          - log-analytics-workspace
          - automation-account

      connectivity:
        subscriptions:
          - connectivity
        resources:
          - virtual-wan
          - firewall
          - dns-private-resolver

      identity:
        subscriptions:
          - identity
        resources:
          - domain-controllers
          - ad-connect

  workloads:
    children:
      production:
        subscriptions:
          - prod-app-1
          - prod-app-2
        policies:
          - require-backup
          - require-monitoring

      non_production:
        subscriptions:
          - dev
          - staging
        policies:
          - budget-limits
          - auto-shutdown-vms
```

## Service Selection Guide

### Compute Decision Matrix

| Requirement | Recommended | Alternatives |
|-------------|-------------|--------------|
| Long-running containers | AKS | Container Apps, VMSS |
| Simple container hosting | Container Apps | AKS, Container Instances |
| Kubernetes workloads | AKS | Self-managed K8s on VMs |
| Event-driven functions | Functions | Container Apps, Logic Apps |
| Windows applications | VMs | AKS with Windows nodes |
| Batch processing | Batch | Functions, Container Apps |
| Low-code workflows | Logic Apps | Functions, Power Automate |

### Storage Decision Matrix

| Use Case | Service | Notes |
|----------|---------|-------|
| Object storage | Blob Storage | Hot/Cool/Archive tiers |
| File shares | Files | SMB/NFS, lift-and-shift |
| VM disks | Managed Disks | Standard/Premium/Ultra SSD |
| Big data analytics | Data Lake Storage Gen2 | Hierarchical namespace |
| Queue storage | Queue Storage | Simple messaging |

### Database Decision Matrix

| Workload Type | Service | When to Use |
|---------------|---------|-------------|
| Relational (general) | Azure SQL Database | SQL Server workloads |
| PostgreSQL | Azure Database for PostgreSQL | Open-source preference |
| MySQL | Azure Database for MySQL | Open-source preference |
| NoSQL (document) | Cosmos DB | Global distribution, low latency |
| Cache | Cache for Redis | Session store, caching |
| Data warehouse | Synapse Analytics | Analytics workloads |
| Search | Cognitive Search | Full-text search |

## Security Best Practices

### RBAC Configuration

```yaml
# rbac-structure.yml
role_assignments:
  platform_team:
    scope: /subscriptions/{management}
    roles:
      - Owner

  network_team:
    scope: /subscriptions/{connectivity}
    roles:
      - Network Contributor

  application_teams:
    pattern: workload-specific
    roles:
      - Contributor (resource group scope)
      - User Access Administrator (for managed identities)

  security_team:
    scope: /providers/Microsoft.Management/managementGroups/{root}
    roles:
      - Security Admin
      - Security Reader (all subscriptions)

managed_identities:
  system_assigned:
    use_for: single-resource-credentials

  user_assigned:
    use_for: shared-credentials
    examples:
      - app-service-to-sql
      - function-to-keyvault
```

### Network Security

```yaml
# network-security-azure.yml
firewall:
  service: azure-firewall
  config:
    tier: Premium
    availability_zones: [1, 2, 3]
    rules:
      - allow_https_outbound
      - deny_high_risk_countries

private_endpoints:
  resources:
    - sql-server
    - storage-account
    - key-vault
    - cosmos-db
    - app-config

nsg_flow_logs:
  enabled: true
  retention: 30
  traffic_analytics:
    enabled: true
    interval: 10

ddos_protection:
  tier: Standard
  protected_resources:
    - vnet-production
```

## Cost Optimization

### Reserved Capacity Strategy

```yaml
# azure-ri-strategy.yml
compute:
  virtual_machines:
    reserved_instances:
      coverage: 70%
      term: 1-year
      payment: monthly

  azure_hybrid_benefit:
    enabled: true
    workloads:
      - windows-server
      - sql-server

storage:
  blob_lifecycle:
    policies:
      - tier_to_cool: 30_days
      - tier_to_archive: 90_days
      - delete: 2555_days

  managed_disks:
    optimization:
      - migrate_to_premium_ssd_v2
      - right_size_based_on_metrics

monitoring:
  log_analytics:
    commitment_tier: 100_GB_per_day
    data_retention: 30_days
```

### Cost Management

```yaml
# cost-management-azure.yml
budgets:
  monthly:
    amount: 50000
    granularity: monthly
    notifications:
      - threshold: 80%
        action: email
      - threshold: 100%
        action: email_and_sms

cost_alerts:
  anomaly_detection:
    enabled: true
    sensitivity: medium

  quota_alerts:
    enabled: true
    threshold: 80%

tags:
  required:
    - environment
    - cost-center
    - project
    - owner
  enforcement: azure-policy
```

## Migration Patterns

### Azure Migrate Strategy

```yaml
# azure-migrate.yml
assessment:
  tool: azure-migrate
  discovery:
    - vmware-vms
    - hyper-v-vms
    - physical-servers
  dependencies:
    tool: azure-migrate-dependency-visualization
    duration: 30_days

migration_phases:
  phase_1_test:
    workloads: non-critical
    approach: rehost
    timeline: 2_weeks

  phase_2_prod:
    workloads: production
    approach: rehost
    timeline: 2_months

  phase_3_optimize:
    approach: replatform
    changes:
      - migrate-to-managed-databases
      - adopt-app-service
      - implement-caching
```

### Cloud Adoption Framework

```yaml
# caf-implementation.yml
strategy:
  business_outcomes:
    - reduce-costs
    - improve-agility
    - enhance-security

plan:
  digital_estate:
    inventory: azure-migrate
    rationalization: 5-r-analysis

ready:
  landing_zones:
    - corp
    - online
    - sap
  shared_resources:
    - networking
    - identity
    - management

adopt:
  migration:
    method: agile
    sprints: 2_weeks

  innovation:
    ai_ml: cognitive-services
    iot: iot-hub
    serverless: functions
```
