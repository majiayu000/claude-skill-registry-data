---
name: azure-monitor
description: |
  Use when working with Azure Monitor — azure Monitor metrics querying, Log
  Analytics workspace management, alert rule configuration, action groups, and
  diagnostic settings via Azure CLI.
connection_type: azure
preload: false
---

# Azure Monitor Skill

Manage and analyze Azure Monitor resources using `az monitor` commands.

## Discovery-First Rule

**ALWAYS discover before acting.** Never assume workspace names, alert rule names, metric names, or action group names.

```bash
# Discover Log Analytics workspaces
az monitor log-analytics workspace list --output json \
  --query "[].{name:name, rg:resourceGroup, sku:sku.name, retentionDays:retentionInDays, dailyCapGB:workspaceCapping.dailyQuotaGb}"

# Discover metric alert rules
az monitor metrics alert list --output json \
  --query "[].{name:name, rg:resourceGroup, severity:severity, enabled:enabled, targetResource:scopes[0]}"
```

## Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
for ws in $(echo "$workspaces" | jq -c '.[]'); do
  {
    name=$(echo "$ws" | jq -r '.name')
    rg=$(echo "$ws" | jq -r '.rg')
    az monitor log-analytics workspace show --workspace-name "$name" --resource-group "$rg" --output json
  } &
done
wait
```

## Helper Functions

```bash
# Run a Log Analytics query
run_log_query() {
  local workspace="$1" query="$2" timespan="${3:-PT1H}"
  az monitor log-analytics query --workspace "$workspace" --analytics-query "$query" --timespan "$timespan" --output json
}

# List available metrics for a resource
list_metrics() {
  local resource_id="$1"
  az monitor metrics list-definitions --resource "$resource_id" --output json \
    --query "[].{name:name.value, displayName:name.localizedValue, unit:unit, aggregations:supportedAggregationTypes}"
}

# Get metric values
get_metrics() {
  local resource_id="$1" metrics="$2" interval="${3:-PT1H}" aggregation="${4:-Average}"
  az monitor metrics list --resource "$resource_id" --metric $metrics \
    --interval "$interval" --aggregation $aggregation --output json
}

# List action groups
list_action_groups() {
  local rg="$1"
  az monitor action-group list --resource-group "$rg" --output json \
    --query "[].{name:name, enabled:enabled, emailReceivers:emailReceivers[].name, smsReceivers:smsReceivers[].name, webhookReceivers:webhookReceivers[].name}"
}
```

## Common Operations

### 1. Workspace Overview and Usage

```bash
workspaces=$(az monitor log-analytics workspace list --output json --query "[].{name:name, rg:resourceGroup, id:customerId}")
for ws in $(echo "$workspaces" | jq -c '.[]'); do
  {
    name=$(echo "$ws" | jq -r '.name')
    rg=$(echo "$ws" | jq -r '.rg')
    ws_id=$(echo "$ws" | jq -r '.id')
    az monitor log-analytics workspace show --workspace-name "$name" --resource-group "$rg" --output json \
      --query "{name:name, sku:sku.name, retentionDays:retentionInDays, dailyCap:workspaceCapping.dailyQuotaGb, ingestionStatus:workspaceCapping.quotaNextResetTime}"
    # Check data volume
    run_log_query "$ws_id" "Usage | where TimeGenerated > ago(24h) | summarize DataGB=sum(Quantity)/1024 by DataType | sort by DataGB desc | take 10" "P1D"
  } &
done
wait
```

### 2. Alert Rules Audit

```bash
# Metric alerts
az monitor metrics alert list --output json \
  --query "[].{name:name, severity:severity, enabled:enabled, condition:criteria.allOf[0].{metric:metricName,operator:operator,threshold:threshold}, actions:actions[].actionGroupId}"

# Log alerts (scheduled query rules)
az monitor scheduled-query list --output json \
  --query "[].{name:name, severity:severity, enabled:enabled, evaluationFrequency:evaluationFrequency, windowSize:windowSize}"

# Activity log alerts
az monitor activity-log alert list --output json \
  --query "[].{name:name, enabled:enabled, scopes:scopes, condition:condition}"
```

### 3. Log Analytics Queries

```bash
# Recent errors across all tables
run_log_query "$WORKSPACE_ID" "union withsource=TableName * | where TimeGenerated > ago(1h) | where Level == 'Error' or severityLevel >= 3 | summarize count() by TableName | sort by count_ desc"

# Heartbeat check for monitored VMs
run_log_query "$WORKSPACE_ID" "Heartbeat | summarize LastHeartbeat=max(TimeGenerated) by Computer | where LastHeartbeat < ago(15m)"

# Ingestion latency
run_log_query "$WORKSPACE_ID" "Heartbeat | where TimeGenerated > ago(1h) | extend IngestionDelay=ingestion_time()-TimeGenerated | summarize avg(IngestionDelay), max(IngestionDelay) by bin(TimeGenerated, 5m)"
```

### 4. Diagnostic Settings Audit

```bash
# Check diagnostic settings for a resource
az monitor diagnostic-settings list --resource "$RESOURCE_ID" --output json \
  --query "[].{name:name, workspace:workspaceId, storageAccount:storageAccountId, eventHub:eventHubAuthorizationRuleId, logs:logs[].{category:category, enabled:enabled, retention:retentionPolicy.days}, metrics:metrics[].{category:category, enabled:enabled}}"
```

### 5. Action Group Configuration

```bash
az monitor action-group list --output json \
  --query "[].{name:name, rg:resourceGroup, enabled:enabled, email:emailReceivers[].{name:name,address:emailAddress}, sms:smsReceivers[].{name:name,phone:phoneNumber}, webhook:webhookReceivers[].{name:name,uri:serviceUri}, logicApp:logicAppReceivers[].{name:name}, azureFunction:azureFunctionReceivers[].{name:name}}"
```

## Output Format

Present results as a structured report:
```
Azure Monitor Report
════════════════════
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

1. **Metric namespaces**: Different resource types expose different metrics. Always use `list-definitions` to discover available metrics before querying.
2. **Log Analytics timespan format**: Use ISO 8601 duration format (e.g., `PT1H`, `P1D`, `P7D`), not date ranges.
3. **Daily cap resets**: When daily ingestion cap is hit, data is dropped until the next reset time. Check `quotaNextResetTime`.
4. **Alert action groups**: An alert without action groups will fire but nobody gets notified. Always verify action group linkage.
5. **KQL vs SQL**: Log Analytics uses Kusto Query Language (KQL), not SQL. Common mistakes include using `SELECT` instead of `project` and `GROUP BY` instead of `summarize`.
