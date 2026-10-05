---




name: cortex
compatibility: opencode
completeness: 95
content-types:
- guidance
- examples
- do-dont
- config
description: '"Cortex in Monitoring & Observability - distributed, horizontally scalable"
  Prometheus system'
license: MIT
maturity: stable
metadata:
  domain: cncf
  output-format: manifests
  role: reference
  scope: infrastructure
  triggers: cortex, distributed, monitoring, observability, cloudwatch, logging
  archetypes:
  - educational
  - strategic
  anti_triggers:
  - brainstorming
  - vague ideation
  - non-containerized architecture
  response_profile:
    verbosity: medium
    directive_strength: low
    abstraction_level: strategic
version: "1.0.0"




---




  related-skills: cncf-aws-cloudwatch, cncf-azure-monitor, cncf-fluentd, cncf-gcp-autoscaling



# Cortex in Cloud-Native Engineering

**Category:** observability  
**Status:** Incubating  
**Stars:** 4,500  
**Last Updated:** 2026-04-22  
**Primary Language:** Go  
**Documentation:** [https://cortexmetrics.io/](https://cortexmetrics.io/)  

---

## Purpose and Use Cases

Cortex is a CNCF incubating project that provides a horizontally scalable, highly available, multi-tenant Prometheus system for long-term storage and distributed metrics collection.

### What Problem Does It Solve?

Prometheus single-node limitations. Standard Prometheus has finite storage, limited scalability, and no multi-tenancy. Cortex addresses these by providing:
- Horizontal scalability across multiple nodes
- Long-term storage integration (S3, GCS, Azure Blob)
- Multi-tenant support with isolation
- Unified query interface across multiple Prometheus instances

### When to Use This Project

Use Cortex when you need:
- Horizontal scalability beyond single Prometheus instance
- Long-term metrics storage with cloud storage integration
- Multi-tenancy with isolated metrics per tenant
- High availability with redundant storage
- Integration with existing Prometheus infrastructure

### Key Use Cases

- **Multi-tenant Observability**: Different teams/tenants with isolated metrics
- **Long-term Storage**: Store metrics for months/years in cloud storage
- **High Availability**: Redundant Prometheus instances with shared storage
- **Federated Monitoring**: Collect metrics from multiple Prometheus instances
- **SaaS Observability Platform**: Multi-tenant metrics backend

---

## Architecture Design Patterns

### Cortex Architecture

#### 1. Control Plane (Stateless)

```
┌─────────────────┐
│   Query Frontend│
│  (Query API)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      Ruler      │
│ (Rule Processing)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      Store      │
│   (Compactor)   │
└─────────────────┘
```

#### 2. Data Plane (Stateful)

```
┌─────────────────┐     ┌─────────────────┐
│     Ingester    │     │    Distributor  │
│ (Write Path)    │────▶│  (Ingestion)    │
└─────────────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐
│     Compactor   │
│  (Storage)      │
└─────────────────┘
```

### Data Flow

```
1. Push Metrics → Distributor
2. Distributor → Ingester (Hash ring)
3. Ingester → Store (Write-ahead log + chunks)
4. Store → Cloud Storage (S3/GCS/Azure)
5. Query → Store Gateway → Query Frontend → User
```

### Consistent Hash Ring

```yaml
# Consistent hash ring for distribution
ring:
  kvstore:
    store: memberlist
  replication_factor: 3
  zone_awareness_enabled: true
```

### Multi-Tenancy

```yaml
# Tenant configuration
tenants:
  - id: tenant-1
    name: Team A
    quota: 10000
    retention: 30d
  - id: tenant-2
    name: Team B
    quota: 50000
    retention: 90d
```

### Storage Compaction

```yaml
# Storage compaction configuration
compactor:
  working_directory: /data/compactor
  data_dir: /data/storage
  compaction_interval: 1h
  retention_enabled: true
  retention_delete_delay: 24h
```

### Query Frontend

```yaml
# Query frontend for caching and querier sharding
query_frontend:
  enabled: true
  cache:
    type: redis
    redis:
      addr: redis:6379
  querier_shard_enabled: true
  max_outstanding_requests_per_tenant: 2000
```

---

## Integration Approaches

### Prometheus Integration

#### 1. Remote Write

```yaml
# Prometheus configuration for Cortex
remote_write:
  - url: "http://cortex:8080/api/v1/push"
    remote_timeout: 30s
    write_relabel_configs:
      - source_labels: [__name__]
        regex: "job:(.*)"
        target_label: tenant_id
        replacement: "${1}"
```

#### 2. Remote Read

```yaml
# Prometheus as Cortex reader
remote_read:
  - url: "http://cortex:8080/api/v1/read"
    remote_timeout: 30s
    required_matchers:
      tenant_id: "my-tenant"
```

### Kubernetes Integration

```yaml
# Deploy Cortex to Kubernetes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cortex
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cortex
  template:
    metadata:
      labels:
        app: cortex
    spec:
      containers:
        - name: cortex
          image: cortexproject/cortex:v1.16.0
          args:
            - "-config.file=/etc/cortex/cortex.yaml"
            - "-target=all"
          ports:
            - containerPort: 8080
          volumeMounts:
            - name: config
              mountPath: /etc/cortex
            - name: data
              mountPath: /data
```

### Cloud Storage Integration

#### 1. AWS S3

```yaml
# S3 storage configuration
storage:
  engine: blocks
  blocks:
    backend: s3
    s3:
      bucket: my-cortex-bucket
      region: us-east-1
      endpoint: ""
      access_key: ""
      secret_key: ""
```

#### 2. Google Cloud Storage

```yaml
# GCS storage configuration
storage:
  engine: blocks
  blocks:
    backend: gcs
    gcs:
      bucket: my-cortex-bucket
      credentials_file: /etc/cortex/gcs-key.json
```

#### 3. Azure Blob Storage

```yaml
# Azure Blob configuration
storage:
  engine: blocks
  blocks:
    backend: azure
    azure:
      storage_account: myaccount
      storage_key: ""
      container_name: my-cortex-container
```

### Query Integration

#### 1. API Endpoint

```bash
# Query Cortex API
curl -G "http://cortex:8080/api/v1/query" \
  --data-urlencode 'query=up' \
  -H "X-Scope-OrgID: tenant-1"

# Range query
curl -G "http://cortex:8080/api/v1/query_range" \
  --data-urlencode 'query=rate(http_requests_total[5m])' \
  --data 'start=1620000000' \
  --data 'end=1620003600' \
  --data 'step=15s' \
  -H "X-Scope-OrgID: tenant-1"
```

#### 2. Grafana Integration

```yaml
# Grafana data source configuration
apiVersion: 1
datasources:
  - name: Cortex
    type: prometheus
    access: proxy
    url: http://cortex-query-frontend:8080
    basicAuth: false
    editable: false
    jsonData:
      httpHeaderName1: "X-Scope-OrgID"
      managed: true
    secureJsonData:
      httpHeaderValue1: "tenant-1"
```

### Alerting Integration

```yaml
# Cortex Ruler for alerting
apiVersion: v1
kind: ConfigMap
metadata:
  name: cortex-rules
data:
  rules.yaml: |
    groups:
      - name: example
        rules:
          - alert: HighRequestRate
            expr: rate(http_requests_total[5m]) > 1000
            for: 5m
            labels:
              tenant: "tenant-1"
            annotations:
              summary: "High request rate detected"
              description: "Request rate is above 1000 for 5 minutes"
```

---
  related-skills: cncf-aws-cloudwatch, cncf-azure-monitor, cncf-fluentd, cncf-gcp-autoscaling

## Common Pitfalls and How to Avoid Them

### 1. Tenant ID Configuration

**Pitfall:** Missing or incorrect tenant ID in headers.

```bash
# ❌ Incorrect - missing tenant ID
curl -G "http://cortex:8080/api/v1/query" \
  --data-urlencode 'query=up'

# ✅ Correct - with tenant ID
curl -G "http://cortex:8080/api/v1/query" \
  --data-urlencode 'query=up' \
  -H "X-Scope-OrgID: tenant-1"
```

### 2. Memory Configuration

**Pitfall:** Insufficient memory causing ingestion failures.

```yaml
# ❌ Incorrect - low memory limits
resources:
  limits:
    memory: "512Mi"
  requests:
    memory: "256Mi"

# ✅ Correct - appropriate memory
resources:
  limits:
    memory: "8Gi"
  requests:
    memory: "4Gi"
```

### 3. Retention Settings

**Pitfall:** Storage costs growing unbounded.

```yaml
# ❌ Incorrect - no retention
blocks_storage:
  backend: s3
  bucket_store:
    sync_dir: /data/tsdb

# ✅ Correct - with retention
blocks_storage:
  backend: s3
  bucket_store:
    sync_dir: /data/tsdb
  retention_period: 30d
```

### 4. Consistency Level

**Pitfall:** Inconsistent queries due to low consistency.

```yaml
# ❌ Incorrect - single consistency
query_frontend:
  consistency:
    mode: single

# ✅ Correct - eventually consistent
query_frontend:
  consistency:
    mode: eventual
    default: 1
```

### 5. Compaction Frequency

**Pitfall:** Too frequent compaction causing performance issues.

```yaml
# ❌ Incorrect - too frequent compaction
compactor:
  compaction_interval: 1m

# ✅ Correct - reasonable interval
compactor:
  compaction_interval: 1h
  compaction_window: 1h
  max_compaction_level: 4
```

### 6. Shard Configuration

**Pitfall:** Uneven query distribution due to missing sharding.

```yaml
# ❌ Incorrect - no querier sharding
query_frontend:
  querier_shard_enabled: false

# ✅ Correct - with sharding
query_frontend:
  querier_shard_enabled: true
  querier_shards: 4
  querier_tenant_shards: 1
```

---

## Coding Practices

### Metrics Collection

```go
// Custom metrics for Cortex
package metrics

import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    // Ingestion metrics
    ingestedSamples = promauto.NewCounterVec(prometheus.CounterOpts{
        Name: "cortex_ingester_samples_total",
        Help: "Total number of samples ingested",
    }, []string{"tenant", "success"})
    
    // Query metrics
    queriesTotal = promauto.NewCounterVec(prometheus.CounterOpts{
        Name: "cortex_query_frontend_queries_total",
        Help: "Total number of queries",
    }, []string{"tenant", "status"})
    
    // Storage metrics
    storageOps = promauto.NewCounterVec(prometheus.CounterOpts{
        Name: "cortex_storage_operations_total",
        Help: "Total number of storage operations",
    }, []string{"operation", "tenant"})
)
```

### Tenant Management

```go
// Tenant management
package tenant

import (
    "context"
    "fmt"
)

type ctxKey string

const tenantIDKey ctxKey = "tenant_id"

// Context with tenant ID
func WithTenant(ctx context.Context, tenantID string) context.Context {
    return context.WithValue(ctx, tenantIDKey, tenantID)
}

// Extract tenant ID from context
func FromContext(ctx context.Context) (string, error) {
    if tenantID, ok := ctx.Value(tenantIDKey).(string); ok {
        return tenantID, nil
    }
    return "", fmt.Errorf("tenant ID not found in context")
}

// Validate tenant ID
func Validate(tenantID string) error {
    if tenantID == "" {
        return fmt.Errorf("tenant ID cannot be empty")
    }
    if len(tenantID) > 255 {
        return fmt.Errorf("tenant ID too long")
    }
    return nil
}
```

### API Handlers

```go
// HTTP handler with tenant isolation
package handler

import (
    "context"
    "net/http"
    
    "github.com/prometheus/client_golang/api"
    "github.com/prometheus/client_golang/prometheus"
)

type Handler struct {
    client api.Client
    registry *prometheus.Registry
}

func NewHandler(client api.Client, registry *prometheus.Registry) *Handler {
    return &Handler{
        client: client,
        registry: registry,
    }
}

func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    // Extract tenant ID from headers
    tenantID := r.Header.Get("X-Scope-OrgID")
    if tenantID == "" {
        http.Error(w, "Missing X-Scope-OrgID header", http.StatusBadRequest)
        return
    }
    
    // Validate tenant
    if err := validateTenant(tenantID); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    
    // Create context with tenant
    ctx := context.WithValue(r.Context(), "tenant_id", tenantID)
    r = r.WithContext(ctx)
    
    // Forward to Prometheus API
    h.client.Do(ctx, r)
}

func validateTenant(tenantID string) error {
    if len(tenantID) == 0 {
        return fmt.Errorf("tenant ID cannot be empty")
    }
    if len(tenantID) > 255 {
        return fmt.Errorf("tenant ID too long (max 255 characters)")
    }
    return nil
}
```

### Testing

```go
// Cortex integration testing
package test

import (
    "context"
    "net/http/httptest"
    "testing"
    
    "github.com/stretchr/testify/assert"
)

func TestTenantIsolation(t *testing.T) {
    // Create test server
    server := httptest.NewServer(nil)
    defer server.Close()
    
    // Test tenant isolation
    tests := []struct {
        name        string
        tenantID    string
        expectError bool
    }{
        {"valid tenant", "tenant-1", false},
        {"empty tenant", "", true},
        {"long tenant", string(make([]byte, 300)), true},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest("GET", server.URL, nil)
            req.Header.Set("X-Scope-OrgID", tt.tenantID)
            
            // Test tenant validation
            err := validateTenant(tt.tenantID)
            
            if tt.expectError {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
            }
        })
    }
}
```

---

## Fundamentals

### Cortex Components

#### 1. Distributor

- Receives incoming metrics
- Validates and batches samples
- Routes to ingesters based on hash ring

#### 2. Ingester

- Receives samples from distributors
- Writes to WAL (Write-Ahead Log)
- Flushes to storage

#### 3. Store Gateway

- Serves data from cloud storage
- Compacted blocks from compactor

#### 4. Query Frontend

- Caches queries
- Shards queries across queriers

#### 5. Compactor

- Compacts blocks in storage
- Deletes old data based on retention

### Storage Engine

#### Blocks Storage (Recommended)

```yaml
storage:
  engine: blocks
  blocks:
    backend: s3
    s3:
      bucket: my-bucket
      region: us-east-1
```

#### Legacy TSDB Storage

```yaml
storage:
  engine: tsdb
  tsdb:
    path: /data/tsdb
```

### API Endpoints

```bash
# Push metrics
POST /api/v1/push

# Query metrics
GET /api/v1/query
GET /api/v1/query_range

# Labels
GET /api/v1/labels
GET /api/v1/label/{label}/values

# Alerts
GET /api/v1/alerts
POST /api/v1/alerts
```

---

## Scaling and Deployment Patterns

### Horizontal Scaling

```bash
# Scale components independently
# Distributors: 3-5 replicas
# Ingester: 5-10 replicas (depending on write load)
# Store Gateway: 2-3 replicas
# Query Frontend: 3-5 replicas
# Querier: 3-10 replicas (depending on query load)
```

### Multi-Tenant Scaling

```yaml
# Per-tenant resource limits
limits:
  max_series_per_user: 100000
  max_series_per_metric: 10000
  max_metadata_per_metric: 1000
  max_series_query_duration: 300s
```

### HA with Replica Zone

```yaml
# Zone awareness for HA
ring:
  replication_factor: 3
  zone_awareness_enabled: true
  instance_availability_zone: us-east-1a
```

### Backup Strategy

```bash
# Backup storage
# Use storage snapshots or cloud storage backup
aws s3 sync s3://my-cortex-bucket/backup/ s3://my-backup-bucket/cortex/

# Restore from backup
aws s3 sync s3://my-backup-bucket/cortex/ s3://my-cortex-bucket/
```

### Monitoring

```yaml
# Cortex metrics for monitoring
- name: cortex_ingester_samples_in
  type: counter
  help: Total number of samples ingested

- name: cortex_ingester_samples_out
  type: counter
  help: Total number of samples sent to storage

- name: cortex_distributor_samples_received
  type: counter
  help: Total number of samples received

- name: cortex_store_gateway_series
  type: histogram
  help: Number of series returned
```

---

## Additional Resources

### Official Documentation

- [Cortex Metrics](https://cortexmetrics.io/) - Project website
- [Cortex Documentation](https://cortexmetrics.io/docs/) - Complete documentation
- [Cortex GitHub](https://github.com/cortexproject/cortex) - Source code
- [Cortex API](https://cortexmetrics.io/docs/api/) - API reference

### Implementations

- [Kubernetes Cortex](https://kubernetes.io/docs/concepts/cluster-administration/system-metrics/#cortex) - Kubernetes integration
- [Cortex Operator](https://github.com/cortexproject/cortex-operator) - Operator for Cortex
- [Cortex Helm Chart](https://github.com/grafana/helm-charts/tree/main/charts/cortex) - Helm installation

### Community Resources

- [CNCF Cortex](https://www.cncf.io/projects/cortex/) - CNCF project page
- [Cortex Slack](https://kubernetes.slack.com/archives/CJNFKL7B3) - Community discussion
- [Cortex Mailing List](https://lists.cncf.io/g/cncf-cortex) - Announcements

### Learning Resources

- [Cortex Getting Started](https://cortexmetrics.io/docs/getting-started/) - Tutorial
- [Cortex Examples](https://github.com/cortexproject/cortex/tree/master/examples) - Example configurations
- [Cortex Webinars](https://www.cncf.io/cortex-webinars/) - Video content

---

*This SKILL.md file was verified and last updated on 2026-04-22. Content based on CNCF Cortex project and production usage patterns.*
## Troubleshooting

### Common Issues

1. **Deployment Failures**
   - Check pod logs for errors
   - Verify configuration values
   - Ensure network connectivity

2. **Performance Issues**
   - Monitor resource usage
   - Adjust resource limits
   - Check for bottlenecks

3. **Configuration Errors**
   - Validate YAML syntax
   - Check required fields
   - Verify environment-specific settings

4. **Integration Problems**
   - Verify API compatibility
   - Check dependency versions
   - Review integration documentation

### Getting Help

- Check official documentation
- Search GitHub issues
- Join community channels
- Review logs and metrics

## Examples

### Basic Configuration


```yaml
# Basic configuration example
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{project_name}}-config
  namespace: default
data:
  # Configuration goes here
  config.yaml: |
    # Base configuration
    # Add your settings here
```

### Kubernetes Deployment


```yaml
# Kubernetes deployment for {{project_name}}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{project_name}}
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {{project_name}}
  template:
    metadata:
      labels:
        app: {{project_name}}
    spec:
      containers:
      - name: {{project_name}}
        image: {{project_name}}:latest
        ports:
        - containerPort: 8080
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
```

### Kubernetes Service


```yaml
# Kubernetes service for {{project_name}}
apiVersion: v1
kind: Service
metadata:
  name: {{project_name}}
  namespace: default
spec:
  selector:
    app: {{project_name}}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
```

---

## When to Use

Use this skill when:

- **Integrating a CNCF project into Kubernetes infrastructure** — You need to configure, deploy, or troubleshoot a cloud-native tool within a cluster
- **Designing cloud-native architecture** — You are selecting and integrating CNCF tools to solve specific infrastructure challenges
- **Resolving operational issues** — A CNCF component is misbehaving, underperforming, or needs configuration changes
---

## Core Workflow

1. **Assess Requirements** — Understand the use case, scale, integration needs, and existing infrastructure. **Checkpoint:** Document requirements, constraints, and success criteria.

2. **Design Architecture** — Plan component interactions, data flow, and deployment strategy using cloud-native best practices. **Checkpoint:** Verify the architecture addresses all requirements and follows CNCF conventions.

3. **Implement & Configure** — Create manifests, configurations, and deployment scripts. Include resource limits, health checks, and observability hooks. **Checkpoint:** Validate all YAML against schema and test in a staging environment.

4. **Deploy & Monitor** — Apply manifests to the cluster, verify component health, and confirm observability is working. **Checkpoint:** Confirm all pods/services are running, probes passing, and metrics/alerts configured.

---

## Constraints

### MUST DO
- Include at least one complete working YAML manifest example
- Note when content is auto-generated vs. manually verified
- Reference relevant CNCF project documentation

### MUST NOT DO
- Deploy manifests without testing in a staging environment first
- Use deprecated API versions (e.g., apps/v1beta1)
- Omit resource limits and requests in Kubernetes manifests
