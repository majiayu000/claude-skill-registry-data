---
name: cloud-deploy-gcp-aws
category: deployment
description: Use when a backend or worker service needs a cloud deploy - container-first GitHub Actions deploys to Google Cloud Run (WIF) or AWS ECS/App Runner (OIDC), with migrate-before-deploy and a health-check gate
---
# Cloud Deploy — GCP & AWS (backend/worker)

## Overview

A backend deploy ships the **container the repo already builds**, not a re-implementation. The same image runs on Google Cloud Run and on AWS ECS — the deploy workflow only differs in the auth handshake and the deploy command. Read [[ci-cd-pipeline-authoring]] first: it defines the workflow naming/dispatch contract this skill fills in with real cloud steps.

**Core principle:** One image, one health-checked deploy per environment, authenticated by OIDC — never a hand-rolled server or a committed key.

## Pick the target, then copy the boilerplate

1. Decide the cloud (project's existing infra wins) and app type (`backend` or `worker`).
2. `search_boilerplate_catalog` → `deploy gcp backend`, `deploy aws worker`, etc. Copy that folder's `deploy-stage/preprod/prod.yml` into the project's `.github/workflows/` as `<id>-deploy-<env>.yml`.
3. Fill in the repo/environment **vars** its README lists (project id, region, service name, image repo). Set up the OIDC trust once (WIF pool / IAM role) — the README has the exact steps.

## GCP — Cloud Run

- Auth: `google-github-actions/auth` with `workload_identity_provider` + `service_account` (no key JSON).
- Deploy: `gcloud run deploy $SERVICE --image $IMAGE --region $REGION` (or `--source .` to build on deploy). Cloud Run gives you the revision URL to smoke-test.
- Worker (no HTTP ingress): deploy as a Cloud Run **job** (`gcloud run jobs deploy ... && gcloud run jobs execute`) or a GKE workload — not a public service.

## AWS — ECS Express Mode / Fargate

- Auth: `aws-actions/configure-aws-credentials` with `role-to-assume` (OIDC), no access keys.
- **ECS Express Mode** is AWS's recommended default (App Runner stopped accepting new customers on 2026-04-30; existing App Runner services keep working, but don't build new ones there): push the image to ECR, then let Express Mode provision and run the service from it — the simplest path for a single service today.
- **ECS Fargate** (more control over task definitions, scaling, networking): push to ECR, render the task definition, `aws-actions/amazon-ecs-deploy-task-definition` with `wait-for-service-stability: true`.
- Worker: an ECS service with no load balancer / no public subnet.

## Migrate before deploy

- Schema migrations run as a **pre-deploy step against the target environment's database**, gated per environment, before the new image is switched in. A failed migration must fail the workflow before any traffic shift.
- Migrations are forward-only and backward-compatible with the currently-running image (expand/contract) so a rollback of the image doesn't break on the new schema. See [[postgres-migrations]].
- Never point a stage/preprod deploy at the production database. One database per environment; the DB URL comes from that environment's vars/secrets.

## Health-check gate & rollback

- End every deploy job with a smoke step: curl the health endpoint (Cloud Run revision URL / ECS service URL / ALB DNS) and **fail the job on non-200**. A failing smoke step fails the deploy — the release goes `failed` and the release engineer rolls it back; only `finish_release` moves a task to `released`. This workflow's smoke step is a build-time gate, not the release verdict itself.
- Rollback is redeploying the previous image tag/revision — keep deploys immutable-tagged (git SHA), never `:latest`. Put the rollback command in the task's `rollback_plan` field (`update_board_task`) so the release engineer reads it on rollback — that field is posted on the card automatically at deploy time, which a comment is not.

## Common Mistakes

- Deploying `:latest` → no deterministic rollback target. Tag with the commit SHA.
- Running migrations from inside app startup instead of a gated pre-deploy step → half-migrated env on crash-loop.
- Stage deploy sharing the prod database.
- A deploy job that reports success without ever hitting the health endpoint.
- Storing a GCP service-account JSON or AWS access key in `secrets` instead of using OIDC/WIF.
- Standing up a new App Runner service instead of ECS Express Mode — it still works for existing services, but it is closed to new customers.

## Red Flags

- The workflow has no `id-token: write` permission (OIDC can't work).
- No smoke step, or a smoke step whose failure doesn't fail the job.
- Preprod/prod deploy triggers on `push` instead of `workflow_dispatch` (unless the component's delivery profile is genuinely `on_merge`).
