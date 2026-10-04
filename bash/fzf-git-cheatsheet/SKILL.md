---
name: fzf-git-cheatsheet
description: Lists the fzf-git.sh Ctrl-G shell pickers (worktrees, hashes, branches…) and in-picker keys. Use for fzf-git or C-g questions.
---

# fzf-git.sh cheatsheet

Source: `~/dotfiles/fzf-git.sh` (submodule), sourced from `.bash_tools`. `grab` moved to `M-g`.

Each picker inserts the selection at the cursor. Second key works with or without Ctrl.
On the Mac, macOS eats Ctrl-H (desktop switch): use `C-g h`; `C-g C-h` just inserts a literal `^G`.
`C-g ?` lists bindings. Pickers open as a tmux popup; `TAB` multi-selects; `C-/` cycles preview.

| Keys | Inserts | Source list |
|---|---|---|
| `C-g C-w` | worktree path | `git worktree list` |
| `C-g C-h` | short hash | `git log --graph` from the shell's current HEAD |
| `C-g C-b` | branch | local branches |
| `C-g C-f` | file path | `git status`, then `git ls-files` (slow in the monorepo) |
| `C-g C-e` | ref | `git for-each-ref` (no remotes) |
| `C-g C-l` | `HEAD@{n}` | reflog |
| `C-g C-s` | `stash@{n}` | stashes |
| `C-g C-t` | tag | tags, newest first |
| `C-g C-r` | remote | remotes |

## In-picker keys

| Key | Where | Does |
|---|---|---|
| `M-a` | branches, hashes, refs | widen: remote branches / `git log --all` / all refs |
| `M-h` | branches | hash picker on the highlighted branch |
| `M-Enter` | branches, refs | insert without the `origin/` prefix |
| `M-f` | hashes | file picker over files the selected commits touched |
| `C-d` | hashes | `git diff <hash>` vs working tree, to terminal |
| `C-s` | hashes | toggle sort |
| `M-e` | files, refs | open in `$EDITOR` |
| `C-o` | most | open on web host (untested with GHE) |
| `C-x` | worktrees, stashes | **deletes without confirm**: `git worktree remove` / `git stash drop` (stash stack is shared) |

## Side effects of sourcing

- `M-r` → `redraw-current-line` (was `revert-line`).
- Readline `C-z` toggles vi/emacs mode (used by the macros; tty still suspends on Ctrl-Z).
- Emacs-mode pickers overwrite the kill ring (`C-y` afterward won't yank your last kill).

## Example: fast-forward another worktree's branch to a detached commit

`git -C ` `C-g C-w` ` merge --ff-only ` `C-g h` → `Enter` on the top hash.
Resolve the hash in *this* shell; a literal `HEAD` would resolve in the target worktree.
