---
name: create-pr
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(git checkout:*), Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*), Bash(git rev-parse:*), Bash(git push:*), Bash(git commit:*), Bash(git worktree:*), Bash(gh pr create:*), Bash(gh pr list:*), Bash(gh repo view:*), Bash(gh label list:*)
description: >
  Create branch, atomic commits, push, and open a pull request with terse, exact messages.
  Conventional branch + commit format. PR title ≤70 chars, body says "why", not "what".
  Use when the user says "create pr", "create pullrequest", "create pull request", "make pr",
  "open pr", "open pullrequest", "open pull request", "submit pr", "raise pr", "/create-pr",
  or asks to ship/send changes as a pull request (PR/pullrequest/pull-request, any spelling).
---

## Context

- Current git status: !`git status --short`
- Diff summary vs HEAD (file + line counts): !`git diff HEAD --stat`
- Current branch: !`git branch --show-current`
- Default branch: !`gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name' 2>/dev/null || echo "main"`
- Recent commits on this branch: !`git log --oneline -10`

The full diff is intentionally NOT loaded above. To write the PR body, read only what you need:
- Per-file hunks: `git diff <base>...HEAD -- <file>` (replace `<base>` with the default branch)
- Branch-wide stat: `git diff <base>...HEAD --stat`
Do not run unfiltered `git diff` — it floods context for nothing.

## Your task

Create a branch (if needed), commit changes as atomic commits, push, and open a pull request. Terse and exact at every layer: branch name, commit messages, PR title, PR body.

### Steps

1. **Detect base branch** — use the default branch from context above. Target the PR against this branch.

2. **Ensure a valid branch name** — `<type>/<short-description>` convention before pushing.
   - Valid types: `feat`, `fix`, `chore`, `refactor`, `docs`, `style`, `perf`, `test`, `build`, `ci`, `revert`
   - Pick a name based on the changes (e.g., `feat/add-user-export`, `fix/login-redirect`)
   - **If on the default branch**: create a new branch with `git checkout -b <type>/<short-description>`
   - **If on a non-conventional branch** (e.g., auto-generated worktree branches like `claude/...`, or any name not matching the convention): rename it in place with `git branch -m <type>/<short-description>`. This works inside worktrees too.
   - **If already on a conventional branch**: keep it.

3. **Analyze and stage changes** — read the code to understand what changed and why. Stage specific files by name. Do NOT use `git add -A` or `git add .`. NEVER stage secret files (`.env`, `*.key`, `*.pem`, credentials, tokens).

4. **Create atomic commits** — split into multiple commits when changes involve different concerns, types, or file patterns. Each commit must build and make sense on its own.

   **Subject line:**
   - `<type>(<scope>): <imperative summary>` — `<scope>` optional
   - Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, `build`, `ci`, `style`, `revert`
   - Imperative mood: "add", "fix", "remove" — not "added", "adds"
   - ≤50 chars when possible, hard cap 72
   - No trailing period
   - Match project convention for capitalization after the colon

   **Body (only if needed):**
   - Skip when the subject is self-explanatory
   - Add for: non-obvious *why*, breaking changes, migration notes, linked issues
   - Wrap at 72 chars, bullets `-` not `*`
   - Reference issues at end: `Closes #42`, `Refs #17`

   **Always include body for:** breaking changes, security fixes, data migrations, reverts.

   **Breaking changes:** mark subject with `!` and add a `BREAKING CHANGE:` footer.

   **What NEVER goes in:** "This commit does X", "I"/"we"/"now"/"currently", "As requested by...", AI attribution, emoji (unless project convention), filename restated when scope covers it.

   Use HEREDOC for commit messages.

5. **Push the branch** — use `git push -u origin <branch>`.

6. **Create the PR** using `gh pr create`:

   **Title:**
   - Same format as a commit subject: `<type>(<scope>): <imperative summary>`
   - Under 70 chars, no trailing period
   - If the branch has one commit, reuse its subject. If multiple, summarize the overall change.

   **Labels:**
   - Infer appropriate labels from the change type and content. Use `--label` flags (one per label).
   - Common labels: `bug`, `enhancement`, `documentation`, `refactor`, `dependencies`, `breaking-change`.
   - Only apply labels that exist in the repository. Run `gh label list` first to check. If none match, skip labeling.

   **Body — terse, why over what:**
   ```
   gh pr create --title "title" --label "label1" --body "$(cat <<'EOF'
   - why this change exists (not a diff restatement)
   - notable decisions or tradeoffs

   ## Test plan
   - [ ] concrete step a reviewer can run
   - [ ] edge case covered
   EOF
   )"
   ```

   **Body rules:**
   - **No `## Summary` heading** — open the body directly with why-bullets. The PR title already names the change; a heading would just repeat it.
   - **`## Test plan` is mandatory** — always include it with concrete, actionable steps a reviewer can run (commands, URLs, edge cases). Avoid vague items like "test it works".
   - Analyze ALL commits on the branch for the why-bullets, not just the latest
   - Why-bullets state the *why*, not a list of files touched
   - Bullets `-` not `*`
   - No AI attribution, no "Generated with Claude Code"
   - No emoji unless project convention requires
   - **Add other sections only when applicable** (skip otherwise):
     - `## Related issues` — when commits reference issues (`#123`, `fixes #456`), list `Closes #N`
     - `## Breaking changes` — for breaking changes, include migration notes
     - `## Screenshots` — for UI changes, include before/after images or a short clip

7. **Output the PR URL** after creation.

### Edge Cases

- No changes at all: say so and stop. Do not create an empty PR.
- Branch already has an open PR: surface the existing URL instead of creating a duplicate (`gh pr list --head <branch>`).
- Push fails due to diverged history: do NOT force push. Inform the user and stop.
