---
name: actions-reusable-workflows
description: Wire a repository to the bitwise-media-group/github-workflows reusable workflows — thin, SHA-pinned caller workflows for CI, security (CodeQL) scanning, release (release-please/GoReleaser/Zensical docs), the signature-preserving fast-forward /merge + merge-review-ack + merge-notice flows, and add-to-project — plus the bitwise-media-group/toolchain mise-task consumer contract and the FF Merge / Project Sync org app setup. Use when setting up CI, security scanning, releases, auto-merge, dependency updates, or project-board sync for a repo; adding a caller that uses the shared/reusable workflows; wiring the mise toolchain library; scaffolding a repo's .github/ with the org's standard automation; or asked which reusable workflow to call and what to grant it.
license: MIT
---

# Wire the bitwise reusable workflows

The org centralises CI, security scanning, release, and the fast-forward `/merge` automation in the
`bitwise-media-group/github-workflows` library, and its mise task contract in
`bitwise-media-group/toolchain`. A consuming repo keeps a **thin caller** in `.github/workflows/`
that owns its triggers and grants a permission ceiling, then delegates the work to a reusable
workflow with `uses:`. Copy a caller from this skill's [templates/](templates/) directory and pin it
by SHA.

Author bespoke workflows with the `actions-style` skill, harden them with `actions-security`, and
run `actions-validate` before committing.

## 1. The caller pattern

The caller declares `on:`, sets the `permissions:` ceiling the reusable workflow's jobs need (a
reusable workflow can never exceed the caller's grant), and calls one workflow per job:

```yaml
name: Continuous integration
on:
  push:
    branches: [main]
  pull_request:
    branches: ["main", "releases/*"]
permissions:
  contents: read
jobs:
  ci:
    uses: bitwise-media-group/github-workflows/.github/workflows/ci.yaml@1eaff010e2929a3583c50ffa325690216bc70462 # v6.2.0
```

A caller may add product-specific jobs (an `integration` job, say) alongside the reusable-workflow
job. None of these workflows use `pull_request_target` to run PR code.

## 2. Catalog

Every reusable workflow lives in the same repo and releases together — one tag, one commit, covers
`ci.yaml`, `security.yaml`, `release.yaml`, every merge workflow, and `add-to-project.yaml` at once.
Grant exactly the listed permission ceiling and nothing more.

### Always wire these

- **`ci.yaml`** ([template](templates/ci.yaml)) — runs the canonical mise tasks (`lint`, `build`,
  `test`, optional `e2e`) as parallel jobs, sets up only the toolchains the repo has (`go.mod` → Go,
  `package.json` → Node, `pyproject.toml` → Python via `uv`), verifies a committed `dist/` stays
  reproducible, and uploads coverage to Codecov. Caller grants `contents: read`. Inputs:
  `go-version-file`, `node-version-file`, `cache-dependency-path`, `e2e` (default `false`),
  `coverage` (default `true`; set `false` for repos that emit neither coverage nor test results).
  No secrets.
- **`security.yaml`** ([template](templates/security.yaml)) — CodeQL over `actions` + `go` +
  `javascript-typescript`, by detection. Caller grants `security-events: write`, `packages: read`,
  `actions: read`, `contents: read`. Inputs: `go-version-file`, `config-file` (pass
  `./.github/codeql/codeql-config.yaml`, [template](templates/codeql-config.yaml), to exclude a
  bundled `dist/`), `languages` (override auto-detection — e.g. a tooling-only `package.json` that
  shouldn't add an empty `javascript-typescript` leg). No secrets.
- **`release.yaml`** ([template](templates/release.yaml)) — release-please (two-pass) → GoReleaser
  (when a `.goreleaser.yaml` exists) and/or a Zensical docs build published to GitHub Pages (when a
  `zensical.toml` exists) — independent of each other, so one release can ship both. Caller grants
  `contents`/`issues`/`pull-requests: write`, plus `id-token`/`attestations`/`artifact-metadata`/
  `packages`/`pages: write` — grant all seven even without a `.goreleaser.yaml` or `zensical.toml`:
  GitHub unions a reusable workflow's job permissions and ignores `if:`, so a missing scope fails the
  run at startup regardless of which jobs actually run. Inputs: `vanity-tags` (default `false`; set
  it for Actions/reusable repos pinned `@v1`), `app-client-id` (optional — author the release PR as
  the "FF Merge" App instead of `GITHUB_TOKEN`, needed only if you auto-merge release PRs via
  `merge.yaml`, since a `GITHUB_TOKEN` push emits no `workflow_run` event). Optional secrets
  `homebrew-tap-token`, `app-private-key` (required only when `app-client-id` is set). Outputs:
  `release_created`, `tag_name`, `sha`, `version`, `major`, `minor`, `patch` — gate a follow-on job
  with `if: needs.release.outputs.release_created` (using the caller's own job id).
- **`merge.yaml`** ([template](templates/merge.yaml)) — signature-preserving fast-forward `/merge`
  plus set-and-forget auto-merge. Caller grants `permissions: {}` (the App token does the privileged
  work). Inputs: `app-client-id` (required), `merge-command`/`arm-command`/`label` (default
  `/merge`/`/auto-merge`/`auto-merge`), `require-approval`/`maintainer-only` (default `true`),
  `squash-authors` (default `bitwise-renovate[bot]` — authors whose PRs are squash-merged via the API
  instead of fast-forwarded, since their branches never rebase onto the base). Required secret
  `app-private-key`. Triggers `issue_comment`, `workflow_run` (list your CI workflow name(s) plus
  `"Merge Review Ack"`), and a `schedule` backstop sweep — deliberately no PR-attached event, so the
  flow adds no skipped-check clutter to a PR.
- **`merge-review-ack.yaml`** ([template](templates/merge-review-ack.yaml)) — required companion to
  `merge.yaml`: carries the **approval** signal (`pull_request_review`, which `merge.yaml`
  deliberately doesn't subscribe to) back in as a `workflow_run`, so fork and same-repo PRs auto-merge
  identically the moment they're approved. Caller grants `permissions: {}`, no inputs, no secrets —
  add `"Merge Review Ack"` to `merge.yaml`'s `workflow_run.workflows` list. Its single `ack` job is
  the only check this whole system adds to a PR.
- **`merge-notice.yaml`** ([template](templates/merge-notice.yaml)) — posts a one-time "this repo
  merges via `/merge`" comment on new PRs. Caller grants `pull-requests: write`. Input: `pr-number`
  (required). No secrets.
- **`add-to-project.yaml`** ([template](templates/add-to-project.yaml)) — adds newly opened issues to
  a shared org Projects v2 board via a "Project Sync" App token (`GITHUB_TOKEN` cannot write an
  org-level project). Caller grants `permissions: {}`. Inputs: `project-url` (required;
  `https://github.com/orgs/<org>/projects/<n>`), `app-client-id` (required),
  `labeled`/`label-operator` (optional label filter, default operator `OR`). Required secret
  `app-private-key`.

## 3. The consumer contract: mise tasks, not raw Makefile targets

The reusable workflows stay config-free by assuming a small contract, and as of the v3+ line
**the mise config is the language boundary, not the Makefile** — `ci.yaml` runs `mise run <task>`
directly, so a Makefile isn't required at all.

- **mise tasks** — `lint`, `build`, `test` (emitting `coverage/cobertura-coverage.xml`, optionally
  `coverage/junit.xml`), and `e2e`, defined in a root `mise.toml` or supplied by the shared task
  library (below). `ci.yaml` discovers the task list with `mise tasks ls --name-only` and skips
  whichever of those four the repo hasn't defined — **no no-op stubs needed** (drop any leftover
  `build: ; @:` from the old Makefile-only contract).
- **Toolchain detection** — a root `go.mod` sets up Go (`setup-go`, from `go-version-file`); a root
  `package.json` sets up Node (`setup-node`); a root `pyproject.toml` sets up Python via
  `astral-sh/setup-uv` (uv reads `requires-python` / `.python-version` itself — no `setup-python`). A
  tools-only `go.work` + `tools/go.mod` is dev tooling, not a product signal, so it does **not**
  trigger the Go path — only a root `go.mod` does.
- **Release** — `release-please-config.json` + `.release-please-manifest.json`; an optional
  `.goreleaser.yaml` (`release-type: go`, `draft: true`) selects the GoReleaser path; an optional
  `zensical.toml` (+ `pyproject.toml` + `uv.lock`, with repo **Settings → Pages → Source** set to
  **GitHub Actions**) selects the docs-publish path independently of GoReleaser. A committed `dist/`
  is verified fresh by `ci.yaml` on every PR, not at release time.

### Wire the toolchain library

A repo gets the mise tasks above from `bitwise-media-group/toolchain`
([latest `v2.4.1`](https://github.com/bitwise-media-group/toolchain/releases/tag/v2.4.1)), mounted as
a submodule at `.mise/`:

```sh
git submodule add https://github.com/bitwise-media-group/toolchain.git .mise
git -C .mise checkout v2.4.1
git add .mise && git commit -m "chore: add bitwise-media-group/toolchain submodule"
```

Then pick an archetype in a root `mise.toml` and reduce the `Makefile` to one include, kept only for
`make <target>` muscle memory and local interchangeability — CI never invokes it:

```toml
# mise.toml
[task_config]
includes = [".mise/tasks/go-cli.toml"] # or node-action / node-lib / docs-site / markdown-lib / terraform
```

```makefile
# Makefile — the whole thing
include .mise/mise.mk
```

Run `mise trust --all` once per clone (CI trusts the workspace automatically). The library's
`config.toml` also supplies the pinned developer tools, `[settings]`, and the universal
license/prose/container/shell lint tasks every archetype shares — see the library's own `README.md`
for the full task/knob reference, and the `terraform-validate` skill for the `terraform.toml`
archetype specifically. Per that same README, the submodule itself bumps via Dependabot's
`gitsubmodule` ecosystem; the tool pins inside `config.toml` bump via Renovate as normal (§7) —
**never** run `mise lock`/`mise upgrade` inside a consumer repo, that writes into the submodule's
working tree.

A caller may still mix a reusable-workflow job with normal jobs — e.g. a Go CLI keeps a
product-specific `integration` job in the same `ci.yaml` that calls the reusable `ci.yaml`.

## 4. Pinning

Every `uses:` line in this skill's templates pins the same full commit SHA, with the release tag as
a trailing comment:

```yaml
uses: bitwise-media-group/github-workflows/.github/workflows/ci.yaml@1eaff010e2929a3583c50ffa325690216bc70462 # v6.2.0
```

A floating tag (`@v6`, `@v6.2`) is simpler to read but mutable — see the `actions-security` skill for
why that matters on a workflow with elevated permissions. Prefer the SHA; Renovate's
`github-actions` manager bumps either form, and for a SHA pin it updates the trailing comment too.
The upstream repo's own illustrative snippets are an unreliable guide to "latest" — they show
inconsistent floating placeholders (`@v2` on most workflows, `@v4` on `add-to-project.yaml`, `@v6` on
`update-tools.yaml`) reflecting whatever major existed when each example was last touched, not the
current release. Resolve the real latest before pinning — and when the SHA above goes stale, the same
way: `git ls-remote --tags https://github.com/bitwise-media-group/github-workflows | sort -t/ -k3 -V`
for the newest tag, then `git rev-parse <tag>` against a local clone for its commit. Avoid `@main`
except for short-lived testing against a feature branch.

## 5. Fast-forward merge: org setup

`merge.yaml`, `merge-review-ack.yaml`, and `merge-notice.yaml` drive the
`bitwise-media-group/ff-merge` action via a short-lived GitHub App token (so commit signatures
survive). The one-time, org-wide setup — the "FF Merge" App, its ruleset bypass, the
`FF_MERGE_CLIENT_ID` variable, and the `FF_MERGE_PRIVATE_KEY` secret — is documented in
[`bitwise-media-group/ff-merge`](https://github.com/bitwise-media-group/ff-merge). The contract is
input `app-client-id` (from `vars.FF_MERGE_CLIENT_ID`) + secret `app-private-key` (from
`secrets.FF_MERGE_PRIVATE_KEY`); align older callers using `client-id`/`app-key` to these names. The
merge flows also require branch protection that requires PR review.

## 6. Add to Project: org setup

`add-to-project.yaml` needs its own GitHub App — "Project Sync" — separate from "FF Merge": the merge
flows act within a repo, while writing to an org-level Projects v2 board needs organization-scoped
permissions no repo-level App grant covers. Create it with organization **projects** read/write plus
repository **issues** + **pull requests** read, install it on every repository, and expose it as the
`ADD_TO_PROJECT_CLIENT_ID` variable + `ADD_TO_PROJECT_PRIVATE_KEY` secret. In this org the caller
itself is fanned out to every repo automatically by `org-config.sh workflows-sync` in
[`github-settings`](https://github.com/bitwise-media-group/github-settings), so copying the
[template](templates/add-to-project.yaml) by hand is only needed for a repo outside that sync.

## 7. Dependency updates: Renovate, not Dependabot

The org replaced Dependabot with a self-hosted Renovate bot
([`bitwise-media-group/renovate-config`](https://github.com/bitwise-media-group/renovate-config)).
It runs hourly with an App-installation token (so its commits are API-created and GitHub-signed —
Verified), autodiscovers every repo the "Renovate" App is installed on, and every discovered repo
inherits the org preset with **no onboarding file** — do not add a `.github/dependabot.yaml` or a
`dependabot-merge.yaml` caller. Renovate squash-merges its own green, approved PRs via the API
(the `merge.yaml` caller's `squash-authors` input defaults to `bitwise-renovate[bot]`), so getting a
repo covered is exactly: get the App installed (an org-level change, not a per-repo one).

A repo only needs its own `.github/renovate.json5` for a deliberate override on top of the preset
(an ignored dependency, a `postUpgradeTasks` rebuild rule for a committed bundle, …):

```json5
{
  extends: ["github>bitwise-media-group/renovate-config:default.json5"],
  // overrides here
}
```
