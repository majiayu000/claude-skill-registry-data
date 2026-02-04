---
name: cluster-status
description: Check Kubernetes cluster health and status. Use when checking nodes, pods, deployments, or overall cluster health.
---

# Cluster Status Check

Check the health and status of the Kubernetes cluster.

## Instructions

### Quick Status Overview

```bash
KUBECONFIG=/home/al/.kube/config

echo "=== Nodes ==="
kubectl get nodes -o wide

echo ""
echo "=== AI Agents Namespace ==="
kubectl get pods -n ai-agents

echo ""
echo "=== vLLM Namespace ==="
kubectl get pods -n vllm

echo ""
echo "=== Temporal Namespace ==="
kubectl get pods -n temporal
```

### Detailed Node Health

```bash
KUBECONFIG=/home/al/.kube/config

# Node resource usage
kubectl top nodes

# Node conditions
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.conditions[-1].type}={.status.conditions[-1].status}{"\n"}{end}'
```

### Flux GitOps Status

```bash
KUBECONFIG=/home/al/.kube/config flux get all -A
```

### Recent Events

```bash
KUBECONFIG=/home/al/.kube/config kubectl get events --sort-by='.lastTimestamp' -A | tail -20
```

### Problem Pods

```bash
KUBECONFIG=/home/al/.kube/config kubectl get pods -A | grep -v Running | grep -v Completed
```

## Health Indicators

- All nodes should be `Ready`
- Critical pods should be `Running`
- No pending or failed pods
- Flux reconciliation should be successful

## Common Issues

1. **ImagePullBackOff**: Image not pushed to registry
2. **CrashLoopBackOff**: Application crash, check logs
3. **Pending**: Insufficient resources or scheduling issues
4. **NotReady nodes**: Node health issue, check kubelet
