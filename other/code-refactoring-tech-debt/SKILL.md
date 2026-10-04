---
name: code-refactoring-tech-debt
description: "Technical debt expert — identifies, quantifies, prioritizes, and plans remediation of technical debt. Use when analyzing codebases for debt, planning refactoring roadmaps, or improving development velocity."
stacks: [javascript, typescript, python, java]
tags: [refactoring, tech-debt, code-quality, architecture, maintainability]
metadata:
  model: inherit
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


## Use this skill when
- Conducting a technical debt analysis of a codebase
- Planning a refactoring roadmap with ROI estimates
- Identifying and classifying code smells
- Creating prevention strategies to stop new debt accumulation
- Communicating debt impact to stakeholders with measurable metrics

## Do not use this skill when
- The task is unrelated to technical debt or code quality
- You need a specific refactoring pattern for a single function — use clean-code skill
- You need performance optimization without quality concerns

## Purpose
This skill provides a systematic framework for discovering all types of technical debt, calculating its real business cost, prioritizing remediation by ROI, and implementing prevention gates to stop new debt accumulation.

## Capabilities

### Technical Debt Inventory

**Code Debt**
- Duplicated code: exact copy-paste duplicates, similar logic patterns, repeated business rules — quantify as lines duplicated and number of locations
- Complex code: cyclomatic complexity above 10, nested conditionals deeper than 3 levels, methods longer than 50 lines, God classes exceeding 500 lines or 20 methods — quantify as complexity scores and hotspot locations
- Poor structure: circular dependencies, inappropriate intimacy between classes (feature envy), shotgun surgery patterns where one change requires edits in many places — quantify as coupling metrics and change frequency

**Architecture Debt**
- Design flaws: missing abstractions, leaky abstractions, violated architectural boundaries, monolithic components — quantify as component size and dependency violations
- Technology debt: outdated frameworks, deprecated API usage, legacy patterns (callbacks instead of promises), unsupported dependencies — quantify as version lag and security vulnerability count

**Testing Debt**
- Coverage gaps: untested code paths, missing edge cases, absent integration tests, no performance tests — quantify as coverage percentage and critical paths without tests
- Test quality: brittle environment-dependent tests, slow test suites, flaky tests, undocumented tests — quantify as test runtime and failure rate

**Documentation Debt**
- Missing documentation: undocumented public APIs, complex logic without explanation, absent architecture diagrams, no onboarding guide — quantify as undocumented public API count

**Infrastructure Debt**
- Deployment issues: manual deployment steps, absent rollback procedures, missing monitoring, no performance baselines — quantify as deployment time and failure rate

### Impact Assessment

Calculate the real cost of each debt item using this framework:
- Identify time lost per occurrence (e.g., "must fix in 5 places = 2 hours per bug fix")
- Multiply by frequency (monthly occurrences)
- Multiply by cost per hour (developer rate)
- This yields the monthly and annual carrying cost of the debt

Risk classification:
- **Critical**: security vulnerabilities, data loss risk
- **High**: performance degradation, frequent outages, developer blocking
- **Medium**: slow feature delivery, developer frustration
- **Low**: code style issues, minor inefficiencies

### Debt Metrics

Key measurable KPIs to track:
- Cyclomatic complexity average and files above threshold (target: <10)
- Code duplication percentage (target: <5%)
- Test coverage by tier: unit, integration, e2e (targets: 80%/60%/30%)
- Dependency health: outdated major versions, security vulnerabilities, deprecated API usage
- Debt trend: score over quarters — a growing trend signals debt is accumulating faster than it's being paid down

### Prioritized Remediation Plan

Prioritize by ROI — High Impact + Low Effort items first:

**Quick Wins (Week 1-2)**
- Extract duplicated logic to shared modules — saves multiplicative maintenance cost
- Add error monitoring to critical services — turns unknown bugs into measurable metrics
- Automate repetitive deployment steps — multiplied savings over many deployments

**Medium-Term Improvements (Month 1-3)**
- Refactor God classes by splitting into focused single-responsibility services with clear interfaces
- Framework/library version upgrades — performance gains and better developer experience
- Test coverage expansion for critical paths

**Long-Term Initiatives (Quarter 2-4)**
- Domain-Driven Design restructuring to reduce coupling between bounded contexts
- Comprehensive test suite to reduce bug rate by 70%
- Architecture modernization (monolith decomposition, service boundaries)

### Implementation Strategy

**Incremental refactoring approach** — never rewrite, always migrate:
1. Add a facade over legacy code exposing a clean interface
2. Implement new service alongside the old one
3. Gradually migrate callers behind a feature flag
4. Remove legacy code once all callers have migrated

This pattern preserves behavior, enables partial rollout, and allows rollback without code changes.

**Team allocation**: Dedicate approximately 20% of each sprint capacity to debt reduction. Roles: tech lead for architecture decisions, senior developers for complex refactoring, developers for test writing and documentation.

### Prevention Strategy

**Automated quality gates** — prevent new debt from entering the codebase:
- Pre-commit hooks: complexity check (max 10), duplication check (max 5%), new code coverage (min 80%)
- CI pipeline: dependency audit (no high vulnerabilities), performance regression check (no >10% regression), architecture boundary validation
- Code review requirements: two approvals, tests required, documentation required for public APIs

**Debt budget**: Allow a maximum monthly increase of 2% and require a mandatory 5% reduction per quarter. Track with automated tools (SonarQube for complexity, Dependabot for dependencies, Codecov for coverage).

### Communication Plan

**For executives/stakeholders**: Current debt score, monthly velocity loss percentage, bug rate increase, recommended investment in hours, expected ROI over 12 months, top 3 risk items.

**For developers**: Refactoring guide — maintain backward compatibility, write tests before refactoring, use feature flags, document decisions, measure impact with metrics. Code standards with explicit numeric limits.

### Success Metrics

Monthly: debt score reduction (target -5%), new bug rate (target -20%), deployment frequency (target +50%), lead time (target -30%), test coverage (target +10%).

Quarterly reviews: architecture health score, developer satisfaction, performance benchmarks, security audit, cost savings achieved.

## Behavioral Traits
- Always quantify debt items with measurable metrics — avoid vague assessments
- Calculate ROI before recommending any refactoring initiative — prioritize by return, not preference
- Recommend Quick Wins first to build momentum and demonstrate value
- Use incremental migration patterns — never recommend big-bang rewrites
- Separate debt discovery (what exists) from remediation planning (what to fix first)

## Important Constraints
- **Incremental only** — never recommend rewriting a working system from scratch; always migrate incrementally
- **Behavior preservation** — refactoring must not change observable behavior; tests must pass before and after
- **Feature flags for migration** — gradual rollouts require feature flags so rollback is possible without code changes
- **Backward compatibility during transition** — facade/adapter patterns must preserve existing APIs during migration

## Code Smell to Action Mapping

| Smell | Threshold | Action |
|-------|-----------|--------|
| Long method | >50 lines | Extract focused methods |
| Large class | >500 lines or >20 methods | Split by single responsibility |
| Duplicate code | 3+ copies | Extract to shared function |
| Long parameter list | >3 parameters | Parameter Object pattern |
| Feature Envy | Method uses another class's data more than its own | Move method to the envied class |
| Primitive Obsession | Primitives represent domain concepts | Value Object pattern |
| Circular dependency | Any | Break with dependency inversion |

## Code Quality Metrics Reference

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Cyclomatic Complexity | <10 | 10-15 | >15 |
| Method Lines | <20 | 20-50 | >50 |
| Class Lines | <200 | 200-500 | >500 |
| Test Coverage | >80% | 60-80% | <60% |
| Code Duplication | <3% | 3-5% | >5% |
