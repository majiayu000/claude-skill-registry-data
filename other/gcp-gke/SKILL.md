---
name: gcp-gke
description: |
  Use when working with Gcp Gke — google Kubernetes Engine cluster operations,
  node pool management, workload analysis, autopilot configuration, and upgrade
  planning via gcloud CLI.
connection_type: gcp
preload: false
---

# GKE Skill

Manage and analyze Google Kubernetes Engine clusters using `gcloud container` commands.

## Discovery-First Rule

**ALWAYS discover before acting.** Never assume cluster names, zones, node pool names, or Kubernetes versions.

```bash
# Discover clusters
gcloud container clusters list --format=json \
  --filter="" \
  | jq '[.[] | {name: .name, location: .location, status: .status, version: .currentMasterVersion, nodeCount: .currentNodeCount, autopilot: .autopilot.enabled}]'
```

## Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
for cluster in $(gcloud container clusters list --format="value(name,location)" | tr '\t' ','); do
  {
    name=$(echo "$cluster" | cut -d',' -f1)
    location=$(echo "$cluster" | cut -d',' -f2)
    gcloud container clusters describe "$name" --location="$location" --format=json
  } &
done
wait
```

## Helper Functions

```bash
# Get cluster details
get_cluster_details() {
  local name="$1" location="$2"
  gcloud container clusters describe "$name" --location="$location" --format=json \
    | jq '{name: .name, status: .status, version: .currentMasterVersion, network: .network, subnetwork: .subnetwork, releaseChannel: .releaseChannel.channel, masterAuth: .masterAuthorizedNetworksConfig, addons: .addonsConfig, autoscaling: .autoscaling, shieldedNodes: .shieldedNodes.enabled}'
}

# List node pools
list_node_pools() {
  local cluster="$1" location="$2"
  gcloud container node-pools list --cluster="$cluster" --location="$location" --format=json \
    | jq '[.[] | {name: .name, version: .version, machineType: .config.machineType, diskSizeGb: .config.diskSizeGb, nodeCount: .initialNodeCount, autoscaling: .autoscaling, status: .status, management: .management}]'
}

# Get available upgrades
get_upgrades() {
  local cluster="$1" location="$2"
  gcloud container get-server-config --location="$location" --format=json \
    | jq '{validMasterVersions: .validMasterVersions[:5], validNodeVersions: .validNodeVersions[:5], defaultClusterVersion: .defaultClusterVersion}'
}

# Get cluster operations
get_operations() {
  local location="$1"
  gcloud container operations list --location="$location" --format=json --sort-by="~startTime" --limit=10 \
    | jq '[.[] | {name: .name, type: .operationType, status: .status, startTime: .startTime, endTime: .endTime, targetLink: .targetLink}]'
}
```

## Common Operations

### 1. Cluster Health Overview

```bash
clusters=$(gcloud container clusters list --format="value(name,location)" | tr '\t' ',')
for cluster in $clusters; do
  {
    name=$(echo "$cluster" | cut -d',' -f1)
    location=$(echo "$cluster" | cut -d',' -f2)
    echo "=== Cluster: $name ==="
    get_cluster_details "$name" "$location"
    list_node_pools "$name" "$location"
  } &
done
wait
```

### 2. Node Pool Management

```bash
# Node pool details with autoscaling config
gcloud container node-pools list --cluster="$CLUSTER" --location="$LOCATION" --format=json \
  | jq '[.[] | {name: .name, machineType: .config.machineType, nodeCount: .initialNodeCount, minNodes: .autoscaling.minNodeCount, maxNodes: .autoscaling.maxNodeCount, autoRepair: .management.autoRepair, autoUpgrade: .management.autoUpgrade, preemptible: .config.preemptible, spot: .config.spot}]'

# Node pool utilization (via kubectl after getting credentials)
gcloud container clusters get-credentials "$CLUSTER" --location="$LOCATION"
kubectl top nodes
```

### 3. Workload Analysis

```bash
# Get credentials and analyze workloads
gcloud container clusters get-credentials "$CLUSTER" --location="$LOCATION"
kubectl get deployments --all-namespaces -o json | jq '[.items[] | {namespace: .metadata.namespace, name: .metadata.name, replicas: .spec.replicas, available: .status.availableReplicas, ready: .status.readyReplicas}]'
```

### 4. Autopilot Configuration

```bash
# Check if cluster is Autopilot
gcloud container clusters describe "$CLUSTER" --location="$LOCATION" --format=json \
  | jq '{autopilot: .autopilot.enabled, workloadPolicies: .autopilot.workloadPolicyConfig, resourceLimits: .autoscaling.resourceLimits}'

# Autopilot workload scaling classes
kubectl get priorityclasses -o json | jq '[.items[] | {name: .metadata.name, value: .value}]'
```

### 5. Upgrade Planning

```bash
# Current vs available versions
gcloud container clusters describe "$CLUSTER" --location="$LOCATION" --format=json \
  | jq '{masterVersion: .currentMasterVersion, nodeVersion: .currentNodeVersion, releaseChannel: .releaseChannel.channel}'

# Available upgrades
get_upgrades "$CLUSTER" "$LOCATION"

# Check node pool version skew
gcloud container node-pools list --cluster="$CLUSTER" --location="$LOCATION" --format=json \
  | jq '[.[] | {pool: .name, version: .version}]'
```

## Output Format

Present results as a structured report:
```
Gcp Gke Report
══════════════
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

1. **Zonal vs regional**: Zonal clusters have a single control plane; regional clusters have three. Use `--location` (not `--zone`) to work with both.
2. **Autopilot restrictions**: Autopilot clusters do not allow SSH to nodes, privileged containers, or host network access. Check autopilot status first.
3. **Release channels**: Clusters in a release channel get automatic upgrades. Manual version pinning requires opting out of the release channel.
4. **Node auto-provisioning**: NAP creates node pools automatically. Check `autoscaling.enableNodeAutoprovisioning` before manually creating pools.
5. **Workload Identity**: GKE Workload Identity replaces node-level service accounts. Check `workloadIdentityConfig` before troubleshooting IAM issues.
