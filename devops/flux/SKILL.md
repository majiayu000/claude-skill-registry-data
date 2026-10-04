---
name: flux
description: "Covers Flux CD v2: GitRepository, Kustomization, HelmRelease, source controllers, image automation, notification controller, multi-tenancy, and Flagger integration. WHEN: \"Flux\", \"Flux CD\", \"flux bootstrap\", \"GitRepository\", \"Kustomization CRD\", \"HelmRelease\", \"HelmRepository\", \"source-controller\", \"flux reconcile\", \"Flagger\", \"flux image\"."
license: MIT
---

# Flux CD Expert

This skill covers Flux CD v2. Flux is a set of continuous delivery controllers for Kubernetes that reconcile the cluster state against desired state stored in Git repositories, Helm charts, OCI artifacts, and S3-compatible buckets.

## How to Approach Tasks

1. **Classify** the request:
   - **Troubleshooting** -- Load `references/diagnostics.md` for reconciliation failures, source errors, and connectivity issues
   - **Architecture** -- Load `references/architecture.md` for controller design, reconciliation loop, source types, and multi-tenancy model
   - **Best practices** -- Load `references/best-practices.md` for repository structure, Helm/Kustomize patterns, security, and scaling

2. **Load context** -- Read the relevant reference file.

3. **Analyze** -- Apply Flux-specific reasoning. Consider source type, reconciliation interval, dependency ordering, and namespace scoping.

4. **Recommend** -- Provide Flux CRD YAML examples and `flux` CLI commands.

5. **Verify** -- Suggest validation (`flux get all`, `flux reconcile`, `flux logs`).

## Core Concepts

### Flux Components

| Controller | CRDs | Purpose |
|---|---|---|
| **Source Controller** | GitRepository, HelmRepository, OCIRepository, Bucket | Fetch artifacts from external sources |
| **Kustomize Controller** | Kustomization | Apply Kustomize overlays and plain YAML |
| **Helm Controller** | HelmRelease | Manage Helm chart releases |
| **Notification Controller** | Provider, Alert, Receiver | Send/receive notifications and webhooks |
| **Image Reflector** | ImageRepository, ImagePolicy | Scan container registries for new tags |
| **Image Automation** | ImageUpdateAutomation | Automatically update image tags in Git |

### Bootstrap

```bash
# Bootstrap Flux with GitHub
flux bootstrap github \
  --owner=my-org \
  --repository=fleet-config \
  --branch=main \
  --path=clusters/production \
  --personal

# Bootstrap with GitLab
flux bootstrap gitlab \
  --owner=my-group \
  --repository=fleet-config \
  --branch=main \
  --path=clusters/production
```

Bootstrap:
1. Creates the Git repository (if it doesn't exist)
2. Installs Flux controllers in the cluster
3. Configures Flux to manage itself from the repository
4. Creates the initial Kustomization pointing to `--path`

### Source: GitRepository

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
spec:
  interval: 5m
  url: https://github.com/org/config-repo.git
  ref:
    branch: main
  secretRef:
    name: git-credentials    # SSH key or token
  ignore: |
    # Ignore files not relevant to deployment
    /*.md
    /docs/
```

### Kustomization (Flux CRD)

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
spec:
  interval: 10m
  targetNamespace: myapp
  sourceRef:
    kind: GitRepository
    name: app-config
  path: ./overlays/production
  prune: true                    # Delete resources removed from Git
  timeout: 5m
  retryInterval: 2m
  wait: true                     # Wait for resources to be ready
  force: false                   # Don't force apply (avoids conflicts)
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: myapp
      namespace: myapp
  dependsOn:
    - name: cert-manager         # Wait for cert-manager to be ready
    - name: database             # Wait for database to be ready
  postBuild:
    substitute:
      ENVIRONMENT: production
    substituteFrom:
      - kind: ConfigMap
        name: cluster-config
```

**Important**: Flux's `Kustomization` CRD is different from Kubernetes' `Kustomization` (`kustomize.config.k8s.io/v1beta1`). Flux's version wraps Kustomize and adds reconciliation, health checks, and dependency management.

### HelmRelease

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
spec:
  interval: 30m
  chart:
    spec:
      chart: ingress-nginx
      version: '4.x'              # Semver range
      sourceRef:
        kind: HelmRepository
        name: ingress-nginx
      interval: 12h               # How often to check for new chart versions
  values:
    controller:
      replicaCount: 3
      resources:
        requests:
          cpu: 200m
          memory: 256Mi
  valuesFrom:
    - kind: ConfigMap
      name: ingress-values
      valuesKey: overrides.yaml
  upgrade:
    remediation:
      retries: 3
      remediateLastFailure: true
  rollback:
    cleanupOnFail: true
  test:
    enable: true                  # Run Helm tests after install/upgrade
  install:
    createNamespace: true
  uninstall:
    keepHistory: false
```

### HelmRepository

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: HelmRepository
spec:
  interval: 24h
  url: https://kubernetes.github.io/ingress-nginx
  type: default    # or 'oci' for OCI registries
```

## Image Automation

Automatically update container image tags in Git when new images are pushed:

```yaml
# 1. Scan registry for tags
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
spec:
  image: ghcr.io/org/myapp
  interval: 5m

# 2. Define policy for selecting tags
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
spec:
  imageRepositoryRef:
    name: myapp
  policy:
    semver:
      range: '>=1.0.0'

# 3. Automate Git updates
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageUpdateAutomation
spec:
  interval: 30m
  sourceRef:
    kind: GitRepository
    name: app-config
  git:
    checkout:
      ref:
        branch: main
    commit:
      author:
        name: fluxcdbot
        email: flux@example.com
      messageTemplate: 'Update image {{ range .Changed.Changes }}{{ .OldValue }} -> {{ .NewValue }}{{ end }}'
    push:
      branch: main
  update:
    path: ./overlays/production
    strategy: Setters
```

Mark fields in YAML for auto-update:

```yaml
spec:
  containers:
    - name: myapp
      image: ghcr.io/org/myapp:1.2.3  # {"$imagepolicy": "flux-system:myapp"}
```

## Dependency Ordering

```yaml
# cert-manager must be ready before apps
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
  dependsOn:
    - name: cert-manager
    - name: database
  # myapp won't reconcile until cert-manager and database are Ready
```

## Notifications

```yaml
# Provider: where to send notifications
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Provider
spec:
  type: slack
  channel: deployments
  secretRef:
    name: slack-webhook-url

# Alert: what events to notify about
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Alert
spec:
  providerRef:
    name: slack
  eventSeverity: info
  eventSources:
    - kind: Kustomization
      name: '*'
    - kind: HelmRelease
      name: '*'
```

## CLI Reference

```bash
# Status
flux get all                          # All resources
flux get kustomizations               # Kustomizations
flux get helmreleases                 # HelmReleases
flux get sources git                  # Git sources

# Reconciliation
flux reconcile source git app-config  # Force Git pull
flux reconcile kustomization myapp    # Force Kustomize apply
flux reconcile helmrelease nginx      # Force Helm upgrade

# Debugging
flux logs                             # All controller logs
flux logs --kind=Kustomization        # Filtered by kind
flux events                           # Recent events

# Suspend/Resume
flux suspend kustomization myapp      # Pause reconciliation
flux resume kustomization myapp       # Resume

# Export (backup)
flux export source git --all > sources.yaml
flux export kustomization --all > kustomizations.yaml

# Health check
flux check                            # Verify Flux installation
flux check --pre                      # Pre-flight checks
```

## Reference Files

- `references/architecture.md` — Controller design, reconciliation loop, source types, artifact storage, multi-tenancy model
- `references/best-practices.md` — Repository structure, Kustomize/Helm patterns, multi-cluster, security, dependency management
- `references/diagnostics.md` — Reconciliation failures, source errors, Helm release issues, image automation problems
