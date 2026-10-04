---
name: wsl-cursor-health
description: >-
  Diagnose WSL2 + Cursor/Claude performance on a Windows PC (Ubuntu/WSL intensive
  coding): memory/swap pressure, load, disk, inotify, tsserver/extensionHost RSS,
  Linux and Windows Cursor caches, .wslconfig, and VHDX size. Use when the user
  asks to check caches, WSL shutdown, lag, swap, slow IDE, memory pressure,
  clear caches, compact VHD, or whether the machine needs a reset after heavy
  agent/context sessions. Prefer detect-then-recommend; never auto wsl --shutdown.
---

# WSL + Cursor health

You are on a **Windows PC** doing intensive context coding with **Cursor** (and
often Claude in-app / Claude Code) against **Ubuntu on WSL2**. When this skill
is invoked, **run the probe first**, then report findings and remediation in
severity order. Do not jump to `wsl --shutdown` or cache wipes without evidence.

## Invoke immediately

From any workspace (script is absolute-path safe):

```bash
bash /home/josh/dev/01-Movemental-Core/my-skills/cursor/wsl-cursor-health/scripts/check-health.sh
```

Or after install (`~/.cursor/skills/wsl-cursor-health` → my-skills):

```bash
bash ~/.cursor/skills/wsl-cursor-health/scripts/check-health.sh
```

Parse the trailing `MACHINE_SUMMARY` line (`severity=OK|WARN|CRIT`, `codes=...`).

## Progress checklist

```
wsl-cursor-health:
- [ ] 1 Run check-health.sh
- [ ] 2 Classify severity from MACHINE_SUMMARY + Findings
- [ ] 3 Soft fixes first (reload TS / window) when WARN
- [ ] 4 Safe cache clear only if sizes flagged + user confirms
- [ ] 5 Recommend wsl --shutdown from Windows only when CRIT/swap/session warrants
- [ ] 6 Optional: .wslconfig / VHDX compact guidance
- [ ] 7 Short report: what is wrong, what to do, what not to do
```

## Hard rules

- **Detect, then recommend.** Never run destructive cleanup unprompted.
- **Never run `wsl --shutdown` from inside WSL** as an “agent action” that you expect to continue afterward — it kills the distro (and this session). Tell the user to run it in **Windows PowerShell or cmd**.
- **Never delete** `~/.cursor/projects`, Claude transcripts, `.git`, `.env*`, or `node_modules` as part of this skill.
- Safe Linux clears require `CONFIRM=1` via `scripts/clear-safe-caches.sh`.
- Windows Cursor `Cache` / `CachedData` clears require **Cursor fully quit** first.
- Prefer soft IDE fixes before VM restart when severity is WARN.

## Severity → action

| Severity | Typical signals | Agent response |
|----------|-----------------|----------------|
| **CRIT** | High swap (≥40% or ≥2GiB), tiny MemAvailable, disk ≥90%, extreme tsserver RSS | Lead with **save work → `wsl --shutdown` from Windows → reopen**. Then re-probe. |
| **WARN** | Moderate swap, elevated RAM, fat caches, long uptime, busy extensionHost | Soft fixes first; optional safe cache clear; shutdown if still bad. |
| **OK** | No thresholds crossed | Say healthy; mention re-run after multi-hour agent marathons. |

## Soft fixes (try before shutdown)

Ask the user (or guide them) in this order when WARN and swap is not critical:

1. **TypeScript: Restart TS Server** (tsserver RSS flagged)
2. **Developer: Reload Window** (extensionHost / stale MCP children)
3. Close unused Cursor windows/workspaces on large monorepos
4. Kill obvious orphaned `node`/`vite`/`playwright` children only if clearly stale (confirm PIDs)

## Safe cache clear (Linux)

Only when the probe flagged sizes and the user agrees:

```bash
CONFIRM=1 bash ~/.cursor/skills/wsl-cursor-health/scripts/clear-safe-caches.sh npx trash
# or: playwright | vite | all
```

## WSL shutdown (Windows host)

When CRIT swap/memory or long uptime + swap WARN that soft fixes did not clear:

```powershell
wsl --shutdown
```

Then reopen Cursor / Ubuntu. Re-run `check-health.sh`.

Optional compact (host disk pressure / large `ext4.vhdx`) — details in [reference.md](reference.md).

## Report format

Keep it short:

```markdown
## Verdict: CRIT|WARN|OK — <one line>

### Signals
- ...

### Do now
1. ...

### Optional later
- ...

### Do not
- Auto-shutdown from WSL / wipe project state / delete node_modules
```

## Extra detail

Thresholds, `.wslconfig` knobs, Windows cache paths, VHDX compact: [reference.md](reference.md).
