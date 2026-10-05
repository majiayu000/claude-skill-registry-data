---
name: follower-onboard
description: >-
  Onboard a new machine as a receive-only follower on a multi-machine agent network: it reads
  the shared vault, canon, skills and memory, runs nothing heavy locally (no RAG, reindex or
  GPU), and never receives executable hooks from the hub. Checklist-driven, with a verify step
  at each stage. Triggers: "/follower-onboard <machine>".
license: MIT
---

# /follower-onboard <name> — connect a follower-consumer (v1 data-only)

> 🧒 When reporting to the operator, end with a child-simple "In plain words" recap (memory `eli5-always`). Reports TO the operator only — never inside the package files.

**Single command** to build + deliver a follower onboarding package. Drives the tested generator over the master template. Full state + every decision + the gotchas = memory [[machine-migration]] (**READ it first each run** — the project is live, this is where the hard-won traps live).

## The v1 shape (decided 2026-06-24, do NOT re-litigate)
A follower = **a reading room for data**. The hub SYNCS DATA the follower READS; it NEVER pushes executable code.

| Folder | Follower-side type | Why |
|---|---|---|
| `Owner-Knowledge` (vault, Bible) | **Receive-Only** | reads the Second Brain |
| `claude-home` (CLAUDE.md + commands) | **Receive-Only** | the canon — whitelist `.stignore` blocks `hooks`/secrets/scripts |
| `claude-memory` | **Receive-Only** | "one shared memory" |
| `claude-imports` | **Receive-Only** | scripts (code only, big data ignored) |
| `claude-skills` | **Receive-Only** | uses all skills |
| `_machine-bus` | sendreceive (tiny, versioned) | the ONLY 2-way folder (mailbox) |

**ALL data folders RECEIVE-ONLY (skills too).** A sendreceive skills/vault share from a follower is a DATA-LOSS VECTOR — a follower's empty folder can propagate deletions cluster-wide (it wiped the hub's skills 2026-06-24). Contributions (skills + vault notes) go via the **moderated `_transit` channel** (`vault-proposals/<name>/`, `canon-proposals/`), hub folds them in — NOT direct sync.

**NO hub-pushed hooks / settings.json in v1.** A follower's stock Claude CORRECTLY refuses to let a remote machine push executable `hooks/**` (a backdoor); a pasted "authorization" is not sufficient proof. So the hub pushes **zero remote-exec**. **The inbox-robot is the one exception BY KIND — MANDATORY on every machine (operator's order, 2026-06-25), but installed LOCALLY by the follower's own Claude with the operator's explicit consent.** A local scheduled task the operator sets up ≠ a hub push, so it is NOT the backdoor the no-hooks rule blocks. It rides the `_machine-bus` (the only sendreceive folder). Install via bootstrap STEP 8/9 (`INBOX-ROBOT-LAUNCHER.md` in `_transit`). The v1/v2 axis is about DATA-scope (v2 adds the Telegram-leads connector), NOT about the robot — the robot is baseline-mandatory, orthogonal to v1/v2.

## Step 0 — CONSENT + QUICK WIN + PITCH (before any technical step; house rule reglament-onboarding-pitch-vtoroy-mozg)
The order: (1) a mini-consent of 4 questions (what · where · who can see it · how to delete it); (2) a quick win on the user's real life — save one useful thing and show it coming back; (3) a 7-point pitch in plain words; (4) the first save with a receipt. In the follower's intro CLAUDE.md, add the operational block "keeper of memory" + a memory check at the end of the session (wording lives in the house rule). At the 1-2 week check-in, look for 3 activation signals; zero signals → the pitch did not land, repeat it through a new quick win. Canon: `reglament-onboarding-pitch-vtoroy-mozg`.

## Step 1 — RECALL (don't duplicate)
Read memory [[machine-migration]] §FOLLOWER-LITE + §v1 DATA-ONLY + the SKILLS-WIPE incident. Confirm the hub's safety nets are still on (see Step 6).

## Step 2 — The operator's name in all grammatical forms + Latin
The generator swaps the template operator name for the target one across every declension of the local language, including **all-caps forms in non-Latin scripts** (a case-insensitive grep cannot fold those). Supply the Latin spelling plus each inflected form the language needs; if the name does not inflect, pass the same form for each. Unsure about the forms → ask the operator.

## Step 3 — Generate
```bash
python "%WORKDIR%\migration-prep\gen_follower_package.py" \
  --latin <Latin> --nom <form1> --gen <form2> --dat <form3> --acc <form4> --ins <form5>
```
Writes `migration-prep\<latin>-follower\`, verifies 0 residual leaks (Unicode-correct, ABORTS on any), builds the zip, creates `vault-proposals\<latin>\`. Hand the operator the **v1 data-only Windows/Mac bootstrap** (`BOOTSTRAP-PROMPT-<NAME>-v1-data.md`) — the autonomous prompt their Claude runs. Also bundle `follower-kit-v1\syncthing_follower_watchdog.ps1` + `install_follower_watchdog.ps1`.

## Step 3b — ⭐ A PERSONAL KIT instead of handing over the owner's CLAUDE.md (2026-07-27)
⛔ Never give a new person the owner's personal `CLAUDE.md`: it carries his paths to secrets, his chat IDs, the layout of his personal disks, and ~90% of the rules are not about this person at all (verified: 22 hits from the leak scan).
Build a kit along two axes instead — person × node:
```bash
python ~/.claude/scripts/persona_build.py --person <key> --node <node code>
```
- Add a new person to `~/.claude/canon/people.json` first (copy the `_template` block; the `may_*` permissions are strictly `true/false`, with the reasoning in `<field>_note`).
- Add a new node to `~/.claude/canon/node_caps.json` (copy `_template`); an unknown node gets `_default` = minimum rights.
- The builder blocks delivery on its own if the safety floor is incomplete or anything personal leaked through; check a finished kit with `--check <folder>` (exit 0 = good, 2 = only half of it was checked).
- The shared law (`canon/CORE.md` + `canon/FLOOR.md`) is byte-identical everywhere — only the owner edits it, and it is receive-only on followers.

## Step 4 — Deliver
**⚠️ NOT via Gmail** — Gmail scans archives and BLOCKS scripts (`.ps1`/`.py`) → the whole email bounces (caught 2026-06-24). **Use Telegram `send_file`** or `SendUserFile`. Caption: "paste BOOTSTRAP-...-v1-data.md into your Claude Code, one message."

## Step 5 — Hub-side share (REST works; on-disk key `hWPF…` in `config.xml`)
Add the follower device + share the 6 folders. Auto-discovery (`/rest/cluster/pending`) is **404 in Syncthing v2.1.1** → instead read `DeviceRejected` events to find a follower's DeviceID. **Use the follower's CURRENT device ID** (it changes after a Syncthing reinstall — a "one folder empty, others fine" symptom = device-ID drift on THAT share).

## Step 6 — Safety nets (verify ON before any follower joins)
- **Syncthing versioning** on every synced folder (skills=simple keep10, memory=trashcan, vault=staggered, home/imports=trashcan) → deletions recoverable from `.stversions`.
- **git backup INITIALIZED + committing** — FIRST run `powershell "$env:USERPROFILE\.claude\scripts\claude_git_backup_setup.ps1"` (idempotent: git-inits skills/memory/scheduled-tasks/_config-backup/scripts/hooks + sets a per-repo identity + a global git identity). **This is mandatory: a present-but-inert "Claude Config Git Snapshot" task commits NOTHING if the repos were never `git init`-ed — exactly how the hub sat unprotected until the 2026-06-24 skills wipe (only a stale manual mirror saved it).** THEN verify the 15-min "Claude Config Git Snapshot" task exists and actually commits (path-agnostic `claude_git_snapshot.ps1`, uses `$env:USERPROFILE`). Canon: [[claude-skills-git-backup]] + [[config-safety-backup-and-migration-check]].
- Followers **Receive-Only** (Step shape) — the deletion vector removed.

## The follower-side GOTCHAS (from a real follower onboard, 2026-06-24 — put them in the bootstrap so they're handled)
1. **`.stfolder` marker missing** after changing a folder's path → create the marker dir + `POST /rest/db/scan`.
2. **Receive-only phantom deletions** — changing an RO folder to a new empty path marks files as "local deletions" and Syncthing STOPS pulling (`need=0`, `local=0`, `global>0`). Fix: `POST /rest/db/revert?folder=<id>` → discards phantom changes, re-pulls from hub.
3. **★ Sandbox-Syncthing eviction (the big one)** — every Claude Code restart launches a SANDBOXED Syncthing inside `…\Packages\Claude_*\LocalCache\Local\Syncthing\` with a sandbox config (no hub device, wrong REST key → CSRF + 0 connections). It grabs port 8384 and evicts the correct daemon → sync silently stalls. **Fix = the follower watchdog** (`follower-kit-v1\syncthing_follower_watchdog.ps1` + `install_follower_watchdog.ps1`): every 10 min it checks REST-key + hub-connected; if wrong/dead, kills all syncthing.exe and relaunches with explicit `--home=%LOCALAPPDATA%\Syncthing`. INSTALL IT as part of every follower onboard.
4. **Battery-friendly scheduled tasks** — on a laptop a task without `-AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable` sits `State=Queued` and never runs. The install script already sets these.
5. **session_archive on RO-vault follower** — its default catalog path is inside the (RO) vault → won't sync up. Run with `SESSION_ARCHIVE_OUT=<synced-bus>\_session-archive-inbound\<machine>`.

## Step 6b — Tailscale join (MANDATORY for EVERY peer; gap caught 2026-07-16)
Every peer in the fleet must be on the tailnet (owner = owner.calendar@example.com, login = Google SSO). Without it there is no direct access (SSH/RDP to the hub are open ONLY from 100.64.0.0/10) — Syncthing and the messaging bus work without the tailnet, so the hole is NOT visible in day-to-day work (that is how one Mac lived off-network unnoticed until 2026-07-16). Steps: (1) install Tailscale (Windows: winget/installer; Mac: .pkg — ⚠️ needs the operator's admin password/Touch ID, a headless session will stall — ask for the operator's hands IMMEDIATELY, not at the end); (2) `tailscale up` → Google SSO as the owner account (password in the secrets store); (3) verify FROM THE HUB: `tailscale status` shows the node. The registry of expected nodes = `~/.claude/scripts/tailnet_expected.json` (hub) — ADD the new node there; the nightly watchdog `tailnet_guard.py` shouts into the bus about missing ones. Canon: memory [[all-peers-in-tailnet]].

## Step 7 — Register + report
- `_machine-bus\machines.json` (role `follower-consumer`), memory `user-registry` + `session-machine-tagging` (+ per-machine default operator, see the house rule reglament-pomechat-mashinu §default operator PER MACHINE).
- Report to the operator post-hoc (what onboarded, what's pending).

## Hard "never"
NEVER ship `claude-secrets`/`claude-config`/`.claude.json`/connectors. Canon never edited by followers → `canon-proposals\`. Vault never directly written by followers → `vault-proposals\<name>\`. Headless `claude -p` on a follower = subscription/OAuth (`set "ANTHROPIC_API_KEY="`). `.ps1` ASCII-only (PS 5.1 mangles non-Latin scripts).

## Don't duplicate
`/migrate` = full HUB move (different job). `/inbox` = the bus the (mandatory, locally-installed) inbox-robot rides. One markdown procedure + one tested generator + the kit scripts — no server, no DB.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
