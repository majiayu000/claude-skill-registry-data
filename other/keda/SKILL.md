---
name: keda
description: >-
  Configure, operate, and master KEDA (Kubernetes Event-driven Autoscaling) —
  ScaledObject, ScaledJob, TriggerAuthentication CRDs, 70+ scalers, HPA
  behavior tuning, scale-to-zero, the KEDA HTTP Add-on, production hardening,
  multi-trigger semantics, scalingModifiers formulas, GitOps integration, and
  troubleshooting stuck scalers. Covers the common traps (cooldownPeriod only
  applies to N→0, CPU/memory cannot drive scale-to-zero alone, activationThreshold
  vs threshold, multi-trigger max-of semantics, HPA conflicts).
when_to_use: >-
  Triggers on "KEDA", "kedacore", "ScaledObject", "ScaledJob",
  "TriggerAuthentication", "ClusterTriggerAuthentication", "keda.sh/v1alpha1",
  "autoscaling.keda.sh", "keda-hpa-", "keda-operator", event-driven autoscaling,
  scale-to-zero in Kubernetes, external metrics apiserver issues, stuck
  scalers, or any Kubernetes autoscaling question involving queues (SQS,
  Kafka, RabbitMQ, Azure Service Bus, Pub/Sub), cron schedules, Prometheus
  queries, or external metric sources. Also triggers on cpu/memory scaler
  questions when KEDA is mentioned. Do NOT trigger on pure HPA-only questions
  that don't involve KEDA.
---

# KEDA — Kubernetes Event-driven Autoscaling

KEDA extends Kubernetes HPA with event-driven scalers (queues, cron, Prometheus,
etc.) and owns the `0 ↔ 1` transition so workloads can truly scale to zero.
The skill covers three CRDs (`ScaledObject`, `ScaledJob`, `TriggerAuthentication`),
70+ scalers, HPA behavior tuning, and the gotchas that make production KEDA
misbehave.

This file holds the mental model and the 80% patterns. Reach for the files in
`references/` for depth.

## Mental model — who owns what

KEDA and the built-in HPA divide responsibility:

| Transition | Owner | Mechanism |
|---|---|---|
| `0 → 1` activation | **KEDA operator** | Polls triggers every `pollingInterval` (default 30s). Any active trigger wakes the workload. |
| `1 → N` scale-up | **HPA** (managed by KEDA) | Reads external metrics via `keda-operator-metrics-apiserver` every ~15s. Replicas = ceil(sum(metric) / target). |
| `N → 1` scale-down | **HPA** | Damped by `behavior.scaleDown.stabilizationWindowSeconds` (default **300s**). |
| `1 → 0` deactivation | **KEDA operator** | All triggers inactive for `cooldownPeriod` (default **300s**). |

For each `ScaledObject`, KEDA creates a managed HPA named `keda-hpa-<scaledobject-name>`.
Don't create a second HPA on the same target — it conflicts. If one already
exists, KEDA's admission webhook rejects the ScaledObject until the manual HPA
is deleted (or adopted via annotation
`scaledobject.keda.sh/transfer-hpa-ownership: "true"`).

ScaledJob is different: no HPA. KEDA spawns new `Job` resources when triggers
activate, and jobs run to completion — they are never killed to scale down.

## Decide between ScaledObject, ScaledJob, and HTTP Add-on

| Workload | Use |
|---|---|
| Long-running service (web, consumer, worker) | `ScaledObject` |
| One event → one job that must complete uninterrupted | `ScaledJob` |
| HTTP traffic, scale on RPS or concurrency (inc. scale-to-zero) | KEDA HTTP Add-on (`HTTPScaledObject`) |

The killer case for `ScaledJob`: a long-running message handler whose pod is
terminated mid-work by the HPA loses progress. Jobs are immune to that.

## Canonical templates

Adapt these. Every real ScaledObject is a variation on one of them.

### Queue-driven worker (RabbitMQ, scale 0 → 30)

```yaml
apiVersion: keda.sh/v1alpha1
kind: TriggerAuthentication
metadata:
  name: rabbitmq-auth
  namespace: apps
spec:
  secretTargetRef:
    - parameter: host
      name: rabbitmq-credentials
      key: amqp-host
---
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-worker
  namespace: apps
spec:
  scaleTargetRef:
    name: order-worker
  pollingInterval: 30
  cooldownPeriod: 300
  minReplicaCount: 0
  maxReplicaCount: 30
  fallback:
    failureThreshold: 3
    replicas: 3
  triggers:
    - type: rabbitmq
      metadata:
        protocol: amqp
        queueName: orders
        mode: QueueLength
        value: "20"           # target: 20 messages per replica
        activationValue: "5"  # wake from 0 at 5 messages
      authenticationRef:
        name: rabbitmq-auth
```

### Prometheus + CPU multi-trigger (web service, scale 3 → 50)

Two triggers in a ScaledObject combine as **max of desired replicas**, not sum.
Whichever trigger wants more pods wins.

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-api
  namespace: apps
spec:
  scaleTargetRef:
    name: order-api
  minReplicaCount: 3
  maxReplicaCount: 50
  advanced:
    horizontalPodAutoscalerConfig:
      behavior:
        scaleUp:
          stabilizationWindowSeconds: 0
          policies:
            - type: Percent
              value: 100
              periodSeconds: 30
        scaleDown:
          stabilizationWindowSeconds: 300
          policies:
            - type: Percent
              value: 10
              periodSeconds: 60
  triggers:
    - type: prometheus
      name: rps
      metadata:
        serverAddress: http://prometheus.monitoring.svc:9090
        query: sum(rate(http_requests_total{service="order-api"}[1m]))
        threshold: "200"
        ignoreNullValues: "true"
    - type: cpu
      metricType: Utilization
      metadata:
        value: "70"
```

### Cron-based schedule (business hours / off-hours)

Overlapping cron triggers combine as max. Use `desiredReplicas` as a floor —
if other triggers demand more, they win.

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: inference
  namespace: ml
spec:
  scaleTargetRef:
    name: inference
  minReplicaCount: 1
  maxReplicaCount: 12
  triggers:
    - type: cron
      metadata:
        timezone: Europe/Stockholm
        start: "0 7 * * 1-5"
        end: "0 18 * * 1-5"
        desiredReplicas: "10"
    - type: cron
      metadata:
        timezone: Europe/Stockholm
        start: "0 18 * * 1-5"
        end: "0 22 * * 1-5"
        desiredReplicas: "5"
```

### Long-running job (one event → one job)

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledJob
metadata:
  name: video-encoder
spec:
  jobTargetRef:
    parallelism: 1
    completions: 1
    backoffLimit: 2
    template:
      spec:
        restartPolicy: Never
        containers:
          - name: encoder
            image: encoder:v1
  pollingInterval: 30
  maxReplicaCount: 20
  successfulJobsHistoryLimit: 5
  failedJobsHistoryLimit: 10
  scalingStrategy:
    strategy: accurate  # queueLength - runningJobs; avoids over-provisioning
  triggers:
    - type: aws-sqs-queue
      metadata:
        queueURL: https://sqs.us-east-1.amazonaws.com/123/videos
        queueLength: "1"        # 1 message per job
        awsRegion: us-east-1
      authenticationRef:
        name: aws-irsa
```

## Gotchas that bite in production

Every item here has cost people incidents. Internalize them.

**1. `cooldownPeriod` only governs `N → 0`, not `N → 1`.**
Scale-down from 10 pods to 1 is controlled entirely by HPA's
`behavior.scaleDown.stabilizationWindowSeconds` (default 300s). Setting
`cooldownPeriod: 1800` does not slow N→1 scale-down. Configure both.

**2. CPU and memory scalers cannot drive scale-to-zero alone.**
HPA requires `minReplicas ≥ 1` for resource metrics — no pods means no
CPU signal to wake them. Pair CPU/memory with a secondary scaler
(`cron`, a queue trigger, `prometheus`) that can evaluate without running pods.

**3. `activationThreshold` is ignored when `minReplicaCount ≥ 1`.**
It only gates the `0 → 1` transition. If `minReplicaCount: 1`, setting a high
`activationThreshold` does nothing — pods are always running, so activation
is always true. Don't try to use it as a second scale-down threshold.

**4. Multiple triggers on a ScaledObject combine as `max`, not sum.**
If Kafka lag suggests 10 pods and CPU suggests 5, the result is **10**. For a
weighted combination or ratio, use `advanced.scalingModifiers.formula` (KEDA
2.13+). See `references/patterns.md`.

**5. `idleReplicaCount` only works with the value `0`.**
Other values have HPA compatibility issues. Use it to run e.g. 2 pods while
active but fully scale to zero when idle:
`idleReplicaCount: 0` + `minReplicaCount: 2`.

**6. Manual HPA on the same target blocks the ScaledObject.**
Check `kubectl describe scaledobject`. Delete the manual HPA to resolve,
or set annotation `scaledobject.keda.sh/transfer-hpa-ownership: "true"`.

**7. One external-metrics provider per cluster.**
The API `external.metrics.k8s.io` can only be served by one component at a
time. If Datadog Cluster Agent or Prometheus Adapter is already registered,
KEDA's metrics-apiserver fails silently. Pick one.

**8. `fallback` does not work for cpu/memory triggers.**
It requires `metricType: AverageValue`, which resource metrics lack. Use
fallback on external-metric triggers only (Prometheus, RabbitMQ, etc.).

**9. Always set a `fallback` on production external-metric triggers.**
When Prometheus/Kafka/etc. is unreachable for `failureThreshold` polls in
a row, KEDA injects the fallback replica count rather than leaving the
deployment flapping to `minReplicaCount`.

**10. Don't poll aggressively against shared metric sources.**
`pollingInterval: 5` across 50 ScaledObjects = 600 queries/min against one
Prometheus. 30s is the sane default; drop below only with a reason.

**11. HPA behavior stabilization windows must be multiples of the HPA sync
period (15s).** Use `15s, 30s, 60s, 300s` — not `20s` or `100s`. Non-aligned
windows lead to non-deterministic decisions.

**12. `useCachedMetrics: true` on triggers reduces scaler load** from the
HPA's 15s sync cycle by reusing cached values within the pollingInterval.
Not available for `cpu`, `memory`, or `cron` scalers.

## Pausing and adopting

Annotations on a ScaledObject (not TriggerAuthentication):

| Annotation | Effect |
|---|---|
| `autoscaling.keda.sh/paused: "true"` | Freeze current replica count. Metrics still collected but HPA not reconciled. |
| `autoscaling.keda.sh/paused-replicas: "5"` | Pin to exactly 5 replicas until removed. |
| `autoscaling.keda.sh/paused-scale-in: "true"` | Block scale-down only (HPA scaleDown → Disabled). |
| `autoscaling.keda.sh/paused-scale-out: "true"` | Block scale-up only. |
| `scaledobject.keda.sh/transfer-hpa-ownership: "true"` | Adopt an existing HPA rather than conflict. |
| `autoscaling.keda.sh/force-activation: "true"` | Force all scalers active immediately (break-glass). |

## Debugging a stuck ScaledObject

Run this sequence. 90% of issues surface in the first three steps:

```bash
# 1. Is the ScaledObject Ready? What reason?
kubectl describe scaledobject <name> -n <ns>

# 2. Was the HPA created?
kubectl get hpa keda-hpa-<name> -n <ns> -o yaml

# 3. Operator saying anything?
kubectl logs -n keda deploy/keda-operator --tail=300 | grep <name>

# 4. Is the external metrics API itself alive?
kubectl get apiservice v1beta1.external.metrics.k8s.io

# 5. Can KEDA serve the metric?
kubectl get --raw \
  "/apis/external.metrics.k8s.io/v1beta1/namespaces/<ns>/<metric-name>?labelSelector=scaledobject.keda.sh%2Fname%3D<name>"

# 6. Metrics server logs (scaler-side errors)
kubectl logs -n keda deploy/keda-operator-metrics-apiserver --tail=200
```

The helper `${CLAUDE_SKILL_DIR}/scripts/debug-scaledobject.sh <name> [namespace]`
runs all of these in one shot. See `references/troubleshooting.md` for a
decision tree mapping symptoms to root causes.

## When to reach for the references

- **Picking a scaler for a given source** → `references/scalers.md` (catalog of
  every scaler with YAML snippets and field-level defaults).
- **Every field of ScaledObject/ScaledJob/TriggerAuthentication** →
  `references/crds.md`.
- **Deployment, Helm values, operator flags, auth providers (IRSA, Azure
  Workload Identity, Vault, Key Vault, Secrets Manager), observability** →
  `references/operations.md`.
- **HPA behavior tuning, scalingModifiers formulas, multi-trigger combining,
  cron overlap semantics, HTTP Add-on, GitOps with Argo/Flux, Karpenter
  interplay, production hardening** → `references/patterns.md`.
- **Detailed troubleshooting trees, scripted debugging, known CVEs** →
  `references/troubleshooting.md`.

## Authoring checklist

When writing or reviewing a ScaledObject, tick these:

- [ ] Is the target a long-running service (ScaledObject) or a batch-unit
  (ScaledJob)? Long-running + terminate-mid-work = wrong shape.
- [ ] Is `minReplicaCount: 0` actually safe for this workload? Cold-start
  cost, warmup probes, first-request latency all acceptable?
- [ ] If using a resource (cpu/memory) trigger, is there also an external
  trigger to enable scale-to-zero (or is minReplica ≥ 1 intentional)?
- [ ] `maxReplicaCount` set to a number the cluster/node pool can actually
  provision? Karpenter/CA can provision in time?
- [ ] `fallback` configured on external-metric triggers?
- [ ] `advanced.horizontalPodAutoscalerConfig.behavior` tuned for this
  workload? Default scaleDown of 300s too aggressive for a 60s-warmup pod?
- [ ] Auth via `TriggerAuthentication` (namespace) or
  `ClusterTriggerAuthentication` (cross-namespace); cloud podIdentity
  preferred over static secrets.
- [ ] Required for multi-trigger: each trigger has `name` when
  `scalingModifiers` is in use.
- [ ] Keep `pollingInterval` ≥ 30s unless the event source is local and cheap.
- [ ] Alerts on `keda_scaler_errors_total` and `keda_scaled_object_errors_total`?

## Working with Helm values and operator flags

Key settings when hardening KEDA itself (see `references/operations.md` for the
full set):

- `KEDA_RESTRICT_SECRET_ACCESS=true` — operator only reads secrets in the `keda`
  namespace (forces `ClusterTriggerAuthentication` for cross-namespace secrets).
- `WATCH_NAMESPACE=team-a,team-b` — operator reconciles only listed namespaces.
- `--kube-api-qps=50 --kube-api-burst=75` — raise client throttle at scale.
- Run 2 operator replicas with leader election enabled (one active, one warm).
- Admission webhook `failurePolicy: Fail` for strict validation (catch invalid
  ScaledObjects at submit time).

## One more thing — the KEDA HTTP Add-on is separate and still beta

The main KEDA project does not scale HTTP workloads by RPS on its own. The
HTTP Add-on (a separate deploy, API group `http.keda.sh/v1alpha1`, CRD
`HTTPScaledObject`) does. As of 2026 it's still beta — not recommended for
critical production paths. For an HTTP-scaling pattern today, either:
- use the HTTP Add-on knowing its status, or
- scale from Prometheus RPS queries via the `prometheus` trigger, or
- pick Knative for a full HTTP serving platform.
Details in `references/patterns.md`.
