---
name: ci-optimization-specialist
description:
  Optimizes GitHub Actions CI/CD workflows through test sharding, intelligent
  caching, and workflow parallelization. Use when CI execution time exceeds
  limits, costs are too high, or workflows need parallelization.
---

# CI Optimization Specialist

## Quick Start

This skill optimizes GitHub Actions workflows for:

1. **Test sharding**: Parallel test execution across multiple runners
2. **Caching**: pnpm store, Playwright browsers, Vite build cache
3. **Workflow optimization**: Job dependencies and concurrency

### When to Use

- CI execution time exceeds 10-15 minutes
- GitHub Actions costs too high
- Need faster developer feedback loops
- Tests not parallelized

## Test Sharding Setup

### Basic Pattern (Automatic Distribution)

Add matrix strategy to `.github/workflows/ci.yml`:

```yaml
e2e-tests:
  name: 🧪 E2E Tests [Shard ${{ matrix.shard }}/3]
  runs-on: ubuntu-latest
  timeout-minutes: 30
  strategy:
    fail-fast: false
    matrix:
      shard: [1, 2, 3]
  steps:
    - name: Run Playwright tests
      run: pnpm exec playwright test --shard=${{ matrix.shard }}/3
      env:
        CI: true
```

**Expected improvement**: 60-65% faster for 3 shards

### Advanced Pattern (Manual Distribution)

For unbalanced test suites, manually distribute by duration:

```yaml
matrix:
  include:
    - shard: 1
      pattern: 'ai-generation|project-management' # Heavy tests
    - shard: 2
      pattern: 'project-wizard|settings|publishing' # Medium tests
    - shard: 3
      pattern: 'world-building|versioning|mock-validation' # Light tests

# In step:
run: pnpm exec playwright test --grep "${{ matrix.pattern }}"
```

## Critical Caching Patterns

### pnpm Store Cache

ALWAYS cache pnpm store to avoid re-downloading packages:

```yaml
- name: Get pnpm store directory
  id: pnpm-cache
  shell: bash
  run: echo "STORE_PATH=$(pnpm store path)" >> $GITHUB_OUTPUT

- name: Setup pnpm cache
  uses: actions/cache@v4
  with:
    path: ${{ steps.pnpm-cache.outputs.STORE_PATH }}
    key: ${{ runner.os }}-pnpm-store-${{ hashFiles('**/pnpm-lock.yaml') }}
    restore-keys: |
      ${{ runner.os }}-pnpm-store-
```

### Playwright Browsers Cache

Cache 500MB+ browser binaries:

```yaml
- name: Cache Playwright browsers
  uses: actions/cache@v4
  id: playwright-cache
  with:
    path: ~/.cache/ms-playwright
    key: ${{ runner.os }}-playwright-${{ hashFiles('**/pnpm-lock.yaml') }}

- name: Install Playwright browsers
  if: steps.playwright-cache.outputs.cache-hit != 'true'
  run: pnpm exec playwright install --with-deps chromium

- name: Install Playwright system dependencies
  if: steps.playwright-cache.outputs.cache-hit == 'true'
  run: pnpm exec playwright install-deps chromium
```

### Vite Build Cache

For monorepos or frequent builds:

```yaml
- name: Cache Vite build
  uses: actions/cache@v4
  with:
    path: |
      dist/
      node_modules/.vite/
    key: ${{ runner.os }}-vite-${{ hashFiles('src/**', 'vite.config.ts') }}
```

## Workflow Optimization

### Job Dependencies

Use `needs` to control execution flow:

```yaml
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: pnpm run build
      - name: Run unit tests
        run: pnpm test

  e2e-tests:
    needs: build-and-test # Wait for build to complete
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3]
    steps:
      - name: Run E2E tests
        run: pnpm exec playwright test --shard=${{ matrix.shard }}/3
```

### Concurrency Control

Prevent multiple runs on same branch:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Artifact Management

### Per-Shard Artifacts

Upload test reports from each shard:

```yaml
- name: Upload Playwright report
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: playwright-report-shard-${{ matrix.shard }}-${{ github.sha }}
    path: playwright-report/
    retention-days: 7
    compression-level: 6
```

### Artifact Cleanup

Set short retention for test reports to reduce storage costs:

```yaml
retention-days: 7 # Default is 90 days
compression-level: 6 # Compress to reduce storage
```

## Performance Monitoring

### Expected Benchmarks

| Optimization             | Before  | After    | Improvement |
| ------------------------ | ------- | -------- | ----------- |
| Test sharding (3 shards) | 27 min  | 9-10 min | 60-65%      |
| pnpm cache hit           | 2-3 min | 10-15s   | 85-90%      |
| Playwright cache hit     | 1-2 min | 5-10s    | 90-95%      |
| Vite build cache         | 1-2 min | 5-10s    | 90-95%      |

### Regression Detection

Set timeout thresholds as guardrails:

```yaml
timeout-minutes: 30 # Fail if shard exceeds 30 minutes
```

Monitor shard execution times and rebalance if one shard consistently exceeds
others by >2 minutes.

## Optimization Workflow

### Phase 1: Baseline

1. Record current CI execution times
2. Identify slowest jobs
3. Measure cache hit rates (check Actions logs)

### Phase 2: Implement Caching

1. Add pnpm store cache (highest impact)
2. Add Playwright browser cache
3. Add build caches if applicable
4. Verify cache keys work correctly

### Phase 3: Implement Sharding

1. Calculate optimal shard count (target 3-5 min per shard)
2. Add matrix strategy to workflow
3. Test locally: `playwright test --shard=1/3`
4. Monitor shard balance in CI

### Phase 4: Monitor & Adjust

1. Track execution times over 5-10 runs
2. Identify unbalanced shards (>2 min variance)
3. Adjust shard distribution if needed
4. Set up alerts for regressions

## Common Issues

**Shard imbalance (one shard takes 2x longer)**

- Use manual distribution with `--grep` patterns
- Group heavy tests together, distribute across shards

**Cache misses despite correct key**

- Verify `hashFiles` glob patterns match actual files
- Check if lock file changes on every run (shouldn't happen)

**Playwright install fails with cache hit**

- Ensure system dependencies installed separately: `playwright install-deps`

**Tests fail in CI but pass locally**

- Check environment variables (CI=true may affect behavior)
- Verify mock setup works in parallel execution
- Increase timeouts for slow operations

## Success Criteria

- CI execution time < 15 minutes total
- Cache hit rate > 85% for dependencies
- Shard execution time variance < 2 minutes
- Zero timeout failures from slow tests

## References

For detailed examples and templates:

- GitHub Actions Caching:
  https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows
- Playwright Sharding: https://playwright.dev/docs/test-sharding
- pnpm in CI: https://pnpm.io/continuous-integration
