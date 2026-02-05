---
name: github-actions-workflows
description: Create and maintain GitHub Actions workflows in .github/workflows
---

# GitHub Actions Workflow Skill (.github/workflows)

Use this skill when creating or maintaining CI/CD automation via GitHub Actions workflows.

## Definition: "When to use this skill"

Create or modify a workflow if you need to:

- run automated tests, linting, or code quality checks
- build and publish Docker images to GHCR
- validate pull requests before merging
- publish releases or create deployment artifacts

## Where workflows live

All workflows live in `.github/workflows/`.

- Each workflow is a single `.yml` file in this directory
- Workflows are triggered by GitHub events (push, pull_request, release, etc.)

## Naming conventions

Use descriptive, kebab-case names:

- `build.yml` — lint, test, build and publish Docker images
- `release-please.yml` — automated release management

## Pinning action versions

**Always pin GitHub Actions to specific commit SHAs**, not floating tags (`v3`, `v4`) or minor versions (`v3.7.1`).

### Why pin to commit SHAs?

- **Security**: Prevents tag hijacking attacks where malicious actors could modify tags
- **Reproducibility**: Ensures exact same action code runs every time
- **Explicit dependencies**: Makes it clear what version is actually being used
- **Auditability**: Easy to review exactly what code is being executed

### How to pin actions to commit SHAs

1. **Find the latest version** using git ls-remote:
   ```bash
   git ls-remote --tags --refs https://github.com/owner/action.git | grep -E 'v3\.' | tail -5
   ```

2. **Get the commit SHA** for the desired version tag

3. **Pin with SHA and version comment**:
   ```yaml
   - uses: docker/setup-buildx-action@f7ce87c1d6bead3e36075b2ce75da1f6cc28aaca # v3.9.0
   ```

### Example: Pinning all actions in a workflow

```yaml
- uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4.3.1

- name: Setup mise
  uses: jdx/mise-action@c37c93293d6b742fc901e1406b8f764f6fb19dac # v2.4.4

- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@f7ce87c1d6bead3e36075b2ce75da1f6cc28aaca # v3.9.0

- name: Login to GitHub Container Registry
  uses: docker/login-action@5e57cd118135c172c3672efd75eb46360885c0ef # v3.6.0

- name: Extract metadata
  uses: docker/metadata-action@318604b99e75e41977312d83839a89be02ca4893 # v5.9.0

- name: Build and push
  uses: docker/build-push-action@4f58ea79222b3b9dc2c8bbdd6debcef730109a75 # v6.9.0
```

### Updating pinned actions

To update to a new version:

1. Find the new commit SHA for the desired version
2. Update both the SHA and the version comment
3. Test the workflow in a branch before merging

## Workflow structure best practices

### Permissions

Be explicit about what the workflow needs:

```yaml
permissions:
  contents: read           # read source code
  packages: write          # push to GHCR
```

### Triggers (on:)

Define what events trigger the workflow:

```yaml
on:
  pull_request:            # on every PR
  push:
    branches:
      - main               # on push to main only
```

### Concurrency

Cancel in-progress runs when a new one is triggered:

```yaml
concurrency:
  group: build-${{ github.ref }}
  cancel-in-progress: true
```

### Jobs structure

- Use `runs-on: ubuntu-latest` for most jobs
- Use `needs: [job1]` to sequence jobs
- Lint and test before building

### Common steps pattern

```yaml
steps:
  - uses: actions/checkout@v4  # Get code
  - name: Setup mise
    uses: jdx/mise-action@v2
  - name: Install dependencies
    run: mise run install
  - name: Run tests
    run: mise run test
```

## Docker image building

Best practices for `docker/build-push-action`:

1. **Use Buildx** for multi-platform builds: `docker/setup-buildx-action`
2. **Login** before pushing: `docker/login-action`
3. **Extract metadata** for tags/labels: `docker/metadata-action`
4. **Build and push**: `docker/build-push-action`
5. **Use caching** to speed up subsequent builds

Tag strategy:
```yaml
tags: |
  type=ref,event=branch           # Branch name
  type=semver,pattern={{version}} # Semantic version
  type=sha,prefix={{branch}}-     # Commit SHA
  type=raw,value=latest,enable={{is_default_branch}}  # Latest on main
```

Push only on main:
```yaml
push: ${{ github.event_name == 'push' && github.ref == 'refs/heads/main' }}
```

## Testing and linting in workflows

Common patterns:

```yaml
- name: Run tests
  run: mise run test

- name: Run linter
  run: mise run lint
```

Use `mise` commands (not direct tool invocations) for consistency with local development.

## Secrets and environment variables

**Never hardcode secrets:**
```yaml
- run: command
  env:
    API_KEY: ${{ secrets.API_KEY }}  # Use GitHub Secrets
```

## Repository-specific notes for yap-on-slack

- **Simple single-purpose tool**: Python script for posting Slack messages
- **Use `mise run`** for all tool invocations (install, test, lint, build)
- **Docker Buildx** is used for building container images
- **GHCR publishing**: Images push to `ghcr.io/echohello-dev/yap-on-slack`
- **Concurrency is important**: Cancel old builds when new ones are triggered

## "Definition of done" checklist

Before committing a workflow:

- [ ] Workflow file named descriptively (kebab-case)
- [ ] All external actions pinned to commit SHAs with version comments (e.g., `@sha # v1.2.3`)
- [ ] Used `git ls-remote` to verify commit SHAs match latest stable versions
- [ ] Permissions explicitly defined (minimal required permissions)
- [ ] Concurrency set up (if applicable)
- [ ] Tests/linting run before build jobs
- [ ] Artifacts uploaded with retention policy (if applicable)
- [ ] Secrets never hardcoded, using `${{ secrets.* }}` pattern
- [ ] Workflow tested in a branch before merging

## Useful commands

```bash
# Validate workflow syntax locally
act -l  # list workflows

# Check for workflow issues
gh workflow view <workflow-name>
gh workflow list
```
