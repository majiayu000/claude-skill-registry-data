---
name: insolvia-aws-auth
description: >-
  How AWS authentication works for the Insolvia repo, locally and in CI. Use
  this WHENEVER you are about to run — or are debugging — anything that touches
  AWS from a developer machine: `terraform plan/apply` against any
  `infra/envs/*`, `docker` build/push to ECR, the `scripts/bootstrap-*` and
  `scripts/dev-aws-*` scripts, `aws` CLI calls, or any local step that needs
  Insolvia's AWS account. Trigger it the moment you see a credential error —
  "No valid credential sources found", "no EC2 IMDS role found", "refreshed,
  but the refreshed credentials are still expired", "InvalidClientTokenId",
  "ExpiredToken", or Terraform/Docker/an SDK reporting no credentials while a
  bare `aws` command works fine — AND whenever `aws sts get-caller-identity`
  shows an account other than 521762924626, or "The config profile (…) could
  not be found": on a machine with more than one AWS account the `default`
  profile may be someone's PERSONAL account. Also consult it before telling the
  user to run any `aws login` / credential-export command, so the advice is
  right the first time. This knowledge is easy to get subtly wrong from memory
  — read it rather than guessing.
---

# AWS authentication in the Insolvia repo

## The one mental model that explains every failure

There are **two credential worlds**, and confusing them causes every symptom below.

1. **The AWS CLI's own world.** `aws` commands read `~/.aws/config`, which on an
   Insolvia dev machine uses the newer **`aws login` session format**
   (`login_session = arn:aws:iam::521762924626:user/…`). This is a browser-based
   sign-in that caches a short-lived session. A bare `aws sts get-caller-identity`
   uses it directly and Just Works.

2. **The SDK / env-var world.** The **Terraform AWS provider** (a Go SDK) and
   **Docker** (pushing to ECR) do *not* understand the `login_session` format.
   They only read the standard credential provider chain, whose top entry is the
   `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` / `AWS_SESSION_TOKEN` environment
   variables. If those aren't set, they fall through to EC2 instance metadata
   (IMDS), which on a laptop isn't there, so they hang and then error.

The bridge between the two worlds is one command:

```bash
eval "$(aws configure export-credentials --format env)"
```

It resolves the CLI session into the three env vars every SDK understands. This
is the same thing `scripts/dev-aws-common.sh`'s `export_temporary_aws_credentials`
does — reuse that helper when a script is already in that family.

**Account:** `521762924626`. **Region:** `us-east-1` everywhere (CloudFront ACM
requirement). Never hard-code, echo, or commit credentials — local uses the CLI
session, CI uses OIDC (below). If a tool lacks credentials it doesn't have, stop
and ask; don't invent a workaround.

## Do I even need the export? — decision table

| Doing this locally | Needs exported env-var creds? |
|---|---|
| `aws …` CLI commands (`s3`, `ecr get-login-password`, `sts`, …) | **No** — the CLI reads its own session natively |
| `terraform plan` / `apply` against `infra/envs/*` | **Yes** — Go SDK can't read the session |
| `docker` build **push** to ECR | **Yes** — plus `aws ecr get-login-password \| docker login …` first |
| Anything via a language SDK (boto3 script, etc.) with no other creds | **Yes** |
| **Anything in CI / GitHub Actions** | **No, and never export** — CI assumes an OIDC role; there are no static keys anywhere |

CI is a different mechanism entirely: workflows authenticate through the
`AWS_ROLE_ARN` OIDC role (`aws-actions/configure-aws-credentials`). Nothing on a
developer machine is involved, and no long-lived keys exist. Don't reach for the
export dance when reasoning about a workflow failure — that's world #1/#2 on a
laptop, not CI.

## The three failure modes, and the exact fix for each

### 1. "No valid credential sources found" / "no EC2 IMDS role found"

`terraform plan` says this while `aws sts get-caller-identity` succeeds two
seconds earlier. Classic world-confusion: Terraform can't read the CLI session.

**Fix:** export first, in the same shell, then run Terraform.

```bash
eval "$(aws configure export-credentials --format env)"
```

### 2. "refreshed, but the refreshed credentials are still expired"

The underlying `aws login` **session has expired**. `export-credentials`
"succeeds" on a dead session but hands back the stale credentials, producing this
opaque message. `aws sts get-caller-identity` will also be failing with "Your
session has expired."

**Fix:** re-authenticate, *then* export.

```bash
aws login ${AWS_PROFILE:+--profile "$AWS_PROFILE"}
```

`aws login` (not `aws sso login` — this repo's config has no `sso_session`
block). It opens a browser. After it, re-run the export from step 1. Keep the
`--profile`: a bare `aws login` refreshes the `default` profile, which on a
multi-account machine is the wrong account (see "The profile").

### 3. A fresh `aws login` still shows no credentials — stale env vars are shadowing it

You just ran `aws login` successfully, but `terraform`, `docker`, or even a
guarded script still reports no/expired credentials. This is the subtle one.

**Cause:** a *previous* `eval "$(aws configure export-credentials --format env)"`
left now-expired `AWS_ACCESS_KEY_ID` etc. **exported in the shell**. Env-var
credentials sit at the *top* of the provider chain, so they win over the freshly
refreshed profile. `aws login` refreshes the profile/session; it does **not**
touch exported env vars. So the good login is being shadowed by dead env vars.

**Fix:** clear them, then let the profile answer (or re-export).

```bash
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_CREDENTIAL_EXPIRATION
```

**Diagnostic to distinguish #2 from #3:** if `env -u AWS_ACCESS_KEY_ID -u
AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN aws sts get-caller-identity` succeeds
but a bare `aws sts get-caller-identity` fails, the profile is fine and stale env
vars are the culprit (#3). If both fail, the session itself is dead (#2 → `aws
login`).

**Implication for scripts you write:** any script doing the export dance should
(a) check the session is alive with `aws sts get-caller-identity` *before*
exporting, so #2 fails loudly instead of opaquely, and (b) if that check fails
while `AWS_ACCESS_KEY_ID` is set, `unset` the AWS_* vars in-process and retry via
the profile, so #3 can't shadow a good login. `scripts/bootstrap-ecr-images.sh`
is the reference implementation of both guards.

**Implication for advice you give the user:** the export pollutes *their* shell
too. If you had them export earlier in a session, and later something breaks
after they re-login, suspect #3 first and have them `unset` — don't send them in
circles re-running `aws login`.

## The profile

Insolvia's account is `521762924626`. **Which profile holds it varies by
machine**: on a single-account machine it's `default`; on a machine that also
holds a personal AWS account, `default` is usually the *personal* one and the
Insolvia session lives under a named profile (e.g. `insolvia`) selected by
`AWS_PROFILE`. Every tool here honours `AWS_PROFILE` — the CLI,
`export-credentials`, Terraform, and the `scripts/dev-aws-*` (which also take
`--profile`) — so when it is set, bare commands are correct and no `--profile`
flag is needed.

**Check the account before anything that writes or costs money** — it is the
one check that catches every variant of this:

```bash
aws sts get-caller-identity --query Account --output text   # must print 521762924626
```

How `AWS_PROFILE` gets set: developers with more than one account export it
from a direnv `.envrc` above the checkout. Your Bash commands run in
non-interactive shells that never fire direnv's prompt hook, so this repo's
SessionStart hook (`.claude/hooks/session-accounts.sh`) loads that environment
into every Bash command and reports the resolved account as an `AWS:` line in
your context. **Read that line first.**

If the account is wrong (or `AWS_PROFILE` is unset and `default` isn't
Insolvia), find the profile that is, without changing any config:

```bash
for p in $(aws configure list-profiles); do
  printf '%s ' "$p"; aws sts get-caller-identity --profile "$p" --query Account --output text 2>&1 | tail -1
done
```

Then prefix your commands with `AWS_PROFILE=<that profile>` (env vars don't
persist between your Bash calls) and tell the human their per-folder setup
didn't load. If no profile maps to `521762924626`, or its session is expired,
**stop and ask** — `aws login --profile <p>` is a browser sign-in the human does.
Never run `aws configure set`, edit `~/.aws/config`, or `aws login` without
`--profile` to "fix" it: that rewrites the developer's other account.

## Quick reference — the whole local flow

```bash
# 1. Make sure the session is alive AND is Insolvia's (re-login if this errors)
aws sts get-caller-identity --query Account --output text   # 521762924626
# or: aws login ${AWS_PROFILE:+--profile "$AWS_PROFILE"}

# 2. Bridge into the SDK/env world (only for terraform / docker / SDKs)
eval "$(aws configure export-credentials --format env)"

# 3. For docker→ECR, also log the daemon in
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin 521762924626.dkr.ecr.us-east-1.amazonaws.com

# 4. Now terraform / docker push / boto3 work in this shell.
#    Creds are short-lived — re-run step 2 (or 1→2) when they expire.
```

Related repo material: `docs/runbooks/aws-bootstrap.md` (the manual applies that
need this), `scripts/dev-aws-common.sh` (`export_temporary_aws_credentials`),
`scripts/bootstrap-ecr-images.sh` (the guarded pattern), and the AWS-credentials
rule in the root `CLAUDE.md`.
