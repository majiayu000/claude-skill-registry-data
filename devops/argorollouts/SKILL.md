---
name: ArgoRollouts
description: Argo Rollouts progressive delivery controller for Kubernetes. USE WHEN user mentions rollouts, canary deployments, blue-green deployments, progressive delivery, traffic shifting, analysis templates, or Argo Rollouts. Provides deployment strategies, CLI commands, metrics analysis, and YAML examples.
---

# Argo Rollouts Skill

Comprehensive guide for Argo Rollouts - a Kubernetes controller providing advanced deployment capabilities including blue-green, canary, and experimentation for Kubernetes.

## Quick Reference

| Resource | Description |
|----------|-------------|
| **Rollout** | Replaces Deployment, adds progressive delivery strategies |
| **AnalysisTemplate** | Defines metrics queries for automated analysis |
| **AnalysisRun** | Instantiated analysis from template |
| **Experiment** | Runs ReplicaSets for A/B testing |
| **ClusterAnalysisTemplate** | Cluster-scoped AnalysisTemplate |

## Core Concepts

### Rollout CRD

The Rollout resource replaces standard Kubernetes Deployment and provides:

- **Blue-Green Strategy**: Instant traffic switching between versions
- **Canary Strategy**: Gradual traffic shifting with analysis gates
- **Traffic Management**: Integration with service meshes and ingress controllers
- **Automated Analysis**: Metrics-based promotion/rollback decisions

### Deployment Strategies

**Blue-Green:**

```yaml
strategy:
  blueGreen:
    activeService: my-app-active
    previewService: my-app-preview
    autoPromotionEnabled: false
```

**Canary:**

```yaml
strategy:
  canary:
    steps:
    - setWeight: 20
    - pause: {duration: 5m}
    - setWeight: 50
    - analysis:
        templates:
        - templateName: success-rate
```

## Traffic Management Integrations

| Provider | Configuration Key |
|----------|-------------------|
| **Istio** | `trafficRouting.istio` |
| **NGINX Ingress** | `trafficRouting.nginx` |
| **AWS ALB** | `trafficRouting.alb` |
| **Linkerd** | `trafficRouting.linkerd` |
| **SMI** | `trafficRouting.smi` |
| **Traefik** | `trafficRouting.traefik` |
| **Ambassador** | `trafficRouting.ambassador` |

## CLI Commands (kubectl-argo-rollouts)

```bash
# Installation
kubectl argo rollouts version

# Rollout Management
kubectl argo rollouts get rollout <name>
kubectl argo rollouts status <name>
kubectl argo rollouts promote <name>
kubectl argo rollouts abort <name>
kubectl argo rollouts retry <name>
kubectl argo rollouts undo <name>
kubectl argo rollouts pause <name>
kubectl argo rollouts restart <name>

# Dashboard
kubectl argo rollouts dashboard

# Validation
kubectl argo rollouts lint <file>
```

## Analysis Providers

| Provider | Use Case |
|----------|----------|
| **Prometheus** | Metrics queries with PromQL |
| **Datadog** | Datadog metrics API |
| **New Relic** | NRQL queries |
| **Wavefront** | Wavefront queries |
| **Kayenta** | Canary analysis platform |
| **CloudWatch** | AWS CloudWatch metrics |
| **Web** | HTTP endpoint checks |
| **Job** | Kubernetes Job-based analysis |

## Reference Documentation

- [Summary](references/summary.md) - Overview and architecture
- [Deployment Strategies](references/deployment-strategies.md) - Blue-green and canary details
- [CLI Commands](references/cli-commands.md) - kubectl plugin reference
- [Analysis & Metrics](references/analysis-metrics.md) - AnalysisTemplate configuration
- [Examples](references/examples.md) - Complete YAML examples

## Common Patterns

### Canary with Automated Analysis

```yaml
steps:
- setWeight: 10
- pause: {duration: 1m}
- analysis:
    templates:
    - templateName: success-rate
    args:
    - name: service-name
      value: my-service
- setWeight: 50
- pause: {duration: 2m}
```

### Blue-Green with Pre-Promotion Analysis

```yaml
strategy:
  blueGreen:
    activeService: active-svc
    previewService: preview-svc
    prePromotionAnalysis:
      templates:
      - templateName: smoke-tests
    autoPromotionEnabled: false
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Rollout stuck in Paused | Run `kubectl argo rollouts promote <name>` |
| Analysis failing | Check AnalysisRun status and metric queries |
| Traffic not shifting | Verify traffic management provider config |
| Pods not scaling | Check HPA and resource limits |

## Best Practices

1. **Always use analysis gates** for production canaries
2. **Set appropriate pause durations** between weight increases
3. **Configure rollback thresholds** in AnalysisTemplates
4. **Use preview services** for blue-green validation
5. **Monitor AnalysisRuns** during deployments
6. **Version your AnalysisTemplates** alongside application code
