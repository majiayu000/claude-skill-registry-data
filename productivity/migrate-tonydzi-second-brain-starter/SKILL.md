---
name: migrate
description: >-
  Move or sync the hub role of an agent-plus-vault setup between computers, where an always-on
  desktop is the hub and laptops are satellites. Checklist with counters verified before and
  after, and it never migrates silently. Triggers: "/migrate", "/migrate check", "/migrate
  pack", "/migrate bootstrap".
license: MIT
---

# /migrate — seamless Claude across Anton's machines

> 🧒 When reporting to Anton end with a child-simple "In plain words" recap. (memory `eli5-always`)

This is the **single command** over the migration project that several sessions already built. It does NOT redesign anything — it reads `MIGRATION-PLAN.md` + the `migration-prep\*` scripts and runs the right one. Full state + decisions = memory [[machine-migration]] (READ it first each run — the project is live and moves fast).

**The shape (decided, do not re-litigate):** always-on Windows **DESKTOP = HUB** (vault + automation + RAG); this laptop + Mac Studio + MacBook = **satellites**. Transport: small CONFIG → git/private GitHub; huge live VAULT → **Syncthing star** (Introducer OFF, `.git` hub-only). "Seamless" = same vault + same `~/.claude` config + same memory on every machine, NOT teleporting the live chat.

**Working dir:** `$USERPROFILE/!CLAUDE-HP17 May26\` · scripts under `migration-prep\` · config repo `$USERPROFILE/.claude/_config-backup/`.

## Modes

- **`check` (default, read-only)** — status + drift. Report: is `_config-backup` fresh (working tree clean vs HEAD; run `config_sync.ps1` if skills/memory changed since)? how many Windows scheduled tasks now vs the 16 captured in `migration-prep\tasks\*.xml` (drift = re-export before a move)? is the F:\ chemodan stale? is `gh` logged in (offsite optional)? Surface what's BLOCKED.
- **`pack`** — refresh the carry-kit right before an actual move (snapshots go stale): `powershell migration-prep\config_sync.ps1` (config+memory → repo) then `powershell migration-prep\build_chemodan.ps1` (→ `<MIGRATION_DRIVE>\`, robocopy COPY-only). Re-export tasks if drifted. ⚠️ confirm with Anton before writing F:\ (it's the seed drive).
- **`bootstrap`** — on a NEW machine: read & execute `_config-backup\BOOTSTRAP-NEW-MACHINE.md` (ordered A→G) or `migration-prep\NEW-SESSION-RUNME.md`. New machine user = **Anton** (`%WORKDIR%`) → every `%USERPROFILE%\` path needs `_→Anton`; memory encoded-path + task XML absolute paths need the rename too. **MANDATORY config-safety step:** run `powershell "$env:USERPROFILE\.claude\scripts\claude_git_backup_setup.ps1"` (idempotent — git-inits the `~/.claude` config repos + sets a global git identity) THEN ensure the 15-min "Claude Config Git Snapshot" task exists. Without the init, the snapshot task commits NOTHING (the 2026-06-24 hub near-loss). Canon: [[claude-skills-git-backup]] + [[config-safety-backup-and-migration-check]].
- **`connectors`** — reconnect external MCPs after a move via `migration-prep\CONNECTORS-INVENTORY.md`. The 3 blind spots the vault+config backup MISSES: `<TELEGRAM_MCP_DIR>\` (.env + patched source), `$USERPROFILE/.claude/secrets/` (n8n.env + SSH key), `$USERPROFILE/.local/share/whatsapp-mcp/`. Enumerate from `.claude.json` mcpServers, not the backup. After reconnecting, verify each server is actually alive & authed with the **`/mcp`** skill (its in-session health check — and it carries the Telegram AUTH_KEY_DUPLICATED landmine that bites right after a move: re-auth per machine, never copy `.claude.json`).
- **`sync`** — Syncthing setup/repair via `migration-prep\SETUP-SYNC.md`. First-sync order is CRITICAL: laptop is most-current → laptop = Send&Receive, desktop = Receive-Only on first pass to ABSORB, THEN flip. Laptop Device ID is in [[machine-migration]]. Same Syncthing pipe also carries the cross-machine RELAY — Claude-to-Claude messages between machines (folder `$OBSIDIAN_VAULT/_machine-bus/`); that is the **`/inbox`** skill's job, NOT `/migrate` (rule lives in [[reglament-multi-machine-claude-i-peredacha-mezhdu-mashinami]]).

## Hard "never" (safety invariants)
- **NEVER copy `$USERPROFILE/.claude.json`** to another machine (Telegram MCP session) → AUTH_KEY_DUPLICATED logs the account out. Re-auth per machine.
- **NEVER start a 2nd MCP client** on the same StringSession (see [[mcp-health-check]]).
- `_originals` (3.75 GB) is **SACRED** — send-only from hub, never delete.
- All migration `.ps1` are **ASCII-only** (PowerShell 5.1 mangles Cyrillic — [[deterministic-script-gotchas]]).
- Writes to F:\ / pushing the repo / registering tasks on a new box = pause + confirm (Tier-2, [[operating-agreement]]).

## Output
One-liner status + what's fresh/stale/blocked + the exact next command. Then 🧒 recap. Don't duplicate logic that lives in the scripts — point at them.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
