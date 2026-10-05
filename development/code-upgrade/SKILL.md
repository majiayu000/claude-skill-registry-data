---
name: code-upgrade
description: Safely upgrade dependencies or migrate framework versions. Use when user asks to upgrade, update dependencies, or migrate to a new version.
---

Safely upgrade dependencies or migrate framework versions.

## Process

- If code changes are involved, inspect with `jj diff -s`; restrict with `jj diff -- path`.

### Step 1 - Identify Upgrade Type

Clarify the target if unclear:

- **Single dependency**: one package (e.g., `react 18 -> 19`).
- **All dependencies**: all packages to latest compatible versions.
- **Framework migration**: major version upgrade with breaking changes (e.g., `Next.js 13 -> 15`).
- **Language version**: runtime update (e.g., `Python 3.11 -> 3.12`).

### Step 2 - Analyze Current State

- Detect project type and package manager:
  - JS/TS: `package.json`, lockfiles, scripts.
  - Python: `pyproject.toml`, `requirements*.txt`, `uv.lock`, `poetry.lock`.
  - Rust: `Cargo.toml`, `Cargo.lock`.
  - Go: `go.mod`, `go.sum`.
  - Ruby: `Gemfile`, `Gemfile.lock`.
  - Nix: `flake.nix`, `flake.lock`, `shell.nix` (read the `nix` skill).
- Read dependency files to identify current versions.
- Identify test, lint/check, build, and format commands from instructions, task runners, wrappers, and scripts.
- Note lockfiles but do not edit them manually.

### Step 3 - Research Changes

Apply a researcher lens to research breaking changes for upgrading {package} from {current_version} to {target_version}:

- Prefer official documentation over blog posts; cite sources with URLs.
- Separate confirmed facts from plausible interpretations; note version requirements.
- Lead with the single most actionable recommendation.

Find official migration guides, changelogs, deprecated API replacements, common pitfalls, dependency manager commands, security advisories, and verification steps. Synthesize findings, prioritizing official sources.

### Step 4 - Generate Plan

Develop an upgrade plan from the research.

- For major/broad/high-risk upgrades:
  - Apply a reviewer lens to review the plan for breaking changes, behavior regressions, and project-convention risks:
    - Ground findings in file paths and line numbers; prioritize the migration-risk lens.
    - Distinguish confirmed findings from speculative risks.
  - Apply an auditor lens to audit the plan for production risks:
    - Data loss, migration hazards, rollback safety, contract compatibility.
    - Flag only material risk; this is a final gate, not iterative style review.

- For framework migrations or changes crossing module boundaries, apply an architect lens to the migration:
  - Map current module boundaries, ownership, and dependency direction first.
  - Recommend the smallest migration path that preserves invariants.
  - Avoid speculative generality.

- The plan must address: deprecated API replacements; breaking changes to address; dependency manager commands to run; lockfile updates (via the package manager only); post-migration verification commands (test, build, lint).
- Seek user approval before executing broad or risky upgrades.

### Step 5 - Execute Upgrades

Once approved, apply a worker lens to apply the upgrade changes:

- Read files before editing; keep diffs minimal, idiomatic, and behavior-preserving.
- Verify with the narrowest meaningful command.

Specifically:

- Update dependency declarations and let the package manager update lockfiles.
- Fix the breaking changes identified in the plan.
- Run test/lint commands after each change.

### Step 6 - Fix Failures

- If you cannot resolve a failure, apply a researcher lens to research the failure:
  - Prefer official documentation over blog posts; cite sources with URLs.
  - Separate confirmed facts from plausible interpretations.
  - Lead with the single most actionable recommendation.
  - Extract the exact symptom, likely root causes, and minimal verification steps.
- Use these to find the root cause and a minimal fix; apply the fix with the same worker lens as Step 5; re-run verification to confirm.

### Step 7 - Report

Provide a final summary detailing:

1. **Upgrading** — target dependencies.
2. **Current Versions** — versions before the upgrade.
3. **Target Versions** — upgraded versions.
4. **Breaking Changes** — key changes identified with sources.
5. **Migration Plan** — steps planned and executed.
6. **Updates Applied** — files changed and commands executed.
7. **Verification Results** — test, build, and lint outcomes.
8. **Failures Fixed** — troubleshooting and resolution details.
9. **Remaining Issues** — tasks requiring manual attention.

## Stop Condition

If a fix fails twice, stop and ask for guidance.
