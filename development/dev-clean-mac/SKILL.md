---
name: dev-clean-mac
description: Reclaim disk space on a Mac dev machine by deleting regenerable dev caches (Cargo/zfb build output, node_modules, pnpm/npm caches, OS/app caches) and thinning APFS local snapshots so the space actually frees. Manual-only — invoke with /dev-clean-mac when a Mac is low on disk.
disable-model-invocation: true
argument-hint: "[--keep-node-modules]"
---

# Dev Clean Mac

Frees disk on a Mac dev machine by deleting caches and build artifacts that
regenerate on demand. Tuned for this layout — `$HOME/repos` (with `myoss/zfb`),
a shared Cargo target dir, pnpm/npm caches — but every step is existence-guarded,
so it runs safely on any Mac with a similar structure (e.g. a second machine).

**Why a script and not ad-hoc `rm`:** on APFS, deleting files frees nothing while
local Time Machine snapshots still reference the data — `df` keeps showing the old
number. The script ends by thinning those snapshots (`tmutil thinlocalsnapshots`),
which is what makes the reclaimed space materialize. Skipping that step is the #1
reason a cleanup "does nothing."

## Workflow

The script lives at `scripts/clean-mac.sh` in this skill directory.

1. **Dry run first** — show the user what will be freed, delete nothing:

   ```bash
   bash "$HOME/.claude/skills/dev-clean-mac/scripts/clean-mac.sh" --dry-run
   ```

   Relay the per-path sizes and the measured total to the user.

2. **Confirm node_modules.** By default the script deletes **all** `node_modules`

   under `$HOME/repos` (reinstallable via `pnpm/npm install`). If the user is
   mid-work on a project, pass `--keep-node-modules` to preserve them.

3. **Run for real:**

   ```bash
   bash "$HOME/.claude/skills/dev-clean-mac/scripts/clean-mac.sh" --run
   # or, to keep node_modules:
   bash "$HOME/.claude/skills/dev-clean-mac/scripts/clean-mac.sh" --run --keep-node-modules
   ```

   The deletions can take a few minutes (millions of small files); it may
   auto-background. Report the BEFORE/AFTER `df` lines it prints.

## What it cleans

- **Cargo:** the shared `target-dir` from `$HOME/.cargo/config.toml` (defaults to

  `$HOME/.cargo-target`, dominated by zfb), `$HOME/.cargo/registry`, and every
  per-project `target/` under `$HOME/repos` (detected by cargo's `CACHEDIR.TAG`).

- **zfb:** checked-in release tarballs (`zfb-*.tar.gz`) and all `.zfb-build/` dirs.
- **node_modules:** every one under `$HOME/repos` (unless `--keep-node-modules`).
- **JS caches:** `pnpm store prune`, `npm cache clean`, `$HOME/Library/Caches/pnpm`.
- **OS/app caches:** ms-playwright, electron, copilot, `$HOME/.cache/codex-runtimes`,

  Homebrew cache, Adobe/CreativeCloud logs, unavailable iOS simulators.

- **Downloads:** `*.dmg` / `*.pkg` installers (re-downloadable).
- **APFS local snapshots:** thinned at the end to release everything above.

## What it never touches

Source trees, image/data stashes (e.g. `zmod-image-stash`), browser profiles,
and app data (Claude/Chrome/Slack containers) — only regenerable caches and
artifacts. Every path is verified to be under `$HOME` before removal; missing
paths are skipped silently, which is what makes it portable across machines.

## Notes

- First builds/installs after running are slower (caches re-download, projects

  rebuild) — that's the expected trade for the space.

- Safe to re-run anytime; all steps are idempotent.
- Local Time Machine snapshots are convenience restore points, not your real

  backup — thinning them does not affect Time Machine backups on disk/network.
