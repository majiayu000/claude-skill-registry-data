---
name: cicd
description: "Routes CI/CD requests to the correct technology skill and compares GitHub Actions, GitLab CI, Azure DevOps, Jenkins, and CircleCI for platform selection. WHEN: \"CI/CD comparison\", \"which CI/CD\", \"pipeline design\", \"CI/CD platform\", \"GitHub Actions vs\", \"Jenkins vs\", \"build pipeline\", \"release pipeline\", \"CI/CD strategy\". Do NOT use for platform-specific syntax or debugging — use the `github-actions`, `gitlab-ci`, `azure-devops`, `jenkins`, or `circleci` skill directly."
license: MIT
---

# CI/CD Platform Router

This skill routes CI/CD requests to the right technology skill and covers cross-platform comparison. Determine which technology best matches the request, then read that skill's SKILL.md for implementation depth.

## Decision Matrix

| Signal | Skill |
|--------|----------|
| GitHub Actions, workflows, `.github/workflows/`, runners, marketplace actions | `github-actions` |
| GitLab CI, `.gitlab-ci.yml`, GitLab runners, stages, artifacts, GitLab DevSecOps | `gitlab-ci` |
| Azure DevOps, Azure Pipelines, `azure-pipelines.yml`, boards, repos, artifacts | `azure-devops` |
| Jenkins, Jenkinsfile, Jenkins plugins, shared libraries, Jenkins skills/nodes | `jenkins` |
| CircleCI, config.yml, orbs, CircleCI workflows, Docker layer caching, contexts | `circleci` |
| CI/CD comparison, "which platform", pipeline architecture | Handle directly (below) |

## How to Route

1. **Extract technology signals** — platform names, config file names, CLI tools, terminology.
2. **Check for version specifics** — read the matched technology skill; version-specific nuance lives in its `references/versions/` directory when applicable (e.g. `gitlab-ci`).
3. **Comparison requests** — handle directly using the framework below.
4. **Ambiguous requests** — if the user says "set up CI/CD" without specifying a tool, gather context (source code hosting, cloud provider, team size) before routing.

## CI/CD Fundamentals

Load `references/concepts.md` when the user needs foundational understanding of CI/CD patterns that apply across all platforms.

## Platform Comparison

### Feature Matrix

| Feature | GitHub Actions | GitLab CI | Azure DevOps | Jenkins |
|---|---|---|---|---|
| **Config format** | YAML (per-workflow) | YAML (single file) | YAML or classic UI | Groovy (Declarative/Scripted) |
| **Hosting** | GitHub.com + self-hosted runners | GitLab.com + self-hosted runners | Azure + self-hosted agents | Self-hosted only |
| **Source integration** | GitHub native | GitLab native | Azure Repos, GitHub, Bitbucket | Any SCM (Git, SVN, etc.) |
| **Marketplace/Plugins** | Marketplace (Actions) | CI/CD components, templates | Task extensions (Marketplace) | 1800+ plugins |
| **Container support** | Docker-native, services | Docker-native, services, DinD | Container jobs, Docker tasks | Docker plugin, K8s plugin |
| **Secrets** | Repository/org/env secrets | CI/CD variables, Vault integration | Variable groups, Azure Key Vault | Credentials plugin, Vault |
| **Artifacts** | Upload/download actions | Job artifacts, packages | Pipeline artifacts, feeds | Archive artifacts, Artifactory |
| **Caching** | actions/cache | Cache directive | Pipeline caching | Custom (stash/unstash) |
| **RBAC** | Org/repo permissions | Group/project roles | Project-level security | Role-based (Matrix Auth) |
| **Cost** | Free tier + per-minute | Free tier + per-minute | Free tier (5 users) + per-agent | Free (OSS) + infrastructure cost |
| **OIDC/Keyless** | Native (aws, azure, gcp) | Native (jwt) | Native (service connections) | Plugin-based |

### Platform Selection Guide

| Scenario | Recommended | Why |
|---|---|---|
| **Code on GitHub, cloud-native** | GitHub Actions | Native integration, marketplace ecosystem, OIDC for cloud auth |
| **Code on GitLab, full DevSecOps** | GitLab CI | Integrated SCM + CI + CD + security scanning + container registry |
| **Azure/.NET shop, enterprise governance** | Azure DevOps | Boards + Repos + Pipelines + Artifacts unified, AAD integration |
| **Maximum flexibility, existing investment** | Jenkins | Plugin ecosystem, any SCM, any target, full control |
| **Multi-SCM, fast Docker builds** | CircleCI or GitLab CI | Docker-layer caching, orbs/components for reuse |
| **Air-gapped / on-premises only** | Jenkins or GitLab Self-Managed | Full self-hosted capability |

### Migration Paths

| From | To | Key Considerations |
|---|---|---|
| Jenkins → GitHub Actions | Rewrite Jenkinsfiles as YAML workflows, replace plugins with Actions, migrate credentials |
| Jenkins → GitLab CI | Map stages to GitLab stages, replace plugins with CI components, migrate job configs |
| Travis CI → GitHub Actions | Nearly 1:1 YAML mapping, automated migration tool available |
| Azure DevOps → GitHub Actions | Microsoft provides migration tooling, variable groups → secrets |
| CircleCI → GitHub Actions | Orbs → marketplace Actions, config.yml → workflow YAML |

## Pipeline Design Principles

### Stages

A well-designed pipeline has clear stages:

```
┌─────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Build   │──▶│   Test   │──▶│   Scan   │──▶│  Stage   │──▶│  Deploy  │
│          │   │          │   │          │   │          │   │          │
│ Compile  │   │ Unit     │   │ SAST     │   │ Deploy   │   │ Canary   │
│ Package  │   │ Integ    │   │ DAST     │   │ to stage │   │ or B/G   │
│ Artifact │   │ E2E      │   │ SCA      │   │ Smoke    │   │ Monitor  │
└─────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

### Reuse Patterns

| Pattern | GitHub Actions | GitLab CI | Azure DevOps | Jenkins |
|---|---|---|---|---|
| **Reusable unit** | Reusable workflow, composite action | CI/CD component, include template | Template (YAML), task group | Shared library |
| **Parameterization** | `inputs:` | `spec.inputs:` | `parameters:` | Method parameters |
| **Sharing** | Marketplace or org-private repos | CI/CD catalog | Task extensions | Shared library repo |

## Anti-Patterns

1. **"Works on my machine" CI** — CI environment must be reproducible. Pin all tool versions, use containers.
2. **Unparallelized pipelines** — Tests that can run concurrently should. Matrix/parallel jobs exist for this.
3. **No artifact versioning** — Every build should produce a versioned, immutable artifact. Don't rebuild for each environment.
4. **Secrets in logs** — Mask secrets, use `::add-mask::` or equivalent. Audit pipeline logs.
5. **No caching** — Downloading dependencies on every run wastes minutes. Cache aggressively.
6. **Manual approvals as the only gate** — Automated quality gates (tests, scans, coverage thresholds) should be the primary gate.

## Reference Files

- `references/concepts.md` — CI/CD pipeline theory (stages, artifacts, caching, matrix builds, security scanning integration, deployment strategies). Read for architecture and comparison questions.
