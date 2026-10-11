---
name: lore-stuck-merge-recovery
description: "Use when a Lore merge is stuck: Invalid merge type at merge.rs:303 from resolve/abort/restart, AntHill conflict panel buttons doing nothing, Changes in conflict, or a merge waiting to be committed. Also when the client refuses to fetch or switch branch until a merge is sent back."
---

# Recovering a stuck Lore merge

A workspace stuck in conflict has **two distinct causes** that look identical in the UI.
Diagnose first: the fixes are different and one is destructive.

If the workspace is one an `AntHill.Lore.Tests` test names (not one in the client's
`workspaces.json`), or you will re-run that suite afterwards, read `anthill-test-environment`
first: some fixtures hold a merge on purpose, the suite needs the Lore server up, and a running
client or dashboard locks the build.

## Diagnose

```bash
lore --repository <workspace> -P status
```

Read the header lines:

- `Pending merge, incoming revision <hash>` → **a real merge**. `branch merge abort`
  works. Go to "Real merge".
- No `Pending merge` line, but `Changes in conflict:` entries marked `!` →
  **corrupt merge state**. Go to "Corrupt merge state".

Confirm corruption cheaply — every merge-path command fails identically:

```bash
lore --repository <ws> -P branch merge resolve theirs --dry-run <path>
lore --repository <ws> -P branch merge abort
lore --repository <ws> -P branch merge restart <path>
```

All three returning this means the state blob is unreadable, not that you used
the wrong command:

```
[Error] Invalid merge type
  at lore-revision\src\branch\merge.rs:303:1
```

Note `status`, `history` and `revision info --metadata` still succeed — only the merge
record, a structure separate from the revision metadata, is unreadable. Do not conclude the
repository is broken.

## Corrupt merge state

No merge command can clear it. `unstage` bypasses the merge state entirely and is
the way out. It is non-destructive: it unstages the entry and leaves working-tree
content alone.

**Back up first**, then unstage every conflicted path:

```bash
# 1. copy each conflicted + staged file somewhere outside the workspace
# 2. then, per conflicted path:
lore --repository <ws> -P unstage <path>
```

Rules:

- Use `unstage`, never `reset`. `reset` overwrites the working file with the
  repository version and **destroys local edits**.
- Unstage the remaining *staged* changes too. `WorkspaceOperations.StatusAsync` sets
  `MergeInProgress` when any staged file is flagged `FlagMerged` or `FlagConflict`, and fetch
  and branch switch refuse with "a merge waiting to be committed" while it is set, so a
  merged-but-staged file keeps blocking after the conflicts are gone. Ordinary staged work
  stopped counting in 5c4ed71 (2026-09-10; verified 2026-09-24).
- The corrupt blob still exists afterwards; merge commands keep failing. That is
  fine — with nothing conflicted or staged, nothing calls them.

Verify: `status` shows only `Changes not staged for commit` / `Untracked files`,
with no `Changes in conflict` and no staged section.

## Real merge

```bash
lore --repository <ws> -P branch merge abort
```

Expect `Merge abort reverted changes` and exit 0.
