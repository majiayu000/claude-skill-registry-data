---
name: hook-effectiveness
description: 'Audit Claude Code hooks for fire frequency, latency, exit codes, and output value. Surfaces hooks that never fire, hooks that fire too often (spam), hooks that exit non-zero silently, and hooks that fire but produce no output Claude actually uses. Run weekly automatically. Required after wiring new hooks.'
user-invocable: true
auto-invoke: 'scheduled-weekly + post-hook-wiring'
argument-hint: "[--days N]"
metadata:
  owner: global-agents
  tier: contextual
  canonical_source: ~/.claude/skills/hook-effectiveness
---

# Hook Effectiveness

You can have 13 hooks wired and not know which are firing. This skill makes the
hook layer observable: counts fires, measures latency, surfaces silent failures,
and flags hooks that fire constantly without value.

## Auto-invocation

- **Scheduled:** weekly via `~/Library/LaunchAgents/com.lucas.hook-effectiveness.plist`
  (Sundays 03:30, after skill-effectiveness so reports interleave). Output to
  `~/.claude/projects/<slug>/memory/hook_effectiveness.md`.
- **Triggered automatically by Claude when:**
  - User wires new hooks (post-`/update-config` or after editing settings.json)
  - User reports unexpected hook output (the "1331 turns REQUIRED ACTION" case)
  - After `/sync pull` if any hook script changed

## Workflow

### 1. Inventory wired vs unwired hooks

```bash
python3 - <<'PY'
import json, os
from pathlib import Path

settings = json.loads((Path.home() / ".claude/settings.json").read_text())
hooks = settings.get("hooks", {})

wired = set()
for event, groups in hooks.items():
    for g in groups:
        for h in g.get("hooks", []):
            cmd = h.get("command", "")
            for token in cmd.split():
                if "hooks/" in token or "rag-index/" in token:
                    wired.add((event, g.get("matcher", "*"), token))

# All scripts on disk
all_hooks = set()
for d in [Path.home() / ".claude/hooks", Path.home() / ".claude/rag-index"]:
    if d.exists():
        for f in d.glob("*.sh"):
            all_hooks.add(str(f))
        for f in d.glob("*.py"):
            all_hooks.add(str(f))

wired_paths = {w[2] for w in wired}
unwired = all_hooks - wired_paths
print(f"WIRED: {len(wired)}, UNWIRED ON DISK: {len(unwired)}")
for u in sorted(unwired):
    print(f"  unwired: {os.path.basename(u)}")
PY
```

### 2. Enable per-hook timing log (one-time setup)

If `~/.claude/hooks-timing.log` doesn't exist, wrap each hook command with a timing
shim. Otherwise read existing log:

```bash
TIMING_LOG="$HOME/.claude/hooks-timing.log"
if [ ! -f "$TIMING_LOG" ]; then
  echo "First run: enabling hook timing. Setup writes to settings.json — confirm."
  # Wrap each hook command in `time-hook.sh <real-command>` that records timing
  # to $TIMING_LOG before executing. (One-time bootstrap, not run every audit.)
fi
```

Per-hook timing entries look like:
```
2026-05-08T22:14:01Z PostToolUse turn-counter.sh exit=0 latency_ms=45 output_bytes=0
2026-05-08T22:14:11Z UserPromptSubmit autorecall-hook.sh exit=0 latency_ms=180 output_bytes=420
2026-05-08T22:14:11Z UserPromptSubmit auto-context-pack.sh exit=124 latency_ms=15000 output_bytes=0
```

### 3. Analyze the timing log

```bash
DAYS=${1:-7}
since=$(date -v-${DAYS}d -u +%Y-%m-%d 2>/dev/null || date -d "$DAYS days ago" -u +%Y-%m-%d)

awk -v since="$since" '$1 >= since' "$TIMING_LOG" \
  | awk '{
      key=$2"::"$3
      fires[key]++
      total_ms[key]+=$5+0
      if ($4=="exit=0") ok[key]++
      if ($6+0 > 0) had_output[key]++
    }
    END {
      for (k in fires) {
        avg = total_ms[k] / fires[k]
        printf "%s\tfires=%d\tavg_ms=%.0f\tok_pct=%.0f\tw_output_pct=%.0f\n",
          k, fires[k], avg, ok[k]/fires[k]*100, had_output[k]/fires[k]*100
      }
    }' | sort -t$'\t' -k2 -rn
```

### 4. Read the tool-failures log

```bash
# Cross-reference hook exit codes with tool-failures.log
tail -200 "$HOME/.claude/tool-failures.log" 2>/dev/null \
  | jq -r 'select(.err | test("hook")) | "\(.ts) \(.err)"' | head -20
```

### 5. Classify each hook

| Pattern | Severity | Action |
|---|---|---|
| Wired but never fired (last 7d) | HIGH | Check matcher, may be misconfigured |
| Fires + non-zero exit >5% of time | HIGH | Failing silently; investigate |
| Fires + p95 latency >2s | HIGH | Slowing every prompt/tool — must optimize |
| Fires + zero output >90% of time | MEDIUM | Likely useless; consider unwiring |
| Fires + outputs same systemMessage repeatedly (turn-counter spam) | MEDIUM | Tighten dedupe |
| Wired and quiet (low fires, no errors) | INFO | Working as expected |

### 6. Output

```
HOOK EFFECTIVENESS REPORT — last 7 days

Hooks wired:        13
Hooks fired ≥1x:    11
Hooks never fired:  2
  - sessionend-rag-sync.sh (matcher * SessionEnd) — possible hook event mismatch
  - automation-orchestrator.sh — UNWIRED on disk; not in settings.json

HIGH severity (2):
  turn-counter.sh — fired 487× in 1 session, output spam every 10 turns
                    Already fixed 2026-05-08 (commit 04ec576). Re-run report next week.
  
  auto-context-pack.sh — exit=124 (timeout) 14% of fires
                    p95 latency 11.4s (timeout 15s). Reduce budget or raise timeout.

MEDIUM (1):
  protect-files.sh — fired 230×, blocked 0 edits, no output
                    Working but maybe over-broad matcher. Audit matcher.

INFO (8):
  rtk-rewrite, autorecall-hook, repeat-read-guard, reindex-hook,
  pre-compact-summary, post-compact-reset, sessionstart-aggregate,
  sessionstart-drift-reindex — all firing, low latency, healthy
```

### 7. Apply quick fixes

If a hook is unambiguously broken (wrong matcher, exit non-zero with clear error,
zero useful output), propose the fix. For threshold/dedupe issues, surface as a
review item.

### 8. Write to memory

Output to `~/.claude/projects/<slug>/memory/hook_effectiveness.md`.

## Outputs / Evidence

- Wired vs unwired inventory
- Per-hook fire/latency/exit/output stats
- Severity-classified findings with proposed fixes
- Memory file for next-session context

## Failure / Stop Conditions

- Timing log not present and user declines bootstrap → run with limited info
  (settings.json inventory + tool-failures cross-ref only)
- launchctl/cron not available → skip schedule-aware checks

## Memory Hooks

- Read prior reports to surface trend (hook X latency rising week over week)
- Write the report as the primary output
