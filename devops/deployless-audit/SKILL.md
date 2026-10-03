---
name: deployless-audit
description: Deployless delivery-model audit. Use first when adapting any repository toward single-mainline development, automatic deployment from main, runtime release controls, production-trace-driven iteration, AI PR governance, or multi-agent delivery workflows.
metadata:
  priority: 6
  docs:
    - "https://trunkbaseddevelopment.com/"
    - "https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development"
  pathPatterns:
    - ".github/workflows/**"
    - ".gitlab-ci.yml"
    - "Jenkinsfile"
    - "CONTRIBUTING.md"
    - "CODEOWNERS"
    - "docs/**"
    - "README.md"
  promptSignals:
    phrases:
      - "deployless"
      - "single mainline"
      - "trunk based"
      - "continuous deployment"
      - "runtime release controls"
      - "ai pr governance"
    allOf:
      - [delivery, audit]
      - [mainline, deploy]
    anyOf:
      - "feature flags"
      - "merge queue"
      - "production traces"
      - "agent workflow"
    noneOf: []
    minScore: 5
---

# Delivery Model Audit for Any-Language Repositories

## Purpose

Create a precise implementation plan for a deployless delivery model without assuming a specific language, package manager, test framework, CI provider, deployment platform, or hosting model.

The target model is:

- `main` is the single long-lived integration and release branch.
- Every accepted change is deployable.
- Merging to `main` eventually deploys to production through an automated, repeatable path.
- User-facing release is controlled at runtime by flags, kill switches, routing rules, or capability gates.
- Production feedback is captured through logs, traces, metrics, and replayable fixtures.
- State changes are backward-compatible and reversible where practical.

## Required stance

Call the result **deployless** only when the repository has a disciplined mainline delivery system with strong safety gates and runtime release controls. When blockers remain, document the target as a deployless migration plan rather than claiming the model is already in place.

## Inputs to inspect

Inspect the repository before changing behavior. Identify as many of these as apply.

### Language and build detection

Look for:

- JavaScript or TypeScript: `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `bun.lockb`, `tsconfig.json`
- Python: `pyproject.toml`, `requirements.txt`, `poetry.lock`, `Pipfile`, `setup.py`, `tox.ini`, `noxfile.py`
- Go: `go.mod`, `go.work`, `Makefile`
- Rust: `Cargo.toml`, `Cargo.lock`
- Java or Kotlin: `pom.xml`, `build.gradle`, `build.gradle.kts`, `settings.gradle`, `gradlew`
- .NET: `*.csproj`, `*.fsproj`, `*.sln`, `global.json`
- Ruby: `Gemfile`, `Rakefile`, `.ruby-version`
- PHP: `composer.json`, `composer.lock`
- Elixir or Erlang: `mix.exs`, `rebar.config`
- Swift: `Package.swift`, `*.xcodeproj`, `*.xcworkspace`
- C or C++: `CMakeLists.txt`, `Makefile`, `meson.build`, `configure.ac`, `vcpkg.json`, `conanfile.*`
- Infrastructure: `main.tf`, `terragrunt.hcl`, `pulumi.yaml`, `cdk.json`, `helm`, `kustomization.yaml`
- Containers: `Dockerfile`, `docker-compose.yml`, `.dockerignore`

### Delivery and operations detection

Look for:

- CI files: `.github/workflows`, `.gitlab-ci.yml`, `bitbucket-pipelines.yml`, `azure-pipelines.yml`, `Jenkinsfile`, `.circleci/config.yml`, `buildkite.yml`
- Deployment files: `vercel.json`, `netlify.toml`, `fly.toml`, `railway.json`, `render.yaml`, `app.yaml`, `serverless.yml`, `sst.config.*`, Kubernetes manifests, Helm charts, Terraform, Pulumi, CloudFormation, CDK
- Branch/release rules: `CONTRIBUTING.md`, `CODEOWNERS`, release scripts, semantic-release configs, changelog tools, protected-branch documentation
- Tests: unit, integration, end-to-end, contract, load, smoke, migration, mobile/device tests
- Observability: OpenTelemetry, Sentry, Datadog, Honeycomb, Grafana, Prometheus, CloudWatch, New Relic, logging libraries, audit logs
- Data and migrations: SQL migrations, ORM migrations, NoSQL schema conventions, event schemas, message queues, cache keys, search indexes
- Existing feature flags: LaunchDarkly, Unleash, Statsig, ConfigCat, Flagsmith, Split, Flipt, homemade flags, environment-config toggles, routing tables, capability checks
- AI and automation workflow: bot authors, agent branches, open AI PR volume, merge queue, PR labels, PR templates, issue links, CODEOWNERS, stale PR automation, CI concurrency, and multi-agent handoff docs
- Agent execution workflow: planning docs, domain glossary, ADRs, issue readiness labels, implementation handoff notes, test-first conventions, review rules, and final-diff review expectations

## Concept mapping

Use this mapping in generated docs.

| Deployless pattern | Any-language practice |
| --- | --- |
| Code is available immediately after a small atomic change | A successful merge to `main` triggers an automated deploy or publish path |
| Feature flags replace deploy-time release decisions | Runtime flags, kill switches, routing rules, capability gates, or remote config control exposure |
| No long-lived branches | `main` is the only long-lived branch; short-lived branches are allowed only as review vehicles |
| Code under use is protected from unsafe edits | Required tests, review, ownership, branch protection, static checks, compatibility checks, and staged rollout |
| Function/type versioning | Backward-compatible APIs, versioned interfaces, adapters, branch-by-abstraction, compatibility tests |
| Database versioning | Expand-contract migrations, dual-read/write, non-destructive deploy steps, migration verification |
| Production traces drive development | Correlated request logs, traces, replay fixtures, sampled production scenarios, regression tests |
| Rollback is mostly behavioral | Turn flags off, kill routes, disable capabilities, or roll back deployment only for infrastructure/runtime failures |
| AI can generate more PRs than humans can review | AI PR intake labels, WIP limits, ownership, merge queues, CODEOWNERS, and low-context PR rejection rules |
| Agents need bounded autonomy | Scope challenge, planning artifacts, vertical slices, test-first implementation, independent design/review passes, and primary-agent merge judgment |

## Audit procedure

1. Classify the repo:
   - application service
   - frontend/static site
   - mobile app
   - desktop app
   - library/package
   - CLI
   - worker/queue processor
   - infrastructure repo
   - monorepo containing several of the above
2. Detect language, build system, test commands, artifact type, and runtime.
3. Detect the current branch model:
   - long-lived `develop`, `staging`, `release/*`, or environment branches
   - tag-based releases
   - manual deployment branches
   - direct commits to `main`
   - PR-based mainline development
4. Detect deployment path:
   - manual
   - branch-based
   - tag-based
   - scheduled
   - CI/CD from `main`
   - external platform auto-deploy
5. Detect release controls:
   - none
   - build-time config only
   - environment variables
   - runtime feature flags
   - routing rules
   - entitlement/capability gates
6. Detect safety gates:
   - tests
   - static analysis
   - type checks
   - linting/formatting
   - code review
   - smoke tests
   - canary or phased rollout
   - production monitoring
7. Detect mutable state and migration risk.
8. Detect AI PR and multi-agent pressure:
   - many bot-authored PRs
   - duplicate or low-context PRs
   - repeated merge conflicts
   - unowned high-risk diffs
   - CI queue starvation
   - missing agent handoff rules
9. Detect agent execution maturity:
   - unclear issue or PRD intake
   - missing acceptance criteria
   - no documented test seams
   - no review of important interface designs
   - no final standards/spec review
   - no owner converting review findings into decisions
10. Document the minimum changes required before `main` can safely deploy to production.

## Output

Create or update `docs/deployless-mainline-plan.md` with this structure:

```markdown
# Deployless Mainline Plan

## Repository classification

## Current delivery model

## Target delivery model

## Language/runtime/toolchain detected

## Current branch and release model

## Required mainline gates

## Runtime release-control strategy

## Deployment automation strategy

## Observability and trace/replay strategy

## Data migration strategy

## Rollback and kill-switch strategy

## AI PR and multi-agent governance

## Agent execution and review loop

## Implementation sequence

## Risks and blockers

## Files to change
```

Also create an ADR when the repo already has an ADR convention. Use the existing naming convention. If no ADR convention exists, create `docs/adr/0001-deployless-mainline-delivery.md`.

## Language adaptation rules

- Prefer the repo's existing task runner over adding a new one.
- If the repo uses `make`, `just`, `task`, `rake`, Gradle, Maven, Cargo, Go tooling, npm scripts, Poetry, Tox, Nox, or .NET CLI, integrate with that tool rather than inventing parallel scripts.
- If no standard build/test commands exist, document the gap and add a minimal task wrapper only when the repo already has enough structure to support one.
- Do not add a feature flag provider dependency before confirming the repo's language and operational model. Start with an interface/facade and a local provider when necessary.
- For monorepos, create per-service findings and one shared governance model.
- For libraries, map “deployment” to package publication or artifact release. Still use `main` as the source of releasable truth.
- For mobile apps, map “deployment” to build/signing/submission pipelines. Runtime release controls may be remote config, capability gates, or backend-side flags.
- For infrastructure repos, map “release controls” to progressive rollout, policy gates, plan/apply separation, and reversible changes.
- For high-volume AI PR repositories, map “review capacity” to an explicit intake queue with WIP limits, owner assignment, labels, CODEOWNERS, and CI budget controls.
- For multi-agent work, map “implementation readiness” to resolved scope, explicit acceptance criteria, test seams, design options for important interfaces, and final review ownership.

## Safety decision rules

- If automated tests are weak or missing, do not enable automatic production deployment yet. Add the required gates first.
- If releases currently depend on long-lived environment branches, propose a migration path instead of deleting them immediately.
- If the app writes persistent data, require expand-contract migration discipline before claiming deployless-like behavior.
- If runtime release controls are impossible, document the limitation and prefer staged deployment plus fast rollback.
- If secrets or production credentials appear in the repo, stop and document a remediation task before touching deployment automation.
- If deployment scripts are not idempotent, require idempotency before auto-deploying from `main`.
- If AI PR volume is higher than review capacity, require intake labels, queue limits, and low-context PR rejection before enabling broad automation.
- If agent work lacks a clear owner, acceptance criteria, or test seam, keep it out of review-ready and merge-queue states.

## Acceptance criteria

The audit is complete when:

- the repository type and language/toolchain are identified
- the current branch/deploy/release model is documented
- the desired single-mainline model is specified
- the minimum CI checks are named
- the release-control mechanism is chosen
- the deployment automation path is described
- rollback and kill-switch behavior is defined
- migration and observability gaps are listed
- AI PR intake and multi-agent coordination risks are listed when relevant
- agent planning, implementation, and final review gates are listed when relevant
- the next skill to run is unambiguous

## Anti-goals

- Do not assume JavaScript, Node, Docker, GitHub Actions, Kubernetes, or any specific host.
- Do not remove review, tests, security controls, or compliance steps.
- Do not enable auto-deploy while known blockers remain unresolved.
- Do not conflate deployment with release.
- Do not claim that branch deletion alone creates deployless delivery.
