---
name: rule-ci-cd
description: MANDATORY when editing files matching [".github/**/*.yml"]. When working on GitHub Actions workflows in .github/
---

# CI/CD Rules

## Per-Application CD Workflow Structure
ALWAYS structure CD workflows as a three-job pipeline: `checks -> deploy -> send-slack-notification`. The deploy job MUST use `max-parallel: 1` and `fail-fast: false` to serialize environment deployments.

Example from codebase:
```yaml
# From .github/workflows/cd-nofos.yml
jobs:
  checks:
    uses: ./.github/workflows/ci-nofos.yml
  deploy:
    needs: [checks]
    uses: ./.github/workflows/deploy-nofos.yml
  send-slack-notification:
    if: failure()
```

## Reusable Workflow Composition
ALWAYS extract shared CI/CD logic into reusable workflows via `workflow_call` when the same job-level logic is needed by more than one workflow. NEVER duplicate multi-step job definitions across workflow files.

Example from codebase:
```yaml
# From .github/workflows/ci-frontend-e2e.yml
create-report:
  if: ${{ !cancelled() }}
  needs: e2e-tests-local
  uses: ./.github/workflows/e2e-create-report.yml
  secrets: inherit
  with:
    run_id: ${{ github.run_id }}
```

## Composite Actions for Step-Level Reuse
ALWAYS use composite actions under `.github/actions/` for step-level reuse. NEVER duplicate the same sequence of steps in multiple jobs.

Example from codebase:
```yaml
# From .github/actions/e2e/action.yml
name: Run Playwright
inputs:
  version:
    required: true
  target:
    default: "local"
  total_shards:
    default: "1"
runs:
  using: "composite"
  steps:
    - name: Validate environment
      shell: bash
      run: |
        if [[ $PLAYWRIGHT_TARGET_ENV != "local" && $PLAYWRIGHT_TARGET_ENV != "staging" ]]; then exit 1; fi
```

## Workflow Naming Convention
ALWAYS name CI workflows `ci-{app}.yml` and CD workflows `cd-{app}.yml`. ALWAYS use descriptive prefixes: `deploy-{app}.yml`, `vulnerability-scans-{app}.yml`, `e2e-{target}.yml`, `lint-{description}.yml`.

## Path-Filtered Triggers with Shared Modules
ALWAYS include `paths:` filters on `push` triggers. ALWAYS include `infra/modules/**` in the paths filter for all service CD workflows.

Example from codebase:
```yaml
# From .github/workflows/cd-api.yml
on:
  push:
    branches: ["main"]
    paths:
      - "api/**"
      - "infra/api/**"
      - "infra/modules/**"
```

## Environment Promotion with Prod-First Ordering
ALWAYS follow: push-to-main deploys to `["dev", "staging"]`, release deploys to `["prod", "training"]`. ALWAYS list `"prod"` before `"training"` in the release matrix. NEVER order training before prod.

## Concurrency Controls
ALWAYS set a `concurrency` group on deploy workflows keyed to the environment name. ALWAYS use `cancel-in-progress: true` on CI workflows.

Example from codebase:
```yaml
# From .github/workflows/deploy-nofos.yml
concurrency: cd-nofos-${{ inputs.environment || 'dev' }}
```

## Guard Against Null Inputs on Push Triggers
ALWAYS handle `inputs.environment` being `null` on `push` events. ALWAYS include a null check in expressions referencing `inputs.environment`.

Example from codebase:
```yaml
# From cd-api.yml
fail_on_vulns: ${{ ! contains(fromJSON(inputs.environment != null && format('["{0}"]', inputs.environment) || github.ref_name == 'main' && '["staging"]' || '["dev"]'), 'staging') }}
```

## Cross-Repo Deployment
NEVER use the generic `deploy.yml` for apps sourced from external repositories. ALWAYS use a dedicated `deploy-{app}.yml` that handles external checkout and non-standard build paths.

## Docker Image Caching
ALWAYS use `actions/cache/save` and `actions/cache/restore` to pass Docker images between CI and CD jobs. ALWAYS include `github.run_id` in the cache key.

Example from codebase:
```yaml
# From .github/workflows/ci-nofos.yml
- uses: actions/cache/save@v4
  with:
    path: /tmp/docker-image.tar
    key: nofos-image-${{ github.sha }}-${{ github.run_id }}
```

## App-Specific Git Hashes for Container Reuse
ALWAYS use the most recent commit hash within each app's folder (not repo-level HEAD) for container image tagging. MUST use `fetch-depth: 1000` on checkout.

## Dual Vulnerability Scanning
ALWAYS run Trivy + Anchore/Grype + Dockle on all deployed images. ALWAYS manage false positives through skip files and ignore lists, NEVER by disabling scans.

## Explicit Minimal Permissions
ALWAYS declare explicit `permissions:` blocks requesting only minimum access. NEVER assume `read` is sufficient when the workflow updates resources.

## E2E Test Sharding
ALWAYS shard Playwright tests with 4 shards. ALWAYS merge blob reports via a separate `create-report` job. ALWAYS use `if: ${{ !cancelled() }}` on the report job.

## E2E Spoofed Login
ALWAYS use spoofed session cookies for authenticated e2e tests. NEVER script actual login.gov authentication in CI.

## Governance Linters
ALWAYS implement governance automation as scripts under `.github/linters/scripts/` with `lint-*.yml` workflows. ALWAYS support `--dry-run` mode.

## Feature Flags in Terraform
ALWAYS gate new API capabilities behind `ENABLE_{FEATURE}_ENDPOINTS = 1` in Terraform configs. ALWAYS enable in dev/staging first, then prod.

## No Bundled Unrelated Changes
NEVER bundle unrelated changes with CD workflow modifications. Each PR touching CD workflows MUST focus on a single concern.

---

## Context Enrichment

When generating significant CI/CD changes (new workflow, new deployment pipeline, sharding changes), enrich your context:
- Call `get_architecture_section("ci-cd")` from the `simpler-grants-context` MCP server to understand CI/CD architectural principles
- Call `get_rule_detail("infra")` for infrastructure patterns that CI/CD interacts with
- Consult **Compound Knowledge** for indexed documentation on pipeline conventions, deployment patterns, and environment promotion

## Related Rules

When working on GitHub Actions workflows, also consult these related rules:
- **`infra.mdc`** — three-layer Terraform structure, feature flags, environment configuration
- **`cross-domain.mdc`** — feature flag conventions, SSM parameter requirements

## Specialist Validation

When generating or significantly modifying CI/CD code:

**For simple changes (updating a path filter, fixing a step):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new job, new composite action):**
Invoke `deployment-verification-agent` to validate pipeline safety.

**For complex changes (new workflow, new deployment pipeline, new sharding strategy):**
Invoke the following specialists (run in parallel where possible):
- `deployment-verification-agent` — pipeline safety, environment promotion, concurrency controls
- `performance-oracle` — CI performance (caching efficiency, shard balance, unnecessary steps)
- `security-sentinel` — permissions blocks, secret handling, no token exposure in logs
