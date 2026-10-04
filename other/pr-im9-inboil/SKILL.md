---
name: pr
description: Create a feature branch, commit changes, push, and open a PR to main.
allowed-tools: Bash(git *), Bash(gh *), Read, Edit, Write, AskUserQuestion
---

# PR

Create a feature branch from current changes, commit, push, and open a pull request.

## Usage

```
/pr
```

## Process

1. **Check state**: Run `git diff`, `git diff --cached`, `git status -u` to see all changes.
2. **Determine branch name**: Analyze changes and generate a branch name (`feat/xxx`, `fix/xxx`, `docs/xxx`, `refactor/xxx`, `chore/xxx`). If already on a feature branch (not `main`), skip branch creation.
3. **Create branch**: `git checkout -b {branch}` (from main).
4. **Stage & commit**: Same rules as `/commit` — analyze changes, draft message, stage specific files, commit with `Co-Authored-By`.
5. **Push**: `git push -u origin {branch}`
6. **Create PR**: `gh pr create` with title and body.
   - PR title: same as commit first line (under 70 chars)
   - PR body: summary bullets + test plan

## Commit Message Format

- First line: `type: short summary` (under 72 chars)
  - Types: `feat`, `fix`, `refactor`, `style`, `docs`, `chore`
- Blank line, then bullet-point details for non-trivial changes
- End with `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`
- Write in English (per CLAUDE.md conventions)
- Pass the message via HEREDOC for proper formatting

## PR Body Format

```markdown
## Summary
<1-3 bullet points>

## Test plan
<bulleted checklist>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Multiple commits on same branch

If already on a feature branch with an open PR:
- Stage & commit only (no new branch, no new PR)
- Push to update the existing PR

## Safety

- Never stage files that may contain secrets (.env, credentials, etc.)
- Never use `git add -A` — always add specific files
- Never force push
- Always create PR to main, never push directly to main
