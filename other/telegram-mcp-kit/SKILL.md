---
name: telegram-mcp-kit
description: "Install and wire a Telegram MCP server (chigwell/telegram-mcp, MTProto user account, not a bot) so Claude Code, Claude Desktop, Codex or any MCP client can read your chats and send replies. Use when connecting an agent to a personal Telegram account, applying the kit patches (shared SSE daemon, search_dialogs, multi-account), generating a session string, or debugging file tools that silently refuse, orphaned uv processes, database is locked, AuthKeyDuplicated or flood-wait."
license: Apache-2.0
---

# telegram-mcp-kit

Connect an agent to the user's own Telegram account in about 15 minutes, on top of the upstream server [`chigwell/telegram-mcp`](https://github.com/chigwell/telegram-mcp). The full step-by-step agent prompt is `PROMPT.md` in this repo; this skill is the short form.

## Steps

0. Check `git` and `uv` (`uv --version`); install `uv` if missing.
1. Ask the user for `api_id` and `api_hash` (from https://my.telegram.org, API development tools). Treat `api_hash` like a password.
2. `git clone https://github.com/chigwell/telegram-mcp.git <MCP_DIR>` then `uv sync`.
3. Patches are pinned to upstream `a008ac2`: `git checkout a008ac2`, then `git apply <KIT_DIR>/patches/0001-transport-sse-env.patch` and `0002-extra-tools-multiaccount.patch`. On latest upstream skip `0001` (transport is env-selectable natively) and try `git apply -3` for `0002`; report conflicting hunks instead of skipping them.
4. Session string: the user runs `uv run session_string_generator.py` in a real interactive terminal (phone + code or QR). You cannot do this step for them.
5. Create a media folder and pass it as a **trailing positional argument** to `main.py`. Without it `download_media` and `send_file` silently refuse.
6. Register with the venv python directly, not `uv run` (on Windows `uv run` leaks orphan processes):
   ```
   claude mcp add telegram --scope user --env TELEGRAM_API_ID=<id> --env TELEGRAM_API_HASH=<hash> --env TELEGRAM_SESSION_STRING=<string> -- <MCP_DIR>/.venv/Scripts/python.exe <MCP_DIR>/main.py <MEDIA_DIR>
   ```
   Optional read-only default: `--env TELEGRAM_EXPOSED_TOOLS=read-only`.
7. Restart the session, call `get_me`, then `list_chats` with limit 5, and report both.
8. Many parallel sessions on one machine: run one shared daemon (`MCP_TRANSPORT=sse`, `MCP_HOST=127.0.0.1`, `MCP_PORT=8765`) and register `{"type":"sse","url":"http://127.0.0.1:8765/sse"}`. Use the watchdog in `daemon/` (two probes with a pause, evidence before restart); a naive restart blinds every live session.

## Rules

- The session string is full account access. Keep it only in the MCP registration env; never in git, logs, synced folders or the final report. Revoke in Telegram, Settings, Devices.
- Never copy one session string to a second machine: `AuthKeyDuplicated` drops both. Each machine logs in once.
- `database is locked` means another copy is running (often an orphan). Kill it; do not regenerate the session.
- Throttle bulk reads and downloads; flood-wait locks are real.
- Private groups have no @username: use `search_dialogs` (patch `0002`) and match chats by numeric ID.

More: `README.md`, `PROMPT.md`, `docs/GOTCHAS.md`, `docs/SECURITY.md`, `daemon/README.md`.

<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/[id]) - X [[аккаунт]](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
