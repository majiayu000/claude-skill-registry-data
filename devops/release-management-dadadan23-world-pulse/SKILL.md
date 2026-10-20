---
name: "release-management"
description: 'Implement release management with versioning strategies, deployment strategies, rollback procedures, and release automation. Use when planning release pipelines, choosing deployment strategies (blue-green, canary, rolling), automating releases, or designing rollback procedures.'
metadata:
 author: "AgentX"
 version: "2.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# Release Management & Deployment Strategies

> **Purpose**: Decision guides, versioning rules, deployment strategy selection, and release checklists.
> For full YAML examples and runbook templates, see the [references/](references/) directory.

---

## When to Use This Skill

- Planning release pipelines and strategies
- Choosing deployment strategies (blue-green, canary, rolling)
- Implementing automated release workflows
- Designing rollback procedures
- Setting up versioning with SemVer or CalVer

## Prerequisites

- CI/CD pipeline infrastructure
- Version control system (Git)

## Quick-Start: Deployment Strategy Selection

Pick your strategy **first** - everything else follows from this choice.

| Strategy | Best For | Downtime | Rollback Speed | Infra Cost | Complexity |
|----------|----------|----------|----------------|------------|------------|
| **Rolling** | Most apps, K8s-native | None | Medium (pod-by-pod) | Same | Low |
| **Blue-Green** | Zero-downtime critical | None | **Instant** (swap) | **2** | Medium |
| **Canary** | Risk-sensitive releases | None | Medium (scale to 0) | +10-25% | High |
| **Feature Flags** | Gradual user rollout | None | **Instant** (toggle) | Same | Medium |
| **Recreate** | Dev/Test environments | **Yes** | Fast (redeploy) | Same | Low |

**Decision tree:**

```
Need zero-downtime?
+- No -> Recreate (dev/test only)
- Yes
 +- Need instant rollback?
 | +- Yes -> Blue-Green (if budget allows 2 infra)
 | - Yes -> Feature Flags (if code-level control preferred)
 - Need gradual risk reduction?
 +- Yes, by traffic % -> Canary
 - Default / simplest -> Rolling
```

> **Full YAML examples** for each strategy: [references/deployment-strategy-examples.md](references/deployment-strategy-examples.md)

---

## Table of Contents

1. [Deployment Strategy Selection](#quick-start-deployment-strategy-selection)
2. [Versioning Strategies](#versioning-strategies)
3. [Deployment Strategies - Concepts](#deployment-strategies--concepts)
4. [Rollback Procedures](#rollback-procedures)
5. [Release Pipeline Architecture](#release-pipeline-architecture)
6. [Release Automation](#release-automation)
7. [Release Checklist](#release-checklist)
8. [Best Practices](#best-practices)
9. [Related Skills & Resources](#related-skills--resources)

---

## Versioning Strategies

### Choosing a Versioning Scheme

```
Is your release cadence time-based (monthly/quarterly)?
+- Yes -> CalVer (YYYY.MM.DD)
- No
 +- Do you expose a public API or library?
 | - Yes -> SemVer (MAJOR.MINOR.PATCH)
 - Internal service / continuous delivery?
 - Commit-Based (v1.0.{count}+{sha})
```

### Semantic Versioning (SemVer)

Format: `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**Version Increment Rules:**

| Bump | When | Example |
|------|------|---------|
| **MAJOR** | Incompatible / breaking API changes | `1.x.x -> 2.0.0` |
| **MINOR** | New functionality, backward-compatible | `1.1.x -> 1.2.0` |
| **PATCH** | Bug fixes, backward-compatible | `1.1.1 -> 1.1.2` |
| **PRERELEASE** | alpha -> beta -> rc progression | `2.0.0-rc.1` |
| **BUILD** | Metadata only (commit hash, CI number) | `2.0.0+build.47` |

**Key rules:**
- Once a version is released, its contents **must not** change
- Pre-release versions (`-alpha.1`, `-beta.2`, `-rc.1`) have lower precedence than the release
- Build metadata (`+build.1`) is ignored for version precedence

### Calendar Versioning (CalVer)

Format: `YYYY.MM[.DD][.MICRO]`

**When to use:**
- Time-based release cadences (monthly, quarterly)
- Marketing-driven version numbers
- Consumer products with regular update schedules
- Ubuntu, pip, and similar projects use CalVer

### Commit-Based Versioning

Format: `v{MAJOR}.{MINOR}.{COMMIT_COUNT}+{SHORT_SHA}`

Best for internal services with continuous delivery where every merge to `main` is a release candidate.

### Pre-Release Label Progression

| Label | Meaning | Audience |
|-------|---------|----------|
| `alpha.N` | Early testing, unstable | Internal team |
| `beta.N` | Feature-complete, bugs expected | Early adopters |
| `rc.N` | Release candidate, production-ready | Wider testing |
| `snapshot` | Development build | CI only |

> **Automation**: Version bump + changelog workflows -> [references/release-automation-workflows.md](references/release-automation-workflows.md)

---

## Deployment Strategies - Concepts

### Blue-Green Deployment

Two identical production environments; deploy to inactive, test, swap traffic.

| Aspect | Detail |
|--------|--------|
| **Mechanism** | DNS / load-balancer swap between Blue Green |
| **Rollback** | Instant - swap back to previous environment |
| **Tradeoff** | Requires 2 infrastructure; database migrations need care |

**Pros:** Zero downtime - Instant rollback - Full pre-switch testing
**Cons:** Double infrastructure cost - DB migration complexity

### Canary Deployment

Route a small percentage of traffic to the new version; expand on success.

| Aspect | Detail |
|--------|--------|
| **Mechanism** | Weighted routing (10% -> 25% -> 50% -> 100%) |
| **Rollback** | Scale canary to 0 replicas |
| **Tradeoff** | Needs monitoring infra; longer total deploy time |

**Pros:** Low risk - Real user feedback - Gradual rollout
**Cons:** Complex setup - Requires robust observability

### Rolling Deployment

Replace instances one-at-a-time (or in small batches).

| Aspect | Detail |
|--------|--------|
| **Mechanism** | Orchestrator replaces pods with `maxSurge` / `maxUnavailable` |
| **Rollback** | Automatic on failed health checks (K8s native) |
| **Tradeoff** | Mixed versions during rollout window |

**Pros:** Built-in to K8s / ECS - Zero downtime - Automatic rollback
**Cons:** Briefly mixed versions - Slower than blue-green

### Feature Flags / Feature Toggles

Deploy code with features disabled; enable via configuration per user/percentage.

| Aspect | Detail |
|--------|--------|
| **Mechanism** | Runtime config toggle (LaunchDarkly, Azure App Config, custom) |
| **Rollback** | Instant - flip flag to `false` |
| **Tradeoff** | Flag debt accumulates; needs cleanup process |

**Pros:** Instant rollback - Decouple deploy from release - A/B testing
**Cons:** Code complexity - Stale flag cleanup required

> **Full YAML & K8s manifests** for all strategies: [references/deployment-strategy-examples.md](references/deployment-strategy-examples.md)

---

## Rollback Procedures

### Rollback Decision Criteria

Trigger a rollback when **any** of these thresholds are breached post-deploy:

| Signal | Threshold | Action |
|--------|-----------|--------|
| Error rate | > 2 baseline | Automatic rollback |
| Health check | HTTP != 200 for > 2 min | Automatic rollback |
| P95 latency | > 50% degradation | Investigate -> manual rollback |
| Critical bug | Functionality broken | Immediate manual rollback |
| Security vuln | Any CVE discovered | Immediate manual rollback |

### Rollback Strategies by Deployment Type

| Deployment Type | Rollback Method | Speed |
|-----------------|----------------|-------|
| **Blue-Green** | Swap traffic back to previous env | Instant |
| **Canary** | Scale canary replicas to 0 | < 1 min |
| **Rolling** | `kubectl rollout undo` | 2-5 min |
| **Feature Flags** | Disable flag | Instant |
| **Container** | Redeploy previous image tag | 2-5 min |

### Database Rollback Principles

1. **Forward-only migrations** - never drop columns; deprecate first
2. **Backward-compatible changes** - new code must work with old schema during rollout
3. **Blue-green with separate DBs** - rollback by switching connection string
4. **Always test undo scripts** in staging before production

> **Full rollback scripts** (automated + manual + DB): [references/rollback-scripts.md](references/rollback-scripts.md)

---

## Release Pipeline Architecture

A release pipeline should follow this stage progression:

```
Validate Tag -> Build -> Test -> Create Release -> Deploy Staging
 -> Smoke Tests -> Deploy Production -> Post-Deploy Verification
```

**Key pipeline principles:**
- Trigger on semantic version tags (`v*.*.*`)
- Build once, deploy the **same artifact** to every environment
- Gate production deployment behind staging smoke tests
- Use GitHub Environments with required reviewers for production
- Generate changelog automatically from conventional commits
- Attach build artifacts to GitHub Releases

> **Full pipeline YAML** (GitHub Actions + Azure Pipelines): [references/release-pipeline-examples.md](references/release-pipeline-examples.md)

---

## Release Automation

### What to Automate

| Task | Tool / Approach |
|------|-----------------|
| **Version bumping** | Conventional Commits -> `npm version` / `dotnet-gitversion` |
| **Changelog generation** | `git log --grep` by type (feat/fix/chore) |
| **Tag + Release creation** | `softprops/action-gh-release` or `gh release create` |
| **Pre-release detection** | Tag contains `-alpha` / `-beta` -> mark as pre-release |
| **Smoke tests** | Automated health check + critical-path tests post-deploy |
| **Rollback trigger** | Health check failure -> auto-redeploy previous version |
| **Notifications** | Slack / Teams webhook on deploy success or failure |

### Conventional Commits -> Version Bump Mapping

| Commit Prefix | Version Bump | Example Message |
|---------------|-------------|-----------------|
| `feat:` | MINOR | `feat: add dark mode support` |
| `fix:` | PATCH | `fix: resolve login timeout (#123)` |
| `BREAKING CHANGE:` | MAJOR | `feat!: redesign auth API` |
| `chore:` / `docs:` | No bump | `docs: update README` |

> **Full automation workflows**: [references/release-automation-workflows.md](references/release-automation-workflows.md)

---

## Release Checklist

### Pre-Release

- [ ] All tests passing (unit, integration, e2e)
- [ ] Code coverage 80%
- [ ] Security scan completed (dependencies + SAST)
- [ ] Dependencies updated and audited
- [ ] Changelog generated from conventional commits
- [ ] Release notes drafted
- [ ] Migration scripts tested in staging
- [ ] Rollback procedure documented and tested
- [ ] Stakeholders notified of release window

### Deployment

- [ ] Deploy to staging environment
- [ ] Smoke tests passed (staging)
- [ ] Load / performance testing completed
- [ ] Deploy to production (via chosen strategy)
- [ ] Smoke tests passed (production)
- [ ] Monitoring dashboards reviewed

### Post-Release

- [ ] Health checks verified (HTTP 200, all endpoints)
- [ ] Error rate at or below baseline
- [ ] P95 latency at or below baseline
- [ ] User feedback channels monitored
- [ ] Incident response team aware and on-call
- [ ] Documentation updated (API docs, runbook, changelog)
- [ ] Release announcement sent to stakeholders

> **Communication template + runbook**: [references/release-runbook-template.md](references/release-runbook-template.md)

---

## Best Practices

### [PASS] DO

- Use semantic versioning consistently; tag every release in VCS
- Maintain changelogs automatically via conventional commits
- Version APIs explicitly (URL path or header)
- Always test in staging before production
- Use gradual rollouts (canary / feature flags) for high-risk changes
- Monitor error rates and latency during and after deployment
- Have a **tested** rollback plan before every release
- Document procedures in a runbook
- Notify stakeholders before the deployment window
- Communicate breaking changes with migration guides
- Automate version bumping, changelog generation, and smoke tests
- Trigger automated rollback on health check failure
- Establish baseline metrics before each release
- Implement `/health` and `/ready` endpoints on every service

### [FAIL] DON'T

- Deploy on Fridays, holidays, or outside on-call hours
- Skip staging validation - even for "small" changes
- Deploy without a documented rollback plan
- Bundle multiple major changes into a single release
- Skip versions or hard-code version numbers
- Deploy without active monitoring and on-call coverage
- Ignore failed health checks
- Rush deployments under time pressure

---

## Related Skills & Resources

**Related Skills:**
- [GitHub Actions & Workflows](../github-actions-workflows/SKILL.md)
- [YAML Pipelines](../yaml-pipelines/SKILL.md)
- [Version Control](../../development/version-control/SKILL.md)
- [Monitoring & Logging](../../development/logging-monitoring/SKILL.md)

**External Resources:**
- [Semantic Versioning Specification](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Kubernetes Deployment Strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Martin Fowler - BlueGreenDeployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)

**Reference Files** (full examples, scripts, and templates):

| Reference | Contents |
|-----------|----------|
| [release-pipeline-examples.md](references/release-pipeline-examples.md) | GitHub Actions + Azure Pipelines YAML |
| [deployment-strategy-examples.md](references/deployment-strategy-examples.md) | Blue-Green, Canary, Rolling, Feature Flag YAML |
| [rollback-scripts.md](references/rollback-scripts.md) | Automated + manual rollback scripts |
| [release-automation-workflows.md](references/release-automation-workflows.md) | Version bump + changelog generation workflows |
| [release-runbook-template.md](references/release-runbook-template.md) | Communication template + production runbook |

---

**Version**: 2.0.0
**Author**: AgentX
**Last Updated**: February 10, 2026

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [`version-bump.ps1`](scripts/version-bump.ps1) | Bump semantic version (major/minor/patch) | `./scripts/version-bump.ps1 -BumpType minor` |
| [`generate-changelog.ps1`](scripts/generate-changelog.ps1) | Generate changelog from conventional commits | `./scripts/generate-changelog.ps1 [-Version 2.0.0]` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Failed deployment with no rollback | Always deploy with rollback plan, use blue-green or canary for zero-downtime |
| Version conflicts between environments | Use immutable artifacts (Docker images, versioned packages) across all stages |