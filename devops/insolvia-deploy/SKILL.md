---
name: insolvia-deploy
description: >-
  How Insolvia ships — and the rule that deploys happen in CI, never from your
  CLI. Use this whenever a task is about deploying, shipping, releasing, or
  "applying" infrastructure/services to staging or prod: "deploy to prod",
  "ship the API", "apply the terraform", "push a new version live", "run
  terraform apply", "update the lambda", "release". Read it BEFORE running any
  `terraform apply`, `docker push` to ECR, `aws lambda update-function-code`, or
  `aws`/`gh` deploy command against staging or prod — those are CI's job, and
  doing them by hand bypasses the OIDC deploy role and the environment gates.
---

# Deploying Insolvia

**Deploys run in GitHub Actions, triggered by git — not from anyone's CLI.**
The only credential that touches staging/prod AWS is the CI OIDC deploy role.

## The pipeline

One workflow, `release.yml`, owns the whole path to production:

1. **Merge to `main`.** The staging stage runs automatically: staging infra
   applies, then the changed services deploy (path-filtered against the last
   commit staging released green, so a leg an earlier run lost is retried),
   in dependency order.
2. **Staging goes green → the run parks at the `promote` job**, waiting on the
   `insolvia-production` environment's required reviewer.
3. **Approve it in the GitHub UI** (the run's page, "Review deployments" —
   one click, once). The production stage then ships the same commit: prod
   infra applies, then every service promotes.

So the deploy procedure is: **open a PR, get it merged, approve the pending
release run when you want prod to have it.** There is no script and no
dispatch in the normal path. Not approving is fine — each new green staging
run cancels older pending ones, so the offer is always the newest validated
commit, and an unapproved run ending `cancelled` is normal, not a failure.

| Target | Trigger |
|---|---|
| **staging** (infra + mailer, api, admin, mcp, marketing, app) | automatic on merge to `main` — the staging stage of `release.yml` |
| **prod** (infra + all services) | approving the `promote` gate of a green `release.yml` run |
| **shared infra** | automatic on merge to `main` — the first leg of `release.yml`'s staging stage (path-filtered on `infra/envs/shared/**` + `infra/modules/**`), ahead of the gate because both envs consume it; `shared-infra-deploy.yml` stays dispatchable out of band |
| **one prod service, out of band** | dispatch its `*-prod.yml` (emergency path: staging-green check + its own approval) |
| **prod infra, out of band** | dispatch `infra-prod.yml` — `mode: plan` (default, read-only → job summary) or `mode: apply` |

## What the production stage actually does

It **promotes**, it does not rebuild — and it promotes **everything at the
approved commit**, not just what that push changed. You can merge five PRs and
approve only the fifth run; nothing is left behind. Details worth knowing
before you debug one:

- The container repositories are shared across environments, so the image
  staging validated is already in the repository prod pulls from; each leg
  resolves the commit's `sha-<commit>` tag to an immutable digest and deploys
  that. The `record` job guarantees the tag exists for *every* service at
  *every* staging-green commit (unchanged services get the digest staging is
  currently serving). The app is the one exception and rebuilds from the
  verified commit, because it bakes its environment in at build time.
- **Prod infra applies as the first leg of the approved release** — same
  shape as staging, behind the approval. `infra-prod.yml` stays dispatchable
  for a read-only plan or an out-of-band apply.
- **A hand-dispatched prod deploy refuses a commit staging never validated.**
  That is `.github/actions/verified-commit` reading the
  `insolvia/staging-release` commit status the `record` job stamps; the fix is
  normally "let staging release it first", not `force: true`.

Rolling back the API or marketing does not need the pipeline at all — they
serve through a `live` Lambda alias, so
`aws lambda update-alias --function-name <fn> --name live --function-version <previous>`
reverts in seconds. That is a read of the alias plus one write; it is the one
production mutation that is faster by hand than through CI, and the job summary
of every deploy prints the exact command with the previous version filled in.
For a full re-promotion of an older commit, re-run its (green) `release.yml`
run and approve the gate again, or dispatch the individual `*-prod.yml`
workflows with `sha=<commit>`.

## The rule

**Do not deploy or apply against staging or prod from the CLI.** Specifically,
never run against staging/prod:

- `terraform apply` in `infra/envs/staging` or `infra/envs/prod`
- `docker push` to a service ECR repo, or `aws lambda update-function-code`
- `aws s3 sync` of client assets or a CloudFront invalidation for a live env

If you want to *see* a prod plan, that is `infra-prod.yml` with `mode: plan`
(the only way to plan against real prod state — `shared-infra-plan.yml` validates
offline with no credentials).

## The only local applies that are legitimate

- **Your own per-machine dev env** — `scripts/dev-aws-*` against `infra/envs/dev`
  (that's your dev database; see the `insolvia-scripts` skill).
- **The `ci-trust` anchor** — `scripts/apply-ci-trust.sh`, human-gated because CI
  cannot apply its own permissions (see `insolvia-deploy-role-permissions`).

Everything else is a merge, an approval, or a dispatch — never a hand-run apply.
