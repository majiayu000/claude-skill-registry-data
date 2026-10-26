---
name: kubernetes
description: Use when deploying services to Kubernetes — starting with a local cluster (kind or k3d), writing Deployments, Services, ConfigMaps and probes, resource requests and limits, rolling updates, debugging pods, and deciding whether a managed cluster (EKS, AKS, GKE) is worth its cost. Also use when a pod is in CrashLoopBackOff, a Service has no endpoints, or manifests work locally but not in a cloud cluster.
---

# Kubernetes

Default: learn and test on a local cluster (kind or k3d) first, plain YAML manifests (add Kustomize for environments), one namespace per app, probes and resource requests on every container, a managed cluster only after estimating its monthly cost.

## Local cluster

```bash
kind create cluster --name dev
docker build -t app:dev . && kind load docker-image app:dev --name dev
kubectl apply -k k8s/overlays/dev
kubectl -n app get pods -w
```

`kind load` puts a local image into the cluster; without it, `imagePullPolicy` and a non-existent registry cause `ErrImagePull`.

## Minimal manifest set

- **Deployment** with `replicas`, labels that match the Service selector, `readinessProbe` and `livenessProbe` (different endpoints or thresholds), `resources.requests` and `limits`.
- **Service** (`ClusterIP`) selecting the pods; an **Ingress** or `kubectl port-forward` to reach it.
- **ConfigMap** for settings, **Secret** for credentials (created from the environment, not committed).
- Run as non-root (`securityContext.runAsNonRoot: true`) with a read-only root filesystem where possible.

## Rolling updates

- Change the image tag (immutable tags, not `latest`) and `kubectl apply`; watch `kubectl rollout status deploy/app`.
- Readiness gates traffic; a missing readiness probe sends requests to pods that are still starting.
- `kubectl rollout undo` for a quick rollback.

## Debugging order

1. `kubectl get pods` → status (`Pending`, `CrashLoopBackOff`, `ImagePullBackOff`).
2. `kubectl describe pod` → events (scheduling, image pulls, probe failures, OOMKilled).
3. `kubectl logs pod [-p]` → application output (`-p` for the previous crashed container).
4. `kubectl get endpoints svc` → empty means the selector does not match pod labels or pods are not ready.
5. `kubectl exec -it pod -- sh` to test DNS and connectivity from inside.

## Managed clusters

- Estimate before creating: control-plane fee (varies by provider), nodes, load balancers, storage and egress. A small always-on cluster costs real money every month even when idle.
- Create budgets and alerts first; tear down test clusters the same day; keep the cluster definition in Terraform so it can be recreated.

## Verification loop

1. `kubectl apply --dry-run=server -k ...` validates against the API.
2. Pods become Ready; `rollout status` succeeds.
3. A smoke request through the Service or Ingress returns the expected response.
4. Delete and re-apply from scratch to prove the manifests are complete.

## Pitfalls

- **Limits without requests** set requests equal to limits; too-low memory limits cause OOMKilled loops.
- **Liveness probes that are too aggressive** restart healthy but slow pods; give a startup probe to slow starters.
- **Selectors are immutable** on Deployments; changing labels later means recreating the Deployment.
- **`latest` tags** make rollouts and rollbacks unpredictable.
- **Local-only assumptions** (host paths, `kind load`) do not exist in cloud clusters; push images to a registry the cluster can pull from.
