---
name: flux-operator-cli
description: >
  Builds Flux manifests locally, diffs YAML files, patches FluxInstance upgrades,
  creates authentication secrets, traces GitOps delivery pipelines, and bootstraps
  clusters with the Flux Operator.
  Use this skill whenever the user mentions flux-operator, FluxInstance, FluxReport,
  ResourceSet, ResourceSetInputProvider, Flux CD operator management, or asks about
  GitOps CLI tooling for Kubernetes with Flux. Also trigger when users ask about
  building Flux manifests, diffing YAML, patching Flux instances, creating Flux secrets,
  tracing GitOps delivery pipelines, or bootstrapping clusters with Flux.
  Even if the user just says "flux operator" or "flux-operator cli" without details,
  this skill has the authoritative reference.
---

# Flux Operator CLI

## Installation

```bash
brew install controlplaneio-fluxcd/tap/flux-operator
```

Uses `~/.kube/config`. Supports offline (no cluster) and online commands.

## Command Overview

Commands fall into two categories: **offline** (no cluster access) and **online** (requires cluster).

### Offline Commands (no cluster needed)

| Command | Purpose |
|---------|---------|
| `build instance` | Generate K8s manifests from a FluxInstance YAML |
| `build rset` | Generate K8s manifests from a ResourceSet YAML |
| `diff yaml <source> <target>` | Compare YAML files, produce RFC 6902 JSON patch |
| `patch instance` | Generate kustomize patches for upgrading Flux controllers |

### Online Commands (cluster access required)

| Command | Purpose |
|---------|---------|
| `get instance\|rset\|rsip\|all` | List Flux Operator resources and their status |
| `export report` | Export FluxReport with distribution status |
| `export resource <kind>/<name>` | Export a Flux resource as YAML/JSON |
| `reconcile instance\|rset\|rsip\|resource\|all` | Trigger reconciliation |
| `suspend instance\|rset\|rsip\|resource` | Pause reconciliation |
| `resume instance\|rset\|rsip\|resource` | Resume reconciliation |
| `delete instance\|rset\|rsip` | Delete Flux resources |
| `stats` | Reconciliation statistics and storage usage |
| `trace <kind>/<name>` | Trace object through GitOps delivery pipeline |
| `tree rset\|ks\|hr` | Visualize managed objects as a tree |
| `wait instance\|rset\|rsip` | Poll until resource is ready |
| `create secret <type>` | Create Kubernetes secrets for Flux |
| `install` | Bootstrap cluster with Flux Operator + instance |
| `uninstall` | Remove Flux Operator from cluster |
| `version` | Show CLI, operator, and distribution versions |

## Common Patterns

### Build and preview manifests locally

```bash
# Build FluxInstance manifests
flux-operator build instance -f flux-instance.yaml

# Build ResourceSet with inputs
flux-operator build rset -f resourceset.yaml \
  --inputs-from inputs.yaml

# Diff two YAML files (local or remote URLs)
flux-operator diff yaml old.yaml new.yaml -o json-patch-yaml
```

### Day-2 cluster operations

```bash
# Check status of everything
flux-operator get all -A

# Filter by readiness
flux-operator get all --ready-status=False

# Reconcile a stuck resource
flux-operator reconcile resource Kustomization/my-app -n default --wait

# Reconcile everything
flux-operator reconcile all --wait

# Trace where an object comes from in the GitOps pipeline
flux-operator trace Deployment/my-app -n default

# View the object tree under a Kustomization
flux-operator tree ks my-app -n default
```

### Upgrade Flux controllers

```bash
# Generate upgrade patches for a target version
flux-operator patch instance -f flux-instance.yaml -v v2.5

# With a custom registry
flux-operator patch instance -f flux-instance.yaml -v v2.5 \
  -r my-registry.example.com/flux

# Verify controllers updated
flux-operator get instance -A
```

### Suspend and resume for maintenance

```bash
# Suspend before maintenance
flux-operator suspend instance flux -n flux-system

# Verify suspended
flux-operator get instance flux -n flux-system

# Resume after maintenance
flux-operator resume instance flux -n flux-system --wait
```

### Delete with safety

```bash
# Delete but keep managed resources in place
flux-operator delete instance flux -n flux-system --with-suspend

# Delete and wait for completion
flux-operator delete rset my-rset -n default --wait

# Verify deletion
flux-operator get all -n default
```

### Bootstrap a cluster

```bash
# Basic install
flux-operator install

# Verify install succeeded
flux-operator get all -A

# Install with Git sync
flux-operator install \
  --instance-sync-url=https://github.com/org/fleet \
  --instance-sync-ref=main \
  --instance-sync-path=clusters/production \
  --instance-sync-creds=username:ghp_token

# Install with cluster tuning
flux-operator install \
  --instance-cluster-type=aws \
  --instance-cluster-size=large \
  --instance-cluster-multitenant
```

### Create secrets for Flux

```bash
# Git SSH auth
flux-operator create secret ssh my-ssh-secret \
  --private-key-file=id_ed25519 \
  --knownhosts-file=known_hosts \
  -n flux-system

# Container registry auth
flux-operator create secret registry my-reg-secret \
  --server=ghcr.io \
  --username=bot \
  --password-stdin \
  -n flux-system

# SOPS age encryption
flux-operator create secret sops my-sops-secret \
  --age-key-file=age.key \
  -n flux-system

# Export as YAML instead of applying (for GitOps)
flux-operator create secret basic-auth my-auth \
  --username=admin --password=secret --export
```

### Uninstall

```bash
# Full removal
flux-operator -n flux-system uninstall

# Keep the namespace
flux-operator -n flux-system uninstall --keep-namespace

# Verify removal
flux-operator version
```

## References

- [references/commands-build-diff-patch.md](references/commands-build-diff-patch.md) - Build, diff, and patch commands
- [references/commands-cluster-ops.md](references/commands-cluster-ops.md) - Cluster operations (get, reconcile, suspend, resume, etc.)
- [references/commands-secrets.md](references/commands-secrets.md) - All create secret subcommands
- [references/commands-skills.md](references/commands-skills.md) - Skills management commands

## Abbreviations

| Short | Full Resource |
|-------|--------------|
| `rset` | ResourceSet |
| `rsip` | ResourceSetInputProvider |
| `ks` | Kustomization |
| `hr` | HelmRelease |

## Tips

- Use `--export` on `create secret` commands to generate YAML without applying — useful
  for GitOps workflows where secrets are managed declaratively.

- `trace` walks backward from any Kubernetes object to find which Flux reconciler
  manages it and where the source manifests live.

- `diff yaml` accepts remote URLs (GitHub, GitLab, Gist, OCI) in addition to local files.

- `patch instance` modifies the FluxInstance YAML in-place and replaces previously
  generated patches, so it's safe to run repeatedly.

- `install` is designed for dev/test environments. For production, use Helm charts.
