---
name: mc-pr
description: ALWAYS use this skill when creating, updating, or preparing pull requests. Verifies clean state, syncs with the default branch, requires fresh verification evidence (or runs the cheapest sufficient checks), and crafts a PR title/description following conventional commit style. Trigger on any create PR, open PR, update PR, edit PR, push and create PR, prepare for review, or PR-related task.
---

# MC PR

Create and update pull requests following conventional commit conventions.

**Requires**: `gh` CLI authenticated, working directory inside the repo whose PR is being managed.

Use the lowest-overhead safe path. Don't run full diffs/checks unless needed to understand or validate the PR.

## Process

### 1. Ensure Clean Working Tree

```bash
git status --porcelain
```

If dirty, use `mc-commit` first. Do not proceed with uncommitted changes.

### 2. Sync with the Default Branch

```bash
BRANCH=$(git branch --show-current)
DEFAULT=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
git fetch origin "${DEFAULT:-main}"
git merge "origin/${DEFAULT:-main}"
```

If the merge has conflicts, report the conflicting files and ask the user how to resolve. Do NOT force-resolve or drop changes.

### 3. Verification Evidence Gate

Before pushing or editing the PR, confirm there's fresh verification evidence after the latest source changes and after the merge from the default branch (if any). Evidence can come from current-session command output or CI — it must reference exact commands run, not a vague assertion.

If evidence is missing or stale, run whatever's cheap and actually applicable — e.g. a `package.json`'s `lint`/`typecheck`/`test` scripts if present and relevant files changed, `bash -n` for shell scripts, or the project's own documented verify command. Don't invent checks the project doesn't have, and don't re-run something that already passed against the current diff.

If a verification command modifies files (e.g. an auto-fixing linter), stop, inspect the diff, commit the fix with `mc-commit`, and restart the clean-tree check before proceeding.

### 4. Push to Remote

```bash
git push -u origin HEAD
```

### 5. Analyze the Changeset

Start compact, then inspect targeted diffs only where needed:

```bash
git log origin/${DEFAULT:-main}..HEAD --oneline
git diff origin/${DEFAULT:-main}...HEAD --stat
git diff origin/${DEFAULT:-main}...HEAD --name-status
```

Review all commits and affected paths to understand the overall narrative and whether this is a feature, fix, refactor, or mixed change. Use full diffs only for files needed to classify the PR or write an accurate test plan.

### 6. Create or Update PR

```bash
gh pr view --json number,title,body,url 2>/dev/null || echo "NO_EXISTING_PR"
```

#### New PR

```bash
cat > /tmp/mc-pr-body.md <<'EOF'
## Summary

<2-5 bullets — bold lead phrase, explain why not just what>

## Test plan

- [ ] <specific manual verification steps>
- [ ] <checks actually run or required before merge>
EOF

gh pr create --title "<type>(<scope>): <description>" --body-file /tmp/mc-pr-body.md
```

Title: conventional commit format, under 70 chars.

#### Update Existing PR

```bash
cat > /tmp/mc-pr-body.md <<'EOF'
<updated description>
EOF

gh pr edit <number> --title "<new title>" --body-file /tmp/mc-pr-body.md
```

Re-analyze the full changeset. Add new bullets for recent changes rather than rewriting. Preserve any manual edits.

#### Body generation safety

Always write the PR body to a temp Markdown file and pass it with `--body-file`. Avoid inline `--body "$(cat <<'EOF' ... EOF)"`: PR bodies often contain backticks, quotes, parentheses, `$`, and apostrophes, and inline shell heredocs are easy to break or interpolate accidentally.

Do **not** add tool/vendor-specific generated-by footers. The PR should stand on its own and not mention Claude, Pi, GPT, or any other agent runtime unless the user explicitly asks.

### 7. Verify

```bash
gh pr view --json number,title,url,state
```

Report the PR URL plus the exact verification evidence included in the PR test plan.

## Example

**Title**: `chore: pivot shell from fish to zsh/oh-my-zsh`

```markdown
## Summary

- **Retired fish entirely** — removed home/.config/fish/, fish/fisher from the Brewfile, and every fish-specific dot command
- **Ported the genuinely custom fish functions to zsh** — worktree suite, gbage/gtest/glp, general utilities — skipped anything oh-my-zsh's git plugin already covers
- **Fixed two things fish's removal would have silently broken** — git's fomo/lg aliases, and ghostty's shell-integration setting

## Test plan

- [ ] `dot apply` runs clean with no conflicts
- [ ] New shell functions load without error in an interactive zsh session
- [ ] `git fomo` and `git lg` work without fish installed
```

## Principles

- One PR per branch — each branch is a coherent unit of work
- Explain **why**, not just what — code shows what; the PR explains why
- All commits matter — summary reflects the entire branch, not just the tip
- Clean before PR — no uncommitted changes, synced with the default branch, and fresh verification evidence after the latest source change
