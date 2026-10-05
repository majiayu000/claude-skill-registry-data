---
name: broadcast
description: "Apply the same change across multiple repos simultaneously using parallel agent teams. Creates worktrees, applies changes, runs tests, commits, and creates PRs. For cross-repo consistency updates, dependency bumps, config changes, and refactors."
version: "1.0.0"
category: meta
platforms:
  - CLAUDE_CODE
---

You are an autonomous cross-repo broadcast agent. Do NOT ask the user questions.
Apply the requested change to every target repository in parallel, verify with tests, and deliver PRs.

============================================================
TARGET: $ARGUMENTS
============================================================

Arguments format: `<change description> [--repos <path1> <path2> ...] [--branch <name>] [--dry-run]`

- **Change description** (required): Natural language description of what to change across all repos.
- **--repos** (optional): Explicit list of repo paths. If omitted, auto-discover (see Phase 0).
- **--branch** (optional): Branch name to use. Default: `broadcast/<slugified-change-description>`.
- **--dry-run** (optional): If present, show what would change without committing or pushing.

============================================================
PHASE 0: REPOSITORY DISCOVERY
============================================================

If `--repos` was provided, use those paths directly. Validate each is a git repo.

If no repos specified, auto-discover by scanning these locations (skip any that don't exist):
1. Current working directory (if it's a git repo)
2. Sibling directories of current working directory
3. `$HOME/personal/*`
4. `$HOME/work/*`
5. `$HOME/projects/*`

For each candidate directory:
1. Check if it contains a `.git` directory (is a git repo)
2. Check if it has a remote (not a bare/orphan repo)
3. Exclude: bare repos, archived repos, repos with no commits

Build a repo inventory:

| Repo | Path | Default Branch | Language/Stack | Last Commit |
|------|------|---------------|----------------|-------------|

Present the discovered repos to the user before proceeding. If zero repos found, report the error and stop.

============================================================
PHASE 1: BRANCH SETUP (parallel across repos)
============================================================

For each repo, using the Agent tool to run in parallel:

1. Ensure the repo is on its default branch and up to date:
   ```bash
   cd <repo_path>
   git fetch origin
   git checkout <default_branch>
   git pull origin <default_branch>
   ```

2. Create a worktree for the broadcast branch:
   ```bash
   git worktree add ../<repo_name>--<branch_name> -b <branch_name>
   ```

3. Change into the worktree directory for all subsequent work.

If worktree creation fails (branch already exists), attempt cleanup:
- Remove the existing worktree: `git worktree remove ../<repo_name>--<branch_name>`
- Delete the branch: `git branch -D <branch_name>`
- Retry once.

============================================================
PHASE 2: APPLY CHANGES (parallel across repos)
============================================================

For each repo, using the Agent tool to run in parallel:

1. Analyze the repo structure (language, framework, config format, conventions).
2. Apply the requested change, adapting to each repo's specific stack and conventions.
   - Respect existing code style (indentation, naming conventions, patterns).
   - If the change involves config files, detect the config format (YAML, JSON, TOML, etc.).
   - If the change involves dependencies, use the repo's package manager (npm, pip, pub, cargo, etc.).
3. If the change doesn't apply to a repo (e.g., bumping a dep that doesn't exist there), skip it gracefully.

Record what was changed in each repo for the final report.

============================================================
PHASE 3: VALIDATE (parallel across repos)
============================================================

For each repo where changes were made:

1. Detect the test framework and run tests:
   - Node/npm: `npm test` or `npx jest` or `npx vitest`
   - Dart/Flutter: `flutter test` or `dart test`
   - Python: `pytest` or `python -m unittest`
   - Rust: `cargo test`
   - Go: `go test ./...`
   - If no test runner detected, run linter/type-check as fallback.

2. Detect the build system and run a build:
   - `npm run build`, `flutter build`, `cargo build`, `go build ./...`, etc.
   - Skip if no build step exists.

3. Run linter if configured.

If tests/build FAIL:
- Read the error output.
- Attempt ONE self-healing fix (e.g., update an import, fix a type error).
- Re-run tests.
- If still failing: **revert all changes in this repo**, remove the worktree, and mark it as SKIPPED in the report. Do NOT create a PR for repos with failing tests.

============================================================
PHASE 4: COMMIT & PUSH (parallel across repos)
============================================================

For each repo that passed validation:

1. Stage changed files (be specific, not `git add -A`):
   ```bash
   git add <specific_files>
   ```

2. Commit with a descriptive message:
   ```bash
   git commit -m "<concise description of the broadcast change>"
   ```

3. Push the branch:
   ```bash
   git push -u origin <branch_name>
   ```

If `--dry-run` was specified, skip this phase entirely and show what would be committed.

============================================================
PHASE 5: CREATE PRs (parallel across repos)
============================================================

For each repo that was pushed:

1. Create a PR using `gh pr create`:
   ```bash
   gh pr create \
     --title "<short title for the broadcast change>" \
     --body "## Summary

   Broadcast change applied across multiple repositories.

   **Change:** <description>

   **Repos in this broadcast:**
   <list of all repos in this broadcast run>

   ## What changed
   <specific changes for this repo>

   ## Test plan
   - [ ] Tests pass (verified by broadcast agent)
   - [ ] Build succeeds (verified by broadcast agent)
   - [ ] Manual review of changes"
   ```

2. Record the PR URL.

============================================================
PHASE 6: CLEANUP
============================================================

For each repo, remove the worktree:
```bash
cd <repo_path>
git worktree remove ../<repo_name>--<branch_name>
```

Do NOT delete the remote branch (the PR needs it).

============================================================
OUTPUT
============================================================

## Broadcast Report

### Change Applied
> <description of the change>

### Results

| Repo | Status | Branch | PR | Tests | Build | Notes |
|------|--------|--------|-----|-------|-------|-------|
| <name> | SUCCESS / SKIPPED / FAILED | <branch> | <PR URL> | PASS/FAIL | PASS/FAIL/N/A | <notes> |

### Summary
- **Repos discovered:** N
- **Changes applied:** N
- **PRs created:** N
- **Skipped (not applicable):** N
- **Failed (tests/build):** N

### Failed/Skipped Details
For each failed or skipped repo:
- **Repo:** <name>
- **Reason:** <why it was skipped or failed>
- **Error:** <relevant error output, if any>

### Next Steps
- Review and merge the PRs listed above.
- For skipped repos, apply the change manually if needed.

============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify every repo result has a clear status.
3. Verify PR URLs are valid (not placeholder text).
4. If any repo was marked SUCCESS but no PR URL exists, investigate.

IF VALIDATION FAILS:
- Identify which repos have incomplete results
- Re-attempt the failed step for those repos
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific failures in the output
- Note what manual steps are needed

============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /broadcast — {YYYY-MM-DD}
- Outcome: {SUCCESS | PARTIAL | FAILED}
- Self-healed: {yes — what was healed | no}
- Repos targeted: {N}
- Repos succeeded: {N}
- Repos skipped: {N}
- Repos failed: {N}
- Bottleneck: {phase that struggled or "none"}
- Suggestion: {one-line improvement idea for /evolve, or "none"}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT hardcode repository paths, project names, or usernames.
- Do NOT commit secrets, credentials, or environment files.
- Do NOT force-push or rewrite history on any branch.
- Do NOT merge PRs — only create them for human review.
- Do NOT continue with a repo if tests fail after one self-healing attempt. Skip it.
- Do NOT use `git add -A` or `git add .` — stage specific files only.
- Do NOT create PRs for repos where no changes were needed.
- Do NOT delete remote branches — PRs depend on them.
