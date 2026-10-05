---
name: tg-check
description: >-
  Self-test both Telegram rails on this machine, the MCP connector and the userbot library, with
  a deterministic zero-token detector plus a real in-session MCP probe, and print a per-rail
  verdict with the exact fix for whichever is down. Triggers: "/tg-check", "are both tg rails
  up", "check telegram channels".
license: MIT
---

# /tg-check — both Telegram rails on THIS machine

The operator's order (2026-06-27): "every computer checks whether BOTH of its Telegram rails work — MCP and telethon."
A local self-test: **this** computer checks **its own** two Telegram rails. Not to be confused with the
hub-only `connector-health-daily` (centralized). The root canon = the house rule
`reglament-shina-telegram-bez-mcp-i-svoya-sessiya-na-mashinu`.

## Why two steps (this matters, don't shortcut it)
- **The telethon rail** is checked DETERMINISTICALLY and SAFELY (a shared lock `_refresh_work_acct_a.lock` → no `AUTH_KEY_DUPLICATED`).
- **MCP cannot honestly be checked by a script** — it is a harness stdio server, reachable only by the LLM inside a session.
  The script gives the best deterministic signal (is the process alive? a fresh fatal in the log?), while the REAL
  MCP verdict comes from THIS skill — probing the tool inside the session. Memory `mcp-health-check`:
  NEVER spin up a second Telethon client as a health check (AUTH_KEY_DUPLICATED).

## Step 1 — the deterministic detector (0 tokens)
```bash
PYTHONIOENCODING=utf-8 python "$USERPROFILE/.claude/scripts/tg_channels_check.py"
```
Prints the per-machine matrix: MCP (by process + the tail of `mcp_errors.log` — a fresh `AuthKeyDuplicated`
= the RED root cause; `TypeNotFound` = an outdated telethon) and the telethon rail (GREEN/RED via
`tg_bus_read.py --check`). Exit 1 = something is RED. Flags: `--json`, `--notify` (pings the bus on RED).

## Step 2 — the REAL in-session MCP test (this decides the MCP verdict)
- **Are the Telegram MCP tools present in this session at all?** If `mcp__telegram__*` are NOT loaded
  (absent from the tool list / ToolSearch cannot find them) → MCP is **RED: not loaded into the session**.
- If they are — call ONE cheap read tool: `mcp__telegram__list_accounts` (or `get_me`, expecting the
  work account). Answered without an error → MCP is **GREEN**. An error (AuthKeyDuplicated / timeout) →
  **RED** + the reason from the error.
- ⚠️ Exactly ONE cheap call. Don't call `get_history`/`search_dialogs` (heavy → they can take the MCP down).

## Step 3 — merge and report (a 🟢/🔴 matrix)
Merge the detector (Step 1) with the live MCP probe (Step 2) into a single per-machine verdict:
```
=== Telegram: both rails @ <machine> ===
🟢/🔴  MCP (chigwell)  : <the Step 2 verdict — it wins> — <reason>
🟢/🔴  telethon rail    : <the Step 1 verdict>
```
- The Step 2 verdict (live) BEATS the Step 1 detector (indirect) — the log can lag behind.
- On RED — hand over the runbook (below). Both 🟢 — a single line: "both rails alive".

## The RED runbook (from the house rules)
- **MCP RED + `AuthKeyDuplicated`** → ROOT CAUSE: one TG session used on 2+ machines. The band-aid is to restart
  Claude Code (the harness brings MCP back up; it will hit the same root cause again). The durable fix is that every
  machine has ITS OWN TG session (Rule B in the house rules) — coordinated by the hub, the operator logs in locally.
- **MCP RED + `TypeNotFound`** → an outdated telethon in `<TELEGRAM_MCP_DIR>\.venv` → update it.
- **MCP "not loaded into the session"** → restart Claude Code (or open a session that loads MCP).
- **The telethon rail RED** → a missing/broken `REFRESH_*` in `$IMPORTS_ROOT/dialogs/.env` on this machine,
  or the group is unreachable → check the `.env` / access to the group `<YOUR_CHAT_ID>`.
- **The bus still works over the rail** (if it is 🟢): `tg_bus_read.py` / `tg_bus_send.py` — no MCP needed.

## Turn it into a routine? (offer it, don't impose — the "recurring → routine" rule)
If the operator wants EVERY computer to watch both rails itself — set up a nightly task (window
23:00-06:00 local) running `python tg_channels_check.py --notify` on each machine: silent when green,
a bus/Saved ping on RED. That is a local watchdog (deterministic, no LLM); the hub watchdog
`connector-health-daily` stays centralized. The operator decides.

## Boundaries
- Read/diagnose only. Reconnecting MCP = restarting Claude Code (a stdio MCP cannot be raised from inside a session).
- Splitting TG sessions across machines is a multi-machine change (Tier-2) → coordinate with the hub.
- Canon: the house rule `reglament-shina-telegram-bez-mcp-i-svoya-sessiya-na-mashinu`, memory
  `machine-bus-telegram-rail`, `connector-health-watchdog`, `mcp-health-check`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
