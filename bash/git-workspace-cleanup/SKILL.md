---
name: git-workspace-cleanup
description: Destructive Git cleanup workflow that keeps only the main worktree and local main branch, then updates main; not for routine status checks, partial cleanup, or implicit repository hygiene.
---

# Git Workspace Cleanup

Return a Git repository to a single clean main worktree: remove every non-main worktree, delete every local branch except `main`, and fast-forward `main` from its remote.

This is destructive. Never run it implicitly.

## Invocation

Use this skill only when the user explicitly invokes it as `$git-workspace-cleanup`.

## Required Flow

1. State that the workflow can delete local worktrees and branches.
2. Resolve the bundled script relative to this `SKILL.md`:

   ```text
   scripts/git_workspace_cleanup.py
   ```

3. Choose the Python 3 launcher available in the user's shell and call it `<python>` in the commands below:

   - POSIX shells commonly use `python3`.
   - Windows PowerShell or `cmd.exe` commonly use `py -3` or `python`.

4. Run the bundled script in dry-run mode from any path inside the repository. The dry run fetches the remote and verifies the preserved branch can fast-forward before reporting the destructive plan:

   ```bash
   <python> <skill-dir>/scripts/git_workspace_cleanup.py --repo . --dry-run
   ```

5. Show the user the main worktree path and the worktrees and branches that would be removed.
6. Ask for explicit approval before mutating the repository. Use the host's native user-input or approval UI when it is available; in Codex, use `request_user_input` when the current mode exposes it. Offer a destructive approval choice and a cancel choice. If no native choice UI is available, ask for a short typed approval phrase instead.
7. After approval, run:

   ```bash
   <python> <skill-dir>/scripts/git_workspace_cleanup.py --repo . --yes
   ```

8. Continue subsequent repository work from the printed main worktree path.
9. Verify the final state with:

   ```bash
   git worktree list
   git branch --format="%(refname:short)"
   git status --short --branch
   git pull --ff-only
   ```

Use `--repo <path>` when the current shell is not inside the target repository.

## Safety Rules

- Do not remove the worktree checked out on `main`.
- Do not delete the local `main` branch.
- Do not mutate anything unless the user approves the dry-run result.
- Stop if the main worktree is dirty.
- Stop if an extra worktree is dirty. Use `--force-worktrees` only when the user explicitly approves discarding files in those dirty extra worktrees. Prefer the host's native user-input or approval UI for this approval when available; otherwise require a typed approval phrase.
- Treat fast-forward failure as a blocker before removing worktrees or deleting branches. Do not merge, rebase, reset, or force-push as part of this skill.
- If the repository uses a preserved branch other than `main`, rerun the script with `--main-branch <branch>` only after the user confirms that branch name.

## Script Behavior

The bundled script:

- locates the worktree checked out on the preserved branch, defaulting to `main`
- runs `git fetch --prune <remote>`, defaulting to `origin`
- verifies the preserved branch can fast-forward to `<remote>/<main-branch>`
- removes every other worktree
- deletes every other local branch with `git branch -D`
- runs `git pull --ff-only <remote> <main-branch>`, defaulting to `origin main`

The script requires Python 3.9 or newer and either `--dry-run` or `--yes`; it refuses to mutate by default.
