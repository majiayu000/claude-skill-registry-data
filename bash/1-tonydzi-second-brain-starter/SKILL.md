---
name: "1"
description: >-
  Recover a session after a hard crash (app died, machine rebooted, context lost mid-work):
  replay the turn-state ledger for the last requests, files and decisions, run a green/red
  health ping over the system map, file sync and MCP connectors, then rebuild the previous
  session history for pickup. Triggers: "/1", "resume after crash", "wake".
license: MIT
---

# /1 — resurrection after a crash ("where were we + is everything working")

**The operator's pain:** the session died mid-work (a crash / the computer went off) → the new session is empty. Before: remember by hand, then separately fire `/arch`, `/sync-check`, `/mcp`, then work out "where did we stop". Now it is one word: `/1` (or `/!`).

**What this is NOT:** `/retro` is for a CLEAN end of session (inventory of what was built → routing to homes → /compact). After a sudden crash there is nothing left to package, the context is already gone → you need resurrection, NOT `/retro`. Two different tools.

## 3 steps (run them in order, report as one panel)

### Step 1 — RECALL: where we were (0 tokens, deterministic)
The TurnState black box writes EVERY turn into SQLite (a Stop hook), and it survives any crash. Read the last turns:
```bash
python "$IMPORTS_ROOT/turnstate/turnstate_show.py" --n 12
```
From the output pull out: what the operator asked for last · which files were touched · which DECISIONS were made · the next step. That is "where we were cut off". (Flags: `--stats`, `--session <id>`, `--n N`.)

**⚠️ Fallback if the box is EMPTY** (`turnstate_show.py --stats` shows `turns: 0` — it happens when the Stop hook hasn't fired yet after a Claude Code restart; see [[crash-recovery-command]]): do NOT say "there is no data". Derive "where we were" from the LAST session — its full seed is already assembled in step 3 (`_Dashboards/sessions-md/_continue/<cli>.seed.md`): read the TAIL of that file (the last 1-2 human→assistant exchanges) and pull the task plus the last step out of them. So with an empty box, step 1 leans on the result of step 3.

### Step 2 — HEALTH PING: is everything alive (green/red)
Three fast deterministic checks:
```bash
python "$IMPORTS_ROOT/arch/arch_status.py"
powershell -NoProfile -ExecutionPolicy Bypass -File "$IMPORTS_ROOT/sync_check\sync_check.ps1"
```
**MCP — IN-SESSION ONLY** (⚠️ NOT `claude mcp list` and NOT a second Telethon client → `AUTH_KEY_DUPLICATED` logs the account out; memory [[mcp-health-check]]): fire one cheap read call per live server — Telegram `mcp__telegram__get_me` (expect the work account), WhatsApp `mcp__whatsapp__get_my_profile`, n8n `mcp__n8n__n8n_health_check`. If a server's tools are missing from the session, it never loaded (diagnostics live in `/mcp`).

### Step 3 — FULL PICKUP: the whole history into the clipboard
Assemble this machine's previous human session into a seed → the clipboard (the `/resume-last` engine):
```bash
python "$IMPORTS_ROOT/claude_sessions/continue_session.py" --last
```
Tell the operator: **"Open a New session and hit Ctrl+V — you get the whole conversation back."** If it prints `clipboard: FAILED`, the seed is on disk at `_Dashboards/sessions-md/_continue/<cli>.seed.md`.

## What to reply with (one panel + 🧒)
```
🔄 Resurrection
📍 Where we were: <1-2 lines from TurnState — the task, the last file/decision, the next step>
💚 System: arch <✅/⚠️/🔴> · sync <✅/⚠️/🔴> · mcp <tg ✅ / wa ✅ / n8n ✅>
📋 The previous session's full history is in the clipboard (New session → Ctrl+V).
➤ Continue from: <the next step>?
```
Then a 🧒 "In plain words" line (memory [[eli5-always]]).

## Boundaries
- **READ-ONLY.** It sends nothing, edits no live data, and does not repair sync/MCP — it only READS the black box and the status scripts, and writes a seed file + the clipboard. Fixing a red light is `/arch` / `/sync-check` / `/mcp` separately.
- The skill's name is `1`, so `/1` works natively; `/!` is an alias trigger (a special character can't be a folder name): when you see `/!`, run this same skill.
- On Macs: `python3`; with a non-standard vault path — env `CLAUDE_VAULT_ROOT=<...>`.

## Canon
Memory [[crash-recovery-command]]. Building blocks: [[turnstate-ledger]] (the black box), [[claude-desktop-sessions-per-account]] (continue_session), [[system-architect]] (/arch), `syncthing-desktop-laptop-sync` (/sync-check), [[mcp-health-check]] (/mcp). Paired with the SessionStart hook `session_resume_hook` (that one shows the previous session at startup on its own — this one gathers recall + health + full history on command).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
