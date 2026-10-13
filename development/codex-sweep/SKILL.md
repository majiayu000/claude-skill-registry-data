---
name: codex-sweep
description: "Kill stale OpenAI Codex plugin processes (orphaned app-server brokers, codex app-server/exec orphans) and clean their cxc-* temp dirs. Use when: (1) User says 'codex sweep', 'stale codex', 'codex processes', 'too many codex processes', or 'kill codex orphans', (2) A build fails with EMFILE, 'too many open files', or fs.inotify.max_user_instances exhaustion (e.g. Vite dev server on WSL2), (3) ps shows many app-server-broker.mjs or codex app-server processes, (4) After force-killing terminals or removing worktrees that had codex review sessions."
argument-hint: "[--dry-run] [--age <hours>]"
allowed-tools:
  - Bash(node *)
  - Bash(ps *)
---

# Codex Sweep

Scans the process table for stale OpenAI Codex plugin processes and kills them, then removes their dead `cxc-*` temp dirs.

Why they accumulate: the codex plugin spawns one detached broker (`app-server-broker.mjs` + a `codex app-server` child) per workspace, and cleanup relies on Claude's SessionEnd hook — which never fires on killed terminals, crashes, or worktree-teammate sessions. Orphans pile up (~3 processes each); on WSL2 they exhaust `fs.inotify.max_user_instances=128` and Vite starts failing with EMFILE.

Safe by design: the plugin respawns a broker on demand (`ensureBrokerSession` self-heal), so a false-positive kill costs at most a ~2s respawn. Brokers belonging to live Claude sessions are detected and kept.

## Run

Run directly — no confirmation step needed (unlike /dev-clean-wsl's deletions, kills here cost nothing to redo):

```bash
node $HOME/.claude/scripts/codex-sweep.js
```

Pass through user args:

- `--dry-run` — when the user asks "what would it kill" (lists each broker: pid, age, tier, workspace)
- `--age <hours>` — tier-2 idle threshold (default 2h; a SessionStart hook also runs this automatically with `--auto` = 6h threshold, throttled to once per 6h)
- `--json` — machine-readable

What it kills:

- **Tier 1** (always): brokers whose `--cwd` workspace was deleted; `codex app-server` orphaned to PPID 1; `codex exec` orphaned to PPID 1 for >60 min
- **Tier 2**: brokers older than the age threshold with no live claude session at or above their workspace

## Report

Relay the script's summary line to the user. On `--dry-run`, show the per-broker table.

## If the user hit EMFILE / inotify exhaustion on WSL2

After sweeping, verify the pressure dropped:

```bash
find /proc/*/fd -lname 'anon_inode:inotify' 2>/dev/null | wc -l
```

If it recurs, raise the ceiling (see the inotify note in /dev-clean-wsl):

```bash
echo 'fs.inotify.max_user_instances=1024' | sudo tee /etc/sysctl.d/60-inotify.conf
sudo sysctl --system
```

## Troubleshooting

- "kept N brokers" is normal — those belong to live Claude sessions or are under the age threshold.
- "tier 2 skipped: liveness lookup failed" — `lsof` (Mac) or `/proc` (Linux) lookup failed; tier 1 still ran. Rerun manually.
- Some `cxc-*` dirs survive one cycle after a sweep (10-min mtime floor guards freshly-spawned sessions); the next sweep removes them.
- A workspace on an unmounted volume looks deleted → its broker gets killed. Harmless: respawns on next use.
