---
name: faaa-sync
description: >-
  Pull fresh follow-up call notes from a dedicated Telegram group into the CRM layer of a vault.
  Incremental and idempotent by message id, safe to re-run, and the manual counterpart of the
  weekly scheduled job. Triggers: "/faaa-sync", "pull the follow-up notes".
license: MIT
---

OBJECTIVE: Pull fresh FAAA follow-up call notes from the operator's Telegram group and incrementally ingest them into the Obsidian Platinum-CRM, on demand. Fully idempotent (dedup by Telegram message id) — safe to re-run, never creates duplicates. Identical pipeline to the weekly task `faaa-weekly-sync`; the only difference is that this fires when the operator asks.

CONTEXT:
- Source: Telegram supergroup "CALLS — FOLLOW-UPS MAIN (call summaries ONLY and NOTHING ELSE)", chat_id = <YOUR_CHAT_ID> (read via the Telegram MCP; logged-in account @work_acct_a).
- Each substantive message is a call follow-up summary (in any language): starts with "Follow-up of our call 👣" / "Follow-Up 👣", has a "Participants:" / "Meeting participants:" line with the lead's @handle, bullets, and "Agreements 🤝". Spam/promos + voice-note ops messages also appear — the scripts' triage filters them out (only real follow-ups become lead cards).
- CRM vault: $OBSIDIAN_VAULT/04-Projects/crypto/Platinum-CRM/leads/. Scripts + checkpoints: $IMPORTS_ROOT/.
- Watermark (last imported msg id) = max integer id in $IMPORTS_ROOT/faaa-archive.jsonl.

STEPS:
1. BACKUP FIRST (vault-backup-rule): run the vault backup (python $IMPORTS_ROOT/vault_backup.py, or the obsidian-backup skill) BEFORE any write. This step renders cards into the live vault — never skip the backup.
2. Health-check the Telegram MCP: call get_me. If it errors, STOP and report "Telegram MCP is down — skipped" (do not proceed).
3. Watermark: read the max integer message id in $IMPORTS_ROOT/faaa-archive.jsonl (python -c that loads the jsonl, prints max int id, ASCII only). Call it WM.
4. Pull history: call the Telegram MCP get_new_messages_since for chat_id <YOUR_CHAT_ID> with min_id = WM, limit 200 (or get_history limit 200 then filter id > WM). If the oldest returned id is still > WM, fetch again with a larger window to cover the whole gap.
5. If NO message has id > WM: STOP and report "No new FAAA follow-ups." Do nothing else.
6. Write the new messages (id > WM) to $IMPORTS_ROOT/faaa/faaa-new-msgs.json as:
   {"chat_id":<YOUR_CHAT_ID>,"watermark":WM,"results":[{"id":<int>,"sender":<from>,"date":<iso8601>,"text":<FULL verbatim text>,"media":<media type if any>}]}
   Include the COMPLETE verbatim text of each message — never truncate or paraphrase (faithful raw import).
7. Run: python $IMPORTS_ROOT/ingest_faaa_live.py
   (classifies follow-ups, regex-extracts the lead @handle from the Participants line, team-filters, dedups vs existing leads by handle → writes faaa\live_bundles.json [NEW leads] and faaa\live_appends.json [calls for EXISTING leads]; prints a summary).
8. Read $IMPORTS_ROOT/faaa/live_bundles.json. For EACH new lead, synthesize a CRM record GROUNDED ONLY in that lead's call text (never invent), an object with EXACTLY these keys: lead_key (echo unchanged), name, company, role, country, category (one of investor/fund/vc/advisor/project/founder/exchange/service/media/kol/dev/other), status (one of new/negotiating/interested/partner/advisor/stale/declined), what_they_do, what_they_want, what_we_offered, agreements, outcome, summary (2-4 sentences), tags (3-7 kebab-case), lang (ru/en). Use "" for unknown fields. Write the array to $IMPORTS_ROOT/faaa/live_synth.json via the Write tool (UTF-8, real Cyrillic, NO byte-order-mark). If live_bundles.json is an empty array, write [] there.
9. Run: python $IMPORTS_ROOT/render_live.py
   (creates lead cards in leads\<year>\ + person overlays in 07-People\ + day-ledger entries for NEW leads; APPENDS fresh calls to existing leads' cards; appends rows to faaa-archive.jsonl to advance the watermark; tags everything #top-lead).
10. Run: python $IMPORTS_ROOT/build_combined_moc.py  (refresh _Platinum-CRM-MOC counts).
11. Validate: python broken-link check (basename resolution vs all vault .md basenames) over the newly created/changed cards — expect 0 broken. If any broken, report them.

CONSTRAINTS:
- WINDOWS cp1252: never print Cyrillic to stdout in python (it crashes) — write results to UTF-8 files and Read them; keep all python stdout ASCII (counts/slugs only).
- INCREMENTAL ONLY — do NOT trigger any full FAAA/CRM rebuild or re-render of the whole leads\ folder (that could change slugs and break the 07-People links).
- Provenance on everything: origin: mixed, authored_by: hybrid — NEVER tag #anton-original (these are records of other people's pitches).
- Team handles (@work_acct_a, @personal_acct, @corp_acct*, @owner_alt*, @Madina*) are NOT leads — the scripts already exclude them.

OUTPUT / SUCCESS CRITERIA: Report: number of new lead cards created, calls appended to existing leads, the new watermark (max id in faaa-archive.jsonl), and confirm 0 broken links. If nothing was new, just report that. End every reply to the operator with a 🧒 In plain words recap.

RELATION TO OTHER ENTRIES (do not duplicate):
- Scheduled twin: $USERPROFILE/.claude/scheduled-tasks/faaa-weekly-sync/SKILL.md (Mondays 09:09) — same scripts.
- Full first-time import + analytics history: memory [[platinum-crm-import]].
- For re-importing a whole EXPORTED chat file (not the live group), use the telegram-reimport skill instead.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
