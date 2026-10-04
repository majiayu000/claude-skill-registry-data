---
name: github-actions
description: >-
  Generates and validates GitHub Actions workflows and custom actions (composite/Docker/JavaScript)
  with SHA-pinned supply chain security, SLSA attestation, OIDC federation, and
  harden-runner enforcement. Use when creating, editing, reviewing, or validating
  CI/CD pipelines, reusable workflows, monorepo CI patterns, container build/deploy
  orchestration, or advanced triggers (workflow_run, dispatch, ChatOps).
---

# [H1][GITHUB-ACTIONS]
>**Dictum:** *Workflow generation and validation enforce security, performance, and supply chain integrity.*

<br>

Generate and validate production-ready GitHub Actions workflows and custom actions.

**Tasks:**
1. Gather requirements — triggers, runners, dependencies, environments, security posture.
2. Read [best-practices.md](./references/best-practices.md) — security hardening, supply chain, performance, anti-patterns.
3. Read [version-discovery.md](./references/version-discovery.md) — SHA resolution protocol, action index, permissions.
4. Read [expressions-and-contexts.md](./references/expressions-and-contexts.md) — contexts, functions, injection prevention.
5. (advanced triggers) Read [advanced-triggers.md](./references/advanced-triggers.md) — workflow_run, dispatch, ChatOps, merge queue.
6. (custom actions) Read [custom-actions.md](./references/custom-actions.md) — composite, Docker, JavaScript action authoring.
7. Resolve action versions — `git ls-remote`, Context7 MCP, or WebSearch for latest SHA.
8. Generate — SHA-pinned actions, minimal permissions, concurrency, caching, timeouts, harden-runner.
9. Validate — Read validation references, run actionlint, apply 11 best practice checks.
10. Fix and re-validate until passing (max 3 iterations).

**Scope:**
- Workflow files (`.github/workflows/*.yml`).
- Custom actions — composite, Docker, JavaScript (`.github/actions/*/action.yml`).
- Reusable workflows (`workflow_call`).
- Supply chain — SLSA attestation, SBOM, Cosign signing.
- Monorepo CI — Nx affected detection, sparse checkout, pnpm workspace caching.

**References:**

| Domain            | File                                                                       |
| ----------------- | -------------------------------------------------------------------------- |
| Best Practices    | [best-practices.md](references/best-practices.md)                          |
| Version Discovery | [version-discovery.md](references/version-discovery.md)                    |
| Expressions       | [expressions-and-contexts.md](references/expressions-and-contexts.md)      |
| Advanced Triggers | [advanced-triggers.md](references/advanced-triggers.md)                    |
| Custom Actions    | [custom-actions.md](references/custom-actions.md)                          |
| Common Errors     | [common_errors.md](references/common_errors.md)                            |
| Supply Chain      | [supply_chain.md](references/supply_chain.md)                              |
| Modern Features   | [modern_features.md](references/modern_features.md)                        |
| Runners           | [runners.md](references/runners.md)                                        |
| Actionlint + Act  | [act_usage.md](references/act_usage.md)                                    |
| Template          | [basic-workflow.template.yml](templates/basic-workflow.template.yml)       |
| Template          | [reusable-workflow.template.yml](templates/reusable-workflow.template.yml) |
| Template          | [composite-action.template.yml](templates/composite-action.template.yml)   |
| Template          | [docker-action.template.yml](templates/docker-action.template.yml)         |
| Template          | [javascript-action.template.yml](templates/javascript-action.template.yml) |
| Example           | [nodejs-ci.yml](examples/nodejs-ci.yml)                                    |
| Example           | [docker-build-push.yml](examples/docker-build-push.yml)                    |
| Example           | [monorepo-ci.yml](examples/monorepo-ci.yml)                                |
| Example           | [dependency-review.yml](examples/dependency-review.yml)                    |
| Example           | [sbom-attestation.yml](examples/sbom-attestation.yml)                      |
| Example           | [setup-node-cached-action.yml](examples/setup-node-cached-action.yml)      |
| Example           | [chatops-dispatch.yml](examples/chatops-dispatch.yml)                      |
| Example           | [oidc-cloud-auth-action.yml](examples/oidc-cloud-auth-action.yml)          |
| Example           | [release-deploy.yml](examples/release-deploy.yml)                          |
| Example           | [docker-lint-scan-action.yml](examples/docker-lint-scan-action.yml)        |
| Example           | [pr-change-router-action.yml](examples/pr-change-router-action.yml)        |

---
## [1][STANDARDS]
>**Dictum:** *Mandatory standards enforce baseline quality across all generated workflows.*

<br>

Every generated workflow enforces defense-in-depth: supply chain integrity prevents compromised actions from executing, minimal permissions limit blast radius if a job is compromised, and harden-runner detects anomalous behavior at runtime. These layers are independent — failure of one leaves others intact.

[CRITICAL]:
- [ALWAYS] SHA-pin every `uses:` reference — mutable tags (`@v1`, `@main`) enable supply chain attacks. The tj-actions incident (CVE-2025-30066) compromised 23,000+ repos via tag retargeting.
- [ALWAYS] `step-security/harden-runner` as first step in every job — detected the tj-actions breach before any other tool.
- [ALWAYS] Top-level `permissions: {}` (deny-all default); grant minimal per-job permissions.
- [ALWAYS] `timeout-minutes:` on every job — prevents runaway billing on stuck workflows.

[IMPORTANT]:
- [ALWAYS] OIDC federation (`id-token: write`) for cloud auth — eliminates static credentials entirely.
- [ALWAYS] `actions/create-github-app-token` for cross-repo ops — scoped, 1-hour expiry, survives offboarding.
- [ALWAYS] `>> $GITHUB_OUTPUT` for step outputs; `>> $GITHUB_STEP_SUMMARY` for job summaries.
- [NEVER] Direct `${{ }}` interpolation of untrusted input in `run:` blocks — route through `env:` indirection.

[REFERENCE] [best-practices.md](./references/best-practices.md) — Security checklist, supply chain controls, anti-patterns.

---
## [2][TEMPLATES]
>**Dictum:** *Templates scaffold canonical workflow and action structure.*

<br>

Templates use `[PLACEHOLDER]` syntax for generation-time substitution. SHA resolution happens at generation time via the discovery protocol — templates contain placeholder SHAs, not static pins.

### [2.1][PLACEHOLDER_CONVENTION]

All templates use a unified `[UPPER_SNAKE_CASE]` placeholder convention:

| [CATEGORY]      | [PLACEHOLDERS]                                                              |
| --------------- | --------------------------------------------------------------------------- |
| **Identity**    | `[ACTION_NAME]`, `[WORKFLOW_NAME]`, `[DESCRIPTION]`, `[AUTHOR_NAME]`        |
| **Runtime**     | `[RUNTIME_VERSION]`, `[RUNTIME_ENV_KEY]`, `[ENABLE_CMD]`                    |
| **Package Mgr** | `[PACKAGE_MANAGER]`, `[INSTALL_CMD]`                                        |
| **Build/Test**  | `[BUILD_CMD]`, `[LINT_CMD]`, `[TEST_CMD]`, `[BUILD_PATH]`, `[RESULTS_PATH]` |
| **Deploy**      | `[ENV_NAME]`, `[ENV_URL]`, `[DEPLOY_CMD]`, `[VERIFY_CMD]`                   |
| **Secrets**     | `[SECRET_KEY]`, `[SECRET_NAME]`, `[REGISTRY_TOKEN]`                         |
| **Docker**      | `[BASE_IMAGE]`, `[BUILDER_IMAGE]`, `[ENTRYPOINT]`                           |

### [2.2][HARDEN_RUNNER_SCOPE]

`harden-runner` is included as the first step in every **workflow** job template (basic, reusable). **Action** templates (composite, Docker, JavaScript) do NOT include `harden-runner` — the **calling workflow** is responsible for adding it as the first step in the job that invokes the action. Actions are steps, not jobs.

### [2.3][TEMPLATE_INDEX]

| [INDEX] | [TEMPLATE]            | [PATH]                                     | [SCAFFOLDS]                                                        |
| :-----: | --------------------- | ------------------------------------------ | ------------------------------------------------------------------ |
|   [1]   | **Basic Workflow**    | `templates/basic-workflow.template.yml`    | CI pipeline: lint, test, build, deploy with parameterized runtime. |
|   [2]   | **Reusable Workflow** | `templates/reusable-workflow.template.yml` | `workflow_call` with typed inputs, secrets, version extraction.    |
|   [3]   | **Composite Action**  | `templates/composite-action.template.yml`  | Multi-step action with parameterized runtime and error handling.   |
|   [4]   | **Docker Action**     | `templates/docker-action.template.yml`     | Container action with distroless multi-stage Dockerfile pattern.   |
|   [5]   | **JavaScript Action** | `templates/javascript-action.template.yml` | Node 24 action with pre/post lifecycle, typed error handling.      |

[REFERENCE] [custom-actions.md](./references/custom-actions.md) — Action type selection, metadata, runtime deprecation.

---
## [3][EXAMPLES]
>**Dictum:** *Examples demonstrate production patterns for common scenarios.*

<br>

Each example demonstrates distinct patterns with minimal overlap. Load relevant examples before generation to match the target scenario.

| [INDEX] | [EXAMPLE]                                | [PATH]                                  | [DEMONSTRATES]                                                    |
| :-----: | ---------------------------------------- | --------------------------------------- | ----------------------------------------------------------------- |
|   [1]   | **Node.js CI**                           | `examples/nodejs-ci.yml`                | Matrix testing, caching, artifact upload, coverage, summaries.    |
|   [2]   | **Docker Build + Push**                  | `examples/docker-build-push.yml`        | Multi-platform builds, GHCR, BuildKit caching, SLSA provenance.   |
|   [3]   | **Monorepo CI**                          | `examples/monorepo-ci.yml`              | Nx affected detection, pnpm workspace, sparse checkout.           |
|   [4]   | **PR Security Gate**                     | `examples/dependency-review.yml`        | Multi-job security: dep review, CodeQL, Gitleaks, triage.         |
|   [5]   | **Container Supply Chain**               | `examples/sbom-attestation.yml`         | SBOM, Trivy severity gating, Cosign, gh attestation verify.       |
|   [6]   | **Composite Action (setup-node-cached)** | `examples/setup-node-cached-action.yml` | Smart caching, corepack detection, cache-dir resolution.          |
|   [7]   | **ChatOps Dispatch**                     | `examples/chatops-dispatch.yml`         | Slash commands, injection prevention, App token, env indirection. |
|   [8]   | **Multi-Cloud OIDC Auth**                | `examples/oidc-cloud-auth-action.yml`   | Composite action: AWS/GCP/Azure OIDC, output normalization.       |
|   [9]   | **Release + Deploy**                     | `examples/release-deploy.yml`           | Environment promotion, reusable workflow, concurrency groups.     |
|  [10]   | **Docker Lint + Scan**                   | `examples/docker-lint-scan-action.yml`  | Composite action: Trivy scan, hadolint, SARIF output.             |
|  [11]   | **PR Change Router**                     | `examples/pr-change-router-action.yml`  | Composite action: paths-filter, dynamic matrix, label sync.       |

---
## [4][ACTION_DISCOVERY]
>**Dictum:** *Runtime version resolution prevents stale SHA pins and supply chain drift.*

<br>

Static SHA catalogs decay — actions release frequently and stale pins miss security patches. Resolve versions at generation time. Never embed hardcoded SHAs in reference docs or templates.

**Resolution protocol:**
1. `git ls-remote --tags https://github.com/{owner}/{repo}` — verify tag exists.
2. `gh api repos/{owner}/{repo}/git/ref/tags/{tag} --jq '.object.sha'` — resolve tag to full SHA.
3. Format: `owner/repo@<40-char-SHA> # vX.Y.Z`.

**Fallback methods:**
- Context7 MCP: `resolve-library-id` then `get-library-docs` for action documentation.
- WebSearch: `"[owner/repo] [version] github action"` for release notes.

[IMPORTANT]:
- [ALWAYS] Verify the tag exists before pinning — deleted tags return empty results.
- [ALWAYS] Include version comment suffix (`# vX.Y.Z`) — Dependabot/Renovate parse these for automated updates.
- [NEVER] Embed static SHAs in reference files — they decay within weeks.

[REFERENCE] [version-discovery.md](./references/version-discovery.md) — Discovery protocol, SHA pinning format, common actions index, automated maintenance.

---
## [5][VALIDATION]
>**Dictum:** *Three-stage pipeline and 11 best practice checks gate workflow quality.*

<br>

**Validation pipeline:**

| [INDEX] | [STAGE]             | [TOOL]            | [VALIDATES]                                                          |
| :-----: | ------------------- | ----------------- | -------------------------------------------------------------------- |
|   [1]   | **Static Analysis** | actionlint 1.7.10 | YAML syntax, expressions, runner labels, action inputs, CRON, globs. |
|   [2]   | **Best Practices**  | 11 custom checks  | SHA pinning, permissions, injection, timeouts, harden-runner.        |
|   [3]   | **Local Execution** | act v0.2.84       | Dry-run validation against Docker images (requires Docker).          |

**Best practice checks (11):**

| [INDEX] | [CHECK]                  | [TAG]              | [DETECTS]                                                    |
| :-----: | ------------------------ | ------------------ | ------------------------------------------------------------ |
|   [1]   | **Deprecated commands**  | `[DEPRECATED-CMD]` | `::set-output`, `::save-state`, `::set-env`, `::add-path`.   |
|   [2]   | **Missing permissions**  | `[PERMISSIONS]`    | No top-level `permissions: {}` deny-all default.             |
|   [3]   | **Unpinned actions**     | `[UNPINNED]`       | Mutable tags (`@v1`, `@main`), abbreviated SHAs.             |
|   [4]   | **SHA without comment**  | `[SHA-NO-COMMENT]` | SHA-pinned but missing `# vX.Y.Z` version comment.           |
|   [5]   | **Missing timeout**      | `[TIMEOUT]`        | Jobs without `timeout-minutes:` (default is 6 hours).        |
|   [6]   | **Deprecated runners**   | `[RUNNER]`         | `ubuntu-20.04`, `macos-12`, `macos-13`, `windows-2019`.      |
|   [7]   | **Missing concurrency**  | `[CONCURRENCY]`    | No `concurrency:` group or missing `cancel-in-progress`.     |
|   [8]   | **PAT usage**            | `[APP-TOKEN]`      | PATs for cross-repo ops (use `create-github-app-token`).     |
|   [9]   | **No harden-runner**     | `[HARDEN]`         | Missing or not first step in job (CVE-2025-30066 detection). |
|  [10]   | **Expression injection** | `[INJECTION]`      | Direct `${{ github.event.* }}` in `run:` blocks.             |
|  [11]   | **Immutable actions**    | `[IMMUTABLE]`      | Action publishing without immutable OCI (informational).     |

**Error routing:** Match error patterns to reference files — [common_errors.md](references/common_errors.md) (syntax, expressions, deprecated), [runners.md](references/runners.md) (labels, deprecations), [supply_chain.md](references/supply_chain.md) (SHA, OIDC, SBOM, harden-runner), [modern_features.md](references/modern_features.md) (reusable workflows, concurrency, matrix, node runtime), [act_usage.md](references/act_usage.md) (actionlint rules, act limitations).

**Troubleshooting:**

| [INDEX] | [ISSUE]                     | [SOLUTION]                                     |
| :-----: | --------------------------- | ---------------------------------------------- |
|   [1]   | **Tools not found**         | Install actionlint + act (see act_usage.md).   |
|   [2]   | **Docker not running**      | Start Docker or validate with actionlint only. |
|   [3]   | **act fails, GitHub works** | See act_usage.md — Limitations.                |
|   [4]   | **ARM Mac arch mismatch**   | Add `--container-architecture linux/amd64`.    |
|   [5]   | **Custom runner labels**    | Declare in `.github/actionlint.yaml`.          |

[VERIFY] Completion:
- [ ] Supply chain: Every `uses:` reference SHA-pinned with `# vX.Y.Z` comment suffix.
- [ ] Security: Top-level `permissions: {}`, per-job minimal grants, `harden-runner` first step.
- [ ] Injection: No direct `${{ github.event.* }}` in `run:` blocks — all through `env:` indirection.
- [ ] Performance: Caching enabled, `concurrency` groups set, `timeout-minutes:` on every job.
- [ ] Structure: Descriptive `name:` on workflow/jobs/steps, lowercase-hyphen filenames.
- [ ] Outputs: `>> $GITHUB_OUTPUT` for data, `>> $GITHUB_STEP_SUMMARY` for summaries.
- [ ] Harden-runner: Workflow jobs include it; action templates note caller responsibility.
- [ ] All errors resolved with reference-backed fixes; warnings documented.

[REFERENCE] [best-practices.md](./references/best-practices.md) — Anti-patterns with specific remediations.
