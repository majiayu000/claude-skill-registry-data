---
name: granola-sync
description: >-
  Pull fresh meetings from Granola (summaries, transcripts, participants) into an Obsidian vault
  over the official API. Incremental and idempotent by note id and updated_at, so re-runs make
  no duplicates. Triggers: "/granola-sync", "pull granola", "refresh meetings".
license: MIT
---

OBJECTIVE: Incrementally pull fresh meetings/calls from Granola into the vault (summary + full transcript + participants + a calendar match), on demand. Idempotent: the script downloads only what is new or changed (state.json: note id → updated_at).

CONTEXT:
- Transport: the official Granola public API `https://public-api.granola.ai/v1` (List Notes / Get Note ?include=transcript; page_size <= 30; 5 rps). Key: `%WORKDIR%\secrets\granola.env` (account owner.calendar@example.com, Workspace2, scopes personal+public, created 2026-07-02).
- ⛔ The MCP transport is NO LONGER used for syncing (browser OAuth, it dies after ~10 days) — only for interactive questions, and only if re-authorized.
- Engine (all the logic lives there, this skill is a thin wrapper): `$IMPORTS_ROOT/granola/granola_pull.py`. The same script does both backfill and increment.
- Home for notes: `$OBSIDIAN_VAULT/04-Projects/granola-meetings/` (auto_generated: true — never hand-edit, they get overwritten). Raw JSON: `_imports\granola\raw\`. Nightly task log: `_imports\granola\pull.log`.
- ⚠️ Granola does NOT start recording by itself: it records only when a human opens the note or clicks the notification. "The app is running" is not "it is recording".

STEPS:
1. BACKUP FIRST ([[vault-backup-rule]]): `python $IMPORTS_ROOT/vault_backup.py` BEFORE running anything.
2. Run it: `python $IMPORTS_ROOT/granola/granola_pull.py` (options: `--dry` to count without writing, `--limit N` to cap).
3. Read the stdout counters: `DONE new=X updated=Y errors=Z state_total=N`. errors>0 → look into it; usually network or 429 (the script retries by itself).
4. If new>0 — report the list of fresh meetings (titles/dates from the state or the new files).
5. Distill (if new>0): `python $IMPORTS_ROOT/granola/call_distill.py` — it breaks each new call into Commitments/Facts/Objections/Alpha with quotes → `04-Projects\granola-meetings\_distilled\` + `commitments.jsonl`. Counters: `DONE distilled=M commitments=C errors=Z`. (The nightly twin is the "Granola Call Distill" task at 03:50; it also eats the Fireflies raw files.)
6. The RAG reindex picks it up overnight ([[reindex-routine]]); after the FIRST big backfill, run `python $IMPORTS_ROOT/brain_embed_update.py` manually. ⚠️ `_distilled` is not in the curated index yet (04-Projects is the evidence layer) — closed by task RUSL-1 (`layer: essence`).

CONSTRAINTS:
- Windows cp1252: do not print non-ASCII to stdout (the script is already ASCII-only).
- INCREMENTAL ONLY — never delete state.json (it would re-download everything).
- Provenance: origin: mixed, authored_by: hybrid — NOT #anton-original (someone else's speech).
- Tier-2: nothing goes outside; API reads and vault writes only.
- A 401/403 from the API means the key was revoked: create a new one in the Granola desktop app (Settings → Connectors → Personal API keys, scopes Personal+Public) and update granola.env. I can do this myself through computer-use (verified 2026-07-02).

OUTPUT: the new/updated/errors counters + the period; if empty, "no new meetings". Finish with an "In plain words" recap.

RELATION (do not duplicate): the Fireflies rail (auto-recording, real speaker names) = skill [[fireflies-sync]]; access and history = memory [[granola-mcp-integration]]; the architecture decision = the vault note `decision-granola-extraction-official-api`; the post-call follow-up SOP = memory [[call-followup-group-sop]] (a separate pipeline); the FAAA sync goes the other way (finished follow-ups out of Telegram).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
