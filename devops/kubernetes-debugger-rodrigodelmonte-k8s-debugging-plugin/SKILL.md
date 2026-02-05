---
name: kubernetes-debugger
description: |
  Kubernetes debugging and troubleshooting best practices using MCP kubernetes tools.
  Use when: (1) Pods are failing, pending, or in CrashLoopBackOff/ImagePullBackOff states,
  (2) Services are unreachable or DNS resolution fails, (3) Deployments aren't rolling out,
  (4) Nodes are unhealthy or unschedulable, (5) Resource issues (OOM, CPU throttling),
  (6) Any "why isn't my Kubernetes workload working?" questions.
  Provides systematic debugging workflows using kubectl_get, kubectl_describe, kubectl_logs,
  exec_in_pod, and other MCP kubernetes tools.
---

# Kubernetes Debugger

Systematic debugging workflows for Kubernetes issues using MCP kubernetes tools.

## Prerequisites

### Install Kubernetes MCP Server

```bash
claude mcp add kubernetes --scope user -- npx mcp-server-kubernetes
```

**Requirements:**
- Access to a Kubernetes cluster configured for kubectl (minikube, Rancher Desktop, GKE, EKS, AKS, etc.)
- kubeconfig at `~/.kube/config` (default) or `KUBECONFIG` env var set
- Helm v3 in PATH (optional, for Helm operations)

**Alternative installation methods:**
```bash
# Global install
npm install -g mcp-server-kubernetes

# Or run directly with npx (no install)
npx mcp-server-kubernetes
```

**Verify installation:**
```bash
claude mcp list  # Should show 'kubernetes' server
```

## Quick Reference: MCP Tools

| Tool | Use For |
|------|---------|
| `kubectl_get` | List resources, check status, find resource names |
| `kubectl_describe` | Detailed info, events, conditions |
| `kubectl_logs` | Container stdout/stderr, application errors |
| `exec_in_pod` | Run commands inside containers |
| `kubectl_rollout` | Deployment rollout status/history |
| `node_management` | Cordon/drain/uncordon nodes |

## Debugging Decision Tree

```
Issue reported
    │
    ├─ Pod not running? ──────────► See: Pod Debugging Workflow
    │
    ├─ Service unreachable? ──────► See: Service/Network Debugging
    │
    ├─ Deployment stuck? ─────────► See: Deployment Debugging
    │
    ├─ Node issues? ──────────────► See: Node Debugging
    │
    └─ Performance/Resources? ────► See: Resource Debugging
```

## Pod Debugging Workflow

### Step 1: Get Pod Status

```
kubectl_get(resourceType="pods", namespace="<ns>")
```

Common statuses and their meaning:
- **Pending**: Scheduling issues (resources, node selector, affinity)
- **CrashLoopBackOff**: Container crashing repeatedly
- **ImagePullBackOff/ErrImagePull**: Cannot pull container image
- **Running** but not ready: Readiness probe failing
- **Terminating**: Stuck deletion (finalizers, PDB)

### Step 2: Check Events and Conditions

```
kubectl_describe(resourceType="pod", name="<pod>", namespace="<ns>")
```

Look for in output:
- **Events section**: Scheduling failures, image pull errors, probe failures
- **Conditions**: PodScheduled, Initialized, ContainersReady, Ready
- **Container State**: Waiting (reason), Running, Terminated (exit code)

### Step 3: Get Container Logs

```
kubectl_logs(resourceType="pod", name="<pod>", namespace="<ns>", container="<container>")
```

Options:
- `previous=true`: Logs from crashed container
- `tail=100`: Last N lines
- `since="1h"`: Logs from last hour

### Step 4: Exec Into Container (if running)

```
exec_in_pod(name="<pod>", namespace="<ns>", command=["sh", "-c", "<cmd>"])
```

Useful commands:
- `["cat", "/etc/resolv.conf"]` - Check DNS config
- `["env"]` - Verify environment variables
- `["ls", "-la", "/app"]` - Check mounted files
- `["nc", "-zv", "<host>", "<port>"]` - Test connectivity

## Common Pod Issues

### CrashLoopBackOff

1. Get logs: `kubectl_logs(previous=true)` for crashed container
2. Check exit code in `kubectl_describe` output
3. Common causes:
   - Exit code 1: Application error
   - Exit code 137: OOMKilled (check memory limits)
   - Exit code 143: SIGTERM (graceful shutdown issue)

### ImagePullBackOff

1. Check image name/tag in describe output
2. Verify image exists in registry
3. Check imagePullSecrets if private registry
4. Look for "Failed to pull image" in events

### Pending Pod

1. Check events for scheduling failure reason
2. Common causes:
   - `Insufficient cpu/memory`: Node capacity exhausted
   - `node(s) didn't match node selector`: Wrong labels
   - `PersistentVolumeClaim not bound`: Storage issue
   - `0/N nodes available`: Taints/tolerations mismatch

## Service/Network Debugging

### Step 1: Verify Service Exists

```
kubectl_get(resourceType="services", namespace="<ns>")
kubectl_describe(resourceType="service", name="<svc>", namespace="<ns>")
```

### Step 2: Check Endpoints

```
kubectl_get(resourceType="endpoints", name="<svc>", namespace="<ns>")
```

No endpoints? Check:
- Pod labels match service selector
- Pods are Running and Ready
- Target port matches container port

### Step 3: Test DNS Resolution

```
exec_in_pod(name="<debug-pod>", command=["nslookup", "<service>.<namespace>.svc.cluster.local"])
```

### Step 4: Test Connectivity

```
exec_in_pod(name="<debug-pod>", command=["nc", "-zv", "<service>", "<port>"])
```

## Deployment Debugging

### Check Rollout Status

```
kubectl_rollout(subCommand="status", resourceType="deployment", name="<deploy>", namespace="<ns>")
```

### View Rollout History

```
kubectl_rollout(subCommand="history", resourceType="deployment", name="<deploy>", namespace="<ns>")
```

### Rollback if Needed

```
kubectl_rollout(subCommand="undo", resourceType="deployment", name="<deploy>", namespace="<ns>")
```

### Common Issues

- **Progressing stuck**: New pods failing (check ReplicaSet pods)
- **Available < desired**: Pods not passing readiness probes
- **Surge/unavailable conflicts**: Check deployment strategy

## Node Debugging

### Check Node Status

```
kubectl_get(resourceType="nodes")
kubectl_describe(resourceType="node", name="<node>")
```

### Node Conditions to Check

| Condition | Problem If |
|-----------|------------|
| Ready | False or Unknown |
| MemoryPressure | True |
| DiskPressure | True |
| PIDPressure | True |
| NetworkUnavailable | True |

### Drain Node for Maintenance

```
node_management(operation="cordon", nodeName="<node>")  # Prevent new pods
node_management(operation="drain", nodeName="<node>", confirmDrain=true)  # Evict pods
# After maintenance:
node_management(operation="uncordon", nodeName="<node>")
```

## Resource Debugging

### Check Resource Usage

```
kubectl_generic(command="top", resourceType="pods", namespace="<ns>")
kubectl_generic(command="top", resourceType="nodes")
```

### OOMKilled Detection

1. `kubectl_describe` pod - look for "OOMKilled" in container state
2. Check memory limits vs actual usage
3. Solutions:
   - Increase memory limits
   - Fix memory leak in application
   - Add memory requests for better scheduling

### CPU Throttling

1. Check if CPU limits are too restrictive
2. Consider removing CPU limits (keep requests)
3. Use `kubectl top pods` to see actual usage

## Reference Files

- **[references/pod-states.md](references/pod-states.md)**: Complete pod state reference
- **[references/common-errors.md](references/common-errors.md)**: Error messages and solutions
- **[references/network-debug.md](references/network-debug.md)**: Network troubleshooting details
