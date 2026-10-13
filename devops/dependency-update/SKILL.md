---
name: dependency-update
description: Review, fix or land dependency updates (Renovate pull requests, the Bun catalog, the Expo SDK, images, actions, Helm charts, OpenTofu providers). Use when a Renovate PR fails CI, the user wants to upgrade a package or tool, or asks how dependencies are kept current.
---

# Dependency updates

Renovate runs in this repository's Actions (`.github/workflows/renovate.yml`, daily;
config in `renovate.json5`), as the GitHub App, so its pull requests run CI. It
schedules updates before 6am UTC on Mondays and waits until a release is 3 days old.
Everything is pinned: npm and Python packages with their lockfiles, images, actions by
digest, Helm charts, OpenTofu providers, and versions marked with a `# renovate:` comment.

## Reviewing a Renovate pull request

1. Read the release notes in its description; majors need the changelog's migration
   steps.
2. Check out the branch and run what CI runs: `bun install`, `bun run lint`,
   `bun run check-types`, `bun run test`; `bun run test:integration` for database,
   queue, auth or HTTP libraries.
3. Fix breakages at the cause in the same pull request (principle 1): no pinning back,
   no `@ts-ignore`.

## Special cases

- **Bun catalog.** Versions shared across workspaces live once in the root
  `package.json` `workspaces.catalog`; packages say `"catalog:"`. Renovate bumps the
  catalog entry and runs `bun install` to refresh `bun.lock`. By hand: edit the catalog
  entry, then `bun install`. Never give one workspace its own version of a catalog
  package.
- **Expo SDK.** `expo`, `expo-*`, `@expo/*`, `react-native*`, `react`, `react-dom` and
  their types are one group: the SDK decides the React Native and React versions. On
  that branch run `bunx expo install --fix` inside `apps/mobile` (the one tool that must
  run from its project folder), then `bun run --cwd apps/mobile doctor`
  (expo-doctor). React is in the catalog, so web moves with it: if `expo install`
  writes a version over a `"catalog:"` entry in `apps/mobile/package.json`, put that
  version in the root catalog and restore `"catalog:"`.
- **Playwright.** `@playwright/test`, `playwright` and the root `playwright-core` are
  one group, and Renovate reinstalls Playwright's skills in `.claude/skills` from the
  new version on that branch. By hand: run the commands `scripts/playwright.test.ts`
  prints when they don't match.
- **kind.** Its PR notes say it: update `SHA256` in `.github/workflows/kind.yml` to the
  release's `kind-linux-amd64.sha256sum` before merging.
- **Postgres majors** are disabled: a major needs a dump and restore or pg_upgrade,
  never a tag bump.
- **Playwright.** `@playwright/test`, `playwright`, `playwright-core` and the
  `mcr.microsoft.com/playwright` image the visual tests run in are one group, since the
  screenshot baselines depend on the exact browser build. The image's tag (in
  `packages/ui/package.json` and `scripts/docker-clean.ts`) must match the packages'
  version, which `scripts/pins.test.ts` checks. If the image isn't published yet when
  the packages are, wait for it rather than splitting the group. Run
  `bun run --cwd packages/ui test:visual` on the branch; a browser change can move
  pixels, and then `test:visual:update` and a look at the new screenshots.
- **Renovate's own config.** `bun run lint:renovate` validates `renovate.json5` in
  strict mode with the Renovate version `renovate.yml` pins; the lint job and the
  pre-commit hook run it. After raising `renovate-version`, run it and fix any setting
  the new version wants migrated.
- **Images** in `deploy/` and the charts: `bun run charts:check` renders and validates
  them. **OpenTofu providers**: `bun run infra:check`.
- **Python** (`apps/ai/uv.lock`): Renovate updates the lockfile; locally
  `bun run lint`, `bun run check-types` and `bun run test` cover apps/ai too.

## Overrides and patches

The root `package.json` forces a few transitive versions (`overrides`) and patches one
package (`patchedDependencies`), each to fix a known vulnerability that its parent pins
exactly. Every entry has a row here, which `scripts/overrides.test.ts` checks, and the
test fails once a row's "review by" date has passed, as `osv-scanner.toml`'s ignores
expire. When the "drop when" holds, remove the entry and its row, run `bun install`,
and check that the Security workflow's OSV scan still passes; otherwise move the date
on.

| Package | Pinned to | Why | Drop when | Review by |
| --- | --- | --- | --- | --- |
| `mysql2` | 3.23.1 | A credential leak and a decompression bomb in the version the Prisma CLI pins; the migrate image ships it. | Prisma requires 3.23.1 or later. | 2027-03-31 |
| `deepmerge-ts` | 8.0.0 | An advisory in the version `@prisma/config` pins; the migrate image ships it. | `@prisma/config` requires 8.0.0 or later. | 2027-03-31 |
| `js-yaml` | 4.3.2 | An advisory in the version `@hey-api/json-schema-ref-parser` pins (code generation). | `@hey-api/openapi-ts` depends on js-yaml 4.3.2 or later. | 2027-03-31 |
| `uuid` | 11.1.1 | An advisory in the version `xcode` asks for (Expo's native project tooling, its only user). | `xcode`, through `@expo/config-plugins`, allows uuid 11.1.1 or later. | 2027-03-31 |
| `next` | the catalog's version | A critical advisory in 16.3.3, which `@react-email/ui` (the email preview server) pins exactly; the override gives it the web app's Next, which has the fix. | `@react-email/ui` depends on a fixed Next. | 2027-01-05 |
| `decode-uri-component` | patched 0.2.2 | Its fix, 0.5.0, is ESM-only and query-string 7 (Expo Router) requires it, so the patch backports 0.5.0's linear-time decoder instead. `osv-scanner.toml` ignores the advisory until the entry expires. | Expo Router moves off query-string 7: drop the patch and the ignore together. | 2027-03-31 |

After merging, the deploy skill covers the rollout to staging.
