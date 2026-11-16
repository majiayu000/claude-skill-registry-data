---
name: deploy
description: "Deploy to a cloud or PaaS, write Docker/Kubernetes/Helm/IaC, set up CI/CD, or diagnose a failing deploy. Platform-aware: AWS, GCP, Azure, Vercel/Netlify/Fly/Railway/Render/Cloudflare, Terraform/OpenTofu/Pulumi/CDK."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "honey-stack research 2026-10-18 (cloud provider docs, Docker/K8s best practices, GitHub Actions OIDC). Full reports distilled into references/."
---

# deploy

Ship a service to where it runs, write the infra for it, or find out why a deploy failed. Pick the platform from the repo (lockfiles, existing `Dockerfile`, `fly.toml`, `vercel.json`, `.github/workflows`, cloud config) before asking.

## Confirm before these (never on your own)
- Any deploy to **production** (prod env/branch, `--prod`, a prod cluster or context).
- `destroy`/`delete`/resource replacement in IaC (`terraform destroy`, a plan showing `-/+` or `- destroy`, `pulumi destroy`, `cdk destroy`, `kubectl delete`).
- Provisioning anything **billable** (clusters, NAT gateways, load balancers, databases, GPUs).
- Rotating/overwriting secrets, changing IAM trust, opening a security group to `0.0.0.0/0`.
- Any `kubectl` before you've run `kubectl config current-context` and confirmed the target.

**Refuse:** committing secrets, printing secret values, `--force`/`--auto-approve`/`--yes` on destructive ops, long-lived cloud keys when OIDC is available. Secrets live in a cloud secret manager or the platform's env store, never in git or an image.

## Pick the target

| You have / want | Use | Skip |
|---|---|---|
| Containerized web service on AWS | **ECS Fargate** (or ECS Express Mode for image→URL) | App Runner — closed to new customers since 2026-04-30 |
| Event-driven, bursty, <15 min on AWS | **Lambda** | |
| Any container on GCP, scale-to-zero | **Cloud Run** (`gcloud run deploy --source .`) | App Engine for new work |
| Any container on Azure | **Container Apps** (`az containerapp up`) | |
| Need real Kubernetes | GKE Autopilot / EKS / AKS | hand-rolled nodes |
| Next.js / frontend | **Vercel** (best previews) | |
| Fast "push and it runs" | Railway / Render / Fly.io | |
| Edge compute | Cloudflare Workers (`wrangler deploy`) | Pages for new projects |

Per-platform commands, the top real errors, and their fixes: `references/{aws,gcp,azure,paas}.md`.

## Containers and Kubernetes
Dockerfiles (multi-stage, slim/distroless, non-root, BuildKit cache, `--mount=type=secret`, `.dockerignore`), and Kubernetes (Deployment/Service/Ingress, readiness/liveness/startup probes, resource requests+limits, rolling update + rollback) and Helm: `references/containers.md`. Build images for the right arch (`linux/amd64`, or `arm64` to match Graviton/Fargate).

## Infrastructure as code
Terraform vs OpenTofu vs Pulumi vs CDK, when to pick each, remote state with locking, and plan/apply safety: `references/iac.md`. Always run `plan`/`preview` and read it; confirm before applying a plan that destroys or replaces anything; never commit state.

## CI/CD
GitHub Actions deploy workflows, OIDC to the cloud (no stored keys), and blue/green vs canary vs rolling with a known rollback: `references/cicd.md`.

## Diagnose a failed deploy (the common loop)
1. Read the real error: platform events/activity first (ECS stopped-reason, Cloud Run revision logs, `az containerapp logs show`, `kubectl describe` + `kubectl logs --previous`), then container logs.
2. Classify it: build, image-pull (tag/auth), startup/crash (exit code, missing env, **port mismatch**), health-probe (path/port/timing), permission (IAM/role/registry), or config (missing env/secret).
3. Most "won't go healthy" failures are a **port mismatch** (app listens on a port ≠ the configured one) or a **failing health probe**, not the deploy tool. Fix the cause, redeploy, confirm healthy, and know the rollback command before you start.

Done when: the new version is serving healthy traffic (or the diagnosis names the exact cause and fix), and you've stated what deployed, where, and how to roll back.
