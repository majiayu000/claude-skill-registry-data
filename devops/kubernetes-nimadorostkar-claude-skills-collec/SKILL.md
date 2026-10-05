---
name: kubernetes
description: Use when deploying to or debugging Kubernetes. Covers workload configuration, resource requests and limits, probes, rollout strategy, networking, and the failure modes that produce CrashLoopBackOff and OOMKilled.
metadata:
  category: devops
  version: 1.0.0
  tags: [kubernetes, k8s, containers, deployment, debugging]
---

# Kubernetes

## Purpose

Deploy workloads that survive node failures, scale predictably, and fail visibly. Most Kubernetes incidents trace back to three things: wrong resource limits, wrong probes, and a rollout that had no way to be judged healthy.

## When to Use

- Writing or reviewing Kubernetes manifests.
- Debugging a pod that will not start, keeps restarting, or is being evicted.
- Configuring autoscaling, rollouts, or disruption budgets.
- Diagnosing networking or DNS problems inside a cluster.

## Capabilities

- Workload configuration: Deployments, StatefulSets, Jobs, CronJobs.
- Resource requests, limits, and quality-of-service classes.
- Liveness, readiness, and startup probes.
- Rollout strategies, `PodDisruptionBudget`, and graceful shutdown.
- Networking: Services, Ingress, NetworkPolicy, cluster DNS.
- Debugging: events, logs, ephemeral containers.

## Inputs

- The workload, its resource profile, and its startup behavior.
- The cluster's constraints: node sizes, available classes, policies.
- The symptom, if debugging: pod status, events, exit code.

## Outputs

- Manifests with explicit requests, limits, and probes.
- A rollout that is safe under disruption.
- A root cause with the evidence that identified it.

## Workflow

1. **Set requests and limits deliberately** — Requests determine scheduling; limits determine throttling and killing. A pod with no requests is scheduled anywhere and evicted first.
2. **Configure the three probes distinctly** — Startup probe protects a slow boot. Readiness controls traffic. Liveness restarts a hung process. Conflating them causes a slow-starting pod to be killed forever.
3. **Handle SIGTERM** — Kubernetes sends SIGTERM, waits `terminationGracePeriodSeconds`, then SIGKILL. A process that ignores SIGTERM drops in-flight requests on every deploy.
4. **Protect the rollout** — `maxUnavailable`, `maxSurge`, and a `PodDisruptionBudget` so a node drain cannot take the last replica.
5. **Debug from the events** — `kubectl describe pod` before `kubectl logs`. The reason is usually in the events, not the application output.

## Best Practices

- A CPU limit throttles; a memory limit kills. Setting a CPU limit equal to the request wastes burst capacity for no reliability gain — in most cases, set CPU requests and omit CPU limits.
- Memory limits should be set. Without one, a leaking pod takes the whole node with it.
- A liveness probe that hits a dependency will restart your pod when the *dependency* is down, converting a partial outage into a total one. Liveness checks the process; readiness checks the dependencies.
- `imagePullPolicy: Always` with a `:latest` tag makes rollbacks impossible. Pin an immutable digest or a version tag.
- Never store secrets in a ConfigMap. Use a Secret, and preferably an external secret store.
- `kubectl exec` into a distroless container will fail. Use `kubectl debug` with an ephemeral container.

## Examples

**A Deployment with correct probes and graceful shutdown:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
spec:
  replicas: 3
  strategy:
    rollingUpdate: { maxSurge: 1, maxUnavailable: 0 }   # never dip below capacity
  template:
    spec:
      terminationGracePeriodSeconds: 45                 # > the longest in-flight request
      containers:
        - name: api
          image: registry.example.com/orders-api@sha256:9f2c...   # immutable
          resources:
            requests: { cpu: 250m, memory: 512Mi }       # scheduling
            limits:   { memory: 1Gi }                    # OOM ceiling; no CPU limit
          startupProbe:                                  # allows up to 60s to boot
            httpGet: { path: /healthz, port: 8080 }
            failureThreshold: 30
            periodSeconds: 2
          readinessProbe:                                # gates traffic; checks deps
            httpGet: { path: /readyz, port: 8080 }
            periodSeconds: 5
          livenessProbe:                                 # restarts a hung process only
            httpGet: { path: /healthz, port: 8080 }
            periodSeconds: 10
            failureThreshold: 3
          lifecycle:
            preStop:
              exec:
                command: ["sleep", "10"]                 # let the LB deregister first
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: orders-api
spec:
  minAvailable: 2
  selector:
    matchLabels: { app: orders-api }
```

**Diagnosing the standard failures:**

```bash
kubectl describe pod orders-api-7d4f -n prod | sed -n '/Events/,$p'
# OOMKilled       -> memory limit too low, or a leak. Check actual usage, then raise or fix.
# CrashLoopBackOff-> read the previous container's logs: kubectl logs --previous
# ImagePullBackOff-> registry auth or a tag that does not exist
# Pending         -> no node satisfies the requests; check `kubectl describe node`
```

## Notes

- The `preStop` sleep is not superstition: the endpoint removal and the SIGTERM race each other. Sleeping for a few seconds lets the load balancer stop sending traffic before the process starts shutting down.
- `readinessProbe` failing removes the pod from the Service but does not restart it — which is exactly right when a dependency is temporarily unavailable.
- Vertical Pod Autoscaler in recommendation mode is the fastest way to discover what your requests should actually be, without letting it change them for you.
