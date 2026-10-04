---
name: do-kubernetes
version: 1.0.0
description: Author or debug Kubernetes manifests with distinct probes, right-sized resources, autoscaling, and safe reversible rollouts.
author: matrixx0070
tags: [kubernetes, k8s, devops, orchestration, scaling, probes]
capabilities: []
---

# do-kubernetes

## When to use

You need to write a Deployment/Service/Ingress set, debug a CrashLoopBackOff or pending pod, add autoscaling, or make a rollout safe and reversible.

**Not for:** building the container image (use do-dockerfile), provisioning the cluster or cloud resources (use do-terraform), or defining alerts and SLOs on the workload (use do-observability).

## Method

1. Pick the workload shape. Decision: stateless -> Deployment; needs stable identity/storage -> StatefulSet; run-to-completion -> Job/CronJob. Set replicas and a RollingUpdate strategy with maxUnavailable/maxSurge tuned to spare capacity.
2. Configure the three probes distinctly: startup (covers slow boot), readiness (gates traffic), liveness (restarts a wedged pod). Decision: if a slow start triggers restarts, raise the startup probe budget — do not loosen liveness.
3. Set requests and limits on every container. Requests drive scheduling and HPA; limits prevent noisy neighbors. Decision: omit CPU limits on latency-sensitive services to avoid throttling; keep memory limits to prevent OOM of neighbors.
4. Add an HPA (or KEDA) keyed on CPU/memory or a custom metric, with sane min/max and a stabilization window.
5. Externalize config via ConfigMap/Secret, mount rather than bake, and set a securityContext (non-root, drop capabilities, readOnlyRootFilesystem).
6. To debug: `kubectl describe` for events, `logs --previous` for crashes; check probe failures, image-pull errors, and resource pressure before editing.

## Example

```yaml
spec:
  containers:
    - name: api
      image: registry/api@sha256:...
      resources:
        requests: { cpu: 100m, memory: 128Mi }   # scheduling + HPA
        limits:   { memory: 256Mi }              # no CPU limit: avoid throttle
      startupProbe:                              # slow boot gets 30x5s = 150s
        httpGet: { path: /healthz, port: 8080 }
        failureThreshold: 30
        periodSeconds: 5
      readinessProbe:                            # gate traffic
        httpGet: { path: /ready, port: 8080 }
      livenessProbe:                             # restart if wedged
        httpGet: { path: /healthz, port: 8080 }
        periodSeconds: 10
```

## Pitfalls

- One endpoint reused for liveness and readiness, so a dependency blip restarts healthy pods instead of just draining traffic.
- No resource requests — the scheduler bin-packs blindly and the HPA has no baseline to scale against.
- A liveness probe that fires during slow startup, producing a CrashLoopBackOff that looks like an app bug.
- CPU limits on a latency-sensitive service, causing throttling that reads as intermittent slowness.

## Output format

```
Manifests: Deployment, Service, HPA, Ingress (as needed), valid YAML.

Probe/resource table per container:
| container | startup | readiness | liveness | cpu req | mem req/limit |

Rollout:  kubectl rollout status deploy/<name>
Rollback: kubectl rollout undo deploy/<name>
Debug findings: likely root cause + evidence (event, log line).
```
