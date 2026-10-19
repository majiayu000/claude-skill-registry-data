---
name: cleanup-dev
description: Free disk space by clearing dev caches and build artifacts. Reports sizes per bucket, asks per-bucket confirmation, then deletes only what the user approves. For fvm SDKs and per-project artifacts, user picks interactively. Use /cleanup-dev [--no-analyze].
purpose: Frees disk space by clearing dev caches and build artifacts, with per-bucket confirmation.
user_invocable: true
stage: desk
---

# Cleanup Dev Caches

Frees disk space by clearing common dev caches and build artifacts. Nothing is deleted without per-bucket approval.

## Arguments

- `--no-analyze` (alias: `--skip-analyze`, `fast`) — skip step 6 (interactive filesystem analyzer). Run only the known buckets, fvm versions, and per-project artifact scan.

## Workflow

### 1. Report global buckets

```bash
~/.claude/hooks/cleanup-dev-report.sh
```

Output is pipe-delimited `bucket|size|detail`. Present as a table sorted by size descending. Skip buckets whose size is `-` (missing) or `0B`.

### 2. Confirm per bucket

For each reportable bucket **except `fvm-versions`**, use AskUserQuestion:

```
question: "Clean <bucket> (<size>)?"
options:
  - label: "Clean"
    description: "<what it does>"
  - label: "Skip"
    description: "Leave it alone"
```

Collect the approved buckets into a list.

### 3. Execute approved buckets

Run once with all approved bucket keys:

```bash
~/.claude/hooks/cleanup-dev-execute.sh <bucket1> <bucket2> ...
```

Skip this step if the list is empty.

### 4. fvm versions (interactive)

If `fvm-versions` count > 1, list the installed versions:

```bash
fvm list
```

Parse the version strings. Use AskUserQuestion with one option per version (multi-select) plus a "Skip all" option. For each selected version:

```bash
~/.claude/hooks/cleanup-dev-execute.sh fvm-remove <version>
```

Never auto-remove — always ask.

### 5. Per-project build artifacts (interactive)

Ask whether to scan for per-project artifacts (`node_modules`, `.dart_tool`, `build`, `target`, `.next`). If approved:

```bash
~/.claude/hooks/cleanup-dev-project-scan.sh
```

Output is `size|path`, already sorted by size desc. Present the top entries. Use AskUserQuestion (multi-select) to let the user pick which paths to delete. For each approved path:

```bash
~/.claude/hooks/cleanup-dev-execute.sh project-path <path>
```

The execute script refuses any path whose basename isn't one of the allowed artifact names — safety net.

### 6. Analyze filesystem (interactive, read-only)

**Skip this entire step if the user passed `--no-analyze` / `--skip-analyze` / `fast`.**

Ask whether to analyze arbitrary paths for other space hogs outside the known buckets. If approved:

1. Ask the user which path to start from (default `$HOME`).
2. Run:

   ```bash
   ~/.claude/hooks/cleanup-dev-analyze.sh <path> 20
   ```

   Output is `size|path`, sorted by size desc. Present as a table.

3. Use AskUserQuestion (multi-select) with one option per returned path plus **Drill in** / **Stop**. Options:
   - **Drill in** — pick one path to re-analyze at the next level.
   - **Stop** — finish analysis.

4. If the user picks a path to drill into, re-run the script with that path. Repeat until the user stops or reaches a leaf directory.

5. For any paths the user wants removed:
   - If the path's basename matches an auto-bucket or `node_modules|.dart_tool|build|target|.next`, route through `cleanup-dev-execute.sh`.
   - Otherwise, surface the path with a clear warning and ask explicit confirmation before deletion. This script never deletes arbitrary paths on its own.

Never recommend deleting system or app-data paths (`~/Library/Application Support`, `~/Library/Containers`, etc.) — these hold user data, not caches.

### 7. Summary

Report what was cleaned and roughly how much space was freed (subtract pre-report total from a fresh report of the same buckets if you want an exact number — otherwise just list the cleaned buckets).

Then record the run timestamp so `/preflight` knows this was done:

```bash
~/.claude/hooks/cleanup-dev-mark-run.sh
```

Run this even if only a subset of buckets was cleaned — partial cleanup still counts.

## Buckets

The report script detects the OS (`macOS` / `Windows` via Git Bash / `Linux`) and only emits buckets that apply. Bucket **keys** are the same everywhere — only the underlying paths differ.

**macOS-only:**
- `xcode-derived-data` — `~/Library/Developer/Xcode/DerivedData`
- `xcode-archives` — `~/Library/Developer/Xcode/Archives`
- `xcode-sim-unavailable` — `xcrun simctl delete unavailable`
- `homebrew-cache` — `brew cleanup -s`

**Cross-platform (different paths per OS):**
- `jetbrains-caches`, `jetbrains-logs` — `~/Library/...` on macOS, `%LOCALAPPDATA%/JetBrains/...` on Windows
- `android-studio-caches` — `~/Library/Caches/Google/AndroidStudio*` on macOS, `%LOCALAPPDATA%/Google/AndroidStudio*` on Windows
- `pub-cache` — `~/.pub-cache` on macOS/Linux, `%LOCALAPPDATA%/Pub/Cache` on Windows
- `yarn-cache` — `~/.yarn/cache` on macOS/Linux, `%LOCALAPPDATA%/Yarn/Cache` on Windows
- `npm-cache` — `~/.npm/_cacache` on macOS/Linux, `%APPDATA%/npm-cache` on Windows
  - `npm-cache-home` — extra Windows bucket when `~/.npm/_cacache` also exists (nvm-windows / Git Bash installs)

**Works anywhere (`$HOME` = `%USERPROFILE%` under Git Bash):**
- `gradle-caches`, `gradle-daemon`
- `pnpm-store`
- `cargo-registry`, `cargo-git`
- `docker-prune` — `docker system prune -af` + `docker volume prune -f`

**Interactive (user picks individual items):**
- `fvm-versions` — Flutter SDK versions via fvm
- `project-artifacts` — per-project `node_modules`, `.dart_tool`, `build`, `target`, `.next`

## Safety

- Scripts refuse unknown buckets and refuse arbitrary paths (only recognized artifact dir names).
- No `sudo`, no system paths, no `~/Library` / `%APPDATA%` outside cache/log dirs.
- Project scan excludes `~/Library` (macOS), `~/AppData`, `~/OneDrive*`, `~/$Recycle.Bin` (Windows), and `~/.Trash`.
- `analyze` uses `du -x` to skip filesystem boundaries and NTFS junctions.
- Report scripts are read-only; only `cleanup-dev-execute.sh` deletes.
