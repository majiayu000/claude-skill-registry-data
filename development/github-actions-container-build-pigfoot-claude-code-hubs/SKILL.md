---
name: github-actions-container-build
description: Build multi-architecture container images in GitHub Actions. Matrix builds (public repos with native ARM64), QEMU emulation (private repos), or ARM64 larger runners (Team/Enterprise). Uses Podman rootless builds with push-by-digest pattern
---

# GitHub Actions Container Build

Build multi-architecture container images in GitHub Actions using Podman and native ARM64 runners.

## Core Principles

### Choose Your Workflow

**CRITICAL: Ask these questions before generating any workflow.**

**Question 1: Is your GitHub repository public?**
- **Yes** → Use `github-actions-workflow-matrix-build.yml` (free standard ARM64 runners, 10-50x faster)
- **No** → Go to Question 2

**Question 2: Do you have GitHub Team/Enterprise + willing to pay for ARM64 builds?**
- **Yes** → Use ARM64 larger runners (custom setup required, paid per minute)
- **No** → Use `github-actions-workflow-qemu.yml` (free QEMU emulation, slower but works on free tier)

### 1. Push-by-Digest (2025 Best Practice - Default)

Matrix builds use **push-by-digest** pattern:
- Images pushed by digest without intermediate `:amd64/:arm64` tags
- Only tiny digest files (~70 bytes) transfer as artifacts
- Registry stays clean (no tag clutter)
- Same debug experience with `--platform` flag

```yaml
# Build job
- name: Push by digest
  run: |
    podman push \
      --digestfile /tmp/digest \
      localhost/build:${{ matrix.arch }} \
      docker://${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

# Merge job
- name: Create manifest from digests
  run: |
    podman manifest create "$IMAGE:latest"
    podman manifest add "$IMAGE:latest" "docker://$IMAGE@${AMD64_DIGEST}"
    podman manifest add "$IMAGE:latest" "docker://$IMAGE@${ARM64_DIGEST}"
    podman manifest push --all "$IMAGE:latest" "docker://$IMAGE:latest"
```

**Debug specific architecture:**
```bash
podman pull --platform linux/arm64 ghcr.io/OWNER/REPO:latest
```

### 2. Matrix Builds (Public Repos)

**For public repositories** - use GitHub-hosted standard ARM64 runners:
- 10-50x faster builds (native vs. emulation)
- Better reliability and accuracy
- Lower CI costs
- **Completely free for public repos**
- **Not available for private repos**

```yaml
strategy:
  matrix:
    include:
      - arch: amd64
        runner: ubuntu-24.04
      - arch: arm64
        runner: ubuntu-24.04-arm  # Standard ARM64 runner (public repos only)
```

### 3. QEMU Builds (Private Repos - Free Tier)

**For private repositories on free tier** - use QEMU emulation:
- Works on GitHub Free plan
- Slower (10-50x) than native ARM64 runners
- Uses `docker/setup-qemu-action` for ARM64 emulation
- Single-job pattern with `--platform linux/amd64,linux/arm64`

```yaml
runs-on: ubuntu-latest
steps:
  - uses: docker/setup-qemu-action@v3
  - run: podman build --platform linux/amd64,linux/arm64 --manifest ...
```

### 4. Podman Over Docker

Use Podman for container builds:
- Rootless by default (better security)
- No daemon required
- Native multi-arch manifest support
- OCI compliant
- **Must use `podman manifest push --all`** (not `podman push`)
- **Format**: Use OCI (default) for modern registries; use `--format v2s2` only for Quay.io or cross-registry (see references for details)
- **Network**: Use `--network=host` flag for builds to avoid container networking SSL issues on GitHub Actions ubuntu-24.04 (see Troubleshooting section)

### 5. podman-static for Heredoc Support

Ubuntu 24.04's bundled podman (4.9.3) uses buildah 1.33.7 which doesn't support heredoc syntax. Install podman-static for full BuildKit compatibility:

```yaml
- name: Install podman-static
  run: |
    ARCH=$(uname -m)
    if [ "$ARCH" = "x86_64" ]; then
      PODMAN_ARCH="amd64"
    else
      PODMAN_ARCH="arm64"
    fi
    curl -fsSL -o /tmp/podman-linux-${PODMAN_ARCH}.tar.gz \
      https://github.com/mgoltzsche/podman-static/releases/latest/download/podman-linux-${PODMAN_ARCH}.tar.gz
    cd /tmp && tar -xzf podman-linux-${PODMAN_ARCH}.tar.gz
    sudo cp -f podman-linux-${PODMAN_ARCH}/usr/local/bin/* /usr/bin/
    podman system migrate
```

**Important:** Install to `/usr/bin/` (not `/usr/local/bin/`) to avoid AppArmor issues.

## Quick Start

### For Public Repos (Matrix Build)

1. **Copy workflow template**:
   ```bash
   cp assets/github-actions-workflow-matrix-build.yml .github/workflows/build.yml
   ```

2. **Customize Containerfile path**:
   ```yaml
   -f ./Containerfile.python-uv  # or your Containerfile
   ```

3. **Add your Containerfile** (see **secure-container-build** plugin for templates)

### For Private Repos (QEMU)

1. **Copy workflow template**:
   ```bash
   cp assets/github-actions-workflow-qemu.yml .github/workflows/build.yml
   ```

2. Follow steps 2-3 from above.

## Workflow Structure

### Matrix Build Workflow (Push-by-Digest)

1. **Build job** (matrix): Build and push images by digest on native runners
2. **Merge job**: Download digests, create and push multi-arch manifest

### QEMU Workflow

1. **Single job**: Build multi-arch manifest directly with `--platform` flag

## Multi-arch Build Approaches

| Approach | Artifact Size | Registry Overhead | Best For |
|----------|---------------|-------------------|----------|
| **Push-by-digest** (default) | ~70 bytes | 1x | Production |
| **Architecture tags** | None | 2x (tags + manifest) | Debugging |
| **OCI artifacts** | Full images | 3x | Maximum privacy |

See `references/github-actions-best-practices.md` for detailed comparison.

## ARM64 Larger Runners (Private Repos with Team/Enterprise)

**For private repositories with GitHub Team or Enterprise Cloud plans:**

Standard ARM64 runners (`ubuntu-24.04-arm`) don't work in private repos. Instead, create **ARM64 larger runners**:

**Setup steps:**
1. Go to **Organization Settings → Actions → Runners → New runner**
2. Select **"Larger runners"**
3. Choose **"Ubuntu 24.04 by Arm Limited"** partner image
4. Name your runner (e.g., `my-org-arm64-runner`)
5. Configure size (e.g., 4-core, 16GB RAM)

**Update workflow to use custom runner:**
```yaml
strategy:
  matrix:
    include:
      - arch: amd64
        runner: ubuntu-24.04
      - arch: arm64
        runner: my-org-arm64-runner  # Your custom ARM64 larger runner name
```

**Cost:**
- Billed per minute (not included in free minutes)
- ~37% cheaper than x64 larger runners
- Ref: [Actions runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing)

## Registry Configuration

### GitHub Container Registry (GHCR) - Default

```yaml
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

- name: Login to GHCR
  run: |
    echo "${{ secrets.GITHUB_TOKEN }}" | podman login "${{ env.REGISTRY }}" \
      -u "${{ github.actor }}" \
      --password-stdin
```

### Docker Hub (Optional)

```yaml
- name: Login to Docker Hub
  run: |
    echo "${{ secrets.DOCKERHUB_TOKEN }}" | podman login docker.io \
      -u "${{ secrets.DOCKERHUB_USERNAME }}" \
      --password-stdin

# Push to Docker Hub
podman manifest push --all "$IMAGE:latest" \
  "docker://docker.io/${{ secrets.DOCKERHUB_USERNAME }}/app:latest"
```

## Debugging Multi-arch Images

```bash
# Pull specific architecture
podman pull --platform linux/arm64 ghcr.io/OWNER/REPO:latest

# Inspect manifest
podman manifest inspect ghcr.io/OWNER/REPO:latest

# Verify architectures
podman manifest inspect ghcr.io/OWNER/REPO:latest | jq '.manifests[].platform'
```

## Reference Documentation

For detailed information, see `references/github-actions-best-practices.md`.

## Containerfile Templates

For Containerfile templates and security best practices, see the **secure-container-build** plugin which provides:
- Production-ready templates for Python/uv, Bun, Node.js/pnpm, Golang, and Rust
- Wolfi runtime images with non-root users
- Multi-stage build patterns
- Allocator optimization for Rust

## Troubleshooting

### Common Issues

**Container networking SSL errors (ubuntu-24.04 runners)**:
- **Symptom**: `UNKNOWN_CERTIFICATE_VERIFICATION_ERROR` or SSL certificate verification failures during `bun install`, `npm install`, `pip install`, etc. inside containers
- **Cause**: GitHub Actions ubuntu-24.04 runner image 20251208.163.1+ has container networking configuration changes that break SSL/TLS connections from inside containers
- **Solution**: Add `--network=host` flag to `podman build`:
  ```yaml
  podman build \
    --network=host \
    --format docker \
    --platform linux/${{ matrix.arch }} \
    -f ./Containerfile \
    .
  ```
- **Verification**: Test repository at https://github.com/pigfoot/test-bun-ssl-issue
- **GitHub Issue**: https://github.com/actions/runner-images/issues/13422
- **Note**: This is a known issue with ubuntu-24.04 runners. The `--network=host` workaround reduces network isolation during build but is acceptable for CI/CD use cases.

**Authentication failed**:
- Ensure GITHUB_TOKEN has package write permission
- Check registry URL and credentials

**Manifest add failed**:
- Verify architecture-specific images exist in registry
- Check digest format is correct (`sha256:...`)

**ARM64 runner not available**:
- Standard ARM64 runners only work for public repos
- For private repos, use QEMU or larger runners

**podman-static installation fails**:
- Verify correct architecture detection
- Check GitHub releases for podman-static availability

**AppArmor issues**:
- Install binaries to `/usr/bin/` not `/usr/local/bin/`
- Run `podman system migrate` after installation

**Wrong architecture pulled**:
- Always use `--platform` flag when pulling
- Use `--format docker` when building for compatibility
