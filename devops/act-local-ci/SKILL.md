---
name: act-local-ci
description: Run GitHub Actions workflows locally with nektos/act to validate CI before pushing.
when_to_use: Reach for this to execute/debug .github/workflows/*.yml locally via `act` before pushing — fast CI iteration. For authoring Azure DevOps pipelines use managing-azure-devops. This skill is GitHub Actions-specific local execution, not pipeline authoring.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Act Local CI Skill

**Quick Reference** - Test GitHub Actions workflows locally using nektos/act

## Mission

Run GitHub Actions workflows locally before pushing to validate CI/CD pipelines, catch errors early, and reduce iteration time. Uses [nektos/act](https://github.com/nektos/act) to simulate GitHub Actions runner environment.

## Core Capabilities

- **Local Workflow Execution**: Run `.github/workflows/*.yml` files locally
- **Job Selection**: Execute specific jobs or entire workflows
- **Event Simulation**: Trigger with push, pull_request, workflow_dispatch events
- **Secret Injection**: Pass secrets securely without committing
- **Matrix Testing**: Test matrix builds before pushing
- **Artifact Handling**: Capture and inspect build artifacts

## Quick Start

```bash
# Run all workflows (default push event)
act

# Run specific workflow
act -W .github/workflows/test.yml

# Run specific job
act -j build

# Simulate pull request event
act pull_request

# Pass secrets
act -s GITHUB_TOKEN=$GITHUB_TOKEN

# List available workflows and jobs
act -l
```

## Prerequisites

```bash
# Install act (macOS)
brew install act

# Install act (Linux)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Docker is required
docker --version  # Must be installed and running
```

## Common Patterns

### Test Before Push
```bash
# Validate test workflow passes
act -j test --dryrun  # Preview what would run
act -j test           # Actually run tests

# If successful, push
git push origin feature-branch
```

### Debug Failing CI
```bash
# Run with verbose output
act -v

# Use specific runner image
act -P ubuntu-latest=catthehacker/ubuntu:act-latest

# Keep container for debugging
act --reuse
```

### Matrix Build Testing
```bash
# Run all matrix combinations
act -j build

# Run specific matrix combination
act -j build --matrix os:ubuntu-latest
```

## Runner Images

| GitHub Runner | Act Default | Recommended |
|---------------|-------------|-------------|
| `ubuntu-latest` | `node:16-buster-slim` | `catthehacker/ubuntu:act-latest` |
| `ubuntu-22.04` | `node:16-buster-slim` | `catthehacker/ubuntu:act-22.04` |
| `ubuntu-20.04` | `node:16-buster-slim` | `catthehacker/ubuntu:act-20.04` |

## Pass/Fail Criteria

**Pass**: Workflow executes successfully locally
- All jobs complete with exit code 0
- Artifacts generated as expected
- No timeout or resource errors

**Fail**: Local execution reveals issues
- Job fails with non-zero exit code
- Missing secrets or environment variables
- Docker resource constraints
- Unsupported GitHub Actions features

## Configuration

```yaml
# .actrc (project root)
-P ubuntu-latest=catthehacker/ubuntu:act-latest
-P ubuntu-22.04=catthehacker/ubuntu:act-22.04
--secret-file .secrets
--env-file .env
```

```bash
# .secrets (gitignored)
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
NPM_TOKEN=npm_xxxxxxxxxxxx
```

## Limitations

- Some GitHub-hosted runner features unavailable locally
- `${{ secrets.GITHUB_TOKEN }}` requires manual token
- Service containers need Docker Compose setup
- Large runner images (2-9GB) on first run

## Performance Target

**Target**: <2 minutes for typical test workflow
- Image pull (first run): 2-5 minutes
- Subsequent runs: <30 seconds startup
- Test execution: Depends on project

## Need More Detail?

**Load**: `skills/act-local-ci/REFERENCE.md` (~20KB)
- Advanced configuration options
- Service container setup
- Troubleshooting common issues
- Integration with ensemble agents
