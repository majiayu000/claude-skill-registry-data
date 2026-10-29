---
name: disk-usage-audit
description: Audit disk usage holistically, explain where storage is going, and rank cleanup candidates by size, reversibility, recency, and risk. Use when Codex needs to free space, investigate low disk warnings, map large directories or files, review cloud-sync policy, identify stale apps or app data, or distinguish safe-to-delete generated artifacts from active personal data on macOS, Linux, or similar environments.
---

# Disk Usage Audit

Build a storage map before recommending or performing cleanup. The audit is complete when it explains the major storage buckets, ranks plausible cleanup candidates, and distinguishes generated or synced data from active unique data.

Use shell tools available in the current harness. Prefer fast primitives such as `df`, `du`, `find`, `ls`, and `stat`, adapting paths and flags to the environment. On macOS/APFS, validate logical-size discoveries with [`scripts/apfs_usage_audit.py`](scripts/apfs_usage_audit.py) before claiming how much space a path will reclaim.

For common platform and provider search targets, read [references/common-buckets.md](references/common-buckets.md) when drilling into a category. Start with the largest buckets; do not scan every listed path by default.

## Audit sequence

### 1. Establish the baseline

- Measure free and used space on the relevant volume. Use `df`, `diskutil`, or the APFS `volume-summary` command below; this is the source of truth for volume usage.
- Measure the largest directories in the user home and relevant system locations. Include developer runtimes, containers, package stores, and hidden user directories when they may explain the gap.
- Record access limits or other measurement blind spots.

On macOS/APFS, these commands provide volume usage, fast hotspot discovery, and a reclaim estimate for a specific path:

```sh
uv run python scripts/apfs_usage_audit.py volume-summary /System/Volumes/Data --json
uv run python scripts/apfs_usage_audit.py validate-top ~/Library --depth 1 --top 8 --json
uv run python scripts/apfs_usage_audit.py path-summary ~/Library/Developer/CoreSimulator --json
```

`validate-top` uses `gdu` when available, then validates leading candidates with clone-aware accounting. Prefer it over a separate raw `du` ranking on APFS. `path-summary` reports an immediate reclaim lower-bound for one path. A report of `fully contained clone groups` means whole-path reclaim may exceed that lower-bound because the full clone group is inside the candidate.

Keep the three measurements distinct:

1. **True volume usage**: free and used bytes from `df`, `diskutil`, or `volume-summary`.
2. **Logical hotspot discovery**: fast ranking from `du` or `validate-top`; APFS clones can make logical size overstate physical ownership.
3. **Clone-aware reclaim validation**: `path-summary` for one path or the validation phase of `validate-top`; treat `reclaimable_bytes` as the immediate reclaim lower-bound.

### 2. Map the major storage buckets

Group findings instead of returning a long path dump. Include the largest subpaths and sizes for the relevant categories:

- System and developer artifacts
- App bundles
- App support and container data
- Cloud-sync local copies
- Package-manager and tool caches
- Hidden user directories
- Code and project trees
- Downloads, media, and archives

Read `references/common-buckets.md` to choose likely paths for the platform, provider, or tool involved. Report major buckets even when they are not cleanup targets.

### 3. Classify large items

Assign each candidate the class that best describes its ownership and recovery path:

- `generated/rebuildable`: caches, indexes, build products, simulators, or package artifacts
- `synced but cold`: Dropbox, Google Drive, iCloud, OneDrive, mirrored folders, or offline copies
- `dormant app + leftovers`: an app bundle and support data with weak evidence of recent use
- `active unique data`: current project state, recordings, notes, archives, or personal files
- `stateful but ambiguous`: browser profiles, local LLM state, app databases, or Electron storage

### 4. Rank cleanup candidates

For each candidate, consider its size, validated reclaim, reversibility, recency, offline need, and blast radius. Prioritize items that are large, rebuildable or cloud-backed, not obviously recent, narrow in scope, and easy to verify after removal.

Treat source trees and working directories, personal documents and media, browser profiles, app state with unclear consequences, and anything that may be the source of truth as high risk. Get explicit user approval before removing a high-risk candidate. Favor caches, build outputs, simulator runtimes and derived data, package caches, container images, stopped containers, and container build caches as lower-risk candidates. Confirm that a cache or mirror is not the source of truth before classifying it this way.

When storage is cloud-backed, inspect provider policy before proposing deletion:

- Is the local data mirrored or partially cached?
- Can selected folders be made online-only?
- Can offline pinning be disabled?
- Which package manager, container runtime, browser, editor, or agent harness owns the local cache?

Verify current official guidance before recommending provider settings or other product-specific policy changes.

### 5. Clean up in small passes

Measure first and delete second. Use separate, explainable passes:

1. Caches and generated artifacts
2. Container and simulator data
3. Dormant apps and orphaned support data
4. Sync-policy changes for mirrored folders
5. Ambiguous app state, only with explicit user approval

Before each destructive pass, state the exact targets, expected reclaim, and meaningful risk. On macOS, validate large APFS targets with `path-summary /path --json` or `validate-top` so the estimate distinguishes logical size from immediate reclaim.

After each pass, verify that the targets are gone or smaller, then measure free space again. Note leftovers that did not shrink because they need product-specific compaction or reset.

## Report

Always provide both views:

- **Where the space is**: the major storage buckets and their largest subpaths, including buckets that are not cleanup targets.
- **Cleanup candidates**: one row per candidate with its path, size, validated reclaim when available, class, reason, recommended action, and risk level.

Use evidence-qualified descriptions such as `safe generated data`, `synced local copy`, `likely stale`, `active app state`, and `personal source-of-truth data`.

## Defaults and failure modes

- Prefer cloud-policy changes over deleting synced local copies.
- Prefer uninstalling an unused app and then cleaning its leftovers over deleting app data while leaving the app installed.
- Summarize by category instead of dumping every path.
- Surface unexpectedly large hidden directories, including package caches, agent directories, editor extensions, and toolchain stores.
- State when a cleanup command targeted a different provider or context than expected.
- Do not delete browser or app state based on size alone.
- Check for hidden directories in the home folder.
- Identify the actual container provider (Docker Desktop, OrbStack, Colima, or another runtime) before attributing its storage.
- Do not treat cloud-sync folders as ordinary local folders until mirror and online-only policy are clear.
- Report the full storage picture, not only deletable data.
- Do not assume a sparse disk image shrinks automatically after deleting data inside the guest.
