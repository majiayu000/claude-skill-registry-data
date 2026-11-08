---
name: k8s-podspec-pro
description: Writes and reviews Kubernetes pod specs against Bret Fisher's production floor (github.com/BretFisher/podspec) for security context, user namespaces, service account tokens, probes, resources, and graceful shutdown. Use it when the user creates or edits a Deployment, StatefulSet, DaemonSet, Job, CronJob, or Pod, changes a Helm chart or Kustomize base that renders one, asks to review or harden a workload for production, or asks why a pod spec setting matters, even if they only say "deploy this to Kubernetes".
license: MIT
compatibility: scripts/floor-check.py needs Python 3 and yq.
---

# Kubernetes pod spec floor

Every pod template you write or review meets the **floor**: the settings in [pod.yaml](references/pod.yaml),
an exact copy of <https://github.com/BretFisher/podspec/blob/main/pod.yaml>. Read pod.yaml at the start of
each task. Its field layout and its inline comments are the shape you copy, and the table below is the
summary with the exceptions.

## Working style

1. Find the pod template. Deployment, StatefulSet, DaemonSet, ReplicaSet, and Job: `spec.template.spec`.
   CronJob: `spec.jobTemplate.spec.template.spec`. Pod: `spec`. A Job, CronJob, DaemonSet, StatefulSet,
   Helm chart, or Kustomize base → read [workload-kinds.md](references/workload-kinds.md) first.
2. Facts are yours to find: the Dockerfile `USER` and `EXPOSE`, the health endpoints in the code, the
   conventions of the repo's other manifests. Read them before you write a value.
3. Values only the user knows are decisions: memory and CPU numbers, a UID when the image has no numeric
   `USER`, a probe path the code does not show, a livenessProbe, a grace period other than 600. Ask for
   them in one bundled question. When the user is unavailable or says to go ahead, write the pod.yaml
   value with a `# TODO:` comment and list it under `## Placeholders`.
4. An edit brings every pod template you touch up to the floor, because the user asked you into that
   file; other files keep their content.

## The floor

| Field                                | Value                                                                                                    | Why, and the exception                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `image`                              | an immutable tag (semver, git SHA, build ID) or a digest                                                 | A moving tag (`latest`, `stable`, none) runs different code in two pods and breaks rollback. Keep the user's tag and add `# TODO: pin to an immutable tag`. Leave `imagePullPolicy` out: its defaults are correct.                                                                                                                                                       |
| `ports[].containerPort`              | the app's port, written in the spec                                                                      | Many images have no `EXPOSE`. A batch container with no server gets no port.                                                                                                                                                                                                                                                                                             |
| `readinessProbe`                     | on every long-running container; `exec` when there is no port                                            | A rolling update and a Service wait for it. Jobs and CronJobs have neither, so they get no readinessProbe.                                                                                                                                                                                                                                                               |
| `livenessProbe`                      | only for an app known to hang                                                                            | A bad one restarts healthy pods. It never checks a dependency, because then a database outage restarts every pod.                                                                                                                                                                                                                                                        |
| `resources`                          | `requests.memory` = `limits.memory`, `requests.cpu` set, no `limits.cpu`                                 | Memory cannot be throttled, so the limit equals what the scheduler reserves. A CPU limit throttles on an idle node. This gives **Burstable** QoS; **Guaranteed** needs CPU and memory limits equal to requests on every container, so add `limits.cpu` = `requests.cpu` only when the user needs Guaranteed (static CPU manager). The pod.yaml numbers are placeholders. |
| container `securityContext`          | `allowPrivilegeEscalation: false`, `privileged: false`                                                   | Blocks setuid gain; a privileged container is host root.                                                                                                                                                                                                                                                                                                                 |
| pod `securityContext.seccompProfile` | `type: RuntimeDefault`                                                                                   | Kubernetes runs `Unconfined` unless asked.                                                                                                                                                                                                                                                                                                                               |
| pod `securityContext` user           | `runAsNonRoot: true`; `runAsUser` and `runAsGroup: 1001` unless the image sets a numeric non-root `USER` | A named `USER` (`USER node`) with `runAsNonRoot` fails with `CreateContainerConfigError`; set `runAsUser` or tell the user to make `USER` numeric. Keep UIDs below 65536.                                                                                                                                                                                                |
| `hostUsers`                          | `false`                                                                                                  | Container root maps to an unused host UID. GA in 1.36, on by default since 1.33. A pod with `hostNetwork`, `hostPID`, or `hostIPC` keeps the host user namespace: leave `hostUsers` out and say why. Name the node requirements in the hand-back.                                                                                                                        |
| `automountServiceAccountToken`       | `false`                                                                                                  | Most apps never call the API. An app that does (operator, controller, CI runner) gets `true`, its own `serviceAccountName`, and minimal RBAC.                                                                                                                                                                                                                            |
| `enableServiceLinks`                 | `false`                                                                                                  | Service env vars clash with the app's own. Tell the user to search the app for `_SERVICE_HOST`, `_SERVICE_PORT`, and `_PORT_` and use DNS names.                                                                                                                                                                                                                         |
| `terminationGracePeriodSeconds`      | `600`                                                                                                    | The 30s default cuts long polls, uploads, and queue drains. It is a maximum: an app that exits early does not wait.                                                                                                                                                                                                                                                      |
| `appArmorProfile`                    | unset, as the commented block in pod.yaml                                                                | Setting it stops pods on SELinux nodes. Uncomment it only when every node runs AppArmor; `Unconfined` is a finding.                                                                                                                                                                                                                                                      |

The node requirements, the token alternatives, and the full reasons are in [why.md](references/why.md):
read it when the user asks why, or when an exception in the table applies.

## Teaching comments

A manifest you write keeps the pod.yaml style: one short inline `#` comment on each floor field that says
why it is there. The comments are how the user's team learns the floor, so they stay in the output.

## Review

When the user asks you to review, audit, or check a manifest for production, run `scripts/floor-check.py`
on it (or on `helm template` / `kustomize build` output piped to `-`) and write the report under these
three `##` headings, in this order:

- `## Meets the floor`: the floor fields already set.
- `## Missing or wrong`: one entry per finding with the field, its location, the fixed YAML, and one
  sentence on why. Cite the script's rule id. Add what the script cannot see: a probe that checks a
  dependency, numbers that look copied from pod.yaml.
- `## Suggested`: `readOnlyRootFilesystem: true`, `capabilities.drop: [ALL]`, a `startupProbe` for a slow
  boot, a PodDisruptionBudget, a NetworkPolicy. One line each.

Change the manifest only when the user asks for fixes, because a review is a report.

## Hand-back

End every create or edit task with these three `##` sections, in this order:

- `## Defaults applied`: a `| Default | Why here |` table, one row per floor field you set.
- `## Questions`: the decisions from working style step 3 that are still open, numbered. Write `none`
  when there are none.
- `## Placeholders`: every `# TODO:` value with its field. Write `none` when there are none.

## Validate

Run `scripts/floor-check.py <file>...` on every manifest you wrote or edited. It prints one line per
finding with a rule id and ends with `floor-check: clean` or the finding count. Fix each finding, or
keep it and say why in the hand-back (a CPU limit for Guaranteed QoS, a token for an operator). When
`kubeconform` is installed, also run `kubeconform -strict -summary <file>` for schema errors. A tool that
is absent: say so by name and offer the `brew install` command.

For fields newer than your training data, the `k8s-catch-up` skill has one file per feature.

## Done when

- [ ] `floor-check.py` is clean on every manifest you wrote or edited, or each remaining rule id is
      named in the hand-back with its reason
- [ ] Every floor field in the output has its teaching comment
- [ ] A review has the three headings and changes no file the user did not ask to change
- [ ] A create or edit ends with `## Defaults applied`, `## Questions`, and `## Placeholders`
