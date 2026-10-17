---
name: fluxcd-gitops
description: Use when flux CD GitOps — source controllers, kustomize/helm controllers,
  image automation, notifications. Use when working with fluxcd gitops.
domain: devops
author: oyi77
license: Apache-2.0
subdomain: devops
tags:
- ci-cd
- devops
- fluxcd
- gitops
- infrastructure
version: 1.0.0
category: devops
---



## Overview

Flux CD is a GitOps toolkit for Kubernetes using source, kustomize, helm, and notification controllers. Declarative CRDs manage the entire delivery pipeline.

## Capabilities

- Source controllers (Git, OCI, Helm repos, S3)
- Kustomize and Helm release controllers
- Image automation (scan repos, update manifests)
- Alert providers (Slack, Discord, PagerDuty)
- Multi-tenancy with impersonation
- Dependency management between resources

## When to Use
**Trigger phrases:**
- "fluxcd gitops"
- "Flux CD GitOps — source controllers, kustomize/helm controllers, image automatio"


- Kubernetes GitOps without a separate UI
- Prefer CRD-only approach over Application objects
- Need image automation (auto-update on new images)
- Multi-tenant clusters with namespace isolation

## Pseudo Source

- Configure automation, controllers, flux, fluxcd, gitops settings before first use


### GitRepository
```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: fleet
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/fleet
  ref:
    branch: main
  secretRef:
    name: github-credentials
```

### Kustomization
```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: GitRepository
    name: fleet
  path: ./apps/myapp/production
  prune: true
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: myapp
      namespace: production
  timeout: 5m
  dependsOn:
    - name: infrastructure
```

### HelmRelease
```yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: nginx
  namespace: production
spec:
  interval: 10m
  chart:
    spec:
      chart: nginx
      sourceRef:
        kind: HelmRepository
        name: bitnami
      version: "15.x.x"
  values:
    replicaCount: 3
    service:
      type: ClusterIP
```

### Image Automation
```yaml
# Scan image repos
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
metadata:
  name: myapp
spec:
  image: ghcr.io/org/myapp
  interval: 5m
---
# Update policy
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: myapp
spec:
  imageRepositoryRef:
    name: myapp
  policy:
    semver:
      range: ">=2.0.0 <3.0.0"
```

### Notifications
```yaml
apiVersion: notification.toolkit.fluxcd.io/v1beta3
kind: Alert
metadata:
  name: on-call
spec:
  providerRef:
    name: slack
  eventSeverity: info
  eventSources:
    - kind: Kustomization
      name: '*'
```

## Common Patterns

- **Bootstrapping**: `flux bootstrap github --owner=org --repository=fleet`
- **Multi-tenancy**: namespace isolation with service account impersonation
- **OCI sources**: store manifests as OCI artifacts
- **SOPS secrets**: encrypted secrets in Git with Mozilla SOPS

## How to Use

1. Define infrastructure as code (Terraform, CloudFormation, Pulumi)
2. Review changes through PR process before applying
3. Configure monitoring and alerting for critical paths
4. Set up secrets management (Vault, AWS Secrets Manager, etc.)
5. Document runbooks for deployment, rollback, and incident response
6. Test disaster recovery procedures regularly

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- **Infrastructure changes without review**: Unreviewed changes cause outages — use PRs for infra code
- **No rollback strategy**: Every deployment needs a tested rollback plan before it runs
- **Secrets in configuration files**: Secrets in YAML/JSON get committed to version control
- **Missing monitoring and alerting**: Without monitoring, outages go undetected until users report them
- **No documentation for runbooks**: Without runbooks, on-call engineers waste time re-discovering procedures

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Manual deployments are fine" | Manual deployments are error-prone and不可 repeatable. Automate. |
| "We do not need monitoring" | Without monitoring, you are flying blind. Add observability from day one. |
| "Infrastructure as code is overkill" | IaC enables reproducibility, version control, and disaster recovery. |