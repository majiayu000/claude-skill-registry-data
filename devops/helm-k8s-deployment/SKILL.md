---
name: helm-k8s-deployment
description: ALWAYS USE when working with Helm charts, Kubernetes deployments, kubectl commands, pod debugging, or container logs. Provides context-efficient strategies for chart development, K8s troubleshooting, and log analysis. MUST be loaded before any Helm or K8s work.
allowed-tools: Read, Grep, Glob, Bash, WebSearch
---

# Helm & Kubernetes Deployment (Research-Driven)

## Philosophy

This skill does NOT dump logs into context. Instead, it guides you to:
1. **Research** the current Helm/K8s state efficiently
2. **Extract** only relevant log lines (not full logs)
3. **Diagnose** issues with targeted commands
4. **Preserve context** by summarising rather than copying

## CRITICAL: Context-Efficient Log Analysis

**NEVER** dump full logs into context. Instead:

```bash
# ✅ GOOD: Get last 20 lines with errors only
kubectl logs <pod> --tail=20 2>&1 | grep -i "error\|fail\|exception"

# ✅ GOOD: Get events (more useful than logs for debugging)
kubectl get events --sort-by='.lastTimestamp' | tail -20

# ✅ GOOD: Check pod status first (often enough)
kubectl get pods -o wide

# ❌ BAD: Full log dump (burns context)
kubectl logs <pod>
```

## Pre-Implementation Research Protocol

### Step 1: Verify Cluster State

**ALWAYS run this first** (small output, high signal):
```bash
# Quick cluster health check
kubectl cluster-info 2>&1 | head -5

# Check namespace pods status
kubectl get pods -n <namespace> -o wide

# Recent events (usually reveals issues)
kubectl get events --sort-by='.lastTimestamp' -n <namespace> | tail -15
```

### Step 2: Helm Chart Validation (Before Deploy)

```bash
# Lint chart
helm lint charts/<chart-name>

# Dry-run template rendering
helm template charts/<chart-name> --debug 2>&1 | head -100

# Validate manifests
helm template charts/<chart-name> | kubectl apply --dry-run=client -f -
```

### Step 3: Targeted Debugging (Context-Efficient)

For pod issues, use this escalation:

1. **Status check** (no logs needed):
   ```bash
   kubectl describe pod <pod> | grep -A 20 "Events:"
   ```

2. **Recent logs only**:
   ```bash
   kubectl logs <pod> --tail=30 --since=5m
   ```

3. **Error extraction**:
   ```bash
   kubectl logs <pod> 2>&1 | grep -i "error\|exception\|fatal" | tail -20
   ```

4. **Container-specific** (for multi-container pods):
   ```bash
   kubectl logs <pod> -c <container> --tail=20
   ```

## Floe-Runtime Chart Structure

```
charts/
├── floe-runtime/       # Umbrella chart
├── floe-dagster/       # Dagster webserver/daemon
├── floe-cube/          # Cube semantic layer
└── floe-infrastructure/ # PostgreSQL, MinIO, Polaris
```

### Common Debugging Patterns

| Symptom | First Command | Not Full Logs |
|---------|--------------|---------------|
| Pod CrashLoopBackOff | `kubectl describe pod <x> \| grep -A10 Events` | Don't dump logs |
| Pod Pending | `kubectl describe pod <x> \| grep -A5 Conditions` | Check resources |
| ImagePullBackOff | `kubectl describe pod <x> \| grep -A3 Warning` | Check image name |
| Service not reachable | `kubectl get endpoints <svc>` | Check selectors |
| Helm install fails | `helm install --debug --dry-run 2>&1 \| tail -50` | Don't dump all |

## Context Injection (For Subagent Delegation)

When spawning the `docker-log-analyser` agent:

```markdown
Analyse logs for [pod-name] focusing on:
- Startup failures
- Connection errors to [service]
- Specific error: [paste only the error line, not full log]

Return ONLY:
1. Root cause (1-2 sentences)
2. Suggested fix
3. Commands to verify fix
```

## Quick Reference: Common Research Queries

**WebSearch patterns** (use when unfamiliar):
- "Helm [chart-name] values.yaml reference 2025"
- "Kubernetes [error-message] troubleshooting"
- "Dagster Helm chart configuration 2025"

## Integration with Floe Skills

| When working on... | Also consider... |
|-------------------|------------------|
| Dagster deployment | dagster-skill (for asset config) |
| Cube deployment | cube-skill (for API endpoints) |
| Polaris in K8s | polaris-skill (for catalog config) |

## Summary: Context Preservation Rules

1. **Never dump full logs** — extract error lines only
2. **Use `kubectl describe`** before `kubectl logs`
3. **Use `--tail=N`** on all log commands
4. **Delegate to docker-log-analyser agent** for deep analysis
5. **Summarise findings** rather than pasting output
