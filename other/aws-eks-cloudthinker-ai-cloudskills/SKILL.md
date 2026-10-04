---
name: aws-eks
description: |
  Use when working with Aws Eks — aWS EKS cluster management, nodegroup status,
  addon management, IRSA configuration, and cluster health analysis. Covers
  Kubernetes version tracking, nodegroup scaling, addon compatibility, IAM role
  mapping, and control plane logging.
connection_type: aws
preload: false
---

# AWS EKS Skill

Analyze AWS EKS clusters with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-eks/` → EKS-specific analysis (clusters, nodegroups, addons, IRSA)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)
- `k8s/` → In-cluster Kubernetes operations (pods, deployments, services)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for cluster in $clusters; do
  describe_eks_cluster "$cluster" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List all EKS clusters
list_eks_clusters() {
  aws eks list-clusters --output text --query 'clusters[]'
}

# Get cluster details
describe_eks_cluster() {
  local cluster=$1
  aws eks describe-cluster --name "$cluster" \
    --output text \
    --query 'cluster.[name,version,status,platformVersion,endpoint,roleArn]'
}

# List nodegroups for a cluster
list_nodegroups() {
  local cluster=$1
  aws eks list-nodegroups --cluster-name "$cluster" \
    --output text --query 'nodegroups[]'
}

# Get nodegroup details
describe_nodegroup() {
  local cluster=$1 nodegroup=$2
  aws eks describe-nodegroup --cluster-name "$cluster" --nodegroup-name "$nodegroup" \
    --output text \
    --query 'nodegroup.[nodegroupName,status,instanceTypes[0],scalingConfig.[minSize,maxSize,desiredSize],amiType,capacityType]'
}

# List addons for a cluster
list_addons() {
  local cluster=$1
  aws eks list-addons --cluster-name "$cluster" \
    --output text --query 'addons[]'
}

# Get addon details
describe_addon() {
  local cluster=$1 addon=$2
  aws eks describe-addon --cluster-name "$cluster" --addon-name "$addon" \
    --output text \
    --query 'addon.[addonName,addonVersion,status,health.issues[0].code]'
}

# List Fargate profiles
list_fargate_profiles() {
  local cluster=$1
  aws eks list-fargate-profiles --cluster-name "$cluster" \
    --output text --query 'fargateProfileNames[]'
}
```

## Common Operations

### 1. Cluster Inventory with Version Status

```bash
#!/bin/bash
export AWS_PAGER=""
CLUSTERS=$(aws eks list-clusters --output text --query 'clusters[]')
for cluster in $CLUSTERS; do
  aws eks describe-cluster --name "$cluster" \
    --output text \
    --query 'cluster.[name,version,status,platformVersion]' &
done
wait
```

### 2. Nodegroup Health and Scaling

```bash
#!/bin/bash
export AWS_PAGER=""
CLUSTER=$1
NODEGROUPS=$(aws eks list-nodegroups --cluster-name "$CLUSTER" --output text --query 'nodegroups[]')
for ng in $NODEGROUPS; do
  aws eks describe-nodegroup --cluster-name "$CLUSTER" --nodegroup-name "$ng" \
    --output text \
    --query 'nodegroup.[nodegroupName,status,instanceTypes[0],scalingConfig.minSize,scalingConfig.maxSize,scalingConfig.desiredSize,amiType,capacityType]' &
done
wait
```

### 3. Addon Compatibility Check

```bash
#!/bin/bash
export AWS_PAGER=""
CLUSTER=$1
ADDONS=$(aws eks list-addons --cluster-name "$CLUSTER" --output text --query 'addons[]')
for addon in $ADDONS; do
  aws eks describe-addon --cluster-name "$CLUSTER" --addon-name "$addon" \
    --output text \
    --query 'addon.[addonName,addonVersion,status,health.issues[0].code,health.issues[0].message]' &
done
wait
```

### 4. IRSA (IAM Roles for Service Accounts) Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
CLUSTER=$1
OIDC_ISSUER=$(aws eks describe-cluster --name "$CLUSTER" \
  --output text --query 'cluster.identity.oidc.issuer' | sed 's|https://||')

# Find IAM roles that trust this cluster OIDC provider
aws iam list-roles --output text \
  --query "Roles[?contains(AssumeRolePolicyDocument | to_string(@), \`$OIDC_ISSUER\`)].[RoleName,Arn]"
```

### 5. Control Plane Logging Status

```bash
#!/bin/bash
export AWS_PAGER=""
CLUSTERS=$(aws eks list-clusters --output text --query 'clusters[]')
for cluster in $CLUSTERS; do
  aws eks describe-cluster --name "$cluster" \
    --output text \
    --query 'cluster.[name,logging.clusterLogging[0].enabled,logging.clusterLogging[0].types[]]' &
done
wait
```

## Anti-Hallucination Rules

1. **Never assume Kubernetes version** - Always query `describe-cluster` for the actual version. EKS versions lag upstream Kubernetes.
2. **Platform version != K8s version** - `platformVersion` (e.g., eks.5) is the EKS platform patch level, not the Kubernetes version.
3. **Nodegroup status is not node status** - A nodegroup can be ACTIVE while individual nodes are NotReady. Use kubectl for node health.
4. **OIDC provider must exist** - IRSA requires the cluster OIDC provider to be created in IAM. Check with `aws iam list-open-id-connect-providers`.
5. **Addon versions are cluster-specific** - Valid addon versions depend on the cluster K8s version. Use `describe-addon-versions` to check compatibility.

## Output Format

Present results as a structured report:
```
Aws Eks Report
══════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **EKS API vs kubectl**: EKS API manages the control plane and nodegroups. In-cluster resources (pods, services) require kubectl/k8s API.
- **Managed vs self-managed nodes**: `list-nodegroups` only returns managed nodegroups. Self-managed nodes (from ASGs) are not visible via EKS API.
- **Fargate profiles**: Fargate pods do not appear in nodegroups. Check `list-fargate-profiles` separately.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Cluster endpoint access**: Check `resourcesVpcConfig.endpointPublicAccess` and `endpointPrivateAccess` to understand API server accessibility.
