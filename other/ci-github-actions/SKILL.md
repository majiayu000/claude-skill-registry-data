---
name: ci-github-actions
description: >
  Design, harden, and optimize automated CI/CD workflows using GitHub Actions.
  Use when writing workflow YAML files, configuring matrix builds, implementing
  dependency caching, locking workflow permissions to least privilege, authenticating
  cloud providers via OIDC, or preventing pull_request_target security vulnerabilities.
compatibility: >
  Agent Skills-compatible coding agents authoring or auditing GitHub Actions workflows.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "github-actions, ci-cd, automation, oidc, security, caching, devops"
  topics: "devops, security, devtools"
---

# GitHub Actions CI/CD Engineering and Security

GitHub Actions provides workflow automation directly within GitHub repositories. High-quality workflow engineering requires strict adherence to the principle of least privilege for `GITHUB_TOKEN` permissions, pinning action versions to full commit SHAs, utilizing fast dependency caching, and defending against untrusted pull request execution attacks.

## Core Rules

1. **Set top-level `permissions: {}` by default**: Grant zero permissions at the workflow root; declare only the specific read/write permissions needed inside each individual job.
2. **Pin third-party actions to full commit SHAs**: Tag names (e.g. `@v4`) are mutable and can be hijacked if an upstream action repository is compromised. Pin to 40-character commit hashes.
3. **Never use `pull_request_target` with checked-out PR code**: `pull_request_target` runs in the context of the base branch with access to repository secrets. Checking out and running untrusted code from a fork allows arbitrary secret exfiltration ("Pwn Request").
4. **Authenticate to clouds via OIDC**: Never store long-lived cloud credentials (e.g. `AWS_ACCESS_KEY_ID`). Use OpenID Connect (OIDC) with short-lived tokens.
5. **Enforce concurrency cancellation**: Cancel obsolete in-progress CI runs when a developer pushes new commits to an open pull request.

---

## 1. Canonical Production CI Workflow (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# Default: Zero permissions
permissions: {}

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

jobs:
  lint-and-typecheck:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    permissions:
      contents: read # Only needs to read source code
    steps:
      - name: Checkout Code
        uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
        with:
          persist-credentials: false

      - name: Setup uv and Python
        uses: astral-sh/setup-uv@1edb512b7d057e84126f29e00020d6fa66192949 # v5.1.0
        with:
          version: "latest"
          enable-cache: true

      - name: Run Ruff Lint
        run: uv run ruff check .

      - name: Run Mypy Type Check
        run: uv run mypy src/

  test-matrix:
    name: Test Matrix (Python ${{ matrix.python-version }})
    needs: lint-and-typecheck
    runs-on: ubuntu-latest
    permissions:
      contents: read
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - name: Checkout Code
        uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
        with:
          persist-credentials: false

      - name: Setup uv
        uses: astral-sh/setup-uv@1edb512b7d057e84126f29e00020d6fa66192949
        with:
          python-version: ${{ matrix.python-version }}
          enable-cache: true

      - name: Run Pytest
        run: uv run pytest --cov=src --cov-report=xml

      - name: Upload Test Coverage Artifact
        uses: actions/upload-artifact@5d5d22a31266ced268874388b861e4b58bb5c2f3 # v4.3.1
        with:
          name: coverage-py${{ matrix.python-version }}
          path: coverage.xml
          retention-days: 7
```

---

## 2. Secure Cloud Authentication with OIDC (No Static Keys)

Authenticate to AWS, GCP, or Azure without saving long-lived credentials in GitHub Secrets:

```yaml
jobs:
  deploy-production:
    name: Deploy via AWS OIDC
    runs-on: ubuntu-latest
    permissions:
      id-token: write # Required for requesting the OIDC JWT token
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11

      - name: Configure AWS Credentials via OIDC
        uses: aws-actions/configure-aws-credentials@e3ddf4a3c70b81802fe9d78caab7756e4ed1d742 # v4.0.2
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsDeploymentRole
          aws-region: eu-central-1

      - name: Sync Artifacts to S3
        run: aws s3 sync ./dist s3://my-production-artifacts/
```

---

## 3. Defending Against `pull_request_target` Exploits

| Event Trigger | Context | Has Secrets? | Code Source | Risk Level |
| :--- | :--- | :--- | :--- | :--- |
| `pull_request` | Fork branch | **NO** (Safe) | Fork PR code | **Low**: Untrusted code runs without secrets |
| `pull_request_target` | Base repository | **YES** (Dangerous) | Base repo (by default) | **CRITICAL**: If you check out PR code (`ref: ${{ github.event.pull_request.head.sha }}`), fork code executes with repo secrets! |

**Rule**: Never checkout untrusted fork code in a `pull_request_target` job that accesses secrets or write permissions.

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Security / CI Risk | Correct Practice |
| :--- | :--- | :--- |
| Default `permissions: write-all` | Stolen token in compromised dependency can push to repository | Declare `permissions: {}` at top level |
| Floating `@v4` tags for actions | Supply chain attack if third-party action tag is redirected | Pin to commit SHA: `uses: action@<commit-hash>` |
| Storing static AWS access keys in secrets | Long-lived keys leaked if job output is compromised | Use short-lived OIDC tokens (`aws-actions/configure-aws-credentials`) |
| No concurrency group defined | Multiple pushes on PR run simultaneously, wasting runners | Use `concurrency` with `cancel-in-progress: true` |

---

## 5. Verification Checklist

- [ ] Top-level `permissions: {}` configured.
- [ ] Third-party actions pinned to full 40-character commit SHAs.
- [ ] No static cloud credentials stored in secrets (OIDC used instead).
- [ ] Concurrency configuration cancels redundant in-progress PR builds.
- [ ] `persist-credentials: false` set on `actions/checkout`.
