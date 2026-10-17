---
name: argocd
description: >
  ArgoCD GitOps operations: Application and ApplicationSet management,
  sync waves, health checks, and best practices for K3s homelab clusters.
license: MIT
compatibility:
  - opencode
metadata:
  author: dotfiles
  tags: [kubernetes, argocd, gitops, helm, cd]
---

# ArgoCD Skill

## Cluster Context

ArgoCD runs on a multi-node K3s cluster (ARM64 Raspberry Pi CM4).

Helm release: `argocd` in namespace `argocd`
Chart version pinned in: `roles/install-argocd/defaults/main.yml`
Chart: `argo/argo-cd` v9.4.17 (ArgoCD v3.3.6)

### Current state

ArgoCD is exposed via `type: ClusterIP` + `HTTPRoute` on the shared Cilium Gateway.

Admin password: `kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d`

URL: `https://argocd.cluster.home`

Key Helm config:
- `dex.enabled: false` — no SSO (single-user homelab)
- `server.insecure: true` — plain HTTP (TLS terminated at Gateway)
- `redis-ha.enabled: false` — single-node
- `server.service.type: ClusterIP`

### ARM64 CM4: repo-server probe tuning

The `argocd-repo-server` does Redis+GPG+git init on startup and its
`/healthz?full=true` endpoint takes 2-3 seconds on CM4 hardware.
Default liveness probe timeout was 1s → constant CrashLoopBackOff.

Fixed probes:
```yaml
repoServer:
  livenessProbe:
    initialDelaySeconds: 30
    periodSeconds: 15
    timeoutSeconds: 5
    failureThreshold: 3
  readinessProbe:
    initialDelaySeconds: 15
    periodSeconds: 10
    timeoutSeconds: 5
    failureThreshold: 3
```

HTTPRoute (HTTP):
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: argocd-http
  namespace: argocd
spec:
  parentRefs:
    - name: cluster-gateway
      namespace: gateway
  hostnames:
    - "argocd.cluster.home"
  rules:
    - backendRefs:
        - name: argocd-server
          port: 80
```

GRPCRoute (CLI uses gRPC — required for `argocd` CLI):
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GRPCRoute
metadata:
  name: argocd-grpc
  namespace: argocd
spec:
  parentRefs:
    - name: cluster-gateway
      namespace: gateway
  hostnames:
    - "argocd.cluster.home"
  rules:
    - backendRefs:
        - name: argocd-server
          port: 80
```

> **Note:** `BackendTLSPolicy` is in the ArgoCD chart but **Cilium does not
> support it yet**. Do not configure `BackendTLSPolicy` — it will be silently
> ignored or cause issues.

> **Note:** `GRPCRoute` support was confirmed in `argo/argo-cd` chart v9.4.17.

## GitOps Pattern for this Cluster

```
~/projects/infra/
└── apps/                        ← ArgoCD Application manifests (future)
    ├── argocd-apps/             ← App-of-apps or ApplicationSets
    └── <service>/
        └── application.yaml
```

Store Application manifests in Git — never create them through the UI.
Use **app-of-apps** or **ApplicationSet** to avoid managing many Application resources.

## Creating an Application

Minimal Application manifest:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/villadalmine/infra
    targetRevision: main
    path: apps/my-app
  destination:
    server: https://kubernetes.default.svc
    namespace: my-app
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## ApplicationSet (preferred for multiple apps)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-apps
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: https://github.com/villadalmine/infra
        revision: main
        directories:
          - path: apps/*
  template:
    metadata:
      name: '{{path.basename}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/villadalmine/infra
        targetRevision: main
        path: '{{path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{path.basename}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

## Sync Waves (ordered deploys)

Use `argocd.argoproj.io/sync-wave` annotation to control order within an Application:
```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "1"   # lower = earlier
```

Typical wave order:
- Wave -1: Namespaces, CRDs
- Wave 0: Secrets, ConfigMaps
- Wave 1: Deployments, StatefulSets
- Wave 2: Jobs, post-deploy checks

## Health Check

```bash
# All ArgoCD pods
kubectl get pods -n argocd

# All Applications and their sync status
kubectl get applications -n argocd

# App details
kubectl describe application <name> -n argocd

# Trigger manual sync
kubectl patch application <name> -n argocd \
  --type merge -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{}}}'

# Check current service type
kubectl get svc argocd-server -n argocd
```

## Troubleshooting

### repo-server CrashLoopBackOff on ARM64
→ Health check `/healthz?full=true` takes 2-3s on CM4 but default probe timeout was 1s.
→ Increase `livenessProbe.timeoutSeconds` to 5 and `initialDelaySeconds` to 30.
→ See `roles/install-argocd/tasks/main.yml` for the fix.

### App stuck `OutOfSync` but diff shows nothing
- Check `argocd.argoproj.io/compare-options` annotations
- Helm chart may generate non-deterministic fields (e.g. random tokens) — use `ignoreDifferences`
- `kubectl get application <name> -n argocd -o yaml | grep -A10 ignoreDifferences`

### App `Degraded` / pods not starting
- Check Events: `kubectl describe application <name> -n argocd`
- Check pod status in target namespace: `kubectl get pods -n <namespace>`
- Sync may have succeeded but app health check fails — check health status field

### `ComparisonError` — cannot get resource
- ArgoCD RBAC may lack permission for a CRD — check `argocd-application-controller` ClusterRole
- If CRDs installed after ArgoCD: restart controller `kubectl rollout restart deploy/argocd-application-controller -n argocd`

### UI not reachable at argocd.cluster.home (post-migration)
- Check HTTPRoute: `kubectl get httproute -n argocd`
- Check Gateway: `kubectl get gateway -n gateway`
- Check service is ClusterIP: `kubectl get svc argocd-server -n argocd`
- Check Pi-hole resolves `argocd.cluster.home` → `192.168.178.200`

## Useful Commands

```bash
# Helm values currently deployed
helm get values argocd -n argocd

# Force app refresh (re-read Git without waiting)
kubectl annotate application <name> -n argocd \
  argocd.argoproj.io/refresh=hard --overwrite

# Delete app WITHOUT pruning resources (orphan)
kubectl patch application <name> -n argocd \
  -p '{"metadata":{"finalizers":[]}}' --type merge
kubectl delete application <name> -n argocd

# App-controller logs (sync errors)
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller --tail=100
```
