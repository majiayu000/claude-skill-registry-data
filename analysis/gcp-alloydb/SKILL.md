---
name: gcp-alloydb
description: |
  Use when working with Gcp Alloydb — google AlloyDB cluster management,
  instance analysis, query insights, maintenance window configuration, and
  performance diagnostics via gcloud CLI.
connection_type: gcp
preload: false
---

# AlloyDB Skill

Manage and analyze Google AlloyDB for PostgreSQL using `gcloud alloydb` commands.

## Discovery-First Rule

**ALWAYS discover before acting.** Never assume cluster names, instance names, regions, or backup names.

```bash
# Discover AlloyDB clusters
gcloud alloydb clusters list --format=json \
  | jq '[.[] | {name: .name | split("/") | last, state: .state, databaseVersion: .databaseVersion, network: .network, location: .name | split("/") | .[3], continuousBackupEnabled: .continuousBackupConfig.enabled}]'
```

## Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
for cluster in $(gcloud alloydb clusters list --format="value(name)" | xargs -I{} basename {}); do
  {
    gcloud alloydb clusters describe "$cluster" --region="$REGION" --format=json
  } &
done
wait
```

## Helper Functions

```bash
# Get cluster details
get_cluster_details() {
  local cluster="$1" region="$2"
  gcloud alloydb clusters describe "$cluster" --region="$region" --format=json \
    | jq '{name: .name | split("/") | last, state: .state, databaseVersion: .databaseVersion, network: .network, encryptionConfig: .encryptionConfig, continuousBackup: .continuousBackupConfig, automatedBackup: .automatedBackupPolicy, initialUser: .initialUser.user}'
}

# List instances in a cluster
list_instances() {
  local cluster="$1" region="$2"
  gcloud alloydb instances list --cluster="$cluster" --region="$region" --format=json \
    | jq '[.[] | {name: .name | split("/") | last, instanceType: .instanceType, state: .state, machineConfig: .machineConfig, availabilityType: .availabilityType, ipAddress: .ipAddress, readPoolConfig: .readPoolConfig, queryInsights: .queryInsightsConfig}]'
}

# List backups
list_backups() {
  local region="$1"
  gcloud alloydb backups list --region="$region" --format=json \
    | jq '[.[] | {name: .name | split("/") | last, state: .state, type: .type, cluster: .clusterName | split("/") | last, createTime: .createTime, sizeBytes: .sizeBytes}]'
}

# Get instance metrics
get_instance_metrics() {
  local instance="$1" cluster="$2"
  gcloud monitoring time-series list \
    --filter="metric.type=starts_with(\"alloydb.googleapis.com/\") AND resource.labels.instance_id=\"$instance\"" \
    --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
    --format=json --limit=50
}
```

## Common Operations

### 1. Cluster and Instance Overview

```bash
clusters=$(gcloud alloydb clusters list --format=json \
  | jq -c '[.[] | {name: .name | split("/") | last, region: .name | split("/") | .[3]}]')
for c in $(echo "$clusters" | jq -c '.[]'); do
  {
    name=$(echo "$c" | jq -r '.name')
    region=$(echo "$c" | jq -r '.region')
    echo "=== Cluster: $name ==="
    get_cluster_details "$name" "$region"
    list_instances "$name" "$region"
  } &
done
wait
```

### 2. Instance Analysis

```bash
# Primary and read pool instances
gcloud alloydb instances list --cluster="$CLUSTER" --region="$REGION" --format=json \
  | jq '[.[] | {name: .name | split("/") | last, type: .instanceType, state: .state, cpu: .machineConfig.cpuCount, availabilityType: .availabilityType, readPoolNodeCount: .readPoolConfig.nodeCount, gceZone: .gceZone}]'

# Check Query Insights configuration
gcloud alloydb instances describe "$INSTANCE" --cluster="$CLUSTER" --region="$REGION" --format=json \
  | jq '{queryInsights: .queryInsightsConfig}'
```

### 3. Query Insights

```bash
# CPU utilization per instance
gcloud monitoring time-series list \
  --filter="metric.type=\"alloydb.googleapis.com/instance/cpu/utilization\" AND resource.labels.instance_id=\"$INSTANCE\"" \
  --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --format=json

# Database connections
gcloud monitoring time-series list \
  --filter="metric.type=\"alloydb.googleapis.com/instance/postgresql/backends\" AND resource.labels.instance_id=\"$INSTANCE\"" \
  --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --format=json

# Replication lag (for read pool instances)
gcloud monitoring time-series list \
  --filter="metric.type=\"alloydb.googleapis.com/instance/postgresql/replication/replica_byte_lag\" AND resource.labels.instance_id=\"$INSTANCE\"" \
  --interval-start-time="$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --format=json
```

### 4. Backup and Recovery

```bash
# List all backups
list_backups "$REGION"

# Continuous backup config
gcloud alloydb clusters describe "$CLUSTER" --region="$REGION" --format=json \
  | jq '{continuousBackup: .continuousBackupConfig, automatedBackup: .automatedBackupPolicy}'

# Check point-in-time recovery window
gcloud alloydb clusters describe "$CLUSTER" --region="$REGION" --format=json \
  | jq '{continuousBackupInfo: .continuousBackupInfo}'
```

### 5. Maintenance Configuration

```bash
# Check maintenance window
gcloud alloydb clusters describe "$CLUSTER" --region="$REGION" --format=json \
  | jq '{maintenanceUpdatePolicy: .maintenanceUpdatePolicy, maintenanceSchedule: .maintenanceSchedule}'

# Recent operations (maintenance, updates)
gcloud alloydb operations list --region="$REGION" --format=json --limit=10 \
  | jq '[.[] | {name: .name | split("/") | last, type: .metadata."@type", done: .done, startTime: .metadata.createTime}]'
```

## Output Format

Present results as a structured report:
```
Gcp Alloydb Report
══════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

1. **Primary vs read pool**: AlloyDB has one primary instance and optional read pool instances. Read pools auto-scale nodes but the primary does not.
2. **Machine type changes**: Changing CPU count requires instance restart. Plan maintenance windows for resize operations.
3. **Network requirement**: AlloyDB requires a VPC with Private Services Access configured. Instances are not publicly accessible by default.
4. **Continuous backup retention**: Default continuous backup retention is 14 days. Cannot be extended beyond 35 days. Plan accordingly for compliance.
5. **Query Insights**: Query Insights must be explicitly enabled per instance. It adds minimal overhead but provides critical performance data. Check `queryInsightsConfig.queryInsightsEnabled`.
