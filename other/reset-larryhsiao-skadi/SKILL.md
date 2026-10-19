---
name: git-reset
description: Use when the user asks to reset the workspace, discard all changes, or restore to HEAD. Resets staged, unstaged, and untracked files after confirmation.
purpose: Resets staged, unstaged, and untracked files back to HEAD after confirmation.
stage: desk
---

# Reset Workspace to HEAD

## Workflow

1. Run `git status` to show current workspace state
2. Summarize what will be lost (staged changes, unstaged changes, untracked files)
3. Ask for user confirmation with AskUserQuestion before proceeding
4. If approved — reset everything; if rejected — abort

## Asking for Confirmation

Use AskUserQuestion to confirm the destructive action:

```
question: "This will discard all local changes. Proceed?"
options:
  - label: "Reset everything"
    description: "Discard staged, unstaged, and untracked files"
  - label: "Keep untracked files"
    description: "Reset staged and unstaged changes but keep new files"
```

## After Approval

**Reset everything:**

```bash
git reset --hard HEAD
git clean -fd
```

**Keep untracked files:**

```bash
git reset --hard HEAD
```

## Important

- Never run without user confirmation — this is destructive and irreversible
- Always show `git status` output so the user knows what will be discarded
