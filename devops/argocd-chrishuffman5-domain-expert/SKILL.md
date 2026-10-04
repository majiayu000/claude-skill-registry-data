---
name: argocd
description: "Covers Argo CD across all versions: Application and ApplicationSet CRDs, sync policies, app-of-apps pattern, RBAC, SSO integration, multi-cluster management, sync waves, and Argo Rollouts. WHEN: \"ArgoCD\", \"Argo CD\", \"argocd\", \"Application CRD\", \"ApplicationSet\", \"app-of-apps\", \"sync wave\", \"Argo Rollouts\", \"argocd sync\", \"argocd app\", \"ArgoCD RBAC\", \"ArgoCD SSO\"."
license: MIT
---

# Argo CD Expert

This skill covers Argo CD across supported versions (2.x, 3.x). Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes. It continuously monitors running applications and compares their live state against the desired state defined in Git. When a question is version-specific, read the matching file under `references/versions/`.

## How to Approach Tasks

1. **Classify** the request:
   - **Troubleshooting** -- Load `references/diagnostics.md` for sync failures, health issues, and connectivity problems
   - **Architecture** -- Load `references/architecture.md` for component internals, controller design, and multi-cluster patterns
   - **Best practices** -- Load `references/best-practices.md` for application design, RBAC, multi-tenancy, and performance

2. **Load context** -- Read the relevant reference file.

3. **Analyze** -- Apply ArgoCD-specific reasoning. Consider sync policy, health status, resource hooks, and project restrictions.

4. **Recommend** -- Provide Application/ApplicationSet YAML examples and `argocd` CLI commands.

5. **Verify** -- Suggest validation (`argocd app diff`, `argocd app get`, sync status in UI).

## Core Concepts

### Application CRD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
spec:
  project: default

  source:
    repoURL: https://github.com/org/config-repo.git
    targetRevision: main
    path: overlays/production

  destination:
    server: https://kubernetes.default.svc
    namespace: myapp

  syncPolicy:
    automated:
      prune: true           # Delete resources removed from Git
      selfHeal: true        # Revert manual changes
      allowEmpty: false     # Don't sync if source is empty
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### Sync Status

| Status | Meaning |
|---|---|
| **Synced** | Live state matches desired state in Git |
| **OutOfSync** | Live state differs from Git (need to sync) |
| **Unknown** | ArgoCD cannot determine status |

### Health Status

| Status | Meaning |
|---|---|
| **Healthy** | Resource is functioning correctly |
| **Progressing** | Resource is not yet healthy but working toward it |
| **Degraded** | Resource has errors |
| **Suspended** | Resource is paused (e.g., scaled to 0, CronJob suspended) |
| **Missing** | Resource defined in Git but doesn't exist in cluster |

### Sync Waves and Phases

Control the order of resource application:

```yaml
# Lower wave numbers sync first
apiVersion: v1
kind: Namespace
    argocd.argoproj.io/sync-wave: "-1"    # Create namespace first

---
apiVersion: apps/v1
kind: Deployment
    argocd.argoproj.io/sync-wave: "0"     # Then deploy app

---
apiVersion: batch/v1
kind: Job
    argocd.argoproj.io/sync-wave: "-1"     # Migrate before app
    argocd.argoproj.io/hook: PreSync       # Run as a pre-sync hook
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
```

### Resource Hooks

| Hook | When |
|---|---|
| `PreSync` | Before the sync operation |
| `Sync` | During the sync (with other resources) |
| `PostSync` | After all resources are synced and healthy |
| `SyncFail` | When sync operation fails |
| `Skip` | Skip this resource during sync |

## ApplicationSet

ApplicationSet generates Application CRDs from templates and generators:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
spec:
  generators:
    - clusters:
        selector:
          matchLabels:
            env: production

  template:
    metadata:
      name: '{{name}}-myapp'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/config-repo.git
        targetRevision: main
        path: 'overlays/{{metadata.labels.env}}'
      destination:
        server: '{{server}}'
        namespace: myapp
```

### Generator Types

| Generator | Source | Use Case |
|---|---|---|
| **List** | Static list of key-value pairs | Known set of environments |
| **Clusters** | ArgoCD-registered clusters | Multi-cluster deployment |
| **Git Directory** | Directories in a Git repo | Monorepo with per-app directories |
| **Git File** | JSON/YAML files in Git | Config-driven application generation |
| **Matrix** | Cartesian product of 2 generators | Cluster × environment combinations |
| **Merge** | Merge results of multiple generators | Combine with overrides |
| **Pull Request** | Open PRs in a repo | Ephemeral preview environments |
| **SCM Provider** | Repositories in a GitHub org/GitLab group | Org-wide standardized deployment |

## App-of-Apps Pattern

```yaml
# Root Application that manages other Applications
apiVersion: argoproj.io/v1alpha1
kind: Application
spec:
  project: default
  source:
    repoURL: https://github.com/org/config-repo.git
    path: argocd-apps/    # Directory containing Application YAMLs
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
```

```
argocd-apps/
├── monitoring.yaml      # Application CRD for monitoring stack
├── logging.yaml         # Application CRD for logging stack
├── myapp.yaml           # Application CRD for business app
└── cert-manager.yaml    # Application CRD for cert-manager
```

## Projects (Multi-Tenancy)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
spec:
  description: "Frontend team applications"

  sourceRepos:
    - 'https://github.com/org/frontend-*'

  destinations:
    - namespace: 'frontend-*'
      server: https://kubernetes.default.svc

  clusterResourceWhitelist:
    - group: ''
      kind: Namespace

  namespaceResourceBlacklist:
    - group: ''
      kind: ResourceQuota

  roles:
    - name: developer
      policies:
        - p, proj:team-frontend:developer, applications, get, team-frontend/*, allow
        - p, proj:team-frontend:developer, applications, sync, team-frontend/*, allow
      groups:
        - frontend-developers    # OIDC group mapping
```

## CLI Reference

```bash
# Application management
argocd app create myapp --repo https://github.com/org/repo.git --path overlays/prod --dest-server https://kubernetes.default.svc --dest-namespace myapp
argocd app list
argocd app get myapp
argocd app sync myapp
argocd app diff myapp
argocd app delete myapp

# Sync with specific revision
argocd app sync myapp --revision v1.2.3

# Sync with prune
argocd app sync myapp --prune

# Rollback
argocd app rollback myapp <history-id>
argocd app history myapp

# Cluster management
argocd cluster add my-context --name production
argocd cluster list

# Repository management
argocd repo add https://github.com/org/repo.git --ssh-private-key-path ~/.ssh/id_rsa
argocd repo list
```

## Version-Specific Guidance

| Version | Reference | What's new |
|---|---|---|
| 3.1 | `references/versions/3.1.md` | ApplicationSet progressive syncs, notification controller folded into core, granular RBAC, faster Helm OCI resolution |
| 3.2 | `references/versions/3.2.md` | Improved multi-cluster management, application health insights, config management plugin v2, sync window enhancements |
| 3.3 | `references/versions/3.3.md` | Declarative application management, enhanced ApplicationSet strategies, improved UI performance, native secret management integration |

## Reference Files

- `references/architecture.md` — ArgoCD components (API server, repo server, application controller, Redis, Dex), reconciliation loop, manifest generation, caching
- `references/best-practices.md` — Application design patterns, RBAC configuration, SSO integration, performance tuning, multi-cluster strategies, secret management
- `references/diagnostics.md` — Sync failures, health check issues, connectivity problems, performance debugging, common error messages

## Diagnostic Scripts

Ready-made argocd CLI triage scripts (read-only) in `scripts/`.

- `scripts/01-app-health.sh` -- Fleet-wide not-Healthy/not-Synced triage with state decoding
- `scripts/02-sync-failures.sh` -- One app's operation state, failing resources, sync history
