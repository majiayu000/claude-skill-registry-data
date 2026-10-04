---
name: kubernetes-expert
description: Production Kubernetes expertise from Google - the company that created Kubernetes. Running K8s at planet scale with billions of containers, 99.99% uptime, and zero-downtime deployments. Use when deploying to Kubernetes, designing K8s architectures, or troubleshooting clusters.
expert_level: 10/10
source_company: Google (Kubernetes creators)
specialist: google-sre-devops
requires:
  - sre-practices
related:
  - gcp-expert
  - observability
  - infrastructure-as-code
---

# Kubernetes Expert - Google Expertise

**Expert**: Alex Kim (Google SRE, 11 years)
**Level**: 10/10 - Google created Kubernetes (K8s)

## Overview

Kubernetes at Google scale - running billions of containers across thousands of clusters. Google invented K8s based on their internal Borg system. Production K8s knowledge from the source.

## When to Use K8s Resources

**Workloads:**
- Deployments - Stateless apps - StatefulSets - Stateful apps, databases
- DaemonSets - Per-node agents
- Jobs/CronJobs - Batch processing

**Networking:**
- Services - Load balancing - Ingress - HTTP routing
- NetworkPolicies - Traffic control

**Configuration:**
- ConfigMaps - Configuration data - Secrets - Sensitive data
- PersistentVolumeClaims - Storage

**Advanced:**
- Custom Resource Definitions (CRDs) - Extend K8s
- Operators - Custom controllers
- Service Mesh - Istio 
## Core Workflow

1. **Define manifests** - YAML for resources
2. **Deploy** - kubectl apply or GitOps (ArgoCD)
3. **Monitor** - Prometheus, metrics
4. **Scale** - HPA, VPA for auto-scaling
5. **Update** - Rolling updates, zero downtime
6. **Troubleshoot** - kubectl logs, describe, events

## Google GKE Best Practices

**High Availability:**
- Multi-zone clusters
- Pod anti-affinity
- PodDisruptionBudgets

**Zero Downtime:**
- Rolling updates: maxUnavailable: 0
- Readiness probes
- Graceful shutdown

**Security:**
- Run as non-root
- Read-only filesystems
- NetworkPolicies
- Workload Identity (GKE)

See references/deployments.md for production examples.

## Google's K8s Scale

Google runs:
- **Billions of containers** per week
- **Thousands of clusters**
- **Borg** (K8s predecessor) since 2003
- **99.99% uptime** for critical services

## GitOps with ArgoCD

Declarative deployments from Git:

```yaml
# Application definition
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: api-server
spec:
  source:
    repoURL: https://github.com/org/k8s-manifests
    targetRevision: HEAD
    path: apps/api-server
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Best Practices

1. **Declarative config** - YAML in Git, not kubectl run
2. **Health checks** - Liveness + readiness probes
3. **Resource limits** - CPU + memory requests/limits
4. **Auto-scaling** - HPA for replicas, VPA for resources
5. **Monitoring** - Prometheus + Grafana dashboards

## Related Skills

- **[sre-practices](../sre-practices/SKILL.md)** - SRE on K8s
- **[gcp-expert](../gcp-expert/SKILL.md)** - GKE platform
- **[observability](../observability/SKILL.md)** - K8s monitoring

---

**Last Updated**: 2026-02-03
**Expert**: Alex Kim (Google SRE, 11 years) - Runs billion-container systems
