---
name: previewing-changes-in-worktrees
description: Drafts a change in a sparse git worktree, shows it side by side in nvim/tmux, then merges it in. Use to show or preview a diff.
argument-hint: <name> <repo-relative files...>
allowed-tools: Bash(source ~/.claude/skills/previewing-changes-in-worktrees/scripts/sparse_worktree.sh *)
---

# Previewing changes in worktrees

Use when the user wants to see a proposed change as a real diff before it lands, e.g. during
plan review ("show me the diff", "open it side by side"). The draft lives in a throwaway worktree
outside the checkout; the user's files, index, stash and config stay untouched until
`worktree_apply`.

The functions are plain bash in `scripts/sparse_worktree.sh`; read its header for what each
does. The Bash tool starts a fresh shell per call, so source it in every call:

```bash
source ~/.claude/skills/previewing-changes-in-worktrees/scripts/sparse_worktree.sh && <function> ...
```

## Steps

1. From inside the source checkout, create the worktree with every file the change touches,
   including files it will create. It snapshots the working tree, uncommitted edits included
   (~3 s on the monorepo):
   ```bash
   ... && sparse_worktree excess_speed learning/x/a.py learning/x/BUILD learning/x/new.yaml
   ```
   It prints the worktree path, `$SPARSE_WORKTREE_ROOT/<name>` (default `/tmp/sparse_worktrees`).
2. Edit the copies under that path with Read/Edit/Write, never the checkout. Batch independent
   edits in one message. More files later: `sparse_worktree_add <name> <files...>`. To delete a
   file: `git -C <worktree> rm <file>`.
3. Show it: `worktree_diff <name>` opens a tmux split running
   `git difftool -t nvimdiff`, one file at a time, base on the left; it prints the pane id. The
   pane closes after the last file. After further edits, rerun with
   `worktree_diff <name> <pane id>`: it reuses the pane if it is still open, else splits anew. Tell the user: `]c`/`[c` jump between changes, `:qa` moves
   to the next file, `:cq` stops. `worktree_patch <name>` writes `<root>/<name>.patch` if they
   want the file.
4. Once approved, `worktree_apply <name>` merges each changed file into the checkout with
   `git merge-file`. It never stages anything. If a file changed in the checkout since the
   snapshot, both changes are kept; overlapping ones get conflict markers, a `conflict: <file>`
   line, and a non-zero exit. Resolve those before going on.
5. `worktree_remove <name>`. Build, lint and test in the checkout, not the worktree: it holds
   only the listed files.

## Gotchas

- Paths are repo-relative, and `sparse_worktree` must run inside the checkout it snapshots.
- Never type into the user's shell with `tmux send-keys`; `worktree_diff` spawns or respawns its
  own pane.
