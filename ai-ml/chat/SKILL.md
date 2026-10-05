---
name: chat
description: >-
  Find a Telegram chat, group or channel by name and return its numeric id and t.me link from a
  local index, with no live crawl. Also answers which groups you share with a person or company.
  This is the chat lane, not people search. Triggers: "/chat <query>", "find the <X> chat",
  "chat id for <X>".
license: MIT
---

# /chat — instant Telegram chat lookup

Anton's pain: "find chat X" used to mean 20–60 min crawling the live dialog list.
The chat's `telegram_id` + link already live in `chats.db` (built from the CRM
`tg_entities` dump — the same extraction the CRM's mtproto-api does). Look it up,
get the id, then operate the chat directly via the Telegram MCP.

## Rule (always)
When you need to act on "some chat by name", FIRST query the local index — never
crawl the live dialog list blind. Memory: [[telegram-chat-index]].

## Lookup — `find_chat.py`
```
cd $IMPORTS_ROOT/dialogs
PYTHONUTF8=1 python find_chat.py <query words>      # chats first, then people
PYTHONUTF8=1 python find_chat.py <query> --all      # include user DMs
PYTHONUTF8=1 python find_chat.py <query> --limit 80
```
Prints `[TYPE] telegram_id  name  t.me-link (+members)`. Matching reuses
`..\namesearch\name_norm.py` so wrong-layout (`dbrnjh`) / translit / typos still hit.
⚠️ ALWAYS `PYTHONUTF8=1` (else cp1252 crash). The `???` in console = ASCII echo only;
the DB stores proper UTF-8 — read it programmatically when you need the real title.

## "Common groups with a person / company" — `common_groups.py`
```
PYTHONUTF8=1 python common_groups.py @handle [--account corp_acct]
PYTHONUTF8=1 python common_groups.py "Firstname Lastname"
PYTHONUTF8=1 python common_groups.py <telegram_id>
```
Lists groups where one of OUR accounts sits alongside that person (ours/theirs +
which account + link). COVERAGE: rosters are full for small/curated groups, partial
for big public ones → for an authoritative per-person answer use the live MCP
`get_common_chats(user, account)`.

## Visual (Anton works by eye)
`_Dashboards\Telegram-Groups.html` — all chats, filter by account / ours-vs-theirs /
topic / value, search, per-group sub-classification.

## Freshness
`chats.db` backbone = CRM dump (refreshed by the `telegram-chat-index-refresh`
routine that appends live `list_chats` from Anton's accounts via `refresh_chats.py`).
If a brand-new chat is missing, run that refresh or fall back to live `search_dialogs`.

## Build / rebuild (rarely)
`build_chats_db.py` → index · `build_group_graph.py` → accounts/members/ours-theirs ·
`build_group_digest.py` + Sonnet classifier → `group_class` · `build_groups_dashboard.py`.
All under `$IMPORTS_ROOT/dialogs/`. See memory [[telegram-chat-index]].


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
