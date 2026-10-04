---
name: cloud-deploy-gcp-aws
category: deployment
description: Use when a web/frontend app needs a cloud deploy - GitHub Actions to Cloud Run/ECS for SSR or GCS+CDN/Firebase and S3+CloudFront for static, with build-time env and cache invalidation
---
# Cloud Deploy — GCP & AWS (web)

## Overview

A web deploy's shape follows the **render mode**, not the framework. Server-rendered (Next.js SSR, SvelteKit node) ships a container exactly like a backend service; a static export (Next.js `output: 'export'`, Vite build) ships files to object storage behind a CDN. Pick the mode first. Read [[ci-cd-pipeline-authoring]] for the workflow naming/dispatch contract this fills in.

**Core principle:** Match the deploy target to the render mode, bake public config at build time, and invalidate the CDN on every deploy — a stale edge cache is the most common "I deployed but nothing changed."

## Pick the target, then copy the boilerplate

`search_boilerplate_catalog` → `deploy gcp web` / `deploy aws web`. Copy its `deploy-stage/preprod/prod.yml` into `.github/workflows/` as `<id>-deploy-<env>.yml`, then set the README's repo/environment **vars**. OIDC auth, no keys.

## SSR (containerized)

Build the image, push it, then deploy it:

- **GCP:** `google-github-actions/auth` with Workload Identity Federation (no key JSON), then `gcloud run deploy $SERVICE --image $IMAGE --region $REGION` to **Cloud Run**. The revision URL is what you smoke-test.
- **AWS:** `aws-actions/configure-aws-credentials` with `role-to-assume` (OIDC), push to ECR, then deploy via **ECS Express Mode** (AWS's current recommended default) or ECS Fargate with `aws-actions/amazon-ecs-deploy-task-definition` (`wait-for-service-stability: true`) for more control.

Use this path when the app has server components, API routes, or ISR.

## Static (object storage + CDN)

- **GCP:** either **Firebase Hosting** (`firebase deploy --only hosting`, simplest, CDN + rollback built in) or a **GCS bucket + Cloud CDN / load balancer**; after upload, invalidate the CDN.
- **AWS:** sync the build output to an **S3** bucket and serve via **CloudFront**; after `aws s3 sync`, run `aws cloudfront create-invalidation --paths '/*'`.
- Set long cache TTLs on hashed assets and `no-cache` on `index.html` so a deploy is picked up immediately.
- Next.js static export is `output: 'export'` in `next.config` (the `next export` CLI command was removed) — keep the build step producing the `out/` directory the sync step uploads.

## Build-time env

- Public config is **inlined at build time** (`NEXT_PUBLIC_*`, `VITE_*`) — it is baked into the bundle, so the build job for each environment sets that environment's values from vars. You cannot change a `NEXT_PUBLIC_` value after build without rebuilding.
- Never put a secret in a `NEXT_PUBLIC_`/`VITE_` var — it ships to the browser. Secrets belong to the server (SSR) or a backend, never the static bundle.

## Health-check gate

End the job by fetching the deployed URL (SSR health route, or the static site's `index.html`) and fail on non-200 / missing marker. A failing smoke step fails the deploy — the release goes `failed` and the release engineer rolls it back; only `finish_release` moves a task to `released`.

## Common Mistakes

- Static deploy with no CDN invalidation → users keep the old bundle.
- Aggressive caching on `index.html` → new asset hashes never get requested.
- A secret in a `NEXT_PUBLIC_` var, shipped to every visitor's browser.
- Rebuilding per env is skipped and one bundle is promoted across envs with the wrong baked config.
- Calling the removed `next export` CLI command instead of setting `output: 'export'`.

## Red Flags

- No `create-invalidation` / hosting cache bust after a static upload.
- Public build vars holding tokens or keys.
- Deploy triggers on `push` for preprod/prod instead of `workflow_dispatch` (unless the component's delivery profile is genuinely `on_merge`).
