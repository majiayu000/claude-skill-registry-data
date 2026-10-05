---
name: sync-check
description: >-
  Report this machine's file-synchronization state with the whole fleet: peers connected,
  per-share state and files still needed, folder errors, and how many sync-conflict files piled
  up, which is the silent sign two machines are fighting over a file. Read-only and zero tokens.
  Triggers: "/sync-check", "is sync alive", "sync status".
license: MIT
---

# /sync-check — is the sync between my machines healthy

One command answers "did it arrive / are we syncing right now" across ALL Syncthing folders of this machine, without poking the REST API by hand. READ-ONLY, 0 tokens, portable (the API key is read from the local config → it works on any machine of the fleet).

**Engine:** `$IMPORTS_ROOT/sync_check/sync_check.ps1` (git-backed in `_imports`, synced through claude-imports). It now also includes **Device ID drift detection** (live `myID` vs `machines.json` → RED on a mismatch — it would have caught the 2026-06-25 incident).

**Cleaning up sync-conflict files** (when the report says "WARN sync-conflict files: N"): `python $IMPORTS_ROOT/sync_check/resolve_conflicts.py` (dry-run) → for each conflict it compares against the live file: `--quarantine` SAFELY moves conflicts of the live tree into `_sync-conflict-archive\<date>\` (a move, not a delete → recoverable; orphans with no live twin are left alone), `--apply` deletes only proven subsets. Already-archived files and `.stversions` are excluded. Canon: the sync-loss incident runbook, §6.

## Run
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$IMPORTS_ROOT/sync_check\sync_check.ps1"
```

## How to read the output
- **PEERS** — how many peers are connected. `0 connected` = sync is DEAD (the machine slept / Syncthing is stuck) → start the watchdog `syncthing_watchdog.ps1` (see the migration runbook, the on-wake task `SyncthingWatchdogOnWake`).
- **per folder** `OK / WARN / RED`:
  - `OK` + `NEED=0` = the folder is in sync, everything arrived.
  - `WARN` + `NEED>0` = still downloading (fine briefly; if it is stuck, look at the peers).
  - `RED` = `state=error` or folder errors → investigate (permissions / disk / conflict).
- **sync-conflict files** — a separate WARN (it does not turn the report RED). Their growth means two machines are editing the same file (e.g. `settings.json`) → decide "fresher beats older" (the operator decides) and clean up `*.sync-conflict-*`.
- **EXIT 0** = all green; **EXIT 2** = something is RED.

## When to call it
- The operator asks "did it reach the hub / the Mac?", "is sync alive?".
- BEFORE relying on a fresh file from another machine ("not found" ≠ "does not exist" — it may still be in transit; memory deterministic-script-gotchas).
- AFTER a sync incident (like the nested-folder D2 case of 2026-06-24/25) — to confirm the bridge is back.
- Each machine runs its own check (the report is local); to compare the whole fleet, ask every machine via `/inbox` or the bus.

## Boundaries
- Read-only: it fixes nothing and moves nothing. Healing a stuck sync is the watchdog's job (separate).
- It only sees what the local Syncthing daemon knows; if the daemon is not running it says so (RED).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
