---
name: k8s-helm-troubleshooting
description: >-
  Use when a Helm install, upgrade or rollback fails or a release is stuck: "UPGRADE
  FAILED" or "INSTALLATION FAILED", "context deadline exceeded" or "resource ... not
  ready" after --wait, "another operation (install/upgrade/rollback) is in progress",
  a release in pending-install, pending-upgrade or failed state, "exists and cannot be
  imported into the current release: invalid ownership metadata", "cannot reuse a name
  that is still in use", "has no deployed releases", hook failures, "field is
  immutable", or "ensure CRDs are installed first". Investigates the release's objects
  with kubectl, gives helm commands to the user to run, and proposes fixes. Reads first
  and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, helm 4.3"
  verified-on: "2026-10-24"
---

# Helm troubleshooting

Find out why a Helm release fails or is stuck, and propose a fix. **Read first, ask
before changing.** Run the investigation commands freely. Run a command under an "Ask
first" line only after the user approves that exact command; if your credentials do not
allow it, give it to the user to run. Never run a "Proposed fix"; hand it to the user.

**Helm keeps every release in a Secret** (type `helm.sh/release.v1`, named
`sh.helm.release.v1.<release>.v<revision>`), with its values, which often hold
passwords. `helm status`, `helm history`, `helm list` and `helm get` all read those
Secrets, and you never read Secrets. So you investigate the release's **objects** with
kubectl, and you give the `helm` commands to the user to run and paste back. They are
under "Proposed fix" only because they read Secrets, not because they change anything;
say so when you hand them over. Never ask for `helm get values` output without warning
that values can contain passwords the user should remove first.

The commands use placeholders: `my-app` (the release), `my-namespace` (its namespace)
and `my-app-podinfo` (an object of the release). Replace them with the real names.

## When to use

- `helm install`, `helm upgrade` or `helm rollback` fails, from a terminal or a CI
  job.
- A release is `failed`, `pending-install`, `pending-upgrade` or `pending-rollback`.
- The app broke right after a Helm upgrade.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The release's pods fail (crash, image, probe, Pending): `k8s-workload-troubleshooting`;
  a Helm `--wait` timeout is usually this.
- Flux manages the release (a HelmRelease): `k8s-flux-troubleshooting`. Argo CD
  renders Helm charts itself and does not create Helm releases:
  `k8s-argocd-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. Get the exact error** from the user: the full output of the failed `helm` command
(or the CI log), and the Helm version (`helm version`). Helm 3 and Helm 4 word some
errors differently.

**2. Find the release's objects.** Helm marks everything it manages with the label
`app.kubernetes.io/managed-by=Helm` and the annotations `meta.helm.sh/release-name` and
`meta.helm.sh/release-namespace`. kubectl cannot select on annotations, so list the
objects with their annotations and read the release name there:

```bash
kubectl get deployments,statefulsets,daemonsets,services,configmaps,ingresses,jobs -n my-namespace -l app.kubernetes.io/managed-by=Helm -o jsonpath='{range .items[*]}{.kind}{" "}{.metadata.name}{" "}{.metadata.annotations}{"\n"}{end}'
kubectl get all -n my-namespace -l app.kubernetes.io/instance=my-app
```

The second command works when the chart follows the common labelling convention.

**3. Look at the objects the error names**, and at what changed: the newest
ReplicaSet, pods that are not Ready, events.

```bash
kubectl get pods -n my-namespace -o wide
kubectl describe deployment my-app-podinfo -n my-namespace
kubectl rollout history deployment/my-app-podinfo -n my-namespace
kubectl events -n my-namespace
```

**4. For an ownership or "already exists" error, read the object's labels and
annotations**: do they say Helm, and which release?

```bash
kubectl get service my-app-podinfo -n my-namespace -o jsonpath='{.metadata.labels}{"\n"}{.metadata.annotations}{"\n"}{.metadata.managedFields[*].manager}{"\n"}'
```

**5. Ask the user to run the release commands** you need, and to paste the output.
They only read, but they read the release Secrets, which you do not:

> Proposed fix: review before running. The agent does not run this.

```bash
helm status my-app -n my-namespace
helm history my-app -n my-namespace
helm list -n my-namespace
# Undo: nothing to undo, these only read (they are for the user because Helm reads its release records)
```

On Helm 3, `helm list` needs `--all` to show pending releases; Helm 4 shows every
status by default.

**6. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| `UPGRADE FAILED` with `context deadline exceeded` or `not ready`, hook failures, `field is immutable`, `has no deployed releases`, the app broken after an upgrade | [references/failed-upgrades.md](references/failed-upgrades.md) |
| `INSTALLATION FAILED`: `exists and cannot be imported`, `cannot reuse a name`, `ensure CRDs are installed first`, removed APIs | [references/install-errors.md](references/install-errors.md) |
| `another operation (install/upgrade/rollback) is in progress`, a release `pending-*` | [references/stuck-releases.md](references/stuck-releases.md) |

## Read the results

What the common findings mean (Helm 4.3; Helm 3.22 where it differs):

- **`resource <Kind>/<ns>/<name> not ready. status: InProgress ... context deadline
  exceeded`** after `--wait`: Helm applied the change, and the objects did not become
  ready before `--timeout`. The cause is in those objects (an image that cannot be
  pulled, a crash, a probe). The release is marked `failed`; the cluster keeps what
  was applied.
- **`another operation (install/upgrade/rollback) is in progress`**: the last revision
  is `pending-*`. Usually the earlier `helm` process was killed (a cancelled CI job, a
  lost terminal) before it could record the result. It does not clear by itself.
- **`<Kind> "<name>" in namespace "<ns>" exists and cannot be imported into the current
  release: invalid ownership metadata`**: an object of that name exists and does not
  carry this release's label and annotations. It was created by hand, by another
  release, or by another tool.
- **`cannot reuse a name that is still in use`** (Helm 3: `cannot re-use`): a release
  of that name exists, perhaps `failed` or `pending-install`.
- **`"<release>" has no deployed releases`**: every revision so far failed; there is
  nothing to upgrade from.
- **`cannot patch "<name>" with kind <Kind>: ... field is immutable`**: the chart
  changed a field Kubernetes does not allow to change (a Deployment's selector, a
  Service's `clusterIP`, a Job's template).

State the cause in one sentence, then the evidence you saw (the error, the object, its
labels or status), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Adding Helm's ownership label and annotations to an object (so a release may adopt it)
is reversible, so it goes under "Ask first" and runs only after the user says yes.
Every `helm` command is for the user, because Helm reads and writes release Secrets:
rollbacks, upgrades, installs and uninstalls are proposed fixes. Deleting objects is a
proposed fix too. Prefer fixing the chart or values in their source. Write each undo
with the values you found.

Let release my-app adopt an object created by hand (only when it should belong to the
release; the next install or upgrade then manages it):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl label service my-app-podinfo -n my-namespace app.kubernetes.io/managed-by=Helm
kubectl annotate service my-app-podinfo -n my-namespace meta.helm.sh/release-name=my-app meta.helm.sh/release-namespace=my-namespace
# Undo: kubectl label service my-app-podinfo -n my-namespace app.kubernetes.io/managed-by- && kubectl annotate service my-app-podinfo -n my-namespace meta.helm.sh/release-name- meta.helm.sh/release-namespace-
```

Roll back to the last revision that worked (`helm history` shows it as `deployed` or
`superseded`):

> Proposed fix: review before running. The agent does not run this.

```bash
helm rollback my-app 1 -n my-namespace --wait --timeout 5m
# Undo: helm rollback my-app <the revision before this rollback> -n my-namespace
```

## Sources

Checked against the Helm 4.3 documentation and source (v4.3.1, and v3.22.1 for Helm 3
wording):

- [Helm 4 overview](https://helm.sh/docs/overview): server-side apply, `--wait`
  strategies, `--rollback-on-failure`, `helm list` showing every status.
- [Troubleshooting](https://helm.sh/docs/v3/faq/troubleshooting) (Helm 3).
- [helm rollback](https://helm.sh/docs/helm/helm_rollback),
  [helm status](https://helm.sh/docs/helm/helm_status) and
  [helm history](https://helm.sh/docs/helm/helm_history).
- [Chart hooks](https://helm.sh/docs/topics/charts_hooks),
  [deprecated Kubernetes APIs](https://helm.sh/docs/topics/kubernetes_apis) and
  [labels and annotations](https://helm.sh/docs/chart_best_practices/labels).
- Error strings and ownership checks from the source:
  [action.go](https://github.com/helm/helm/blob/v4.3.1/pkg/action/action.go),
  [install.go](https://github.com/helm/helm/blob/v4.3.1/pkg/action/install.go),
  [validate.go](https://github.com/helm/helm/blob/v4.3.1/pkg/action/validate.go),
  [statuswait.go](https://github.com/helm/helm/blob/v4.3.1/pkg/kube/statuswait.go),
  [secrets.go](https://github.com/helm/helm/blob/v4.3.1/pkg/storage/driver/secrets.go).
  The messages quoted here were also seen with Helm 4.3.0 on a Kubernetes 1.37 kind
  cluster.
