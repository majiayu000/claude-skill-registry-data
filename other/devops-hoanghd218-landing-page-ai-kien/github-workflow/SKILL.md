---
name: "github-workflow"
description: "GitHub Actions optimization patterns and deployment workflows for static sites. Use when creating CI/CD pipelines, optimizing builds, or troubleshooting GitHub Actions."
---

# GitHub Workflow Patterns

## Deployment Workflow Template

For static site deployment to GitHub Pages:

```yaml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci
      - run: npm run build

      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

**Critical settings:**
- `permissions`: Required for GitHub Pages deployment
- `concurrency`: Prevents simultaneous deployments
- `cache: 'npm'`: Caches dependencies automatically

## Caching Strategy

### Automatic Dependency Caching

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # Automatic npm cache
```

**How it works**: Caches `node_modules` based on `package-lock.json` hash.

**When cache is invalidated**: When `package-lock.json` changes.

### Build Output Caching

For expensive build steps:

```yaml
- uses: actions/cache@v3
  with:
    path: |
      .next/cache
      .astro/cache
    key: ${{ runner.os }}-build-${{ hashFiles('**/*.ts', '**/*.tsx') }}
    restore-keys: |
      ${{ runner.os }}-build-
```

**Use when**: Build takes >1 minute and can use previous artifacts.

## Optimization Checklist

- [ ] Dependencies cached (`cache: 'npm'`)
- [ ] Build artifacts cached if applicable
- [ ] Fast jobs run first (lint before build)
- [ ] Jobs run in parallel where possible
- [ ] Fail fast enabled for matrix builds
- [ ] Minimal checkout depth if history not needed

## Conditional Execution

### Run on specific paths

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'content/**'
      - 'package.json'
```

**Use when**: Large repo, only want to run on relevant changes.

### Skip CI

Include `[skip ci]` in commit message to skip workflow.

## Debugging Workflows

### Enable Debug Logging

Repository Settings → Secrets → Add:
- `ACTIONS_RUNNER_DEBUG`: `true`
- `ACTIONS_STEP_DEBUG`: `true`

### Print Context

```yaml
- name: Debug
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
```

### Common Issues

**Cache not restoring:**
- Verify cache key matches
- Check if cache exists (Actions tab → Cache management)
- Ensure paths are correct

**Deployment fails:**
- Check permissions are set correctly
- Verify output directory exists and contains files
- Check Pages settings (should be "GitHub Actions")

**Build works locally, fails in CI:**
- Check Node version matches
- Verify all dependencies in `package.json`
- Check for environment-specific code

## Performance Targets

Aim for:
- **Total workflow time**: <5 minutes
- **Cache hit rate**: >80% for dependencies
- **Build time**: <2 minutes (incremental caching helps)

**Measure**: Actions tab shows timing breakdown per step.

## Matrix Builds

For testing across versions:

```yaml
strategy:
  matrix:
    node: [18, 20]
    os: [ubuntu-latest, windows-latest]
  fail-fast: true  # Stop all on first failure

runs-on: ${{ matrix.os }}
steps:
  - uses: actions/setup-node@v4
    with:
      node-version: ${{ matrix.node }}
```

**Use when**: Need to verify compatibility across versions/platforms.
**Avoid when**: Only deploying to single environment (use single config).

## Secrets Management

### Using Secrets

```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

**Add secrets**: Repository Settings → Secrets and variables → Actions

**Never log secrets**: GitHub automatically masks secrets in logs, but avoid `echo $SECRET`.

## Workflow Triggers

### Common Patterns

```yaml
# On push to main
on:
  push:
    branches: [main]

# On PR to main
on:
  pull_request:
    branches: [main]

# Manual trigger
on:
  workflow_dispatch:

# Scheduled (cron)
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
```

## Job Dependencies

### Sequential Jobs

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [...]

  deploy:
    needs: build  # Wait for build
    runs-on: ubuntu-latest
    steps: [...]
```

### Parallel Jobs

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    runs-on: ubuntu-latest
    steps: [...]

  # Both run simultaneously
```

## Artifacts

### Upload Build Output

```yaml
- uses: actions/upload-artifact@v3
  with:
    name: build
    path: dist/
    retention-days: 7
```

### Download in Another Job

```yaml
- uses: actions/download-artifact@v3
  with:
    name: build
    path: dist/
```

**Use when**: Passing data between jobs.

## Best Practices

1. **Fail fast**: Put quick checks (lint, type check) before slow builds
2. **Cache aggressively**: Cache dependencies and build artifacts
3. **Minimal permissions**: Only grant necessary permissions
4. **Pin action versions**: Use `@v4` or commit SHAs
5. **Clear job names**: Use descriptive names for debugging
6. **Monitor performance**: Track workflow duration over time

## Quick Wins

**Already fast?** These optimizations have diminishing returns:
- Parallel jobs (if you only have 2-3 steps)
- Build caching (if builds are <30 seconds)
- Matrix builds (if you only deploy to one environment)

**Focus on**:
- Dependency caching (always beneficial)
- Fail fast (catch errors early)
- Clear error messages (faster debugging)

## Repository Settings

For GitHub Pages deployment:
1. Settings → Pages
2. Source: "GitHub Actions"
3. No branch configuration needed

For custom domain:
1. Add CNAME file to output directory
2. Configure DNS
3. Add custom domain in Pages settings
