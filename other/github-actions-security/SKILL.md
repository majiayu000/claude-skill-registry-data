---
name: github-actions-security
description: Harden GitHub Actions workflows against the well-known footguns. Covers SHA-pinned third-party actions, scoped GITHUB_TOKEN permissions, OIDC in place of long-lived cloud credentials, the pull_request_target trap, untrusted-input interpolation, and protected deploy environments. Invoke when adding a new workflow, introducing a third-party action, or migrating from long-lived secrets to OIDC.
---

# GitHub Actions Security

GitHub Actions runs code with access to your secrets, your code, and increasingly your cloud accounts. Most teams ship workflows with the defaults, which are convenient but expose more than necessary. This skill is the working baseline for production-grade Actions usage.

## When to invoke

- Adding a new workflow
- Introducing a third-party action (`uses: someone/some-action@v1`)
- A workflow leaked a secret (cleanup + prevention)
- Migrating from long-lived cloud credentials to OIDC
- Periodic audit of `.github/workflows/`
- Inheriting a repo with unfamiliar workflows

## Rule 1 — Pin third-party actions to commit SHA

`uses: someone/action@v1` looks safe. It's not. Tags and branches can be moved at any time. If the action's maintainer is compromised, every workflow using `@v1` runs the new attacker code on next CI.

**Pin to a commit SHA.** Comment the version for readability:

```yaml
# Bad
- uses: actions/checkout@v4

# Good
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```

For your own org / first-party actions, tag pinning is acceptable because you control the tag. For external actions: SHA pin.

`dependabot` can update SHA pins automatically — turn it on for `.github/workflows/`:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule: { interval: weekly }
```

## Rule 2 — Scope `GITHUB_TOKEN` permissions

`GITHUB_TOKEN` is created per workflow run. Its default permissions are broad — write to repo contents, issues, PRs, packages. Most workflows need read.

**Set the floor at the workflow level, raise per-job only when needed**:

```yaml
name: CI

# Workflow-level default — read-only
permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    # inherits read-only
    steps:
      - uses: actions/checkout@<sha>
      - run: npm test

  release:
    runs-on: ubuntu-latest
    needs: test
    # Raise only for this job
    permissions:
      contents: write           # for creating tags/releases
      packages: write           # for publishing
    steps:
      - uses: actions/checkout@<sha>
      - run: npm publish
```

Or set repo-wide default-restricted in **Settings → Actions → General → Workflow permissions → "Read repository contents and packages permissions"**. Then individual workflows opt in to writes explicitly.

## Rule 3 — OIDC instead of long-lived cloud secrets

Storing `AWS_ACCESS_KEY_ID` / `GCP_SA_KEY` / `CLOUDFLARE_API_TOKEN` as repository secrets means: if a workflow logs them, leaks them, or a malicious action exfiltrates them, the credential is good until you notice and rotate. OIDC eliminates that — GitHub mints a short-lived token per workflow run that your cloud provider trusts based on configurable claims.

**AWS example**:

```yaml
permissions:
  id-token: write          # required for OIDC
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - uses: aws-actions/configure-aws-credentials@<sha>
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-deploy-myrepo
          aws-region: eu-central-1
      - run: aws s3 sync ./dist s3://my-bucket/
```

The IAM role's trust policy restricts which repo + branch can assume it:

```json
{
  "Effect": "Allow",
  "Principal": { "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com" },
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" },
    "StringLike": { "token.actions.githubusercontent.com:sub": "repo:my-org/my-repo:ref:refs/heads/main" }
  }
}
```

GCP, Cloudflare, Azure, HashiCorp Vault, and most modern providers support similar federation. Use it.

## Rule 4 — `pull_request_target` is dangerous by default

`pull_request_target` runs in the context of the **base repo** with **base-repo secrets** — but the workflow file and code can be from the PR. An attacker opens a PR that modifies a workflow to print all secrets, GitHub helpfully runs it with access to those secrets.

```yaml
# Bad — runs PR-author code with repo secrets
on: pull_request_target
jobs:
  test:
    steps:
      - uses: actions/checkout@<sha>
        with: { ref: ${{ github.event.pull_request.head.sha }} }
      - run: npm test    # PR-author code executes with full secret access
```

Patterns:

- **Use `pull_request` (not `_target`)** for CI on untrusted contributions. It runs in PR's fork context, no secrets. This is the right default.
- If you need `pull_request_target` (e.g. for labeling, comment automation), **do not check out PR code**. Only operate on metadata.
- If you must run PR code with secrets (rare, e.g. test against a real DB), **gate behind a manual `workflow_dispatch` or a label that only maintainers can apply**, and require approval via a protected environment.

## Rule 5 — Untrusted-input injection

GitHub Action expressions interpolate strings into shell scripts. Untrusted input that contains `; rm -rf /` becomes that, executed.

```yaml
# Bad — issue title is attacker-controlled
- run: echo "New issue: ${{ github.event.issue.title }}"

# Good — pass through env
- env:
    TITLE: ${{ github.event.issue.title }}
  run: echo "New issue: $TITLE"
```

Anything user-controllable — issue title/body, PR title/body, commit messages, branch names, fork names — must go through `env:` and be referenced as a shell variable. Same for `head_ref`, `head_repository_name`.

## Rule 6 — Reviewing third-party actions

Before you `uses: someone/some-action@<sha>`:

- **What does it do?** Read the source — at the SHA you're pinning. Not just the README.
- **What does it access?** Marketplace listing shows requested permissions; the source shows actual API calls and shell commands.
- **Who maintains it?** Single maintainer with no other repos? Recent ownership transfer?
- **Is there a recent fork that's more maintained?** Sometimes the canonical action is abandoned.
- **What's in its `action.yml`?** `composite` and `node` actions can call other actions; check transitive deps.

A reasonable rule: third-party actions for non-trivial work need a 5-minute review before adoption. Pinning by SHA is necessary but not sufficient.

## Rule 7 — Secrets discipline

- **Repository secrets**: shared across all workflows. Smallest blast radius is per-environment secrets (next bullet).
- **Environment secrets** (Settings → Environments): scoped to specific environments (e.g. `production`), with optional reviewer approval before deployment proceeds.
- **Don't echo secrets**. Even `echo "$MY_SECRET"` will be redacted in logs, but `echo "$MY_SECRET" | base64` will not.
- **`if: github.actor == 'dependabot[bot]'`** workflows: dependabot PRs run with `read-only` `GITHUB_TOKEN` since 2021. Don't grant write back unless you intentionally support auto-merge.
- **Rotate on offboarding** — when a contributor leaves, rotate all secrets they could have seen (which is: every secret the workflows they touched used).

## Rule 8 — Environment protections for deploys

For deploy-to-prod workflows, GitHub Environments provide a real release gate:

```yaml
jobs:
  deploy-prod:
    environment:
      name: production
      url: https://example.com
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
```

In **Settings → Environments → production**:

- **Required reviewers** — one or more humans must approve before the job starts
- **Wait timer** — N minutes before the job can begin (gives time to abort)
- **Deployment branches** — only `main` (or a specific branch list) can deploy to this environment
- **Environment secrets** — production credentials scoped here, not at repo level

## Detecting a leaked secret

If you suspect a workflow leaked a secret:

1. **The secret is burned.** Rotate it before doing anything else.
2. **Search workflow logs.** GitHub retains run logs; check the redaction worked — search for the secret value (now-rotated) across the last N days of runs.
3. **Check if the run was visible to forks/PRs** — public repos have public logs.
4. **Audit `secrets` references** across all workflows — any `echo`, `printenv`, `env`, `cat ~/.env`, `xxd`, `base64` near a secret is a smell.
5. **Add CodeQL or pattern-based scanning** for known patterns (echoing env, writing env to artifacts).

## Workflow audit script

```bash
#!/usr/bin/env bash
# Run inside a repo
echo "=== Unpinned third-party actions (uses: org/action@tag) ==="
grep -rE 'uses:\s+[^a-z]*([a-z0-9_-]+)/([a-z0-9_-]+)@(v[0-9]|main|master)' .github/workflows/ \
  | grep -vE 'uses:\s+(actions|github)/' || echo "none"

echo "=== Workflows without explicit permissions ==="
for f in .github/workflows/*.{yml,yaml}; do
  [ -f "$f" ] || continue
  grep -q '^permissions:' "$f" || echo "$f"
done

echo "=== Workflows using pull_request_target ==="
grep -lE '^\s*pull_request_target' .github/workflows/*.{yml,yaml} 2>/dev/null || echo "none"

echo "=== Workflows accessing secrets ==="
grep -lE 'secrets\.[A-Z_]+' .github/workflows/*.{yml,yaml} 2>/dev/null

echo "=== Workflows that might echo env ==="
grep -rE 'echo.*\$|printenv|env\s*$' .github/workflows/ 2>/dev/null | head -10
```

## Checklist for any new workflow

- [ ] Third-party actions pinned to commit SHA, with version comment
- [ ] `permissions:` block set, read-only by default
- [ ] No `pull_request_target` (or, if needed, doesn't check out PR code)
- [ ] No `${{ }}` interpolation of user-controlled strings into shell — uses `env:` instead
- [ ] If touching cloud, uses OIDC not long-lived secrets
- [ ] Deploy jobs use a protected environment with required reviewers
- [ ] No secrets echoed, base64-ed, or otherwise transformed before output
- [ ] If untrusted code runs (PR CI), no production secrets are in scope
- [ ] Dependabot enabled for `github-actions`

## What this skill will not do

- Help bypass GitHub authentication or exfiltrate secrets from repos you do not own
- Endorse `pull_request_target` + PR-code checkout for general CI
- Recommend running CI with secrets accessible to every step "for convenience"
