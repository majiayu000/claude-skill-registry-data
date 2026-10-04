---
name: pr-title
description: Set or update PR/MR titles as semantic commits for squash-merge workflows. Use when the user says "pr title", "mr title", "fix pr title", "rename pr", or "prepare pr".
---

# PR Title

Format: `<type>: <short description in lowercase>`

Types: `feat`, `fix`, `chore`, `refactor`, `perf`, `docs`, `test`, `ci`, `build`, `style`

No scope. No capital after colon.

## Steps

1. **Detect platform** - run in parallel:
   - `gh pr view --json number,title,url 2>/dev/null`
   - `glab mr view --output json 2>/dev/null`
   - Both fail → ask user to create one (and on which platform)
   - Both succeed → ask user which one

2. **Analyze** - infer type from branch name, commits, and diff. Branch hints:
   - `feature/*`, `feat/*` → `feat`
   - `fix/*`, `bugfix/*`, `hotfix/*` → `fix`
   - `refactor/*` → `refactor`
   - `chore/*`, `deps/*` → `chore`
   - Ambiguous → inspect commits/diff

3. **Propose** - present 2-3 title options via AskUserQuestion

4. **Apply**:
   - GitHub: `gh pr edit --title "…"` or `gh pr create --title "…" --body ""`
   - GitLab: `glab mr update --title "…"` or `glab mr create --title "…" --description ""`
