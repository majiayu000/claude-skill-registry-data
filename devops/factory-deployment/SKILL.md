---
name: factory-deployment
description: Deployment and infrastructure conventions across builds. Vercel + Neon for web (with PR branch DBs), Cloud Run for Python services (one service per entry-point variant), GitHub Actions matrix-deploy on merge, Terraform with environments/modules layout for AWS / compliance customers, RDS IAM authentication for AWS DBs, Docker per Python entry point, env vars via t3-oss/env-nextjs, and the single-tenant customer-cloud deployment model (per the factory thesis). Migrations in CI, never at runtime.
---

# Factory deployment

Most of this skill is Recipe — deployment is where stack-specific decisions are the substance, not the surface. The few load-bearing principles (one service per entry point, migrations in CI, boot-time assertions, single-tenant customer-cloud as the commercial wedge) lead their sections; the rest are marked `Recipe only`.

## Web — Vercel + Neon

**Recipe only** — stack pick.

| Aspect | Choice |
|---|---|
| Hosting | Vercel |
| Database | Neon (Postgres) — dev branches for PRs, prod for main |
| Migrations | `drizzle-kit migrate` in GitHub Actions, against ephemeral Neon branch |
| Env vars | Vercel project + `t3-oss/env-nextjs` Zod validation |
| Preview safety | Boot-time assertion: `VERCEL_ENV=preview` MUST NOT use prod `DATABASE_URL` |

## Boot-time assertions for configuration safety

**Principle.** Configuration mistakes that could cause data loss or cross-environment writes fail loud at boot.

**Why.** A misconfigured preview deployment that connects to prod is the silent kind of incident — preview writes look like real writes, no error fires, the data contaminates for days. A boot-time assertion that compares `VERCEL_ENV` against `DATABASE_URL` makes the misconfiguration instant and visible. Three lines of code; one prevented incident pays for them many times over.

**Recipe.**

```ts
// src/db/index.ts — boot-time assertion
const isPreview = process.env.VERCEL_ENV === 'preview';
if (isPreview && process.env.DATABASE_URL === process.env.PROD_DATABASE_URL) {
  throw new Error('Preview deployment cannot use prod DATABASE_URL');
}
```

## One Cloud Run service per Python entry point

**Principle.** Each Python entry-point variant (CLI, API, Pub/Sub) gets its own Cloud Run service with its own Dockerfile.

**Why.** Sharing a service across entry points means the startup command is conditional — `if mode == 'api' run uvicorn; else run pubsub-handler` — which makes the service definition impossible to validate at deploy time. Separate services have separate Dockerfiles, separate startup commands, separate scaling configurations. The cost is more Cloud Run services; the benefit is each one is independently deployable, scalable, and debuggable.

**Recipe.**

| Service | Entry point | Trigger |
|---|---|---|
| `myservice-api` | `main_api.py` (FastAPI) | HTTP request |
| `myservice-pubsub` | `main_pubsub.py` (handler) | Pub/Sub topic |

```dockerfile
# Dockerfile.api
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen
COPY src/ ./src/
COPY main_api.py ./
ENV PYTHONUNBUFFERED=1
USER nonroot
CMD ["uv", "run", "uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8080"]
```

```dockerfile
# Dockerfile.pubsub
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen
COPY src/ ./src/
COPY main_pubsub.py ./
ENV PYTHONUNBUFFERED=1
USER nonroot
CMD ["uv", "run", "python", "main_pubsub.py"]
```

Non-root user; `PYTHONUNBUFFERED=1` for log streaming.

## GitHub Actions — ephemeral DBs + matrix deploy

> **Cross-reference.** `factory-ci.md` owns the merge gate (typecheck, lint, test, build, claude-review). This section owns the deploy half — the Neon branch action for ephemeral PR DBs that the `test` job depends on, and the matrix-deploy jobs that run after the gate passes on `main`.

**Principle.** Every PR gets a real ephemeral database via Neon branch; production data and dev data never mix in test pipelines.

**Why.** Shared dev DBs are a constant source of false test failures — a parallel PR mutated the schema, another test left stale rows, the test that "always passed" suddenly doesn't. Ephemeral per-PR DBs eliminate the shared state: each PR's tests run against a clean branch off main, deleted on PR close. The cost is one Neon project; the benefit is test reliability.

**Recipe.**

```yaml
# .github/workflows/ci-cd.yml (sketch)
name: ci-cd

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: neondatabase/create-branch-action@v5
        id: neon
        with:
          project_id: ${{ secrets.NEON_PROJECT_ID }}
          parent: main
          branch_name: pr-${{ github.event.pull_request.number }}
      - run: pnpm install
      - run: pnpm db:migrate
        env:
          DATABASE_URL: ${{ steps.neon.outputs.db_url }}
      - run: pnpm test

  deploy-web:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: --prod

  deploy-python:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [myservice-api, myservice-pubsub]
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v2
        with: { credentials_json: '${{ secrets.GCP_SA_KEY }}' }
      - run: gcloud run deploy ${{ matrix.service }} --source ./models/myservice ...
```

## Env vars — validate at build with Zod

**Principle.** Env vars are validated against a Zod schema at build time; the build fails if any required var is missing or wrong-shaped.

**Why.** Missing env vars surface at runtime as `undefined` reads — sometimes the page renders blank, sometimes a server action throws a cryptic error, sometimes auth silently degrades. Build-time validation makes the missing var fail at deploy, before any user sees the symptom. `t3-oss/env-nextjs` is the discriminated client/server split that keeps client bundles from leaking secrets.

**Recipe.**

```ts
// src/env.js
import { createEnv } from '@t3-oss/env-nextjs';
import { z } from 'zod';

export const env = createEnv({
  server: {
    DATABASE_URL: z.string().url(),
    BETTER_AUTH_SECRET: z.string().min(32),
    RESEND_API_KEY: z.string(),
    RESEND_BAA_SIGNED: z.enum(['true', 'false']).optional(),
  },
  client: {
    NEXT_PUBLIC_POSTHOG_KEY: z.string(),
    NEXT_PUBLIC_SENTRY_DSN: z.string().url().optional(),
  },
  runtimeEnv: { ... },
});
```

Don't ship past the build error.

## Terraform — when AWS / compliance is in scope

**Recipe only** — pick when single-tenant customer-cloud deployment is the model. Use the environments/modules layout below; per-env values in `terraform.tfvars`, never hardcoded in `main.tf`.

```
infra/terraform/
├── environments/
│   ├── production/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   └── ...
│   └── dev/
│       └── ...
└── modules/
    ├── database/           # RDS, parameter groups, backups
    ├── compute/            # ECS / Cloud Run / Fargate
    ├── networking/         # VPC, subnets, security groups
    └── secrets/            # KMS, Secrets Manager
```

Pick when:
- Customer requires single-tenant deployment in their cloud (HIPAA, FDA 21 CFR 820, SOC 2 Type II)
- AWS RDS (vs Neon) for compliance posture
- Need IaC for VPCs, security groups, KMS keys, IAM roles

## RDS IAM authentication — no long-lived passwords

**Principle.** When AWS RDS is the database, use IAM authentication; never long-lived passwords in env vars.

**Why.** A long-lived DB password in an env var is a credential that can leak via logs, build artifacts, or a misconfigured secrets manager — and a leaked password is valid until rotated, which requires coordinated downtime. IAM tokens rotate every 14 minutes; a leaked token expires before exploitation is practical. The cost is a token-fetch helper and a refresh loop; the benefit is a credential-leak failure mode that bounds the blast radius.

**Recipe.**

```ts
// src/db/rds-auth.ts
import { Signer } from '@aws-sdk/rds-signer';

const signer = new Signer({
  hostname: process.env.RDS_HOSTNAME!,
  port: 5432,
  username: process.env.RDS_USERNAME!,
  region: process.env.AWS_REGION!,
});

async function getToken(): Promise<string> {
  return signer.getAuthToken();
}
```

Token rotates every 14 minutes; cache and refresh near expiry. Pair with a lazy DB singleton (`Proxy`-wrapped) so connections only open after IAM token is fetched.

## Migrations — CI, never runtime

**Principle.** Migrations run in CI against an ephemeral branch DB or on a CI step before deploy; never at application startup.

**Why.** Same principle as `factory-data-layer.md §migrations — CI, not runtime`. Runtime migrations turn deployment into a database operation — slow boots, half-migrated states on failure, rollback-deploy-without-rollback-schema. CI migrations keep schema changes a separate gate.

**Recipe.**

```sh
# Local dev — schema push (fast iteration)
drizzle-kit push

# Pre-merge — generate migration file from schema diff
drizzle-kit generate

# CI — apply migrations against ephemeral PR DB
drizzle-kit migrate

# CI / merge to main — apply migrations against prod DB before deploying app
drizzle-kit migrate
```

**Never put `drizzle-kit migrate` in a Cloud Run `CMD` or Vercel build step.**

**Failure mode.** Migrations in Cloud Run startup → 30-second cold starts; if a migration fails mid-startup, the service is in a broken half-migrated state with no clean recovery.

## Single-tenant customer-cloud — the commercial wedge

**Principle.** For compliance-sensitive customers, deploy a single-tenant container into the customer's cloud; the factory is the substrate, not the host.

**Why.** Multi-tenant SaaS is incompatible with the compliance postures that high-value verticals require (HIPAA, FDA 21 CFR 820, SOC 2 Type II as a control, not as a marketing badge). Single-tenant customer-cloud lets the customer own data residency, secrets, and access — which makes their compliance officer's review fast — while the factory ships updates as pinned tags of the kit's repo. The trade-off vs SaaS: more per-customer onboarding, no shared infrastructure economies. The trade-off vs custom-built: dramatically less per-customer cost.

**Recipe.**

| Aspect | Choice |
|---|---|
| Deployment | Single-tenant container in customer's GCP or AWS account |
| Bootstrap | One-command Terraform module — "deploys in 2 hours" |
| Data residency | Customer's region — never crosses into the factory's infra |
| Secrets | Customer's AWS Secrets Manager / GCP Secret Manager — never in the factory repo |
| Updates | Customer pulls a new pinned tag of the factory-kit repo |

This is the differentiator vs. SaaS competitors (Retool, Superblocks). Customer data never leaves their cloud.

## Source patterns

Encode/monorepo (Cloud Run with separate Dockerfile.api / Dockerfile.pubsub, GitHub Actions ephemeral Neon branches, matrix-deploy on merge, PostHog ingest rewrite), duezy (Terraform environments/modules layout, RDS IAM authentication with 14-min refresh, lazy DB singleton via Proxy), fleet-advisor (Vercel + Neon, t3-oss/env-nextjs Zod validation, monorepo deploy strategy), ford-analysis (`VERCEL_ENV` preview-DB safety check), Obsidian software-factory-idea (single-tenant customer-cloud deployment as commercial differentiator).
