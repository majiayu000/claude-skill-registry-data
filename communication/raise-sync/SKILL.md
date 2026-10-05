---
name: raise-sync
description: >-
  Recover a fleet whose machines cannot see each other over the file-sync network: establish
  ground truth at the hub from the live sync API rather than memory or one peer's claim, publish
  the hub's verified device id over the messaging rail, and walk each disconnected peer through
  re-pairing. Triggers: "/raise-sync", "sync is down", "machines cannot see each other".
license: MIT
---

# /raise-sync — raise the sync when machines can't see each other

An active runbook for the "sync lost" incident (full canon + the why = the house rule [[reglament-chp-poterya-sinka-mezhdu-mashinami]]). The principle: **ground truth comes from the hub's LIVE API, never from memory and never from one peer's claim** (a peer can be holding a stale record — that is how the laptop once confidently insisted "restore 2KPYBY4", which would have broken the peer that was already working).

The messaging account/group and the API key come from `~/.claude/tg_bus.json` (Telegram) and the env var `STGUIAPIKEY` (Syncthing API). Hub on the LAN = `10.0.0.10:22000`.

## Step 0 — Detect (where does it hurt)
```bash
APIKEY=$(powershell -NoProfile -Command "[Environment]::GetEnvironmentVariable('STGUIAPIKEY','User')" | tr -d '\r')
curl -s -H "X-API-Key: $APIKEY" "http://127.0.0.1:8384/rest/system/connections" | python -c "import sys,json;d=json.load(sys.stdin);[print(k[:7], v.get('connected'), v.get('address')) for k,v in d.get('connections',{}).items()]"
```
(Or the quick red/green view — the `/sync-check` skill.) Anyone with `connected:false` has dropped off.

## Step 1 — Ground truth AT THE HUB (facts, not memory)
```bash
# the hub's myID (must match machines.json HUB-1 = EEAETB6...)
curl -s -H "X-API-Key: $APIKEY" "http://127.0.0.1:8384/rest/system/status" | python -c "import sys,json;print('myID=',json.load(sys.stdin)['myID'])"
# is the daemon serving the REAL vault? (paths under %VAULT_ROOT%\..., data present)
curl -s -H "X-API-Key: $APIKEY" "http://127.0.0.1:8384/rest/config/folders" | python -c "import sys,json;[print(f['id'],'->',f['path']) for f in json.load(sys.stdin)]"
```
- If `myID` does NOT match the registry / the folders are empty → the daemon came up on the WRONG home: **fix the home (the one with the native cert.pem + the folders), do NOT re-pair the peers onto a temporary ID.**
- If `myID` matches and the folders are real → the identity is legitimate and the problem is on the peers' side (a stale hub record).

## Step 2 — Compare against the registry (drift detection)
Compare the live `myID` with `_machine-bus/machines.json` (the hub's `deviceID` field). A mismatch with no explicit migration = suspicion; a match = publish it as canon.

## Step 3 — Publish the hub's VERIFIED device ID onto the bus (out-of-band proof)
Via the Telegram MCP (`chat_id`/`account` from `tg_bus.json`):
```
🤖 [<hub> -> ALL] hub <name> = <EEAETB6-full-ID>, addr tcp://10.0.0.10:22000. VERIFIED against the live API (it serves the whole vault). Peers: write this ID in, delete the stale one, restart the daemon, report connected.
```
This clears the peer's Tier-2 gate ("writing in someone else's ID = handing over the vault") — the peer now has proof from the hub itself.

## Step 4 — Walk the peers through it (they fix it locally; I cannot reconfigure someone else's Syncthing)
For each disconnected peer: write the hub in as the verified ID, with the correct address, **delete the stale ID** (a common pitfall — a phantom old entry gives "Hello → forcibly closed / unknown device"), restart the daemon through the standard watchdog → report `🤖 [peer -> hub] connected`, or what is blocking it.

## Step 5 — Verify
Repeat Step 0: everyone `connected:true`, the backlog draining (`needFiles` going down). Report the roster to the operator.

## Anti-pitfalls (learned the hard way, 2026-06)
- Do NOT trust ONE peer's diagnosis of identity — the source of truth is the hub's live API.
- Do NOT roll the hub back to an old ID if another peer is already working on the new one (you will break the peer that works).
- A watchdog that "hangs" → check the visibility layer first (logs/key/403), not the core.

## Related
- `/sync-check` — read-only status (detection). This skill is RECOVERY.
- The dead-man switch `sync_monitor.py` (the "Claude Sync Monitor" task) pings the operator when a peer drops → `/raise-sync` often starts FROM that ping.
- Canon: [[reglament-chp-poterya-sinka-mezhdu-mashinami]], [[machine-bus-telegram-rail]], [[syncthing-v21-gotchas]].


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
