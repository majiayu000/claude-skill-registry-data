---
name: pr
description: Create or update a GitHub pull request following Medox conventions (author spicode-bot, reviewer spideystreet). Invoke manually with /pr — do NOT trigger automatically.
disable-model-invocation: true
---

# Skill: Pull Request

Create or update a GitHub PR following the conventions defined in `.claude/rules/git.md`.

## Steps

1. **Pre-flight: docs sync** — run `/docs-up` first to ensure docs are up to date with code changes
2. `git log main..HEAD --oneline` — review commits included
3. Push if needed: `git push -u origin <branch>`
4. **Check if a PR already exists** for the current branch:
   - Use `mcp__github__list_pull_requests` with `head: "spideystreet:<branch>"` and `state: "open"`
   - If a PR exists → **update** it (step 5b)
   - If no PR exists → **create** it (step 5a)

### 5a. Create PR

- Use `mcp__github__create_pull_request`:
  - `title`: `<type>(<scope>): <summary>`
  - `head`: current branch
  - `base`: `main`
  - `body`: see Body format below
- Add reviewer: `gh pr edit <number> --add-reviewer spideystreet`

### 5b. Update PR

- Use `gh pr edit <number>` to update `--title` and/or `--body` if commits changed the scope
- Push new commits (already done in step 3)
- Report the existing PR URL to the user

## Body format

```
## Summary

- <bullet points from commits>

## Test plan

- [ ] `uv run pytest <tests> -v`
- [ ] Manual: <scenario>

🤖 Generated with [Claude Code](https://claude.ai/claude-code)
```

## Rules

- **Always prefer GitHub MCP tools** (`mcp__github__*`) over `gh` CLI for GitHub operations (create PR, list issues, add comments, etc.)
- Use `git` CLI only for local operations (log, push, diff, status)
- Use `gh pr edit` for updating title/body (no MCP equivalent)
