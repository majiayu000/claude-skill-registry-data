---
name: operate-aws
description: Use when operating AWS by CLI — SSO profiles, explicit profile and region, caller-identity check first, least privilege without long-lived keys, CloudTrail and cost lookups, Session Manager over SSH, CDK version skew avoided.
---

# Operate AWS

Read-only by default. **Never change prd by hand when the resource is IaC-managed; change the code
and promote it** ([set-up-terraform-pipeline](../../infra/set-up-terraform-pipeline/SKILL.md)).
Every command names its `--profile` and `--region` explicitly — no defaults, no surprises.

## 1. Audit — who am I, and where (change nothing)

```bash
aws --version
aws sts get-caller-identity --profile <profile> --region <region>     # FIRST — account, user or role
aws configure list --profile <profile>                                 # region and its source
aws configure list-profiles                                            # SSO profiles that exist
```

`get-caller-identity` answers the three questions that break everything when wrong: which
account, which principal, which permission set. Run it before anything else, every session.
Organizations view (management or delegated admin profile only):
`aws organizations list-accounts --profile <mgmt-profile>`.

## 2. Decide

- **Read-only investigation (default)** — `describe-*`, `list-*`, CloudTrail lookups, cost calls.
- **The resource is IaC-managed** (Terraform state, CDK stack, CloudFormation stack) — change the
  code and promote it. A hand edit drifts from the stack and the next deploy reverts it or fails.
- **One-off CLI change with a record** — security-group closing, tag fix, snapshot cleanup. Exact
  command and JSON output into the ticket; the revert named before running.

## 3. Detect the track

| Signal | Track | Then |
|---|---|---|
| `tofu -chdir=terraform/envs/<env> state list \| grep aws_`, or the resource is in `*.tf` | Terraform | Read-only here; change via [set-up-terraform-pipeline](../../infra/set-up-terraform-pipeline/SKILL.md) |
| `cdk.json` / `cdk.out` in the repo | CDK | Change the app code, `cdk diff`, deploy through the pipeline |
| `aws cloudformation list-stacks` (step 1 profile) shows the stack | CloudFormation | Change the template, not the resource |
| None of the above | CLI-managed | One-off change with a record |

## 4. Install only what is missing

```bash
brew install awscli                                  # verify version before pinning (../_shared/stack-versions.md)
brew install --cask session-manager-plugin           # for aws ssm start-session
npm install -g aws-cdk                               # only for CDK repos — keep in lockstep with aws-cdk-lib
brew install aws-sam-cli                             # only for serverless repos
```

Optional profile helpers: `granted`, `aws-vault` — [cli-toolbox](../_shared/cli-toolbox.md).

## 5. Do the work

**Sign in through SSO, one profile per account and role:**

```bash
aws configure sso                          # once — wizard writes a named profile
aws sso login --profile <profile>
aws sts get-caller-identity --profile <profile> --region <region>
```

**No long-lived access keys.** If a tool needs env vars, export into a subshell only:

```bash
( eval "$(aws configure export-credentials --profile <profile> --format env)" && <tool-command> )   # subshell: the exports die with it, nothing lands in argv
```

**CloudTrail — "who changed what":**

```bash
aws cloudtrail lookup-events --lookup-attributes AttributeKey=ResourceName,AttributeValue=<name> \
  --profile <profile> --region <region> --query 'Events[].{time:EventTime, who:Username, what:EventName}' --output table
```

**Cost:**

```bash
aws ce get-cost-and-usage --time-period Start=<yyyy-mm-dd>,End=<yyyy-mm-dd> --granularity MONTHLY \
  --metrics UnblendedCost --profile <billing-profile>     # billing access lives on the payer/management account
```

**Session Manager, not SSH:**

```bash
aws ssm describe-instance-information --query 'InstanceInformationList[].{id:InstanceId, name:PingStatus}' \
  --profile <profile> --region <region> -o table
aws ssm start-session --target <instance-id> --profile <profile> --region <region>
```

**Tagging** (group and audit by tags, same scheme as Azure): `aws resourcegroupstaggingapi
get-resources --tag-filters Key=env,Values=prd --profile <profile> --region <region>`.

**Region trap:** the console and the CLI each remember a region, separately. "The instance is
gone" almost always means "the instance is in another region" — check `aws configure get region
--profile <profile>` and the console's region selector before concluding anything.

**CDK skew:** the CDK CLI and `aws-cdk-lib` must move together — a lib bump with an old CLI (or
the reverse) fails on cloud-assembly schema mismatch. Bump both in one PR.

**Organizations:** Identity Center administration works only from the management account or a
delegated admin account. The AWS MCP server, when present, is preferred for exploration; scripts
stay on the CLI.

## 6. Wire

- **CI access to AWS** is an OIDC role per environment trusting
  `token.actions.githubusercontent.com` with `sub = repo:<org>/<repo>:environment:<env>` —
  generated per pipeline run, no keys: [set-up-terraform-pipeline](../../infra/set-up-terraform-pipeline/SKILL.md).
- **Keys and secrets** never in `~/.aws/credentials` for humans — SSO profiles instead;
  anything that must persist goes to [manage-secrets](../../infra/manage-secrets/SKILL.md).
- **Account IDs and role names** are identifiers, not secrets — real values in the IaC repo's
  env config, placeholders in docs and tickets.
- Tools and versions: [cli-toolbox](../_shared/cli-toolbox.md), [stack-versions](../_shared/stack-versions.md).

## 7. Verify

```bash
aws sts get-caller-identity --profile <profile> --region <region> --query Account -o tsv | grep -q <account-id> && echo right-account
aws configure get region --profile <profile>          # the region you intended
aws ce get-cost-and-usage --time-period Start=<yyyy-mm-dd>,End=<yyyy-mm-dd> --granularity MONTHLY \
  --metrics UnblendedCost --profile <billing-profile> --query 'ResultsByTime[0].Total.UnblendedCost.Amount' -o tsv
aws resourcegroupstaggingapi get-resources --tag-filters Key=env,Values=prd --profile <profile> --region <region> --query 'ResourceTagMappingList | length(@)'
```

Expected: `right-account`, the intended region, a cost figure, and a tag count you can explain.
After a session: no keys exported in the current shell (`env | grep AWS_` is empty, or scoped to
the subshell that already exited).

## References
- [aws-patterns.md](./aws-patterns.md): the traps — identity-first, region mismatch, key-free
  auth, OIDC role trust, Session Manager, CDK lockstep, Identity Center admin scope.
- [cli-toolbox](../_shared/cli-toolbox.md), [stack-versions](../_shared/stack-versions.md).
- [manage-secrets](../../infra/manage-secrets/SKILL.md),
  [set-up-terraform-pipeline](../../infra/set-up-terraform-pipeline/SKILL.md).
- [security-baseline](../../core/_shared/security-baseline.md).
