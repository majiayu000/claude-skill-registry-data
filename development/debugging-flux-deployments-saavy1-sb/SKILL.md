---
name: debugging-flux-deployments
description: Diagnoses and resolves issues with Flux GitOps deployments, Kubernetes pods, services, and HelmReleases in the Superbloom cluster
---

# Debugging Flux Deployments

This skill provides systematic approaches to diagnose and fix deployment issues in the Superbloom K3s cluster.

## Capabilities

- Diagnose pod startup failures
- Debug empty service endpoints
- Troubleshoot HelmRelease errors
- Fix SOPS decryption issues
- Resolve certificate/ingress problems
- Identify RBAC permission issues

## Diagnostic Flow

```
1. Check Flux sync status
2. Check HelmRelease status
3. Check Pod status
4. Check Service endpoints
5. Check container logs
6. Test internal connectivity
```

## Essential Commands

### Flux Status
```bash
# Check all Flux resources
flux get all -A

# Check specific kustomization
flux get kustomization flux-system -n flux-system

# Force reconciliation
flux reconcile kustomization flux-system --with-source

# Check GitRepository
flux get source git -A
```

### HelmRelease Status
```bash
# List all HelmReleases
kubectl get helmrelease -A

# Detailed status
kubectl describe helmrelease <name> -n <namespace>

# Force HelmRelease reconciliation
flux reconcile helmrelease <name> -n <namespace>
```

### Pod Diagnostics
```bash
# List pods with status
kubectl get pods -n <namespace>

# Detailed pod info
kubectl describe pod <pod-name> -n <namespace>

# Container logs
kubectl logs -n <namespace> <pod-name> -c <container-name>

# All containers
kubectl logs -n <namespace> <pod-name> --all-containers

# Previous crashed container
kubectl logs -n <namespace> <pod-name> -c <container> --previous
```

### Service/Endpoint Check
```bash
# Check service
kubectl get svc -n <namespace>

# Check endpoints (empty = no healthy pods)
kubectl get endpoints <service-name> -n <namespace>

# Test internal connectivity
kubectl run curl-test --rm -it --restart=Never --image=curlimages/curl -- \
  curl -s http://<service>.<namespace>.svc.cluster.local:<port>/health
```

### Secret Verification
```bash
# Check secret exists
kubectl get secret <name> -n <namespace>

# View secret data (base64 decoded)
kubectl get secret <name> -n <namespace> -o jsonpath='{.data.<key>}' | base64 -d

# SOPS decrypt locally
cd flux && sops -d clusters/superbloom/apps/<app>/secrets.yaml
```

## Common Issues & Solutions

### Pod CrashLoopBackOff

**Symptom**: Pod shows `CrashLoopBackOff`, `1/2 Ready`

**Diagnosis**:
```bash
kubectl describe pod <pod> -n <namespace> | tail -30
kubectl logs -n <namespace> <pod> -c <container>
```

**Common causes**:
- Missing RBAC permissions (Tailscale sidecar)
- Missing environment variables
- Failed health probes
- Image pull errors

**Tailscale fix**: Add RBAC for secrets management:
```yaml
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get", "create", "update", "patch"]
```

### Empty Service Endpoints

**Symptom**: Service has no endpoints, traffic fails

**Diagnosis**:
```bash
kubectl get endpoints <svc> -n <namespace>
kubectl get pods -n <namespace> -o wide
```

**Cause**: Pod not "Ready" (all containers must pass readiness probes)

**Fix**: Ensure all containers are healthy. If sidecar failing, fix that first.

### HelmRelease Schema Validation Error

**Symptom**: `values don't meet the specifications of the schema`

**Example error**:
```
at '/serviceAccount/name': got string, want object
```

**Cause**: bjw-s app-template v4 schema mismatch

**Fix for serviceAccount**: Move inside controller:
```yaml
controllers:
  main:
    serviceAccount:        # CORRECT - inside controllers.main
      name: my-app
    containers:
      main:
        ...
```

NOT at top level:
```yaml
serviceAccount:           # WRONG - top level
  name: my-app
```

### SOPS Decryption Failure

**Symptom**: Flux can't decrypt secrets

**Diagnosis**:
```bash
# Check sops-age secret exists
kubectl get secret sops-age -n flux-system

# Test local decryption
cd flux && sops -d clusters/superbloom/apps/<app>/secrets.yaml
```

**Fixes**:
- Ensure `.sops.yaml` path_regex matches file location
- Verify age key is available locally and in cluster

### Certificate/ACME Failures

**Symptom**: 521 errors, certificate not issued

**Diagnosis**:
```bash
kubectl logs -n caddy-system -l app=caddy --tail=50
```

**Common causes**:
- Domain not in DDNS → Add to DOMAINS list
- Rate limited → Wait 1 hour
- Origin unreachable → Check Cloudflare proxy settings

**Fix**:
```bash
# Add domain to DDNS
sops -d flux/clusters/superbloom/infra/ddns/secrets.yaml
# Add to DOMAINS, re-encrypt

# Restart DDNS and Caddy
kubectl rollout restart deployment ddns -n ddns
kubectl rollout restart deployment caddy -n caddy-system
```

### Image Pull Errors

**Symptom**: `ImagePullBackOff`, `ErrImagePull`

**Diagnosis**:
```bash
kubectl describe pod <pod> -n <namespace> | grep -A5 "Events"
```

**Fixes**:
- Check image exists in GHCR
- Verify image tag is correct
- Check imagePullSecrets if private registry

### Exec Format Error (Corrupted Image Cache)

**Symptom**: Container crashes with `exec /usr/local/bin/<binary>: exec format error`

**Cause**: Containerd cached a wrong-architecture image (common with multi-arch `latest` tags)

**Diagnosis**:
```bash
kubectl logs -n <namespace> <pod> -c <container>
# Shows "exec format error"

# Check cached images
ssh superbloom "sudo ctr --address /run/k3s/containerd/containerd.sock -n k8s.io images ls | grep <image>"
```

**Fix**: Remove corrupted image from containerd cache:
```bash
ssh superbloom "sudo ctr --address /run/k3s/containerd/containerd.sock -n k8s.io images rm <image>:<tag>"

# Delete pods to force fresh pull
kubectl delete pod -n <namespace> -l app.kubernetes.io/instance=<app>
```

**Prevention**: Pin to specific version tags instead of `latest` for sidecars like Tailscale.

### Container Exits Immediately (Exit Code 0)

**Symptom**: Container shows `Completed` with exit code 0, restarts in CrashLoopBackOff

**Cause**: Often a Docker build issue - source files are empty (0 bytes)

**Diagnosis**:
```bash
# Check file sizes in image
kubectl run debug --rm -it --image=<image>:<tag> -- ls -la /app/src/
# If files show 0 bytes, the build is broken
```

**Fix**: Rebuild with cache disabled:
```yaml
# In .github/workflows/<app>.yml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    no-cache: true  # Temporarily disable cache
```

After successful rebuild, re-enable caching.

## Useful Patterns

### Watch Resources
```bash
# Watch pods
kubectl get pods -n <namespace> -w

# Watch events
kubectl get events -n <namespace> -w --sort-by='.lastTimestamp'
```

### Exec Into Container
```bash
kubectl exec -it -n <namespace> <pod> -c <container> -- /bin/sh
```

### Port Forward for Testing
```bash
kubectl port-forward -n <namespace> svc/<service> 8080:3000
curl http://localhost:8080/health
```

### Delete and Recreate HelmRelease
```bash
# Sometimes needed to clear stuck state
kubectl delete helmrelease <name> -n <namespace>
flux reconcile kustomization flux-system --with-source
```

## Best Practices

1. Always check Flux sync status first
2. Read HelmRelease events for schema errors
3. Empty endpoints = pod not Ready
4. Check ALL container logs in multi-container pods
5. Test internal connectivity before debugging ingress
6. Rate limits require waiting, not repeated attempts
