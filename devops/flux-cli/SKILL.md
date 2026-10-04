---
name: flux-cli
description: >
  Bootstraps Flux CD on Kubernetes clusters, creates and manages GitOps sources
  (Git/Helm/OCI/Bucket), configures kustomizations and Helm releases, reconciles
  resources, sets up image automation and alerting, and pushes OCI artifacts.
  Use this skill whenever the user mentions the flux CLI, flux bootstrap, flux create
  source, flux create kustomization, flux create helmrelease, flux reconcile, flux get,
  Flux CD, GitOps with Flux, or asks about managing Kubernetes deployments via GitOps.
  Also trigger when users ask about creating Git/Helm/OCI/Bucket sources, building
  or diffing kustomizations, pushing OCI artifacts, setting up image automation,
  creating Flux alerts/receivers, or bootstrapping Flux on GitHub/GitLab/Gitea/Bitbucket.
  Even if the user just says "flux" in a Kubernetes context, this skill applies.
---

# Flux CLI

## Installation

```bash
brew install fluxcd/tap/flux
# or: curl -s https://fluxcd.io/install.sh | sudo bash
```

Default namespace is `flux-system`. Uses `~/.kube/config`.

## Command Map

### Bootstrap — Initialize Flux on a cluster via GitOps

```bash
flux bootstrap github|gitlab|gitea|bitbucket-server|git|azure-devops

# Example
flux bootstrap github \
  --owner=my-org \
  --repository=fleet-infra \
  --branch=main \
  --path=clusters/production \
  --personal
```

### Sources — Where Flux pulls manifests and charts from

```bash
# Create sources
flux create source git <name> --url=<repo-url> --branch=<branch>
flux create source helm <name> --url=<chart-repo-url>
flux create source oci <name> --url=<oci-url>
flux create source bucket <name> --bucket-name=<name> --endpoint=<url>

# Query sources
flux get sources all|git|helm|oci|bucket|chart
flux export source git|helm|oci|bucket [name] [--all]
flux reconcile source git|helm|oci|bucket|chart <name>
flux suspend source git|helm|oci|bucket <name>
flux resume source git|helm|oci|bucket <name>
flux delete source git|helm|oci|bucket <name>
```

### Kustomizations — Deploy manifests from sources

```bash
# Create
flux create kustomization <name> \
  --source=GitRepository/<source-name> \
  --path=./path \
  --prune=true

# Build locally (preview what would be applied)
flux build kustomization <name> --path=./local/path

# Diff against cluster (exit 0=no diff, 1=has diff)
flux diff kustomization <name> --path=./local/path

# Manage
flux get kustomizations
flux reconcile kustomization <name>
flux suspend kustomization <name>
flux resume kustomization <name>
flux export kustomization <name>
flux delete kustomization <name>
```

### Helm Releases — Deploy Helm charts

```bash
# From a HelmRepository
flux create helmrelease <name> \
  --source=HelmRepository/<repo-name> \
  --chart=<chart-name> \
  --chart-version=">=1.0.0" \
  --values=./values.yaml

# From a GitRepository
flux create helmrelease <name> \
  --source=GitRepository/<repo-name> \
  --chart=./charts/my-chart

# Manage
flux get helmreleases
flux reconcile helmrelease <name>
flux suspend helmrelease <name>
flux resume helmrelease <name>
flux export helmrelease <name>
flux delete helmrelease <name>
flux debug helmrelease <name>
```

### Image Automation — Auto-update images

```bash
# Set up image scanning
flux create image repository <name> --image=<registry/image>
flux create image policy <name> \
  --image-ref=<repo-name> \
  --select-semver=">=1.0.0"

# Set up auto-update
flux create image update <name> \
  --git-repo-ref=<git-source> \
  --git-repo-path=./clusters \
  --checkout-branch=main \
  --push-branch=main \
  --author-name=flux \
  --author-email=flux@example.com

# Query
flux get images all|repository|policy|update
flux reconcile image repository|policy|update <name>
```

### Alerts & Receivers — Notifications

```bash
# Create an alert provider (Slack, Teams, GitHub, etc.)
flux create alert-provider <name> \
  --type=slack \
  --channel=general \
  --address=https://hooks.slack.com/...

# Create an alert
flux create alert <name> \
  --provider-ref=<provider-name> \
  --event-source="Kustomization/*"

# Webhook receivers (trigger reconciliation from external events)
flux create receiver <name> \
  --type=github \
  --event=push \
  --resource=GitRepository/<source-name> \
  --secret-ref=webhook-secret
```

### Secrets — Authentication for sources

```bash
flux create secret git <name> --url=<repo-url> --username=<u> --password=<p>
flux create secret helm <name> --username=<u> --password=<p>
flux create secret oci <name> --url=<registry> --username=<u> --password=<p>
flux create secret tls <name> --cert-file=cert.pem --key-file=key.pem
flux create secret proxy <name> --address=<proxy-url>
flux create secret githubapp <name> --app-id=<id> --app-installation-id=<id> \
  --app-private-key-file=key.pem
```

### OCI Artifacts — Push/pull manifests as OCI images

```bash
# Push local manifests to an OCI registry
flux push artifact oci://<registry>/<name>:<tag> \
  --path=./manifests \
  --source=https://github.com/org/repo \
  --revision=main@sha1:abc123

# Pull artifact locally
flux pull artifact oci://<registry>/<name>:<tag> --output=./output

# Tag, list, diff
flux tag artifact oci://<registry>/<name>:<tag> --tag=latest
flux list artifacts oci://<registry>/<name>
flux diff artifact oci://<registry>/<name>:<tag> --path=./local
```

### Diagnostics & Debugging

```bash
# View controller logs
flux logs [-f] [--level=error] [--kind=Kustomization] [--name=my-app] [-A]

# View events
flux events [--for=Kustomization/<name>] [-A]

# Trace an object through the GitOps pipeline
flux trace <kind> <name> [-n <namespace>]

# View resource tree under a Kustomization/HelmRelease
flux tree kustomization|helmrelease <name> [-n <namespace>]

# Reconciliation statistics
flux stats

# Check Flux prerequisites and installation
flux check
```

### Installation & Lifecycle

```bash
# Install Flux controllers (without bootstrap)
flux install [--components=source-controller,kustomize-controller,...]

# Uninstall Flux
flux uninstall

# Check installation health
flux check

# Version info
flux version
```

## Common Workflows

### Bootstrap + deploy an app

```bash
# 1. Bootstrap Flux on a cluster
flux bootstrap github --owner=my-org --repository=fleet --path=clusters/prod --personal

# 2. Verify bootstrap succeeded
flux check
flux get all

# 3. Create a source
flux create source git my-app \
  --url=https://github.com/my-org/my-app \
  --branch=main --interval=1m

# 4. Deploy via Kustomization
flux create kustomization my-app \
  --source=GitRepository/my-app \
  --path=./deploy --prune=true --interval=5m

# 5. Verify reconciliation
flux get kustomization my-app
```

### Deploy a Helm chart

```bash
# 1. Add the chart repo
flux create source helm bitnami \
  --url=https://charts.bitnami.com/bitnami --interval=1h

# 2. Create the release
flux create helmrelease nginx \
  --source=HelmRepository/bitnami \
  --chart=nginx \
  --chart-version=">=15.0.0" \
  --values=./nginx-values.yaml

# 3. Verify release is ready
flux get helmrelease nginx
```

### Preview changes before applying

```bash
# Build locally
flux build kustomization my-app --path=./deploy

# Diff against live cluster
flux diff kustomization my-app --path=./deploy
```

### Debug a failing reconciliation

```bash
# Check what's failing
flux get all -A --status-selector ready=false

# View logs for errors
flux logs --level=error -f

# Trace a specific object
flux trace deployment my-app -n default

# Debug a HelmRelease
flux debug helmrelease my-release -n default
```

### Export for backup / migration

```bash
# Export everything
flux export source git --all > sources.yaml
flux export kustomization --all > kustomizations.yaml
flux export helmrelease --all > helmreleases.yaml
```

### Maintenance window

```bash
# Suspend all kustomizations
flux suspend kustomization --all -n flux-system

# Do maintenance...

# Resume
flux resume kustomization --all -n flux-system
```

## References

- [references/bootstrap.md](references/bootstrap.md) - All `flux bootstrap` subcommands with provider-specific flags
- [references/sources.md](references/sources.md) - `flux create source git|helm|oci|bucket` with every flag
- [references/kustomizations.md](references/kustomizations.md) - Kustomization create, build, and diff commands
- [references/helmreleases.md](references/helmreleases.md) - `flux create helmrelease` with all flags
- [references/artifacts-and-images.md](references/artifacts-and-images.md) - OCI artifact and image automation commands

## Global Flags

All commands inherit standard Kubernetes flags:

| Flag | Default | Description |
|------|---------|-------------|
| `--kubeconfig` | `~/.kube/config` | Path to kubeconfig |
| `--context` | — | Kubeconfig context |
| `-n, --namespace` | `flux-system` | Namespace scope |
| `--timeout` | `5m` | Operation timeout |
| `--verbose` | — | Print generated objects |
| `--export` | — | Output YAML to stdout instead of applying |

## Tips

- `--export` on any `create` command generates YAML without applying — pipe to a file
  and commit to Git for true GitOps.
- `flux get all -A --status-selector ready=false` finds problems fast.
- `flux diff kustomization` exits with code 1 if there are differences — useful for
  CI pipeline gates.
- `flux reconcile` triggers an immediate sync instead of waiting for the interval.
- `flux trace` walks backward from any Kubernetes object to its Flux source.
