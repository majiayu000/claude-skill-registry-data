---
name: atomic-commit-push
description: Git Operations sub-skill — safe git staging and push. Create small, reviewable git commits from local changes and push the current branch safely using a hybrid Conventional Commit subject plus Lore body. Use when the user asks to commit, split changes into atomic commits, push/publish a branch, or perform a careful commit-and-push workflow while preserving unrelated work and avoiding accidental secrets or broad staging. For advanced git operations (rebase, bisect, conflict resolution, reflog recovery, cherry-pick, worktree), see the parent skill **git-operations**.
---

# Atomic Commit Push

> **Git Operations sub-skill.** Handles basic commit and push workflows. Advanced git operations belong to the parent **`git-operations`** skill (`skills/git-operations/SKILL.md`).

## Goal

Turn local changes into one or more atomic commits, verify each commit as appropriate, and push the branch without staging unrelated work or leaking secrets.

## Safety rules

- Commit/push only within user authorization. Approval to continue an IssueOps cycle through
  draft PR/MR publication includes commits and pushes to that cycle's issue branch; do not
  request the same approval again. A request limited to local edits does not authorize publication.
- Read the repo's nearest `AGENTS.md`/`CLAUDE.md` and relevant project docs before committing. When `.issueops/TESTING.md` exists, it decides which checks a commit must pass; if it is an index whose module table hands a topic (for example the changed language's basic checks) to a module file, open that module too. Open the `.issueops/CAUTIONS.md` modules for secrets and commit identity when they exist.
- If `.issueops/COMMIT_POLICY.md` exists, use it as the commit-message source of truth.
- Never use `git add .` or `git commit -a`. Stage exact files, and use `git add -p` when a file mixes unrelated changes.
- Do not discard, stash, reformat, or rewrite user changes unless the user explicitly asks.
- Treat `.env`, private keys, credentials, local state, logs, and generated secrets as blockers until inspected or excluded.
- Never force-push unless explicitly requested; prefer `--force-with-lease` only after explaining the risk.
- Ask before pushing shared/protected branches such as `main`, `master`, `develop`, `release/*`, or a branch with unclear ownership.

## Workflow

1. **Pre-start gate / Preflight**
   - Run `python3 <skill>/scripts/git_preflight.py [repo]` if available.
   - Before planning commits, run `python3 <skill>/scripts/api_doc_gate.py [repo]` if available. This hook-style gate calls the agent-backed API documentation reviewer and exits non-zero on blocking Swagger/OpenAPI drift.
   - If that script is unavailable, run the equivalent API documentation gate when staged API candidate files exist: `issueops api-doc check --json` or MCP `api_doc_static_check` plus `api_doc_review`.
   - If the API documentation gate fails, stop at the gate and report the blocking Swagger/OpenAPI findings instead of continuing to stage/commit.
   - Also inspect `git status --short`, current branch, upstream, and recent commit style.
   - If the directory is not a git repo, stop and report.

2. **Understand scope**
   - Review unstaged, staged, and untracked changes with `git diff`, `git diff --cached`, and targeted file reads.
   - Decide what belongs to the requested work: the active cycle's issue, or exactly what the user asked to commit. Changes outside it stay unstaged even when they are small and worth keeping; list them in the report so the user can commit them separately.
   - Build an atomic commit plan within that scope: each commit should represent one intent and be revertible on its own. Splitting into atomic commits never pulls out-of-scope changes into a commit of their own.

3. **Verify before staging**
   - Run the smallest relevant tests/checks for the changed scope when practical, starting with the required checks in `.issueops/TESTING.md` when it exists.
   - If checks are expensive or unavailable, note the reason and use targeted inspection.

4. **Stage one atomic unit**
   - Stage exact paths: `git add -- path/to/file`.
   - For mixed files, stage hunks interactively: `git add -p path/to/file`.
   - Verify the staged patch with `git diff --cached --stat` and `git diff --cached`.
   - Ensure unrelated work remains unstaged with `git status --short`.

5. **Commit**
   - To save context and ensure compliance with this format, you can execute the `commit_suggest` MCP tool (or run `issueops project commit-suggest --staged`) to automatically generate the commit message from your staged diff. Review the suggested draft and refine it as needed before executing the final commit.
   - Match stronger repository-specific rules first, then use the hybrid format below.
   - Use a Conventional Commit subject: `<type>(<scope>)!?: <summary>`.
   - Add a `Lore:` body for AI-readable context:
     - `Intent`: one purpose for this atomic commit.
     - `Why`: the user/request/problem context.
     - `Changes`: concise bullets describing the staged diff.
     - `Verify`: record the commands run, or `Not-tested: <reason>`. When `.issueops/TESTING.md` exists, record which of its required checks ran.
     - `Risk`: rollout/compatibility/secret/generated-file risk, or `Low`.
   - Commit only after the staged diff matches the planned atomic unit.

6. **Repeat**
   - Repeat staging, verification, and commit for each remaining atomic unit.
   - If a hook modifies files, inspect the modifications and amend or create a follow-up commit only if they belong to the same intent.

7. **Push**
   - Re-check status and branch/upstream.
   - If upstream exists, use `git push`.
   - If no upstream exists and `origin` is appropriate, use `git push -u origin HEAD` unless branch policy requires confirmation.
   - Do not push if tests failed, secrets are suspected, or the branch target is risky without user confirmation.

## Hybrid commit message format

Use this default template unless the repository has a stricter local rule:

```text
<type>(<scope>)!?: <summary>

Lore:
- Intent: <one purpose for this atomic commit>
- Why: <context or reason>
- Changes:
  - <important staged change>
  - <important staged change>
- Verify: <command/result or Not-tested: reason>
- Risk: <Low or specific remaining risk>
```

Examples:

```text
docs(skill): define hybrid commit policy

Lore:
- Intent: Make commit history useful to both developers and AI agents.
- Why: Conventional subjects are concise, but agents need durable context.
- Changes:
  - Document the Conventional + Lore commit format.
  - Update atomic-commit-push to emit structured commit bodies.
- Verify: python3 scripts/validate-skill.py skills/atomic-commit-push
- Risk: Low; documentation-only policy change.
```

For very small typo/docs commits, keep the Lore body short but still include `Intent` and `Verify` when practical.

## Atomic grouping guidance

Prefer separate commits for:

- behavior changes vs tests
- source changes vs generated files
- docs-only changes vs code changes
- refactors vs feature/bug fixes
- dependency/lockfile updates vs application code

Keep together:

- a code change and its direct unit tests
- a generated artifact required by the changed source
- a config change and the docs/tests that explain that config

## Completion report

Report:

- commits created: short SHA + subject
- validation commands run and results
- push target and result
- any remaining unstaged/untracked files
- any skipped checks as `Not-tested: <reason>`
