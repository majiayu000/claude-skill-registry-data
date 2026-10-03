---
name: deployless-mainline
description: Single-mainline governance for deployless repositories. Use after a deployless audit when a repo needs trunk-based branch rules, branch protection, contribution guidance, review gates, merge queue policy, AI PR intake rules, or agent-ready mainline practices.
metadata:
  priority: 6
  docs:
    - "https://trunkbaseddevelopment.com/"
    - "https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development"
  pathPatterns:
    - "CONTRIBUTING.md"
    - "CODEOWNERS"
    - ".github/pull_request_template.md"
    - ".github/workflows/**"
    - "docs/**"
  promptSignals:
    phrases:
      - "mainline"
      - "trunk based"
      - "branch protection"
      - "merge queue"
      - "long-lived branches"
      - "ai pull requests"
    allOf:
      - [main, branch]
      - [pull, request]
    anyOf:
      - "develop branch"
      - "release branch"
      - "CODEOWNERS"
      - "review gates"
    noneOf: []
    minScore: 5
---

# Single Mainline Governance for Any-Language Repositories

## Purpose

Make `main` the single long-lived branch used for integration and release, while preserving safety through review, tests, ownership, and runtime release controls.

The intended result is not “everyone commits anything directly to production.” The intended result is:

- small changes
- short-lived review branches when needed
- fast integration into `main`
- required checks before merge
- no long-lived `develop`, `staging`, `qa`, or `release/*` branches as integration backlogs
- unfinished behavior hidden behind release controls
- AI-generated PRs entering the same queue as human PRs, with clear ownership and review gates

## Preconditions

Run `deployless-audit` first. Do not apply this skill blindly. The audit should identify:

- default branch name
- existing long-lived branches
- CI provider
- test commands
- release process
- deployment dependencies on branch names
- code review rules
- compliance or approval requirements
- AI or bot PR sources, agent handoff conventions, and current PR queue pressure
- issue readiness, planning artifact, test seam, and final review conventions for agent-authored work

## Branch model target

Use this model unless repo-specific constraints require a documented exception:

```text
main                       long-lived source of truth
short-lived/topic-branch    optional, review-only, deleted after merge
hotfix branch               optional, short-lived, merged back to main immediately
release tag                 optional immutable marker, not a long-lived branch
```

Forbidden as long-lived integration branches:

```text
develop
staging
qa
release/*
env/*
production
preprod
integration
```

These names may still exist temporarily during migration, but they should not remain part of the target operating model.

## Files to inspect and possibly update

- `CONTRIBUTING.md`
- `README.md`
- `CODEOWNERS`
- `.github/pull_request_template.md` or equivalent PR templates
- `.github/workflows/*`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/config.yml`, `azure-pipelines.yml`, `buildkite.yml`
- release scripts and docs
- deployment configuration that references branch names
- docs mentioning `develop`, `staging`, `qa`, `release/*`, or manual branch promotion
- package publishing or artifact release config
- monorepo ownership files
- issue labels, project boards, merge queue configuration, stale PR automation, and bot account rules
- planning docs, ADRs, domain glossary, implementation handoff docs, and final review reports

## Implementation procedure

### 1. Confirm the default branch

Detect whether the default branch is `main`, `master`, or another name.

- If the repo already uses `main`, preserve it.
- If it uses `master`, do not rename automatically unless the user asked for branch renaming. Document `main` as the conceptual trunk and adapt wording to the actual default branch if needed.
- If deployment config points to another production branch, document the current behavior before changing it.

### 2. Add or update contribution guidance

Create or update `CONTRIBUTING.md` with:

```markdown
# Mainline development

This repository uses a single long-lived mainline branch.

- Keep changes small and merge frequently.
- Use short-lived branches only for review.
- Do not create long-lived feature, develop, staging, qa, or release branches.
- Keep `main` deployable at all times.
- Hide incomplete product behavior behind runtime release controls.
- Prefer forward fixes and feature-flag rollback over branch reverts.
- Use expand-contract migrations for persistent data changes.
```

Adapt wording to the repo's existing tone and compliance requirements.

### 3. Add merge readiness checklist

Add a checklist to the PR template or contribution docs:

```markdown
## Mainline readiness

- [ ] The change is small enough to review safely.
- [ ] The change is deployable when merged to main.
- [ ] AI-generated work has clear intent, scope, owner, and linked issue or decision.
- [ ] Scope, acceptance criteria, and test seams are resolved enough for an agent to work independently.
- [ ] Incomplete or risky behavior is behind a runtime release control.
- [ ] Required tests were added or updated.
- [ ] Final review checked both repository standards and the originating spec or issue.
- [ ] Observability was added for new production behavior.
- [ ] Data migrations are backward-compatible, if any.
- [ ] Rollback or kill-switch behavior is documented.
```

If the repo does not use PRs, put the same checklist in `CONTRIBUTING.md` under “Pre-merge checklist.”

### 4. Align CI with mainline

Update CI triggers so the same required checks run on:

- pull requests or merge requests into `main`
- direct pushes to `main`, if allowed
- merge queue/batch merge events, if the platform supports them

Do not assume a CI provider. Use the existing CI system.

Minimum checks should include the repo-appropriate equivalent of:

- dependency install or restore
- formatting check
- lint or static analysis
- type check or compile
- unit tests
- integration or contract tests where available
- security/dependency checks where already present
- migration validation where persistent data exists
- build/package verification

### 5. Document branch protection rules

If the connector or repo access allows branch protection changes, configure them only when safe. Otherwise create `docs/mainline-branch-protection.md` with desired settings:

```markdown
# Mainline branch protection

Required for `main`:

- Pull request or equivalent review before merge, unless direct-to-main is explicitly approved.
- Required status checks must pass.
- Branch must be up to date or merge queue must be enabled.
- No force-pushes.
- No deletion of `main`.
- Code owner review for owned paths.
- Signed commits if the repo already requires them.
- Admin bypass only for documented break-glass cases.
```

### 6. Replace branch-based release language

Search docs and scripts for branch-promotion vocabulary:

- `merge to develop`
- `promote staging to production`
- `cut release branch`
- `qa branch`
- `production branch`
- `release/*`

Replace with mainline-oriented language:

- merge to `main`
- deploy from `main`
- release through runtime controls
- validate via preview/staging environment generated from commit or artifact
- tag immutable release points only if needed

### 7. Preserve necessary compliance gates

Some environments require approvals, change tickets, or segregation of duties. Do not remove them. Instead, make them part of the `main` merge or deployment gate.

Examples:

- approval required before enabling a flag to 100%
- approval required before production deploy job proceeds
- change ticket linked in PR template
- CODEOWNERS required for sensitive paths
- audit log entry for flag changes

## AI PR and multi-agent governance

When AI agents generate PRs, keep them inside the same mainline discipline:

- require draft PRs until intent, scope, tests, and risk are documented
- require a linked issue, task, incident, or decision for every agent PR
- label AI PRs separately from human PRs without giving them weaker gates
- cap active AI PRs per owner area so review and CI do not starve
- require one accountable owner for every AI PR
- reject or park low-context PRs that only claim generic cleanup or improvement
- prevent multiple agents from editing the same risky area without an explicit coordinator
- use merge queues for review-ready PRs instead of long-lived integration branches

Suggested labels:

```text
ai/generated
ai/needs-intent
ai/needs-owner
ai/needs-scope
ai/needs-tests
ai/conflict-risk
ai/ready-for-human-review
ai/parked
ai/rejected
```

Recommended agent branch names:

```text
agent/<tool-or-agent>/<ticket-or-area>-<short-slug>
bot/<provider>/<ticket-or-area>-<short-slug>
```

Do not create a long-lived AI staging branch. AI work should be split, reviewed, and merged through the same single mainline.

## Agent execution loop

Use this loop for agent-authored deployless work:

1. Orient on repository instructions, domain glossary, relevant ADRs, and the source issue or plan.
2. Challenge unclear scope before implementation. Ask one blocking question at a time only when the answer cannot be inferred safely.
3. Convert ready work into vertical slices that are independently buildable, reviewable, and testable.
4. For important interface or module boundaries, generate multiple distinct design options before choosing one.
5. Build non-trivial changes with a vertical test-first loop: one behavior, failing test, minimal implementation, refactor after green.
6. Run local checks regularly, with focused checks during the work and broader checks before final review.
7. Review the final diff on two axes: repository standards and fidelity to the originating spec, issue, or plan.
8. Classify review findings as accepted, rejected, deferred, or requiring a human decision before merge.

The primary coordinator remains accountable for merge readiness. Independent agents can critique, design, implement, or review, but they do not decide to merge by themselves.

## Migration plan from long-lived branches

When a repo currently depends on long-lived branches, use a staged migration:

1. Freeze new work on long-lived branches.
2. Rebase or merge active work into short-lived branches targeting `main`.
3. Move environment deployment triggers away from branch names and toward commits/artifacts from `main`.
4. Convert unfinished work to runtime release controls.
5. Delete stale branches only after deployment and release docs no longer reference them.
6. Protect `main` and document the new process.

## Monorepo rules

For monorepos:

- `main` is still the only long-lived branch.
- Use path-aware CI to run affected checks.
- Keep ownership in `CODEOWNERS` or equivalent.
- Deploy services independently from the same mainline when possible.
- Use per-service release controls.
- Avoid service-specific long-lived branches.

## Library/package rules

For libraries:

- `main` must always build and pass tests.
- Publishing may be tag-based, but tags are immutable markers, not integration branches.
- Use compatibility tests and semantic versioning policy where applicable.
- Use feature flags only for runtime libraries that can evaluate runtime context; otherwise use versioned APIs and compatibility shims.

## Infrastructure repo rules

For infrastructure-as-code repos:

- `main` must represent intended infrastructure state.
- Pull requests should run format, validate, plan, and policy checks.
- Production apply can remain approval-gated.
- Do not maintain long-lived environment branches unless there is a documented regulatory reason.
- Prefer environment directories, workspaces, stacks, or overlays over environment branches.

## Output

Create or update:

- `CONTRIBUTING.md`
- PR/MR template, if present or appropriate
- `docs/mainline-branch-protection.md`
- `docs/deployless-mainline-plan.md`, appending a “Mainline governance” section
- AI PR intake labels, queue rules, and agent branch naming docs when relevant
- agent execution-loop guidance in contribution or workflow docs
- CI config triggers and required checks, when safe to edit

## Acceptance criteria

This skill is complete when:

- the repo has documented single-mainline rules
- long-lived branch usage is identified and either removed or given a migration plan
- PR/merge readiness criteria mention deployability and release controls
- CI runs required checks for changes targeting `main`
- branch protection expectations are documented or configured
- AI-generated PRs have the same deployability and ownership requirements as human PRs
- agent-authored work has documented scope challenge, test-first implementation expectations, and final review gates
- deployment/release docs no longer teach branch promotion as the target model

## Anti-goals

- Do not remove approvals required for safety, security, or compliance.
- Do not delete active branches without explicit instruction and a migration plan.
- Do not force direct commits to `main` if PRs are the established review mechanism.
- Do not replace runtime release controls with branch discipline alone.
- Do not auto-merge AI-generated PRs just because CI passes.
- Do not let agent volume create a hidden second integration process.
- Do not let critique, design, implementation, and review agents make unowned merge decisions.
