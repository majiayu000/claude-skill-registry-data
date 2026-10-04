---
name: speckit-git-worktree
description: Create a new git worktree under the project's ${PROJ}.worktrees collector
  directory
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: git:commands/speckit.git.worktree.md
---

# Create Worktree

Create a new Git worktree for an existing or new branch. By default, the command derives the collector directory from the primary checkout and places the worktree at:

`<parent-of-primary-checkout>/<project>.worktrees/<branch>`

This matches the same convention used by the feature workflow.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Behavior

1. Require a branch argument (`<branch>`).
2. Optionally accept a start-point (`<start-point>`) to create a new branch from.
3. Derive the target path using the shared collector convention unless overridden.
4. Create the collector directory when missing.
5. Create the worktree with `git worktree add`.
6. After successful creation, ask the user whether to move into the new worktree directory using the `AskUserQuestion` tool.
7. Print a short status summary including branch and path.

## Post-Creation Prompt

After parsing command output and obtaining `WORKTREE_PATH`, call the `AskUserQuestion` tool with a yes/no choice:

- `question`: `Worktree created at <WORKTREE_PATH>. Move into this directory now?`
- `options[]`:
	- `{label: "Yes", description: "I will move into the new worktree now"}`
	- `{label: "No", description: "Stay in the current directory"}`
- `multiSelect`: `false`

If the user selects **Yes**, output and execute the command:

```bash
cd <WORKTREE_PATH>
```

If the user selects **No**, continue without changing directories.

## Arguments

- `--path <absolute-path>`: Explicit worktree path override (same behavior as `SPECKIT_WORKTREE_PATH`).
- `--parent <absolute-path>`: Explicit collector directory override (same behavior as `SPECKIT_WORKTREE_PARENT`).
- `<branch>`: Required branch name.
- `<start-point>`: Optional revision/branch/tag used when creating a new branch.

## Execution

- **Bash**: `.specify/extensions/git/scripts/bash/worktree-add.sh [--path <absolute-path>] [--parent <absolute-path>] <branch> [<start-point>]`

## Graceful Degradation

- If Git is not available or the current directory is not a repository: warn and exit.
- If the target path already exists: refuse and explain how to override with `--path`.
- If branch creation/worktree add fails: print Git error output and exit non-zero.