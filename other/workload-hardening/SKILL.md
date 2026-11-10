---
name: workload-hardening
description: Writes and fixes production Kubernetes manifests (Deployment, StatefulSet, Job, CronJob, Pod) for Kubernetes 1.34-1.37, checked against the v1.37 source and a 1.37 cluster. Covers Pod Security Standards restricted on every init, sidecar and ephemeral container (seccompProfile, not the removed annotations; drop ALL; volume allowlist), the kubelet runAsNonRoot check that rejects images whose USER is a name or unset, readOnlyRootFilesystem with emptyDir, probes, graceful shutdown (preStop sleep action in distroless images, grace period budgets), PodDisruptionBudget with unhealthyPodEvictionPolicy, HPA autoscaling/v2 with CPU requests on every container, topology spread, native sidecars for Jobs, removed API versions. Use when editing Kubernetes YAML, moving a namespace to enforce restricted, or debugging CreateContainerConfigError, FailedPreStopHook, 502s during rollouts, drains blocked by a PDB, HPA unknown CPU, or a Job stuck on a proxy sidecar.
license: MIT
---

# Kubernetes workload hardening

Current Kubernetes is **1.37** (1.37.2, 2026-10-28; 1.34 to 1.37 are supported). Much of the YAML
in tutorials and training data predates 1.25 to 1.37 and is wrong in ways that apply cleanly and
fail later: pods that are never created, containers stuck in `CreateContainerConfigError`, hooks
that fail silently, drains that hang. Everything below was checked against the v1.37.2 source,
kubernetes.io, and a 1.37 cluster.

## What changed (check against this, not memory)

| Change | Since | What it means for the manifest |
| --- | --- | --- |
| seccomp annotations (`seccomp.security.alpha.kubernetes.io/pod`, `container.seccomp...`) | kubelet ignores them since 1.25, removed 1.27 | They do nothing. Use `securityContext.seccompProfile.type: RuntimeDefault`. The API server warns "non-functional in v1.27+", and PSA restricted rejects a pod that only has the annotation. |
| AppArmor fields | GA 1.30 | `securityContext.appArmorProfile`; the `container.apparmor.security.beta.kubernetes.io/*` annotations are deprecated. |
| Native sidecars: `initContainers[*].restartPolicy: Always` | on by default 1.29, GA 1.33 | Proxies and log shippers in Jobs no longer block completion. Main containers get SIGTERM first; sidecars stop afterwards in reverse order. |
| `lifecycle.preStop.sleep.seconds` | on by default 1.30, GA 1.34 (`seconds: 0` allowed since 1.34) | Run by the kubelet, needs nothing in the image. The way to delay shutdown in distroless or scratch images. |
| PDB `unhealthyPodEvictionPolicy: AlwaysAllow` | GA 1.31 | Lets drains evict Running-but-not-Ready pods; the default `IfHealthyBudget` blocks drains of crash-looping workloads. |
| PSS baseline: no `host` in `httpGet`/`tcpSocket` probes or lifecycle handlers | 1.34 | Leave `host` unset. |
| PSS restricted forbids `procMount` other than `Default` | 1.35 | Even with user namespaces. |
| PSS relaxes `runAsNonRoot` and `runAsUser` for `hostUsers: false` | policy 1.35; user namespaces GA 1.36 | Pods in a user namespace may run as uid 0 inside it. |
| `image` volumes | GA 1.36 | Allowed by the restricted volume check (the docs table omits it; the admission code allows it). |
| HPA `behavior.scaleUp/scaleDown.tolerance` | GA 1.37 | Per-direction tolerance instead of the global 10%. |
| HPA `minReplicas: 0` | beta, on by default 1.37 | Only with at least one Object or External metric. |
| Pod-level `spec.resources` | beta, on by default 1.34 | The HPA uses pod-level requests when set. |
| Removed API versions | 1.22 to 1.32 | `policy/v1beta1` PDB and `batch/v1beta1` CronJob (1.25), `autoscaling/v2beta1` (1.25) and `v2beta2` (1.26), `extensions/v1beta1` and `networking.k8s.io/v1beta1` Ingress (1.22). See [API versions](references/api-versions.md). |

## Procedure for any workload change

1. **Inventory.** List every pod template (Deployment, StatefulSet, DaemonSet, ReplicaSet, Job,
   CronJob `spec.jobTemplate.spec.template`, bare Pods) and every container in each: `initContainers`
   (regular and sidecar), `containers`, `ephemeralContainers`. Policies apply to all of them.
2. **Know each image.** For every image, find out: its `USER` (numeric, a name, or none, which means
   root), whether it has a shell and coreutils (distroless, scratch and chiseled images do not), and
   which paths it writes at runtime (`/tmp`, caches, pid files). Read the Dockerfile when the image
   is built in the repo; `docker image inspect --format '{{.Config.User}}' IMAGE` otherwise.
3. **Apply the restricted security context** (below) to every container, then check that each
   container can still start and write what it needs.
4. **Probes**: startup for slow starts, liveness that only checks the process, readiness that checks
   dependencies.
5. **Shutdown**: drain delay that works in this image, a grace period that covers it plus the
   longest request.
6. **Availability**: PDB that allows drains at every replica count, HPA with requests on every
   container, spread across zones.
7. **Validate offline**: `kubeconform -strict` with schemas for the cluster's version (a typo such as
   `readOnlyRootFileSystem` or a removed `apiVersion` fails). Against a cluster:
   `kubectl apply --dry-run=server` (field validation is strict by default) and
   `kubectl label --dry-run=server --overwrite ns <ns> pod-security.kubernetes.io/enforce=restricted`
   lists existing pods that would violate the policy.

## Rule 1: the restricted security context, exactly

PSA `enforce` checks **Pods**, not Deployments: `kubectl apply` of a non-compliant Deployment
succeeds with a warning, then the ReplicaSet fails to create pods (`FailedCreate ... violates
PodSecurity "restricted:latest"`) and the rollout sits at 0 ready. Do not treat a clean apply as
proof.

```yaml
spec:
  template:
    spec:
      securityContext:                 # pod level: inherited by every container
        runAsNonRoot: true
        runAsUser: 10001               # numeric; see Rule 2
        runAsGroup: 10001
        seccompProfile:
          type: RuntimeDefault         # or Localhost; the annotation does nothing
      initContainers:
        - name: wait-for-cache
          image: busybox:1.37
          securityContext:             # repeat on EVERY container, init and sidecar included
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]            # exactly "ALL"; "all" is rejected
      containers:
        - name: web
          image: registry.example.com/web:1.4.2
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
```

What restricted requires (full table with versions in [pod security](references/pod-security-restricted.md)):

- `allowPrivilegeEscalation: false` explicitly on every container (unset fails). Container-level only.
- `runAsNonRoot: true` at pod level, or on every container; an explicit `false` anywhere fails.
- `runAsUser` never `0` (pod or container).
- `seccompProfile.type` `RuntimeDefault` or `Localhost` at pod level, or on every container;
  `Unconfined` anywhere fails.
- `capabilities.drop` contains `ALL` on every container; `add` may only contain `NET_BIND_SERVICE`.
- Volumes only `configMap`, `secret`, `projected`, `downwardAPI`, `emptyDir`, `ephemeral`,
  `persistentVolumeClaim`, `csi`, `image`. No `hostPath`, `nfs`, in-tree cloud disks or `gitRepo`.
- Plus baseline: no `hostNetwork`/`hostPID`/`hostIPC`, no `hostPort`, not `privileged`, no `host`
  in probes and lifecycle handlers, AppArmor only `RuntimeDefault`/`Localhost`, SELinux type only
  `container_t`/`container_init_t`/`container_kvm_t`/`container_engine_t` with no user or role,
  only the safe sysctls.
- Pods with `spec.os.name: windows` are exempt from the privilege-escalation, seccomp and
  capability controls, not from `runAsNonRoot`.

`readOnlyRootFilesystem` is not part of restricted, but it is the usual companion requirement.
Mount an `emptyDir` wherever the process writes (`/tmp` for `os.tmpdir()`, `java.io.tmpdir`,
Python `tempfile`, nginx cache and pid dirs). Prefer pointing the app at one scratch dir (`TMPDIR`)
over many mounts. `emptyDir` is world-writable, so it works with any uid; `sizeLimit` caps it.

Replacing a `hostPath`: CA bundles and config come from a `configMap`/`projected` volume (mount
the directory, or a single key with `subPath`, and keep the path the app reads); node agents
(dogstatsd, OTel) are reached over the network via `status.hostIP` instead of a socket.

## Rule 2: runAsNonRoot needs a numeric user the kubelet can see

With `runAsNonRoot: true` and no `runAsUser`, the kubelet reads the image's `USER` before starting
the container:

| Image `USER` | Result |
| --- | --- |
| numeric, non-zero (`10001`, `65532`, `1000:1000`) | starts |
| a name (`node`, `nonroot`, `app`, `appuser:appgroup`) | `CreateContainerConfigError: container has runAsNonRoot and image has non-numeric user (node), cannot verify user is non-root` |
| none or `0` (busybox, most official images, distroless `:latest` tags) | `CreateContainerConfigError: container has runAsNonRoot and image will run as root` |

Admission passes in all three cases; the failure only shows on the node. Fix with a numeric
`runAsUser` (pod level covers init containers too) matching the image's user when files are owned
by it (`node` is 1000 in the official Node images, `nonroot` is 65532 in distroless), or change the
Dockerfile to `USER 10001` / `USER 1000:1000`. Third-party init containers such as busybox need a
uid too: a pod-level `runAsUser` gives them one.

## Rule 3: probes

- **startupProbe** for anything that can take more than a few seconds to start: liveness and
  readiness do not run until it succeeds. Budget = `failureThreshold * periodSeconds`
  (e.g. `periodSeconds: 5, failureThreshold: 24` allows 120 s).
- **livenessProbe** checks only that the process is not wedged: a cheap endpoint that does not
  touch the database, caches or other services. If liveness fails when a dependency is down, one
  database blip restarts every pod at once and turns an outage into a crash loop.
- **readinessProbe** may check dependencies: failing it only removes the pod from Service
  endpoints. Keep it on a different endpoint from liveness.
- httpGet success is 200-399. Probe by port name. `tcpSocket` and `grpc` probes need nothing in the
  image; `exec` probes need the binary to exist (not in distroless) and fork processes each period.
- Never set `host` on probes (baseline 1.34+): the kubelet probes the pod IP.

## Rule 4: graceful shutdown that actually delays

On termination the pod's endpoints are marked terminating **at the same time** as the kubelet
starts the shutdown, but ingress controllers, kube-proxy and cloud load balancers act on that a few
seconds later. A pod that closes its listener on SIGTERM drops the requests they still send it
(502, connection refused).

Sequence: preStop hook runs to completion, then SIGTERM, then SIGKILL when
`terminationGracePeriodSeconds` (default 30) runs out. The grace period counts from the start, so
it must cover **hook + drain + the longest request**. A hook still running at the deadline gets one
2-second extension, then everything is killed.

```yaml
spec:
  terminationGracePeriodSeconds: 50     # 10 s delay + 30 s longest request + headroom
  containers:
    - name: web
      lifecycle:
        preStop:
          sleep:
            seconds: 10                 # kubelet-side; works in distroless and scratch images
```

- `exec: {command: ["sh", "-c", "sleep 10"]}` (or `["sleep", "10"]`) only works if the image has a
  shell and a `sleep` binary. In distroless/scratch/chiseled images the exec fails at once with a
  `FailedPreStopHook` event, SIGTERM follows immediately, and the delay you added does not exist.
  Measured on 1.37: pod deletion took 1 s with the exec hook, 9 s with `sleep: {seconds: 8}`.
- An exec of the runtime that is in the image also works (`["/nodejs/bin/node", "-e",
  "setTimeout(() => {}, 10000)"]` in distroless Node), but only with its absolute path: distroless
  PATH directories are empty.
- Alternatively the app delays closing its listener after SIGTERM, then drains. Either way the app
  must still finish in-flight requests after it stops accepting and then exit on its own.
- `lifecycle` `tcpSocket` handlers are deprecated and not run by the kubelet.
- Details, sidecar ordering and the worked budget: [shutdown and probes](references/shutdown-and-probes.md).

## Rule 5: PodDisruptionBudget that allows drains

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: checkout
spec:
  maxUnavailable: 1                     # tracks the replica count, unlike minAvailable
  unhealthyPodEvictionPolicy: AlwaysAllow
  selector:
    matchLabels:
      app.kubernetes.io/name: checkout  # exactly this workload's pods
```

- Allowed disruptions = ready pods minus desired healthy. `minAvailable` equal to the replica count,
  `100%`, or `maxUnavailable: 0` allow zero evictions: every drain of a node running one of those
  pods hangs until someone intervenes.
- `minAvailable: N` is a fixed count: with an HPA, `minAvailable: 2` allows 10 concurrent evictions
  at 12 replicas and blocks all evictions at 2. Use `maxUnavailable` when the replica count moves.
- Percentages round **up** for both fields (`maxUnavailable: 10%` of 12 is 2).
- Default `IfHealthyBudget`: a Running-but-not-Ready pod can be evicted only if the budget is
  currently met. When a bad release has every pod crash-looping, nothing can be evicted and drains
  stall. `AlwaysAllow` evicts unready pods regardless; Pending/Succeeded/Failed pods are always
  evictable.
- One PDB per pod: a pod matched by two budgets cannot be evicted at all (the API returns 500).
  In `policy/v1` an empty selector `{}` matches every pod in the namespace.

## Rule 6: HPA autoscaling/v2

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: checkout
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: checkout }
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 65 }
```

- `Utilization` is usage divided by **requests**, summed over every container in the pod,
  including sidecars (init containers with `restartPolicy: Always`). One container without a CPU
  request makes utilization undefined for the pod ("missing request for cpu in container ...") and
  the HPA does not scale. Set requests on every container, or use pod-level `spec.resources.requests`
  (1.34+), or a `ContainerResource` metric naming one container.
- A request defaults to the limit when only `limits.cpu` is set.
- `targetAverageUtilization` is the removed v2beta1 field; v2 uses `target.averageUtilization`.
- No `metrics` means 80% CPU.
- Remove `spec.replicas` from the Deployment manifest once an HPA manages it, or every apply resets
  the replica count (expect a one-time scale to the default when you first remove it; see
  [availability](references/availability.md)).

## Rule 7: spread replicas

```yaml
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway   # DoNotSchedule can leave pods Pending
          labelSelector:
            matchLabels: { app.kubernetes.io/name: checkout }
          matchLabelKeys: [pod-template-hash] # spread each rollout revision separately
```

The `labelSelector` must match the pod's own labels or the constraint counts nothing.

## Rule 8: Jobs with a proxy or agent sidecar

A sidecar listed under `containers` never exits, so the Job's pod never completes. Make it a native
sidecar:

```yaml
      initContainers:
        - name: db-proxy
          image: gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.27.0
          args: ["--health-check", "--http-address=0.0.0.0", "--http-port=9801", "PROJECT:REGION:INSTANCE"]
          restartPolicy: Always          # sidecar: starts before, stops after the main container
          startupProbe:                  # main containers wait until it passes; probes hit the
            httpGet: { path: /startup, port: 9801 }   # pod IP, not localhost
      containers:
        - name: backfill
```

Measured on 1.37: with the proxy in `containers` the Job stayed Running forever; as a native sidecar
it completed. A sidecar that ignores SIGTERM delays completion by the pod's grace period. Old
workarounds (shared process namespace plus `pkill`, `/quitquitquit` endpoints, shell traps on a
shared file) are no longer needed. More: [sidecars and Jobs](references/sidecars-and-jobs.md).

## Rule 9: resources and the rest

- Requests on every container (scheduling, HPA, eviction order). Memory limit = request for
  predictable OOM behaviour; CPU limits are optional and cause throttling.
- Pin images by tag and digest; `imagePullPolicy` defaults to `Always` only for `:latest` or untagged.
- `automountServiceAccountToken: false` unless the pod calls the API.
- YAML is read with YAML 1.1 rules: quote `"on"`, `"off"`, `"yes"`, `"no"`, `"y"`, `"n"` and
  version-like strings, or they become booleans and floats.

## Review checklist

- [ ] Every container (init, sidecar, app, ephemeral) has `allowPrivilegeEscalation: false`,
      `capabilities.drop: ["ALL"]`, `readOnlyRootFilesystem: true`.
- [ ] Pod-level `runAsNonRoot: true`, numeric non-zero `runAsUser`, `seccompProfile: RuntimeDefault`;
      no seccomp/AppArmor annotations.
- [ ] Every image's USER is numeric or overridden by `runAsUser`; root-default images get a uid.
- [ ] Only allowed volume types; every written path is an `emptyDir`.
- [ ] Liveness never depends on another service; slow starts have a startupProbe.
- [ ] preStop delay works in this image (sleep action for distroless); grace period >= delay +
      longest request.
- [ ] PDB uses `maxUnavailable` (or a safe `minAvailable`) at every replica count, has
      `unhealthyPodEvictionPolicy: AlwaysAllow`, and selects exactly one workload.
- [ ] HPA is `autoscaling/v2`; every container has a CPU request.
- [ ] Jobs with sidecars use `restartPolicy: Always` init containers.
- [ ] Only API versions served by the target cluster; `kubeconform -strict` passes.

## References

- [Pod Security Standards: every control, version and exception](references/pod-security-restricted.md)
- [Shutdown sequence, preStop variants, probes](references/shutdown-and-probes.md)
- [PDB arithmetic, eviction rules, HPA, topology spread](references/availability.md)
- [Native sidecars and Jobs](references/sidecars-and-jobs.md)
- [API versions, annotations, validation](references/api-versions.md)
- [Sources](references/sources.md)
