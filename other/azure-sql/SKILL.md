---
name: azure-sql
description: |
  Use when working with Azure Sql — azure SQL Database DTU/vCore analysis, query
  performance insights, elastic pool management, geo-replication status, and
  database health monitoring via Azure CLI.
connection_type: azure
preload: false
---

# Azure SQL Skill

Manage and analyze Azure SQL databases using `az sql` commands.

## Discovery-First Rule

**ALWAYS discover before acting.** Never assume server names, database names, or elastic pool names.

```bash
# Discover SQL servers
az sql server list --output json \
  --query "[].{name:name, rg:resourceGroup, fqdn:fullyQualifiedDomainName, state:state, adminLogin:administratorLogin}"

# Discover databases per server
az sql db list --server "$SERVER" --resource-group "$RG" --output json \
  --query "[].{name:name, status:status, sku:currentSku, maxSize:maxSizeBytes, zoneRedundant:zoneRedundant}"
```

## Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
for server_info in $(echo "$servers" | jq -c '.[]'); do
  {
    name=$(echo "$server_info" | jq -r '.name')
    rg=$(echo "$server_info" | jq -r '.rg')
    az sql db list --server "$name" --resource-group "$rg" --output json
  } &
done
wait
```

## Helper Functions

```bash
# Get database service tier and performance details
get_db_tier() {
  local server="$1" rg="$2" db="$3"
  az sql db show --server "$server" --resource-group "$rg" --name "$db" --output json \
    --query "{sku:currentSku, maxSize:maxSizeBytes, status:status, earliestRestoreDate:earliestRestoreDate, zoneRedundant:zoneRedundant, readScale:readScale}"
}

# Get DTU/vCore usage metrics
get_db_metrics() {
  local resource_id="$1"
  az monitor metrics list --resource "$resource_id" \
    --metric "dtu_consumption_percent" "cpu_percent" "storage_percent" "deadlock" "connection_failed" \
    --interval PT1H --aggregation Average Max --output json
}

# List elastic pools
list_elastic_pools() {
  local server="$1" rg="$2"
  az sql elastic-pool list --server "$server" --resource-group "$rg" --output json \
    --query "[].{name:name, sku:sku, maxSizeBytes:maxSizeBytes, perDbMinDtu:perDatabaseSettings.minCapacity, perDbMaxDtu:perDatabaseSettings.maxCapacity, state:state, zoneRedundant:zoneRedundant}"
}

# Get geo-replication links
get_geo_replication() {
  local server="$1" rg="$2" db="$3"
  az sql db replica list-links --server "$server" --resource-group "$rg" --name "$db" --output json
}
```

## Common Operations

### 1. Database Health Overview

```bash
servers=$(az sql server list --output json --query "[].{name:name, rg:resourceGroup}")
for s in $(echo "$servers" | jq -c '.[]'); do
  {
    server=$(echo "$s" | jq -r '.name')
    rg=$(echo "$s" | jq -r '.rg')
    az sql db list --server "$server" --resource-group "$rg" --output json \
      --query "[?name!='master'].{name:name, sku:currentSku.name, tier:currentSku.tier, capacity:currentSku.capacity, status:status, maxSizeGB:maxSizeBytes}"
  } &
done
wait
```

### 2. DTU/vCore Performance Analysis

```bash
resource_id=$(az sql db show --server "$SERVER" --resource-group "$RG" --name "$DB" --query "id" -o tsv)
az monitor metrics list --resource "$resource_id" \
  --metric "dtu_consumption_percent" "cpu_percent" "physical_data_read_percent" "log_write_percent" \
  --interval PT1H --aggregation Average Max --output json

# Check if database needs scaling
az monitor metrics list --resource "$resource_id" \
  --metric "dtu_consumption_percent" --interval PT5M --aggregation Max \
  --start-time "$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)" --output json
```

### 3. Elastic Pool Management

```bash
# List pools and their databases
pools=$(list_elastic_pools "$SERVER" "$RG")
for pool in $(echo "$pools" | jq -c '.[]'); do
  {
    pool_name=$(echo "$pool" | jq -r '.name')
    echo "Pool: $pool_name"
    az sql elastic-pool show --server "$SERVER" --resource-group "$RG" --name "$pool_name" --output json
    az sql db list --server "$SERVER" --resource-group "$RG" --elastic-pool "$pool_name" --output json \
      --query "[].{name:name, status:status}"
  } &
done
wait
```

### 4. Query Performance Insights

```bash
# Top resource-consuming queries (requires Query Store enabled)
az sql db show --server "$SERVER" --resource-group "$RG" --name "$DB" --output json \
  --query "{queryStoreState:currentSku, readScale:readScale}"

# Check long-running queries via metrics
resource_id=$(az sql db show --server "$SERVER" --resource-group "$RG" --name "$DB" --query "id" -o tsv)
az monitor metrics list --resource "$resource_id" \
  --metric "blocked_by_firewall" "deadlock" "connection_failed" "connection_successful" \
  --interval PT1H --aggregation Total --output json
```

### 5. Geo-Replication Status

```bash
# Check replication links and lag
az sql db replica list-links --server "$SERVER" --resource-group "$RG" --name "$DB" --output json \
  --query "[].{partnerServer:partnerServer, partnerDatabase:partnerDatabase, role:role, replicationState:replicationState, percentComplete:percentComplete}"

# List failover groups
az sql failover-group list --server "$SERVER" --resource-group "$RG" --output json \
  --query "[].{name:name, readWriteEndpoint:readWriteEndpoint, readOnlyEndpoint:readOnlyEndpoint, replicationRole:replicationRole, databases:databases}"
```

## Output Format

Present results as a structured report:
```
Azure Sql Report
════════════════
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

1. **DTU vs vCore confusion**: DTU-based tiers use `dtu_consumption_percent` metric; vCore-based use `cpu_percent`. Check the SKU tier first.
2. **Elastic pool oversubscription**: Per-database max DTU can exceed pool total. Check aggregate usage, not just per-db settings.
3. **master database**: The `master` database always appears in listings. Filter it out with `[?name!='master']` in queries.
4. **Serverless auto-pause**: Serverless tier databases may show zero metrics when paused. Check `autoPauseDelay` setting.
5. **Geo-replication lag**: `replicationState` shows link health but not actual data lag. Use `replication_lag` metric for RPO assessment.
