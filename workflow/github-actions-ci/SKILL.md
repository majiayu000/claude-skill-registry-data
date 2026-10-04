---
name: github-actions-ci
description: Set up GitHub Actions CI pipeline with test, lint, type-check, and build jobs for a Node.js/TypeScript project. Includes output grouping, error annotations, and job summary patterns.
---

# GitHub Actions CI Pipeline

## Goal

Set up a comprehensive CI pipeline for a Node.js/TypeScript project with GitHub Actions output integration.

## CI Workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI
on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [22]
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm ts:check
      - run: pnpm lint
      - run: pnpm test
      - run: pnpm build

  format:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm format:check
```

Adapt branch names, package manager (pnpm/npm/yarn), and script names to match the project.

## Output Grouping

Group related output in CI logs for cleaner display:

```ts
function startGroup(label: string): void {
  if (process.env['GITHUB_ACTIONS']) {
    console.error(`::group::${label}`)
  }
}

function endGroup(): void {
  if (process.env['GITHUB_ACTIONS']) {
    console.error('::endgroup::')
  }
}

// Usage:
startGroup(`Processing: ${taskName}`)
await doWork()
endGroup()
```

## Error Annotations

Surface errors as inline annotations on the PR diff:

```ts
function annotateError(message: string, file?: string, line?: number): void {
  if (process.env['GITHUB_ACTIONS']) {
    const location = file ? ` file=${file}${line ? `,line=${line}` : ''}` : ''
    console.error(`::error${location}::${message}`)
  }
}
```

## Job Summary

Write a markdown summary after execution:

```ts
function writeSummary(markdown: string): void {
  const summaryFile = process.env['GITHUB_STEP_SUMMARY']
  if (summaryFile) {
    fs.appendFileSync(summaryFile, markdown + '\n')
  }
}
```

## Security

Pin third-party action versions by SHA for supply chain security:

```yaml
- uses: pnpm/action-setup@a7487c7e89a18df4991f7f222e4898a00d66ddda # v4.1.0
```

For first-party GitHub actions (`actions/*`), tags are acceptable.
