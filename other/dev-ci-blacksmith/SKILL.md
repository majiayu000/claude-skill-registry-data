---
name: dev-ci-blacksmith
description: "Run GitHub Actions on Blacksmith runners: setup, migrating from GitHub-hosted / self-hosted (detect-runner) runners, runner label choice, caching, concurrency, cost/perf habits, gotchas, debugging. Use when the user says 'blacksmith', 'CI runner', 'faster CI', 'slow CI', 'migrate runners', 'switch to blacksmith', 'drop detect-runner', or when a workflow has (or should get) a `blacksmith-*` `runs-on` label, a job sits queued forever, or a `useblacksmith/*` action shows up."
---

# CI on Blacksmith

[Blacksmith](https://docs.blacksmith.sh/) = drop-in ephemeral runners for GitHub Actions (Firecracker microVM per job, same image as GitHub's, half the per-minute price, co-located cache). General workflow rules (timeouts, permissions, SHA pinning, security) live in `/gh-actions-wisdom` — this skill only covers what is Blacksmith-specific or a house convention.

Docs index for anything not covered here: `https://docs.blacksmith.sh/llms.txt` (every page has a `.md` twin — `curl` it rather than guessing).

## House conventions (surveyed from the zp repos)

- **Default label: `blacksmith-2vcpu-ubuntu-2204`**, hardcoded, on *every* job including 5-minute gate jobs. New repos that have no 22.04 history may use `-2404` (zudo-ez-host does); don't mix both in one repo.
- **`blacksmith-4vcpu-ubuntu-2204` only for Playwright e2e** — 2 Playwright workers + a dev/preview server starve on 2 cores (spec timeouts, ~2x wall clock). Nothing else has earned 4vcpu. Shard (`--shard=N/3` matrix) before going bigger.
- **macOS: `blacksmith-6vcpu-macos-15`** (Apple Silicon). Intel macOS has no Blacksmith equivalent — keep `macos-15-intel`.
- **No `useblacksmith/*` actions anywhere.** Vanilla `actions/checkout`, `pnpm/action-setup`, `actions/setup-node`, `actions/cache`, all SHA-pinned with a `# vX.Y.Z` comment. Blacksmith redirects the vanilla cache calls to its own backend transparently.
- **Every label in use is declared in `.github/actionlint.yaml`** — actionlint can't know Blacksmith labels, and the repos run an `actionlint.yml` workflow. Adding a new size/OS means adding it here too (plus `config-variables:` for any `vars.*` the `runs-on` expression reads).

  ```yaml
  self-hosted-runner:
    labels:
      - blacksmith-2vcpu-ubuntu-2204
      - blacksmith-4vcpu-ubuntu-2204 # e2e only
  ```

- **Setup order: pnpm before node.**

  ```yaml
  - uses: pnpm/action-setup@<sha> # v6
  - uses: actions/setup-node@<sha> # v5+
    timeout-minutes: 3
    with:
      node-version-file: ".github/.node-version" # or node-version: '22'
      cache: 'pnpm' # transparent Blacksmith cache; omit on small repos
  - run: pnpm install --frozen-lockfile
  ```

- **`timeout-minutes` on every job** — in use: 5 gates/notify, 10–20 lint/test/build, 30–60 e2e/deploy. Plus `timeout-minutes: 3` on the `setup-node` step itself so a hung cache restore fails fast.
- **Concurrency groups are named per workflow, not `${{ github.workflow }}`**: PR lanes `pr-checks-${{ github.head_ref }}` (or `...pull_request.number`) with `cancel-in-progress: true`; deploys a fixed name (`cf-workers-production-deploy`, `doc-pages-deploy`) with `cancel-in-progress: false`.
- **No repo-wide concurrency throttle.** Blacksmith has no shared-pool queueing, so a throttle trades PR latency for nothing. Slowness is per-runner CPU starvation → fix with label size or sharding.
- **Notify jobs**: IFTTT notify runs as a tail step or a tiny `needs: [...]`, `if: always()` job (see `/dev-ci-ifttt-notify`). The one `ubuntu-latest` job left in pgen is a nightly notify job — reasonable, since an alert about a failed run shouldn't depend on the runner that may have failed.

## Setup (new repo)

1. Install the **Blacksmith GitHub App** on the org/repo *first*. Without it a `blacksmith-*` label is just an unknown self-hosted label: the job sits **queued waiting for a runner** instead of failing with a useful error. This is the #1 "CI is stuck" cause.
2. Set `runs-on:` labels. No secrets, no workflow-level config.
3. Verify in the job log header / `app.blacksmith.sh` that the run landed on Blacksmith.

The app is per-owner. A workflow that also exists in a fork/mirror under another owner needs a guard or it queues there:

```yaml
# Blacksmith is installed on the org only — skip on the personal mirror
if: github.repository == 'my-org/my-repo'
runs-on: blacksmith-2vcpu-ubuntu-2204
```

### Opt-in with fallback (when the app install isn't confirmed yet)

Used in zudo-ez-host — a repo Actions **variable** gates the label; unset/typo falls back to GitHub-hosted so PRs can never queue on a missing runner:

```yaml
runs-on: ${{ vars.ZEH_RUNNER_MODE == 'blacksmith' && 'blacksmith-4vcpu-ubuntu-2404' || 'ubuntu-latest' }}
# matrix form: include a blacksmith_os key per row
runs-on: ${{ vars.ZEH_RUNNER_MODE == 'blacksmith' && matrix.blacksmith_os || matrix.os }}
```

Name the variable `<REPO>_RUNNER_MODE`, document the label mapping in `docs/ops/ci-runners.md`, roll back by deleting the variable. Once proven, hardcode the labels and drop the expression.

## Caching

- **`actions/cache`, `cache/save`, `cache/restore`, and `setup-*` `cache:` inputs are transparently served by Blacksmith's cache** (~4x throughput, 25 GB/repo/week, LRU after 7 days idle, branch-scoped like GitHub's). Zero config, no extra cost.
- **The `useblacksmith/cache` and `useblacksmith/setup-node|go|python|...` forks are archived.** If you see them, replace with upstream.
- **pnpm store caching is optional.** zzmod uses `cache: 'pnpm'`; zudo-doc-cloud deliberately doesn't (small dep tree → cache round-trip is a net loss). Never add a separate `actions/cache` step for the pnpm store, never cache `node_modules`.
- **Do cache large binary downloads**, e.g. Playwright browsers: `actions/cache` on `~/.cache/ms-playwright`, key `${{ runner.os }}-playwright-${{ hashFiles('pnpm-lock.yaml') }}` — ephemeral runners re-download Chromium every run otherwise.
- **setup-node v5+ gotcha**: it auto-enables pnpm caching when `package.json` has `packageManager: pnpm@…` and shells out to `pnpm store path`. A checkout-only job with no `pnpm/action-setup` dies with `Unable to locate executable file: pnpm` → set `package-manager-cache: false` on that job's setup-node.
- **Inter-job data**: house order of preference is (1) don't — let independent jobs each checkout/install/build so they run in parallel with no `needs:`; (2) one job; (3) `upload-artifact` → `download-artifact` with `retention-days: 1–2`. `/gh-actions-wisdom` rule 9 prefers `cache/save`→`restore` keyed on `run_id` to save org artifact storage; it works on Blacksmith but was the source of `Cache not found` failures from container jobs — use artifacts when a container job is downstream.
- **Sticky disks / Docker layer caching**: not used in any house repo yet. Reach for them only for multi-GB state or Docker builds — see [references/blacksmith-features.md](references/blacksmith-features.md).

## Migrating an existing repo

From GitHub-hosted: swap labels, done (plus the app install). From **self-hosted / `detect-runner`** (zmod still has this pattern) there are leftovers that break on ephemeral runners — run the audit, then follow [references/migration.md](references/migration.md):

```bash
bash $HOME/.claude/skills/dev-ci-blacksmith/scripts/audit.sh [repo-root]
```

Validation trap: a single-job `pr-checks` going green proves nothing about a multi-job deploy workflow (cross-job passing, container jobs, deploy-only jobs missing setup). The real gate is the first post-merge run — say so in the PR and `/watch-ci` it.

## Cost / perf habits

- Billing is per-minute × vCPU tier; 2vcpu ≈ half of `ubuntu-latest`'s price and usually faster. Bigger label only when the job is CPU-bound *and* parallelizable — measure before/after, record the issue number in a comment above `runs-on:`.
- 2vcpu has 8 GB RAM. Heavy Node builds set `NODE_OPTIONS: '--max-old-space-size=4096'`; tests needing 4+ GB heap belong in a local/`@heavy` lane, not the PR gate.
- Cheap gate job first (`check-should-run`: branch pattern, `[skip test]` marker, no install) so `noci/*`-style branches cost ~10 seconds.
- Path filters + `cancel-in-progress: true` on PR lanes matter more than runner size.
- Runners are sometimes silently upgraded a tier for free — don't benchmark from a single run.

## Debugging

| Symptom | Cause → fix |
| --- | --- |
| Job stuck "Queued / Waiting for a runner" | GitHub App not installed for this owner/repo, label typo, or fork without the app → install / fix label / add `github.repository` guard |
| `Unable to locate executable file: pnpm` in setup-node | v5 auto pnpm cache in a job without pnpm → `package-manager-cache: false` |
| `pnpm: command not found` in deploy job | Self-hosted leftover: job has no own setup steps → add checkout + pnpm + node |
| `Cache not found ...-<run_id>` downstream | cache used as inter-job pipe (esp. from a container job) → artifacts |
| `fatal: detected dubious ownership` | `container:` job → `git config --global --add safe.directory "$GITHUB_WORKSPACE"` step before checkout |
| Playwright spec timeouts only on CI | CPU starvation on 2vcpu → 4vcpu and/or shard |
| JS heap OOM | `NODE_OPTIONS` max-old-space, or move test to heavy lane |

More context per row: [references/troubleshooting.md](references/troubleshooting.md). Live inspection (SSH into a running job, log search, `blacksmith` CLI, per-job CPU/memory metrics): [references/blacksmith-features.md](references/blacksmith-features.md). Check `https://status.blacksmith.sh` before blaming the workflow.
