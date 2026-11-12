---
name: ak-devops
description: "Deploy to Cloudflare (Workers, R2, D1), Docker, GCP (Cloud Run, GKE) and Kubernetes (kubectl, Helm)."
when_to_use: "Invoke for serverless, containers, CI/CD, GitOps or security audits."
category: engineering
keywords: [cloudflare, docker, gcp, kubernetes, cicd]
license: Proprietary
argument-hint: "[platform] [task]"
metadata:
  author: agentkit
  version: "2.1.0"
---

# DevOps Skill

Deploy and manage cloud infrastructure across Cloudflare, Docker, Google Cloud, and Kubernetes.

## When to Use

- Deploy serverless apps to Cloudflare Workers/Pages
- Containerize apps with Docker, Docker Compose
- Manage GCP with gcloud CLI (Cloud Run, GKE, Cloud SQL)
- Kubernetes cluster management (kubectl, Helm)
- GitOps workflows (Argo CD, Flux)
- CI/CD pipelines, multi-region deployments
- Security audits, RBAC, network policies

## Select the target and effect

Read repository deployment/container configuration and the user's target first. Preserve
that provider; do not change cloud vendors to fit an example. Choose local build/test,
preview or production rollout explicitly. Local Docker work does not call cloud CLIs.

Load only the target reference below. For new-platform comparisons or invocation examples,
use `references/platform-recipes.md`, verifying CLI/version-sensitive details first.
Before production rollout establish exact account/project/region, health checks and rollback;
reuse existing authorization for those effects. Keep secrets out of output and preserve
state ownership. Track and stop only processes started for this work.

## Reference Navigation

### Cloudflare Platform
- `cloudflare-platform.md` - Edge computing overview
- `cloudflare-workers-basics.md` - Handler types, patterns
- `cloudflare-workers-advanced.md` - Performance, optimization
- `cloudflare-workers-apis.md` - Runtime APIs, bindings
- `cloudflare-r2-storage.md` - Object storage, S3 compatibility
- `cloudflare-d1-kv.md` - D1 SQLite, KV store
- `browser-rendering.md` - Puppeteer automation

### Docker
- `docker-basics.md` - Dockerfile, images, containers
- `docker-compose.md` - Multi-container apps

### Google Cloud
- `gcloud-platform.md` - gcloud CLI, authentication
- `gcloud-services.md` - Compute Engine, GKE, Cloud Run

### Kubernetes
- Use upstream Kubernetes and Helm documentation for cluster-specific details.

### Scripts
- `scripts/cloudflare_deploy.py` - Automate Worker deployments
- `scripts/docker_optimize.py` - Analyze Dockerfiles

## Best Practices

**Security:** Non-root containers, RBAC, secrets in env vars, image scanning
**Performance:** Multi-stage builds, edge caching, resource limits
**Cost:** R2 for large egress, caching, right-size resources
**Development:** Docker Compose local dev, wrangler dev, version control IaC

When an authorized task sets up or changes an operational route — a deploy path,
a log source, a credential retrieval route, a webhook/OAuth/DNS entry, or a
backup/rollback route — update the affected project guide within authorized
scope, or report the proposed diff and the blocker when the write is not
authorized. Route it through the project's documentation workflow (`/ak-docs update`).

## Resources

- Cloudflare: https://developers.cloudflare.com
- Docker: https://docs.docker.com
- GCP: https://cloud.google.com/docs
- Kubernetes: https://kubernetes.io/docs
- Helm: https://helm.sh/docs
