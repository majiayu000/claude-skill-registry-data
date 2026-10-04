---
name: reclaim-disk-space
description: >-
  Audit and reclaim disk space cautiously on a development Mac, especially
  when storage is nearly full, caches and build artifacts have accumulated, or
  a Git repository has many temporary worktrees. Use for disk-usage
  investigation, cleanup planning, cache pruning, and explicitly requested
  deletion. Separates reproducible data from user state, verifies Git
  worktrees are registered, clean, and merged, and reports exact targets,
  recovery risk, and measured space before and after.
---

# Reclaim disk space

Treat size as a discovery signal, never as deletion authority. Prefer a smaller
verified cleanup over a broad deletion with ambiguous ownership.

## Establish authority

Classify the request before mutating anything:

- For "inspect," "audit," "what can I delete," or equivalent, perform
  read-only discovery and return a ranked plan.
- For an explicit request to delete a named category, treat that category as
  approved. Re-resolve its exact targets immediately before deletion.
- Stop for a new choice when cleanup would include personal files, application
  state, credentials, active sessions, database volumes, dirty Git state, or
  anything outside the approved category.

Never expand "delete caches" into repositories, application support, or user
history. Never expand "delete worktrees" into branches.

## Audit in phases

1. Record `df -h .`.
2. Inspect likely roots with bounded `du` calls. Use `du -x -d 1 <root>` on
   macOS; remember its default units are 512-byte blocks. Use `du -sk <path>`
   when reporting KiB/GiB.
3. Drill into only the largest relevant roots. Do not launch overlapping
   whole-home scans that repeatedly traverse the same files.
4. Classify each candidate:
   - **Reproducible:** build output, package caches, model caches, derived data,
     and clean merged worktrees.
   - **Conditionally reproducible:** simulators, Docker images, offline media,
     application runtime bundles, and dependency installations.
   - **User state:** documents, Git changes, app databases, chat/session
     history, credentials, Docker volumes, and editor global state.
5. Report exact paths, physical sizes, why each is safe or risky, and the
   expected recovery. Do not count sparse-file apparent size as physical usage.

Prefer supported pruning commands over raw deletion when they preserve useful
state. Close an application before deleting its caches.

## Clean Git worktrees

Use the bundled script from the repository root:

```sh
bun run .agents/skills/reclaim-disk-space/scripts/worktree-cleanup.ts
```

The default is audit-only. It fetches the default remote, preferring `origin`
when present, resolves that remote's symbolic HEAD, and labels every registered
worktree. When the integration branch differs or the remote HEAD is not
available, name an explicit remote-tracking branch:

```sh
bun run .agents/skills/reclaim-disk-space/scripts/worktree-cleanup.ts \
  --target upstream/trunk
```

A candidate is removable only when all of these hold:

- It is neither the repository's primary worktree nor the worktree invoking the script.
- Its exact path is still registered.
- The directory exists.
- `git status --porcelain` is empty, including untracked files.
- Its `HEAD` is an ancestor of the freshly fetched remote target.

After reviewing the audit and receiving deletion authority, pass every approved
path explicitly:

```sh
bun run .agents/skills/reclaim-disk-space/scripts/worktree-cleanup.ts \
  --target upstream/trunk \
  --remove /exact/clean-worktree-one \
  --remove /exact/clean-worktree-two
```

The script validates the whole manifest before deleting the first path,
revalidates each path at action time, and calls `git worktree remove` without
`--force`. It never deletes branches. Do not replace this with `rm`, a glob, a
prefix sweep, or a broad temporary-directory cleanup.

Exclude dirty, unmerged, missing, unregistered, primary, and current worktrees.
Preserve them and name the failed predicate.

## Handle common large categories

- **Build output and dependency caches:** safe when reproducible, but note the
  reinstall or rebuild cost.
- **Xcode DerivedData:** reproducible. Keep archives and signing material out
  of scope.
- **Simulator devices:** inspect runtimes and device state first. Prefer
  `xcrun simctl delete unavailable`; require explicit approval to delete active
  devices.
- **Docker:** inspect images, build cache, containers, and volumes separately.
  Never delete `Docker.raw` directly and never infer that volumes are
  disposable.
- **Editor/Application Support databases:** treat as user state even when
  unusually large. A file named `state.vscdb`, `workspaceStorage`, or
  `globalStorage` may hold history. Do not delete it as a cache.
- **Codex or agent sessions:** treat active and archived sessions as user
  history. Delete only when the user explicitly accepts that loss.
- **Package/model caches:** usually redownloadable. State the network and
  wall-clock cost before removal.

If free space is too low for normal tools, reclaim one small,
high-confidence reproducible target first. Do not attempt an in-place database
vacuum that needs temporary space larger than the available capacity.

## Verify and report

After deletion:

1. Run `df -h .` again.
2. Verify removed worktrees no longer appear in `git worktree list`.
3. Report removed targets, refusals, recovered space, and remaining risky
   candidates.
4. State whether recovery is possible: caches are redownloadable; removed
   worktree branches and commits remain; untracked files would not be
   recoverable and therefore must have blocked deletion.

Do not describe a partial cleanup as complete when a command failed or a target
was skipped.

This workflow is adapted from an MIT-licensed upstream repository skill.
