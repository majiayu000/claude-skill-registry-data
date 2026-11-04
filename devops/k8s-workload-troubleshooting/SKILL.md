---
name: k8s-workload-troubleshooting
description: >-
  Use when a pod or workload is unhealthy in Kubernetes: pods stuck in Pending,
  CrashLoopBackOff, ImagePullBackOff or ErrImagePull, containers OOMKilled (exit code
  137), failing liveness, readiness or startup probes, pods Running but not Ready, a
  Deployment rollout that does not progress (ProgressDeadlineExceeded), or a Job or
  CronJob that fails. Investigates with kubectl get, describe, logs and events, and
  proposes fixes. Reads first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37"
  verified-on: "2026-10-23"
---

# Kubernetes workload troubleshooting

Find out why a pod, Deployment, StatefulSet, DaemonSet, Job or CronJob is unhealthy, and
propose a fix. **Read first, ask before changing.** Run the investigation commands
freely. Run a command under an "Ask first" line only after the user approves that exact
command; if your credentials do not allow it, give it to the user to run. Never run a
"Proposed fix"; hand it to the user.

The commands use placeholders: `my-namespace`, `my-app` (the workload) and `my-pod`
(one of its pods). Replace them with the real names. Never read Secrets. If logs or
output contain passwords, tokens or keys, do not repeat them.

## When to use

- A pod is `Pending`, `ContainerCreating`, `ErrImagePull`, `ImagePullBackOff`,
  `CrashLoopBackOff`, `OOMKilled`, `Error`, or `Running` but not ready (`0/1`).
- A container keeps restarting, or a probe keeps failing (`Unhealthy` events).
- A rollout never finishes: `kubectl rollout status` waits or reports that the
  Deployment "exceeded its progress deadline".
- A Job fails or never completes, or a CronJob's runs fail.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The node is the cause (`NotReady`, memory, disk or PID pressure, evictions, taints no
  pod tolerates): `k8s-node-troubleshooting`.
- A PersistentVolumeClaim is the cause (unbound claim, attach or mount errors):
  `k8s-storage-troubleshooting`.
- The pods are healthy and Ready, but traffic still does not arrive (Service, DNS,
  NetworkPolicy, Ingress): `k8s-network-troubleshooting`.
- A controller cannot create its pods at all (`FailedCreate` with `failed calling
  webhook` or `denied the request`), or a namespace stays `Terminating`:
  `k8s-api-troubleshooting`.
- The pods belong to a CloudNativePG Cluster (label `cnpg.io/cluster`, or an `-initdb`
  or `-join` job pod): `k8s-cloudnative-pg-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. See the pods and their status.** The `STATUS`, `READY` and `RESTARTS` columns say
which reference applies.

```bash
kubectl get pods -n my-namespace -o wide
kubectl get pods -n my-namespace -l app=my-app
```

`app=my-app` is an example label. Take the real selector from the workload, with
`kubectl get deployment my-app -n my-namespace -o jsonpath='{.spec.selector.matchLabels}'`
or the `Selector:` line of `kubectl describe deployment my-app -n my-namespace`, and use
it wherever a command here says `-l app=my-app`.

**2. Describe the failing pod.** Read the container `State` and `Last State` (reason and
exit code), `Restart Count`, `Limits` and `Requests`, the probes, the pod `Conditions`
and the `Events` at the bottom.

```bash
kubectl describe pod my-pod -n my-namespace
kubectl events -n my-namespace --for pod/my-pod
```

**3. Read the logs**, of the current container and of the one that ran before the last
restart. A crash usually explains itself in the previous container's last lines.

```bash
kubectl logs my-pod -n my-namespace --tail=100
kubectl logs my-pod -n my-namespace --previous --tail=100
kubectl logs my-pod -n my-namespace --all-containers --tail=100
```

**4. Look at the owning controller.** Find what changed and whether a rollout is stuck.

```bash
kubectl get deployment my-app -n my-namespace
kubectl describe deployment my-app -n my-namespace
kubectl rollout status deployment/my-app -n my-namespace --timeout=10s
kubectl rollout history deployment/my-app -n my-namespace
kubectl get replicasets -n my-namespace -l app=my-app
kubectl get deployment my-app -n my-namespace -o jsonpath='{.spec.progressDeadlineSeconds}'
```

`describe deployment` does not print the progress deadline; the last command reads it.

For a StatefulSet or DaemonSet use the same `describe`, `rollout status` and `rollout
history` commands with `statefulset/my-app` or `daemonset/my-app`. For a Job:

```bash
kubectl get jobs -n my-namespace
kubectl describe job my-app -n my-namespace
kubectl get pods -n my-namespace -l job-name=my-app
```

**5. Check the namespace's recent warnings**, which also show problems of objects that
never got a pod (quota, admission, ReplicaSet creation).

```bash
kubectl events -n my-namespace --types=Warning
```

**6. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| `Pending`, `FailedScheduling` | [references/pending.md](references/pending.md) |
| `CrashLoopBackOff`, `Error`, restarts | [references/crashloop.md](references/crashloop.md) |
| `ErrImagePull`, `ImagePullBackOff`, `InvalidImageName` | [references/image-pull.md](references/image-pull.md) |
| `Unhealthy` events, `Running` but `0/1` ready, liveness restarts | [references/probes.md](references/probes.md) |
| `OOMKilled`, exit code 137, CPU throttling, quota or LimitRange errors | [references/oom-and-limits.md](references/oom-and-limits.md) |
| Rollout stuck, `ProgressDeadlineExceeded`, `ReplicaFailure` | [references/rollouts.md](references/rollouts.md) |
| Job failed, `BackoffLimitExceeded`, `DeadlineExceeded`, CronJob not running | [references/jobs.md](references/jobs.md) |

## Read the results

What the common findings mean (Kubernetes 1.37):

- **Pod phase `Pending`**: the pod is accepted but not all containers are set up and
  ready to run. This covers both waiting to be scheduled and pulling images. If the
  `PodScheduled` condition is `False` with a `FailedScheduling` event, the scheduler
  found no node; see [pending.md](references/pending.md).
- **Container state `Waiting`** with reason `ErrImagePull` or `ImagePullBackOff`: the
  image could not be pulled. The pull event's message says why (tag not found,
  unauthorized, cannot reach the registry). The kubelet keeps retrying with a growing
  delay, capped at 5 minutes.
- **`CrashLoopBackOff`**: the container starts, exits, and the kubelet waits longer
  before each restart (10s, 20s, 40s, ... capped at 5 minutes by default; reset after
  10 minutes of running). The cause is in `Last State` and in `kubectl logs --previous`,
  not in the word CrashLoopBackOff.
- **`Last State: Terminated`, `Reason: OOMKilled`, `Exit Code: 137`**: the container
  used more memory than its memory limit and the kernel killed it. Raise the limit or
  reduce the app's memory use. A node under memory pressure evicting pods is a different
  cause (an `Evicted` event and pod status); that one belongs to
  `k8s-node-troubleshooting`.
- **`Reason: Error` with another exit code**: the app exited by itself. The logs of the
  previous container say why (missing config, bad argument, failed dependency).
- **`Running` but `READY 0/1`, no restarts, `Unhealthy` "Readiness probe failed"
  events**: the readiness probe fails, so the pod is not a ready endpoint of its Services
  and gets no traffic (unless a Service sets `publishNotReadyAddresses: true`). The
  container is not restarted.
- **Restarts with `Unhealthy` "Liveness probe failed" (or startup probe) events**: the
  kubelet kills the container after `failureThreshold` failures in a row and restarts it.
- **Deployment condition `Progressing=False`, reason `ProgressDeadlineExceeded`**: the
  new ReplicaSet made no progress for the Deployment's `progressDeadlineSeconds` (read it
  from the spec; 600 is only the default when unset). Kubernetes
  only reports this; it does not roll back. The new ReplicaSet's pods show the real
  cause (image pull, crash, readiness, quota).
- **Job condition `Failed`, reason `BackoffLimitExceeded`**: pods failed more times than
  `backoffLimit` (default 6). Reason `DeadlineExceeded`: the Job ran longer than
  `activeDeadlineSeconds`.

State the cause in one sentence, then the evidence you saw (the event reason and
message, the exit code, the condition), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it. The
fixes here are reversible, so they go under "Ask first" and run only after the user says
yes. Anything destructive or hard to undo (deleting a pod or a Job, `replace --force`)
is never run by you: hand it to the user as a proposed fix and say why. Prefer fixing
the source the workload is deployed from (manifest, Helm values, GitOps repository) when
there is one; a direct command is for when there is not, or for an urgent mitigation.
Typical fixes:

Correct an image tag that does not exist (the container name is the one in the pod
spec):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl set image deployment/my-app app=registry.example.com/my-app:1.4.2 -n my-namespace
# Undo: kubectl set image deployment/my-app app=registry.example.com/my-app:1.4.3 -n my-namespace
```

Roll a stuck Deployment back to the previous revision. First note the current revision
with `kubectl rollout history deployment/my-app -n my-namespace`; the undo returns to it
by number (here revision 3):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl rollout undo deployment/my-app -n my-namespace
# Undo: kubectl rollout undo deployment/my-app -n my-namespace --to-revision=3
```

Raise a memory limit that the app outgrows (choose the value from the app's real use):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl set resources deployment/my-app -c app --limits=memory=256Mi --requests=memory=256Mi -n my-namespace
# Undo: kubectl set resources deployment/my-app -c app --limits=memory=32Mi --requests=memory=32Mi -n my-namespace
```

Point a readiness probe at a path the app serves:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch deployment my-app -n my-namespace --type=json -p '[{"op": "replace", "path": "/spec/template/spec/containers/0/readinessProbe/httpGet/path", "value": "/"}]'
# Undo: kubectl patch deployment my-app -n my-namespace --type=json -p '[{"op": "replace", "path": "/spec/template/spec/containers/0/readinessProbe/httpGet/path", "value": "/healthz"}]'
```

Write the undo with the values you actually found, so it restores the current state.

## Sources

Checked against the Kubernetes 1.37 documentation:

- [Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/):
  phases, container states, restart backoff, CrashLoopBackOff, pod conditions, probes.
- [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
  and [Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/):
  probe fields, defaults, HTTP success range.
- [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/):
  OOM kills, CPU throttling, `FailedScheduling`, `OOMKilled` with exit code 137.
- [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/):
  endpoint `ready` condition, `publishNotReadyAddresses`.
- [Images](https://kubernetes.io/docs/concepts/containers/images/): `ImagePullBackOff`,
  pull back-off, image pull policy.
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/):
  `progressDeadlineSeconds`, `ProgressDeadlineExceeded`, rollout history and undo.
- [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) and
  [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/):
  `backoffLimit`, pod failure back-off, `activeDeadlineSeconds`, CronJob policies.
- [Debug Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/) and
  [Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/):
  Pending and Waiting pods, `kubectl logs --previous`.
