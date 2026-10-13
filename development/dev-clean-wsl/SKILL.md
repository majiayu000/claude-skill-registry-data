---
name: dev-clean-wsl
description: "Reclaim disk space on WSL2 by purging dev caches and orphaned build artifacts, then guide the user through compacting the ext4.vhdx from Windows. Use when: (1) the user says 'dev-clean-wsl', 'clean wsl', 'wsl disk full', 'free disk space', 'reclaim space', 'purge caches', or 'disk almost full' on a WSL machine; (2) a build or tool fails with ENOSPC / no space left; (3) the user wants to shrink the WSL virtual disk. Covers cargo target/registry, pnpm/npm caches, node_modules, and the vhdx-compaction step that actually returns space to the Windows drive holding it (C: or wherever it was moved)."
argument-hint: "[code-root]"
---

# dev-clean-wsl

Free space on a WSL2 machine, then hand the user the one step they must run
themselves to make that space real.

## The crux (why WSL is different)

On WSL2 the Linux filesystem is a single `ext4.vhdx` file on a **Windows drive** —
`C:` by default, but it is often moved (e.g. to `D:`). The scan resolves the real
location from the registry (`HKCU\...\Lxss` → `BasePath` for `$WSL_DISTRO_NAME`). Two consequences drive this whole skill:

1. **`/` looking healthy is not enough.** The disk that actually fills up is

   usually the drive holding the vhdx, not the Linux `/`. The scan reports both —
   read that drive first. The vhdx size minus data inside `/` is the compaction ceiling.

2. **Deleting files inside WSL does not shrink the vhdx.** The vhdx only grows; freed

   blocks stay allocated until the vhdx is **compacted from Windows**. So every purge
   below is "banked" inside WSL and becomes real free space on the host drive only after the
   compaction step. Always finish with that step — skipping it makes the cleanup
   look like it did nothing from Windows' side. Often the vhdx has ballooned far past
   the real data (e.g. 674G file vs 204G used) — then compaction itself is the big win.

`wsl --shutdown` (required for compaction) kills this session, so compaction is
always handed to the user as commands to run in a **Windows** terminal — never run
it from inside WSL.

## Step 1 — Scan (read-only)

```bash
bash $HOME/.claude/skills/dev-clean-wsl/scripts/scan.sh [code-root]
```

`code-root` is optional (defaults to `$HOME/repos`, else `$HOME`) — the directory
searched for `node_modules` and orphaned `target/` dirs, and the cwd for
`pnpm store path` (which is cwd-dependent: from `/mnt/c` it reports the Windows-side store). The deep home scan takes
~1 minute. It deletes nothing and prints: `/` vs host-drive usage, the vhdx path + size,
top home consumers, and per-category reclaimable sizes. Docker Desktop's vhdx
(`AppData\Local\Docker\wsl`) is not the distro's disk — never hand it out for compaction.

## Step 2 — Present findings and confirm

Turn the scan into a short table grouped by safety, then get the user's pick
(AskUserQuestion works well for multi-select). Do not delete large or ambiguous
things silently — these caches are recoverable but rebuilds/re-downloads cost time.

Safety tier, highest-value-and-safest first:

| Tier | Item | Why safe |
|---|---|---|
| Free (zero cost) | **Orphaned in-repo `target/`** when a global `target-dir` redirect is active | Nothing builds there anymore — pure dead weight (often the single biggest win) |
| Free (zero cost) | **Orphaned pnpm `store/vN`** (older than the active version) | `pnpm store prune` never touches old store versions; they are abandoned |
| Safe | cargo `debug/incremental`, `release/incremental` | Pure incremental cache; only slightly slows the next build |
| Safe | cargo `registry/src` + `registry/cache` | Re-fetched on demand (keep `registry/index` — refresh is slow) |
| Safe | `pnpm store prune` on the active store | Drops only unreferenced packages |
| Safe | `npm cache clean --force` (`~/.npm`) | Re-downloaded on demand |
| Costs a rebuild | active cargo `target` `debug/deps` (the big GB) | Only `cargo clean` / `rm` reclaims it; forces a full cold rebuild |
| Reinstallable | idle projects' `node_modules` | `pnpm/npm install` restores them; clear projects you are not actively on |

**Leave alone unless the user explicitly names them:**

- **User data**, not cache — e.g. `~/youtube-dl`, `~/Downloads`, media. Never auto-delete.
- **Published/intentional build outputs** — `dist/`, packaged release tarballs.

  These are project-specific and may be wanted; do not treat a generic `dist/` as cache.

## Step 3 — Purge (only what the user confirmed)

Safety rules:

- **Relative-path deletes only.** `cd` into the parent, then `rm -rf ./name` —

  never `rm -rf /absolute/path`. This is a guardrail against a mistyped absolute path.

- **Check nothing is using a dir before clearing it.** Before wiping a `target/`,

  build dir, or CI-runner workspace, confirm no live build/process owns it
  (`ps -eo cmd | grep -iE 'cargo|Runner\.Worker'`). Clearing a dir mid-build breaks it.

- **Confirm "orphaned" before claiming zero-cost.** An in-repo `target/` is orphaned

  only if a global `target-dir` redirect (env `CARGO_TARGET_DIR` or
  `~/.cargo/config.toml [build] target-dir`) points elsewhere AND its newest artifact
  predates the switch. The scan prints both signals.

Per-category commands (adapt paths from the scan output):

```bash
# Orphaned in-repo target (zero rebuild cost — redirect is active elsewhere)
cd /path/to/repo && rm -rf ./target

# Orphaned old pnpm store version (active is vN; vN-1 etc. are dead)
cd "$(dirname "$(pnpm store path)")" && rm -rf ./v10        # example: active is v11

# cargo incremental cache (safe; minor next-build slowdown)
cd "$ACTIVE_TARGET/debug" && rm -rf ./incremental

# cargo registry (re-fetched; keep index)
cd "$HOME/.cargo/registry" && rm -rf ./src ./cache

# pnpm + npm caches
pnpm store prune
npm cache clean --force

# idle project's node_modules (reinstallable)
cd /path/to/idle-project && rm -rf ./node_modules
```

For the big active cargo `debug/deps`, only offer `cargo clean` / deleting the whole
target dir if the user accepts a full cold rebuild — call out the tradeoff explicitly.

After purging, re-run a quick `df -h /` and re-measure the touched dirs so the
reported total reflects reality.

## Step 4 — Hand off the vhdx compaction (the step that frees the host drive)

This is the finale every run must end on. Pull the vhdx path from the scan output and
give the user a ready-to-paste block for a **Windows PowerShell** terminal (not WSL):

```powershell
wsl --shutdown
# Easiest (modern WSL — also keeps it sparse going forward):
wsl --manage <DistroName> --set-sparse true    # DistroName from: wsl -l -v

# …or a reliable one-time compaction via diskpart:
diskpart
  select vdisk file="<vhdx Windows path from the scan>"
  attach vdisk readonly
  compact vdisk
  detach vdisk
  exit
```

Set expectations honestly: compaction reclaims only the *free* blocks inside the
filesystem, so the vhdx shrinks to about the real data still inside WSL (the scan's
"data inside /"). State the rough before/after free numbers for the host drive from the scan so the user knows what to expect.

If the scan could not find the vhdx, have the user locate it on Windows with
`Get-ChildItem -Recurse $env:LOCALAPPDATA -Filter ext4.vhdx` — or, if it was moved
off `C:`, by reading `BasePath` under `HKCU\Software\Microsoft\Windows\CurrentVersion\Lxss`.

## Bonus — stale Codex processes (EMFILE / inotify exhaustion)

Not a disk problem, but the same "WSL slowly rots" family: orphaned codex plugin
brokers pile up (~3 processes each) and each eats inotify instances; at
`fs.inotify.max_user_instances=128` Vite starts failing with EMFILE. Sweep them:

```bash
node $HOME/.claude/scripts/codex-sweep.js
```

(A SessionStart hook runs this automatically once per 6h; the manual run is for
when EMFILE already struck. See /codex-sweep for details.)

Belt and braces — raise the ceiling so accumulation between sweeps can't bite:

```bash
echo 'fs.inotify.max_user_instances=1024' | sudo tee /etc/sysctl.d/60-inotify.conf
sudo sysctl --system
```

## Notes

- Self-hosted CI runners sometimes show up as large dirs. Their `_work/` is

  ephemeral CI workspace (safe to clear when idle); fully removing a runner means
  stopping + uninstalling its **root-owned** systemd service first
  (`sudo ./svc.sh stop && sudo ./svc.sh uninstall`), which needs the user's sudo
  password — hand them those commands rather than guessing.

- This skill assumes WSL2. On a non-WSL host the scan still reports reclaimable

  caches, but the vhdx/compaction step does not apply — the script flags this.
