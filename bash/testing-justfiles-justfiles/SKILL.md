---
name: testing
description: Verify Justfiles code, configuration, generated artifacts, and executable examples. Use for these changes or explicitly requested checks.
---

# Test changes

Choose checks for the affected packages and behavior. Use package typecheck scripts,
Biome on changed files, and focused tests. Include affected dependents when shared
contracts change. For example, run a focused test from the repository root:

```sh
pnpm run test packages/fs/watch.test.ts
```

Broaden verification when shared impact, failures, or unresolved concerns justify it.
Before opening a code PR, complete the repository-wide checks required by
`.github/workflows/ci.yml` from the repository root:

```sh
pnpm run typecheck
pnpm run lint
pnpm run test
```

Fix failures caused by the requested change and rerun affected checks. Report unrelated
failures. Repeat passing checks only after relevant changes. Scope formatting and
autofixes to changed files and review their diffs; the root `format` and `lint:fix`
scripts rewrite files across the repository.

## Check the Frieren UI

For a visible change in `platform/frieren`, use a short Playwright CLI smoke check. Do not add a full end-to-end test unless the user asks for one.

Start the app from the repository root:

```sh
pnpm run dev
```

In a second shell, open the authenticated test session:

```sh
pnpm --filter frieren run verify:ui
```

This command creates or reuses a Clerk development user, signs in, and opens `http://localhost:5173` in the `frieren` session. Inspect only the changed flow. Use commands such as:

```sh
pnpm --filter frieren exec playwright-cli -s=frieren snapshot
pnpm --filter frieren exec playwright-cli -s=frieren console
pnpm --filter frieren exec playwright-cli -s=frieren requests
pnpm --filter frieren exec playwright-cli -s=frieren close
```

Use `fill` and `click` as needed.

## Check the sandbox reducer frame

After a change to `sandboxWorkerSource` in `packages/app/sandbox.ts` or the reducer frame in `platform/frieren/src/apps/sandbox.worker.ts`, run:

```sh
pnpm --filter frieren run verify:sandbox
```

This check confirms that the classic reducer Worker loads and answers the protocol in real browsers. If a required Playwright browser is missing, install it with:

```sh
pnpm --filter frieren exec playwright install chromium firefox webkit
```
