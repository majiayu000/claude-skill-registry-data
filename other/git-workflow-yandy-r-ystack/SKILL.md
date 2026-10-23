---
name: git-workflow
description: 'Orchestrates commits, documentation updates, pushes, and PRs. Use when finishing a feature with docs, coordinating multiple commits, or shipping changes through a full Git workflow.'
argument-hint: '[--commit] [--push] [--pr] [--dry-run] [--no-docs] [--draft] [--base <branch>] [--ci] [--ci-max-pushes=N] [--ci-max-same-failure=N] [--ci-timeout-min=N] [--ci-yes]'
---

# Git Workflow Manager

Analyzes changes, writes Conventional Commit messages, coordinates documentation updates (parallel agents when the change is large), and optionally pushes, opens a PR, and monitors CI.

## Current Task

**Managing git workflow for**: `$ARGUMENTS`

## Hard Rules (survive compaction)

- Push and PR are never implicit. Push only when `push ∈ actions`; create a PR only when `pr ∈ actions`; the action set comes from explicit flags or the Phase 0.5 menu reply.
- Every commit must be a Conventional Commit: `<type>(<scope>): <subject>`. Types: `feat fix docs style refactor test chore perf ci build revert`. Subject imperative, lowercase start, no trailing period, ≤50 chars (≤72 max); scope lowercase alphanumeric with hyphens; breaking change via `!` and/or `BREAKING CHANGE:` footer; body wrapped at 72. Enforced by `scripts/validate-commit.sh`.
- Validate before committing (direct commits), after agents finish (agent commits; amend non-conformant ones), and for PR titles. Do not leave Phase 3b until all agent commits pass.
- Read `templates/commit-types.md` before writing any commit message.
- NEVER `git push --force`, NEVER `--no-verify`, anywhere including the CI loop. CI-loop pushes go only to the PR head branch; refuse if head equals the default branch.
- Stage and commit in a single operation. Agents never push; this skill pushes.
- `--dry-run` makes no changes: STOP after the Phase 1 dry-run report.
- Lack of MCP tools never blocks the workflow; on any MCP failure fall back to `gh`.
- Never update the root `CLAUDE.md`.

## Arguments

At least one action flag is required in normal use; with none, resolve interactively in Phase 0.5. Bare `--ci` is valid on its own (monitor CI on the existing PR for this branch). Flag order does not matter.

**Action flags** (cumulative ladder `--commit` < `--push` < `--pr`; each implies the lower ones):

- **--commit**: commit only
- **--push**: commit and push
- **--pr**: commit, push, create PR

**Modifier flags** (do not satisfy the action requirement):

- **--dry-run**: show analysis and plan, change nothing
- **--no-docs**: skip documentation updates
- **--draft**: create PR as draft (requires `--pr`)
- **--base <branch>**: PR base branch (requires `--pr`); overrides the base from `RELEASING.md` or the forge default (Step 22b)
- **--ci**: monitor CI on the current branch's PR and auto-fix until green or a bail. Works with `--pr` (create-then-monitor), `--push` (push-then-monitor), or bare (monitor only: no commit, no push). An open PR for the branch must exist when Phase 6 starts. Incompatible with `--dry-run` and with `--commit`-only.
- **--ci-max-pushes=N** (default 5), **--ci-max-same-failure=N** (default 3), **--ci-timeout-min=N** (default 30, from first iteration), **--ci-yes** (skip the one-time auth prompt)

**Questions:** class `clarify` (Phase 0.5 action menu): headless (no question tool or chat turn), print the menu and stop; pass `--commit`, `--push` or `--pr`. Class `confirm-publish` (Step 22a "run --ci against the existing PR?", Phase 6 CI authorization): headless and without `--ci-yes`, skip CI monitoring and print `rerun with --ci-yes`. Class `confirm-publish` (backport-label question): headless, add no label and print the `/ycc:backport` hint. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

## Tool Preference (before Phase 0)

If tools matching `mcp__github__*` exist, use MCP for GitHub operations (PR create/view/list); otherwise use `gh` via Bash. `git` operations, the skill scripts, and file reading always use Bash and the Read/Grep/Glob tools regardless.

## Phase Checklist

- [ ] Phase 0 Analyze (Steps 1–3): `git status`/diff, `scripts/analyze-changes.sh`, group changes.
- [ ] Phase 0.5 Resolve action set (Step 3.5): below.
- [ ] Phase 1 Strategy (Steps 4–5): small (1–3 files, single feature) → direct; large (4+ files, multiple features, breaking/API changes) → agents; `--dry-run` report then STOP.
- [ ] Phase 2 Documentation decision (Steps 6–7): skip if `--no-docs`, internal refactor, test-only, docs-only, or trivial.
- [ ] Phase 3a Direct commit (Steps 8–12) or Phase 3b Agent deployment (Steps 13–18), gated on `commit ∈ actions`.
- [ ] Phase 4 Summary and push (Steps 19–21), push gated on `push ∈ actions`.
- [ ] Phase 5 PR (Steps 22–31), gated on `pr ∈ actions`.
- [ ] Phase 6 CI monitoring (Steps 32–37), gated on `--ci`.

## Phase 0.5: Resolve Action Set (Step 3.5)

Every later phase keys off the action set.

1. Start `actions` from explicit flags (`commit`, `push`, `pr`).
2. Apply implications: `pr` adds `push` and `commit`; `push` adds `commit`.
3. If empty:
   - `--ci ∈ flags`: leave empty, skip the menu (bare `--ci`: only Phase 6 runs; Phases 3, 4, 5 skip).
   - Otherwise show this menu and wait; reject other replies and re-prompt. Map `1 → {commit}`, `2 → {commit, push}`, `3 → {commit, push, pr}`:

     ```
     No action flag provided. What do you want to do?

       1) Commit only
       2) Commit and push
       3) Commit, push, and create PR

     Reply with 1, 2, or 3 (or pass --commit / --push / --pr next time).
     ```

4. Validate:
   - `--draft` without `pr`: stop with "`--draft` requires `--pr`. Re-run with `--pr --draft`, or omit `--draft`."
   - `--base <branch>` without `pr`: stop with "`--base` requires `--pr`."
   - `--ci` with `actions == {commit}`: hard-stop with `--ci requires --push or --pr (CI runs on the remote, so local-only commits can't be monitored). Pass --ci alone to skip commits and monitor an existing PR.`
   - `--ci` with `--dry-run`: hard-stop with `--ci is incompatible with --dry-run; the loop performs real pushes.`
5. Record the set. `--dry-run` and `--no-docs` apply regardless of the set.

## Phases 0–4 (commit flow)

Read `references/commit-phases.md` before Phase 0 for exact commands, the dry-run report template, the documentation rules, the commit-message steps, the `docs-git-committer` agent prompt, agent-result validation (including the `git rebase -x` check), and the summary template. Key decisions:

- Strategy: direct commit vs parallel agents (single message, multiple Agent calls, one `docs-git-committer` per scope; todos per agent).
- Read `templates/documentation-decision.md` (Step 6), `templates/commit-types.md` (Step 8), `templates/agent-prompts.md` (Step 14) when the step is reached.
- Documentation: feature docs only for new user-facing features, significant API changes, complex flows, breaking changes; directory-level `CLAUDE.md` only for critical directory-specific patterns.
- Step 12/21: `git push` only when `push ∈ actions`.

## Phase 5: Pull Request (Steps 22–31)

Only when `pr ∈ actions`. Read `references/pr-creation.md` before Step 22. Decision points:

- Step 22a: existing PR → with `--ci`, ask whether to skip creation and run Phase 6 against it (`no` exits cleanly, no Phase 6); without `--ci`, stop with the "PR already exists" message.
- Step 22b: resolve `$BASE`, run the sync-check guard (exit 3: no PR, stop), offer backport, per `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/pr-base-and-backport.md`. Exit 2 (malformed `RELEASING.md`) stops with the parse error and `/ycc:release-model --audit`.
- Step 23: read `templates/pr-template.md`.
- Step 25: PR title must be Conventional Commit format and pass `validate-commit.sh`.
- Step 28: MCP `mcp__github__create_pull_request` first, `gh pr create` fallback; forge routing via `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/forge-detection.md` (`tea` for forgejo/gitea).
- Step 27: draft when work is incomplete or feedback is wanted; honor `--draft`.

## Phase 6: CI Monitoring (Steps 32–37)

Only when `--ci ∈ flags`. Read `references/ci-monitoring-phase.md` before Step 32, and `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/ci-monitoring.md` (authoritative policy: classification, termination, audit log, loop protocol) at Step 33. GitHub-only: `RESULT=unsupported-provider` is reported and skipped without error. No PR number: hard-stop. Authorization prompt unless `--ci-yes`. Branch on `RESULT=`: `green` → report; `handoff` → fix, validate, commit, push head branch, loop; `rerun-pending` → `sleep 30`, loop, no fix; `bail-*` → diagnosis, end; `pr-not-found` / `refused-default-branch` → surface, no retry. Print the Goal Signals block verbatim as the last lines of the run (`PR_IN_SCOPE`, `PR_URL_PRINTED`, `CI_GREEN`, `CI_BAIL_VISIBLE`); criteria are in that reference.

## /goal Pairing

Pair `/goal` only in `--ci` mode. Read `references/goal-pairing.md` for keep-looping/done/stop semantics and the condition template, and `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/goal-pairing.md` before relying on a `/goal` loop.

## Quality, Examples, Troubleshooting

Read `references/examples-and-troubleshooting.md` for the commit/docs/agent/PR/overall checklists, eight worked examples, and failure fixes (validation failures, MCP fallback, `gh` install/auth, no upstream, existing PR, draft-to-ready). Key reminders: small changes direct, large changes agents; atomic commits; draft PRs for WIP; PR creation needs MCP or authenticated `gh`.

## Reference Map

- `references/commit-phases.md` — read before Phase 0.
- `references/pr-creation.md` — read before Step 22.
- `references/ci-monitoring-phase.md` — read before Step 32.
- `references/goal-pairing.md` — read when pairing with `/goal`.
- `references/examples-and-troubleshooting.md` — read for checklists, examples, or when a step fails.
- `templates/commit-types.md`, `templates/documentation-decision.md`, `templates/agent-prompts.md`, `templates/pr-template.md` — read at Steps 8, 6, 14, 23.
- `scripts/analyze-changes.sh` (Step 2), `scripts/validate-commit.sh` (Steps 10, 18, 25, 36), `scripts/create-pr.sh` (Step 24; `--analyze --base "$BASE"`; defensive existing-PR check).
- Shared: `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/{forge-detection,pr-base-and-backport,ci-monitoring,goal-pairing}.md`, `${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/{pr-guard,ci-monitor}.sh`. `branch-prep.md` does not apply: this skill never creates branches.
