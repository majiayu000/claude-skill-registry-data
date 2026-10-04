---
name: aws-tenant-standup
description: Stand up or rebuild an AWS Shifter tenant end to end (teardown, bootstrap, secrets, image bakes, deploy via the real deploy.yml dispatch, health check, base-range smoke, and a POLARIS range walkthrough). AWS only. Use when asked to rebuild, redeploy, or stand up an AWS tenant such as proof or aws-dev from a clean state.
---

# AWS tenant standup and rebuild (AWS only)

This skill drives a full AWS Shifter tenant from a clean (or dirty) account to a
healthy, verified tenant with a live POLARIS range. It exists so a fresh session
does not repeat the deploy-docs archaeology and does not re-hit the
fresh-environment gotchas already fixed on `dev`. GCP is out of scope.

## Ground rules

- All Shifter AWS resources live in `us-east-2` unless the operator says otherwise.
- The canonical GitHub repository is `Brad-Edwards/shifter` (see `AGENTS.md`).
- Never add AI or Claude attribution to any commit, PR, issue, or file.
- Do not merge branches. Merges are operator-driven. Fixes land as PRs to `dev`.
- Run long-running Terraform and deploys in the background. A foreground tool
  timeout can kill a Terraform provider plugin mid-apply and corrupt progress.
- Do not stack pushes to an environment branch while its CI or deploy is in flight.
- Verify with the CLI before stating a fact. Do not fabricate on a failed step.
- Fix root causes and PR them to `dev`. Do not jury-rig around a real bug.

## Parameters

Read these from the invocation arguments if supplied (natural language or
`key=value` pairs). Ask the operator for any that are missing before doing
anything destructive.

- `profile`: the AWS CLI profile to use (for example `proof` or `aws-dev`).
- `region`: the AWS region. Default `us-east-2`; confirm rather than assume.
- `mode`: one of
  - `teardown`: rip out everything, including AMIs, and re-bake fresh images.
  - `preserve-amis`: tear down the infrastructure but keep existing AMIs and
    skip the bake phase (faster restart when the images are still good).

Derive the environment from the profile and confirm it with the operator:
`proof` maps to Terraform env `proof` and deploy input `aws-proof`; `aws-dev` or
`dev` maps to Terraform env `dev` and deploy input `aws-dev`. The `deploy.yml`
`workflow_dispatch` environment options are `aws-dev` and `aws-proof`.

## Authoritative sources (read these first)

Read these before acting. They are the real process. Do not follow
`docs/technical/platform_infrastructure/manual-deployment.md` as the primary
path; it is a legacy fallback, not the deploy pipeline.

- `docs/dev/deploy-secrets.md`: the single authoritative checklist of every
  secret a fresh AWS environment needs, plus the fresh-account bootstrap order.
- `docs/dev/aws-teardown-runbook.md`: the teardown procedure and the tag-scoped
  account-recovery sweep.
- `docs/technical/dev/secrets.md`: where runtime secrets live and how tfvars
  reach Terraform (real values come from `TF_VARS_<ENV>_*` GitHub secrets
  rendered to a gitignored `local.auto.tfvars`, not committed tfvars).
- `.github/workflows/deploy.yml`: the real deploy path (`workflow_dispatch` with
  an `environment` input; the branch you dispatch from is the code that deploys).
- `.github/workflows/packer.yml`: the image bake pipeline.

## Phase 0: preflight

1. Confirm the account identity and record the account id:
   `aws --profile <profile> sts get-caller-identity`.
2. Confirm the local overlay exists for each stack:
   `platform/terraform/environments/<env>/local.auto.tfvars` (core),
   `.../<env>/range/local.auto.tfvars`, and `.../<env>/portal/local.auto.tfvars`.
   These are gitignored real values. If any is missing, the values must already
   be in the matching `TF_VARS_<ENV>_*` GitHub secret. Keep the overlay and the
   secret in step with `scripts/sync-deploy-secrets.sh` (it never prints
   contents). You may read and edit the local overlay; never paste its contents
   into chat, a PR, a commit, or an issue.
3. Run the deploy preflight to confirm required secrets are present:
   `python3 scripts/bootstrap/preflight.py` (see `deploy-secrets.md` for the
   required set).

## Phase 1: teardown

Follow `docs/dev/aws-teardown-runbook.md`. Key points learned in practice:

- Destroy all three Terraform roots: portal, then range, then core
  (`platform/terraform/environments/<env>/{portal,range,}`). The portal root
  declares `cloud_provider`; pass `-var="cloud_provider=aws"` there. The range
  and core roots do not declare it, and Terraform 1.15+ errors on an undeclared
  `-var`, so do not pass it to those.
- Empty versioned buckets (logs, ECR, Terraform state) before destroy, including
  all object versions and delete markers, or the destroy fails on non-empty
  buckets.
- The account-recovery sweep is tag-scoped (`Project=shifter` plus the
  environment tag). Run it to catch anything Terraform missed.
- If `mode=preserve-amis`: before teardown, capture the AMI ids you will reuse
  (`ec2_ami_id`, `ctfd_ami_id` in the portal overlay; the `/shifter/ami/*` SSM
  parameters; `polaris-vm` and `polaris-dc`; `shifter/packer/dc-amis.json`).
  Do not deregister those AMIs, and skip Phase 3.

## Phase 2: bootstrap and secrets

1. Bootstrap the fresh account bits (OIDC role, state bucket, global IAM):
   `python3 scripts/bootstrap/deploy.py bootstrap --env <env>`. This sets
   `AWS_ROLE_ARN_<ENV>` and `TF_INFRA_STATE_BUCKET_<ENV>`.
2. Ensure the runners are registered per the runbook.
3. Ensure the deploy secrets exist. Assume the same starting secrets as before.
   Push local overlays with `scripts/sync-deploy-secrets.sh --env <env>` (add
   `--stack config --shifter-config <path>` for the `SHIFTER_CONFIG_*` payload).

## Phase 3: image bakes (skip when preserving AMIs)

Bake base images (kali, ubuntu, windows, dc) and the POLARIS images
(`polaris-vm`, `polaris-dc`) via `packer.yml`.

- Bakes need per-account `PACKER_VERIFY_{SUBNET,SG,INSTANCE_PROFILE}_ID_<ENV>`
  variables plus a `<env>.pkrvars.hcl`, both derived from the freshly rebuilt
  VPC. There is a post-build DNS validation gate.
- After baking, update `ec2_ami_id` and `ctfd_ami_id` in the portal overlay,
  update `shifter/packer/dc-amis.json`, update the `/shifter/ami/*` SSM
  parameters, then re-sync the portal secret with `sync-deploy-secrets.sh`.
- Known design issue: baking must not depend on a branch merge (tracked in
  issue #1680). If a bake seems to require merging first, stop and flag it.

## Phase 4: deploy

Deploy via the real pipeline, dispatched from the code branch you want live
(usually `dev` for a standard standup):

```
gh workflow run deploy.yml --repo Brad-Edwards/shifter \
  -f environment=aws-<env> --ref <code-branch>
```

The stages run Core, then Range, then Engine, then Platform. Monitor the run to
a terminal state. On the first deploy of a fresh account, watch the portal
migration step: if it fails because there is no in-service ASG instance yet, or
because the runtime DB user does not exist, run the migration by hand over SSM as
the DB master:

```
scripts/portal-deploy/deploy_portal.sh --migrate-only   # via SSM on the portal EC2
```

The entrypoint switches to the RDS-IAM runtime user (`portal_runtime`), which is
created by a migration, so on a fresh DB the migrate must run with
`DB_IAM_AUTH_RUNTIME=false` (the `--migrate-only` path sets this).

## Phase 5: health verification

- ALB target health: `proof-portal-tg` (portal app) and `proof-portal-guacamole`
  should be all healthy (substitute the env prefix).
- ACM certificate validated for the portal domain.
- Portal responds: `/health/` returns 200 and `/` returns 200. If Cloudflare DNS
  is not yet pointed at the new ALB, verify against the raw ALB with a host
  header or `curl --resolve <domain>:443:<alb-ip>`.

## Phase 6: base-range smoke

Run the post-deploy smoke against a base range to prove provisioning works end to
end. See `scripts/post_deploy_smoke/README.md` for the entrypoint. This exercises
subnet allocation, guest launch, and bootstrap. Do this before POLARIS to avoid
range contention.

## Phase 7: POLARIS range walkthrough

Provision a POLARIS range and confirm it reaches READY.

1. Provision via the portal Django shell over SSM. Get the portal instance,
   `docker exec` the portal container, re-export the app environment from
   `/proc/1/environ` (the shell needs `DJANGO_SECRET_KEY` and friends), then call
   `cms_create_range(user, 'polaris', {}, False)`.
2. Poll the range status to READY or FAILED. The provisioner launches as an ECS
   task off the latest ACTIVE `<env>-portal-pulumi-provisioner` task definition.
3. On READY, confirm: two guests running (kali attacker on `polaris-vm`, dc01 on
   `polaris-dc`), the DC promoted (`boreas.local`), the full container stack up on
   the kali host (17 containers including `a14-kali`, the Bedrock agent), and the
   agent verify checks pass (identity via credential_process plus regional STS,
   and a Bedrock `invoke-model`).

POLARIS Bedrock requirements:

- The account must have Bedrock model access for the configured agent models.
  Verify with an actual `bedrock-runtime invoke-model`, not
  `list-foundation-models` (the latter shows region availability, not account
  access). See `reference_proof_bedrock_model_access` in operator notes: the
  proof account can invoke only `sonnet-4-6`; all haiku variants are Marketplace
  gated.
- The `aws_polaris_agent_*` variables must be set in the portal overlay and the
  `TF_VARS_<ENV>_PORTAL` secret. Empty values make POLARIS fail at variable
  build. Point both the main and small models at a model the account can invoke.

## Phase 8: report and DNS handoff

Report the outcome and the DNS records the operator must set in Cloudflare (DNS
is external; the agent does not hold those credentials):

- `<env>.shifter.keplerops.com` CNAME to the portal ALB DNS name.
- `polaris.keplerops.com` A record to the CTFd EIP.

Note that a running POLARIS range costs money until it is destroyed. State
clearly whether the range was left running.

## Known pitfalls (already fixed on dev; verify, do not re-hit)

These were the fresh-environment failures found during the proof rebuild. They
are fixed on `dev`. On a fresh account, confirm the fix is present rather than
rediscovering the failure.

- Provisioner image must copy the whole `shared` package, not a subset, or range
  provisioning fails with `ModuleNotFoundError: shared.range_instantiation_policy`
  (issue #1678). Broke all range provisioning in every environment.
- The CI permissions boundary must carry the per-range POLARIS agent carve-out
  and the IAM read permissions the provider needs after role creation
  (`iam:ListAttachedRolePolicies`, `iam:ListInstanceProfilesForRole`)
  (issue #1683, fixes #1681).
- First-deploy migrate race: the deploy waits for an in-service ASG instance
  before migrating (issue #1677). If it still fails, run the manual migrate from
  Phase 4.
- POLARIS agent verify runs host-side because the a14-kali container has no `aws`
  CLI, and the container aws-config needs `sts_regional_endpoints = regional`
  plus an STS host pin (issue #1688).
- Environment parity: a new import-time environment variable must be added to
  `user_data.sh`, the portal SSM parameters, and `deploy_portal.sh` common env,
  or a fresh AWS deploy fails at migrate.
- Range guests can fail SSM when the VPC DNS resolver is not reachable; see the
  guest DNS operator note.

## Progress and traceability

- Track phases with a task list and give the operator running status. Do not run
  the whole thing silently in a subagent.
- File an issue for every new bug found, fix the root cause, and PR it to `dev`.
- Keep a durable scratch record of parameters, decisions, resource ids, and PRs
  so the run survives a context reset.
