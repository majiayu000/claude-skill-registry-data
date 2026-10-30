---
name: shedding-season
description: Appa's shedding season for reclaiming disk. Every spring Appa sheds his winter coat, and the team sweeps up what he no longer needs, never what someone is still using. Use for worktree-cleanup, "what's using my disk", "clean up worktrees", "prune safe-to-prune worktrees", "free up space", or "delete old simulators". Audits every git worktree read-only, cross-checks pinned and active chats, pauses on any uncommitted work, then prunes only the confirmed set.
---

# Appa's shedding season

Every spring Appa sheds his thick winter coat, and fur ends up everywhere. The team sweeps it up. They do not sweep up Momo, the saddle, or Sokka's map. Old worktrees and simulators are shed fur. Clear them, and never clear something a person or an agent is still using.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

This is the one skill that deletes user state with no code review to catch a slip. The gates below are the review.

## Steps

1. **Snapshot and audit.** Record `df -h /`. Then run the audit (Build the Lever, Fire in `four-elements`).

   ```bash
   node <this-skill>/scripts/worktree-audit.mjs [repo-path] [transcripts-path ...]
   ```

   [scripts/worktree-audit.mjs](scripts/worktree-audit.mjs) reads paths from `git worktree list`, never hand-typed ones. A hand-typed `myrepo-worktrees/x` misses a worktree that lives at `.worktrees/myrepo/x` (Encode Lessons in Structure, Fire in `four-elements`). It classifies each worktree by size, age, merge state, uncommitted work, PR state, and the newest chat that touched it, then suggests a bucket. Without a transcripts path it scans Claude Code's projects under `$CLAUDE_CONFIG_DIR` and Codex's sessions under `$CODEX_HOME`. The transcript scan is slow, so run it in the background. The audit never deletes anything. Any fact it cannot read stays unknown, and an unknown fact keeps a row out of the `safe` bucket.
2. **Treat the bucket as advice, not permission.** The pinned and active chats are the real artifact (Prove It Works, Earth in `four-elements`). Get that set from the user or your own session list, and cross-check every candidate. The audit has marked `safe` a worktree the user had pinned, so the pinned set wins.
3. **Verify usage before deleting.** For every `verify-recent-chat` row, or anything you doubt, dispatch characters to read the transcripts and report whether the chat is pinned or ongoing and which worktrees it touches (Guard the Context Window, Fire in `four-elements`, because transcripts are bulk). A pinned chat spawns comparison and repro trees into sibling worktrees through background agents, and those are in use even when their names never appear in the session list. Pick each dispatch's effort for the job, as `avatar-mode` describes.
4. **Pause on irreversible loss.** Read the DIRTY column.
   - `wip:N` is N tracked paths with uncommitted changes.
   - `untracked:N` is N files git has never seen. A worktree with both prints both, as in `wip:1,untracked:5`.
   - `ignored:N` is N paths git ignores outside the build and cache directories named in the audit's `DISPOSABLE` list, such as `.env` or `.claude/settings.local.json`. These may exist nowhere else. List them with `git -C <path> status --porcelain --ignored=matching`.
   - `reflog:N` is N commits that no branch, tag, or remote reaches. Only the worktree's HEAD and its reflog keep them, as with work committed on a detached HEAD. They are among the entries `git -C <path> reflog` prints. Keep any of them with `git branch <name> <sha>`.

   A clean worktree is recoverable from its branch. Uncommitted work of either kind is gone once the directory goes. List it with the same call the audit counted from, `git -C <path> status --porcelain --untracked-files=all --ignore-submodules=none`. Show the diff from `git -C <path> diff HEAD --ignore-submodules=none --submodule=log`, and get a decision first. Each status line is work at stake, and an empty diff never means there is none. A diff leaves out every untracked file, and a plain `git diff` can leave out a submodule. A `wip` line that names a submodule stands for files changed or added inside it, or for commits made there. Run the same status call inside the submodule to list them.

   The bucket `hold-locked` means another tool or agent locked the tree, with its reason in the LOCKED column. `git worktree remove` refuses a locked tree, so never `rm -rf` around it.

   Clean, merged, and not in use proceeds without asking. Every `wip`, `untracked`, `ignored`, `reflog`, locked, or in-use worktree pauses for the user.
5. **Prune the confirmed set.** For each path, run `git worktree remove --force <path>`. If the directory survives on ignored build artifacts, remove it with `rm -rf`, then run `git worktree prune`. Branch refs survive, so commits on the worktree's branch are kept. The worktree's HEAD reflog goes with it, so a commit only that reflog reaches is lost. Commits made inside a submodule are stored with the worktree and go with it. Confirm with `df -h /` and list the worktrees again.
6. **Simulators and other reclaimers.** Simulators are usually the next biggest win.
   - `xcrun simctl --set testing delete all` removes XCTestDevices clones.
   - `xcrun simctl delete unavailable` removes simulators for missing runtimes.
   - `xcrun simctl runtime list`, then `xcrun simctl runtime delete <id>`, removes old runtimes.

   When you need more, the other reclaimers are Xcode `DerivedData` and `iOS DeviceSupport`, your editor's application-support caches, `~/.claude/shell-snapshots/`, old `~/.claude/projects/` transcripts (keep the recent ones that `spirit-world` and `break-camp` read), and package caches (pnpm, uv, brew, yarn). Clear only caches the user has not said to keep.

## Rules

- The audit is read-only. Deletion happens only in step 5, and only for the confirmed set.
- Never delete a worktree with uncommitted, untracked, ignored, or reflog-only work without the user's word on that worktree.
- Never force past a lock.

## Reply

`df -h /` before and after, with the space reclaimed. The worktrees pruned. A one-line reason for each one held back (in use by which chat, or which uncommitted work).
