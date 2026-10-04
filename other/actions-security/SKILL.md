---
name: actions-security
description: Security hardening for GitHub Actions workflows with a least-privilege posture — default-deny permissions ({} then minimal per-job scopes), SHA-pinning every third-party action, avoiding pull_request_target (and the safe trusted-event allowlist pattern when an elevated trigger is unavoidable), preventing expression/script injection via env indirection, explicit secrets (no inherit), and OIDC over long-lived keys. Use when writing or reviewing GitHub Actions workflows for security, locking down permissions or GITHUB_TOKEN, deciding whether pull_request_target is safe, handling untrusted PR input or secrets, or pinning actions.
license: MIT
---

# GitHub Actions security posture

A reusable workflow cannot constrain how a consumer wires its trigger, and a CI workflow runs on
code a stranger proposed. Treat every workflow as reachable by an untrusted contributor and apply
least privilege. These rules are enforced mechanically by the `actions-validate` skill (actionlint +
zizmor) and CodeQL; the authoring conventions they assume live in `actions-style`. For attack
anatomy and extended examples, see [reference.md](reference.md).

## 1. Default-deny permissions

Declare `permissions: {}` at the top level and grant each job only the scopes it needs. Never use
`permissions: write-all`, and never rely on the repository default token (it can be broad).

```yaml
permissions: {} # deny everything by default
jobs:
  build:
    permissions:
      contents: read # the minimum: check out the repo
```

A job that uploads code-scanning results adds `security-events: write`; one that comments on a PR
adds `pull-requests: write`. Grant at the job level so a compromised step holds only that job's
token. A reusable workflow's jobs can never exceed the **caller's** grant — keep that ceiling tight.

## 2. Pin every third-party action to a full commit SHA

A tag (`@v4`) or branch (`@main`) is mutable: whoever controls the action's repo can repoint it at
new code that then runs with your token. Pin to a full 40-character commit SHA with the version in a
comment — for first-party actions too.

```yaml
- uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3
```

Keep pins fresh with Renovate's `github-actions` manager so updates arrive as reviewable PRs:

```json5
{
  extends: ["config:recommended"],
  minimumReleaseAge: "7 days",
}
```

## 3. Avoid `pull_request_target`

`pull_request_target` runs in the **base** repository's context — with repository secrets and a
read/write `GITHUB_TOKEN` — while the pull request comes from an untrusted fork. Check out and run
the PR's head code under it and a fork author can exfiltrate those secrets (the "pwn request"). So:

- **Test PR code with `pull_request`**, not `pull_request_target`. Fork PRs then get a read-only
  token and no secrets — safe by construction.
- If you genuinely need base context (label, size, or comment on a PR), run **no** PR-controlled
  code and never check out the PR head. The org's `merge-notice` caller uses `pull_request_target`
  safely because it only calls the API — it checks out and runs nothing.
- For privileged build/release jobs that a fork-controllable event could reach, gate them on a
  positive **trusted-event allowlist** so the path fails closed:

  ```yaml
  if: ${{ contains(fromJSON('["push","workflow_dispatch","schedule"]'), github.event_name) }}
  ```

## 4. Prevent expression/script injection

Never interpolate attacker-controlled text — a PR title, branch name, or comment body — directly
into a `run:` script. The value is substituted before the shell runs, so `$(...)` or backticks in a
PR title execute as code. Pass it through a quoted environment variable and reference the variable:

```yaml
# WRONG — the title is injected into the shell
- run: echo "Title: ${{ github.event.pull_request.title }}"

# RIGHT — the title is data in the environment, never code
- env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: echo "Title: $PR_TITLE"
```

## 5. Handle secrets explicitly

- Pass secrets to a reusable workflow by name through `secrets:`; never `secrets: inherit`, which
  hands over every secret in the repo.
- Don't `echo` secrets or write them to logs/artifacts; GitHub masks known secret values but not
  values derived from them.
- Prefer **OIDC** (`permissions: id-token: write` plus the cloud's federation) to authenticate to
  AWS/GCP/Azure over storing long-lived access keys as secrets.

## 6. Know the `GITHUB_TOKEN`

On a fork pull request the `GITHUB_TOKEN` is read-only and secrets are withheld; on a same-repo
event it carries whatever `permissions:` you granted. Scope it down rather than up, and gate
same-repo-only logic (label arming, review handling) so fork PRs skip it.

## 7. Enforce mechanically

Run the `actions-validate` loop (actionlint + zizmor) locally before committing, and scan `actions`
with CodeQL in CI (the `actions-reusable-workflows` skill wires the shared `security.yaml`). Treat
their findings — unpinned actions, injectable expressions, over-broad permissions — as violations,
not suggestions.
