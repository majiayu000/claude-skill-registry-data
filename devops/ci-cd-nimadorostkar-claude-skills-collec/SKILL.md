---
name: ci-cd
description: Use when building or fixing a delivery pipeline. Covers pipeline structure, caching, test parallelization, deployment strategies, secrets, and making the pipeline fast enough that people do not route around it.
metadata:
  category: devops
  version: 1.0.0
  tags: [ci-cd, github-actions, pipelines, deployment, automation]
---

# CI/CD

## Purpose

Build a pipeline that catches problems before production and is fast enough that engineers do not learn to ignore it. A twenty-minute CI run is a pipeline people bypass.

## When to Use

- Setting up CI/CD for a new project.
- A pipeline that is slow, flaky, or routinely skipped.
- Introducing a safer deployment strategy.
- Managing secrets and deployment credentials.

## Capabilities

- Pipeline structure: what runs on every commit, what runs on merge, what runs on release.
- Caching and parallelization to cut wall-clock time.
- Deployment strategies: blue/green, canary, rolling, feature flags.
- Secrets management and OIDC-based cloud authentication.
- Flaky-test detection and quarantine.

## Inputs

- The repository, its test suite, and current pipeline timings.
- The deployment target and its rollback capability.
- Compliance requirements: approvals, audit trail, signed artifacts.

## Outputs

- A pipeline with a fast feedback stage and a thorough merge stage.
- Deployments that are observable and reversible.
- No long-lived cloud credentials in CI.

## Workflow

1. **Split fast from thorough** — Lint, type-check, and unit tests on every push, in under five minutes. Integration, E2E, and security scans on the merge queue or on main.
2. **Cache the right things** — Dependencies, build artifacts, and Docker layers. A cache keyed on the lockfile hash is correct; one keyed on the branch is a source of stale-build mysteries.
3. **Parallelize the test suite** — Shard by timing, not alphabetically. The slowest shard determines the wall clock.
4. **Deploy progressively** — Canary to a small percentage, watch the error rate and latency, then proceed. Automate the abort.
5. **Authenticate with OIDC** — Short-lived tokens federated from the CI provider to the cloud. A long-lived access key in CI secrets is a breach waiting to be exfiltrated by a malicious dependency.
6. **Track flakes** — A test that fails 2% of the time will train the team to re-run the pipeline reflexively, at which point CI has stopped working.

## Best Practices

- A pipeline slower than about ten minutes changes behavior: people batch changes, stop pushing, and merge without waiting. Speed is a correctness property.
- Never allow a re-run to be the standard response to a red build. Quarantine the flaky test and fix it; re-running is how a real failure gets merged.
- Pin action and image versions by SHA, not by tag. A compromised or updated tag is a supply-chain compromise with commit access.
- Deployment must be a single button (or a single merge) with a single rollback. If deploying requires a runbook of six manual steps, one of them will be skipped at 2am.
- Build the artifact once and promote it through environments. Rebuilding per environment means the thing you tested is not the thing you shipped.
- The pipeline's own configuration is code: review it, and restrict who can change the deployment steps.

## Examples

**Pipeline with fast feedback, sharded tests, and OIDC deployment:**

```yaml
name: ci
on: [push, pull_request]

jobs:
  fast:                                   # < 5 min: runs on every push
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4, pinned by SHA
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci
      - run: npm run lint && npm run typecheck

  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]               # sharded by recorded timings
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci
      - run: npm test -- --shard=${{ matrix.shard }}/4

  deploy:
    needs: [fast, test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      id-token: write                     # OIDC: no stored AWS keys anywhere
      contents: read
    environment: production               # requires approval, records an audit trail
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/deploy
          aws-region: eu-west-1
      - run: ./scripts/deploy.sh --canary 10 --abort-on-error-rate 1.0
```

## Notes

- OIDC federation removes long-lived cloud credentials from CI entirely. This is the single highest-value security change available to most pipelines, and it takes an afternoon.
- `fail-fast: false` on a test matrix means you see all the failures in one run rather than the first one — significantly cheaper in wall-clock terms when several shards fail.
- A merge queue (GitHub merge queue, Zuul, Bors) tests the *merged* result rather than the branch, which prevents the semantic conflict where two independently green PRs break main together.
