---
name: reboot
description: >-
  Reboot a fleet node safely by one protocol: pre-flight (save state, finish syncing, warn
  peers, verify autostart is armed), then a full restart rather than a fast-startup hybrid, then
  a post-reboot check through the crash-recovery skill. Triggers: "/reboot", "restart this
  machine".
license: MIT
---

# /reboot — a controlled restart of a fleet node

**The pain:** rebooting blind = a lost unsynced file (sync-conflict), a false SEV1 alarm from the
peer watchdogs ("the node is dead!"), a robot that never came back after boot, and — as with the
HP Wolf driver on 2026-07-24 — "I rebooted and the driver is still in memory", because Fast Startup
does not clear RAM on an ordinary shutdown.

Reboot ONLY when: (a) there is a reason (evict a hook/driver from RAM, apply an update, unstick
something), and (b) autostart is armed → the machine will come back on its own.

## STEP 1 — PRE-FLIGHT (before the reboot, in order)

1. **Reason + confirmation.** One line: why the reboot and what it fixes. If it is risky
   (away-mode, a machine without auto-login, FileVault/BitLocker with a manual password at boot) → ask the operator first.
2. **Save state.** The TurnState black box writes on every turn by itself (it survives the reboot → /1 will bring it back).
   Any active uncommitted work in code or the vault → commit/save it now.
3. **Finish the Syncthing sync** (otherwise: loss/conflict). Wait for `need=0` on every share:
   ```bash
   powershell -NoProfile -ExecutionPolicy Bypass -File "$IMPORTS_ROOT/sync_check/sync_check.ps1"
   ```
   need>0 → wait for the sync / raise it (`/raise-sync`); do NOT reboot with a pending need.
4. **Warn the peers** (otherwise the observers raise a false offline SEV1) — into the bus + the fleet log chat, BEFORE the reboot:
   ```bash
   python "$HOME/.claude/scripts/bus_send.py" --text "🔁 <host> going down for a reboot (~N min), reason: <...>. I'll come back on my own."
   ```
5. **Verify autostart is armed** (the machine must come back WITHOUT hands):
   - **PC:** Claude Desktop = a single launcher `%APPDATA%\...\Startup\Claude-Autostart.lnk`
     (`shell:AppsFolder\Claude_pzs8sxrjxfjjc!Claude`), NOT a broken HKCU\Run pointing at an old version
     ([[claude-desktop-autostart-race]]); Syncthing = `start-syncthing.vbs` in Startup; the watchdog tasks in place.
     On the hub, also auto-login + `hub_boot_report.py` ([[hub-boot-selfreport]]).
   - **Mac:** Login Items / launchd agents for Syncthing + Claude; a FileVault password at boot is manual
     (without it an unattended reboot will not come back — only do it with a human present).

## STEP 2 — THE REBOOT (with the right command)

⚠️ **A FULL Restart, not a Shutdown** — Fast Startup (hiberboot) on Windows does NOT clear the
kernel/drivers/RAM on `shutdown /s`; `Restart` (`/r`) always does a full cycle and clears them. To
"evict a driver/hook from memory" (HP Wolf, an antivirus, a stuck driver) ONLY a full Restart works.

- **PC (Windows):**
  ```bash
  shutdown /r /t 0
  ```
  (a guaranteed clean exit even with Fast Startup ON; the Claude Code session ends with it).
- **Mac:**
  ```bash
  osascript -e 'tell app "System Events" to restart'   # or: sudo shutdown -r now
  ```

## STEP 3 — POST-REBOOT (once it's up — through /1)

The machine is back → in a new session run **`/1`** (resurrection): RECALL from the black box + a
health ping (arch/sync/mcp) + the previous session's full history into the buffer. Then:
- Confirm autostart fired: Syncthing connected, Claude Desktop = a single instance (no race),
  connectors green.
- **Check that the reason for the reboot was actually achieved** (e.g. the black windows are gone /
  the driver is no longer in memory) — by looking or measuring, not on faith ([[prichina-kak-claim]]).
- A boot self-report into the bus (the hub does it itself; on a peer — a short "✅ <host> is back, all green").

## Boundaries
- READ-only right up to the reboot itself; the reboot is a deliberate action with a stated reason.
- ⛔ Away-mode / no auto-login / a manual FileVault-BitLocker prompt at boot → reboot only with the operator's approval
  (risk: it never comes back without hands).
- A peer reboots ITSELF ([[peers-own-outbound-local-full-member]]); rebooting the hub while away — carefully
  ([[away-mode-45-days]], BIOS "Restore on AC Power Loss").
- The folder name is `reboot`; `/restart` is a text trigger for the same skill (case does not matter).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
