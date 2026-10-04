---
name: insolvia-aws-naming
description: >-
  Repo rule. Name every AWS resource in Insolvia as
  [project]-[env]-[component]-[identifier] — lowercase kebab, environment always
  second, component named for what it serves. Covers the per-resource-type
  patterns, the global-uniqueness suffix S3 needs, the required tags, and which
  resources cannot be renamed without destroying data. Use before creating or
  renaming any AWS resource, writing a new Terraform module, adding a service,
  or widening the deploy role's ARN patterns in infra/envs/ci-trust.
---

# Naming AWS resources

## The pattern

```
[project]-[env]-[component]-[identifier]
```

`insolvia-prod-api` · `insolvia-staging-mailer-ingress` · `insolvia-prod-case-documents-us-east-1`

- **project** — always `insolvia`. This account is single-tenant.
- **env** — `prod`, `staging`, `shared`, or `dev-<machine-short-id>` for a
  developer's own environment. Always the **second** segment, never the last,
  never omitted. There are no `pr-<number>` previews in this repo.
- **component** — what the resource *serves*, not which tier it belongs to.
  `api`, `admin`, `admin-api`, `marketing`, `app`, `cases`. Not `backend`,
  not `frontend`, not `web`.
- **identifier** — only when a component needs more than one instance
  (`...-dlq`, `...-role`). Leave it off otherwise.

Lowercase letters, digits and hyphens only. No underscores, no uppercase, no
spaces — several AWS services reject them and others handle them inconsistently.
Keep names short; per-service character limits are real (IAM roles 64, Lambda
64, S3 63, DynamoDB 255).

**If AWS can generate the name and nothing in our workflow needs to predict it,
let AWS generate it.** A name you never look up is a name that can't drift.

## `shared` is an environment, not an exemption

Account-wide resources — the container repositories, the deploy role, the state
bucket — take `shared` in the env slot: `insolvia-shared-api`,
`insolvia-shared-deploy-role`. They already tag `Environment = "shared"`, so the
name now says what the tag says.

This replaced an earlier carve-out where those resources simply had no env
segment (`insolvia-api`, `insolvia-mailer`). The carve-out read fine in
isolation and was unreadable in a console listing, because
`insolvia-api` sorted nowhere near `insolvia-prod-api` and nothing in the name
said which one was the repository.

## Component names carry meaning — pick the one that's true

The failure this rule exists to prevent is a name that describes the *tier*
rather than the *thing*, because tiers stop being distinguishing the moment a
service has two of them. This repo had `insolvia-web-<env>` (the app's SPA
bucket), `insolvia-web-admin-<env>` (the admin portal's bucket), and
`insolvia-web-<env>` again as the Cognito *app client* — three different things,
one word, and `admin` meanwhile named both the admin portal and its backend API.

Name it after the surface it serves or the job it does:

| Serves | Component |
| --- | --- |
| `api.insolvia.ai` | `api` |
| `admin-api.insolvia.ai` | `admin-api` |
| `admin.insolvia.ai` (the staff portal SPA) | `admin` |
| `app.insolvia.ai` (the Expo app) | `app` |
| `www.insolvia.ai` | `marketing` |
| case rows and their key | `cases` |
| case files in S3 | `case-documents` |
| a queue consumer | the thing it consumes — `api-send`, `feedback` |

## Per-resource-type patterns

Most resources are just `[project]-[env]-[component]`. These need more:

| Resource | Pattern | Example |
| --- | --- | --- |
| **S3 bucket** | `[project]-[env]-[component]-[region]` | `insolvia-prod-marketing-us-east-1` |
| **IAM role** | `[project]-[env]-[component]-role` | `insolvia-prod-api-role` |
| **IAM policy** | `[project]-[env]-[component]-[grant]` | `insolvia-prod-cases-access` |
| **SQS DLQ** | `[project]-[env]-[component]-dlq` | `insolvia-prod-mailer-feedback-dlq` |
| **CloudFront OAC** | `[project]-[env]-[component]-oac` | `insolvia-prod-app-oac` |
| **CloudWatch alarm** | `[project]-[env]-[component]-[condition]` | `insolvia-prod-mailer-ses-bounce-rate` |
| **KMS alias** | `alias/[project]-[env]-[component]` | `alias/insolvia-prod-cases` |
| **Log group** | `/aws/lambda/[function-name]` | derived — never hand-written |
| **SSM parameter** | `/[project]/[env]/[name]` | `/insolvia/prod/api/case-table-name` |

**S3 bucket names are globally unique across all of AWS**, which is why they
alone take a suffix. Use the region code. A short random hash works too, but the
region is deterministic — Terraform can build it from the provider, and a human
reading the console learns something from it. Everything here is `us-east-1`
(the CloudFront ACM requirement), so in practice every bucket ends
`-us-east-1`; take it from `data.aws_region.current.region`, never a literal, so
a future region change cannot leave a lying name behind.

**IAM is where published guidance disagrees with itself.** The article this
convention came from puts role type first (`admin-myapp-prod`) while every other
type in the same table is project-first. We use **project-first everywhere**: a
console sorted by name should group by service, and one exception costs more in
confusion than it buys in readability. This is why the old
`access-insolvia-cases-<env>` and `invoke-insolvia-mailer-<env>` policy names
are gone.

## Tags do the work names can't

Names are constrained, sometimes immutable, and always one-dimensional. Tags are
none of those. **Every resource that supports tagging gets all three:**

| Tag | Value |
| --- | --- |
| `Project` | `insolvia` |
| `Environment` | `prod` / `staging` / `shared` / `dev-<machine-short-id>` |
| `ManagedBy` | `terraform` |

Put them in `local.common_tags` in the environment's `main.tf` and pass them
into every module — that is the existing pattern in every root under
`infra/envs/`.

Ownership is deliberately not a tag here. This is a single-tenant account with
one maintainer, so a constant `Owner` value would carry no information — and the
one place ownership is a real question, `infra/envs/dev` (several machines, one
account), already answers it with the `DeveloperMachineId` / `DeveloperPrincipal`
/ `MachineName` tags that root sets on top of the three above.

**Do not overload the name with what a tag should carry.** Cost centre, ticket,
lifecycle — those are tags. If you're tempted to add a fifth segment, it's
almost certainly a tag.

## The names are load-bearing in IAM — check `ci-trust` before you rename

`infra/envs/ci-trust/main.tf` fences the deploy role by ARN pattern, and those
patterns encode the naming convention. Because env is the **second** segment,
a component-scoped fence needs a wildcard in the middle:

```
arn:aws:s3:::insolvia-*-marketing-*      # not insolvia-marketing-*
alias/insolvia-*-cases                   # not alias/insolvia-cases-*
```

Two of those patterns are not merely scoping — they are controls:
`DenyCaseDataDecryption` (alias-matched) and `DenyAuditLogErasure`
(bucket-matched). **A rename that misses them does not fail the apply. It
silently stops the deny matching**, and the pipeline quietly gains the access
the deny existed to remove. `ci-trust` is human-applied
(`scripts/apply-ci-trust.sh`), so a rename touching any fenced family is a
two-apply change: `ci-trust` first, then the env.

**That first apply must be a UNION of the old and new patterns, not a swap.**
This is the one that is easy to get wrong, because the finished state looks
correct and the plan is clean. Terraform REFRESHES a resource before it
destroys it, so for the single apply that renames a bucket the deploy role
needs to read the OLD name — which the new pattern no longer matches. Swapping
them produced a wall of

```
AccessDenied ... s3:GetBucketVersioning on insolvia-audit-staging
```

for buckets the apply was about to delete, and there is no route to the destroy
that skips the read. So: add the old patterns alongside the new, apply
`ci-trust`, apply the environments, then remove the old patterns in a third
apply. Mark them `TRANSITIONAL` when you add them, or they become permanent.

For a **deny**, keeping both spellings is the safe direction rather than merely
the working one — narrowing a deny to the new name while the old resource still
exists un-protects it for the length of the transition.

S3 is usually the only family that needs this, and the reason is worth
internalising: every other grant is fenced flat (`function:insolvia-*`,
`table/insolvia-*`, `role/insolvia-*`, `alias/insolvia*`) and a flat prefix
matches both spellings by construction. Only the bucket grants are fenced per
COMPONENT — and the component is what moved.

## Before you rename anything: know what it costs

A rename in Terraform is a **destroy and recreate** for most AWS resources.
Some of those are free; some destroy data irrecoverably. Check which you're
touching before you touch it.

**Free — recreated automatically:**
Lambda functions (the image is in ECR), ECR repositories (CI re-pushes), IAM
roles and policies, API Gateways, CloudFront OACs / functions / cache policies,
log groups, alarms, SSM parameters.

**Destroys data — needs an explicit decision, and usually a migration:**

| Resource | What is lost |
| --- | --- |
| Cognito user pool | every account and password. Users cannot be migrated with passwords intact — they must reset |
| DynamoDB table | every row |
| S3 bucket | every object. Names are also not immediately reusable after deletion |
| SQS queue | in-flight messages |
| SES domain identity | verification, until DNS re-propagates — outbound mail fails in the window |

Prod sets `deletion_protection = true` on the Cognito pool and on the case,
firm and admin-audit tables, and `force_destroy = false` on the document and
audit buckets. **A rename apply against prod fails mid-plan on those** — the
protections have to be turned off in their own apply first, and the buckets
emptied. `scripts/rename-teardown.sh` does both, in that order.

CloudFront distributions have no name attribute at all: renaming the *Terraform
address* is free, and a `moved` block makes it a state move rather than a
15-minute replacement of a live distribution.

**Renaming a Terraform resource or module is not the same as renaming the AWS
resource.** Use `moved` blocks for the former; they cost nothing. Only a change
to the `name`/`bucket`/`function_name` argument triggers a replacement.

## Adding a service

Pick the component name to match the surface it serves, pass the root's
`local.common_tags` into the module, and name every resource from the pattern
above. If a component name needs explaining in a comment, it's the wrong
component name.
