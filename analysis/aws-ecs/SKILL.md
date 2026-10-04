---
name: aws-ecs
description: |
  Use when working with Aws Ecs — aWS ECS cluster health, service status, task
  analysis, capacity provider management, and deployment tracking. Covers
  service stability, task failure investigation, container insights, resource
  utilization, and scaling analysis.
connection_type: aws
preload: false
---

# AWS ECS Skill

Analyze AWS ECS clusters, services, and tasks with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-ecs/` → ECS-specific analysis (clusters, services, tasks, capacity providers)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

# CORRECT: Parallel service analysis
for service in $services; do
  describe_service "$cluster" "$service" &
done
wait
```

**FORBIDDEN**: Sequential loops for independent describe calls.

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List all clusters
list_clusters() {
  aws ecs list-clusters --output text --query 'clusterArns[]' | tr '\t' '\n' | sed 's|.*/||'
}

# Get cluster details
describe_cluster() {
  local cluster=$1
  aws ecs describe-clusters --clusters "$cluster" \
    --include STATISTICS ATTACHMENTS \
    --output text \
    --query 'clusters[].[clusterName,status,registeredContainerInstancesCount,runningTasksCount,pendingTasksCount,activeServicesCount]'
}

# List services in a cluster
list_services() {
  local cluster=$1
  aws ecs list-services --cluster "$cluster" \
    --output text --query 'serviceArns[]' | tr '\t' '\n' | sed 's|.*/||'
}

# Get service details
describe_service() {
  local cluster=$1 service=$2
  aws ecs describe-services --cluster "$cluster" --services "$service" \
    --output text \
    --query 'services[].[serviceName,status,desiredCount,runningCount,pendingCount,launchType,deployments[0].rolloutState]'
}

# Get recent task failures
get_stopped_tasks() {
  local cluster=$1
  aws ecs list-tasks --cluster "$cluster" --desired-status STOPPED \
    --output text --query 'taskArns[]' | tr '\t' '\n' | head -10
}

# Describe tasks (batch)
describe_tasks() {
  local cluster=$1
  shift
  local task_arns="$@"
  [ -z "$task_arns" ] && return
  aws ecs describe-tasks --cluster "$cluster" --tasks $task_arns \
    --output text \
    --query 'tasks[].[taskArn,lastStatus,stoppedReason,stopCode,containers[0].exitCode]'
}

# Get service events (last 5)
get_service_events() {
  local cluster=$1 service=$2
  aws ecs describe-services --cluster "$cluster" --services "$service" \
    --output text \
    --query 'services[0].events[:5].[createdAt,message]'
}
```

## Common Operations

### 1. Cluster Health Overview

```bash
#!/bin/bash
export AWS_PAGER=""
CLUSTERS=$(aws ecs list-clusters --output text --query 'clusterArns[]' | tr '\t' '\n' | sed 's|.*/||')
for cluster in $CLUSTERS; do
  aws ecs describe-clusters --clusters "$cluster" \
    --include STATISTICS \
    --output text \
    --query 'clusters[].[clusterName,status,registeredContainerInstancesCount,runningTasksCount,pendingTasksCount,activeServicesCount]' &
done
wait
```

### 2. Service Deployment Status

```bash
#!/bin/bash
export AWS_PAGER=""
CLUSTER=$1
SERVICES=$(aws ecs list-services --cluster "$CLUSTER" --output text --query 'serviceArns[]' | tr '\t' '\n' | sed 's|.*/||')
for svc in $SERVICES; do
  aws ecs describe-services --cluster "$CLUSTER" --services "$svc" \
    --output text \
    --query 'services[].[serviceName,desiredCount,runningCount,deployments[0].rolloutState,deployments[0].taskDefinition]' &
done
wait
```

### 3. Task Failure Investigation

```bash
#!/bin/bash
export AWS_PAGER=""
CLUSTER=$1
TASK_ARNS=$(aws ecs list-tasks --cluster "$CLUSTER" --desired-status STOPPED \
  --output text --query 'taskArns[]' | tr '\t' '\n' | head -20)
[ -z "$TASK_ARNS" ] && echo "No stopped tasks" && exit 0
aws ecs describe-tasks --cluster "$CLUSTER" --tasks $TASK_ARNS \
  --output text \
  --query 'tasks[].[group,lastStatus,stoppedReason,stopCode,containers[0].exitCode,stoppedAt]'
```

### 4. Capacity Provider Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
CLUSTERS=$(aws ecs list-clusters --output text --query 'clusterArns[]' | tr '\t' '\n' | sed 's|.*/||')
for cluster in $CLUSTERS; do
  aws ecs describe-clusters --clusters "$cluster" \
    --include ATTACHMENTS \
    --output text \
    --query 'clusters[].[clusterName,capacityProviders[],defaultCapacityProviderStrategy[].[capacityProvider,weight,base]]' &
done
wait
```

### 5. Container Resource Utilization

```bash
#!/bin/bash
export AWS_PAGER=""
CLUSTER=$1
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "1 day ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-1d +"%Y-%m-%dT%H:%M:%S")
SERVICES=$(aws ecs list-services --cluster "$CLUSTER" --output text --query 'serviceArns[]' | tr '\t' '\n' | sed 's|.*/||')
for svc in $SERVICES; do
  {
    cpu=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/ECS --metric-name CPUUtilization \
      --dimensions Name=ClusterName,Value="$CLUSTER" Name=ServiceName,Value="$svc" \
      --start-time "$START" --end-time "$END" \
      --period 86400 --statistics Average Maximum \
      --output text --query 'Datapoints[0].[Average,Maximum]')
    mem=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/ECS --metric-name MemoryUtilization \
      --dimensions Name=ClusterName,Value="$CLUSTER" Name=ServiceName,Value="$svc" \
      --start-time "$START" --end-time "$END" \
      --period 86400 --statistics Average Maximum \
      --output text --query 'Datapoints[0].[Average,Maximum]')
    printf "%s\tCPU:%s\tMEM:%s\n" "$svc" "$cpu" "$mem"
  } &
done
wait
```

## Anti-Hallucination Rules

1. **Never assume launch type** - Always check `launchType` field. Services can be FARGATE, EC2, or EXTERNAL. Do not assume Fargate.
2. **Desired vs Running count** - `desiredCount != runningCount` does not always mean failure. It can indicate scaling in progress.
3. **Task definition != running version** - Services may have multiple deployments active during rolling updates. Check `deployments[]` not just `taskDefinition`.
4. **Container Insights required** - CPU/Memory utilization metrics require Container Insights enabled on the cluster. If no metrics exist, check cluster settings.
5. **Service ARN format changed** - Newer accounts use long ARN format. Always parse service name from the end of the ARN.

## Output Format

Present results as a structured report:
```
Aws Ecs Report
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

- **Batch describe limits**: `describe-tasks` accepts max 100 task ARNs per call. Chunk if needed.
- **Service vs task metrics**: CloudWatch ECS metrics are at service level (ClusterName + ServiceName dimensions), not individual task level.
- **Stopped task retention**: ECS only retains stopped tasks for ~1 hour. For historical failures, use CloudWatch Logs or EventBridge.
- **Fargate platform version**: Check `platformVersion` for Fargate tasks. `LATEST` is not always the newest version.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum` (NOT `Average,Maximum`).
