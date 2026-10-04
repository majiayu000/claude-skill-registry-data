---
name: insolvia-scripts
description: >-
  The catalogue of Insolvia's repo scripts and WHICH one to run WHEN — they are
  the project's tools, not incidental files. Use this the moment a task involves
  setting up or running any part of the monorepo locally, provisioning or
  wiping this machine's dev AWS resources, bootstrapping an environment, or
  deploying: "set up my dev environment", "get the API running", "reset/clear
  my dev database", "run the marketing site / Storybook / the app", "deploy to
  prod / staging", "seed the ECR image", "apply ci-trust", "auth to GitHub
  Packages", or any time you're about to hand-roll a Terraform/docker/npm command
  that a committed script already wraps. Reach for this BEFORE improvising shell
  — running the wrong thing by hand can create real AWS resources or skip a
  required step. Defers AWS-credential specifics to insolvia-aws-auth and
  ci-trust specifics to insolvia-deploy-role-permissions.
---

# Insolvia repo scripts — which one, when

Full details live in [`scripts/README.md`](../../../scripts/README.md); this is
the fast index so you pick the right tool instead of hand-rolling commands.
Every `dev-setup.sh` is idempotent and takes `--check` (report without
installing).

## First-time / toolchain setup

| Want to… | Run |
|---|---|
| Install the shared toolchain (Terraform, tflint, AWS CLI, jq, Node ≥24, Watchman, Python 3.12) | `scripts/dev-setup.sh` |
| Make a `read:packages` token available so `npm ci` can pull `@insolvia-ai/design-system` | `scripts/github-packages-auth.sh` |

## Run everything at once

| Want to… | Run |
|---|---|
| Bring the whole system up in one terminal (API + mailer + app + marketing), prefixed logs, one Ctrl-C stops it all | `scripts/dev-up.sh` — **takes no arguments** |
| Stop everything after a lost terminal or a killed dev-up, or reclaim ports/containers another **checkout**'s run left held | `scripts/dev-down.sh` (idempotent) |
| Stop one area only | that area's `scripts/dev-down.sh` (idempotent) |

`dev-up.sh` delegates to the per-area `dev-up.sh`/`dev-down.sh` pairs below
rather than duplicating them — which is also why it has no `--only`: to run one
part, run that part's own script. It refuses to start until `dev-aws-setup.sh`
has run, because there is no DynamoDB emulator and no fake Cognito.

## Run a package locally

Each package has a thin `scripts/dev-setup.sh` (bootstrap) + `dev-up.sh` (run):

| Package | Setup → Run |
|---|---|
| App (Expo/RN web SPA) | `apps/insolvia_app/scripts/dev-setup.sh` → `dev-up.sh` (`expo start --web`, pinned to **:3000** — Cognito registers that exact origin) |
| Marketing site | `apps/insolvia_marketing/scripts/dev-setup.sh` → `dev-up.sh` (RR7 SSR dev server) |
| API | `services/api/scripts/dev-setup.sh` → `dev-up.sh` (compose) → `dev-test.sh` (ruff+mypy+pytest, the UNIT tier, matches CI) → `dev-test-integration.sh` (the INTEGRATION tier: the running API over HTTP, signed in as `seeds/dev.json`'s person — needs `dev-up.sh` and `dev-aws-seed.sh`) |
| Mailer | `services/mailer/scripts/dev-setup.sh` → `dev-up.sh` (compose + Mailpit) → `dev-test.sh` |

`packages/insolvia_api_client` deliberately has no scripts — the root workspace
install covers it.

## Test

Four tiers, each a directory, each aimed at fixed environments — the
`insolvia-testing` skill says how to write one, ADR 0021 says which runs where.

| Want to… | Run |
|---|---|
| Run every **unit** suite in the repo, or only those a set of files can break (what the **pre-push hook** runs; `--list` shows the mapping) | `scripts/dev-test-unit.sh [files…]` |
| One Python unit's full gate (ruff → mypy → pytest, exactly as its PR check) | that unit's `scripts/dev-test.sh`; a bare `pytest` there is unit-only |
| The API's **integration** tier against this machine's dev stack (HTTP, signed in by SRP; no AWS credentials) | `services/api/scripts/dev-test-integration.sh [pytest args]` — needs `dev-up.sh` running and `dev-aws-seed.sh` done |
| The browser suite against this machine's dev stack — both projects, or `--project smoke` for the unauthenticated half | `e2e/scripts/dev-test.sh [--headed] [playwright args]` |
| The same tiers against **staging** or the smoke project against **production** | never from a laptop — `api-staging.yml`, `app-staging.yml` and `app-prod.yml` run them after each deploy |

The design system and the design tokens are **not in this repo** at all; they
live in `insolvia-ai/design-system` and install from GitHub Packages. If an
install here 401s on `@insolvia-ai/*`, that is registry auth, not a missing
setup script: run `./scripts/github-packages-auth.sh`.

## Per-machine dev AWS resources (the API's real dev DB — there is no emulator)

These touch real AWS, so read **insolvia-aws-auth** first if credentials aren't
already working.

| Want to… | Run |
|---|---|
| Provision this machine's isolated dev resources (`infra/envs/dev`: waitlist table + Cognito) and wire `services/api/.env` | `scripts/dev-aws-setup.sh` (`--check` verifies) |
| Get a usable signed-in dev environment: creates the dev sign-in account if missing — there is **no sign-up screen** on any pool (`allow_admin_create_user_only`) — and seeds its firm **and the fixture case** `seeds/dev.json` names (sample documents copied server-side from the shared fixture bucket). Also the fix for **"signed in, but every route 403s"** (`accessor unresolved / no_active_firm_user` in the API log): the account exists in Cognito but belongs to no firm, and the first firm cannot come from the API because `POST /v1/firm/users` is itself behind `FIRM_ADMINISTRATION`. Password from `~/.config/insolvia/dev.env`, `DEV_USER_PASSWORD`, or a no-echo prompt that offers to write that file | `scripts/dev-aws-seed.sh` (`--check`) |
| Wipe this machine's dev **data** (table delete+recreate incl. firms, Cognito users); resources survive. Leaves you with **neither an account nor a firm** — re-run the row above, which restores both | `scripts/dev-aws-reset.sh` (`--dry-run`, `--skip-cognito`) |
| Publish a committed seed-fixture version (`seeds/fixtures/<v>/`) into the account's shared fixture bucket, idempotently — once, after its PR merges; or **capture** a new version out of this machine's dev stack (refuses any other source) | `scripts/dev-fixture.sh publish v1 [--check]` · `scripts/dev-fixture.sh capture v2 <case-id> <handle>` |
| `terraform destroy` this machine's dev resources + unwind `.env` | `scripts/dev-aws-destroy.sh` |
| Destroy a **previous** machine-id's orphaned dev resources (leftovers a lost/regenerated `~/.config/insolvia/machine-id` strands, which destroy can't reach) | `scripts/dev-aws-destroy-orphan.sh <short-id>` |

(`dev-aws-common.sh` is sourced, not run.)

## Environment bootstrap & deploys

| Want to… | Run | Notes |
|---|---|---|
| Seed the ECR image an env's Image-package Lambdas need before Terraform can create them | `scripts/bootstrap-ecr-images.sh <env> [api\|mailer\|marketing] [--dispatch] [--yes]` | Breaks the documented first-apply deadlock |
| Apply `infra/envs/ci-trust` (OIDC provider + deploy role + policy) after a deploy fails on a newly-granted IAM permission | `scripts/apply-ci-trust.sh` | Human-gated; CI **cannot** apply this. See **insolvia-deploy-role-permissions** |
| Add / remove / show a required status check on `main`'s `protect-main` ruleset | `scripts/update-ruleset.sh [show\|add\|remove] "<check name>"` | Resolves the ruleset **by name**, never a hard-coded id, and re-PUTs the whole ruleset so it can't drop the other rules. Names must match a workflow job's `name:` exactly. See **insolvia-branch-protection** |

There is no deploy script at all: staging deploys automatically on merge to
`main`, and production ships by approving the release run's `promote` gate in
the GitHub UI. See the **insolvia-deploy** skill.
