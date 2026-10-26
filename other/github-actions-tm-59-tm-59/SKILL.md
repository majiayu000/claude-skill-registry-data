---
name: github-actions
description: Use when adding or reviewing GitHub Actions workflows under a limited minutes budget — deciding what belongs in CI at all, lightweight pull-request gates with paths filters and concurrency cancellation, keeping E2E, media generation and deployments local, pinning actions, permissions, and measuring actual minutes used. Also use when a free-tier budget runs out, CI duplicates on push and pull_request, or a workflow needs secrets it should not have.
---

# GitHub Actions on a budget

Default: CI runs **only lightweight gates on pull requests**; everything heavy is a local script. The budget is protected by classifying work before writing a workflow, not by reacting after minutes run out.

## Classify first

| Class | Examples | Where it runs |
|---|---|---|
| PR gate | lint, type-check, unit tests, size budget, content checks | Actions, `pull_request` only |
| Local only | E2E/browser tests with recording, video or image generation, full rebuild verification, docs/context sync, opening PRs, container scans | npm script / Make target / shell script |
| Scheduled | only checks that cannot be done any other way (e.g. weekly expiry detection) | Actions `schedule`, rare |
| Deploy | production deployment | a local deploy script from the main branch |

New workflows or steps must fit one of these classes.

## Gate template

```yaml
name: test
on:
  pull_request:
    paths: ["src/**", "tests/**", "package*.json", ".github/workflows/test.yml"]
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci && npm test
```

- `pull_request` only (no `push`): one run per change instead of two.
- `paths` skips documentation-only changes.
- `concurrency` cancels superseded runs on new pushes to the same PR.
- `timeout-minutes` caps runaway jobs.
- Least-privilege `permissions`; secrets are not available to forks' PRs, so gates should not need them.

## Measure

- Read actual usage from the billing API for Actions only (other products, e.g. AI features, may appear in the same report — filter by product).
- Compare actual minutes per repository with the planned estimate; a big gap points to a misclassified workflow.
- Remember multipliers: macOS and Windows runners cost several times more per minute than Linux.

## Verification loop

1. `actionlint` on workflow files.
2. Open a PR touching a gated path → the job runs once; push a docs-only change → it does not run.
3. Push twice quickly → the first run is cancelled.

## Pitfalls

- **Dependency bot PRs** trigger gates too; with many repositories, group updates and cap open PRs to keep minutes predictable.
- **`pull_request_target`** runs with write permissions on untrusted code; avoid it unless you understand the risk.
- **Caches** count against storage and can be evicted; do not depend on them for correctness.
- **Matrix builds** multiply minutes; test the full matrix locally or on a schedule, not on every PR.
- **Third-party actions:** pin to a release (or a commit SHA for sensitive workflows) and review what they do with tokens.
