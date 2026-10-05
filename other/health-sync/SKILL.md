---
name: health-sync
description: >-
  Pull fresh messages from a set of health-related Telegram chats (medicine, supplements,
  longevity, fasting) into an Obsidian vault. Incremental and idempotent by message id, and the
  manual counterpart of the weekly job. Triggers: "/health-sync", "pull the health chats".
license: MIT
---

OBJECTIVE: Pull fresh messages from Anton's 7 Telegram health chats and incrementally fold them into the Obsidian vault (day-ledgers + atomic notes + MOC + dashboard), on demand. Fully idempotent (dedup by Telegram message id). Identical pipeline to the weekly task `health-weekly-sync`; the only difference is this fires when Anton asks.

CONTEXT:
- 7 source chats (registry: $IMPORTS_ROOT/health/chats.json). ALWAYS pull with the Telegram MCP using account="default" (@work_acct_a); the other account errors (GEN-ERR-862) on these basic groups.
  - <YOUR_CHAT_ID>  medicine-health-main
  - <YOUR_CHAT_ID>  blood-pressure
  - <YOUR_CHAT_ID>  longevity-weightloss-fasting
  - <YOUR_CHAT_ID>  vitamins-bads
  - <YOUR_CHAT_ID>  healing-head
  - <YOUR_CHAT_ID>  medicine-for-mind
  - <YOUR_CHAT_ID> fasting-community
- Vault home: $OBSIDIAN_VAULT/01-Conversations/Telegram/Health/ (per-chat folders + posts\ + _Health-MOC.md). Dashboard: _Dashboards\Health-Dashboard.html. Scripts + watermarks + raw: $IMPORTS_ROOT/health/.
- Watermark per chat (last imported msg id) = $IMPORTS_ROOT/health/watermarks.json (keyed by chat_id as string).
- Provenance: health data is NOT private (Anton's explicit instruction) — do NOT tag #private. Anton's own messages -> origin: anton (+ #anton-original); forwarded -> origin: external (+ forwarded_from); community members (fasting-community) -> origin: external.

STEPS:
1. Health-check the Telegram MCP: call mcp__telegram__get_me. If it errors, STOP and report "Telegram MCP is down — skipped".
2. Read watermarks: load $IMPORTS_ROOT/health/watermarks.json -> {chat_id: max_msg_id}.
3. For EACH of the 7 chats: call mcp__telegram__get_new_messages_since(chat_id=<id>, min_id=<watermark for that id>, account="default") (or get_history limit 100 then keep id > watermark). Collect the message objects with id > watermark.
4. For each chat, write its new messages (id > watermark) VERBATIM to $IMPORTS_ROOT/health/raw/_new/<slug>.json as a JSON array of the raw message objects (every field: id, sender, sender_id, date, out, text, media, forwarded, reply_to, grouped_id, pinned, edited, action). NEVER truncate or paraphrase text. If a chat has no new messages, write [] (or skip its file).
5. Run: python $IMPORTS_ROOT/health/merge_health_raw.py  (merges raw\_new\* into raw\*, dedup by id; writes last_merge.json).
6. Read $IMPORTS_ROOT/health/last_merge.json. If total_new == 0: STOP and report "No new health messages." Do nothing else.
7. BACKUP FIRST (vault-backup-rule): run python $IMPORTS_ROOT/vault_backup.py. If it reports a git index.lock from a concurrent process, note it but proceed — the import is purely ADDITIVE to the Health folder (reversible by deleting new files); never force-remove another process's lock.
8. Run: python $IMPORTS_ROOT/health/run_health_pipeline.py  (parse -> generate -> moc -> dashboard -> validate; expects BROKEN=0).
9. Robocopy staging into the vault (PowerShell):
   robocopy "$IMPORTS_ROOT/health/staging" "$OBSIDIAN_VAULT/01-Conversations/Telegram/Health" /E /XO /NFL /NDL /NJH /NJS
   (exit code 0-7 = success.)
10. Reindex for RAG (so the new notes are searchable): python $IMPORTS_ROOT/brain_embed_update.py --wait-gpu 10  (or rely on the nightly Brain Reindex at 04:00 if the GPU is busy).
11. Report: new messages per chat, new atomic notes / ledgers created, the new watermarks (max ids), and confirm BROKEN=0. End with a 🧒 In plain words recap (messages TO Anton only).

CONSTRAINTS:
- WINDOWS cp1252: never print Cyrillic to python stdout (crashes) — write results to UTF-8 files and Read them; keep python stdout ASCII (counts/slugs only).
- INCREMENTAL ONLY by design, but the pipeline is a full deterministic rebuild of staging from the archive (idempotent) + robocopy /XO — it never duplicates and never deletes existing vault notes.
- Raw files may have a UTF-8 BOM (the scripts read utf-8-sig) — fine.
- Faithful raw import: write message text VERBATIM into raw\_new files. The atomic-note bodies are the raw text; do not summarize.

RELATION (do not duplicate):
- Scheduled twin: $USERPROFILE/.claude/scheduled-tasks/health-weekly-sync/ (Mondays) — same scripts.
- First-time backfill design + counts: memory [[health-import]].
- Sibling pattern: [[faaa-sync]] (CRM calls). Reuses the FAAA weekly-sync architecture.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
