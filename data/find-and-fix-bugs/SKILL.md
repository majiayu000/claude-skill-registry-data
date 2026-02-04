---
name: find-and-fix-bugs
description: Find, triage, and fix bugs with or without user input. Autonomously scan codebases, produce an issues list, implement a fix, create a fix branch, commit via semantic-commit, and open a PR with gh.
---

# Find and Fix Bugs

## Contract

Prereqs:

- Run inside the target git repo.
- `rg` available on `PATH` for codebase scanning.
- `git` and `gh` available on `PATH`, and `gh auth status` succeeds.
- `$AGENT_KIT_HOME/scripts/kit-tools.sh` available for helper commands (recommended).

Inputs:

- Optional bug report (repro steps, expected vs actual, environment); otherwise autonomous discovery.

Outputs:

- An issues list (per `references/ISSUES_TEMPLATE.md`), a fix branch, commits, and a GitHub PR.

Exit codes:

- N/A (multi-command workflow; failures surfaced from underlying commands)

Failure modes:

- Cannot reproduce or insufficient input to confirm impact (record as uncertainty rather than guessing).
- High-risk changes (auth/billing/migrations) should halt or be skipped per guardrails.
- Missing tooling (`rg`/`git`/`gh`) or insufficient repo permissions.

## Setup

- Load commands with `source $AGENT_KIT_HOME/scripts/kit-tools.sh`

## Trigger

Use this skill when the user asks to find or fix bugs, or when no concrete issue is provided and you are asked to proactively discover issues.

## Intake rules

- If the user provides a bug report: ensure reproduction steps, expected vs actual, and environment. Ask only for missing details.
- If the user provides no input: do not ask; proceed autonomously.

## Discovery

- Scope scanning to tracked files only (ignore untracked files).
- Use `rg` to scan for bug-prone patterns (TODO, FIXME, BUG, HACK, XXX, panic, unwrap, throw, catch, console.error, assert).
- Exclude generated, vendor, or codegen directories when present (node_modules, dist, build, vendor, .git, gen, generated, codegen).
- Keep scan rules general; do not add repo-specific patterns.
- Do not rely on grep results alone; use LLM analysis to confirm plausibility and impact.
- Produce an issues list using `references/ISSUES_TEMPLATE.md`.
- Use the ID format `PR-<number>-BUG-###` (example: `PR-128-BUG-001`). If the PR number is not known yet, use `PR-<number>` as a placeholder and update after PR creation.
- For project-specific skills, consider adding a minimal repro script requirement; see `references/REPRO_GUIDE.md`.

## Context window management

- Prioritize scanning changed files and adjacent code before wider searches.
- If `rg` results are large, process in batches (for example: 20-50 hits per batch).
- Stop after enough high-confidence issues are identified to proceed with a fix.

## Selection

- If user input exists, fix that issue.
- If autonomous, fix the single most severe or highest-confidence issue.
- Only fix multiple issues when they share the same root cause and the diff remains small.
- Severity levels are fixed: critical, high, medium, low.

## Severity rubric

- critical: security exploit, auth bypass, data loss/corruption, or production outage
- high: frequent crash, major feature broken, or incorrect core outputs
- medium: incorrect behavior with workaround, edge cases, or performance regression
- low: minor bug, UX issue, or noisy logs without functional impact

## Confidence rubric

- high: clear reproduction or strong evidence, root cause identified, fix is validated
- medium: likely issue with partial evidence, root cause inferred, fix is plausible
- low: speculative issue, weak evidence, or no repro path

## High-risk guardrails

- Do not auto-fix changes involving auth, permission/authorization, payment/billing, migration, or infrastructure/deployment.
- If autonomous and the top issue is high-risk, record it and move to the next eligible issue. If all issues are high-risk, stop after reporting.

## Fix workflow

1. Create a new branch: `fix/<severity>-<slug>` using the fixed severity levels.
2. Implement the fix with minimal scope; avoid refactors.
3. Add or update tests when possible; run lint/test/build commands when present (see Validation commands). If validation fails, follow Retry policy.
4. Update the issues list with status.

## Validation commands

- package.json scripts: `lint`, `test`, `build` (npm, pnpm, yarn, or bun)
- Makefile targets: `lint`, `test`, `build`
- Justfile targets: `lint`, `test`, `build`
- Taskfile targets: `lint`, `test`, `build`
- Language defaults when applicable: `go test ./...`, `pytest`, `cargo test`, `mvn test`, `gradle test`, `dotnet test`

## Retry policy

- If validation fails, fix based on error output and retry up to 2 times.
- After 2 failed attempts, stop and report the failure with the last error output.

## Commit

- Use the `semantic-commit` skill to generate a Semantic Commit message.
- Prefer a single commit unless there is a clear reason to split.

## PR

- Use `gh pr create` and write the body using `references/PR_TEMPLATE.md`.
- Set the PR title to the primary issue or a short summary of the fix. Do not reuse the commit subject. Capitalize the first word.
- Replace the first H1 line in `references/PR_TEMPLATE.md` with the same PR title.
- The PR must include:
  - Issues found (including those not fixed)
  - Fix approach
  - Testing results or "not run"
- Include the issues list in the PR body.
- Use `scripts/render_issues_pr.sh --pr` (or `--issues`) to generate templates quickly.

## Output and clarification rules

- Use `references/OUTPUT_TEMPLATE.md` as the response format.
- The response must include, in order:
  1. Issues list
  2. `git-scope` output
  3. Tests run (commands and results)
  4. PR link
