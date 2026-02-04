---
name: deploying-k8s-services
description: Deploys new containerized services to the Superbloom K3s cluster using Flux GitOps with bjw-s app-template, Authelia forward auth, Caddy reverse proxy, and DDNS
---

# Deploying Kubernetes Services

This skill provides step-by-step guidance for deploying new services to the Superbloom K3s cluster using GitOps.

## Capabilities

- Create Flux manifests for new services (namespace, HelmRelease, secrets)
- Configure bjw-s app-template v4 Helm values correctly
- Set up Authelia forward authentication
- Configure Caddy reverse proxy routing
- Add domains to Cloudflare DDNS
- Set up RBAC for sidecars (e.g., Tailscale)
- Encrypt secrets with SOPS

## Architecture

```
Internet → Cloudflare → Caddy (LoadBalancer) → forward_auth (Authelia) → Service → Pod
                              ↓
                         DDNS updates Cloudflare DNS
```

## Required Files

Create in `flux/clusters/superbloom/apps/<app-name>/`:

### ns.yaml
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: <app-name>
```

### kustomization.yaml
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ns.yaml
  - rbac.yaml      # if using Tailscale or K8s API access
  - release.yaml
  - secrets.yaml
```

### release.yaml
```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: <app-name>
  namespace: <app-name>
spec:
  interval: 5m
  chart:
    spec:
      chart: app-template
      version: "4.1.1"
      sourceRef:
        kind: HelmRepository
        name: bjw-s
        namespace: flux-system
  valuesFrom:
    - kind: Secret
      name: <app-name>-secrets
      valuesKey: values.yaml
```

### secrets.yaml (SOPS encrypted)

**CRITICAL**: In app-template v4, `serviceAccount` goes inside `controllers.<name>.serviceAccount`, NOT at top level.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <app-name>-secrets
  namespace: <app-name>
type: Opaque
stringData:
  values.yaml: |
    controllers:
      main:
        serviceAccount:
          name: <app-name>    # MUST be inside controllers.main
        containers:
          main:
            image:
              repository: ghcr.io/saavy1/<app-name>
              tag: latest
            env:
              PORT: "3000"
            probes:
              liveness:
                enabled: true
                custom: true
                spec:
                  httpGet:
                    path: /health
                    port: 3000
              readiness:
                enabled: true
                custom: true
                spec:
                  httpGet:
                    path: /health
                    port: 3000
    service:
      main:
        controller: main
        ports:
          http:
            port: 3000
```

### rbac.yaml (for Tailscale sidecar)
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: <app-name>
  namespace: <app-name>
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: <app-name>
  namespace: <app-name>
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get", "create", "update", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: <app-name>
  namespace: <app-name>
subjects:
  - kind: ServiceAccount
    name: <app-name>
    namespace: <app-name>
roleRef:
  kind: Role
  name: <app-name>
  apiGroup: rbac.authorization.k8s.io
```

## Caddy Configuration

Add to `flux/clusters/superbloom/infra/caddy/caddyfile.yaml`:

```yaml
<app-name>.saavylab.dev {
    forward_auth authelia.authelia.svc.cluster.local:9091 {
        uri /api/authz/forward-auth
        copy_headers Remote-User Remote-Groups Remote-Email Remote-Name
    }
    reverse_proxy <app-name>.<app-name>.svc.cluster.local:3000
}
```

## DDNS Configuration

Add domain to `flux/clusters/superbloom/infra/ddns/secrets.yaml` DOMAINS field:
```
DOMAINS: saavylab.dev,mc.saavylab.dev,auth.saavylab.dev,nexus.saavylab.dev,<app-name>.saavylab.dev
```

## SOPS Encryption

```bash
cd flux
sops --encrypt --in-place clusters/superbloom/apps/<app-name>/secrets.yaml
```

## Deployment Commands

```bash
git add -A && git commit -m "feat: add <app-name> service" && git push
flux reconcile kustomization flux-system --with-source
kubectl rollout restart deployment ddns -n ddns
kubectl rollout restart deployment caddy -n caddy-system
```

## Debugging Commands

```bash
kubectl get pods -n <app-name>
kubectl get endpoints <app-name> -n <app-name>
kubectl get helmrelease -n <app-name>
kubectl describe helmrelease <app-name> -n <app-name>
kubectl logs -n <app-name> -l app.kubernetes.io/name=<app-name> --all-containers
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Pod 1/2 Ready | Sidecar crashing | Add RBAC, check TS_KUBE_SECRET |
| Empty endpoints | Pod not Ready | All containers must pass probes |
| Schema validation error | Wrong values structure | serviceAccount inside controllers.main |
| 521 from Cloudflare | DNS not updated | Add domain to DDNS |
| ACME rate limit | Failed cert attempts | Wait 1 hour |

## Tailscale Sidecar

For services needing Tailscale network access, add to containers:

```yaml
tailscale:
  image:
    repository: ghcr.io/tailscale/tailscale
    tag: latest
  env:
    TS_AUTHKEY: "tskey-auth-..."
    TS_HOSTNAME: <app-name>
    TS_STATE_DIR: /var/lib/tailscale
    TS_USERSPACE: "true"
    TS_KUBE_SECRET: <app-name>-tailscale
  securityContext:
    runAsUser: 0
    runAsGroup: 0
```

Requires RBAC for secrets management.
