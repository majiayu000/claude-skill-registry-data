---
name: actions-style
description: GitHub Actions workflow authoring conventions for readable, least-privilege workflows — .github/workflows/*.yaml layout, explicit scoped triggers, boolean logic with truthy/falsey expressions (if ${{ inputs.flag }} over == 'true'), concurrency, matrix builds, job outputs, and authoring reusable (workflow_call) and composite actions. Use when writing, reviewing, or refactoring GitHub Actions workflows or composite actions (.github/workflows/*.yaml, action.yml), adding a job, matrix, or if-condition, or deciding how to structure triggers, inputs, and expressions.
license: MIT
---

# GitHub Actions workflow style

Apply these conventions to every workflow and composite action; match them when editing existing
ones. They keep workflows readable, reproducible, and least-privilege. For the rationale behind
each rule — especially GitHub's truthy/falsey coercion — see [reference.md](reference.md).

The security rules these conventions assume (SHA-pinning, no `pull_request_target`, minimal
`permissions`) live in the `actions-security` skill; the shared CI/release/merge automation lives
in the `actions-reusable-workflows` skill; validate with the `actions-validate` skill before
committing.

## 1. File layout and naming

- One workflow per file under `.github/workflows/`, named for what it does (`ci.yaml`,
  `release.yaml`). Use the `.yaml` extension, not `.yml`.
- Give every workflow a top-level `name:`, and name jobs and steps so the Checks UI and logs read
  well (`name: Continuous integration`, `- name: Build`).

## 2. Declare explicit, scoped triggers

Spell out `on:` events and narrow them — never lean on defaults. Filter `branches` and `paths` so
a workflow only runs when it must.

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: ["main", "releases/*"]
```

Use `pull_request` to test PR code. Reach for `pull_request_target` only for the rare base-context
task that runs **no** PR code (see `actions-security`).

## 3. Boolean logic uses truthy/falsey expressions

GitHub coerces an `if:` (or any `${{ }}`) result to a boolean. The **only** falsey values are
`false`, `0`, `-0`, `''` (empty string), and `null`. Everything else is truthy — including the
non-empty string `'false'`. So how you gate depends on the value's type:

- A `boolean`-typed input is a real boolean — gate on it directly:

  ```yaml
  on:
    workflow_call:
      inputs:
        e2e:
          type: boolean
          default: false
  # ...
        if: ${{ inputs.e2e }} # not: inputs.e2e == 'true'
  ```

- A **string** value (`vars.*`, `env.*`, a non-boolean `workflow_dispatch` input) holding
  `"false"` is a non-empty string and therefore **truthy** — you must compare explicitly:

  ```yaml
  if: ${{ vars.DEPLOY == 'true' }} # bare ${{ vars.DEPLOY }} would be truthy even when "false"
  ```

Declare boolean inputs `type: boolean` so the bare form works; reserve `== 'true'` for genuinely
string-typed values. Use `||` for defaults (`${{ inputs.runner || 'ubuntu-latest' }}`) and the
status functions `success()`, `failure()`, `always()`, `cancelled()` to gate on job state.

## 4. Concurrency

Cancel superseded runs on a branch or PR; never cancel a run that moves a ref.

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true # release/merge workflows use a fixed group with cancel-in-progress: false
```

## 5. Matrix builds

Use `strategy.matrix` for the same job across versions or platforms; keep `fail-fast: true` unless
you need every leg's result. Build a matrix at runtime from a prep job's output with `fromJSON`:

```yaml
strategy:
  fail-fast: false
  matrix:
    target: ${{ fromJSON(needs.prep.outputs.targets) }}
```

## 6. Orchestrate jobs with `needs` and outputs

Order jobs with `needs:` and pass data through job `outputs` (sourced from step outputs via
`$GITHUB_OUTPUT`), not by re-deriving state. Pin `runs-on` to a concrete image
(`ubuntu-24.04`) where reproducibility matters.

## 7. Setup and caching

Read toolchain versions from files, not the workflow, and let the `setup-*` actions cache:

```yaml
- uses: actions/setup-go@<sha> # v6.4.0 — pin by SHA (see actions-security)
  with:
    go-version-file: go.mod
    cache: true
```

## 8. Authoring reusable workflows and composite actions

- **Reusable workflow** (`on: workflow_call`): give every `inputs`/`secrets` entry a `type`,
  `description`, and `required`/`default`; expose results through `outputs`. Declare
  `permissions: {}` at the top and grant the minimum per job — the caller's grant is the ceiling.
  Pass secrets explicitly through `secrets:`; never `secrets: inherit`.
- **Composite action** (`action.yml`, `runs.using: composite`): declare `inputs` with descriptions
  and defaults, reference them as `${{ inputs.x }}`, and name each `run` step.
- Pin every third-party `uses:` to a full commit SHA with a version comment (see
  `actions-security`).

To wire the org's shared CI, CodeQL, release, and merge workflows instead of writing your own, use
the `actions-reusable-workflows` skill.
