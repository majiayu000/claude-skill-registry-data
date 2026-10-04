---
name: insolvia-deploy-role-permissions
description: >-
  How to change what the Insolvia CI deploy role is allowed to do — and why
  those changes can't be applied by CI. Use this WHENEVER a change touches the
  GitHub Actions deploy role's IAM permissions: editing
  infra/envs/ci-trust/main.tf (the OIDC provider / insolvia-shared-deploy-role
  role / its policy), or diagnosing a deploy that fails with an IAM
  AccessDenied. Trigger it the moment you see "not authorized to perform:
  <service>:<Action>" / "no identity-based policy allows" in a staging, prod,
  or shared apply, or "AccessDenied" on iam:PutRolePolicy in the
  Infra · Terraform apply · Shared run, or any time you're about to add an IAM
  action so the pipeline can create/modify some AWS resource. Also consult it
  before telling the user "just merge it" for anything that grants the pipeline
  a new permission — because that specific change needs a human-run apply, and
  forgetting that sends everyone in circles. Read it rather than guessing;
  getting the apply order wrong around the trust anchor can lock CI out of AWS.
---

# Changing the CI deploy role's permissions (Insolvia)

## The rule in one line

**CI cannot grant itself AWS permissions. A human admin must apply the change.**
When a deploy fails on an IAM `AccessDenied`, the fix is almost always: add the
action to the deploy role's policy, merge, then a human runs
`scripts/apply-ci-trust.sh`. CI applying it would fail by design.

## Why — the trust anchor and its self-deny

The deploy role (`insolvia-shared-deploy-role`) and the GitHub OIDC provider it's
assumed through live in their own Terraform root, **`infra/envs/ci-trust`**,
separate from everything CI applies. That root's policy contains an explicit
`Deny` (`DenySelfPrivilegeEscalation`) on `iam:PutRolePolicy` (and friends)
targeting the role's *own* ARN. In IAM an explicit deny beats every allow, so:

- A `terraform apply` of `ci-trust` run **as the deploy role** (i.e. from CI)
  cannot modify the role's permissions → `AccessDenied`.
- A `terraform apply` run **as a human admin** (your `aws login` session) is not
  subject to that deny → it works.

Same Terraform, same state, different identity. That's the security property:
a privilege change to the pipeline can't take effect from merged code alone —
someone holding admin has to consciously apply it. So there is deliberately **no
`ci-trust-*.yml` workflow**. (Full reasoning: `docs/runbooks/aws-bootstrap.md` §
"The ci-trust anchor"; `docs/reference/terraform.md`.)

## The two signals that mean "this needs a human ci-trust apply"

1. **A deploy fails with an IAM AccessDenied.** In an `api/mailer/marketing/
   app-<env>.yml` or `Infra · Terraform apply · Shared` run:
   `AccessDeniedException: … not authorized to perform: <service>:<Action> …
   no identity-based policy allows …`. The deploy role is missing that action.
2. **A PR edits the deploy role's policy** (`infra/envs/ci-trust/main.tf`,
   `data.aws_iam_policy_document.github_permissions`). The post-merge
   `Infra · Terraform apply · Shared` will NOT apply it (that's `shared`, a
   different root now) — and nothing else auto-applies `ci-trust`, so the grant
   is inert until a human applies it.

When you see either, don't tell the user "merge and it'll deploy." Tell them:
merge, then run `scripts/apply-ci-trust.sh`, then re-run the deploy.

## Adding a permission — the workflow

1. **Find the exact missing action** from the error (`<service>:<Action>`), and
   what resource it targets. Watch for the subtlety that bit us repeatedly:
   an action may authorize against a *different resource ARN* than you expect.
   - `lambda:CreateEventSourceMapping` carries a FunctionName, so AWS populates
     the `lambda:FunctionArn` condition key — scope it by that **condition**
     (`function:insolvia-*`), which is the real fence and works.
   - The by-UUID mapping actions — `lambda:GetEventSourceMapping`,
     `UpdateEventSourceMapping`, `DeleteEventSourceMapping`, `ListTags`,
     `TagResource`, `UntagResource` — must be granted on `resources = ["*"]`.
     Two traps here, both cost a round-trip: (a) a `FunctionArn` condition
     DENIES them (the request carries no function ARN, so the key is absent);
     (b) scoping by resource to `event-source-mapping:*` ALSO denies them —
     despite the AWS Service Authorization Reference listing an
     `eventSourceMapping` resource type, IAM evaluates these against `*` at
     runtime (the deny reads "...on resource: * because no identity-based
     policy allows..."). `"*"` is not a real widening: these actions are only
     valid on event source mappings, and in a single-tenant account `"*"` and
     `event-source-mapping:*` confer identical access — `"*"` is just the one
     IAM honors. Trust the `on resource: *` in the deny over the SAR table.
   - Creating a SecureString SSM param needs KMS (`kms:Encrypt`/`Decrypt` via
     `kms:ViaService = ssm.<region>.amazonaws.com`), not just `ssm:*`.
2. **Scope it tightly**, matching the file's style: prefer an ARN pattern
   (`insolvia-*`) or a condition over `resources = ["*"]`. Explain *why* in a
   comment — that file documents the reasoning for every grant.
3. **Edit `infra/envs/ci-trust/main.tf`**, then `terraform -chdir=infra/envs/
   ci-trust validate` + `terraform fmt`.
4. **Merge**, then have the user run `scripts/apply-ci-trust.sh` (credential
   dance + plan review + apply — it refuses if run as the deploy role itself).
5. **Re-run the failed deploy.**

Each of these is a round-trip (merge + human apply + redeploy), so when you
already know several related actions will be needed, grant the coherent set at
once rather than discovering them one apply at a time — but keep each grant
scoped and explained.

## Do NOT

- Remove or weaken `DenySelfPrivilegeEscalation` / `DenyTrustAnchorMutation` to
  "make CI able to apply it." That deletes the entire security property.
- Add a `ci-trust` deploy workflow. Same reason.
- `terraform destroy` or blindly `apply` ci-trust without reading the plan —
  a destroy/replace of the role or OIDC provider locks CI out of AWS. The
  script guards this, but the caution stands for bare commands.

Credential mechanics for the local apply (the `aws login` session vs. the env
vars Terraform needs, and the stale-var trap) live in the **`insolvia-aws-auth`** skill.
