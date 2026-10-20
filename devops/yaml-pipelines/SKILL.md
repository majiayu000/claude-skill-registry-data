---
name: "yaml-pipelines"
description: 'Build YAML-based CI/CD pipelines across Azure Pipelines and GitLab CI with progressive disclosure. Use when creating Azure DevOps YAML pipelines, configuring GitLab CI/CD, designing multi-stage pipelines, implementing pipeline templates, or managing pipeline secrets and variables.'
metadata:
 author: "AgentX"
 version: "2.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
compatibility:
 platforms: ["azure-devops", "gitlab"]
---

# YAML Pipelines & CI/CD Configuration

> **Purpose**: Quick-reference guide for YAML-based CI/CD pipelines. Start here for platform selection, core patterns, and best practices. Dive into reference files for full examples.

---

## When to Use This Skill

- Creating Azure DevOps YAML pipelines
- Configuring GitLab CI/CD pipelines
- Designing multi-stage deployment pipelines
- Implementing pipeline templates and variable groups
- Managing pipeline secrets and caching

## Prerequisites

- Azure DevOps or GitLab project access
- YAML syntax knowledge
- CI/CD concepts understanding

## Platform Comparison - Start Here

| Feature | Azure Pipelines | GitLab CI | GitHub Actions |
|---------|----------------|-----------|----------------|
| **Config File** | `azure-pipelines.yml` | `.gitlab-ci.yml` | `.github/workflows/*.yml` |
| **Stages** | [PASS] Native | [PASS] Native | [WARN] Jobs only |
| **Templates** | [PASS] Full support | [PASS] Includes/Extends | [PASS] Reusable workflows |
| **Caching** | [PASS] Cache task | [PASS] Built-in | [PASS] actions/cache |
| **Environments** | [PASS] Native | [PASS] Native | [PASS] Native |
| **Approvals** | [PASS] Environment gates | [PASS] Manual `when` | [PASS] Environment rules |
| **Matrix** | [PASS] `strategy.matrix` | [PASS] `parallel.matrix` | [PASS] `strategy.matrix` |
| **Secrets** | [PASS] Variable groups | [PASS] CI/CD Variables | [PASS] Secrets |
| **Self-hosted** | [PASS] Agent pools | [PASS] Runners | [PASS] Self-hosted runners |
| **Best for** | Azure-heavy orgs | All-in-one DevOps | Open source / GitHub |

---

## Decision Tree - Choosing a Platform

```
Is your code hosted on GitHub?
+- YES -> Use GitHub Actions (see ../github-actions-workflows/SKILL.md)
+- NO
| +- Using Azure DevOps for work items & repos?
| | - YES -> Use Azure Pipelines
| +- Using GitLab for repos & issue tracking?
| | - YES -> Use GitLab CI/CD
| - Need multi-platform or hybrid?
| - Use Azure Pipelines (broadest agent/pool support)
```

**Key considerations**:
- **Azure Pipelines**: Best native integration with Azure services, variable groups, service connections, and approval gates.
- **GitLab CI**: Tightest integration when you already use GitLab for SCM + issues + registry.
- **GitHub Actions**: Ideal for open-source and GitHub-native workflows (covered in its own skill).

---

## Core Concepts

### Pipeline Anatomy

Every YAML pipeline shares these building blocks:

| Concept | Azure Pipelines | GitLab CI |
|---------|----------------|-----------|
| **Trigger** | `trigger:` / `pr:` | `rules:` / `only:` / `except:` |
| **Stage** | `stages: [{stage: ...}]` | `stages: [build, test, deploy]` |
| **Job** | `jobs: [{job: ...}]` | Job name at root level |
| **Step** | `steps: [{script: ...}]` | `script:` array |
| **Template** | `template:` keyword | `include:` + `extends:` |
| **Variable** | `variables:` / `parameters:` | `variables:` |
| **Artifact** | `PublishPipelineArtifact` | `artifacts:` |
| **Cache** | `Cache@2` task | `cache:` keyword |
| **Environment** | `environment:` on deployment | `environment:` on job |

---

## Minimal Examples

### Azure Pipelines - Build + Deploy

```yaml
# azure-pipelines.yml
trigger: [main]

pool:
 vmImage: 'ubuntu-latest'

variables:
 buildConfig: 'Release'

stages:
- stage: Build
 jobs:
 - job: BuildJob
 steps:
 - script: dotnet build --configuration $(buildConfig)
 - script: dotnet test --no-build
 - publish: $(Build.ArtifactStagingDirectory)
 artifact: drop

- stage: Deploy
 dependsOn: Build
 condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
 jobs:
 - deployment: Production
 environment: production
 strategy:
 runOnce:
 deploy:
 steps:
 - download: current
 artifact: drop
 - script: echo "Deploying..."
```

> **Full examples**: [references/azure-pipelines-examples.md](references/azure-pipelines-examples.md)

### GitLab CI - Build + Deploy

```yaml
# .gitlab-ci.yml
image: node:20
stages: [build, test, deploy]

cache:
 paths: [node_modules/]

build:
 stage: build
 script: [npm ci, npm run build]
 artifacts:
 paths: [dist/]

test:
 stage: test
 script: [npm test]

deploy:production:
 stage: deploy
 script: [npm run deploy:production]
 environment: { name: production }
 rules:
 - if: '$CI_COMMIT_BRANCH == "main"'
 when: manual
```

> **Full examples**: [references/gitlab-ci-examples.md](references/gitlab-ci-examples.md)

---

## Pipeline Design Patterns (Summary)

| Pattern | When to use | Key idea |
|---------|------------|----------|
| **Sequential** | Simple build -> test -> deploy | Each stage `dependsOn` the prior |
| **Parallel jobs** | Independent test suites | Multiple jobs in one stage |
| **Fan-out / Fan-in** | Build once, test many, deploy once | Parallel stage converges to single deploy |
| **Canary** | Progressive production rollout | Deploy to canary -> validate -> full rollout |
| **Matrix** | Cross-platform / multi-version | `strategy.matrix` with OS or runtime combos |
| **Environment promotion** | Dev -> QA -> Staging -> Prod | `dependsOn` chain with approval gates |

> **Full pattern YAML**: [references/pipeline-design-patterns.md](references/pipeline-design-patterns.md)

---

## Multi-Stage Pipelines (Summary)

Multi-stage pipelines split CI and CD into discrete, gated stages.

**Azure**: Use `stages:` with `deployment` jobs, `environment:` for gate approvals, and `condition:` for branch filtering.

**GitLab**: Use named stages with `environment:`, `when: manual` for approval gates, and `rules:` for branch filtering.

| Capability | Azure | GitLab |
|-----------|-------|--------|
| Approval gates | Environment checks & approvals | `when: manual` |
| Branch filters | `condition:` expressions | `rules:` / `only:` |
| Artifact passing | `download: current` | `dependencies:` / `needs:` |
| Rollback | Re-run previous deployment | Re-trigger prior stage |

> **Full multi-stage YAML**: [references/multi-stage-pipelines.md](references/multi-stage-pipelines.md)

---

## Templates, Variables, Caching (Summary)

### Templates & Reusability

- **Azure**: `template:` keyword with `parameters:`. Supports step, job, and stage templates.
- **GitLab**: `include:` (local/remote/project) + `extends:` for inheritance.

### Variables & Parameters

- **Azure**: `variables:` (compile/runtime), `parameters:` (typed inputs), variable groups.
- **GitLab**: `variables:` (global/job), CI/CD UI variables, `dotenv` artifacts.

### Caching

- **Azure**: `Cache@2` task with composite key (`OS | lockfile`).
- **GitLab**: `cache:` with `key:`, `paths:`, `policy:` (pull/push/pull-push).

### Conditions

- **Azure**: `condition:` with expressions - `eq()`, `and()`, `startsWith()`.
- **GitLab**: `rules:` with `if:`, `changes:`, `exists:`, `when:`.

> **Full reference**: [references/templates-variables-caching.md](references/templates-variables-caching.md)

---

## Security & Secrets

### Principles

1. **Never hardcode secrets** - use platform secret stores
2. **Least privilege** - scope service connections and tokens narrowly
3. **Mask secrets** - both platforms auto-mask; verify with `echo` tests
4. **Rotate regularly** - automate rotation where possible
5. **Scan continuously** - integrate SAST, dependency scanning, secret detection

### Platform Secret Stores

| Platform | Store | Access pattern |
|----------|-------|----------------|
| Azure Pipelines | Variable groups + Key Vault | `AzureKeyVault@2` task, `$(secret)` |
| GitLab CI | Settings -> CI/CD -> Variables | `$SECRET_NAME`, protected/masked flags |

### Security Scanning Checklist

- [ ] SAST (static analysis) in test stage
- [ ] Dependency scanning for known CVEs
- [ ] Secret detection in pre-commit and CI
- [ ] Container image scanning (if applicable)
- [ ] License compliance checks

> **Full security examples**: [references/templates-variables-caching.md](references/templates-variables-caching.md) (security section)

---

## Best Practices

### [PASS] DO

**Pipeline Structure:**
- Use multi-stage pipelines for complex workflows
- Separate build, test, and deploy stages
- Implement proper stage dependencies
- Use templates for reusable logic

**Performance:**
- Cache dependencies aggressively (lockfile-keyed)
- Use matrix builds for parallel testing
- Minimize artifact size and retention
- Parallelize independent jobs

**Security:**
- Store secrets in platform-native secret stores
- Use protected variables for production
- Scan for vulnerabilities automatically
- Implement least-privilege service connections
- Never log or echo sensitive values

**Testing:**
- Run tests in CI - fail the build on failure
- Publish test results and coverage reports
- Fail fast on critical errors
- Test deployment process in lower environments first

**Deployment:**
- Use environment-specific configurations
- Implement approval gates for production
- Test rollback procedures
- Monitor deployment health post-release

### [FAIL] DON'T

**Anti-Patterns:**
- Hardcode secrets or credentials in YAML
- Skip testing stages for "quick" deploys
- Deploy to production from feature branches
- Ignore pipeline failures ("it'll fix itself")
- Build monolithic single-job pipelines

**Performance Anti-Patterns:**
- Run all jobs sequentially when they can be parallel
- Skip caching for dependencies restored every run
- Retain all artifacts indefinitely (set `expire_in`)
- Run unnecessary steps on every trigger

**Security Anti-Patterns:**
- Echo secrets in scripts or expose in artifacts
- Use org-wide service connections for single projects
- Skip security scanning to "save time"
- Share production credentials across environments

---

## Reference Files

| Topic | File |
|-------|------|
| Azure Pipelines full examples | [references/azure-pipelines-examples.md](references/azure-pipelines-examples.md) |
| GitLab CI/CD full examples | [references/gitlab-ci-examples.md](references/gitlab-ci-examples.md) |
| Pipeline design patterns (YAML) | [references/pipeline-design-patterns.md](references/pipeline-design-patterns.md) |
| Multi-stage pipelines (Azure + GitLab) | [references/multi-stage-pipelines.md](references/multi-stage-pipelines.md) |
| Templates, variables, caching, security | [references/templates-variables-caching.md](references/templates-variables-caching.md) |

---

## Related Skills

- [GitHub Actions & Workflows](../github-actions-workflows/SKILL.md) - GitHub-native CI/CD
- [Release Management](../release-management/SKILL.md) - Versioning, changelogs, release flows
- [Security](../../architecture/security/SKILL.md) - Application security practices
- [Remote Git Operations](../remote-git-operations/SKILL.md) - Branch strategies and git workflows

## Resources

- [Azure Pipelines Documentation](https://learn.microsoft.com/azure/devops/pipelines/)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [YAML Specification](https://yaml.org/spec/)

---

**Version**: 2.0.0
**Author**: AgentX
**Last Updated**: February 10, 2026

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Pipeline YAML validation error | Use the pipeline editor validation feature, check indentation and syntax |
| Secret not available in pipeline | Check variable group is linked, verify secret scope matches stage/job |