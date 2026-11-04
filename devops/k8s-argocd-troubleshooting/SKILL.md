---
name: k8s-argocd-troubleshooting
description: >-
  Use when Argo CD does not deploy or update an application in Kubernetes: an
  Application that is OutOfSync, Unknown, Degraded, Missing or Progressing, a
  ComparisonError ("app path does not exist", "unable to resolve ... to a commit SHA"),
  an InvalidSpecError ("do not match any of the allowed destinations in project"), a
  sync that fails ("one or more objects failed to apply"), auto-sync that never runs,
  resources that stay OutOfSync after a sync, or ApplicationSets that generate nothing.
  Investigates with kubectl get, describe, events and logs, and proposes fixes. Reads
  first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, argo-cd 3.5"
  verified-on: "2026-10-24"
---

# Argo CD troubleshooting

Find out why Argo CD does not deploy or update an application, and propose a fix.
**Read first, ask before changing.** Run the investigation commands freely. Run a
command under an "Ask first" line only after the user approves that exact command; if
your credentials do not allow it, give it to the user to run. Never run a "Proposed
fix"; hand it to the user.

An **Application** says: render this path of this repository at this revision, and
apply it to this destination. Argo CD compares the rendered manifests with the cluster
and reports two things: **sync status** (does the cluster match Git: `Synced`,
`OutOfSync`, `Unknown`) and **health** (do the deployed objects work: `Healthy`,
`Progressing`, `Degraded`, `Missing`, `Suspended`). Conditions on the Application say
why it could not compare or sync. An **AppProject** limits which repositories,
destinations and kinds an Application may use.

The commands use placeholders: `argocd` (where Argo CD and its Applications live, the
default), `my-app` (the Application) and `my-namespace` (where it deploys). Replace them
with the real names.

Never read Secrets. Argo CD keeps repository credentials, cluster credentials and its
own settings in Secrets (`argocd-secret`, and Secrets labelled
`argocd.argoproj.io/secret-type`). Read the ConfigMaps instead (`argocd-cm`,
`argocd-rbac-cm`, `argocd-cmd-params-cm`); the Application's conditions say when a
credential is missing or wrong.

## When to use

- An Application shows `OutOfSync`, `Unknown`, `Degraded`, `Missing` or `Progressing`
  for longer than expected.
- A change merged to Git never reaches the cluster.
- A sync fails, or resources go `OutOfSync` again right after a sync.
- An ApplicationSet creates no Applications, or the wrong ones.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- Argo CD synced, but the deployed pods fail (health `Degraded` or `Progressing` because
  of crashes, images, probes, Pending): `k8s-workload-troubleshooting`.
- The Argo CD components themselves crash or stay Pending:
  `k8s-workload-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. List the Applications** with their sync and health status. The built-in `view`
role cannot read Applications (Argo CD adds nothing to it); if the command is
forbidden, say so and ask the user for the Application's status from the Argo CD UI or
CLI.

```bash
kubectl get applications -n argocd
```

**2. Read the Application**: its source, destination, project, sync policy, conditions
and the last sync operation.

```bash
kubectl describe application my-app -n argocd
kubectl get application my-app -n argocd -o jsonpath='{.spec.source}{"\n"}{.spec.destination}{"\n"}{.spec.project}{"\n"}{.spec.syncPolicy}{"\n"}'
kubectl get application my-app -n argocd -o jsonpath='{.status.conditions}{"\n"}{.status.sync}{"\n"}{.status.health}{"\n"}'
kubectl get application my-app -n argocd -o jsonpath='{.status.operationState.phase}{" "}{.status.operationState.message}{"\n"}'
```

**3. See which resources differ.** Each entry of `status.resources` has a sync status;
the failed ones of the last sync have a message.

```bash
kubectl get application my-app -n argocd -o jsonpath='{range .status.resources[*]}{.kind}{" "}{.namespace}{"/"}{.name}{" "}{.status}{"\n"}{end}'
kubectl get application my-app -n argocd -o jsonpath='{range .status.operationState.syncResult.resources[*]}{.kind}{" "}{.name}{" "}{.status}{" "}{.message}{"\n"}{end}'
```

**4. Read the AppProject** the Application uses: allowed source repositories,
destinations and resource kinds.

```bash
kubectl get appprojects -n argocd
kubectl get appproject default -n argocd -o jsonpath='{.spec.sourceRepos}{"\n"}{.spec.destinations}{"\n"}{.spec.clusterResourceWhitelist}{"\n"}'
```

**5. If the conditions do not explain it, read the components.** The repo-server
renders manifests (Git and Helm errors), the application controller compares and syncs.

```bash
kubectl get pods -n argocd
kubectl logs -n argocd deployment/argocd-repo-server --tail=100 | grep my-app
kubectl logs -n argocd statefulset/argocd-application-controller --tail=200 | grep my-app
kubectl events -n argocd --for application/my-app
```

**6. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| `ComparisonError`, `Unknown` sync status: `app path does not exist`, `unable to resolve ... to a commit SHA`, Helm or Kustomize errors, repository access | [references/comparison-errors.md](references/comparison-errors.md) |
| `InvalidSpecError`: destinations or repositories not permitted in the project, cluster not found | [references/projects-and-destinations.md](references/projects-and-destinations.md) |
| `OutOfSync` that never syncs, a failed sync, `OutOfSync` again after a sync, auto-sync skipped | [references/sync.md](references/sync.md) |
| `Degraded`, `Progressing`, `Missing` health; ApplicationSets that generate nothing | [references/health-and-appsets.md](references/health-and-appsets.md) |

## Read the results

What the common findings mean (Argo CD 3.5):

- **Sync `Unknown` with a `ComparisonError`** `Failed to load target state: failed to
  generate manifest for source 1 of 1: ...`: Argo CD could not render the manifests.
  The text at the end says why: `<path>: app path does not exist` (wrong `path`),
  `unable to resolve '<rev>' to a commit SHA` (wrong `targetRevision`), a Helm or
  Kustomize error, or repository access.
- **An `InvalidSpecError`** `application destination server '<server>' and namespace
  '<ns>' do not match any of the allowed destinations in project '<project>'`: the
  AppProject does not allow that destination. Either the Application targets the wrong
  namespace or the project is missing a destination.
- **`OutOfSync` and `Missing`, no error, and no sync ever ran**: the Application has no
  `spec.syncPolicy.automated`, so Argo CD only reports the difference and waits for
  someone to sync. This is not a fault, but often not what the user expects.
- **A sync `Failed` with `one or more objects failed to apply, reason: ...`**: the API
  server refused an object; the per-resource message in `syncResult` is the API error.
- **`OutOfSync` again right after a successful sync**: something in the cluster
  changes the objects after Argo CD applies them (a mutating webhook, an operator, an
  HPA on `replicas`), or the manifest has defaults the API server fills in differently.
- **Health `Degraded` or `Progressing`** with sync `Synced`: Argo CD did its part; the
  deployed workload is not healthy.

State the cause in one sentence, then the evidence you saw (the condition and its
message, the spec field, the project rule), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Asking Argo CD to refresh, starting one sync and patching an Application's spec are
reversible, so they go under "Ask first" and run only after the user says yes.
Changing AppProjects, repository or cluster credentials, syncing with prune or replace,
and deleting Applications are never run by you: hand them to the user as proposed
fixes. Applications are often themselves managed from Git (app-of-apps, ApplicationSets,
or a GitOps repository for Argo CD); a patch on the live Application is then reverted,
so propose the change in Git. Write each undo with the values you found.

Point an Application at the right path (to test before fixing Git; the undo puts back the
value you found in step 2):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch application my-app -n argocd --type=merge -p '{"spec": {"source": {"path": "guestbook"}}}'
# Undo: kubectl patch application my-app -n argocd --type=merge -p '{"spec": {"source": {"path": "guestbook-ui"}}}'
```

Ask Argo CD to compare again now, for example after fixing the repository (the
controller removes the annotation when it is done):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl annotate application my-app -n argocd argocd.argoproj.io/refresh=normal --overwrite
# Undo: nothing to undo; the annotation only asks for one refresh
```

Sync once, without prune, when the user wants the current Git revision deployed and
the Application has no automated sync (`initiatedBy` records who asked):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch application my-app -n argocd --type=merge -p '{"operation": {"initiatedBy": {"username": "my-user"}, "sync": {"revision": "master"}}}'
# Undo: sync the revision of the previous entry in status.history the same way; objects this sync created stay until removed with prune, which is for the user
```

Turning on automated sync is a change to how the Application behaves from then on;
propose it in the source, with the user deciding on `prune` and `selfHeal`.

## Sources

Checked against the Argo CD 3.5 documentation and source (v3.5.6):

- [Troubleshooting](https://argo-cd.readthedocs.io/en/stable/operator-manual/troubleshooting/)
  and the [FAQ](https://argo-cd.readthedocs.io/en/stable/faq/).
- [Sync with kubectl](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-kubectl/)
  and [annotations and labels](https://argo-cd.readthedocs.io/en/stable/user-guide/annotations-and-labels/):
  the `operation` field and the refresh annotation.
- [Diffing customization](https://argo-cd.readthedocs.io/en/stable/user-guide/diffing/)
  and [resource tracking](https://argo-cd.readthedocs.io/en/stable/user-guide/resource_tracking/).
- [Projects](https://argo-cd.readthedocs.io/en/stable/user-guide/projects/) and
  [automated sync](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/).
- [Installation](https://argo-cd.readthedocs.io/en/stable/getting_started/) and the
  [upgrade notes](https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/overview/)
  for 3.x.
- Status types and messages from the source:
  [types.go](https://github.com/argoproj/argo-cd/blob/v3.5.6/pkg/apis/application/v1alpha1/types.go),
  [path.go](https://github.com/argoproj/argo-cd/blob/v3.5.6/util/app/path/path.go),
  [argo.go](https://github.com/argoproj/argo-cd/blob/v3.5.6/util/argo/argo.go),
  [appcontroller.go](https://github.com/argoproj/argo-cd/blob/v3.5.6/controller/appcontroller.go).
  The messages quoted here were also seen on a Kubernetes 1.37 kind cluster with Argo
  CD 3.5.6.
