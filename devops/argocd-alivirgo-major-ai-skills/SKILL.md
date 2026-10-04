---
name: argocd
description: "Configure Argo CD Applications, AppProjects, and sync policies; inspect health checks and troubleshoot GitOps rollouts."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["argocd", "gitops", "kubernetes", "cd", "sync", "helm"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Argo CD GitOps AI Skill Guide

## Overview

Argo CD continuously reconciles Kubernetes cluster state to manifests stored in Git (plain YAML, Helm, Kustomize). An **Application** points at a repo path and destination cluster/namespace; sync status and health drive rollout visibility. Agents should favor declarative Application CRs, restrict AppProjects, and avoid click-ops syncs that bypass PR review.

```
Git repo (desired) ----> Argo CD Application controller
                              |
                              v
                     Destination cluster API
                              |
                              v
                     Live resources + health
```

## When to use

- Wiring Kubernetes CD so merges to main deploy automatically
- Debugging `OutOfSync`, `Degraded`, or hook failures
- Multi-cluster or multi-tenant AppProject boundaries
- Comparing Argo CD vs Flux for GitOps on existing clusters

## Operational directives

1. Desired state lives in Git - do not `kubectl edit` production objects managed by Argo.
2. Prefer automated sync with **prune** and **selfHeal** only after dry-run confidence.
3. Scope AppProjects to allowed repos, namespaces, and cluster destinations.
4. Use sync waves/hooks sparingly; document ordering assumptions.
5. Never embed cluster admin tokens in Application manifests.

## Concrete examples

### Application manifest

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: api
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/example/platform-gitops
    targetRevision: main
    path: apps/api/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: api
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### CLI diagnostics

```bash
argocd login argocd.example.com --sso
argocd app list
argocd app get api
argocd app sync api --dry-run
argocd app history api
argocd app rollback api <id>
argocd app diff api
```

### Health and sync interpretation

| Status | Meaning | Next step |
| :--- | :--- | :--- |
| Synced + Healthy | Live matches Git and probes OK | Done |
| OutOfSync | Drift or pending commit | `app diff`; sync or revert Git |
| Progressing | Rollout in flight | Watch RS/Pods |
| Degraded | Resource unhealthy | Pod logs/events; fix Git |

## Best practices

1. One Application per deployable service (or ApplicationSet for fleets).
2. Separate render tools clearly - don't mix Helm values chaos with Kustomize overlays blindly.
3. Protect `main` with PR checks; Argo only watches reviewed revisions.
4. Use ignoreDifferences only for known controller-owned fields (e.g. HPA replicas).

## Limitations

- Argo does not build images; pair with CI that updates tags/digests in Git.
- Misconfigured automation+prune can delete resources quickly - test in nonprod first.
- Multi-source Applications add complexity; document which source owns which path.

## Related skills

- `kubernetes` - underlying workload debugging
- `fluxcd` - alternative GitOps engine
- `docker` - image digests referenced from Git
- `trivy` - scan images before Git tag bumps
