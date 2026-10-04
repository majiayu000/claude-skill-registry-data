---
name: github-manager
description: Use when configuring or optimising GitHub repositories for cost-effective, consistent operations — CI triggers, Actions billing, issue tracking, labelling, branch protection, or release workflow.
---

# GitHub Manager

> **CI validates what cannot be cheaply verified locally. It is not a remote test runner for every commit.**

This skill enforces disciplined, cost-aware GitHub operations. It turns GitHub from a free-for-all into a governed delivery surface: selective automation, traceable issues, consistent labels, and protected mainlines.

## When to use

- Setting up or revising a repository's CI/CD workflow
- Investigating unexpected GitHub Actions spend
- Creating or triaging issues and defining acceptance criteria
- Designing a label taxonomy or branch-protection policy
- Preparing a release process or tag strategy

## Operating model context

This skill governs the GitHub surfaces that enforce the harness contract at the repository
level. It is not general DevOps housekeeping — each procedure below maps to a harness
invariant:

- **Branch protection + required status checks** are the enforcement mechanism for the
  PR review gate and the exact-candidate binding rule. A CI check that passes on an
  unprotected branch is a claim; a passing check required by branch rules is evidence.
- **CI receipts are delivery evidence.** "It worked locally" is not an artefact. A CI
  run tied to a commit SHA is. Structure your workflow so evidence is machine-readable
  and SHA-bound, not dependent on a contributor's local environment.
- **Modifying branch protection, CI pipelines, or billing settings is an R2 action.**
  These changes affect all contributors and shared infrastructure. Classify risk, confirm
  authority, and record the decision before any write.

Use `release-readiness` to gate a specific deployment. Use this skill to configure and
audit the repository surfaces that make those gates trustworthy.

## Procedure

### 1. Rightsize CI triggers

- **Push to default branches** should run lightweight gates only (lint, typecheck, unit tests).
- **Pull requests and version tags** run the full pipeline, including packaging and cross-platform smoke tests.
- **Feature branches** do not fire CI on every push; open a PR when ready for validation.
- **Path filters** skip irrelevant jobs: docs-only changes should not rebuild the extension, code-only changes should not re-render documentation.

### 2. Minimise Actions billing

- Know the runner multipliers: Linux ×1, Windows ×2, **macOS ×10**.
- Gate expensive runners (macOS, Windows) behind PRs and releases, not every push.
- Cache dependency stores (`cache: 'pnpm'`, `cache: 'npm'`, pip, etc.).
- Do not run local-integration or exploratory tests in CI; keep them local or on-demand.
- Set a spending limit and billing alert before usage surprises you.

### 3. Structure issues and tracking

- Every issue states a **problem or outcome** and has **acceptance criteria**.
- Link PRs to issues (`Closes #123` or `Refs #123`).
- Close issues with a concise note explaining what changed and where.
- Use milestones or projects for release-scope tracking, not long-lived catch-all issues.

### 4. Label consistently

Adopt a namespaced taxonomy and avoid one-off labels:

| Namespace | Examples | Purpose |
|---|---|---|
| `kind/` | `kind/bug`, `kind/feature`, `kind/docs` | Type of work |
| `area/` | `area/ci`, `area/ui`, `area/security` | Component or domain |
| `priority/` | `priority/p0`, `priority/p1` | Triage urgency |
| `status/` | `status/blocked`, `status/needs-review` | Workflow state |

### 5. Protect the mainline

- Require PR reviews before merging to `main`.
- Require status checks to pass (lint, typecheck, test).
- Use squash or rebase merges for a linear history; avoid merge commits unless the project explicitly allows them.
- Restrict force-push and deletion on default branches.

### 6. Define the release workflow

- Tags (`v*`) trigger release builds and deployments, not manual uploads.
- A release checklist verifies version alignment, changelog entry, and rollback plan.
- Generated artifacts (VSIX, containers, packages) are produced by CI, not a local workstation.

## Outputs

- CI trigger matrix: event → jobs that run
- Monthly Actions cost estimate with runner-multiplier breakdown
- Issue template with acceptance criteria
- Label taxonomy
- Branch-protection policy
- Release checklist

## Guardrails

- **Local testing is not CI.** If a check belongs on a developer's machine, do not run it on every push.
- **macOS minutes are the silent budget killer.** A one-minute macOS job costs ten billable minutes.
- **Unconditional full pipelines scale badly.** Every unconditional job is a tax on every future commit.
- **Labels without a taxonomy become noise.** Delete or consolidate labels that do not fit the scheme.
- **Never deploy from a local build.** Release artifacts must come from CI to be reproducible.

## Anti-rationalization table

| Excuse | Counter |
|---|---|
| "Run everything on every push to be safe" | Safety is selective gates, not redundant burn. Run full checks on PRs and tags. |
| "It's only a few CI minutes" | At 10× for macOS, "a few minutes" becomes hundreds of dollars per cycle. |
| "We'll clean up labels later" | Label debt compounds fast and breaks automation that depends on them. |
| "Force-push is fine, we're a small team" | Force-push on `main` destroys recovery options. Protect the branch. |
| "I'll build the release artifact locally" | Local builds are not reproducible or auditable. CI produces release artifacts. |
