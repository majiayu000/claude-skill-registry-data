---
name: configure-ci
description: Use when setting up CI/CD for a frontend project — a least-privilege GitHub Actions pipeline (install, lint, typecheck, audit, test, build, e2e, bundle budget) that gates merges, plus preview deploys per pull request for the project's host (Netlify, Vercel, self-hosted).
---

# Configure CI

The pipeline that makes "CI is the real gate" true: every PR must pass lint, types, tests, build, and e2e before merge, and gets a preview to click through where the host supports it.

## 1. Audit current state
```bash
cat .claude/stack-profile.md 2>/dev/null || cat ~/.claude/stack-profile.md 2>/dev/null   # package_manager, frontend.framework, hosting, ci
ls .github/workflows/ .github/actions/ netlify.toml vercel.json vercel.ts Caddyfile .nvmrc 2>/dev/null
grep -E '"(lint|format|test|build|e2e|size)"' package.json 2>/dev/null   # the scripts CI will call
grep -rn "uses:" .github/workflows 2>/dev/null | grep -vE "@[0-9a-f]{40}" | grep -v "uses: \./"   # unpinned actions
```
Read from the profile: `package_manager` (this skill is written for pnpm — for another manager swap the install line and drop `pnpm/action-setup`: `npm ci`, `bun install --frozen-lockfile`, `yarn install --immutable`), `frontend.framework` (the `typecheck` script already picks `tsc -b` or `vue-tsc -b`), `hosting` (step 4), `ci` (must be `github-actions`; anything else: stop and say so). Test commands come from `package.json` scripts, so `tests.layout` does not change the workflow.

**Prerequisites:** `configure-linting` (Biome), `configure-test-stack` (Vitest + Playwright), a Node version in `.nvmrc` (`scaffold-frontend-project`). The bundle-budget step expects `size-limit` from `optimize-performance`.

## 2. Decide
- No workflow → full setup. Partial → add missing jobs. Present → confirm jobs cover lint, types, audit, test, build, e2e, and that every action is pinned.
- Containerised deploy to a server (self-hosted)? The deploy half belongs to [`set-up-delivery-pipeline`](../../infra/set-up-delivery-pipeline/SKILL.md); this skill owns the PR checks only.

## 3. The pipeline
Shared setup as a local composite action, so the three jobs do not repeat it. Action refs are full commit SHAs with the version in a comment (`ci-patterns.md`); Dependabot bumps both.
```yaml
# .github/actions/setup/action.yml
name: Setup
description: pnpm, Node from .nvmrc, frozen-lockfile install
runs:
  using: composite
  steps:
    - uses: pnpm/action-setup@ea17c68df8912ef543352723c149a84f56e3d413 # v6.1.0
    - uses: actions/setup-node@949feb2413d6458794dcd2491c4babbbce0c15c1 # v7.1.0
      with:
        node-version-file: .nvmrc
        cache: pnpm
    - run: pnpm install --frozen-lockfile
      shell: bash
```
```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}

jobs:
  quality:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: ./.github/actions/setup
      - run: pnpm exec biome ci .
      - run: pnpm typecheck
      - run: pnpm audit --prod --audit-level high

  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: ./.github/actions/setup
      - run: pnpm exec playwright install --with-deps chromium
      - run: pnpm test
      - run: pnpm exec playwright test
      - uses: actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9 # v7.0.2
        if: ${{ !cancelled() }}
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 14

  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: ./.github/actions/setup
      - run: pnpm build
      - run: pnpm exec size-limit
```
Match script/binary names to `package.json` (`pnpm test` = Vitest; drop `size-limit` unless `optimize-performance` wired it). `pnpm/action-setup` reads the pnpm version from `package.json`'s `packageManager` field (set by `scaffold-frontend-project`); without that field, pin it with `with: { version: <n> }` — which means editing the `setup/action.yml` snippet above, since it hardcodes no version. Typecheck needs the generated route tree: commit `src/routeTree.gen.ts` (`set-up-routing`), or `pnpm typecheck` fails in a clean checkout. Run `pnpm audit` in `quality` only for production deps: a dev-only advisory should not block a hotfix. `pnpm audit` queries the registry, so make the step non-blocking (`continue-on-error: true`) if the registry is unreliable or requires auth.

## 4. Preview deploys — branch on `hosting`
| Profile `hosting` / evidence | Branch |
|---|---|
| `netlify`, or `netlify.toml` | 4a |
| `vercel`, or `vercel.json` / `vercel.ts` | 4b |
| `hetzner`, `ionos`, Caddyfile | 4c |
| `supabase`, `none`, unknown | Ask one question: where is the SPA served from? |

In every branch the host builds the preview with its own Git integration. Do not duplicate the build inside the workflow.

### 4a. Netlify
Enable Deploy previews in the Netlify UI (Site → Build & deploy). Add the build config to `netlify.toml` (`set-up-security-headers` owns the `[[headers]]` block, so merge):
```toml
[build]
  command = "pnpm build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 4b. Vercel
Import the repo in Vercel once; every PR push then gets a preview URL, and `main` deploys to production. Vite is auto-detected. Add only the SPA fallback to `vercel.json` (`set-up-security-headers` owns `headers`; merge):
```json
{ "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }] }
```
Keep Deployment Protection on for previews of anything not public. Setup, env vars, domains: [`../../infra/deploy-to-vercel/SKILL.md`](../../infra/deploy-to-vercel/SKILL.md).

### 4c. Self-hosted
There is no built-in preview. CI gates the merge; the deploy (image build, push, rollout, TLS) is [`../../infra/deploy-to-hetzner/SKILL.md`](../../infra/deploy-to-hetzner/SKILL.md) and `set-up-delivery-pipeline`. A per-PR preview stack is optional and costs a server slot per open PR — add it when reviewers need to click, not by default.

## 5. Make it the gate
Branch protection lives in GitHub settings, not the repo: Settings → Branches → protect `main` → require `quality`, `test`, `build`. On Netlify/Vercel also require the host's deploy check if the preview must work before merge. Without protection, CI is advisory. Document it — a committed file cannot set it. Also enable Dependabot for `github-actions` (`set-up-security-headers` step 6).

## 6. Verify
Open a PR: the three jobs run and pass; Netlify/Vercel post a preview link. Push a lint error → `quality` fails → merge is blocked. `grep -rn "uses:" .github/workflows | grep -vE "@[0-9a-f]{40}"` prints nothing except `./` paths.

## References
- ./ci-patterns.md — CI-as-the-gate, `--frozen-lockfile`, SHA-pinned actions, least-privilege token, caching, the bundle budget, preview-per-PR per host, when to deviate.
- ../configure-linting/SKILL.md — the lint/format the pipeline runs.
- ../configure-test-stack/SKILL.md — Vitest + Playwright.
- ../set-up-security-headers/SKILL.md — shares the host config file (owns the headers; this skill owns build + fallback).
- ../../infra/set-up-delivery-pipeline/SKILL.md — the build-once, promote-by-digest pipeline for server deploys.
