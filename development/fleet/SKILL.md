---
name: fleet
description: >-
  Show what the background agents across every machine are doing right now, what they have built
  or committed, and whether anything is stuck or burning tokens. Read-only diagnostic. Triggers:
  "/fleet", "what are my agents doing", "is anything stuck".
license: MIT
---

# /fleet — what are my background agents doing?

> 🧒 **When reporting to a non-technical operator:** end with a child-simple "In plain words" recap in their language. (memory `eli5-always`)

The operator runs an autonomous fleet (Claude Desktop "Cowork" app → many headless `claude.exe` Code agents) building their Second Brain in the background. This answers: how many, what they're building, anything stuck/looping/burning. **READ-ONLY — never kill a process without the operator's explicit go** (killing mid-write loses uncommitted work; git holds only committed state).

## 🖥️ Dashboard first (the operator works visually)
`python "$IMPORTS_ROOT/build_fleet_dashboard.py"` → open `$OBSIDIAN_VAULT/_Dashboards/Fleet-Dashboard.html`: KPIs (agents / masters / files in flight / work commits / MCP) + a health flag 🟢/🟡/🔴 + a commit feed (real work vs auto-backups) + what is being written right now. READ-ONLY. The text below is for digging by hand.

## Recipe (all read-only)
1. **Who's running + the master:**
   ```powershell
   $cl = Get-CimInstance Win32_Process -Filter "Name='claude.exe'"
   "claude agents: $($cl.Count)"
   $cl.ParentProcessId | Sort-Object -Unique | ForEach-Object { $p = Get-CimInstance Win32_Process -Filter ("ProcessId="+$_) -EA SilentlyContinue; if ($p) { "parent $_ = $($p.Name) | $($p.CommandLine.Substring(0,[Math]::Min(80,$p.CommandLine.Length)))" } }
   ```
   Many children sharing ONE `Claude.exe` parent = the Desktop "Cowork" master; an `explorer.exe` grandparent = the operator launched it from the GUI.
2. **What they built (committed):** `git -C "$OBSIDIAN_VAULT" log -20 --pretty="%cr | %s"` — DESCRIPTIVE messages are the fleet's work; terse `pre-intervention` are auto-backups. Group by theme.
3. **Writing right now:** `git -C "$OBSIDIAN_VAULT" status --short` → count = files in flight this second (re-run after ~30s; growing = actively writing).
4. **New reusable artifacts:** `python "$IMPORTS_ROOT/retro_inventory.py" 1` → read its digest (new skills/scripts/notes).
5. **MCP load (optional):** count `python.exe … telegram-mcp … main.py` processes (~2 per agent) — high = many live sessions eating memory.
6. **Collision lens — who's in which FILE right now (`session_monitor.py`, merged in here 2026-06-13):** `python "$USERPROFILE/!CLAUDE-HP17 May26\session_monitor.py"` (snapshot) · `--watch` (live terminal) · `--serve` → http://127.0.0.1:8765 (browser, auto-refresh). Parses the session `.jsonl` logs for file-level touches and flags **⚠️ COLLISIONS** (one file edited by 2+ sessions within 15 min) + hot files. Steps 1–5 answer *"what are they building / stuck / burning"*; this answers *"are any about to overwrite each other"*. **Run it before any structural / bulk vault edit when sessions run hot.** Same fleet, two lenses — `/fleet` is the front door. (memory `session-monitor`)

## Flags to surface
- 🟢 healthy = commits advancing through DIFFERENT real themes over time.
- 🟡 stuck/looping = many agents but no NEW descriptive commits for a long stretch, or the same commit message repeating.
- 🔴 burn = dozens of lingering agents / MCP procs with no progress → tell the operator; HE decides whether to stop the Desktop app (you don't kill it).

## Output
Tight one-liner + detail: "N agents (master PID …) · building: <themes> · writing now: <k> files · flags: 🟢/🟡/🔴 …". Then 🧒 recap. If you spotted something durable they built that isn't captured, mention it (or note `/retro` / the daily sweep will catch it).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
