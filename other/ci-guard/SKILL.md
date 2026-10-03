---
name: ci-guard
version: "1.0"
description: Use when starting work in a repository under repositories/ that may lack CI configuration. Detects missing CI workflows (GitHub Actions, GitLab CI, CircleCI) and alerts the user to add one. Skips repos marked as research-only.
---

# CI Guard

Repositories benefit from CI, but this skill is advisory. It checks for CI configuration and alerts when it is missing, while allowing research, prototypes, and intentionally local projects.

## When to Activate

- At session start, after repository status is reported
- When a user clones or creates a new repo under `repositories/`
- When running `/verify` or `/quality-gate` in a repo without CI

## How to Check

Run the check script against any repo:

```bash
uv run skills/ci-guard/scripts/check-ci.py <repo-path>
```

The script checks for common CI indicators and the research exemption.

## CI Indicators (any one is sufficient)

| Provider | Path |
|----------|------|
| GitHub Actions | `.github/workflows/` (with at least one `.yml`/`.yaml`) |
| GitLab CI | `.gitlab-ci.yml` |
| CircleCI | `.circleci/config.yml` |
| Jenkins | `Jenkinsfile` |
| Travis | `.travis.yml` |
| Azure | `azure-pipelines.yml` |

## Research Exemption

A repo is exempt from the CI requirement if:

1. A `.research` file exists in the repo root, OR
2. `pyproject.toml` contains `purpose = "research"` in `[project.optional]` or as a comment marker

To mark a repo as research: `touch <repo>/.research`

## Alert Behavior

When CI is missing and the repo is not research:

1. **Warn clearly** at session start: "This repo has no CI configuration."
2. **Suggest a starter workflow** based on the detected stack (Python/Node/Rust/Go)
3. **Reference the basecamp's own CI** (`.github/workflows/ci.yml`) as a working template
4. **Do not block work** - this is an alert, not a gate

## Starter Templates

### Python (uv-based, matching basecamp conventions)

```yaml
name: CI
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv python install 3.12
      - run: uv sync --group dev
      - run: uv run ruff check .
      - run: uv run ruff format --check .

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv python install 3.12
      - run: uv sync --group dev
      - run: uv run pytest -v
```

### Node.js

```yaml
name: CI
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run lint
      - run: npm test
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting CI on quick prototype repos | Use `.research` file for true prototypes, add CI for everything else |
| Adding CI but not running tests | CI without tests is a false safety net - at minimum lint |
| Blocking the user from working | This is an alert, not a blocker - warn and continue |
