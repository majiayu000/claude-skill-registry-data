---
name: Uptick CI Patterns
description: This skill should be used when the user asks to "set up CI", "configure GitHub Actions", "create a workflow", "pin actions", "use ratchet", "set up Claude code review", "configure AWS OIDC", "deploy with tickforge", or mentions GitHub Actions, CI/CD pipelines, or workflow security. Provides Uptick's security-first GitHub Actions patterns.
version: 0.1.0
---

# Uptick CI Patterns

This skill provides guidance for GitHub Actions following Uptick's security-first patterns from [uptick/actions](https://github.com/uptick/actions).

## Core Principles

### Security-First Approach

Avoid external action dependencies where possible. External actions are security risks that can steal credentials. Implement functionality through Python and bash scripts using built-in libraries only.

### Standardization

Use reusable workflows to ensure consistency across the organization. Make it easy to do the right thing and easy to update all pipelines.

### Action Pinning with Ratchet

Pin all actions to SHA for immutability using [Ratchet](https://github.com/sethvargo/ratchet):

```bash
# Install ratchet
go install github.com/sethvargo/ratchet@latest

# Pin all actions in workflows
ratchet pin .github/workflows/*.yaml

# Update pinned versions to latest
ratchet update .github/workflows/*.yaml
```

Pinned format:
```yaml
uses: 'actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683' # ratchet:actions/checkout@v4
```

**Excluding reusable workflows:** Use `# ratchet:exclude` to exclude Uptick reusable workflows from pinning (they are maintained centrally):

```yaml
uses: uptick/actions/.github/workflows/ci.yaml@main  # ratchet:exclude
```

## Uptick Reusable Workflows

### 1. CI Pipeline (`ci.yaml`)

The "God CI Pipeline" supporting 90% of standard use cases:

```yaml
name: CI
on: [push, pull_request]

jobs:
  ci:
    uses: uptick/actions/.github/workflows/ci.yaml@main  # ratchet:exclude
    with:
      python: true
      uv: true
      mise: true
      aws: true
      command: "mise run ci"
    secrets: inherit
```

Key features:
- Python/uv installation and caching
- Mise for task running
- Node.js/pnpm support
- AWS OIDC authentication (no long-lived credentials)
- Docker image building and ECR push
- Tickforge deployment bumping

See `references/uptick-workflows.md` for complete input options.

### 2. Claude PR Review (`claude_review.yaml`)

Automated code review on pull requests:

```yaml
name: Claude Review
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

jobs:
  review:
    uses: uptick/actions/.github/workflows/claude_review.yaml@main  # ratchet:exclude
    secrets:
      CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

Reviews focus on: code quality, security vulnerabilities, performance, test coverage.

### 3. Claude Mention (`claude_mention.yaml`)

Interactive AI assistant triggered by @claude mentions:

```yaml
name: Claude Mention
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  mention:
    uses: uptick/actions/.github/workflows/claude_mention.yaml@main  # ratchet:exclude
    secrets:
      CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

## Workflow Patterns

### AWS OIDC Authentication

Never use long-lived AWS credentials. Configure OIDC:

```yaml
with:
  aws: true
  aws-region: ap-southeast-2
  aws-iam-role-arn: arn:aws:iam::ACCOUNT:role/github-actions-role
```

### Running Tests with Mise

Use mise for consistent task execution:

```yaml
with:
  mise: true
  command: "mise run test"
```

Common mise tasks in `mise.toml`:
```toml
[tasks.ci]
run = "mise run lint && mise run test"

[tasks.test]
run = "uv run pytest"

[tasks.lint]
run = "uv run ruff check ."
```

### Docker Build + Tickforge Deployment

Build and push Docker images, then trigger Tickforge deployment:

```yaml
with:
  docker-enabled: true
  docker-repository: ACCOUNT.dkr.ecr.ap-southeast-2.amazonaws.com/my-app
  docker-image-platforms: "linux/amd64,linux/arm64"
  bump-app: my-app  # Triggers Tickforge deployment
```

The `bump-app` input triggers a deployment bump in Tickforge after the Docker image is pushed.

### Caching Strategy

The CI workflow automatically caches:
- uv dependencies (based on uv.lock)
- pnpm dependencies
- Mise tools

## Compliance Checklist

When setting up CI for a repository:

1. **Pin all actions** - Run `ratchet pin .github/workflows/*.yaml`
2. **Exclude reusable workflows** - Add `# ratchet:exclude` to `uptick/actions` references
3. **Use Uptick reusable workflows** - Prefer `uptick/actions` over custom workflows
4. **No external actions** - Implement custom logic in scripts, not third-party actions
5. **AWS OIDC only** - Never commit long-lived AWS credentials
6. **Enable Claude review** - Add `claude_review.yaml` for automated PR feedback

## Additional Resources

### Reference Files

For detailed configuration options:
- **`references/uptick-workflows.md`** - Complete CI workflow inputs and secrets
- **`references/ratchet-guide.md`** - Ratchet commands and patterns

### Example Files

Working examples in `examples/`:
- **`ci-python-uv.yaml`** - Python project with uv and mise
- **`ci-docker-tickforge.yaml`** - Docker build with Tickforge deployment
