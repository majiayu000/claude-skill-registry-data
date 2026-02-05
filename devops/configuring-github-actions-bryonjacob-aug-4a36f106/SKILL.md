---
name: configuring-github-actions
description: Use when setting up GitHub Actions CI/CD for pull request checks - provides workflow templates for Python, JavaScript, and polyglot projects that run quality gates on every PR
---

# Configuring GitHub Actions

## Purpose

PR checks workflow running `just check-all` on every PR/push. All templates at `.github/workflows/pr-checks.yml`.

## Python Template

```yaml
name: PR Checks

on:
  pull_request:
    branches: [main, master]
  push:
    branches: [main, master]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: extractions/setup-just@v2

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: |
          uv venv .venv
          source .venv/bin/activate
          uv pip install -e ".[dev]"

      - name: Run checks
        run: |
          source .venv/bin/activate
          just check-all

      - name: Upload coverage
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: htmlcov/
```

## JavaScript Template

```yaml
name: PR Checks

on:
  pull_request:
    branches: [main, master]
  push:
    branches: [main, master]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: extractions/setup-just@v2

      - name: Setup pnpm
        uses: pnpm/action-setup@v3
        with:
          version: 8

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install

      - name: Run checks
        run: just check-all

      - name: Upload coverage
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/
```

## Polyglot Template

```yaml
name: PR Checks

on:
  pull_request:
    branches: [main, master]
  push:
    branches: [main, master]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: extractions/setup-just@v2

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Setup pnpm
        uses: pnpm/action-setup@v3
        with:
          version: 8

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: just dev

      - name: Run checks
        run: just check-all

      - name: Upload coverage (Python)
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: python-coverage
          path: api/htmlcov/

      - name: Upload coverage (JS)
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: js-coverage
          path: web/coverage/
```

## Matrix Testing

```yaml
strategy:
  matrix:
    python-version: ['3.11', '3.12']
    node-version: ['20', '21']
steps:
  - name: Set up Python ${{ matrix.python-version }}
    uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```

## Setup

```bash
mkdir -p .github/workflows
# Copy template to .github/workflows/pr-checks.yml
git add .github/workflows/pr-checks.yml
git commit -m "chore: add GitHub Actions PR checks"
git push
```

## Branch Protection

**Settings → Branches → Add rule:**
- ✅ Require status checks to pass
- ✅ Require branches up to date
- ✅ Select `check` job
- ✅ Require conversation resolution
- ✅ No bypass

## Useful Patterns

**Skip docs-only:**
```yaml
on:
  pull_request:
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

**Main-only expensive tests:**
```yaml
- name: Integration tests
  if: github.ref == 'refs/heads/main'
  run: just test-integration
```

**Manual trigger:**
```yaml
on:
  pull_request:
  push:
  workflow_dispatch:  # Adds "Run workflow" button
```

**Security - pin versions:**
```yaml
- uses: actions/checkout@v4  # ✅ Good
- uses: actions/checkout@main  # ❌ Bad
```

**Limit permissions:**
```yaml
permissions:
  contents: read
  pull-requests: write
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Just not found | Add `extractions/setup-just@v2` |
| Permission denied | Add `chmod +x` before script |
| Cache miss | Verify lock files exist |
| CI-only failures | Match versions locally |

**Debug output:**
```yaml
- run: |
    python --version
    node --version
    just --version
    ls -la
```

**Enable debug:** Re-run jobs → "Enable debug logging"
