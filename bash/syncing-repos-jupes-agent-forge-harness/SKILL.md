---
name: syncing-repos
description: Multi-repo git operations — init, reset, status, branch management, refresh (rebase), stacked rebase. JSON output for agent consumption.
---

# syncing-repos

Manages multiple sub-repos registered in **local** `repos/repos.json` (gitignored; bootstrap from `repos/repos.json.example`). All operations emit JSON so agents can parse results.

## When to Use

- Cloning repos for the first time (`init`)
- Pulling latest changes across all repos (`refresh`)
- Creating feature branches across repos for an epic (`branch create`)
- Cleaning up merged branches (`branch cleanup`)
- Checking sync status of all repos (`status`)
- Rebasing stacked branches

## CLI Usage

```bash
bun run repo <command> [options]
```

All commands accept `--repo <name>` to target a single repo, or operate on all repos by default.

## Commands

### init
Clone or pull all repos in repos.json.
```bash
bun run repo init              # Non-interactive, JSON output
bun run repo init --human      # Human-readable output with progress
```

### status
Show sync status of all repos.
```bash
bun run repo status
# → { "repos": [{ "name": "my-api", "branch": "main", "ahead": 0, "behind": 2, "dirty": false }] }
```

### refresh
Pull and rebase all repos on their default branch.
```bash
bun run repo refresh
bun run repo refresh --repo my-api
```

### reset
Hard reset a repo to its remote HEAD. Discards all local changes.
```bash
bun run repo reset --repo my-api    # DESTRUCTIVE — confirm before use
```

### branch create
Create a feature branch in one or all repos.
```bash
bun run repo branch create feat/T-42-my-feature
bun run repo branch create feat/T-42-my-feature --repo my-api
```

### branch cleanup
Delete merged branches from one or all repos.
```bash
bun run repo branch cleanup
bun run repo branch cleanup --repo my-api --dry-run
```

### stacked-rebase
Rebase a stack of branches sequentially.
```bash
bun run repo stacked-rebase feat/base feat/feature-a feat/feature-b
```

## Output Format

All commands return:
```json
{
  "ok": true,
  "command": "init",
  "repos": [
    {
      "name": "my-api",
      "ok": true,
      "action": "cloned",
      "path": "repos/my-api",
      "branch": "main"
    }
  ],
  "errors": []
}
```

On failure:
```json
{
  "ok": false,
  "command": "refresh",
  "repos": [...],
  "errors": [{ "repo": "my-api", "message": "merge conflict in src/index.ts" }]
}
```

## repos.json Schema

```json
{
  "repos": [
    {
      "name": "my-api",
      "url": "https://github.com/org/my-api.git",
      "defaultBranch": "main"
    }
  ]
}
```
