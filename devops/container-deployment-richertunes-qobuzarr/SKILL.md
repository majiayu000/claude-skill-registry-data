---
name: container-deployment
description: Containerize Qobuzarr plugin and automate deployments. Use when working with Docker images, container registries, deployment automation, or orchestration. Critical for establishing containerization from scratch.
---
<!-- docval:ignore-workflow-refs -->

# Container & Deployment Engineer

## Mission
Design and implement complete containerization and deployment infrastructure for Qobuzarr, enabling easy distribution and automated deployments.

## Current Status
- **Containerization**: ❌ CRITICAL GAP - No Docker images
- **Deployment**: ⚠️ Manual ZIP extraction only
- **Orchestration**: ❌ No Kubernetes/Helm
- **IaC**: ⚠️ Documentation examples only

## Key Deliverables Needed
1. Dockerfile for Lidarr + Qobuzarr image
2. Container build workflow in CI
3. GHCR publishing automation
4. Multi-arch support (amd64, arm64)
5. Docker Compose for easy deployment
6. Helm chart for Kubernetes

## Implementation Priority

### Phase 1: Basic Images (HIGH)
```dockerfile
FROM ghcr.io/hotio/lidarr:pr-plugins-3.1.2.4913
COPY artifacts/plugin/ /config/plugins/RicherTunes/Qobuzarr/
HEALTHCHECK CMD curl -f http://localhost:8686/ping || exit 1
```

### Phase 2: CI Integration (HIGH)
```yaml
# Add to .github/workflows/release.yml
- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    platforms: linux/amd64,linux/arm64
    push: true
    tags: ghcr.io/richertunes/qobuzarr:${{ env.VERSION }}
```

### Phase 3: Orchestration (MEDIUM)
- Create Helm chart
- Add Kubernetes manifests
- Document deployment strategies

## Related Skills
- `release-automation` - Integrate container builds
- `deployment-manager` - Automate deployments
