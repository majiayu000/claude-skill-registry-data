---
name: check-cluster-health
description: Checks comprehensive health check for a Kubernetes Cluster.
allowed-tools: Read, Grep, Glob
---

# Check Cluster Health

Perform comprehensive health check of Kubernetes cluster infrastructure.

## When to Use

- Initial investigation of any production issue
- Before deep-diving into specific pods or services
- User reports "something is wrong" without specifics
- Periodic health checks
- Post-deployment validation
- After scaling events or cluster changes

## Skill Objective

Quickly assess the overall state of the Kubernetes cluster to identify:
- Node health and resource pressure
- Pod health across all namespaces
- System component status
- Recent critical events
- Resource constraints or bottlenecks

## Investigation Steps

### Step 1: Check Node Health

Get overview of all nodes in the cluster:

```bash
kubectl get nodes -o wide
```

**Look for:**
- Nodes in NotReady state
- Node ages (very old or very new nodes)
- Kubernetes versions (version skew)
- Internal/External IPs

**Expected Output:**
```
NAME      STATUS   ROLES           AGE   VERSION
node-1    Ready    control-plane   45d   v1.28.0
node-2    Ready    <none>          45d   v1.28.0
node-3    Ready    <none>          45d   v1.28.0
node-4    NotReady <none>          45d   v1.28.0  ⚠️
```

### Step 2: Check Node Resource Usage

Get current CPU and memory utilization:

```bash
kubectl top nodes
```

**Look for:**
- CPU usage > 80%
- Memory usage > 85%
- Significant imbalance between nodes

**Expected Output:**
```
NAME     CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
node-1   450m        22%    4Gi             50%
node-2   890m        44%    6Gi             75%
node-3   1200m       60%    7Gi             87%  ⚠️
node-4   100m        5%     2Gi             25%
```

### Step 3: Check Node Conditions

Inspect for resource pressure conditions:

```bash
kubectl describe nodes | grep -A 5 "Conditions:"
```

**Look for:**
- MemoryPressure: True
- DiskPressure: True
- PIDPressure: True
- NetworkUnavailable: True

**Critical Conditions:**
```
Conditions:
  Type             Status  Reason
  ----             ------  ------
  MemoryPressure   True    NodeHasInsufficientMemory  ⚠️
  DiskPressure     False   NodeHasSufficientDisk
  PIDPressure      False   NodeHasSufficientPID
  Ready            True    KubeletReady
```

### Step 4: Find Problematic Pods

Get all pods that are not in Running or Succeeded state:

```bash
kubectl get pods --all-namespaces --field-selector=status.phase!=Running,status.phase!=Succeeded
```

**Alternative - get all pods with issues:**
```bash
kubectl get pods --all-namespaces | grep -vE 'Running|Completed|Succeeded'
```

**Look for:**
- CrashLoopBackOff
- ImagePullBackOff
- Pending
- Error
- Evicted
- OOMKilled

**Expected Output:**
```
NAMESPACE   NAME                    READY   STATUS             RESTARTS   AGE
api         api-service-abc         0/1     CrashLoopBackOff   5          10m  ⚠️
api         api-service-xyz         0/1     OOMKilled          3          15m  ⚠️
default     worker-123              0/1     Pending            0          5m   ⚠️
monitoring  prometheus-456          0/2     ImagePullBackOff   0          20m  ⚠️
```

### Step 5: Check System Components

Verify kube-system namespace health:

```bash
kubectl get pods -n kube-system
```

**Critical components to check:**
- kube-apiserver
- kube-controller-manager
- kube-scheduler
- etcd
- coredns (or kube-dns)
- kube-proxy

**Expected Output:**
```
NAME                              READY   STATUS    RESTARTS   AGE
coredns-565d847f94-abcde          1/1     Running   0          45d
coredns-565d847f94-fghij          1/1     Running   0          45d
etcd-node-1                       1/1     Running   0          45d
kube-apiserver-node-1             1/1     Running   0          45d
kube-controller-manager-node-1    1/1     Running   0          45d
kube-proxy-klmno                  1/1     Running   0          45d
kube-scheduler-node-1             1/1     Running   0          45d
```

### Step 6: Review Recent Critical Events

Get events from the last hour, filtered for warnings and errors:

```bash
kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -50 | grep -E 'Warning|Error'
```

**Alternative - more structured:**
```bash
kubectl get events --all-namespaces --sort-by='.lastTimestamp' --field-selector type!=Normal
```

**Look for patterns:**
- Repeated OOMKilled events
- FailedScheduling (resource constraints)
- FailedMount (volume issues)
- ImagePullBackOff (registry issues)
- Evictions (resource pressure)
- BackOff (crashing containers)

**Expected Output:**
```
10m  Warning  FailedScheduling   pod/worker-123    0/4 nodes available: insufficient memory
8m   Warning  BackOff           pod/api-service   Back-off restarting failed container
5m   Warning  OOMKilled         pod/api-service   Container exceeded memory limit
3m   Warning  Evicted           pod/cache-789     The node was low on resource: memory
```

### Step 7: Check for Evicted Pods

Find pods that were evicted due to resource pressure:

```bash
kubectl get pods --all-namespaces --field-selector=status.phase=Failed | grep Evicted
```

**Evictions indicate:**
- Node resource pressure (memory/disk)
- Need for resource limits/requests tuning
- Possible need for cluster scaling

### Step 8: Review Resource Allocation

Check cluster-wide resource allocation:

```bash
kubectl describe nodes | grep -A 7 "Allocated resources:"
```

**Look for:**
- CPU allocation > 80%
- Memory allocation > 80%
- Pods per node approaching limits

**Expected Output:**
```
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource           Requests      Limits
  --------           --------      ------
  cpu                3800m (95%)   7200m (180%)  ⚠️
  memory             24Gi (75%)    32Gi (100%)   ⚠️
  ephemeral-storage  0 (0%)        0 (0%)
  hugepages-2Mi      0 (0%)        0 (0%)
```

## MCP Tools to Use

```
kubernetes.get_nodes()
kubernetes.get_node_metrics()
kubernetes.describe_node(node_name)
kubernetes.get_pods(namespace="all", field_selector="status.phase!=Running")
kubernetes.get_pods(namespace="kube-system")
kubernetes.get_events(namespace="all", since="1h", field_selector="type!=Normal")
```

## Output Format

Provide a structured summary in this format:

```markdown
# CLUSTER HEALTH SUMMARY
========================

## Cluster Overview
- **Total Nodes:** 5
- **Healthy Nodes:** 4
- **Unhealthy Nodes:** 1
- **Kubernetes Version:** v1.28.0

## Node Health

### Healthy Nodes ✓
- node-1: Ready (CPU: 22%, Memory: 50%)
- node-2: Ready (CPU: 44%, Memory: 75%)
- node-3: Ready (CPU: 60%, Memory: 87%) ⚠️ High memory

### Unhealthy Nodes ⚠️
- **node-4:** NotReady
  - Condition: KubeletNotReady
  - Reason: Node had insufficient memory
  - Duration: 15 minutes

## Pod Health Summary

**Total Pods:** 127
- Running: 120
- Pending: 4 ⚠️
- CrashLoopBackOff: 2 ⚠️
- ImagePullBackOff: 1 ⚠️

### Critical Pod Issues

1. **api-service-abc** (namespace: api)
   - Status: CrashLoopBackOff
   - Restarts: 5 times in 10 minutes
   - Action needed: Investigate with debug-pod-issues skill

2. **api-service-xyz** (namespace: api)
   - Status: OOMKilled
   - Restarts: 3 times in 15 minutes
   - Action needed: Memory limit investigation required

3. **worker-123** (namespace: default)
   - Status: Pending
   - Reason: Insufficient memory to schedule
   - Action needed: Resource analysis needed

4. **prometheus-456** (namespace: monitoring)
   - Status: ImagePullBackOff
   - Reason: Failed to pull image
   - Action needed: Check registry connectivity

## System Components ✓

All critical system components healthy:
- coredns: 2/2 pods running
- kube-apiserver: Running
- kube-controller-manager: Running
- kube-scheduler: Running
- etcd: Running
- kube-proxy: DaemonSet 5/5 ready

## Recent Critical Events (Last 60 minutes)

**OOM Kills:** 3 occurrences
- 14:23: api-service-xyz OOMKilled (namespace: api)
- 14:25: api-service-xyz OOMKilled (namespace: api)
- 14:27: api-service-xyz OOMKilled (namespace: api)

**Scheduling Failures:** 4 occurrences
- 14:20: worker-123 FailedScheduling: insufficient memory
- 14:22: worker-456 FailedScheduling: insufficient memory
- 14:25: worker-789 FailedScheduling: insufficient memory
- 14:28: cache-abc FailedScheduling: insufficient cpu

**Node Issues:**
- 14:15: node-4 NodeNotReady: KubeletNotReady

**Evictions:** 2 occurrences
- 14:18: cache-xyz Evicted: node low on memory
- 14:22: cache-abc Evicted: node low on memory

## Resource Pressure Analysis

### Node-4: MemoryPressure Detected ⚠️
- Current usage: 28Gi / 32Gi (87%)
- Condition: MemoryPressure True
- Impact: Pods may be evicted
- Action: Investigate high memory consumers

### Cluster-Wide Resource Allocation
- **CPU:** 75% allocated (approaching capacity)
- **Memory:** 82% allocated ⚠️ (critical threshold)
- **Risk:** New pods may not schedule

## Issues Detected

### 🚨 CRITICAL Issues (Require Immediate Action)

1. **Multiple OOM Kills in api namespace**
   - Impact: Service degradation/outages
   - Pods affected: api-service-xyz
   - Recommendation: Increase memory limits or investigate memory leak
   - Next step: Use `debug-pod-issues` skill

2. **Node-4 Unhealthy (NotReady)**
   - Impact: Reduced cluster capacity
   - Duration: 15 minutes
   - Recommendation: Investigate node logs, consider cordoning/draining
   - Next step: SSH to node or check kubelet logs

3. **Cluster Memory Capacity Critical (82% allocated)**
   - Impact: Risk of scheduling failures
   - Pods pending: 4
   - Recommendation: Scale cluster or optimize workloads
   - Next step: Use `analyze-resource-usage` skill

### ⚠️ WARNING Issues (Should Be Addressed)

4. **Node-3 High Memory Usage (87%)**
   - Impact: Risk of pressure condition
   - Current state: Still Ready
   - Recommendation: Monitor closely, consider rebalancing pods

5. **ImagePullBackOff in monitoring namespace**
   - Impact: Prometheus not available
   - Likely cause: Registry connectivity or credentials
   - Recommendation: Check image repository access

## Recommended Actions (Priority Order)

### Immediate (Next 15 minutes)
1. **Investigate api-service OOM kills** → Use `debug-pod-issues` skill on api-service-xyz
2. **Check node-4 status** → SSH to node or review kubelet logs
3. **Review pending pods** → Use `analyze-resource-usage` to understand capacity

### Short Term (Next hour)
4. Increase memory limits for api-service pods
5. Consider scaling cluster (add nodes or upsize)
6. Fix ImagePullBackOff for prometheus
7. Investigate memory usage on node-3

### Long Term (This week)
8. Implement pod resource requests/limits across all workloads
9. Set up cluster autoscaling
10. Review and optimize memory-intensive workloads
11. Implement monitoring alerts for:
    - Node NotReady conditions
    - OOM kill events
    - Resource allocation thresholds (>80%)
    - Pod evictions

## Next Steps

Based on the findings, I recommend:

1. **Deep dive into OOM issues** → Skill: `debug-pod-issues`
   - Target: api-service-xyz in api namespace
   
2. **Analyze resource usage patterns** → Skill: `analyze-resource-usage`
   - Focus on memory consumption and allocation
   
3. **Check logs for crash patterns** → Skill: `inspect-logs`
   - Target: api-service pods for error patterns

Would you like me to proceed with investigating the OOM kills in the api-service pods?
```

## Red Flags to Watch For

- 🚨 **Node NotReady status** - Immediate impact on capacity
- 🚨 **Multiple pods in CrashLoopBackOff** - Application issues
- 🚨 **Repeated OOMKilled events** - Memory configuration problems
- 🚨 **System component failures** - Cluster instability
- 🚨 **High resource allocation** (>85%) - Scheduling issues imminent
- ⚠️ **High restart counts** (>5 in last hour) - Application instability
- ⚠️ **Pending pods** - Resource constraints
- ⚠️ **ImagePullBackOff** - Registry or networking issues
- ⚠️ **Volume mount failures** - Storage problems
- ⚠️ **Evicted pods** - Node resource pressure

## Decision Tree - Next Skill to Use

```
Based on findings, recommend next skill:

If OOMKilled or CrashLoopBackOff detected:
  → Use `debug-pod-issues` skill

If high CPU/Memory usage detected:
  → Use `analyze-resource-usage` skill

If connection errors in events:
  → Use `check-network-connectivity` skill

If errors in events but pods running:
  → Use `inspect-logs` skill

If multiple issues:
  → Prioritize by severity, start with pod crashes
```

## Common Patterns & Root Causes

### Pattern: Multiple OOM Kills
**Indicates:** Memory limits too low or memory leak
**Next Action:** debug-pod-issues + inspect-logs

### Pattern: Many Pending Pods
**Indicates:** Insufficient cluster capacity
**Next Action:** analyze-resource-usage

### Pattern: Node NotReady + Evictions
**Indicates:** Node resource exhaustion
**Next Action:** Investigate node directly, consider draining

### Pattern: System Component Failure
**Indicates:** Critical cluster issue
**Next Action:** Immediate investigation, possibly escalate

### Pattern: ImagePullBackOff
**Indicates:** Registry access issues
**Next Action:** Check network connectivity, registry credentials

## Skill Completion Criteria

This skill is complete when:
- ✓ Node health assessed
- ✓ Pod health across all namespaces evaluated
- ✓ System components verified
- ✓ Recent critical events reviewed
- ✓ Issues categorized by severity
- ✓ Recommended next steps provided
- ✓ Clear indication of which skill to use next

## Notes for Agent

- Always start with this skill for vague issues
- Provide executive summary before detailed findings
- Categorize issues by severity (Critical/Warning/Info)
- Explicitly recommend next skill based on findings
- Include specific pod names, namespaces, timestamps
- Highlight patterns, not just individual issues
- Keep summary concise but comprehensive