---
name: worktree
description: "[Utilities] Create isolated git worktree for parallel development"
argument-hint: [feature-description] OR [project] [feature] (monorepo)
infer: true
---

Create an isolated git worktree for parallel feature development.

## Summary

**Goal:** Create isolated git worktrees with auto-detected branch prefixes for parallel feature development.

| Step | Action | Key Notes |
|------|--------|-----------|
| 1 | Get repo info | `worktree.cjs info` -- detect monorepo/standalone, env files, dirty state |
| 2 | Gather info | Auto-detect branch prefix from keywords (fix/feat/refactor/docs/test/chore/perf) |
| 3 | Convert to slug | Description to kebab-case, max 50 chars |
| 4 | Execute create | `worktree.cjs create` with prefix, env files, project (monorepo) |

**Key Principles:**
- For monorepo: ask which project if not specified via AskUserQuestion
- Always ask which env files to copy to the worktree
- Use `worktree.cjs remove` to clean up worktrees and branches

## Workflow

### Step 1: Get Repository Info

```bash
node .claude/scripts/worktree.cjs info --json
```

**Response fields:**
- `repoType`: "monorepo" or "standalone"
- `baseBranch`: detected base branch
- `projects`: array of {name, path} for monorepo
- `envFiles`: array of .env* files found
- `dirtyState`: boolean

### Step 2: Gather Info via AskUserQuestion

**Detect branch prefix from user's description:**
- Keywords "fix", "bug", "error", "issue" → prefix = `fix`
- Keywords "refactor", "restructure", "rewrite" → prefix = `refactor`
- Keywords "docs", "documentation", "readme" → prefix = `docs`
- Keywords "test", "spec", "coverage" → prefix = `test`
- Keywords "chore", "cleanup", "deps" → prefix = `chore`
- Keywords "perf", "performance", "optimize" → prefix = `perf`
- Everything else → prefix = `feat`

**For MONOREPO:** Use AskUserQuestion if project not specified:
```javascript
// If user said "/worktree add auth" but multiple projects exist
AskUserQuestion({
  questions: [{
    header: "Project",
    question: "Which project should the worktree be created for?",
    options: projects.map(p => ({ label: p.name, description: p.path })),
    multiSelect: false
  }]
})
```

**For env files:** Always ask which to copy:
```javascript
AskUserQuestion({
  questions: [{
    header: "Env files",
    question: "Which environment files should be copied to the worktree?",
    options: envFiles.map(f => ({ label: f, description: "Copy to worktree" })),
    multiSelect: true
  }]
})
```

### Step 3: Convert Description to Slug

- "add authentication system" → `add-auth`
- "fix login bug" → `login-bug`
- Remove filler words, kebab-case, max 50 chars

### Step 4: Execute Command

**Monorepo:**
```bash
node .claude/scripts/worktree.cjs create "<PROJECT>" "<SLUG>" --prefix <TYPE> --env "<FILES>"
```

**Standalone:**
```bash
node .claude/scripts/worktree.cjs create "<SLUG>" --prefix <TYPE> --env "<FILES>"
```

**Options:**
- `--prefix` - Branch type: feat|fix|refactor|docs|test|chore|perf
- `--env` - Comma-separated .env files to copy
- `--json` - Output JSON for parsing
- `--dry-run` - Preview without executing

## Commands

| Command  | Usage                        | Description                |
| -------- | ---------------------------- | -------------------------- |
| `create` | `create [project] <feature>` | Create new worktree        |
| `remove` | `remove <name-or-path>`      | Remove worktree and branch |
| `info`   | `info`                       | Get repo info              |
| `list`   | `list`                       | List existing worktrees    |

## Error Codes

| Code                       | Meaning                              | Action                    |
| -------------------------- | ------------------------------------ | ------------------------- |
| `MISSING_ARGS`             | Missing project/feature for monorepo | Ask for both              |
| `MISSING_FEATURE`          | No feature name (standalone)         | Ask for feature           |
| `PROJECT_NOT_FOUND`        | Project not in .gitmodules           | Show available projects   |
| `MULTIPLE_PROJECTS_MATCH`  | Ambiguous project name               | Use AskUserQuestion       |
| `MULTIPLE_WORKTREES_MATCH` | Ambiguous worktree for remove        | Use AskUserQuestion       |
| `BRANCH_CHECKED_OUT`       | Branch in use elsewhere              | Suggest different name    |
| `WORKTREE_EXISTS`          | Path already exists                  | Suggest use or remove     |
| `WORKTREE_CREATE_FAILED`   | Git command failed                   | Show git error            |
| `WORKTREE_REMOVE_FAILED`   | Cannot remove worktree               | Check uncommitted changes |

## Example Session

```
User: /worktree fix the login validation bug

Claude: [Runs: node .claude/scripts/worktree.cjs info --json]
        [Detects: standalone repo, envFiles: [".env.example"]]
        [Detects prefix from "fix" keyword: fix]
        [Converts slug: "login-validation-bug"]

Claude: [Uses AskUserQuestion for env files]
        "Which environment files should be copied?"
        Options: .env.example

User: .env.example

Claude: [Runs: node .claude/scripts/worktree.cjs create "login-validation-bug" --prefix fix --env ".env.example"]

Output: Worktree created at ../worktrees/myrepo-login-validation-bug
        Branch: fix/login-validation-bug
```

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
