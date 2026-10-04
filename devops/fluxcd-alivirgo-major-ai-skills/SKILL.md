---
name: fluxcd
description: "Configure Flux CD GitRepository, Kustomization, and HelmRelease resources; troubleshoot reconciliation and image-update automation."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["flux", "fluxcd", "gitops", "kubernetes", "helmrelease", "kustomization"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Flux CD GitOps AI Skill Guide

## Overview

Flux reconciles Kubernetes clusters from Git using composable controllers: **source-controller** (GitRepository, OCIRepository, HelmRepository), **kustomize-controller**, **helm-controller**, and optional **image-automation**. Unlike a single Application CR, Flux models sources and apply pipelines as separate objects. Agents should debug by reading Ready conditions on each object in the dependency chain.

```
GitRepository / OCIRepository
        |
        v
Kustomization / HelmRelease  -->  cluster apply
        ^
ImageRepository + ImagePolicy + ImageUpdateAutomation (optional)
```

## When to use

- Bootstrapping Flux on a cluster (`flux bootstrap`)
- Authoring GitRepository + Kustomization or HelmRelease pipelines
- Debugging stalled reconciliations and chart render errors
- Image tag automation updating Git automatically

## Operational directives

1. Trace Ready conditions from source -> Kustomization/HelmRelease -> workload health.
2. Prefer immutable digests in production overlays; use image automation deliberately.
3. Keep bootstrap and tenant paths separated; restrict Impersonation / SA privileges.
4. Use `flux reconcile` after Git pushes when waiting on long intervals is costly.
5. Do not manually patch Flux-managed resources without suspending first.

## Concrete examples

### Bootstrap (GitHub)

```bash
flux bootstrap github \
  --owner=example \
  --repository=fleet-gitops \
  --branch=main \
  --path=clusters/prod \
  --personal
```

### GitRepository + Kustomization

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: platform
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/example/fleet-gitops
  ref: { branch: main }
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: api
  namespace: flux-system
spec:
  interval: 5m
  path: ./apps/api/prod
  prune: true
  sourceRef:
    kind: GitRepository
    name: platform
  targetNamespace: api
```

### HelmRelease sketch

```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: redis
  namespace: data
spec:
  interval: 10m
  chart:
    spec:
      chart: redis
      version: "19.x"
      sourceRef:
        kind: HelmRepository
        name: bitnami
        namespace: flux-system
  values:
    auth:
      enabled: true
```

### CLI debug chain

```bash
flux get sources git
flux get kustomizations
flux get helmreleases -A
flux logs --kind=Kustomization --name=api
flux reconcile source git platform
flux reconcile kustomization api --with-source
flux suspend kustomization api
flux resume kustomization api
```

## Condition cheat sheet

| Object | Not Ready clue | Action |
| :--- | :--- | :--- |
| GitRepository | auth / clone fail | Fix secret, URL, ref |
| Kustomization | build/apply error | `flux logs`; fix YAML |
| HelmRelease | values/schema | `helm template` locally; pin chart |
| ImagePolicy | no tag match | Fix semver policy filter |

## Best practices

1. Directory-per-cluster under `clusters/` with clear promotion paths.
2. Enable prune carefully; review inventory before first automated prune.
3. Use OCI artifacts for air-gapped or signed delivery when required.
4. Document suspend/resume runbook for incident freezes.

## Limitations

- Flux does not replace CI builds; it consumes artifacts and manifests.
- Multi-tenancy needs careful RBAC and namespace isolation.
- HelmRelease debugging can be opaque without local helm rendering.

## Related skills

- `argocd` - alternative GitOps UX and Application model
- `kubernetes` - workload-level failure diagnosis
- `trivy` - scan images before automation bumps tags
- `makefile-automation` - local render/validate targets for GitOps repos
