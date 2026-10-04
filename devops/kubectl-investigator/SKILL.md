---
name: kubectl-investigator
description: Investigate a live or recent incident in a Kubernetes cluster. Anchor the window, bisect the change surface (rollouts, ConfigMaps/Secrets, RBAC, HPA/cluster changes, CronJobs), classify against four reference failure paths (OOM, DNS, cascading-failure, deploy-correlator), confirm the hypothesis with three independent signals, quantify blast radius, and propose mitigation before root cause. Use whenever an agent is asked "what is breaking in the cluster right now", "why did this pod/Deployment just page", "did the rollout cause Z", or to triage an active Kubernetes incident. Vendor-neutral by default (works with kubectl, kube-state-metrics, and whatever telemetry you have); an opt-in Anyshift integration is documented separately.
---

# kubectl-investigator

Methodology skill for investigating a live or recent incident on **Kubernetes**. Produces a timeline, a ranked set of hypotheses, a blast-radius estimate, and a recommended mitigation. Hands off cleanly to `postmortem-author` once the incident is mitigated.

Scope: workloads running on Kubernetes (Deployments, StatefulSets, DaemonSets, Jobs/CronJobs) and the cluster primitives around them (Services, Ingress, CoreDNS, ConfigMaps/Secrets, RBAC, HPA, nodes). External dependencies (third-party APIs, partner TLS endpoints, managed databases) are in scope only as seen *from* a Kubernetes workload — the methodology investigates the cluster-side symptom and the in-cluster change surface.

## When to invoke

- A `PrometheusRule` / Alertmanager alert just fired on a workload and the agent needs to triage before paging a human.
- A user asks "what is breaking in the cluster right now" or "why did Deployment X just page".
- A `kubectl rollout` / Helm release / Argo CD sync went out in the last hour and a metric moved; need to know whether they are linked.
- Pods are crash-looping, `OOMKilled`, or `Pending`, or customer impact is reported with no alert yet; need to find the failing surface.

## The methodology, in order

The order matters. Skipping a step produces confident wrong answers.

### 1. Anchor the window

Lock two timestamps before doing anything else:

- **T0**: the trigger timestamp. Apply this order:
  1. **If an alert is provided as the trigger, T0 = alert fire time.** Use this verbatim. Do not substitute an earlier "first error in logs / first `OOMKilled` event" timestamp just because one exists; the alert fire time is the agreed-upon coordination point for the incident.
  2. **If a customer report is the trigger, T0 = report timestamp.**
  3. **If neither exists (operator-initiated investigation, "pods slow all morning"), T0 = earliest unambiguous signal in the available telemetry** (first `OOMKilled` event, first `SERVFAIL`, first error-rate inflection), and mark T0 as ambiguous (see below).
- **Tnow**: current time, or the timestamp the investigation was triggered.

Every later signal is filtered to `[T0 - 15min, Tnow]`. The 15-minute lead-in catches changes that landed just before the symptom surfaced (a rollout's pods take time to roll, an HPA scale-down takes time to bite).

**If T0 is ambiguous** (operator-triggered with no alert, or "slow all morning"-class reports), the methodology's recommended mitigation in step 6 **must begin with "re-run the investigation with a widened window"** before any irreversible action. The change identified within the original narrow window is likely incomplete; the actual causal change may sit outside it. Do not silently round and do not skip the re-run step.

### 2. Bisect the change surface

Pull every change event that overlaps the window. On Kubernetes the change surface is:

- **Workload rollouts**: `kubectl rollout` / `kubectl apply` / `kubectl set image`, new image tags, new ReplicaSets, Helm releases, Argo CD / Flux syncs.
- **Cluster / capacity changes**: node-pool scaling, node cordon/drain, resource `requests`/`limits` edits, HPA / VPA changes, PodDisruptionBudget edits, PV/PVC/StorageClass changes.
- **RBAC / ServiceAccount changes**: Role / ClusterRole / RoleBinding / ClusterRoleBinding edits, ServiceAccount or its token/permissions changed (these break Secret reads, API access, admission).
- **Config / feature-flag changes**: ConfigMap / Secret edits, CoreDNS `Corefile` ConfigMap edits, Ingress/NetworkPolicy changes, feature-flag flips.
- **Admission / operator changes**: Validating/MutatingWebhookConfiguration edits, CRD or controller upgrades.
- **CronJobs / Jobs** that ran in the window (batch, data migrations, cluster maintenance jobs).

If the window has **zero** change events, treat it as a strong signal in itself: the failure is likely external (upstream provider, certificate expiry, DNS, capacity drift from organic growth) rather than a self-inflicted regression.

### 3. Classify against the four reference paths

Match the failure shape to one of these four canonical paths first. They cover the majority of Kubernetes incidents; only branch out once they are ruled out.

| Path | Tell-tale signals | Confirming evidence |
|---|---|---|
| **OOM** | Container restart count climbing, `CrashLoopBackOff`, RSS / working-set at the container memory limit, `OOMKilled` pod events, retry storm from upstream | Container exit code 137, `reason: OOMKilled` in pod events / `kubectl describe pod`, working-set metric at or above `resources.limits.memory` at T0, a recent rollout that increased per-pod memory footprint |
| **DNS** | Connection failures with `NXDOMAIN` / `SERVFAIL` in logs, `getaddrinfo` / `no such host` errors, sudden latency on in-cluster Service calls, `*.svc.cluster.local` resolution failing while external hosts resolve | CoreDNS error / `SERVFAIL` counts elevated, a recent change to the CoreDNS `Corefile` ConfigMap, kube-dns/CoreDNS pod restarts, `ndots`/search-domain or NetworkPolicy change in the window |
| **Cascading-failure** | One in-cluster dependency degrades, retry counts spike across callers, connection pools / thread pools / sidecar (Envoy) circuits saturate, queue depth grows | Latency increases hop-by-hop toward the root Service, retry-budget metrics, circuit-breaker state changes, 2nd-order Deployments start failing, upstream Pod `Unhealthy` / readiness-probe failures |
| **Deploy-correlator** | Metric breaks within 5 minutes of a rollout on the failing surface, only pods from the new ReplicaSet show the symptom | Canary / blue-green or rolling-update split shows old-RS healthy / new-RS failing, `kubectl rollout undo` restores the metric, the rollout diff touches the failing code path |

If the failure does not match any of the four, classify as **"outside reference paths"** and document why. Outside-reference-paths means the methodology has no reference path for the failure shape, so its confidence in the *root cause* is low and **escalation to a human is mandatory** (step 6). It does not mean the agent does nothing: a pre-approved safe mitigation (traffic-shift to a healthy peer, feature-flag-off) is still recommended as the top action when available, with the root-cause investigation escalated in parallel. See step 6 for the exact ordering.

### 4. Confirm with three independent signals

Never declare a hypothesis on one signal. Require at least three of the following, drawn from independent sources:

- **Pod / cluster events** (`kubectl get events`, kubelet: `OOMKilled`, `BackOff`, `Unhealthy`, `FailedScheduling`).
- **Logs** (application container logs, system component logs).
- **Metrics** (request rate, error rate, latency, saturation, working-set, CoreDNS error rate — from Prometheus / kube-state-metrics).
- **Traces** (distributed traces showing the failing hop / Service).
- **Change events** (rollouts, ConfigMap/Secret, RBAC, HPA/cluster changes).
- **External signals** (customer reports, status pages of dependencies the workload calls).

Two signals from the same source (e.g. two log lines) count as one. The independence requirement is the guard against confirmation bias.

**Split aggregate signals before trusting them.** Error rate, latency, and saturation are usually reported as a single number across every region, cluster, AZ, shard, or canary/stable split. Before classifying, break each aggregate down along these dimensions. A **per-dimension asymmetry** — one region failing while its peer is healthy, one shard hot while the rest are flat — is a first-class diagnostic signal, and aggregate metrics actively hide it (a 25% failure in one of two equally-sized regions shows up as a moderate ~12% aggregate that matches no clean reference path).

When the failing and healthy slices run the **same image tag / same code**, a code-regression path (OOM, deploy-correlator) is ruled out by construction: identical code cannot fail in one slice and not the other. The cause is environmental — config/GitOps drift, a stale Service reference, per-region capacity, an external dependency reachable from only one slice. **A confirmed asymmetry short-circuits the four-path search: stop trying to fit OOM/DNS/cascade/deploy-correlator on the aggregate, classify "outside reference paths" with a `regional-asymmetry` (or shard/AZ-asymmetry) reason, and move to step 5.** Continuing to hunt for a reference-path match on aggregate signals after an asymmetry is detected wastes the investigation and is the single most common way this step runs long.

### 5. Quantify blast radius

Before recommending action, estimate:

- **Users affected** (count or percentage of traffic).
- **Surfaces affected** (which Services/endpoints, which namespaces, which clusters/regions, which customer segments).
- **Business impact** (revenue, SLO burn, contractual obligations if known).

A wrong mitigation that touches more surface than the incident itself is worse than the incident.

### 6. Propose mitigation before root cause

Mitigation comes first. Root cause comes after the bleeding stops.

**Hard constraints, in order. Check these before ranking the standard actions below:**

- **If the classification from step 3 is "outside reference paths", escalation to a human is mandatory — but it is not automatically the *top* action.** Two mitigations are pre-approved as safe because they are reversible and contained, and when one of them is available it becomes the top recommended action:
  - **Traffic-shift away from the failing slice to a healthy peer** (other region/cluster/shard/replica). This is the canonical first move for a regional/shard asymmetry: it stops the bleeding immediately and is trivially reversible. When the asymmetry detector in step 4 has identified a healthy peer, *recommend the traffic-shift as action #1*, then escalate the root-cause investigation (config/GitOps drift, the failing dependency) to a human as the parallel follow-up.
  - **Feature-flag off the failing code path**, if a flag exists.

  Every *other* option — contacting an external provider, irreversible config/RBAC/state changes, anything touching the failing slice directly — is surfaced as an alternative for the human to approve, not executed by the agent. The principle (from FAILURE_MODES M1): outside-reference-paths means low confidence in *root cause*, so escalate the root cause; it does not forbid the safe, reversible mitigation that an on-call would reach for first.
- **If T0 was flagged as ambiguous in step 1, the top recommended action is "re-run the investigation with a widened window".** Only after that re-run identifies a fuller change surface should any irreversible mitigation (`rollout undo`, RBAC change, cluster/infra rollback) be recommended.
- **If the implicated change has `bundle_size > 1` (multiple changes shipped in one rollout), `rollout undo` remains the top recommendation but requires explicit human approval before execution.** Surface the asymmetry explicitly: "the rollback reverts N changes when the incident affects only K of them".
- **If the classification is "cascading-failure", the top action is to break the amplification loop at its source, not to undo a rollout.** A pure cascade typically has no rollout in the window (the trigger is a degraded dependency, not a deploy), so there is nothing to revert. Recommend, in order: open the circuit breaker on / shed load from the **degraded dependency** itself (the root of the cascade), then cap or disable the retry budget at the callers driving the retry storm. Shedding the callers' retries alone treats the symptom (the amplification) while leaving the degraded dependency saturated; opening the circuit at the dependency stops the loop at its origin and lets the dependency recover.

**Standard mitigation order (applies when the constraints above do not fire):**

1. **`kubectl rollout undo`** the workload identified in step 2, if one rollout is clearly implicated and reversible (or revert the implicated ConfigMap / RBAC change).
2. **Feature-flag off** the failing code path, if a flag exists.
3. **Scale** the saturated resource (`kubectl scale` / raise the HPA ceiling / raise `resources.limits`), if the path is capacity-bound and not regression-bound.
4. **Traffic-shift** away from the failing region / cluster / Service version / shard.
5. **Manual intervention** (`kubectl delete pod` to force a fresh restart, kill a stuck Job) as a last resort, with explicit acknowledgement that it does not address cause — pods will recreate from the same broken spec.

If no safe mitigation exists even after applying the above, surface that explicitly and escalate.

### 7. Hand off

Produce a structured handoff for `postmortem-author`. All four elements below are **mandatory** and must appear as labelled sections, even when an element is empty (write "Open questions: none identified", not nothing — a silently missing section reads as "investigation incomplete" to the next responder):

- **Timeline** (T0, key events, mitigation timestamp, Tresolved).
- **Ranked hypotheses** with the evidence supporting each.
- **Mitigation** taken / recommended and observed effect.
- **Open questions** (gaps in signals, unverified assumptions, root-cause threads the mitigation did not close). This section is the most-often dropped and the most valuable to the postmortem: list every unresolved thread explicitly. If the investigation truly left no gaps, say so explicitly rather than omitting the heading.

## Output format

The agent's final message in any invocation must include:

1. **Anchored window**: `T0 = ..., Tnow = ...`.
2. **Change surface**: bulleted list of overlapping changes (rollouts, ConfigMap/Secret, RBAC, HPA/cluster, CronJobs), or "no changes in window".
3. **Classified path**: one of the four, or "outside reference paths" with justification.
4. **Confirming signals**: three or more, each cited with source.
5. **Blast radius**: users + surfaces + business impact.
6. **Recommended mitigation**: ordered, with explicit "do not address cause" notes where applicable.
7. **Handoff payload**: structured for `postmortem-author`, containing all four labelled sections from step 7 — **timeline**, **ranked hypotheses**, **mitigation**, and **open questions**. Do not collapse or omit any of them; an absent "open questions" section is treated as an incomplete handoff.

## Worked examples

Eleven end-to-end examples are committed under `examples/`, each with fixtures and a runnable replay test.

**Reference paths** (one canonical example per path):

- [`examples/01-oom-cascade.md`](./examples/01-oom-cascade.md): OOM in a payments Deployment triggering a retry storm from the API gateway.
- [`examples/02-dns-resolution-failure.md`](./examples/02-dns-resolution-failure.md): CoreDNS `Corefile` ConfigMap misconfiguration causing intermittent `SERVFAIL` for an internal Service.
- [`examples/03-cascading-failure-retry-storm.md`](./examples/03-cascading-failure-retry-storm.md): pure cascade from an upstream DB query-plan slowdown; no rollout in window.
- [`examples/04-deploy-correlator-serialization.md`](./examples/04-deploy-correlator-serialization.md): pure deploy-correlator regression (serialization change breaks downstream parsers).

**Escalation cases** (exercise the FAILURE_MODES.md rules):

- [`examples/05-outside-reference-paths-third-party-rate-limit.md`](./examples/05-outside-reference-paths-third-party-rate-limit.md): a third-party API rate-limits a workload; the methodology escalates rather than force-fitting one of the four paths (M1).
- [`examples/06-ambiguous-t0-slow-burn.md`](./examples/06-ambiguous-t0-slow-burn.md): slow-burn memory leak where T0 is genuinely ambiguous; escalation (M2) recommends re-running with a widened window.
- [`examples/07-blast-radius-asymmetric-revert.md`](./examples/07-blast-radius-asymmetric-revert.md): a rollout bundling six unrelated changes; `rollout undo` is the top mitigation but escalates (M3) because the rollback blast radius exceeds the incident.
- [`examples/08-deploy-correlator-confirmation-bias.md`](./examples/08-deploy-correlator-confirmation-bias.md): a rollout and an RBAC change collide in time; the methodology rejects the deploy-correlator classification (M4 guard) because the rollout diff does not touch the failing surface.

**Edge / boundary cases**:

- [`examples/09-zero-changes-external-cert-expiry.md`](./examples/09-zero-changes-external-cert-expiry.md): zero changes in window, failure is an external partner TLS certificate expiry seen from a cluster workload.
- [`examples/10-multi-region-asymmetry.md`](./examples/10-multi-region-asymmetry.md): same image deployed to two clusters/regions, one fails; the methodology surfaces the per-region asymmetry as a first-class signal.
- [`examples/11-capacity-bound-organic-growth.md`](./examples/11-capacity-bound-organic-growth.md): organic traffic growth saturates capacity; the methodology recommends scaling (HPA) instead of `rollout undo`.

The examples mirror the seven methodology steps so contributors can see the methodology in motion, not just described.

## Replay tests

Every example has a replay test in `tests/` that runs the methodology against committed fixtures, with no external credentials (no live cluster needed). Run from the skill directory:

```bash
for t in tests/replay_*.py; do python "$t" || exit 1; done
```

The 11 tests cover the four reference paths, the FAILURE_MODES.md escalation rules (M1, M2, M3, M4), and the edge cases (zero changes, multi-region asymmetry, capacity saturation). Tests exit non-zero if the methodology produces the wrong classification, mitigation, or escalation against known-good fixtures. See [`tests/README.md`](./tests/README.md) for the fixture schema and how to add a new replay test.

## Failure modes

This skill is wrong in predictable ways. Read [`FAILURE_MODES.md`](./FAILURE_MODES.md) before relying on it for production triage. Highlights:

- The four reference paths cover most but not all Kubernetes incidents; novel failure shapes get force-fit if the agent does not check step 4 carefully.
- Anchoring on the wrong T0 produces a confidently wrong change-surface bisection.
- The mitigation recommendation is not a substitute for a human approver on changes with broad blast radius.

## Anyshift integration (opt-in)

The methodology above runs end-to-end with whatever telemetry, rollout/event source, and RBAC audit log you already have for your cluster (kubectl, the Kubernetes events API, kube-state-metrics, Prometheus). No Anyshift dependency.

The Anyshift MCP can act as a context primer for step 2 (change surface) by exposing a versioned resource graph that links rollouts, RBAC changes, and cluster/infrastructure changes to the specific Kubernetes resources implicated in the incident. See the per-skill README for the measured "with vs without" delta on the OOM and DNS examples (published once the integration has been exercised against the replay tests).
