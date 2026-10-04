---
name: azure-aks
description: |
  Use when working with Azure Aks — azure Kubernetes Service (AKS) cluster
  management, node pool status, addon management, upgrade planning, and health
  diagnostics via Azure CLI.
connection_type: azure
preload: false
---

# AKS Skill

Manage and analyze Azure Kubernetes Service clusters using `az aks` commands.

## Discovery-First Rule

**ALWAYS discover before acting.** Never assume cluster names, resource groups, node pool names, or Kubernetes versions. Run discovery commands first, then use the actual values returned.

```bash
# Step 1: Discover clusters
az aks list --output json --query "[].{name:name, rg:resourceGroup, version:kubernetesVersion, state:powerState.code}"

# Step 2: Use discovered values in subsequent commands
az aks show --name "$CLUSTER" --resource-group "$RG" --output json
```

## Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
# CORRECT: Parallel cluster inspection
for cluster_info in $clusters; do
  {
    name=$(echo "$cluster_info" | jq -r '.name')
    rg=$(echo "$cluster_info" | jq -r '.rg')
    az aks show --name "$name" --resource-group "$rg" --output json
  } &
done
wait
```

## Helper Functions

```bash
# Get cluster credentials (non-destructive, merge into kubeconfig)
get_aks_credentials() {
  local name="$1" rg="$2"
  az aks get-credentials --name "$name" --resource-group "$rg" --overwrite-existing --output none
}

# List node pools with key metrics
list_node_pools() {
  local name="$1" rg="$2"
  az aks nodepool list --cluster-name "$name" --resource-group "$rg" \
    --output json --query "[].{name:name, vmSize:vmSize, count:count, mode:mode, osType:osType, version:orchestratorVersion, state:provisioningState, powerState:powerState.code}"
}

# Check available upgrades
check_upgrades() {
  local name="$1" rg="$2"
  az aks get-upgrades --name "$name" --resource-group "$rg" --output json
}

# Get cluster diagnostics
get_diagnostics() {
  local name="$1" rg="$2"
  az aks show --name "$name" --resource-group "$rg" --output json \
    --query "{networkProfile:networkProfile, addonProfiles:addonProfiles, apiServerAccessProfile:apiServerAccessProfile, autoScalerProfile:autoScalerProfile}"
}
```

## Common Operations

### 1. Cluster Health Overview

```bash
clusters=$(az aks list --output json --query "[].{name:name, rg:resourceGroup}")
for c in $(echo "$clusters" | jq -c '.[]'); do
  {
    name=$(echo "$c" | jq -r '.name')
    rg=$(echo "$c" | jq -r '.rg')
    echo "=== $name ==="
    az aks show --name "$name" --resource-group "$rg" --output json \
      --query "{version:kubernetesVersion, state:powerState.code, fqdn:fqdn, nodeRG:nodeResourceGroup, sku:sku}"
    list_node_pools "$name" "$rg"
  } &
done
wait
```

### 2. Node Pool Scaling and Status

```bash
# Check autoscaler status and node counts
az aks nodepool list --cluster-name "$CLUSTER" --resource-group "$RG" --output json \
  --query "[].{name:name, count:count, minCount:minCount, maxCount:maxCount, enableAutoScaling:enableAutoScaling, vmSize:vmSize}"

# Scale a node pool (manual)
az aks nodepool update --cluster-name "$CLUSTER" --resource-group "$RG" \
  --name "$POOL" --enable-cluster-autoscaler --min-count 2 --max-count 10
```

### 3. Addon Management

```bash
# List enabled addons
az aks show --name "$CLUSTER" --resource-group "$RG" --output json \
  --query "addonProfiles" | jq 'to_entries[] | select(.value.enabled==true) | .key'

# Enable monitoring addon
az aks enable-addons --name "$CLUSTER" --resource-group "$RG" --addons monitoring \
  --workspace-resource-id "$WORKSPACE_ID"
```

### 4. Upgrade Planning

```bash
# Current version and available upgrades
az aks get-upgrades --name "$CLUSTER" --resource-group "$RG" --output json \
  --query "{currentVersion:controlPlaneProfile.kubernetesVersion, upgrades:controlPlaneProfile.upgrades[].kubernetesVersion}"

# Check node pool versions (detect skew)
az aks nodepool list --cluster-name "$CLUSTER" --resource-group "$RG" --output json \
  --query "[].{pool:name, version:orchestratorVersion}"
```

### 5. Network and Security Configuration

```bash
az aks show --name "$CLUSTER" --resource-group "$RG" --output json \
  --query "{networkPlugin:networkProfile.networkPlugin, networkPolicy:networkProfile.networkPolicy, serviceCidr:networkProfile.serviceCidr, podCidr:networkProfile.podCidr, dnsServiceIP:networkProfile.dnsServiceIP, authorizedIPs:apiServerAccessProfile.authorizedIpRanges, privateCluster:apiServerAccessProfile.enablePrivateCluster, aad:aadProfile}"
```

## Output Format

Present results as a structured report:
```
Azure Aks Report
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

1. **Version skew**: Node pool versions can differ from control plane. Always check both before upgrading.
2. **System vs user pools**: System node pools cannot be scaled to zero. Use `mode` field to distinguish.
3. **Private clusters**: `az aks command invoke` is required to run kubectl commands on private clusters.
4. **Addon dependencies**: Some addons require specific node pool configurations or extensions. Check prerequisites before enabling.
5. **Autoscaler vs manual**: Never set `--node-count` on a pool with autoscaler enabled -- use `--min-count` and `--max-count` instead.
