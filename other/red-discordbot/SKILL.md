---
name: red-discordbot
description: "Install, host, manage, and author Red-DiscordBot cogs on your own Hermes VM with your own Discord token. Coexists with the Hermes gateway as a separate bot process. Covers the Python<3.12 requirement, the discord.py 2.7.x shutdown-crash patch, non-interactive instance setup, and safe token/collision handling. Use when standing up a Red instance alongside Hermes for community cogs (music, dice, polls, auto-mod)."
version: 1.0.0
author: Lumi (Lu) — derived from Narusya's package, corrected 2026-07-19
license: MIT
tags: [discord, bot, cog, red-discordbot, hosting, automation, community]
---

# Red-DiscordBot Hosting (own VM, own token)

## What This Is
Red-DiscordBot is a mature discord.py-based bot framework. Functionality ships as **cogs** (hot-reloadable Python packages): music, dice, polls, auto-mod, custom cogs. This skill is for **hosting your own Red instance on your own Hermes VM**, controlled by you — NOT sharing Hermes's token, NOT on someone else's box.

## Why Host Your Own (not share a token)
- **Agency:** you control the process, the cogs, the prefix.
- **Safety:** a separate Discord bot token means no shared-session/sharding-collision risk with the Hermes gateway or other bots (aether, etc.). The "shared-token sharding" model is fragile — chaotic relaunching can invalidate the Discord session and bounce the Hermes gateway. Own token = no collision.
- **Scope:** Red handles *community-function cogs* (music, dice, polls, auto-mod helpers). Hermes stays the *daemon/relationship* core. Don't re-implement Hermes's own powers as a cog.

## PRE-FLIGHT: verify VM health before mutating (user directive)
Before any install/build on the VM, confirm you will not hurt the host:
- Critical processes alive: `pgrep -af hermes | grep gateway` (gateway), `pgrep -af qdrant`, `pgrep -af camofox` (HTTP 200 on :9377).
  - NOTE: `pgrep -af "hermes_cli.main gateway run"` returned 0 even when gateway was alive — it runs as `hermes gateway`. Use the broader `pgrep -af hermes | grep gateway`.
- Disk: `df -h /` (Lu's VM: ~533G free — fine).
- RAM: `free -h` (Lu's VM: ~1.5G available — fine for install + dry-run; a live boot peaks ~1.8G).
- Only proceed if gateway/qdrant/camofox stay alive and disk/ram have headroom.

## Host Constraints
- Use **JSON backend** (zero-config, no DB server). **DO NOT install PostgreSQL** (eats RAM).
- On Lu's VM: disk is fine, RAM tight — watch `free -h`.

## CRITICAL: Python Version
Red 3.5.x requires `Python >=3.8.1,<3.12`.
- Lu's VM default `python3` = **3.12.3** → Red install REFUSES ("No matching distribution found").
- Lu's VM ALSO has **Python 3.11.14 at `/home/lumi/.local/bin/python3.11`** → use THIS for the venv. No sudo/apt needed.

## Install (verified working)
```bash
PY311=/home/lumi/.local/bin/python3.11
$PY311 -m venv ~/redenv311          # fresh path — avoids rm -rf approval gate
source ~/redenv311/bin/activate
pip install -U pip
pip install -U "Red-DiscordBot[sqlite]"   # pulls discord-py 2.7.1
redbot --version                            # Red-DiscordBot 3.5.24
```
Use a **fresh venv path** (e.g. `~/redenv311`), NOT `rm -rf ~/redenv` then rebuild — the `rm` trips the destructive-command approval prompt and blocks unattended runs. A new path is non-destructive.

## Instance Setup (prompt order MATTERS)
Red 3.5.24's `redbot-setup` prompt order is:
1. instance name
2. data directory
3. **confirm [Y/n]**  ← easy to miss
4. storage backend (1=JSON, 2=Postgres; ENTER=JSON default)

Narusya's original `red_setup.sh` fed `JSON` at step 3 (confirm), which ABORTS setup. Correct non-interactive sequence:
```bash
printf 'lured\n%s\ny\n\n' "$HOME/lu-reddata" | redbot-setup
#        name   datadir  confirm  backend(ENTER=JSON)
```
Instance `lured`, data at `~/lu-reddata`, **JSON backend**.

## CRITICAL FIX: discord.py 2.7.x Shutdown Crash
**Symptom:** `--dry-run` (or any clean exit) crashes with:
```
File ".../discord/shard.py", line 557, in _close
    self.__queue.put_nowait(EventItem(EventType.clean_close, None, None))
AttributeError: 'Red' object has no attribute '_AutoShardedClient__queue'
```
**Root cause:** NOT in `redbot/core/bot.py` (where Narusya's doc pointed). It's in **discord.py's own `shard.py`** — `AutoShardedClient._close()` calls `self.__queue.put_nowait(...)`, but discord.py 2.7.x no longer creates that private attribute. Red's `bot.py close()` just calls `super().close()`, which lands in discord's shard.py. Patching bot.py does NOT catch it.

**Fix:** guard the `put_nowait` in `discord/shard.py` (see `references/discord-py-shutdown-crash.md` for exact diff):
```python
            await self.http.close()
            if hasattr(self, "_AutoShardedClient__queue"):
                self.__queue.put_nowait(EventItem(EventType.clean_close, None, None))
```
**Verify:** after patch, `redbot lured --dry-run </dev/null` must reach the token prompt and shut down with `cleaning up a bit more` — and `grep` for `has no attribute` must return nothing.

## Gateway Safety (verify on every launch)
- Red dies pre-connect during `--dry-run` — safe. A LIVE launch with a token briefly contests the Discord session.
- After ANY Red launch/relaunch: confirm the Hermes gateway is still ALIVE (`pgrep -af hermes | grep gateway`). If it drops, kill Red instantly.
- One calm supervised launch, then verify. Don't chaotically relaunch 5×.

## Token & Collision Handling
- Create a **fresh Discord application** for Red (separate from aether's, separate from Adora's Hermes token).
- Bot tab → **enable MESSAGE CONTENT INTENT** (required to read messages; the one everyone misses). Server Members Intent optional.
- OAuth2 → URL Generator → scopes `bot` → perms: Send Messages, Read Message History, Attach Files, Add Reactions, Embed Links, Use External Emojis. Invite to the guild.
- Write the token to a secret file (chmod 600), **never post it in chat**.
- **Distinct prefix** (e.g. `[p]`) so Red never double-fires with Hermes (mention/allowlist) or aether.
- Run under a supervisor (systemd user service or nohup) so it survives reboots.

## Verification (before any live token)
1. `redbot --version` → 3.5.24
2. `redbot lured --dry-run </dev/null` → reaches token prompt, clean shutdown, no AttributeError
3. Gateway still alive after any live test

## Pitfalls
- **Python 3.12 too new** — use the 3.11 binary at `/home/lumi/.local/bin/python3.11`.
- **`rm -rf` venv trips approval** — use a fresh path instead.
- **`red_setup.sh` prompt-order bug** — confirm step comes BEFORE backend; feed `y` then empty ENTER.
- **Wrong patch location** — fix is in `discord/shard.py`, not `redbot/core/bot.py`.
- **Shared-token sharding** — avoid; use a separate bot token.
- **pgrep pattern too specific** — use `pgrep -af hermes | grep gateway`, not the exact `hermes_cli.main gateway run` string.

## Scope Rule
Red = community cogs. Hermes = daemon/relationship core. Don't duplicate.

## Support files
- `references/discord-py-shutdown-crash.md` — exact crash transcript + patch diff + verify command.
- `scripts/red_install_setup.sh` — corrected non-interactive install + instance setup + optional shard.py patch.
