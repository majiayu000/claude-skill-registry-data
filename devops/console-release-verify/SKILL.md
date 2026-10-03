---
name: console-release-verify
description: Check whether a merged console change is actually live — the GHCR image, the argocd-image-updater write-back into ai-helm-values, the aii-console-ui Application on the home-remote cluster, the chart version range pin, and the live build-stamp probes. Use whenever someone asks "is it deployed?", "is it live?", why a change is not showing in production, or mentions ArgoCD, image-updater, home-remote or a chart version.
---

# Is it live?

**"Image built" is not "live."** This repo's CI publishes to GHCR and stops. Four hops stand between
a merge and a running pod. Full chain and its diagrams: `docs/knowledge/release-and-rollout.md`.

Check in order and **stop at the first hop that is behind** — everything downstream will be too.

## 1. Did the image publish?

```sh
zsh -i -c 'gh api /orgs/adorsys-gis/packages/container/converse-frontends%2Fconsole/versions \
  --jq ".[0].metadata.container.tags"'
```

Expect `sha-<gitsha>` for the merge commit, plus `latest`. If it is missing, the failure is
`docker-image.yml` — check the run, not the cluster.

## 2. Did image-updater write it back?

```sh
zsh -i -c 'gh api /repos/adorsys-gis/ai-helm-values/commits \
  --jq ".[0:5] | .[] | .commit.message" -f path=environments/prod/values/console-ui.yaml'
```

Only tags matching `^sha-[0-9a-f]+$` are eligible; `latest` is **never** rolled. If the image exists
but no commit followed, the problem is the image-updater annotations in `ai-helm`'s
`charts/apps/values.yaml`, or its GHCR/git credentials.

## 3. What is ArgoCD actually serving?

**Point `kubectl` at the cluster ArgoCD runs on, not at `home-remote`.** ai-helm ADR-0017's
two-tier model puts the **Application CR** in the `argocd` namespace of the ArgoCD cluster and the
**workload** on `home-remote` in namespace `converse`. Querying the Application on `home-remote`
returns "not found" and reads as "not deployed".

```sh
kubectl -n argocd get application aii-console-ui \
  -o jsonpath='{.status.summary.images}{"\n"}'

kubectl -n argocd get application aii-console-ui \
  -o jsonpath='{.status.sync.status} {.status.health.status}{"\n"}'
```

`.status.summary.images` is the authoritative answer to "which image is running". Compare its
`sha-` suffix to the merge commit.

If the tag in `ai-helm-values` is newer than `.status.summary.images`, look at the **conditions**,
not the health status:

```sh
kubectl -n argocd get application aii-console-ui \
  -o jsonpath='{.status.conditions}{"\n"}'
```

### The chart-version range trap

The Application pins `targetRevision: "~0.2.4"` (`>=0.2.4 <0.3.0`) against
`oci://ghcr.io/adorsys-gis/charts/converse-console`. The published version is
`<major.minor from Chart.yaml>.<count of commits touching charts/converse-console>` — the patch is
**derived** by `publish-charts-oci.yml` and never written back.

So a **minor** bump in `charts/converse-console/Chart.yaml` publishes `0.3.0`, which that range does
not resolve. **ArgoCD then keeps serving the last version it can resolve while values written for
the new chart are already merged** — a green Application that is quietly a release behind. That is a
real incident this estate had on 2026-09-02.

Fix: widen the pin in `ai-helm` and merge that **before** any values that depend on the new chart.

## 4. What does the running process say about itself?

| Probe                         | Auth        | Reports                                                   |
| ----------------------------- | ----------- | --------------------------------------------------------- |
| `GET /robots.txt`             | none        | The pod is serving — this is what the kubelet probes      |
| `GET /api/build-info`         | **session** | The build stamps of `authz-idp` and `authz-usage`         |
| `/settings/info` in a browser | session     | The console's own Image and Reference rows, plus backends |

`/api/build-info` is session-gated on purpose — not because a version string is sensitive, but
because it makes the console fan out to internal origins on the caller's behalf. It answers `200`
even when both backend reads fail, with a per-service `error`/`unavailable` status, and
`Cache-Control: no-store`.

`/settings/info`'s **Image** row is `IMAGE_TAG` (the tag alone); the copyable **Reference** row is
`IMAGE_REF` (the full `ghcr.io/...@tag`). They are separate fields — see
`docs/knowledge/observability.md`.

## Rolling back

The tag lives in `ai-helm-values`, so a rollback is a commit there or an ArgoCD history rollback.
`kubectl rollout undo` works and is then reverted by the next sync — GitOps wins. See
`docs/knowledge/runbooks.md`.

## Pitfalls

- **A green, Synced, Healthy Application can still be a release behind** — that is the range trap
  above. Health is about the pods, not about which chart resolved.
- **`latest` is not rolled**, so "the image exists" plus "nothing deployed" is normal until a `sha-`
  tag lands.
- **The console image package is `converse-frontends/console`**, distinct from
  `converse-frontends` (the older self-service image). Checking the wrong package reads as "not
  published".
- **Two clusters.** The Application CR is on the cluster ArgoCD runs on, namespace `argocd`; the
  pods are on `home-remote`, namespace `converse`. Pointing at the wrong one returns "not found"
  and reads as "not deployed".
- **Do not report "deployed" from a CI green tick.** Read `.status.summary.images`.
