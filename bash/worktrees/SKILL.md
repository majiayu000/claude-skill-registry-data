---
name: worktrees
description: Git worktree patterns for isolated parallel development. Use when creating feature branches, managing git worktrees, isolating feature work, parallel development, setting up a worktree, listing worktrees, worktree naming conventions, or cleaning up worktrees.
user-invocable: false
---

## Structure
```
project-root/          # Main worktree — stays on main, read-only for implementation
├── .worktrees/        # All feature worktrees (gitignored)
│   ├── 12345-feature-a/
│   └── 12346-feature-b/
```

## Rules
- **Never modify code in main worktree** — use it for reading/searching/comparing
- **One worktree per feature** (enables isolated or parallel agent sessions)
- **Naming**: `.worktrees/<ticket-id>-<short-description>`

## Commands
```bash
# Create worktree for a feature — use git -C from the repo root, no cd compound
git -C <repo-root> worktree add .worktrees/<id>-<desc> -b feature/<id>-<desc> main

# List worktrees
git -C <repo-root> worktree list
```

To inspect the new worktree, use the client's working-directory option or separate
`git -C`/inspection calls. Never combine `cd <repo>` with a redirection or write in
one shell call; see `shell-rules` for client-specific approval behavior.

## .gitignore
Ensure `.worktrees/` is in `.gitignore`.
