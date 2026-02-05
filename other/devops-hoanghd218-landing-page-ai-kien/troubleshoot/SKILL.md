---
name: troubleshoot
description: Diagnoses Kubernetes pod issues automatically. Use when pods are in CrashLoopBackOff, ImagePullBackOff, Pending, or Error state. Analyzes events, logs, and resource status to identify root causes.
allowed-tools: Bash, Read, Grep, Glob
---

# Kubernetes Troubleshoot

Automatically diagnose common Kubernetes issues.

## Trigger Phrases

- "왜 안돼", "왜 안되지", "pod가 죽어", "에러나"
- "troubleshoot", "debug", "diagnose"
- "CrashLoopBackOff", "ImagePullBackOff", "Pending", "Error"

## Diagnostic Flow

### 1. Get Pod Status

```bash
export KUBECONFIG=$HOME/.kube/config.home
kubectl get pods -n <namespace> <pod-name> -o wide
```

### 2. Check Events

```bash
kubectl describe pod -n <namespace> <pod-name> | grep -A 20 "Events:"
```

### 3. Get Logs

```bash
# Current container
kubectl logs -n <namespace> <pod-name> --tail=100

# Previous container (if restarting)
kubectl logs -n <namespace> <pod-name> --previous --tail=100

# All containers in pod
kubectl logs -n <namespace> <pod-name> --all-containers=true --tail=50
```

### 4. Check Resource Status

```bash
# Node resources
kubectl top nodes

# Pod resources
kubectl top pods -n <namespace>

# PVC status
kubectl get pvc -n <namespace>
```

## Common Issues & Solutions

### CrashLoopBackOff

1. **Check logs** for application errors
2. **Verify** environment variables (Infisical secrets mounted?)
3. **Check** resource limits (OOMKilled?)
4. **Validate** startup/liveness probes

### ImagePullBackOff

1. **Verify** image name and tag
2. **Check** imagePullSecrets configured
3. **Test** registry connectivity
4. **Confirm** image exists in registry

### Pending

1. **Check** node resources (CPU/Memory)
2. **Verify** nodeSelector/affinity matches
3. **Check** PVC binding status
4. **Review** taints/tolerations

### OOMKilled

1. **Increase** memory limits
2. **Check** for memory leaks in application
3. **Review** JVM heap settings (if Java)

### GPU Issues

```bash
# Check GPU operator
kubectl get pods -n gpu-operator

# Check device plugin
kubectl logs -n gpu-operator -l app=nvidia-device-plugin-daemonset --tail=50

# Check GPU allocation
kubectl describe node | grep -A 5 "nvidia.com/gpu"
```

## ArgoCD Sync Issues

```bash
# App status
argocd app get <app-name>

# Sync details
argocd app sync <app-name> --dry-run

# Resource diff
argocd app diff <app-name>

# Force refresh
argocd app get <app-name> --refresh
```

## Output Format

Provide diagnosis in this format:

```
## Issue Summary
[Brief description of the problem]

## Root Cause
[Identified cause with evidence]

## Solution
[Step-by-step fix]

## Prevention
[How to avoid this in the future]
```

## Reference

- @.claude/rules/kubernetes.md
- @.claude/rules/argocd-apps.md
