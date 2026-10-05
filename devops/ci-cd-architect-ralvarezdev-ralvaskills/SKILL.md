---
name: ci-cd-architect
version: 1.0.0
description: CI/CD principles — pipeline taxonomy, trigger design, supply-chain hygiene (SHA-pinned actions), OIDC cloud auth, caching, matrix strategy, test gates, release automation, deployment strategies. Suggestion-mode (trade-offs over mandates). GitHub Actions recipes in RECIPES.md. Use when designing, reviewing, or scaffolding CI/CD workflows.
---

# CI/CD Architecture

Framework-agnostic CI/CD principles. The body presents trade-offs and common defaults; concrete pipelines live in [RECIPES.md](RECIPES.md) (GitHub Actions). See [STACK.md](STACK.md) for pinned action/tool versions used in the recipes.

This skill is **suggestion-mode**: most CI/CD decisions depend on team size, deployment target, risk tolerance, and existing infra. Each section names the choice, the trade-off, and a common default — not a mandate. Override locally with an ADR when a decision diverges from the suggestion.

Image-level rules (Dockerfile, multi-arch, scanning) live in [docker-architect](../docker-architect/SKILL.md); this skill covers only the workflow shape around them.

## 1. Pipeline taxonomy

Most projects need four pipeline shapes. Keeping them in separate workflow files is the common default — it makes "what triggers what" obvious and lets each evolve independently.

- **CI** — runs on every push and PR. Lint, type-check, test, build. Fast feedback (target under ~10 min).
- **Release** — runs on tag or main-branch merge. Produces versioned artifacts (binaries, images, packages). Must be idempotent.
- **Deploy** — promotes an existing artifact to an environment. Triggered manually or by release. Never rebuilds.
- **Scheduled** — periodic jobs: dependency scans, SBOM refresh, dead-link checks. Decoupled from the change cycle.

**Trade-off:** one mega-workflow is simpler at first but couples "what was built" to "where it ran" — rolling back gets harder. Splitting them lets you redeploy yesterday's image without re-running CI. Reach for the split once the project ships to more than one environment.

## 2. Trigger design

- **`push` to main** — CI + release. Path filters skip docs-only changes.
- **`pull_request`** — CI only. Required status checks live here.
- **`workflow_dispatch`** — deploys, ad-hoc reruns. Expose on every workflow you might ever need to retrigger manually.
- **`schedule`** — dependency / security scans. Use `cron` at non-peak times.
- **Concurrency** — every workflow should set a `concurrency:` group. For PRs, cancel-in-progress (don't waste CI on stale commits); for main/release, queue (don't race deploys).

GitHub Actions concurrency + path-filter examples in [RECIPES.md §2](RECIPES.md#2-concurrency-and-triggers).

## 3. Pipeline composition

DRY without overcomplicating. Three composition levels, in order of cost:

- **Single workflow file** — fine for small repos. Inline duplication is cheaper than abstraction here.
- **Composite actions** — share a single step block within a workflow. Reach for this when ≥3 jobs need the same setup steps.
- **Reusable workflows** (`workflow_call`) — share a multi-job pipeline across repos. Reach for this when ≥3 repos need the same shape.

**Trade-off:** premature abstraction makes the pipeline harder to read and debug. Factor out at the third copy, not the second. Reusable workflows in particular have non-trivial debugging overhead — stay inline until the duplication is clearly painful.

## 4. Supply-chain hygiene

CI runners can produce anything that gets deployed — they are high-value targets. Defaults that meaningfully reduce risk:

- **Pin third-party actions by SHA**, not tag. Tags are mutable; SHAs aren't. `actions/checkout@<sha>` with a `# v5.0.0` comment for humans. Renovate auto-bumps SHAs while preserving the comment.
- **First-party actions** (`actions/*`, `docker/*`) — pinning by major tag (`@v5`) is a common compromise; SHA-pin if your threat model warrants it.
- **`permissions:`** — set at workflow level to the most restrictive scope (`contents: read`). Elevate per-job as needed (`packages: write`, `id-token: write`). The default `GITHUB_TOKEN` grant is too broad in most repos.
- **Dependency Review action** on PRs catches known-vulnerable additions before merge.

SHA-pinning + Renovate config snippet in [RECIPES.md §4](RECIPES.md#4-action-pinning--renovate).

## 5. Secrets & cloud auth

- **Prefer OIDC** (workload identity federation) over long-lived credentials when the target supports it — AWS, GCP, Azure, HashiCorp Vault, npm + PyPI trusted publishing all do. The runner exchanges a short-lived JWT for a scoped token; no `AWS_ACCESS_KEY_ID` lives in repo secrets.
- **When long-lived secrets are unavoidable**, scope them to GitHub `environments:` with required reviewers — not to the repo.
- **Never echo a secret** in logs. Masking catches direct prints; derivative leaks (a token shaped into a URL, a hash printed for "debugging") happen anyway. Treat any code path that reads `${{ secrets.X }}` as opaque.
- **Rotate scheduled secrets** via a dedicated workflow; track rotation cadence in an ADR.

OIDC trust-policy snippets (AWS + GCP) in [RECIPES.md §5](RECIPES.md#5-oidc-cloud-auth).

## 6. Caching

Cache what's expensive to fetch and safe to reuse:

- **Language deps** — `setup-*` actions have built-in cache flags (`actions/setup-go` with `cache: true`, `actions/setup-python` with `cache: 'pip'` or `'uv'`). Prefer those over hand-rolled `actions/cache` blocks.
- **Build artifacts** — only cache compiled outputs when builds are deterministic. Non-deterministic build → stale cache → mystery failures that waste hours.
- **Docker layer cache** — `docker/build-push-action` with `cache-from: type=gha` + `cache-to: type=gha,mode=max` is the GitHub-native option. A registry cache (`type=registry,ref=<image>:cache`) survives across runners and is the better default for prod images.
- **Key the cache on the lockfile hash.** Collisions silently degrade builds.

Per-language caching examples in [RECIPES.md §6](RECIPES.md#6-language-caching).

## 7. Matrix strategy

Fan out only when the dimension genuinely matters:

- **OS matrix** — only if you ship cross-platform binaries or have OS-specific code paths.
- **Language version matrix** — only if you support multiple. A library targeting "Python 3.12+" tests 3.12, 3.13, 3.14; an app pinning 3.14 doesn't need a matrix.
- **`fail-fast: false`** when you want to see all failures (compatibility surveys); default `true` saves CI minutes when any failure is a blocker.

**Trade-off:** every matrix cell costs runner time + log volume. A 3×3×2 matrix is 18 jobs — each dimension should justify itself or come out.

## 8. Test gates + required status checks

- **Required checks live on the branch protection rule**, not in workflow YAML. The workflow runs the test; the rule decides whether main can merge.
- **Name jobs explicitly and stably** — required checks reference the job name. Renaming a job silently makes the rule unenforceable until someone notices and re-checks it.
- **Soft gates** (coverage delta, performance regression) post a PR comment; hard gates fail the job.
- **Flaky tests** — quarantine fast (mark `skip` with a tracking issue), don't normalize retry. Retry-as-default trains the team to ignore real flakiness.

## 9. Build & artifact publishing

This skill covers the **workflow shape**, not the Dockerfile — see [docker-architect](../docker-architect/SKILL.md) for image rules.

- **Multi-arch images** — `docker/setup-qemu-action` + `docker/setup-buildx-action` + `docker/build-push-action` with `platforms: linux/amd64,linux/arm64`.
- **Build once, push many** — build the image once, push with multiple tags (`:<short-sha>`, `:<semver>`, `:latest`) in one action. Parallel rebuilds for tags are an antipattern.
- **Sign with Cosign + OIDC** for prod-bound images (no key material). Verify on pull in the deployment platform.
- **SBOM** — generated alongside the image via `docker/build-push-action` attestations (`provenance: true`, `sbom: true`).

Full build + push workflow in [RECIPES.md §9](RECIPES.md#9-build--push-image).

## 10. Release automation

- **Conventional Commits → version + changelog** is the cheapest workable pattern. Tools: `release-please` (GitHub-native, manifest-driven), `semantic-release` (Node ecosystem), `git-cliff` (Rust-based, language-agnostic). Pick one and own it; switching costs are low.
- **Tag-driven release workflow** — `on: push: tags: 'v*'` triggers the build-and-publish workflow. Decoupling "version bump merged" from "artifact published" makes a failed release retryable.
- **Pre-release tags** (`v1.2.0-rc.1`) get pushed to a separate channel (npm `next`, container `:rc`, Go pseudo-versions).

`release-please` workflow + manifest in [RECIPES.md §10](RECIPES.md#10-release-please).

## 11. Deployment strategies

Pick by blast radius, not by fashion:

- **Direct deploy** — fine for low-risk services with a healthy rollback story. Don't over-engineer.
- **Blue-green** — two parallel environments, flip traffic atomically. Best when rollback must be instant.
- **Canary** — route a percentage of traffic to the new version, ramp over time. Needs traffic-shaping + per-version metrics to mean anything.
- **Manual approval gate** — `environments:` with required reviewers on prod. Cheap, high-signal, no infra needed; pairs with any of the above.

Whatever the strategy, the deploy workflow must be **idempotent and re-runnable**. A failed deploy mid-flight should be safe to retry without manual cleanup.

## 12. Out of scope

- **Deep Kubernetes / Argo / Flux** — future `kubernetes-architect` (planned).
- **Infrastructure provisioning** (Terraform, Pulumi) — future `iac-architect` (planned).
- **Per-language test conventions** — see the matching language architect (`go-architect`, `python-architect`).
- **Container security in depth** — see [docker-architect §4, §10](../docker-architect/SKILL.md).
- **Vulnerability findings catalog** — workflow runs the scanner; `security-reviewer` interprets the findings.
