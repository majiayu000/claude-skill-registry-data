---
name: deploying-public-apps
description: Deploys public-facing apps that handle their own authentication (like Jellyfin, game servers) without Authelia forward auth
---

# Deploying Public-Facing Apps

For apps that handle their own auth (Jellyfin, Minecraft, etc.) and don't need Authelia forward auth.

## Checklist

When deploying a new public-facing app, complete these steps:

1. [ ] Create app manifests in `flux/clusters/superbloom/apps/<app>/`
2. [ ] Add app to `flux/clusters/superbloom/apps/kustomization.yaml`
3. [ ] Add domain to DDNS in `flux/clusters/superbloom/infra/ddns/release.yaml`
4. [ ] Add Caddy route in `flux/clusters/superbloom/infra/caddy/caddyfile.yaml`
5. [ ] Commit, push, and reconcile Flux

## 1. App Manifests

Create `flux/clusters/superbloom/apps/<app>/`:

### kustomization.yaml
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: <app>
resources:
  - ns.yaml
  - release.yaml
```

### ns.yaml
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: <app>
```

### release.yaml
```yaml
apiVersion: helm.toolkit.fluxcd.io/v2
kind: HelmRelease
metadata:
  name: <app>
  namespace: <app>
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
  values:
    controllers:
      main:
        containers:
          main:
            image:
              repository: <image>
              tag: latest
            env:
              TZ: America/Denver
            probes:
              liveness:
                enabled: true
                # ... probe config
    service:
      main:
        controller: main
        ports:
          http:
            port: <port>
    persistence:
      # ... as needed
```

## 2. Add to Apps Kustomization

Edit `flux/clusters/superbloom/apps/kustomization.yaml`:
```yaml
resources:
  - ...existing...
  - <app>/
```

## 3. Add Domain to DDNS

Edit `flux/clusters/superbloom/infra/ddns/release.yaml`:
```yaml
env:
  DOMAINS: saavylab.dev,...existing...,<subdomain>.saavylab.dev
```

## 4. Add Caddy Route (NO forward_auth)

Edit `flux/clusters/superbloom/infra/caddy/caddyfile.yaml`:
```yaml
data:
  Caddyfile: |
    # <App> - no forward_auth (handles own auth)
    <subdomain>.saavylab.dev {
        reverse_proxy <app>.<app>.svc.cluster.local:<port>
    }
```

**Key difference from internal services:** No `forward_auth` block. The app handles its own authentication.

## 5. Deploy

```bash
cd ~/dev/sb
git add -A && git commit -m "Add <app> at <subdomain>.saavylab.dev"
git push

# Reconcile
flux reconcile kustomization flux-system --with-source

# Watch deployment
kubectl get pods -n <app> -w
```

## Examples

### Jellyfin (Media Server)
- URL: `watch.saavylab.dev`
- Port: 8096
- Auth: Built-in (easier for TVs, Xbox, etc.)
- Special: GPU passthrough via `/dev/dri` hostPath

### Minecraft (Game Server)
- URL: `mc.saavylab.dev`
- Port: 25565
- Auth: Mojang/Microsoft accounts
- Special: Uses LoadBalancer service, not Caddy

## Common Patterns

### GPU Passthrough
```yaml
persistence:
  dri:
    enabled: true
    type: hostPath
    hostPath: /dev/dri
    globalMounts:
      - path: /dev/dri
```
Requires `securityContext.privileged: true` on the container.

### Host Storage (ZFS Pool)
```yaml
persistence:
  media:
    enabled: true
    type: hostPath
    hostPath: /tank/media
    globalMounts:
      - path: /media
        readOnly: true  # if app only reads
```

### NVMe Storage (Fast Cache)
```yaml
persistence:
  cache:
    enabled: true
    type: persistentVolumeClaim
    accessMode: ReadWriteOnce
    size: 50Gi
    storageClass: local-path  # provisions on NVMe root
    globalMounts:
      - path: /cache
```

## Post-Deploy: Certificate Provisioning

After adding a new domain, **restart Caddy** so it provisions the TLS certificate:

```bash
# Restart Caddy to trigger cert provisioning
kubectl rollout restart deployment/caddy -n caddy-system

# Watch logs for certificate acquisition
kubectl logs deployment/caddy -n caddy-system -f | grep -E "(obtain|certificate|watch)"
```

If cert fails with 520 error:
1. Check DDNS logs: `kubectl logs deployment/ddns -n ddns`
2. Verify DNS points to correct IP: `dig +short <subdomain>.saavylab.dev`
3. Restart DDNS if needed: `kubectl rollout restart deployment/ddns -n ddns`

## Debugging

```bash
# Check pod status
kubectl get pods -n <app>

# Check logs
kubectl logs -n <app> -l app.kubernetes.io/name=<app>

# Check service endpoints
kubectl get endpoints -n <app>

# Check HelmRelease status
kubectl get helmrelease -n <app>
flux logs --kind=HelmRelease --name=<app> -n <app>

# Test internal connectivity
kubectl run -it --rm debug --image=curlimages/curl -- curl http://<app>.<app>.svc.cluster.local:<port>/health
```

## Why No Authelia?

Some apps need direct access without SSO:
- **Smart TVs / Streaming devices** - Can't handle browser redirects
- **Game consoles** - Xbox, PlayStation native apps
- **Mobile apps** - Native Jellyfin/Plex apps
- **Game clients** - Minecraft, etc.

These apps have their own auth mechanisms (app logins, Mojang accounts, etc.) that work better for their use case.
