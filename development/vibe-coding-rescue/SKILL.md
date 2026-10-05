---
name: vibe-coding-rescue
description: Use when an AI-built, Vibe Coding, or inherited software project cannot start, build, test, validate, run locally, pass CI, or match its README; also use when environment, dependency, API contract, database migration, test fixture, deployment, or fake-completion failures must be diagnosed before repair.
---

# Vibe Coding Rescue

Recover an AI-built or inherited project to a known-good engineering baseline. The job is not to make a confident guess; it is to reproduce the real failure, identify the first broken boundary, make the smallest justified repair, and prove the original failure no longer reproduces.

## Use This Instead Of

- Use `vibe-coding` for formal Spec-to-code delivery from an approved engineering-ready Spec.
- Use `internal-app-standards` for broad stack selection, architecture design, or internal-system production review.
- Use `dengbao-code-audit` for MLPS/等保 security audit.
- Use this skill first when the immediate problem is rescue: startup failure, red tests, broken README, CI failure, environment drift, contract mismatch, migration failure, or AI-generated fake completion.

## Required Start

1. Protect the worktree: run `git status --short --branch` and identify user changes before editing.
2. Read the README, manifests, lockfiles, env templates, and the user-reported failing command or area.
3. Run the read-only context collector when possible. Write its JSON outside the target repo, such as `/tmp` or a separate work directory, unless the user explicitly asks for an artifact in the repo:

   ```bash
   python3 <skill-dir>/scripts/collect_rescue_context.py <project-root> --output <workdir>/rescue-context.json
   ```

4. Read the CI/deploy files, migrations, tests, generated contracts, and code paths indicated by the collector and failure report.
5. Reproduce the reported failure with the exact command or the closest safe substitute. Record command, exit code, and key log lines before changing code.
6. If the command would mutate production, require credentials, or call an external system, stop and state the safe substitute or missing authorization.

## Reference Routing

- Read [references/failure-taxonomy.md](references/failure-taxonomy.md) when classifying install, startup, build, test, API, database, CI/deploy, README drift, or AI fake-completion failures.
- Read [references/rescue-workflow.md](references/rescue-workflow.md) before changing files or deciding the repair sequence.
- Read [references/output-contract.md](references/output-contract.md) before reporting a fix, partial fix, or blocker.

## Hard Rules

- Do not edit before baseline reproduction unless the baseline command is unsafe; then document why and use a dry-run, local-only, or synthetic substitute.
- Fix one proven failure chain at a time. Do not batch dependency upgrades, framework swaps, format churn, or broad refactors into a rescue.
- Separate environment/config, dependency, contract, code, test, data, documentation, and deployment causes. Do not label a test or script broken until upstream configuration and contract evidence has been checked.
- For behavior changes, use a failing test first when feasible. For config/docs/runbook fixes, prove them with the command they are supposed to repair.
- Never copy secrets, private URLs, tokens, cookies, database contents, `.env` values, or local browser state into reports, commits, fixtures, or logs.
- Do not claim "fixed", "green", "newcomer-ready", "CI-ready", or "deployable" without fresh command evidence.
- Do not claim "newcomer-ready" unless the README path was verified from a clean checkout/container or an equivalent isolated state with only documented setup inputs.
- When Git push is requested, prefer an isolated branch unless the user explicitly requested direct push and repository policy permits it. Never mix user changes into the rescue commit.
- If remote access, credentials, private packages, databases, external services, or production permissions are missing, report a blocker with the exact missing artifact and the last safe local evidence.

## Expected Output

Lead with the rescue verdict: `fixed`, `partially fixed`, or `blocked`.

Then provide:

- Scope and original failure command.
- Failure chain: symptom -> failing boundary -> root cause -> repair.
- Files changed and why.
- Verification commands actually run, with exit status and remaining failures.
- README/newcomer runbook status.
- Remaining risks, skipped unsafe checks, and required owner action.
- Git commit, branch, PR, or push status when delivery was requested.
