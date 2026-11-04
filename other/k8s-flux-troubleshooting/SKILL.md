---
name: k8s-flux-troubleshooting
description: >-
  Use when Flux does not deploy or update something in Kubernetes: a GitRepository,
  OCIRepository or HelmRepository that is not Ready ("couldn't find remote ref",
  "authentication required"), a Kustomization that is not Ready ("kustomization path not
  found", "kustomize build failed", "dependency ... is not ready", health check
  timeouts), a HelmRelease that is not Ready (HelmChart "invalid chart reference",
  InstallFailed, UpgradeFailed, RetriesExceeded), changes in Git that never reach the
  cluster, or suspended Flux objects. Investigates with kubectl get, describe, events and
  logs, and proposes fixes. Reads first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, flux 2.9"
  verified-on: "2026-10-24"
---

# Flux troubleshooting

Find out why Flux does not deploy or update a workload, and propose a fix. **Read first,
ask before changing.** Run the investigation commands freely. Run a command under an
"Ask first" line only after the user approves that exact command; if your credentials do
not allow it, give it to the user to run. Never run a "Proposed fix"; hand it to the user.

Flux works in a chain. A **source** (GitRepository, OCIRepository, HelmRepository,
Bucket) fetches an artifact. A **Kustomization** builds and applies a path from that
artifact; a **HelmRelease** installs a chart, through a **HelmChart** that Flux creates
from the HelmRelease. Every object reports `Ready`, and the first object in the chain
that is not Ready holds the cause. Follow the chain from the object that deploys the
workload back to its source.

The commands use placeholders: `flux-system` (where Flux and most of its objects live),
`my-app` (the Kustomization or HelmRelease, and its source), and `my-namespace` (where
the workload runs). Replace them with the real names; Flux objects can live in any
namespace.

Never read Secrets: not Git or registry credentials, not SOPS keys, not values or
`postBuild` substitutions from Secrets, not Helm release Secrets. The status of the
Flux objects says when credentials are missing or wrong. For the same reason do not use
`flux tree`, `flux diff` or `flux debug ... --show-values` / `--show-vars`: they read
Secrets.

## When to use

- A change pushed to Git, an OCI registry or a Helm repository never reaches the
  cluster.
- `kubectl get kustomizations,helmreleases -A` shows `READY False` or `Unknown`.
- A GitRepository, OCIRepository, HelmRepository or HelmChart is not Ready.
- Objects are `SUSPENDED`, or a HelmRelease is Stalled after failed installs or
  upgrades.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- Flux applied the workload, but its pods fail (crash, image, probe, Pending):
  `k8s-workload-troubleshooting`.
- A HelmRelease's install or upgrade fails inside Helm (hooks, ownership, immutable
  fields): read [references/helmreleases.md](references/helmreleases.md) first; for the
  Helm side, `k8s-helm-troubleshooting`.
- The Flux controllers themselves crash or stay Pending: `k8s-workload-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. List the Flux objects and their state.** `READY`, `STATUS` (the Ready message) and
`SUSPENDED` are the columns that matter.

```bash
kubectl get kustomizations,helmreleases -A
kubectl get gitrepositories,ocirepositories,helmrepositories,helmcharts,buckets -A
```

**2. Read the object that deploys the workload**: its conditions, the source it points
at, and its events.

```bash
kubectl describe kustomization my-app -n flux-system
kubectl get kustomization my-app -n flux-system -o jsonpath='{.spec.sourceRef}{"\n"}{.spec.path}{"\n"}{.spec.suspend}{"\n"}{.status.conditions}{"\n"}'
kubectl describe helmrelease my-app -n flux-system
kubectl events -n flux-system --for kustomization/my-app
```

**3. Read its source.** A Kustomization's `sourceRef`, or the HelmChart a HelmRelease
uses (named `<namespace>-<name>`, in the HelmRelease's namespace) and its
HelmRepository or OCIRepository.

```bash
kubectl describe gitrepository my-app -n flux-system
kubectl get gitrepository my-app -n flux-system -o jsonpath='{.spec.url}{"\n"}{.spec.ref}{"\n"}{.status.artifact.revision}{"\n"}{.status.conditions}{"\n"}'
kubectl describe helmchart flux-system-my-app -n flux-system
kubectl describe helmrepository -n flux-system
```

**4. If the objects look right but nothing happens, check the controllers.** Their logs
name each object they reconcile.

```bash
kubectl get deployments -n flux-system
kubectl logs -n flux-system deployment/source-controller --tail=100 | grep my-app
kubectl logs -n flux-system deployment/kustomize-controller --tail=100 | grep my-app
kubectl logs -n flux-system deployment/helm-controller --tail=100 | grep my-app
```

If the `flux` CLI is installed, `flux get all -A` and `flux events -n flux-system` show
the same state in one view; they are optional, kubectl is enough.

**5. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| A GitRepository, OCIRepository, HelmRepository or HelmChart not Ready; `couldn't find remote ref`, `authentication required`, `invalid chart reference` | [references/sources.md](references/sources.md) |
| A Kustomization not Ready: `kustomization path not found`, `kustomize build failed`, `dependency ... is not ready`, health check timeout, `Source artifact not found` | [references/kustomizations.md](references/kustomizations.md) |
| A HelmRelease not Ready: `SourceNotReady`, `InstallFailed`, `UpgradeFailed`, `RetriesExceeded`, drift | [references/helmreleases.md](references/helmreleases.md) |
| Nothing happens at all, `SUSPENDED True`, objects on removed `v1beta` APIs, controllers down | [references/suspend-and-controllers.md](references/suspend-and-controllers.md) |

## Read the results

What the common findings mean (Flux 2.9):

- **A Kustomization with `Source artifact not found, retrying in 30s`** (reason
  `ArtifactFailed`): its source has no artifact yet. The cause is on the source; read it.
- **A GitRepository with `failed to checkout and determine revision: unable to clone
  '<url>': couldn't find remote ref "refs/heads/<branch>"`** (reason
  `GitOperationFailed`, `FetchFailed` `True`): the branch in `spec.ref` does not exist.
  `authentication required` or `repository not found` mean credentials or the URL.
- **`kustomization path not found: stat ...`** (reason `ArtifactFailed`): the source is
  fine, but `spec.path` names a folder the artifact does not have.
- **`kustomize build failed: ...`** (reason `BuildFailed`): the folder exists, but
  kustomize cannot build it; the message says why.
- **A HelmRelease with `HelmChart '<ns>/<name>' is not ready: ...`** (reason
  `SourceNotReady`): read the HelmChart. `invalid chart reference: ... no '<chart>' chart
  with version matching '<version>' found` (reason `InvalidChartReference`, `Stalled`
  `True`) means the repository has no such version; Flux will not retry until the spec
  changes.
- **`Stalled` `True` with `RetriesExceeded`** on a HelmRelease: install or upgrade
  failed and the retries are used up (install retries default to 0). Flux waits for a
  spec change or a reset.
- **`SUSPENDED True`**: Flux skips the object; its conditions are from the last run
  before it was suspended and can be stale.
- **A source that is Ready, with the new commit in `status.artifact.revision`, but
  the cluster unchanged**: look at the Kustomization or HelmRelease that uses it, and
  its `lastAppliedRevision`.

State the cause in one sentence, then the evidence you saw (the condition reason and
message, the spec field, the revision), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Asking Flux to reconcile now, resuming a suspended object and patching a Flux object's
spec are reversible, so they go under "Ask first" and run only after the user says yes.
Deleting Flux objects or the workloads they manage, changing credentials, and
reinstalling Flux are never run by you: hand them to the user as proposed fixes.

The fix almost always belongs in Git. Flux objects are themselves usually applied by a
parent Kustomization (often `flux-system`), which puts back the version in Git at its
next run; a patch on the live object is then only a test. Say so, and propose the
change in the repository. Write each undo with the values you found.

Point a Kustomization at the right folder, to test before fixing Git:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch kustomization my-app -n flux-system --type=merge -p '{"spec": {"path": "./kustomize"}}'
# Undo: kubectl patch kustomization my-app -n flux-system --type=merge -p '{"spec": {"path": "./kustomize/overlays/production"}}'
```

Ask Flux to reconcile an object now instead of waiting for its interval (use the
current time as the value; any new value triggers a run):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl annotate --overwrite gitrepository my-app -n flux-system reconcile.fluxcd.io/requestedAt=2026-10-24T12:00:00Z
# Undo: nothing to undo; the annotation only asks for one reconciliation
```

Resume an object that was suspended (only once the reason for suspending it is gone):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch kustomization my-app -n flux-system --type=merge -p '{"spec": {"suspend": false}}'
# Undo: kubectl patch kustomization my-app -n flux-system --type=merge -p '{"spec": {"suspend": true}}'
```

## Sources

Checked against the Flux 2.9 documentation and the controllers' source (flux2 v2.9.6,
source-controller and kustomize-controller v1.9.6, helm-controller v1.6.5):

- [Troubleshooting cheatsheet](https://fluxcd.io/flux/cheatsheets/troubleshooting/).
- [GitRepositories](https://fluxcd.io/flux/components/source/gitrepositories/),
  [HelmCharts](https://fluxcd.io/flux/components/source/helmcharts/),
  [Kustomizations](https://fluxcd.io/flux/components/kustomize/kustomizations/) and
  [HelmReleases](https://fluxcd.io/flux/components/helm/helmreleases/): specs,
  conditions and reasons.
- [flux reconcile](https://fluxcd.io/flux/cmd/flux_reconcile/) and
  [flux suspend](https://fluxcd.io/flux/cmd/flux_suspend/): the annotation and the
  `spec.suspend` field they set.
- [flux debug](https://fluxcd.io/flux/cmd/flux_debug/): it can print values from
  Secrets, which is why this skill does not use it.
- [Events](https://fluxcd.io/flux/monitoring/events/) and
  [Security](https://fluxcd.io/flux/security/): the aggregated `flux-view` role.
- [flux2 v2.7.0](https://github.com/fluxcd/flux2/releases/tag/v2.7.0),
  [v2.8.0](https://github.com/fluxcd/flux2/releases/tag/v2.8.0) and
  [v2.9.0](https://github.com/fluxcd/flux2/releases/tag/v2.9.0) release notes: removed
  beta APIs.
- Condition messages from the source:
  [gitrepository_controller.go](https://github.com/fluxcd/source-controller/blob/v1.9.6/internal/controller/gitrepository_controller.go),
  [kustomization_controller.go](https://github.com/fluxcd/kustomize-controller/blob/v1.9.6/internal/controller/kustomization_controller.go),
  [helmrelease_controller.go](https://github.com/fluxcd/helm-controller/blob/v1.6.5/internal/controller/helmrelease_controller.go).
  The messages quoted here were also seen on a Kubernetes 1.37 kind cluster with Flux
  2.9.6. Flux 2.9 lists Kubernetes 1.34 to 1.36 as supported; 1.37 is not on that list
  yet.
