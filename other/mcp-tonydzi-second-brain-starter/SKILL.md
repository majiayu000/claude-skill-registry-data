---
name: mcp
description: >-
  Health-check the connected MCP servers and scout new ones: the safe pre-flight before
  integration work, plus a connector finder. Read-only by default. Triggers: "/mcp", "/mcp
  health", "/mcp discover <need>", "which MCP servers are alive", "find an MCP for <X>".
license: MIT
---

# /mcp — connector health-check & discovery

> 🧒 When reporting to Anton end with a child-simple "In plain words" recap. (memory `eli5-always`)

Two jobs: (1) **health** — is each MCP server alive & authorized? (2) **discover** — is there an MCP for a need Anton has? Full rules + the Telegram landmine = memory [[mcp-health-check]].

## health (READ-ONLY, safe order)
1. **In-session tool check FIRST (zero-risk)** — if a server's tools are present in the session, call ONE cheap read tool to confirm auth + liveness:
   - Telegram → `mcp__telegram__get_me` (expect Tony / @work_acct_a).
   - WhatsApp → `mcp__whatsapp__get_my_profile`. n8n → `mcp__n8n__n8n_health_check`. Google Drive/Calendar → a list call. MongoDB → `list-databases`.
   This uses the ALREADY-RUNNING server — no second client.
2. **Only if a server's tools are ABSENT** → it didn't load. Diagnose registration (`$USERPROFILE/.claude.json` mcpServers) + processes, then reconnect.
3. **⚠️ TELEGRAM LANDMINE:** do NOT run `claude mcp list` or spawn a Telethon client as a casual check — a 2nd client on the same StringSession triggers **AUTH_KEY_DUPLICATED** and logs the account out. Prefer in-session `get_me`. Use `claude mcp list` only when the server clearly isn't loaded.
4. **Zombie/leak watch (Windows):** stdio MCPs launched via `uv run`/`npx` can orphan → prefer the direct interpreter as `command`; the "Telegram MCP Janitor" task (every 15 min) kills true orphans (no live `claude.exe` ancestor). Don't guess a hung process — verify with facts (alive? progress mtime? elapsed?).

## discover
Use the registry tools: `mcp__mcp-registry__suggest_connectors` (for a stated need), `mcp__mcp-registry__search_mcp_registry`, `mcp__mcp-registry__list_connectors` (what's already available). Rank by: does it solve a REAL recurring need? subscription/local (free) over paid ([[prefer-included-limits-before-paid-api]])? does a stdio server risk Windows orphaning? Propose, don't auto-install — wiring a new server = Anton's call.

## Safety
- Health = read-only, run anytime (this is the standing pre-flight before Telegram/integration work).
- Reconnecting, editing `.claude.json`, installing a new server = pause + confirm.

## Output
Per-server 🟢/🔴 (alive + authed) + any down one with its fix command; for discover, a short ranked shortlist. Then 🧒 recap. Setup detail: [[telegram-mcp-connector]], [[whatsapp-mcp-integration]], [[n8n-stack]].


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
