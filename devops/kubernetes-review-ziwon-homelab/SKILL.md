---
name: kubernetes-review
description: Reviews Kubernetes manifests for best practices, security, and homelab standards compliance. Use when reviewing YAML files, K8s manifests, Helm values, or ArgoCD applications.
allowed-tools: Read, Grep, Glob
---

# Kubernetes Manifest Review

Review Kubernetes manifests against homelab standards.

## Checklist

### Resource Management
- [ ] CPU/Memory requests set
- [ ] CPU/Memory limits set
- [ ] Requests < Limits

```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 1000m
    memory: 1Gi
```

### Health Checks
- [ ] Liveness probe configured
- [ ] Readiness probe configured
- [ ] Appropriate initialDelaySeconds

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Security Context
- [ ] runAsNonRoot: true
- [ ] readOnlyRootFilesystem: true
- [ ] allowPrivilegeEscalation: false

```yaml
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
```

### Labels
- [ ] app.kubernetes.io/name
- [ ] app.kubernetes.io/instance
- [ ] app.kubernetes.io/version
- [ ] app.kubernetes.io/managed-by: argocd

### Secrets
- [ ] No hardcoded secrets in values
- [ ] Uses Infisical or external secrets
- [ ] No .env files committed

## GPU Workloads

For GPU workloads, also check:
- [ ] nvidia.com/gpu resource set
- [ ] GPU tolerations present
- [ ] nodeSelector for GPU nodes

## Reference

See @.claude/rules/kubernetes.md for complete guidelines.
