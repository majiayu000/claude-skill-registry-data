---
name: mac-optimize
description: Diagnose and fix macOS resource pressure for Claude Code workflows. Use when load avg is high, swap is saturated, CC feels slow, or before spinning up parallel agents/worktrees. Covers CPU top-talkers, swap pressure, zombie claude processes, Node heap tuning, Spotlight/background-agent pruning, and purge. Apple Silicon aware.
allowed-tools: Bash, Read, Write, Edit
---

# mac-optimize

Fast triage + fix skill for macOS resource pressure on this workstation. Keep CC responsive, keep parallel agents/worktrees from thrashing swap.

## When to run

- Load avg > 4 (Apple Silicon: sustained, not spikes)
- `sysctl vm.swapusage` shows >70% of swap used
- CC replies feel slow / tools time out
- Before starting a parallel-agents session or >2 worktrees
- Session-start (via hook)

## Triage: one-shot diagnose

```bash
bash ~/.claude/skills/mac-optimize/diagnose.sh
```

## Boost: one-shot apply (reversible)

```bash
bash ~/.claude/skills/mac-optimize/boost.sh          # kills zombies, renices competitors, sets NODE_OPTIONS
bash ~/.claude/skills/mac-optimize/boost.sh --purge  # also runs sudo purge (prompts)
```

Reports: load avg, swap %, top 10 CPU procs, top 10 RSS procs, zombie claude sessions (>6h old), Node version + NODE_OPTIONS, Spotlight worker count.

## Common fixes (ranked by impact)

### 1. Kill zombie claude processes (biggest quick win)
Stale CC sessions hold 400–700MB each. Find + kill anything older than 6 hours:
```bash
ps -axo pid,etime,rss,comm | awk '$4=="claude" && $2 ~ /-/ {print $1, $2, $3}'
# Review output, then:
kill <PID>   # not -9; let it flush
```
Restart via `claude --resume` if that terminal tab is still open.

### 2. Free compressed/purgeable memory
```bash
sudo purge   # needs password; reclaims cached/purgeable pages
```
Use when swap >70%. Takes 2–5s. Safe — only drops reclaimable caches.

### 3. Tune Node heap for CC
Default V8 old-space is ~4GB. On a 24GB Mac running 2+ CC sessions, cap each:
```bash
# Add to ~/.zshrc (or ~/.config/zsh/env.zsh)
export NODE_OPTIONS="--max-old-space-size=6144"
```
Prevents one CC process from ballooning past 6GB when parsing huge tool outputs.

### 4. Audit launch agents
```bash
ls -1 ~/Library/LaunchAgents
launchctl list | grep -v "^-" | sort -k2 -rn | head -15   # sort by PID (running)
```
Disable unused ones:
```bash
launchctl unload -w ~/Library/LaunchAgents/<plist>
```

### 5. Spotlight pruning (CC source dirs)
Developer directories don't need Spotlight indexing — saves mdworker CPU:
```bash
sudo mdutil -i off /Volumes/External\ HD/Desenvolvimento
sudo mdutil -E /Volumes/External\ HD/Desenvolvimento   # erase existing index
```

### 6. Close known high-idle-CPU offenders
Check diagnose output. Usual suspects on this box:
- **Bitwarden** (20–30% idle CPU — known Electron bug) — quit when not unlocking
- **UTM / Virtualization.framework VM** — `osascript -e 'tell application "UTM" to quit'` then `kill <VM-XPC-pid>` if orphaned (parent=1). Frees 3–4 GB RAM.
- **OpenClaw** (no longer used on this machine): `launchctl unload -w ~/Library/LaunchAgents/ai.openclaw.*.plist` + `pkill -f openclaw`.
- **Spotify / Discord / WhatsApp** — quit during heavy CC sessions
- **Brave tabs** — each renderer ≈ 200–300MB, 49 procs ≈ 6.6GB total on this box.

### 7. Brave Memory Saver (applied 2026-04-15)
Prefs patched at `~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Preferences`:
- `performance_tuning.high_efficiency_mode.state = 2` (always on)
- `tab_discarding.enabled = true`

Requires a **Brave restart** to take effect. After restart, inactive tabs auto-suspend (~60–80% RAM reclaim on idle tabs without losing session).

To reapply after profile reset: re-run the python snippet in `boost.sh` or:
```bash
python3 -c "import json; p='$HOME/Library/Application Support/BraveSoftware/Brave-Browser/Default/Preferences'; d=json.load(open(p)); d.setdefault('performance_tuning',{}).setdefault('high_efficiency_mode',{})['state']=2; d.setdefault('tab_discarding',{})['enabled']=True; json.dump(d,open(p,'w'),separators=(',',':'))"
```

## Preflight before parallel agents / worktrees

Before `dispatch-parallel-agents` or spawning >2 worktrees, run diagnose. Abort if:
- Free memory < 1GB AND swap > 85%
- Load avg > 6

First run fix #1 (zombies) + #2 (purge), recheck, then proceed.

## Integration

- Session-start hook: `~/.claude/hooks/session-start-mac-check.sh` runs diagnose and warns if thresholds breached.
- Codex mirror: `~/.codex/scripts/mac-optimize.sh` (symlink or copy of diagnose.sh).

## Don't do

- Don't `kill -9` claude — it leaves orphaned MCP server processes that eat RAM.
- Don't disable Spotlight system-wide (breaks Raycast, Alfred).
- Don't `sudo purge` in a tight loop — once per hour max.
- Don't set `--max-old-space-size` above 8192 on a 24GB Mac with VMs running.
