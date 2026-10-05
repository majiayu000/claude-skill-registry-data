---
name: chatgpt-sync
description: >-
  Pull fresh ChatGPT conversations into an Obsidian vault on demand, the manual twin of the
  nightly job. Incremental and idempotent by conversation id: never clobbers enriched notes,
  never duplicates. Triggers: "/chatgpt-sync", "pull chatgpt", "sync chatgpt chats".
license: MIT
---

OBJECTIVE: Pull ChatGPT conversations updated since the vault's newest note and fold them into the Obsidian vault (notes + MOC + SQLite), on demand. Idempotent. IDENTICAL pipeline to the scheduled `ChatGPT Nightly Sync`; the only difference is this fires when the operator asks.

CONTEXT (canon: memory [[chatgpt-export-pipeline]]):
- ChatGPT chats are NOT on disk - pulled via `/backend-api` with a bearer token in `$IMPORTS_ROOT/chatgpt/secrets/bearer.txt`. The cookie/bearer lives ~1-2 weeks; there is NO refresh-token, so it must be hand-refreshed periodically (this is why the flow is semi-auto, not a blind cron).
- ⚠️ GRABLI: the detail endpoint `/conversation/{id}` 403s with the bearer alone - `incremental_pull.py` already sends the required headers (`OAI-Device-Id`, `oai-language`, Referer/Origin). The LIST endpoint works without them.
- Single source of truth = `$IMPORTS_ROOT/chatgpt/nightly_sync.py` - it chains: vault_backup (pre) -> incremental_pull.py CUTOFF -> chatgpt_export_to_vault.py --zip -> copy staging->vault (NEVER overwrites a concept-enriched note, only `related_concepts: []`) -> build_chatgpt_moc.py -> vault_backup (post). CUTOFF = newest vault note date - 1 day (so a missed day leaves no gap).
- Vault home: `$OBSIDIAN_VAULT/01-Conversations/ChatGPT/conversations/` + `_ChatGPT-MOC.md`. SQLite: `_imports\chatgpt\chatgpt_conversations.db`. Freshness heartbeat: `_imports\chatgpt\_freshness.json`.

STEPS:
1. Run the orchestrator (it does backup + pull + fold + MOC + backup itself):
   `cmd.exe /c "$IMPORTS_ROOT/chatgpt/nightly_sync.cmd"`  (or `python $IMPORTS_ROOT/chatgpt/nightly_sync.py`).
   Run it foreground; it logs to `_imports\chatgpt\_nightly_sync.log`.
2. Read the tail of `$IMPORTS_ROOT/chatgpt/_nightly_sync.log` for the result line(s): `copy: +N new, ~M refreshed, K enriched-preserved` and `nightly_sync DONE: +N new chats`.
3. Interpret the exit code:
   - **0** = success (even +0 new is fine - nothing new to pull).
   - **7** = PULL FAILED, token dead/expired. nightly_sync.py now **self-heals this automatically** (calls `token_heal.py` on exit 7 → re-mints the bearer from the long-lived session cookie → retries the pull), so a bare exit 7 in the log usually means the automatic heal ALSO failed. **DEFAULT ACTION: run skill `/chatgpt-token-heal`** (root-cause fix: session cookie → fresh bearer, 0 browser, 0 LLM; falls back to Chrome cookie re-harvest only if the cookie itself died). Do NOT hand-do the old Chrome Blob-download dance — that is the fallback the skill handles. ESCALATE to the operator (D-type) ONLY if `/chatgpt-token-heal` reaches L3 (Chrome logged out of chatgpt.com on the hub).
   - **8** = staging build failed (rare) → report the log tail, do not guess.
4. (optional) Reindex for RAG so new notes are searchable now: `python $IMPORTS_ROOT/brain_embed_update.py --wait-gpu 10` - OR just rely on the nightly Brain Reindex @04:00 (skip if the GPU is busy with a parallel session).
5. Report: how many new chats folded, the newest note date, freshness FRESH/STALE (read `_freshness.json`), and BROKEN-link status if a validate ran. End with a 🧒 In plain words recap (messages TO the operator only).

CONSTRAINTS:
- ANTI-RECENTS: when hunting for ONE specific chat by hand on chatgpt.com, never conclude "the chat does not exist" from the recents list. Use the built-in SEARCH by keyword + check Projects/archive + confirm the active account by email. The scripted path (`/backend-api` LIST via `incremental_pull.py`) pulls ALL chats and is more reliable than eyeballing the page. Canon: memory [[web-ui-search-not-recents]] (incident 2026-07-23).
- DON'T duplicate logic - ALWAYS go through `nightly_sync.py`; never re-implement the pull/convert here. If `incremental_pull.py` or the converter needs a change, edit THOSE files (single source), not this skill.
- AK-47: this skill is just this SKILL.md (a procedure). No new server/DB/service.
- WINDOWS cp1252: the log may show mojibake for Cyrillic titles - cosmetic only; the vault notes are correct UTF-8. Don't "fix" by re-encoding the notes.
- Token is a secret: never print it, never paste it into a message/vault/always-loaded layer (credential-store anti-leak boundary).
- Backup-before-write is already inside nightly_sync.py (vault_backup pre+post) - don't double-run it.

RELATION (do not duplicate):
- Scheduled twin: Windows task `ChatGPT Nightly Sync` (~02:00) + watchdog `ChatGPT Vault Freshness (Daily)` (~10:00, pings the operator on STALE via Telegram). Same scripts. **Live on the always-on HUB `HUB-1` since 2026-06-25** (moved off the laptop HP17 so sync no longer depends on the laptop waking; may still be duplicated on HP17 as backup — idempotent, a double run just sees +0).
- Canon + gotchas + token how-to: memory [[chatgpt-export-pipeline]].
- Sibling sync skills: [[health-sync]], [[faaa-sync]], [[claudeai-sync]], [[whatsapp-sync]].


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
