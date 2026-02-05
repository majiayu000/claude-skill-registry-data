---
name: validate
description: Validate cluster configuration and health. Use when checking if cluster is properly configured, before deployments, or diagnosing issues.
---

# Validate Cluster Health

Comprehensive validation of cluster configuration and health.

## Instructions

### 1. Node Connectivity

```bash
KUBECONFIG=/home/al/.kube/config

echo "=== Node Connectivity ==="
for node in $(kubectl get nodes -o jsonpath='{.items[*].metadata.name}'); do
    status=$(kubectl get node $node -o jsonpath='{.status.conditions[-1].status}')
    echo "$node: Ready=$status"
done
```

### 2. Critical Services

```bash
KUBECONFIG=/home/al/.kube/config

echo ""
echo "=== Critical Services ==="

# Check Temporal
temporal_ready=$(kubectl get pods -n temporal -l app=temporal-frontend -o jsonpath='{.items[0].status.phase}' 2>/dev/null || echo "missing")
echo "Temporal Frontend: $temporal_ready"

# Check vLLM
vllm_ready=$(kubectl get pods -n vllm -l app=llm-api -o jsonpath='{.items[0].status.phase}' 2>/dev/null || echo "missing")
echo "vLLM API: $vllm_ready"

# Check Flux
flux_ready=$(kubectl get pods -n flux-system -l app=source-controller -o jsonpath='{.items[0].status.phase}' 2>/dev/null || echo "missing")
echo "Flux Source Controller: $flux_ready"
```

### 3. Storage

```bash
KUBECONFIG=/home/al/.kube/config

echo ""
echo "=== Persistent Volume Claims ==="
kubectl get pvc -A
```

### 4. Network Policies

```bash
KUBECONFIG=/home/al/.kube/config

echo ""
echo "=== Services ==="
kubectl get svc -n ai-agents
kubectl get svc -n vllm
```

### 5. Secrets

```bash
KUBECONFIG=/home/al/.kube/config

echo ""
echo "=== Secrets (presence check) ==="
kubectl get secrets -n ai-agents | grep -v default-token
```

### 6. ConfigMaps

```bash
KUBECONFIG=/home/al/.kube/config

echo ""
echo "=== Model Configuration ==="
kubectl get configmap model-config -n ai-agents -o yaml | grep -A5 "data:"
```

## Validation Checklist

- [ ] All nodes Ready
- [ ] Temporal frontend accessible
- [ ] vLLM API serving requests
- [ ] Model ConfigMaps in sync across namespaces
- [ ] Secrets present for Discord, database
- [ ] PVCs bound and accessible
