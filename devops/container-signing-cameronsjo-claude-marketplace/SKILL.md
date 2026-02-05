---
name: container-signing
description: Set up Docker image signing with Cosign and SLSA provenance attestations. Use when configuring CI/CD for container builds, setting up GHCR publishing, or implementing supply chain security.
---

# Container Image Signing

Set up cryptographic signing and provenance attestations for container images using Sigstore Cosign and GitHub attestations.

## When to Use

- Setting up a new Docker/container CI/CD pipeline
- Adding supply chain security to existing container builds
- Publishing to GHCR (GitHub Container Registry)
- Implementing SLSA compliance for container artifacts

## Prerequisites

- GitHub repository with GitHub Actions
- Dockerfile in repository
- Container registry (GHCR recommended for GitHub projects)

## Implementation Steps

### 1. Add OCI Labels to Dockerfile

```dockerfile
# Build args for version info
ARG VERSION=dev
ARG GIT_COMMIT=unknown
ARG BUILD_TIME=unknown

# OCI labels for container registry linking and metadata
LABEL org.opencontainers.image.source="https://github.com/OWNER/REPO"
LABEL org.opencontainers.image.description="Brief description of the application"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.revision="${GIT_COMMIT}"
LABEL org.opencontainers.image.created="${BUILD_TIME}"
```

### 2. Create GitHub Actions Workflow

Create `.github/workflows/docker.yml`:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]
    paths-ignore:
      - "**.md"
      - "docs/**"
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      id-token: write      # Required for keyless Cosign signing
      attestations: write  # Required for provenance attestation

    outputs:
      digest: ${{ steps.build.outputs.digest }}

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push
        id: build
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            VERSION=${{ github.ref_name }}
            GIT_COMMIT=${{ github.sha }}
            BUILD_TIME=${{ github.event.head_commit.timestamp }}

      - name: Install Cosign
        uses: sigstore/cosign-installer@v3

      - name: Sign image with Cosign (keyless)
        env:
          DIGEST: ${{ steps.build.outputs.digest }}
        run: |
          cosign sign --yes ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${DIGEST}

      - name: Generate build provenance attestation
        uses: actions/attest-build-provenance@v2
        with:
          subject-name: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          subject-digest: ${{ steps.build.outputs.digest }}
          push-to-registry: true
```

### 3. Document Verification Commands

Add to README.md:

```markdown
#### Verify Image Signatures

Images are signed with [Cosign](https://github.com/sigstore/cosign) and include SLSA build provenance:

\`\`\`bash
# Verify signature (requires cosign)
cosign verify ghcr.io/OWNER/REPO:latest \
  --certificate-identity-regexp="github.com/OWNER/REPO" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com"

# Verify provenance (requires gh CLI)
gh attestation verify oci://ghcr.io/OWNER/REPO:latest --owner OWNER
\`\`\`
```

### 4. Set Package Visibility (After First Build)

```bash
# Make public
gh api --method PATCH /user/packages/container/REPO \
  -f visibility=public
```

## Verification Commands

### Cosign Signature Verification

```bash
cosign verify ghcr.io/OWNER/REPO:TAG \
  --certificate-identity-regexp="github.com/OWNER/REPO" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com"
```

### GitHub Attestation Verification

```bash
gh attestation verify oci://ghcr.io/OWNER/REPO:TAG --owner OWNER
```

## Key Concepts

### Keyless Signing

Uses GitHub's OIDC identity provider - no keys to manage. The signature is tied to:
- The GitHub Actions workflow that built it
- The repository and commit SHA
- The GitHub actor who triggered the build

### SLSA Provenance

SLSA (Supply-chain Levels for Software Artifacts) provenance provides cryptographic proof of:
- Where the image was built (GitHub Actions)
- What source code was used (commit SHA)
- What workflow built it (workflow path)

### Required Permissions

| Permission | Purpose |
|------------|---------|
| `contents: read` | Read repository contents |
| `packages: write` | Push to GHCR |
| `id-token: write` | Get OIDC token for keyless signing |
| `attestations: write` | Create provenance attestations |

## Registry Comparison

| Feature | GHCR | Docker Hub |
|---------|------|------------|
| Integration | Native GitHub | Separate account |
| Rate Limits | Generous | 100 pulls/6hrs anon |
| Signing | Native Cosign + attestations | Manual setup |
| Cost | Free for public | Free tier with limits |

## Troubleshooting

### "permission denied" on Cosign sign

Add `id-token: write` permission to workflow.

### Attestation not showing

Add `attestations: write` permission and ensure `push-to-registry: true`.

### Package not linked to repo

Add `org.opencontainers.image.source` label pointing to repository URL.
